# Benchmark Design

## Purpose

The purpose of this benchmark is to evaluate whether a solver can reason over single-cell RNA-seq marker evidence rather than only perform shallow label matching.

## Task Types

### 1. Hidden Cluster Annotation

The solver receives:

- cluster ID
- top filtered marker genes
- candidate labels

The solver must infer the likely cell type and provide supporting marker evidence.

### 2. Marker Contradiction Detection

The solver receives marker profiles from two clusters.

The task is to detect whether the clusters show biological ambiguity or overlapping marker signatures.

### 3. Masked Marker Recovery

Canonical marker genes are deliberately removed.

The solver must infer the cell type from secondary marker evidence and state uncertainty.

## Public vs Hidden Files

Public files contain solver-facing task inputs.

Hidden files contain answer keys used to generate oracle responses.

Oracle outputs are derived from hidden answers and used for scoring.

## Validators

Validators score solver answers using:

- label correctness
- marker-gene overlap
- contradiction detection
- uncertainty acknowledgement
- rationale presence

## Calibration

The current calibration layer is a framework, not empirical frontier-model calibration.

The repository includes:

- calibration log template
- initial task difficulty review
- explicit limitation statement

Empirical calibration requires running tasks against human solvers or model systems and recording attempts.
