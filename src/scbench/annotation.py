from __future__ import annotations

from pathlib import Path
import pandas as pd
import scanpy as sc


CLUSTER_ANNOTATIONS = {
    "0": {
        "label": "T cells",
        "confidence": "medium",
        "evidence": ["CD3D", "CD3E", "IL7R", "LTB"],
        "notes": "T-cell markers present; broad cluster likely includes naive/memory T cells.",
    },
    "1": {
        "label": "CD14+ monocytes",
        "confidence": "high",
        "evidence": ["LYZ", "S100A8", "S100A9", "FCN1", "CST3"],
        "notes": "Strong classical monocyte marker profile.",
    },
    "2": {
        "label": "B cells",
        "confidence": "high",
        "evidence": ["CD79A", "CD79B", "MS4A1", "CD74", "HLA-DRA"],
        "notes": "Strong B-cell and antigen-presentation marker profile.",
    },
    "3": {
        "label": "Cytotoxic T cells",
        "confidence": "medium",
        "evidence": ["CD3D", "CCL5", "NKG7", "GZMA", "CST7"],
        "notes": "T-cell marker CD3D plus cytotoxic markers; overlaps with NK-like cytotoxic signature.",
    },
    "4": {
        "label": "NK cells",
        "confidence": "high",
        "evidence": ["NKG7", "GNLY", "GZMB", "PRF1", "FGFBP2"],
        "notes": "Strong NK/cytotoxic marker profile with GNLY, GZMB, PRF1.",
    },
    "5": {
        "label": "FCGR3A+ monocytes",
        "confidence": "high",
        "evidence": ["LST1", "FCER1G", "FCGR3A", "AIF1", "IFITM3"],
        "notes": "Non-classical monocyte-like marker profile.",
    },
    "6": {
        "label": "Dendritic cells",
        "confidence": "medium",
        "evidence": ["HLA-DPA1", "HLA-DPB1", "HLA-DRA", "FCER1A", "CST3"],
        "notes": "Antigen-presentation genes and FCER1A support dendritic/APC-like identity.",
    },
    "7": {
        "label": "Platelets",
        "confidence": "high",
        "evidence": ["PPBP", "PF4", "GNG11", "SDPR", "NRGN"],
        "notes": "Strong platelet marker profile.",
    },
    "8": {
        "label": "Cycling cells",
        "confidence": "medium",
        "evidence": ["KIAA0101", "TYMS", "ZWINT", "TUBB"],
        "notes": "Cell-cycle/proliferation-associated genes; small cluster, interpret cautiously.",
    },
}


def create_annotation_table(
    marker_table_path: str = "results/tables/cluster_marker_genes_filtered.csv",
    output_path: str = "results/tables/cluster_annotations.csv",
) -> pd.DataFrame:
    markers = pd.read_csv(marker_table_path)
    rows = []

    for cluster, info in CLUSTER_ANNOTATIONS.items():
        top_markers = (
            markers[markers["group"].astype(str) == cluster]["names"]
            .head(15)
            .tolist()
        )

        rows.append(
            {
                "cluster": cluster,
                "label": info["label"],
                "confidence": info["confidence"],
                "evidence_genes": ";".join(info["evidence"]),
                "top_filtered_markers": ";".join(top_markers),
                "notes": info["notes"],
            }
        )

    df = pd.DataFrame(rows)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    return df


def add_annotations_to_anndata(
    input_path: str = "data/processed/pbmc3k_markers.h5ad",
    output_path: str = "data/processed/pbmc3k_annotated.h5ad",
) -> None:
    adata = sc.read_h5ad(input_path)

    label_map = {cluster: info["label"] for cluster, info in CLUSTER_ANNOTATIONS.items()}
    confidence_map = {cluster: info["confidence"] for cluster, info in CLUSTER_ANNOTATIONS.items()}

    adata.obs["marker_annotation"] = adata.obs["leiden"].astype(str).map(label_map)
    adata.obs["annotation_confidence"] = adata.obs["leiden"].astype(str).map(confidence_map)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(output)
