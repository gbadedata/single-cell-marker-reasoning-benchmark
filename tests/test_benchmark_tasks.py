from pathlib import Path
import json


PUBLIC_FILES = [
    "benchmark_tasks/public/hidden_cluster_annotation_tasks.json",
    "benchmark_tasks/public/marker_contradiction_tasks.json",
    "benchmark_tasks/public/masked_marker_recovery_tasks.json",
]

HIDDEN_FILES = [
    "benchmark_tasks/hidden/hidden_cluster_annotation_answers.json",
    "benchmark_tasks/hidden/marker_contradiction_answers.json",
    "benchmark_tasks/hidden/masked_marker_recovery_answers.json",
]


def load_json(path: str):
    return json.loads(Path(path).read_text())


def test_public_benchmark_task_files_exist():
    for path in PUBLIC_FILES:
        assert Path(path).exists(), f"Missing public benchmark task file: {path}"


def test_hidden_answer_files_exist():
    for path in HIDDEN_FILES:
        assert Path(path).exists(), f"Missing hidden answer file: {path}"


def test_expected_task_counts():
    assert len(load_json(PUBLIC_FILES[0])["tasks"]) == 9
    assert len(load_json(PUBLIC_FILES[1])["tasks"]) == 2
    assert len(load_json(PUBLIC_FILES[2])["tasks"]) == 5

    assert len(load_json(HIDDEN_FILES[0])["answers"]) == 9
    assert len(load_json(HIDDEN_FILES[1])["answers"]) == 2
    assert len(load_json(HIDDEN_FILES[2])["answers"]) == 5


def test_public_tasks_have_required_fields():
    required = {
        "task_id",
        "task_type",
        "difficulty",
        "scientific_premise",
        "input_given_to_solver",
        "question",
        "expected_answer_schema",
    }

    for file_path in PUBLIC_FILES:
        payload = load_json(file_path)
        for task in payload["tasks"]:
            assert required.issubset(task.keys()), f"Missing fields in {task.get('task_id')}"


def test_public_and_hidden_task_ids_match():
    task_answer_pairs = [
        (PUBLIC_FILES[0], HIDDEN_FILES[0]),
        (PUBLIC_FILES[1], HIDDEN_FILES[1]),
        (PUBLIC_FILES[2], HIDDEN_FILES[2]),
    ]

    for public_path, hidden_path in task_answer_pairs:
        public_ids = {task["task_id"] for task in load_json(public_path)["tasks"]}
        hidden_ids = {answer["task_id"] for answer in load_json(hidden_path)["answers"]}

        assert public_ids == hidden_ids
