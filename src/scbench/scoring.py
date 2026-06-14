from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scbench.validators import build_oracle_index, validate_answer


ORACLE_PATHS = {
    "hidden_cluster_annotation": "benchmark_tasks/oracle_outputs/hidden_cluster_annotation_oracle_outputs.json",
    "marker_contradiction_detection": "benchmark_tasks/oracle_outputs/marker_contradiction_oracle_outputs.json",
    "masked_marker_recovery": "benchmark_tasks/oracle_outputs/masked_marker_recovery_oracle_outputs.json",
}


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2))


def load_all_oracles() -> dict[str, dict[str, Any]]:
    oracle_index: dict[str, dict[str, Any]] = {}

    for oracle_path in ORACLE_PATHS.values():
        oracle_index.update(build_oracle_index(oracle_path))

    return oracle_index


def score_solver_answers(
    solver_answer_path: str = "sample_solver_answers/sample_answers.json",
    output_path: str = "results/reports/sample_solver_score_report.json",
) -> dict[str, Any]:
    solver_payload = load_json(solver_answer_path)
    oracle_index = load_all_oracles()

    scored_answers = []

    for item in solver_payload["answers"]:
        task_id = item["task_id"]
        task_type = item["task_type"]
        solver_answer = item["answer"]

        if task_id not in oracle_index:
            scored_answers.append(
                {
                    "task_id": task_id,
                    "task_type": task_type,
                    "is_correct": False,
                    "score": 0.0,
                    "error": "No oracle response found for task_id.",
                }
            )
            continue

        result = validate_answer(
            task_type=task_type,
            solver_answer=solver_answer,
            oracle_response=oracle_index[task_id],
        )

        scored_answers.append(
            {
                "task_id": task_id,
                "task_type": task_type,
                **result,
            }
        )

    total = len(scored_answers)
    correct = sum(1 for item in scored_answers if item.get("is_correct") is True)
    average_score = (
        sum(float(item.get("score", 0.0)) for item in scored_answers) / total
        if total
        else 0.0
    )

    report = {
        "summary": {
            "total_answers": total,
            "correct_answers": correct,
            "accuracy": round(correct / total, 3) if total else 0.0,
            "average_score": round(average_score, 3),
        },
        "scored_answers": scored_answers,
    }

    write_json(output_path, report)
    return report
