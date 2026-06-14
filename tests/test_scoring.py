from pathlib import Path
import json

from scbench.scoring import score_solver_answers, load_all_oracles


def test_load_all_oracles_contains_expected_task_count():
    oracle_index = load_all_oracles()
    assert len(oracle_index) == 16


def test_score_solver_answers_creates_report():
    report = score_solver_answers()

    assert report["summary"]["total_answers"] == 3
    assert report["summary"]["correct_answers"] == 3
    assert report["summary"]["accuracy"] == 1.0
    assert report["summary"]["average_score"] > 0.8

    output_path = Path("results/reports/sample_solver_score_report.json")
    assert output_path.exists()


def test_score_report_has_expected_schema():
    path = Path("results/reports/sample_solver_score_report.json")
    payload = json.loads(path.read_text())

    assert "summary" in payload
    assert "scored_answers" in payload
    assert len(payload["scored_answers"]) == 3

    for item in payload["scored_answers"]:
        assert "task_id" in item
        assert "task_type" in item
        assert "is_correct" in item
        assert "score" in item
        assert "feedback" in item
