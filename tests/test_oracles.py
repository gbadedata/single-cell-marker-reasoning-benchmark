from pathlib import Path
import json

from scbench.oracles import (
    oracle_hidden_cluster_annotation,
    oracle_marker_contradiction,
    oracle_masked_marker_recovery,
)


ORACLE_FILES = [
    "benchmark_tasks/oracle_outputs/hidden_cluster_annotation_oracle_outputs.json",
    "benchmark_tasks/oracle_outputs/marker_contradiction_oracle_outputs.json",
    "benchmark_tasks/oracle_outputs/masked_marker_recovery_oracle_outputs.json",
]


def load_json(path: str):
    return json.loads(Path(path).read_text())


def test_oracle_generation_functions_run():
    hidden_payload = oracle_hidden_cluster_annotation()
    contradiction_payload = oracle_marker_contradiction()
    masked_payload = oracle_masked_marker_recovery()

    assert len(hidden_payload["oracle_outputs"]) == 9
    assert len(contradiction_payload["oracle_outputs"]) == 2
    assert len(masked_payload["oracle_outputs"]) == 5


def test_oracle_output_files_exist():
    for path in ORACLE_FILES:
        assert Path(path).exists(), f"Missing oracle output file: {path}"


def test_hidden_cluster_oracle_schema():
    payload = load_json(ORACLE_FILES[0])

    for item in payload["oracle_outputs"]:
        assert "task_id" in item
        assert "oracle_response" in item

        response = item["oracle_response"]
        assert "predicted_label" in response
        assert "supporting_genes" in response
        assert "confidence" in response
        assert "rationale" in response
        assert isinstance(response["supporting_genes"], list)
        assert response["confidence"] in {"low", "medium", "high"}


def test_marker_contradiction_oracle_schema():
    payload = load_json(ORACLE_FILES[1])

    for item in payload["oracle_outputs"]:
        response = item["oracle_response"]

        assert "contradiction_detected" in response
        assert "contradiction_type" in response
        assert "supporting_labels" in response
        assert "rationale" in response
        assert response["contradiction_detected"] is True
        assert isinstance(response["supporting_labels"], list)


def test_masked_marker_recovery_oracle_schema():
    payload = load_json(ORACLE_FILES[2])

    for item in payload["oracle_outputs"]:
        response = item["oracle_response"]

        assert "predicted_label" in response
        assert "masked_genes" in response
        assert "secondary_supporting_genes" in response
        assert "uncertainty_comment" in response
        assert "rationale" in response
        assert isinstance(response["masked_genes"], list)
        assert isinstance(response["secondary_supporting_genes"], list)


def test_oracle_task_ids_match_hidden_answers():
    pairs = [
        (
            "benchmark_tasks/hidden/hidden_cluster_annotation_answers.json",
            "benchmark_tasks/oracle_outputs/hidden_cluster_annotation_oracle_outputs.json",
        ),
        (
            "benchmark_tasks/hidden/marker_contradiction_answers.json",
            "benchmark_tasks/oracle_outputs/marker_contradiction_oracle_outputs.json",
        ),
        (
            "benchmark_tasks/hidden/masked_marker_recovery_answers.json",
            "benchmark_tasks/oracle_outputs/masked_marker_recovery_oracle_outputs.json",
        ),
    ]

    for hidden_path, oracle_path in pairs:
        hidden_ids = {x["task_id"] for x in load_json(hidden_path)["answers"]}
        oracle_ids = {x["task_id"] for x in load_json(oracle_path)["oracle_outputs"]}

        assert hidden_ids == oracle_ids
