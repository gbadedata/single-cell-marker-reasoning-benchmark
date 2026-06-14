# Single-Cell RNA-seq Benchmark Task Suite for Cell-Type Annotation and Marker-Gene Reasoning

## Overview

This project builds a reproducible single-cell RNA-seq analysis and benchmark-design workflow using Scanpy.

It starts with PBMC3k single-cell data, performs preprocessing, clustering, marker-gene ranking, and marker-derived annotation, then converts the outputs into benchmark-style scientific reasoning tasks with hidden answers, oracle outputs, validators, scoring, and calibration assets.

The goal is not just to run a Scanpy workflow. The goal is to demonstrate how single-cell analysis outputs can be transformed into evaluable scientific reasoning tasks.

## Why This Project Exists

This project is aligned with roles that require:

- computational biology reasoning
- single-cell genomics workflows
- scientific software implementation
- benchmark and evaluation design
- Python-based oracle and validator functions
- reproducible Linux/terminal workflows

## Current Status

Implemented:

- PBMC3k data loading
- Scanpy preprocessing pipeline
- QC filtering
- PCA, neighbours, UMAP, Leiden clustering
- marker-gene ranking
- filtered marker-gene table
- marker-derived cluster annotation
- public benchmark task generation
- hidden answer generation
- oracle output generation
- validator functions
- solver-answer scoring workflow
- calibration log template
- initial task difficulty review
- pytest test suite
- evidence capture

Current test status: 34 passed.

## Dataset

Dataset: PBMC3k loaded through scanpy.datasets.pbmc3k().

Raw shape:

- 2700 cells
- 32738 genes

Processed shape:

- 2694 cells
- 2000 highly variable genes

## Marker-Derived Cluster Annotations

| Cluster | Working label | Confidence |
|---|---|---|
| 0 | T cells | Medium |
| 1 | CD14+ monocytes | High |
| 2 | B cells | High |
| 3 | Cytotoxic T cells | Medium |
| 4 | NK cells | High |
| 5 | FCGR3A+ monocytes | High |
| 6 | Dendritic cells | Medium |
| 7 | Platelets | High |
| 8 | Cycling cells | Medium |

These are marker-derived working annotations, not experimentally validated labels.

## Benchmark Task Types

### 1. Hidden Cluster Annotation

The solver receives filtered marker genes and candidate labels but not the oracle label.

### 2. Marker Contradiction Detection

The solver compares two marker profiles and identifies biological ambiguity or overlapping signatures.

### 3. Masked Marker Recovery

Canonical markers are removed, forcing the solver to infer cell identity from secondary evidence.

## Benchmark Assets

Public task files:

- benchmark_tasks/public/

Hidden answer files:

- benchmark_tasks/hidden/

Oracle outputs:

- benchmark_tasks/oracle_outputs/

Calibration logs:

- benchmark_tasks/calibration_logs/

## Scoring Workflow

A sample solver answer file is provided:

- sample_solver_answers/sample_answers.json

Run scoring with:

PYTHONPATH=src python scripts/07_score_solver_answers.py

Example scoring output:

- total_answers: 3
- correct_answers: 3
- accuracy: 1.0
- average_score: 0.923

## Reproduce the Workflow

Activate the environment:

conda activate sc-marker-benchmark

Run the workflow:

PYTHONPATH=src python scripts/01_download_data.py
PYTHONPATH=src python scripts/02_preprocess.py
PYTHONPATH=src python scripts/03_rank_markers.py
PYTHONPATH=src python scripts/04_annotate_clusters.py
PYTHONPATH=src python scripts/05_generate_benchmark_tasks.py
PYTHONPATH=src python scripts/06_generate_oracle_outputs.py
PYTHONPATH=src python scripts/07_score_solver_answers.py
PYTHONPATH=src python scripts/08_generate_calibration_assets.py
PYTHONPATH=src pytest -q

## Repository Structure

- benchmark_tasks/
- configs/
- data/
- docs/
- notebooks/
- results/
- sample_solver_answers/
- scripts/
- src/scbench/
- tests/

## Evidence

Evidence outputs are stored in:

- docs/evidence/

They include:

- project trees
- pytest outputs
- preprocessing outputs
- marker-ranking outputs
- annotation outputs
- benchmark-generation outputs
- oracle-generation outputs
- solver-scoring outputs
- calibration outputs

## Limitations

See docs/limitations.md.

Key limitations:

- annotations are marker-derived, not experimental ground truth
- PBMC3k is small
- empirical frontier-model calibration has not yet been performed
- Docker reproducibility is not yet implemented

## Next Steps

Planned improvements:

- Dockerfile and containerized reproducibility
- richer README evidence map
- generated figures
- empirical calibration attempts
- GitHub Actions CI
