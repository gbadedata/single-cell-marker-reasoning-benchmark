# Evidence Map

This document maps the main project claims to the files, tests, outputs, and evidence artifacts that support them.

## 1. Repository and Reproducibility Evidence

| Claim | Supporting evidence |
|---|---|
| The project is version-controlled and published on GitHub | Git commit history and remote repository |
| The project has a Conda/Mamba environment | `environment.yml` |
| The project has Docker reproducibility | `Dockerfile`, `.dockerignore`, `Makefile` |
| Docker unit tests run successfully | `docs/evidence/26_docker_unit_test_output.txt` |
| The full Docker pipeline runs from a clean container | `docs/evidence/27_docker_full_pipeline_test_output.txt` |
| GitHub Actions CI is enabled and passing | `.github/workflows/ci.yml`, GitHub Actions badge in `README.md` |

## 2. Data Loading Evidence

| Claim | Supporting evidence |
|---|---|
| PBMC3k data is downloaded using Scanpy | `scripts/01_download_data.py` |
| Raw AnnData file is generated | `data/raw/pbmc3k_raw.h5ad` |
| Dataset loading was validated | `tests/test_data_io.py` |
| Dataset loading evidence was captured | `docs/evidence/03_dataset_load_output.txt` |

## 3. Preprocessing Evidence

| Claim | Supporting evidence |
|---|---|
| QC metrics are calculated | `src/scbench/preprocessing.py` |
| Cells and genes are filtered | `src/scbench/preprocessing.py` |
| Raw counts are preserved | `src/scbench/preprocessing.py` |
| Normalisation and log transformation are applied | `src/scbench/preprocessing.py` |
| PCA, neighbours, UMAP, and Leiden clustering are generated | `src/scbench/preprocessing.py` |
| Processed AnnData file is generated | `data/processed/pbmc3k_processed.h5ad` |
| Preprocessing tests exist | `tests/test_preprocessing.py` |
| Preprocessing evidence was captured | `docs/evidence/06_preprocessing_output.txt` |

## 4. Marker Ranking Evidence

| Claim | Supporting evidence |
|---|---|
| Marker genes are ranked per Leiden cluster | `src/scbench/analysis.py`, `scripts/03_rank_markers.py` |
| Raw marker table is generated | `results/tables/cluster_marker_genes.csv` |
| Filtered marker table is generated | `results/tables/cluster_marker_genes_filtered.csv` |
| Noisy ribosomal, mitochondrial, and housekeeping genes are filtered | `src/scbench/analysis.py` |
| Marker ranking evidence was captured | `docs/evidence/08_marker_ranking_output.txt` |

## 5. Cluster Annotation Evidence

| Claim | Supporting evidence |
|---|---|
| Clusters are assigned marker-derived working annotations | `src/scbench/annotation.py`, `scripts/04_annotate_clusters.py` |
| Annotation confidence levels are stored | `results/tables/cluster_annotations.csv` |
| Annotated AnnData file is generated | `data/processed/pbmc3k_annotated.h5ad` |
| Annotation tests exist | `tests/test_annotation.py` |
| Annotation evidence was captured | `docs/evidence/09_annotation_output.txt` |

## 6. Visual Output Evidence

| Claim | Supporting evidence |
|---|---|
| UMAP by Leiden cluster is generated | `results/figures/umap_by_leiden.png` |
| UMAP by marker-derived annotation is generated | `results/figures/umap_by_annotation.png` |
| Visual generation script exists | `scripts/09_generate_visual_outputs.py` |
| Visual generation module exists | `src/scbench/visualization.py` |
| Visual output tests exist | `tests/test_visualization.py` |
| Visual output evidence was captured | `docs/evidence/28_visual_outputs.txt` |

## 7. Benchmark Task Evidence

| Claim | Supporting evidence |
|---|---|
| Public benchmark tasks are generated | `benchmark_tasks/public/` |
| Hidden answer keys are generated | `benchmark_tasks/hidden/` |
| Hidden cluster annotation tasks exist | `benchmark_tasks/public/hidden_cluster_annotation_tasks.json` |
| Marker contradiction tasks exist | `benchmark_tasks/public/marker_contradiction_tasks.json` |
| Masked marker recovery tasks exist | `benchmark_tasks/public/masked_marker_recovery_tasks.json` |
| Benchmark generation script exists | `scripts/05_generate_benchmark_tasks.py` |
| Benchmark task tests exist | `tests/test_benchmark_tasks.py` |
| Benchmark task summary table exists | `results/tables/benchmark_task_summary.csv` |
| Benchmark generation evidence was captured | `docs/evidence/11_benchmark_generation_output.txt` |

## 8. Oracle Output Evidence

| Claim | Supporting evidence |
|---|---|
| Oracle outputs are generated for benchmark tasks | `benchmark_tasks/oracle_outputs/` |
| Oracle generation script exists | `scripts/06_generate_oracle_outputs.py` |
| Oracle generation module exists | `src/scbench/oracles.py` |
| Oracle tests exist | `tests/test_oracles.py` |
| Oracle generation evidence was captured | `docs/evidence/14_oracle_generation_output.txt` |

## 9. Validator and Scoring Evidence

| Claim | Supporting evidence |
|---|---|
| Solver answers can be scored | `src/scbench/scoring.py`, `scripts/07_score_solver_answers.py` |
| Validators are implemented | `src/scbench/validators.py` |
| Sample solver answers exist | `sample_solver_answers/sample_answers.json` |
| Sample solver scoring report is generated | `results/reports/sample_solver_score_report.json` |
| Validator tests exist | `tests/test_validators.py` |
| Scoring tests exist | `tests/test_scoring.py` |
| Solver scoring evidence was captured | `docs/evidence/17_solver_scoring_output.txt` |

## 10. Calibration Evidence

| Claim | Supporting evidence |
|---|---|
| Calibration framework exists | `src/scbench/calibration.py` |
| Calibration asset generation script exists | `scripts/08_generate_calibration_assets.py` |
| Calibration log template exists | `benchmark_tasks/calibration_logs/calibration_log_template.json` |
| Initial difficulty review exists | `benchmark_tasks/calibration_logs/initial_task_difficulty_review.json` |
| Calibration tests exist | `tests/test_calibration.py` |
| Calibration evidence was captured | `docs/evidence/21_calibration_assets_output.txt` |

## 11. Test Evidence

| Claim | Supporting evidence |
|---|---|
| Full local test suite passes | `PYTHONPATH=src pytest -q` |
| Current local test count is 36 passed | Latest local pytest output |
| Unit tests are separated from integration tests | `pytest.ini`, test markers |
| Unit test evidence exists | `docs/evidence/24_unit_tests_after_docker_split.txt` |
| Integration test evidence exists | `docs/evidence/25_integration_tests_after_docker_split.txt` |

## 12. Known Limitations and Honest Scope

| Limitation | Where it is documented |
|---|---|
| PBMC3k-only benchmark scope | `README.md`, `docs/limitations.md` |
| Marker-derived annotations are not experimental ground truth | `README.md`, `docs/methods.md`, `docs/limitations.md` |
| Calibration is design-stage, not empirical frontier-model calibration | `README.md`, `docs/benchmark_design.md`, `docs/limitations.md` |
| Benchmark task count is prototype-scale | `README.md`, `docs/benchmark_design.md` |
| Larger datasets may need memory/performance hardening | `README.md`, `docs/limitations.md` |
