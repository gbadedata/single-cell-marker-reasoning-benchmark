from pathlib import Path
import pytest
import scanpy as sc


@pytest.mark.integration
def test_processed_pbmc3k_exists():
    path = Path("data/processed/pbmc3k_processed.h5ad")
    assert path.exists(), "Processed PBMC3k dataset was not found."


@pytest.mark.integration
def test_processed_pbmc3k_has_expected_structure():
    adata = sc.read_h5ad("data/processed/pbmc3k_processed.h5ad")

    assert adata.n_obs > 2500
    assert adata.n_vars == 2000

    assert "leiden" in adata.obs.columns
    assert "X_pca" in adata.obsm
    assert "X_umap" in adata.obsm

    assert "neighbors" in adata.uns
    assert "pca" in adata.uns
    assert "umap" in adata.uns

    assert "counts" in adata.layers


@pytest.mark.integration
def test_processed_pbmc3k_has_multiple_clusters():
    adata = sc.read_h5ad("data/processed/pbmc3k_processed.h5ad")
    clusters = adata.obs["leiden"].unique().tolist()

    assert len(clusters) >= 5
