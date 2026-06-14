from pathlib import Path

import pandas as pd
import pytest

from scbench.visualization import create_benchmark_task_summary


def test_create_benchmark_task_summary(tmp_path):
    output_csv = tmp_path / "benchmark_task_summary.csv"

    df = create_benchmark_task_summary(
        public_tasks_dir=Path("benchmark_tasks/public"),
        output_csv_path=output_csv,
    )

    assert output_csv.exists()
    assert set(df.columns) == {"task_family", "public_task_file", "task_count"}
    assert int(df[df["task_family"] == "total"]["task_count"].iloc[0]) == 16


@pytest.mark.integration
def test_visual_outputs_exist_after_generation():
    assert Path("results/figures/umap_by_leiden.png").exists()
    assert Path("results/figures/umap_by_annotation.png").exists()
    assert Path("results/tables/benchmark_task_summary.csv").exists()
