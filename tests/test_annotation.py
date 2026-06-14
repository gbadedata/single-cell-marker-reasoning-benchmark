from pathlib import Path
import pandas as pd
import scanpy as sc


EXPECTED_LABELS = {
    "T cells",
    "CD14+ monocytes",
    "B cells",
    "Cytotoxic T cells",
    "NK cells",
    "FCGR3A+ monocytes",
    "Dendritic cells",
    "Platelets",
    "Cycling cells",
}


def test_annotation_table_exists():
    path = Path("results/tables/cluster_annotations.csv")
    assert path.exists(), "Cluster annotation table was not found."


def test_annotation_table_has_expected_labels():
    df = pd.read_csv("results/tables/cluster_annotations.csv")

    assert df.shape[0] == 9
    assert set(df["label"]) == EXPECTED_LABELS
    assert {"cluster", "label", "confidence", "evidence_genes", "top_filtered_markers", "notes"}.issubset(df.columns)


def test_annotated_anndata_exists():
    path = Path("data/processed/pbmc3k_annotated.h5ad")
    assert path.exists(), "Annotated AnnData file was not found."


def test_annotated_anndata_has_annotation_columns():
    adata = sc.read_h5ad("data/processed/pbmc3k_annotated.h5ad")

    assert "marker_annotation" in adata.obs.columns
    assert "annotation_confidence" in adata.obs.columns
    assert adata.obs["marker_annotation"].notna().all()
    assert adata.obs["annotation_confidence"].notna().all()


def test_annotation_confidence_values_are_controlled():
    adata = sc.read_h5ad("data/processed/pbmc3k_annotated.h5ad")
    observed = set(adata.obs["annotation_confidence"].astype(str).unique())

    assert observed.issubset({"low", "medium", "high"})
