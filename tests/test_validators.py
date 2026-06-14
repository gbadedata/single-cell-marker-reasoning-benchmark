from scbench.validators import (
    normalize_label,
    score_gene_overlap,
    validate_hidden_cluster_annotation_answer,
    validate_marker_contradiction_answer,
    validate_masked_marker_recovery_answer,
)


def test_normalize_label_handles_synonyms():
    assert normalize_label("t cell") == "T cells"
    assert normalize_label("natural killer cells") == "NK cells"
    assert normalize_label("classical monocytes") == "CD14+ monocytes"


def test_score_gene_overlap_is_case_insensitive():
    submitted = ["cd3d", "IL7R"]
    oracle = ["CD3D", "CD3E", "IL7R", "LTB"]

    assert score_gene_overlap(submitted, oracle) == 0.5


def test_hidden_cluster_validator_accepts_good_answer():
    solver = {
        "predicted_label": "t cell",
        "supporting_genes": ["CD3D", "CD3E", "IL7R"],
        "confidence": "medium",
        "rationale": "CD3D, CD3E and IL7R support a T-cell identity.",
    }
    oracle = {
        "predicted_label": "T cells",
        "supporting_genes": ["CD3D", "CD3E", "IL7R", "LTB"],
        "confidence": "medium",
        "rationale": "T-cell markers present.",
    }

    result = validate_hidden_cluster_annotation_answer(solver, oracle)

    assert result["is_correct"] is True
    assert result["label_correct"] is True
    assert result["score"] >= 0.75


def test_hidden_cluster_validator_rejects_wrong_label():
    solver = {
        "predicted_label": "B cells",
        "supporting_genes": ["CD3D"],
        "confidence": "medium",
        "rationale": "Weak answer.",
    }
    oracle = {
        "predicted_label": "T cells",
        "supporting_genes": ["CD3D", "CD3E", "IL7R", "LTB"],
        "confidence": "medium",
        "rationale": "T-cell markers present.",
    }

    result = validate_hidden_cluster_annotation_answer(solver, oracle)

    assert result["is_correct"] is False
    assert result["label_correct"] is False


def test_marker_contradiction_validator_accepts_good_answer():
    solver = {
        "contradiction_detected": True,
        "contradiction_type": "T-cell and NK cytotoxic marker overlap",
        "supporting_genes": ["NKG7", "GZMA", "CD3D"],
        "rationale": "Cytotoxic genes overlap between both populations.",
    }
    oracle = {
        "contradiction_detected": True,
        "contradiction_type": "T-cell and NK-like cytotoxic marker overlap",
        "supporting_labels": ["Cytotoxic T cells", "NK cells"],
        "rationale": "Expected ambiguity.",
    }

    result = validate_marker_contradiction_answer(solver, oracle)

    assert result["is_correct"] is True
    assert result["contradiction_correct"] is True


def test_masked_marker_recovery_validator_accepts_good_answer():
    solver = {
        "predicted_label": "natural killer cells",
        "secondary_supporting_genes": ["PRF1", "CTSW", "CST7"],
        "uncertainty_comment": "Canonical markers were masked, so confidence is limited.",
        "rationale": "Secondary cytotoxic markers support NK identity.",
    }
    oracle = {
        "predicted_label": "NK cells",
        "masked_genes": ["GNLY", "GZMB", "NKG7"],
        "secondary_supporting_genes": ["PRF1", "CTSW", "CST7", "HLA-C"],
        "uncertainty_comment": "Expected uncertainty.",
        "rationale": "Oracle rationale.",
    }

    result = validate_masked_marker_recovery_answer(solver, oracle)

    assert result["is_correct"] is True
    assert result["label_correct"] is True
    assert result["score"] >= 0.75
