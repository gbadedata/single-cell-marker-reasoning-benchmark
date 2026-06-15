# Single-Cell Marker Reasoning Benchmark

[![CI](https://github.com/gbadedata/single-cell-marker-reasoning-benchmark/actions/workflows/ci.yml/badge.svg)](https://github.com/gbadedata/single-cell-marker-reasoning-benchmark/actions/workflows/ci.yml)

A reproducible single-cell RNA-seq analysis and benchmark-engineering project built with **Scanpy**, **AnnData**, **Python**, **pytest**, **Docker**, **GitHub Actions**, and structured benchmark assets.

This project turns a standard single-cell RNA-seq workflow into a tested, containerised, evidence-backed benchmark suite for marker-gene reasoning, cluster annotation, contradiction detection, oracle generation, answer validation, scoring, and calibration planning.

Repository: `gbadedata/single-cell-marker-reasoning-benchmark`

---

## 1. Executive Summary

This project analyses the PBMC3k single-cell RNA-seq dataset and builds a benchmark layer on top of the analysis outputs.

The project does four main things:

1. Runs a reproducible Scanpy workflow on PBMC3k.
2. Identifies and filters cluster marker genes.
3. Produces marker-derived working cluster annotations.
4. Converts scientific outputs into benchmark tasks with hidden answers, oracle responses, validators, scoring, calibration assets, visual outputs, Docker reproducibility, GitHub Actions CI, and evidence-backed documentation.

The result is not a notebook-only analysis. It is a structured scientific software project that connects computational biology, benchmark design, reproducibility engineering, automated testing, and project evidence.

---

## 2. At a Glance

| Area               | Current state                                             |
| ------------------ | --------------------------------------------------------- |
| Dataset            | PBMC3k single-cell RNA-seq                                |
| Analysis framework | Scanpy and AnnData                                        |
| Processed dataset  | 2,694 cells × 2,000 highly variable genes                 |
| Clustering         | Leiden clustering with 9 clusters                         |
| Annotation style   | Marker-derived working annotations with confidence levels |
| Benchmark tasks    | 16 public benchmark tasks                                 |
| Hidden answers     | 16 hidden answer records                                  |
| Oracle outputs     | 16 oracle outputs                                         |
| Test suite         | 36 passing tests                                          |
| Reproducibility    | Conda/Mamba, Makefile, Docker                             |
| CI                 | GitHub Actions unit-test workflow passing                 |
| Evidence           | Evidence logs, visual outputs, and `docs/evidence_map.md` |
| Current status     | Portfolio-ready prototype benchmark system                |

---

## 3. Why This Project Exists

Many single-cell RNA-seq examples stop at preprocessing, clustering, marker-gene ranking, and UMAP visualisation.

This project goes further by asking:

> Can a single-cell RNA-seq analysis workflow be converted into a reproducible benchmark suite for testing biological reasoning?

The benchmark focuses on practical marker-gene reasoning tasks, including:

* identifying likely cell types from marker genes;
* detecting contradictions between related immune-cell labels;
* recovering likely cell identities when canonical markers are partially masked;
* scoring solver answers against hidden answers and oracle outputs;
* separating public benchmark inputs from hidden answer keys;
* documenting limitations honestly instead of overstating the benchmark.

---

## 4. What Makes This Different From a Standard Scanpy Project

| Standard Scanpy workflow     | This project                                                     |
| ---------------------------- | ---------------------------------------------------------------- |
| Loads single-cell data       | Loads and stores raw AnnData reproducibly                        |
| Performs QC and clustering   | Performs QC and clustering with reusable modules and tests       |
| Ranks marker genes           | Produces raw and filtered marker tables                          |
| Annotates clusters manually  | Stores marker-derived working annotations with confidence levels |
| Ends with figures/tables     | Converts outputs into benchmark tasks                            |
| No hidden answers            | Separates public tasks from hidden answer keys                   |
| No oracle layer              | Generates structured oracle outputs                              |
| No scoring framework         | Implements validators and scoring reports                        |
| No clean-container proof     | Adds Docker pipeline reproducibility                             |
| No automated CI              | Adds GitHub Actions unit-test CI                                 |
| No claim-to-evidence mapping | Adds `docs/evidence_map.md`                                      |

---

## 5. Key Features

* Reproducible Scanpy workflow using PBMC3k.
* Structured Python package under `src/scbench`.
* Raw, processed, and annotated AnnData workflow.
* QC filtering, normalisation, log transformation, HVG selection, PCA, neighbours, UMAP, and Leiden clustering.
* Marker-gene ranking using Scanpy.
* Filtered marker-gene table to reduce noisy ribosomal, mitochondrial, and housekeeping markers.
* Marker-derived cluster annotation layer with confidence levels.
* Public benchmark tasks.
* Hidden answer files.
* Oracle output generation.
* Validator functions for scoring solver responses.
* Sample solver scoring report.
* Calibration framework and design-stage difficulty review.
* Unit and integration test separation.
* Dockerfile for clean-container reproducibility.
* Makefile for repeatable command execution.
* GitHub Actions CI for unit tests.
* UMAP visual outputs committed and rendered in the README.
* Evidence map linking project claims to files and outputs.

---

## 6. Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── benchmark_tasks/
│   ├── public/
│   ├── hidden/
│   ├── oracle_outputs/
│   └── calibration_logs/
├── configs/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
├── docs/
│   ├── benchmark_design.md
│   ├── evidence_map.md
│   ├── limitations.md
│   ├── methods.md
│   └── evidence/
├── results/
│   ├── tables/
│   ├── figures/
│   ├── metrics/
│   └── reports/
├── sample_solver_answers/
├── scripts/
├── src/
│   └── scbench/
├── tests/
├── .dockerignore
├── Dockerfile
├── Makefile
├── environment.yml
├── pytest.ini
└── README.md
```

---

## 7. Dataset

This project uses the PBMC3k dataset available through Scanpy.

| Item                 | Value                              |
| -------------------- | ---------------------------------- |
| Dataset              | PBMC3k                             |
| Source access method | `scanpy.datasets.pbmc3k()`         |
| Raw cells            | 2,700                              |
| Raw genes            | 32,738                             |
| Format               | AnnData `.h5ad`                    |
| Biological context   | Peripheral blood mononuclear cells |

The large `.h5ad` files are intentionally not committed to GitHub. They are regenerated through the local or Docker pipeline.

---

## 8. Analysis Workflow

The workflow is implemented through scripts and reusable Python modules.

### 8.1 Data download

Script:

```text
scripts/01_download_data.py
```

Output:

```text
data/raw/pbmc3k_raw.h5ad
```

### 8.2 Preprocessing

Script:

```text
scripts/02_preprocess.py
```

Main operations:

1. Load raw PBMC3k AnnData.
2. Identify mitochondrial genes.
3. Calculate QC metrics.
4. Filter low-quality cells.
5. Filter lowly detected genes.
6. Filter cells with high mitochondrial percentage.
7. Preserve raw counts in `adata.layers["counts"]`.
8. Normalise total counts.
9. Apply log transformation.
10. Store raw-normalised representation in `adata.raw`.
11. Select highly variable genes.
12. Scale data.
13. Run PCA.
14. Build nearest-neighbour graph.
15. Compute UMAP.
16. Run Leiden clustering.

Output:

```text
data/processed/pbmc3k_processed.h5ad
```

Processed dataset:

| Item               |  Value |
| ------------------ | -----: |
| Processed cells    |  2,694 |
| Processed genes    |  2,000 |
| Clustering method  | Leiden |
| Number of clusters |      9 |

### 8.3 Marker-gene ranking

Script:

```text
scripts/03_rank_markers.py
```

Outputs:

```text
results/tables/cluster_marker_genes.csv
results/tables/cluster_marker_genes_filtered.csv
```

The project produces both raw and filtered marker tables.

The filtered marker table removes common noisy genes such as:

* ribosomal genes beginning with `RPS`;
* ribosomal genes beginning with `RPL`;
* mitochondrial genes beginning with `MT-`;
* selected housekeeping or broadly expressed genes such as `MALAT1`, `TPT1`, `EEF1A1`, and `B2M`.

This filtering step was added after early marker outputs were dominated by ribosomal genes, which reduced the biological usefulness of the benchmark tasks.

### 8.4 Cluster annotation

Script:

```text
scripts/04_annotate_clusters.py
```

Outputs:

```text
results/tables/cluster_annotations.csv
data/processed/pbmc3k_annotated.h5ad
```

Important note:

The annotations are marker-derived working labels, not experimentally validated ground truth.

---

## 9. Visual Results

The project includes UMAP visualisations for both the unsupervised Leiden clustering output and the marker-derived biological annotation layer.

### 9.1 UMAP by Leiden Cluster

![UMAP by Leiden Cluster](results/figures/umap_by_leiden.png)

This figure shows PBMC3k cells grouped by Leiden cluster after preprocessing, PCA, neighbour graph construction, and UMAP embedding.

### 9.2 UMAP by Marker-Derived Annotation

![UMAP by Marker-Derived Annotation](results/figures/umap_by_annotation.png)

This figure shows the same UMAP embedding coloured by marker-derived working cell-type annotations.

Visual outputs are generated by:

```text
scripts/09_generate_visual_outputs.py
```

The benchmark task summary table is saved at:

```text
results/tables/benchmark_task_summary.csv
```

---

## 10. Cluster Annotation Summary

| Cluster | Working annotation | Confidence | Supporting marker evidence                |
| ------: | ------------------ | ---------- | ----------------------------------------- |
|       0 | T cells            | Medium     | CD3D, CD3E, IL7R, LTB                     |
|       1 | CD14+ monocytes    | High       | LYZ, S100A8, S100A9, FCN1, CST3           |
|       2 | B cells            | High       | CD79A, CD79B, MS4A1, CD74, HLA-DRA        |
|       3 | Cytotoxic T cells  | Medium     | CD3D, CCL5, NKG7, GZMA, CST7              |
|       4 | NK cells           | High       | NKG7, GNLY, GZMB, PRF1, FGFBP2            |
|       5 | FCGR3A+ monocytes  | High       | LST1, FCER1G, FCGR3A, AIF1, IFITM3        |
|       6 | Dendritic cells    | Medium     | HLA-DPA1, HLA-DPB1, HLA-DRA, FCER1A, CST3 |
|       7 | Platelets          | High       | PPBP, PF4, GNG11, SDPR, NRGN              |
|       8 | Cycling cells      | Medium     | KIAA0101, TYMS, ZWINT, TUBB               |

---

## 11. Benchmark Design

The benchmark contains three task families.

### 11.1 Hidden Cluster Annotation

The solver receives marker genes for a cluster and must infer the most likely cell type.

Public input:

```text
benchmark_tasks/public/hidden_cluster_annotation_tasks.json
```

Hidden answer key:

```text
benchmark_tasks/hidden/hidden_cluster_annotation_answers.json
```

Number of tasks:

```text
9
```

### 11.2 Marker Contradiction Detection

The solver receives marker evidence that may create ambiguity or contradiction between related immune-cell labels.

Public input:

```text
benchmark_tasks/public/marker_contradiction_tasks.json
```

Hidden answer key:

```text
benchmark_tasks/hidden/marker_contradiction_answers.json
```

Number of tasks:

```text
2
```

### 11.3 Masked Marker Recovery

The solver receives partially masked marker evidence and must recover the likely cell identity using remaining supporting evidence.

Public input:

```text
benchmark_tasks/public/masked_marker_recovery_tasks.json
```

Hidden answer key:

```text
benchmark_tasks/hidden/masked_marker_recovery_answers.json
```

Number of tasks:

```text
5
```

### 11.4 Benchmark Summary

| Task family                    | Public tasks | Hidden answers | Purpose                                                |
| ------------------------------ | -----------: | -------------: | ------------------------------------------------------ |
| Hidden cluster annotation      |            9 |              9 | Test marker-to-cell-type reasoning                     |
| Marker contradiction detection |            2 |              2 | Test ability to detect conflicting biological evidence |
| Masked marker recovery         |            5 |              5 | Test reasoning under incomplete marker evidence        |
| Total                          |           16 |             16 | Prototype benchmark suite                              |

---

## 12. Oracle Outputs

Oracle outputs provide structured reference responses for benchmark tasks.

Script:

```text
scripts/06_generate_oracle_outputs.py
```

Outputs:

```text
benchmark_tasks/oracle_outputs/hidden_cluster_annotation_oracle_outputs.json
benchmark_tasks/oracle_outputs/marker_contradiction_oracle_outputs.json
benchmark_tasks/oracle_outputs/masked_marker_recovery_oracle_outputs.json
```

Oracle outputs include:

* predicted label;
* supporting genes;
* confidence level;
* rationale.

Example oracle response shape:

```json
{
  "task_id": "task_hidden_annotation_cluster_0",
  "oracle_response": {
    "predicted_label": "T cells",
    "supporting_genes": ["CD3D", "CD3E", "IL7R", "LTB"],
    "confidence": "medium",
    "rationale": "T-cell markers present; broad cluster likely includes naive/memory T cells."
  }
}
```

---

## 13. Validators and Scoring

Validators are implemented in:

```text
src/scbench/validators.py
```

Scoring workflow:

```text
src/scbench/scoring.py
scripts/07_score_solver_answers.py
```

The validators score solver answers using structured criteria.

### 13.1 Hidden cluster annotation scoring

| Component               | Weight |
| ----------------------- | -----: |
| Correct label           |   0.60 |
| Supporting gene overlap |   0.30 |
| Rationale present       |   0.10 |

Correct threshold:

```text
0.75
```

### 13.2 Marker contradiction scoring

| Component                      | Weight |
| ------------------------------ | -----: |
| Correct contradiction decision |   0.50 |
| Contradiction type overlap     |   0.35 |
| Rationale present              |   0.15 |

Correct threshold:

```text
0.75
```

### 13.3 Masked marker recovery scoring

| Component                | Weight |
| ------------------------ | -----: |
| Correct label            |   0.50 |
| Supporting gene overlap  |   0.25 |
| Uncertainty acknowledged |   0.15 |
| Rationale present        |   0.10 |

Correct threshold:

```text
0.75
```

Sample solver answers are stored in:

```text
sample_solver_answers/sample_answers.json
```

Sample score report:

```text
results/reports/sample_solver_score_report.json
```

Current sample scoring result:

| Metric                 | Value |
| ---------------------- | ----: |
| Total sample answers   |     3 |
| Correct sample answers |     3 |
| Accuracy               |   1.0 |
| Average score          | 0.923 |

---

## 14. Calibration Framework

Calibration assets are generated by:

```text
scripts/08_generate_calibration_assets.py
```

Outputs:

```text
benchmark_tasks/calibration_logs/calibration_log_template.json
benchmark_tasks/calibration_logs/initial_task_difficulty_review.json
```

The current calibration layer is a design-stage framework.

It documents:

* task family;
* expected difficulty;
* likely failure modes;
* calibration risks;
* recommended next improvements;
* future human/model evaluation fields.

Important limitation:

This is not yet an empirical frontier-model calibration study. Empirical calibration would require running the benchmark against multiple human solvers or model systems, recording attempts, measuring accuracy, analysing failure patterns, and revising task difficulty based on observed results.

The calibration asset generation is deterministic. Re-running the calibration script does not create Git timestamp noise.

---

## 15. Reproducibility

This project supports local, Docker-based, and CI-backed reproducibility.

### 15.1 Local environment

Create the Conda environment:

```bash
mamba env create -f environment.yml
```

Activate the environment:

```bash
conda activate sc-marker-benchmark
```

Run all tests locally:

```bash
PYTHONPATH=src pytest -q
```

Current full local test status:

```text
36 passed
```

### 15.2 Makefile commands

Run unit tests:

```bash
make unit-test
```

Run integration tests:

```bash
make integration-test
```

Run all tests:

```bash
make test
```

Run the full local pipeline:

```bash
make pipeline
```

Pipeline target sequence:

```text
download → preprocess → markers → annotate → tasks → oracles → score → calibration → visuals → test
```

### 15.3 Docker reproducibility

Build the Docker image:

```bash
make docker-build
```

Run Docker unit tests:

```bash
make docker-test
```

Run the full pipeline inside Docker:

```bash
make docker-pipeline-test
```

The full Docker pipeline test regenerates the dataset, preprocessing outputs, marker tables, annotations, benchmark tasks, oracle outputs, scoring report, calibration assets, visual outputs, and test results inside a clean container.

This proves that the project is not dependent only on local files already existing on the developer machine.

### 15.4 GitHub Actions CI

GitHub Actions CI runs unit tests automatically on push and pull request events against the `main` branch.

Workflow file:

```text
.github/workflows/ci.yml
```

The CI badge at the top of this README reflects the latest workflow status.

---

## 16. Unit and Integration Test Strategy

The project separates lightweight tests from data-dependent tests.

Unit tests do not require generated `.h5ad` files and are suitable for fast CI validation.

Integration tests require generated data files and full pipeline outputs.

This split was introduced after Docker testing exposed that the original tests assumed local generated data files already existed. The fix made the test strategy more realistic, reproducible, and CI-friendly.

---

## 17. Evidence and Review Trail

Evidence files are stored under:

```text
docs/evidence/
```

A full claim-to-evidence map is available at:

```text
docs/evidence_map.md
```

Important evidence files:

| Evidence file                                 | What it proves                      |
| --------------------------------------------- | ----------------------------------- |
| `01_project_tree.txt`                         | Initial project structure           |
| `02_pytest_day1.txt`                          | Early baseline test status          |
| `03_dataset_load_output.txt`                  | PBMC3k dataset loading worked       |
| `06_preprocessing_output.txt`                 | Preprocessing pipeline output       |
| `08_marker_ranking_output.txt`                | Marker ranking completed            |
| `09_annotation_output.txt`                    | Cluster annotation completed        |
| `11_benchmark_generation_output.txt`          | Benchmark task generation completed |
| `14_oracle_generation_output.txt`             | Oracle output generation completed  |
| `17_solver_scoring_output.txt`                | Solver scoring completed            |
| `21_calibration_assets_output.txt`            | Calibration assets generated        |
| `24_unit_tests_after_docker_split.txt`        | Unit tests after test split         |
| `25_integration_tests_after_docker_split.txt` | Integration tests after test split  |
| `26_docker_unit_test_output.txt`              | Docker unit tests completed         |
| `27_docker_full_pipeline_test_output.txt`     | Full Docker pipeline completed      |
| `28_visual_outputs.txt`                       | Visual outputs generated            |

The evidence files are intentionally kept in the repository to show that the project was built, tested, debugged, and improved through verifiable stages.

---

## 18. Engineering Challenges and Fixes

This section documents real issues encountered during the project and how they were resolved.

### 18.1 Accidental Git repository creation in the wrong directory

Git was initially created outside the intended project folder.

Why this mattered:

* It risked tracking unrelated files.
* It made the repository boundary unclear.
* It could have caused accidental commits from outside the project.

Fix:

* Removed the mistaken Git setup.
* Recreated the project inside the correct project directory.
* Reinitialised Git inside the intended repository root.
* Verified the repository with `pwd`, `ls`, and `git status`.

Result:

The final repository is clean, correctly scoped, and published to GitHub.

### 18.2 Raw marker ranking was dominated by noisy genes

The first marker ranking outputs contained many ribosomal and broadly expressed genes.

Why this mattered:

* These genes are often less useful for cell-type reasoning.
* They can make benchmark tasks biologically weaker.
* They reduce the clarity of marker-to-cell-type inference.

Fix:

* Added marker filtering logic.
* Removed genes beginning with `RPS`, `RPL`, and `MT-`.
* Removed selected broadly expressed genes such as `MALAT1`, `TPT1`, `EEF1A1`, and `B2M`.
* Preserved both raw and filtered marker tables.

Result:

The benchmark tasks became more biologically meaningful while preserving the raw marker output for transparency.

### 18.3 Cluster labels could be overstated as ground truth

Marker-derived annotations are useful but are not equivalent to experimentally validated labels.

Why this mattered:

* Overclaiming would weaken scientific credibility.
* Benchmark answers should not pretend to be absolute truth when they are derived from marker evidence.
* Related immune-cell populations can share markers.

Fix:

* Described cluster labels as marker-derived working annotations.
* Added confidence levels.
* Used supporting genes and rationales in oracle outputs.
* Documented the limitation clearly.

Result:

The project remains scientifically honest while still producing useful benchmark assets.

### 18.4 Hidden answer files were initially blocked by `.gitignore`

The benchmark design requires both public tasks and hidden answer files, but hidden answer files were initially at risk of being ignored by Git.

Why this mattered:

* The benchmark would be incomplete without answer keys.
* Scoring could not be reproduced reliably.
* Oracle generation and validation depend on hidden answer files.

Fix:

* Adjusted `.gitignore`.
* Kept broad protection for generated files.
* Explicitly allowed required hidden JSON answer files and oracle outputs to be tracked.

Result:

The repository contains the benchmark assets needed for reproducible scoring.

### 18.5 Docker tests failed because generated `.h5ad` files were excluded

The Docker image intentionally excluded large generated `.h5ad` files, but some tests expected those files to already exist.

Why this mattered:

* Excluding large generated data is good repository hygiene.
* However, tests that require generated files should not be treated as clean-container unit tests.
* The failure exposed a real reproducibility weakness.

Fix:

* Added `pytest.ini`.
* Marked data-dependent tests as `integration`.
* Added Makefile targets for unit tests, integration tests, Docker unit tests, and Docker full-pipeline testing.
* Changed Docker’s default test command to run non-integration tests.
* Added a full Docker pipeline test to regenerate data from scratch.

Result:

The project now supports both fast Docker unit testing and full clean-container pipeline reproducibility.

### 18.6 Docker full pipeline initially failed because `make` was missing

The Docker container initially did not include the Linux `make` package.

Why this mattered:

* The Makefile is the main project command interface.
* Docker needed to support the same command interface as local development.

Fix:

* Updated the Dockerfile to install `make`.
* Also installed `tree` for evidence generation support.
* Rebuilt the Docker image.
* Re-ran Docker tests.

Result:

The Docker container can run the project’s Makefile targets.

### 18.7 Calibration generation created timestamp noise

The calibration script originally used dynamic timestamps, which caused tracked JSON files to appear modified after repeated runs.

Why this mattered:

* It made the Git working tree dirty after routine commands.
* It created unnecessary version-control noise.
* It reduced reproducibility cleanliness.

Fix:

* Removed dynamic timestamp generation from calibration assets.
* Made calibration output deterministic.
* Verified that re-running the calibration script leaves the working tree clean.

Result:

Calibration assets are now stable and reproducible across repeated runs.

### 18.8 README initially lagged behind the actual project state

After adding Docker, visual outputs, CI, and evidence mapping, the README still described some completed items as future work.

Why this mattered:

* A stale README weakens first impressions.
* It can make a completed project look unfinished.
* Reviewers depend on the README to understand project status quickly.

Fix:

* Rewrote and polished the README.
* Added CI badge.
* Added UMAP visual results.
* Updated project status.
* Linked the evidence map.
* Corrected section numbering.
* Updated limitations and future-work sections to reflect the actual current state.

Result:

The README now reflects the completed project accurately and professionally.

---

## 19. Current Project Status

| Area                              | Status              |
| --------------------------------- | ------------------- |
| Data download                     | Complete            |
| Scanpy preprocessing              | Complete            |
| Marker ranking                    | Complete            |
| Marker filtering                  | Complete            |
| Cluster annotation                | Complete            |
| Visual outputs                    | Complete            |
| Benchmark task generation         | Complete            |
| Hidden answer generation          | Complete            |
| Oracle output generation          | Complete            |
| Validators                        | Complete            |
| Solver scoring                    | Complete            |
| Calibration framework             | Complete            |
| Deterministic calibration outputs | Complete            |
| Unit/integration test split       | Complete            |
| Docker unit testing               | Complete            |
| Docker full pipeline test         | Complete            |
| GitHub repository                 | Published           |
| GitHub Actions CI                 | Complete            |
| Evidence map                      | Complete            |
| README visual rendering           | Complete            |
| Empirical benchmark calibration   | Not yet implemented |
| Multi-dataset benchmark expansion | Not yet implemented |

---

## 20. Limitations

This project is intentionally transparent about its current limitations.

1. The benchmark is based on PBMC3k only.
2. Cluster annotations are marker-derived working labels, not experimentally validated ground truth.
3. The benchmark contains 16 tasks, so it is a prototype-scale benchmark.
4. The calibration framework is design-stage, not empirical calibration across multiple solvers or models.
5. The visual layer includes UMAP figures but does not yet include richer marker-gene dot plots or heatmaps.
6. The workflow is suitable for PBMC3k scale but would need memory and performance review for much larger datasets.
7. Scanpy warnings about sparse densification and Leiden backend changes should be addressed in future hardening.
8. GitHub Actions currently runs unit tests; full Docker pipeline CI remains a future hardening improvement.

---

## 21. Future Improvements

Planned improvements include:

1. Add marker-gene heatmaps or dot plots.
2. Add optional Docker-based CI for full-pipeline validation.
3. Add empirical calibration using human or model solvers.
4. Add more datasets beyond PBMC3k.
5. Add stronger task difficulty tiers based on observed solver performance.
6. Add richer scoring reports with per-task error analysis.
7. Add performance profiling for larger datasets.
8. Package the benchmark as an installable Python package.
9. Add more benchmark task families beyond marker-gene reasoning.
10. Add comparative solver evaluation across multiple human or model systems.

---

## 22. Quickstart

Clone the repository:

```bash
git clone https://github.com/gbadedata/single-cell-marker-reasoning-benchmark.git
cd single-cell-marker-reasoning-benchmark
```

Create the environment:

```bash
mamba env create -f environment.yml
conda activate sc-marker-benchmark
```

Run tests:

```bash
PYTHONPATH=src pytest -q
```

Run the full local pipeline:

```bash
make pipeline
```

Build Docker image:

```bash
make docker-build
```

Run Docker unit tests:

```bash
make docker-test
```

Run the full Docker pipeline:

```bash
make docker-pipeline-test
```

---

## 23. Main Technologies

| Category             | Tools                                                             |
| -------------------- | ----------------------------------------------------------------- |
| Language             | Python                                                            |
| Single-cell analysis | Scanpy, AnnData                                                   |
| Data structures      | pandas, NumPy                                                     |
| Testing              | pytest                                                            |
| Reproducibility      | Conda, Mamba, Docker                                              |
| Automation           | Makefile                                                          |
| CI                   | GitHub Actions                                                    |
| Version control      | Git, GitHub                                                       |
| Benchmark design     | Public tasks, hidden answers, oracle outputs, validators, scoring |

---

## 24. Reviewer Guide

A reviewer can inspect the project quickly in this order:

1. Read this README for the project overview.
2. Check the CI badge for current unit-test status.
3. Review the UMAP visual outputs in the Visual Results section.
4. Open `docs/evidence_map.md` to map claims to files.
5. Inspect `benchmark_tasks/public/` for public benchmark tasks.
6. Inspect `benchmark_tasks/hidden/` for answer keys.
7. Inspect `benchmark_tasks/oracle_outputs/` for oracle responses.
8. Inspect `src/scbench/validators.py` and `src/scbench/scoring.py` for scoring logic.
9. Run `make unit-test` for fast tests.
10. Run `make docker-pipeline-test` for full clean-container reproducibility.

---

## 25. Project Outcome

This project demonstrates how a single-cell RNA-seq analysis can be transformed into a reproducible benchmark-engineering system.

It shows:

* scientific data processing;
* marker-gene reasoning;
* careful marker-derived annotation;
* benchmark task construction;
* hidden answer management;
* oracle response generation;
* validator-based scoring;
* calibration planning;
* deterministic asset generation;
* Docker reproducibility;
* automated CI;
* visual result generation;
* evidence-backed documentation.

The project is complete as a portfolio-ready prototype benchmark system. It includes analysis, benchmark assets, tests, Docker validation, CI, visual outputs, and evidence mapping. The remaining work is not basic completion work; it is research and production hardening: empirical calibration, additional datasets, richer marker-gene visualisation, optional full-pipeline Docker CI, performance profiling, packaging, and broader solver evaluation.
