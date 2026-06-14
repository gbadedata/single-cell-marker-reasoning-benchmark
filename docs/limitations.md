# Limitations

## Marker-Derived Labels Are Not Ground Truth

Cluster annotations are inferred from marker genes. They are working labels, not experimentally confirmed biological truth.

## PBMC3k Is a Small Dataset

PBMC3k is useful for demonstration and controlled benchmarking, but it is not enough to prove broad single-cell expertise.

## Marker Overlap Can Create Ambiguity

Some immune populations share cytotoxic, antigen-presentation, or activation-related genes. This affects annotation confidence.

## Filtered Marker Tables May Remove Useful Genes

Filtering ribosomal, mitochondrial, or broad housekeeping-like genes improves interpretability but can remove context that may still be biologically relevant in some settings.

## Calibration Is Not Yet Empirical

The current calibration framework defines how calibration should be recorded, but tasks have not yet been tested against frontier AI models or independent human solvers.

## No Reference-Based Annotation Yet

This project currently uses manual marker-based annotation. It does not yet compare labels against reference mapping tools.

## No Docker Reproducibility Yet

The current workflow is Conda/Mamba-based. Docker will be added in a later phase.
