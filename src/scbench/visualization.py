from pathlib import Path

import pandas as pd
import scanpy as sc


def save_umap_figures(
    annotated_h5ad_path: str | Path,
    figures_dir: str | Path,
) -> dict[str, Path]:
    """Save UMAP figures coloured by Leiden cluster and marker-derived annotation."""
    annotated_h5ad_path = Path(annotated_h5ad_path)
    figures_dir = Path(figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)

    adata = sc.read_h5ad(annotated_h5ad_path)

    sc.settings.figdir = str(figures_dir)

    sc.pl.umap(
        adata,
        color="leiden",
        legend_loc="on data",
        title="PBMC3k Leiden Clusters",
        frameon=False,
        show=False,
        save="_by_leiden.png",
    )

    sc.pl.umap(
        adata,
        color="marker_annotation",
        legend_loc="right margin",
        title="PBMC3k Marker-Derived Cell-Type Annotations",
        frameon=False,
        show=False,
        save="_by_annotation.png",
    )

    # Scanpy prefixes saved files with "umap"
    leiden_path = figures_dir / "umap_by_leiden.png"
    annotation_path = figures_dir / "umap_by_annotation.png"

    return {
        "umap_by_leiden": leiden_path,
        "umap_by_annotation": annotation_path,
    }


def create_benchmark_task_summary(
    public_tasks_dir: str | Path,
    output_csv_path: str | Path,
) -> pd.DataFrame:
    """Create a summary table of public benchmark task counts."""
    public_tasks_dir = Path(public_tasks_dir)
    output_csv_path = Path(output_csv_path)
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)

    files = {
        "hidden_cluster_annotation": public_tasks_dir / "hidden_cluster_annotation_tasks.json",
        "marker_contradiction_detection": public_tasks_dir / "marker_contradiction_tasks.json",
        "masked_marker_recovery": public_tasks_dir / "masked_marker_recovery_tasks.json",
    }

    rows = []
    for task_family, path in files.items():
        tasks = pd.read_json(path)
        rows.append(
            {
                "task_family": task_family,
                "public_task_file": str(path),
                "task_count": len(tasks),
            }
        )

    df = pd.DataFrame(rows)
    df.loc[len(df)] = {
        "task_family": "total",
        "public_task_file": "all public task files",
        "task_count": int(df["task_count"].sum()),
    }

    df.to_csv(output_csv_path, index=False)
    return df
