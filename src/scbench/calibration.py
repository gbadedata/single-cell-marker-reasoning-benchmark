from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from datetime import datetime, timezone


DIFFICULTY_RULES = {
    "too_easy": "Most solvers answer correctly with shallow marker lookup or obvious label matching.",
    "target": "Solver must combine marker evidence, ambiguity handling, and biological reasoning.",
    "too_hard": "Task is under-specified, ambiguous beyond reasonable evidence, or requires unavailable domain knowledge.",
    "too_ambiguous": "Multiple answers are defensible but the validator expects only one narrow answer.",
}


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2))


def create_calibration_log_template(
    output_path: str = "benchmark_tasks/calibration_logs/calibration_log_template.json",
) -> dict[str, Any]:
    payload = {
        "project": "single-cell-marker-reasoning-benchmark",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": (
            "Template for recording benchmark task calibration against human solvers, "
            "LLMs, or other model systems."
        ),
        "difficulty_categories": DIFFICULTY_RULES,
        "calibration_fields": {
            "task_id": "Unique benchmark task identifier.",
            "task_type": "hidden_cluster_annotation | marker_contradiction_detection | masked_marker_recovery",
            "solver_type": "human | LLM | script | other",
            "solver_name": "Name/version of solver, if applicable.",
            "attempt_number": "Integer attempt number.",
            "solver_answer_summary": "Short summary of solver answer.",
            "score": "Numeric validator score.",
            "passed": "Boolean correctness from validator.",
            "failure_mode": "marker_lookup_only | wrong_label | missing_uncertainty | weak_rationale | ambiguity_failure | unavailable_information | other",
            "difficulty_assessment": "too_easy | target | too_hard | too_ambiguous",
            "revision_required": "Boolean.",
            "revision_plan": "How the task should be changed.",
            "reviewer_notes": "Human reviewer comments.",
        },
    }

    write_json(output_path, payload)
    return payload


def create_initial_calibration_review(
    output_path: str = "benchmark_tasks/calibration_logs/initial_task_difficulty_review.json",
) -> dict[str, Any]:
    review = {
        "project": "single-cell-marker-reasoning-benchmark",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "review_scope": "Initial human design review before external solver calibration.",
        "important_limitation": (
            "This is not yet empirical frontier-model calibration. It is a design-stage "
            "difficulty review. Real calibration requires running tasks against one or more "
            "human or model solvers and recording scored attempts."
        ),
        "task_type_reviews": [
            {
                "task_type": "hidden_cluster_annotation",
                "expected_count": 9,
                "initial_difficulty": "medium",
                "risk": "Some clusters may be too easy because canonical markers are visible.",
                "planned_revision_strategy": (
                    "Increase difficulty by masking canonical markers or requiring uncertainty-aware annotation."
                ),
            },
            {
                "task_type": "marker_contradiction_detection",
                "expected_count": 2,
                "initial_difficulty": "hard",
                "risk": "Ambiguity may be underspecified unless supporting gene evidence is required.",
                "planned_revision_strategy": (
                    "Require contradiction type, supporting genes, and explanation of why a single-label answer is insufficient."
                ),
            },
            {
                "task_type": "masked_marker_recovery",
                "expected_count": 5,
                "initial_difficulty": "expert",
                "risk": "Could become too hard if secondary markers are weak or non-specific.",
                "planned_revision_strategy": (
                    "Keep candidate labels visible, require uncertainty comments, and score partial gene evidence."
                ),
            },
        ],
    }

    write_json(output_path, review)
    return review


def generate_calibration_assets() -> None:
    create_calibration_log_template()
    create_initial_calibration_review()
