from pathlib import Path
import json

from scbench.calibration import (
    create_calibration_log_template,
    create_initial_calibration_review,
)


def load_json(path: str):
    return json.loads(Path(path).read_text())


def test_create_calibration_log_template():
    payload = create_calibration_log_template()

    assert "difficulty_categories" in payload
    assert "calibration_fields" in payload
    assert "task_id" in payload["calibration_fields"]
    assert "difficulty_assessment" in payload["calibration_fields"]


def test_create_initial_calibration_review():
    payload = create_initial_calibration_review()

    assert "important_limitation" in payload
    assert "task_type_reviews" in payload
    assert len(payload["task_type_reviews"]) == 3


def test_calibration_files_exist():
    assert Path("benchmark_tasks/calibration_logs/calibration_log_template.json").exists()
    assert Path("benchmark_tasks/calibration_logs/initial_task_difficulty_review.json").exists()


def test_initial_review_is_honest_about_limitation():
    payload = load_json("benchmark_tasks/calibration_logs/initial_task_difficulty_review.json")
    limitation = payload["important_limitation"].lower()

    assert "not yet empirical" in limitation
    assert "frontier-model calibration" in limitation
