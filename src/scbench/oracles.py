from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2))


def build_answer_index(hidden_answer_path: str | Path) -> dict[str, dict[str, Any]]:
    payload = load_json(hidden_answer_path)
    return {answer["task_id"]: answer for answer in payload["answers"]}


def oracle_hidden_cluster_annotation(
    hidden_answer_path: str = "benchmark_tasks/hidden/hidden_cluster_annotation_answers.json",
    output_path: str = "benchmark_tasks/oracle_outputs/hidden_cluster_annotation_oracle_outputs.json",
) -> dict[str, Any]:
    answers = build_answer_index(hidden_answer_path)

    oracle_outputs = []
    for task_id, answer in answers.items():
        oracle_outputs.append(
            {
                "task_id": task_id,
                "oracle_response": {
                    "predicted_label": answer["oracle_label"],
                    "supporting_genes": answer["evidence_genes"],
                    "confidence": answer["oracle_confidence"],
                    "rationale": answer["notes"],
                },
            }
        )

    payload = {"oracle_outputs": oracle_outputs}
    write_json(output_path, payload)
    return payload


def oracle_marker_contradiction(
    hidden_answer_path: str = "benchmark_tasks/hidden/marker_contradiction_answers.json",
    output_path: str = "benchmark_tasks/oracle_outputs/marker_contradiction_oracle_outputs.json",
) -> dict[str, Any]:
    answers = build_answer_index(hidden_answer_path)

    oracle_outputs = []
    for task_id, answer in answers.items():
        oracle_outputs.append(
            {
                "task_id": task_id,
                "oracle_response": {
                    "contradiction_detected": answer["contradiction_detected"],
                    "contradiction_type": answer["contradiction_type"],
                    "supporting_labels": [
                        answer["cluster_a_label"],
                        answer["cluster_b_label"],
                    ],
                    "rationale": (
                        "The task compares marker profiles from two clusters with overlapping "
                        "biological signatures. The expected answer must identify the ambiguity type."
                    ),
                },
            }
        )

    payload = {"oracle_outputs": oracle_outputs}
    write_json(output_path, payload)
    return payload


def oracle_masked_marker_recovery(
    hidden_answer_path: str = "benchmark_tasks/hidden/masked_marker_recovery_answers.json",
    output_path: str = "benchmark_tasks/oracle_outputs/masked_marker_recovery_oracle_outputs.json",
) -> dict[str, Any]:
    answers = build_answer_index(hidden_answer_path)

    oracle_outputs = []
    for task_id, answer in answers.items():
        visible_secondary_genes = [
            gene for gene in answer["full_marker_genes"]
            if gene not in set(answer["masked_genes"])
        ]

        oracle_outputs.append(
            {
                "task_id": task_id,
                "oracle_response": {
                    "predicted_label": answer["oracle_label"],
                    "masked_genes": answer["masked_genes"],
                    "secondary_supporting_genes": visible_secondary_genes[:8],
                    "uncertainty_comment": (
                        "Canonical markers were intentionally masked, so the answer should rely "
                        "on secondary marker evidence and explicitly acknowledge uncertainty."
                    ),
                    "rationale": (
                        "The oracle label is derived from the marker-based annotation table, "
                        "with canonical markers removed from the solver-facing input."
                    ),
                },
            }
        )

    payload = {"oracle_outputs": oracle_outputs}
    write_json(output_path, payload)
    return payload


def generate_all_oracle_outputs() -> None:
    oracle_hidden_cluster_annotation()
    oracle_marker_contradiction()
    oracle_masked_marker_recovery()
