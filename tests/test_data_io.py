from pathlib import Path
import pytest
import scanpy as sc


@pytest.mark.integration
def test_raw_pbmc3k_exists():
    path = Path("data/raw/pbmc3k_raw.h5ad")
    assert path.exists(), "PBMC3k raw dataset was not found."


@pytest.mark.integration
def test_raw_pbmc3k_loads_as_anndata():
    adata = sc.read_h5ad("data/raw/pbmc3k_raw.h5ad")
    assert adata.n_obs == 2700
    assert adata.n_vars == 32738
    assert "gene_ids" in adata.var.columns
