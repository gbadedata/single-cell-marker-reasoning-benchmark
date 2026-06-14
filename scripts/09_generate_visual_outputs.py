from pathlib import Path

from scbench.visualization import create_benchmark_task_summary, save_umap_figures


PROJECT_ROOT = Path(__file__).resolve().parents[1]

ANNOTATED_H5AD = PROJECT_ROOT / "data" / "processed" / "pbmc3k_annotated.h5ad"
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"
PUBLIC_TASKS_DIR = PROJECT_ROOT / "benchmark_tasks" / "public"
SUMMARY_CSV = PROJECT_ROOT / "results" / "tables" / "benchmark_task_summary.csv"


def main() -> None:
    figures = save_umap_figures(
        annotated_h5ad_path=ANNOTATED_H5AD,
        figures_dir=FIGURES_DIR,
    )

    summary = create_benchmark_task_summary(
        public_tasks_dir=PUBLIC_TASKS_DIR,
        output_csv_path=SUMMARY_CSV,
    )

    print("Visual outputs generated.")
    print("Figures:")
    for name, path in figures.items():
        print(f"- {name}: {path}")

    print("\nBenchmark task summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
