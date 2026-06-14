from __future__ import annotations

import json
from pathlib import Path
from typing import Any


LABEL_SYNONYMS = {
    "t cell": "T cells",
    "t cells": "T cells",
    "naive t cells": "T cells",
    "memory t cells": "T cells",
    "cd14 monocytes": "CD14+ monocytes",
    "cd14+ monocytes": "CD14+ monocytes",
    "classical monocytes": "CD14+ monocytes",
    "b cell": "B cells",
    "b cells": "B cells",
    "cytotoxic t cells": "Cytotoxic T cells",
    "cytotoxic t": "Cytotoxic T cells",
    "nk cells": "NK cells",
    "natural killer cells": "NK cells",
    "fcgr3a monocytes": "FCGR3A+ monocytes",
    "fcgr3a+ monocytes": "FCGR3A+ monocytes",
    "non-classical monocytes": "FCGR3A+ monocytes",
    "dendritic cells": "Dendritic cells",
    "dc": "Dendritic cells",
    "platelets": "Platelets",
    "platelet": "Platelets",
    "cycling cells": "Cycling cells",
    "proliferating cells": "Cycling cells",
}


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def normalize_label(label: str) -> str:
    cleaned = str(label).strip().lower()
    return LABEL_SYNONYMS.get(cleaned, str(label).strip())


def normalize_gene(gene: str) -> str:
    return str(gene).strip().upper()


def build_oracle_index(oracle_output_path: str | Path) -> dict[str, dict[str, Any]]:
    payload = load_json(oracle_output_path)
    return {item["task_id"]: item["oracle_response"] for item in payload["oracle_outputs"]}


def score_gene_overlap(
    submitted_genes: list[str],
    oracle_genes: list[str],
) -> float:
    submitted = {normalize_gene(gene) for gene in submitted_genes}
    oracle = {normalize_gene(gene) for gene in oracle_genes}

    if not oracle:
        return 0.0

    return len(submitted & oracle) / len(oracle)


def validate_hidden_cluster_annotation_answer(
    solver_answer: dict[str, Any],
    oracle_response: dict[str, Any],
) -> dict[str, Any]:
    predicted_label = normalize_label(solver_answer.get("predicted_label", ""))
    oracle_label = normalize_label(oracle_response.get("predicted_label", ""))

    label_correct = predicted_label == oracle_label

    submitted_genes = solver_answer.get("supporting_genes", [])
    oracle_genes = oracle_response.get("supporting_genes", [])
    gene_overlap_score = score_gene_overlap(submitted_genes, oracle_genes)

    rationale_present = bool(str(solver_answer.get("rationale", "")).strip())

    score = 0.0
    score += 0.6 if label_correct else 0.0
    score += 0.3 * gene_overlap_score
    score += 0.1 if rationale_present else 0.0

    return {
        "is_correct": score >= 0.75,
        "score": round(score, 3),
        "label_correct": label_correct,
        "gene_overlap_score": round(gene_overlap_score, 3),
        "rationale_present": rationale_present,
        "feedback": {
            "expected_label": oracle_label,
            "submitted_label": predicted_label,
            "expected_supporting_genes": oracle_genes,
            "submitted_supporting_genes": submitted_genes,
        },
    }


def validate_marker_contradiction_answer(
    solver_answer: dict[str, Any],
    oracle_response: dict[str, Any],
) -> dict[str, Any]:
    contradiction_correct = (
        bool(solver_answer.get("contradiction_detected", False))
        == bool(oracle_response.get("contradiction_detected", False))
    )

    submitted_type = str(solver_answer.get("contradiction_type", "")).lower()
    oracle_type = str(oracle_response.get("contradiction_type", "")).lower()

    type_keywords = [
        token
        for token in oracle_type.replace("+", " ").replace("-", " ").split()
        if len(token) >= 3
    ]

    type_overlap = any(token in submitted_type for token in type_keywords)
    rationale_present = bool(str(solver_answer.get("rationale", "")).strip())

    score = 0.0
    score += 0.5 if contradiction_correct else 0.0
    score += 0.35 if type_overlap else 0.0
    score += 0.15 if rationale_present else 0.0

    return {
        "is_correct": score >= 0.75,
        "score": round(score, 3),
        "contradiction_correct": contradiction_correct,
        "type_overlap": type_overlap,
        "rationale_present": rationale_present,
        "feedback": {
            "expected_contradiction_type": oracle_response.get("contradiction_type"),
            "submitted_contradiction_type": solver_answer.get("contradiction_type"),
        },
    }


def validate_masked_marker_recovery_answer(
    solver_answer: dict[str, Any],
    oracle_response: dict[str, Any],
) -> dict[str, Any]:
    predicted_label = normalize_label(solver_answer.get("predicted_label", ""))
    oracle_label = normalize_label(oracle_response.get("predicted_label", ""))

    label_correct = predicted_label == oracle_label

    submitted_genes = solver_answer.get("secondary_supporting_genes", [])
    oracle_genes = oracle_response.get("secondary_supporting_genes", [])
    gene_overlap_score = score_gene_overlap(submitted_genes, oracle_genes)

    uncertainty_present = bool(str(solver_answer.get("uncertainty_comment", "")).strip())
    rationale_present = bool(str(solver_answer.get("rationale", "")).strip())

    score = 0.0
    score += 0.5 if label_correct else 0.0
    score += 0.25 * gene_overlap_score
    score += 0.15 if uncertainty_present else 0.0
    score += 0.1 if rationale_present else 0.0

    return {
        "is_correct": score >= 0.75,
        "score": round(score, 3),
        "label_correct": label_correct,
        "gene_overlap_score": round(gene_overlap_score, 3),
        "uncertainty_present": uncertainty_present,
        "rationale_present": rationale_present,
        "feedback": {
            "expected_label": oracle_label,
            "submitted_label": predicted_label,
            "expected_secondary_genes": oracle_genes,
            "submitted_secondary_genes": submitted_genes,
            "masked_genes": oracle_response.get("masked_genes", []),
        },
    }


def validate_answer(
    task_type: str,
    solver_answer: dict[str, Any],
    oracle_response: dict[str, Any],
) -> dict[str, Any]:
    if task_type == "hidden_cluster_annotation":
        return validate_hidden_cluster_annotation_answer(solver_answer, oracle_response)

    if task_type == "marker_contradiction_detection":
        return validate_marker_contradiction_answer(solver_answer, oracle_response)

    if task_type == "masked_marker_recovery":
        return validate_masked_marker_recovery_answer(solver_answer, oracle_response)

    raise ValueError(f"Unsupported task type: {task_type}")
