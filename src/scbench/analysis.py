from __future__ import annotations

from pathlib import Path
import pandas as pd
import scanpy as sc


NOISY_GENE_PREFIXES = (
    "RPS",
    "RPL",
    "MT-",
)

NOISY_GENES = {
    "MALAT1",
    "TPT1",
    "EEF1A1",
    "B2M",
}


def is_informative_gene(gene: str) -> bool:
    gene_upper = str(gene).upper()

    if gene_upper in NOISY_GENES:
        return False

    if gene_upper.startswith(NOISY_GENE_PREFIXES):
        return False

    return True


def rank_marker_genes(
    input_path: str = "data/processed/pbmc3k_processed.h5ad",
    output_path: str = "data/processed/pbmc3k_markers.h5ad",
    marker_table_path: str = "results/tables/cluster_marker_genes.csv",
    filtered_marker_table_path: str = "results/tables/cluster_marker_genes_filtered.csv",
    groupby: str = "leiden",
    method: str = "wilcoxon",
    n_genes: int = 50,
    filtered_top_n: int = 20,
):
    adata = sc.read_h5ad(input_path)

    sc.tl.rank_genes_groups(
        adata,
        groupby=groupby,
        method=method,
        use_raw=True,
    )

    marker_df = sc.get.rank_genes_groups_df(adata, group=None)
    marker_df = marker_df.groupby("group", group_keys=False).head(n_genes)

    marker_table = Path(marker_table_path)
    marker_table.parent.mkdir(parents=True, exist_ok=True)
    marker_df.to_csv(marker_table, index=False)

    filtered_df = marker_df[marker_df["names"].map(is_informative_gene)].copy()
    filtered_df = filtered_df.groupby("group", group_keys=False).head(filtered_top_n)

    filtered_marker_table = Path(filtered_marker_table_path)
    filtered_marker_table.parent.mkdir(parents=True, exist_ok=True)
    filtered_df.to_csv(filtered_marker_table, index=False)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(output)

    return adata, marker_df, filtered_df
