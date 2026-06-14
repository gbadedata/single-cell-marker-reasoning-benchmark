from __future__ import annotations

from pathlib import Path
import scanpy as sc


def preprocess_pbmc3k(
    input_path: str = "data/raw/pbmc3k_raw.h5ad",
    output_path: str = "data/processed/pbmc3k_processed.h5ad",
    min_genes_per_cell: int = 200,
    min_cells_per_gene: int = 3,
    max_pct_mito: float = 10.0,
    target_sum: float = 1e4,
    n_top_genes: int = 2000,
    n_pcs: int = 40,
    n_neighbors: int = 10,
    leiden_resolution: float = 0.8,
):
    adata = sc.read_h5ad(input_path)

    adata.var["mt"] = adata.var_names.str.upper().str.startswith("MT-")
    sc.pp.calculate_qc_metrics(
        adata,
        qc_vars=["mt"],
        percent_top=None,
        log1p=False,
        inplace=True,
    )

    sc.pp.filter_cells(adata, min_genes=min_genes_per_cell)
    sc.pp.filter_genes(adata, min_cells=min_cells_per_gene)

    adata = adata[adata.obs["pct_counts_mt"] < max_pct_mito].copy()

    adata.layers["counts"] = adata.X.copy()

    sc.pp.normalize_total(adata, target_sum=target_sum)
    sc.pp.log1p(adata)

    adata.raw = adata

    sc.pp.highly_variable_genes(
        adata,
        n_top_genes=n_top_genes,
        subset=True,
        flavor="seurat",
    )

    sc.pp.scale(adata, max_value=10)
    sc.tl.pca(adata, svd_solver="arpack")
    sc.pp.neighbors(adata, n_neighbors=n_neighbors, n_pcs=n_pcs)
    sc.tl.umap(adata)
    sc.tl.leiden(adata, resolution=leiden_resolution, key_added="leiden")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(output)

    return adata
