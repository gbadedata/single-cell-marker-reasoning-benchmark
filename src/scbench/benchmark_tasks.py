from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def load_marker_and_annotation_tables(
    marker_table_path: str = "results/tables/cluster_marker_genes_filtered.csv",
    annotation_table_path: str = "results/tables/cluster_annotations.csv",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    markers = pd.read_csv(marker_table_path)
    annotations = pd.read_csv(annotation_table_path)

    markers["group"] = markers["group"].astype(str)
    annotations["cluster"] = annotations["cluster"].astype(str)

    return markers, annotations


def generate_hidden_cluster_annotation_task(
    markers: pd.DataFrame,
    annotations: pd.DataFrame,
    output_dir: str = "benchmark_tasks",
) -> None:
    public_tasks = []
    hidden_answers = []

    for _, row in annotations.iterrows():
        cluster = str(row["cluster"])
        marker_subset = (
            markers[markers["group"] == cluster]["names"]
            .head(8)
            .tolist()
        )

        task_id = f"task_hidden_annotation_cluster_{cluster}"

        public_tasks.append(
            {
                "task_id": task_id,
                "task_type": "hidden_cluster_annotation",
                "difficulty": "medium",
                "scientific_premise": (
                    "A PBMC single-cell cluster has been processed through a Scanpy workflow. "
                    "The solver receives filtered marker genes but not the cluster label."
                ),
                "input_given_to_solver": {
                    "cluster_id": cluster,
                    "top_filtered_marker_genes": marker_subset,
                    "candidate_labels": sorted(annotations["label"].unique().tolist()),
                },
                "question": (
                    "Infer the most likely cell-type label for this cluster and provide supporting marker evidence."
                ),
                "expected_answer_schema": {
                    "predicted_label": "string",
                    "supporting_genes": ["string"],
                    "confidence": "low|medium|high",
                    "rationale": "string",
                },
            }
        )

        hidden_answers.append(
            {
                "task_id": task_id,
                "oracle_label": row["label"],
                "oracle_confidence": row["confidence"],
                "evidence_genes": str(row["evidence_genes"]).split(";"),
                "notes": row["notes"],
            }
        )

    _write_json(Path(output_dir) / "public" / "hidden_cluster_annotation_tasks.json", {"tasks": public_tasks})
    _write_json(Path(output_dir) / "hidden" / "hidden_cluster_annotation_answers.json", {"answers": hidden_answers})


def generate_marker_contradiction_task(
    markers: pd.DataFrame,
    annotations: pd.DataFrame,
    output_dir: str = "benchmark_tasks",
) -> None:
    public_tasks = []
    hidden_answers = []

    contradiction_cases = [
        {
            "task_id": "task_marker_contradiction_cytotoxic_t_vs_nk",
            "cluster_id": "3",
            "comparison_cluster_id": "4",
            "difficulty": "hard",
            "contradiction_type": "T-cell and NK-like cytotoxic marker overlap",
        },
        {
            "task_id": "task_marker_contradiction_apc_bcell_vs_dc",
            "cluster_id": "2",
            "comparison_cluster_id": "6",
            "difficulty": "hard",
            "contradiction_type": "antigen-presentation marker overlap",
        },
    ]

    for case in contradiction_cases:
        c1 = case["cluster_id"]
        c2 = case["comparison_cluster_id"]

        markers_1 = markers[markers["group"] == c1]["names"].head(10).tolist()
        markers_2 = markers[markers["group"] == c2]["names"].head(10).tolist()

        public_tasks.append(
            {
                "task_id": case["task_id"],
                "task_type": "marker_contradiction_detection",
                "difficulty": case["difficulty"],
                "scientific_premise": (
                    "Two PBMC clusters show partially overlapping marker evidence. "
                    "The solver must identify whether the annotation is straightforward or ambiguous."
                ),
                "input_given_to_solver": {
                    "cluster_a": c1,
                    "cluster_a_markers": markers_1,
                    "cluster_b": c2,
                    "cluster_b_markers": markers_2,
                },
                "question": (
                    "Identify the likely source of marker ambiguity or contradiction between these clusters."
                ),
                "expected_answer_schema": {
                    "contradiction_detected": "boolean",
                    "contradiction_type": "string",
                    "supporting_genes": ["string"],
                    "rationale": "string",
                },
            }
        )

        hidden_answers.append(
            {
                "task_id": case["task_id"],
                "contradiction_detected": True,
                "contradiction_type": case["contradiction_type"],
                "cluster_a_label": annotations.loc[annotations["cluster"] == c1, "label"].iloc[0],
                "cluster_b_label": annotations.loc[annotations["cluster"] == c2, "label"].iloc[0],
            }
        )

    _write_json(Path(output_dir) / "public" / "marker_contradiction_tasks.json", {"tasks": public_tasks})
    _write_json(Path(output_dir) / "hidden" / "marker_contradiction_answers.json", {"answers": hidden_answers})


def generate_masked_marker_recovery_task(
    markers: pd.DataFrame,
    annotations: pd.DataFrame,
    output_dir: str = "benchmark_tasks",
) -> None:
    public_tasks = []
    hidden_answers = []

    canonical_markers_to_mask = {
        "0": {"CD3D", "CD3E", "IL7R"},
        "1": {"LYZ", "S100A8", "S100A9"},
        "2": {"MS4A1", "CD79A", "CD79B"},
        "4": {"NKG7", "GNLY", "GZMB"},
        "7": {"PF4", "PPBP"},
    }

    for cluster, masked_genes in canonical_markers_to_mask.items():
        full_markers = markers[markers["group"] == cluster]["names"].head(15).tolist()
        visible_markers = [gene for gene in full_markers if gene not in masked_genes]

        task_id = f"task_masked_marker_recovery_cluster_{cluster}"

        public_tasks.append(
            {
                "task_id": task_id,
                "task_type": "masked_marker_recovery",
                "difficulty": "expert",
                "scientific_premise": (
                    "Canonical marker genes have been deliberately removed. "
                    "The solver must infer the likely cell identity from secondary evidence."
                ),
                "input_given_to_solver": {
                    "cluster_id": cluster,
                    "visible_filtered_marker_genes": visible_markers,
                    "number_of_masked_markers": len(masked_genes),
                    "candidate_labels": sorted(annotations["label"].unique().tolist()),
                },
                "question": (
                    "Infer the most likely cell-type label despite masked canonical markers."
                ),
                "expected_answer_schema": {
                    "predicted_label": "string",
                    "secondary_supporting_genes": ["string"],
                    "uncertainty_comment": "string",
                    "rationale": "string",
                },
            }
        )

        hidden_answers.append(
            {
                "task_id": task_id,
                "oracle_label": annotations.loc[annotations["cluster"] == cluster, "label"].iloc[0],
                "masked_genes": sorted(masked_genes),
                "full_marker_genes": full_markers,
            }
        )

    _write_json(Path(output_dir) / "public" / "masked_marker_recovery_tasks.json", {"tasks": public_tasks})
    _write_json(Path(output_dir) / "hidden" / "masked_marker_recovery_answers.json", {"answers": hidden_answers})


def generate_all_benchmark_tasks() -> None:
    markers, annotations = load_marker_and_annotation_tables()

    generate_hidden_cluster_annotation_task(markers, annotations)
    generate_marker_contradiction_task(markers, annotations)
    generate_masked_marker_recovery_task(markers, annotations)


if __name__ == "__main__":
    generate_all_benchmark_tasks()
