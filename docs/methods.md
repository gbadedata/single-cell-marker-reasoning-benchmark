# Methods

## Dataset

This project uses the PBMC3k single-cell RNA-seq dataset loaded through `scanpy.datasets.pbmc3k()`.

The raw dataset contains:

- 2,700 cells
- 32,738 genes
- AnnData `.h5ad` format

## Preprocessing Workflow

The preprocessing pipeline performs:

1. Raw AnnData loading
2. Mitochondrial gene detection
3. QC metric calculation
4. Cell filtering
5. Gene filtering
6. High mitochondrial percentage filtering
7. Raw count preservation in `adata.layers["counts"]`
8. Library-size normalization
9. Log transformation
10. Highly variable gene selection
11. Scaling
12. PCA
13. Neighbour graph construction
14. UMAP embedding
15. Leiden clustering

## Marker-Gene Ranking

Cluster marker genes are ranked using Scanpy's `rank_genes_groups` with the Wilcoxon method.

Two marker tables are produced:

- `results/tables/cluster_marker_genes.csv`
- `results/tables/cluster_marker_genes_filtered.csv`

The filtered marker table suppresses common noisy genes such as ribosomal, mitochondrial, and broad housekeeping-like genes.

## Annotation Strategy

Cluster labels are marker-derived working annotations. They are not experimentally validated ground truth.

Each annotation includes:

- cluster ID
- marker-based label
- confidence level
- evidence genes
- top filtered markers
- interpretation notes

## Benchmark Construction

The analysis outputs are converted into benchmark-style tasks.

The benchmark includes:

- hidden cluster annotation tasks
- marker contradiction tasks
- masked marker recovery tasks

Each task has:

- public solver-facing input
- hidden answer file
- oracle output
- validator scoring
- calibration framework
