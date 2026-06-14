.PHONY: test unit-test integration-test download preprocess markers annotate tasks oracles score calibration visuals pipeline evidence docker-build docker-test docker-pipeline-test clean

test:
	PYTHONPATH=src pytest -q

unit-test:
	PYTHONPATH=src pytest -q -m "not integration"

integration-test:
	PYTHONPATH=src pytest -q -m "integration"

download:
	PYTHONPATH=src python scripts/01_download_data.py

preprocess:
	PYTHONPATH=src python scripts/02_preprocess.py

markers:
	PYTHONPATH=src python scripts/03_rank_markers.py

annotate:
	PYTHONPATH=src python scripts/04_annotate_clusters.py

tasks:
	PYTHONPATH=src python scripts/05_generate_benchmark_tasks.py

oracles:
	PYTHONPATH=src python scripts/06_generate_oracle_outputs.py

score:
	PYTHONPATH=src python scripts/07_score_solver_answers.py

calibration:
	PYTHONPATH=src python scripts/08_generate_calibration_assets.py

visuals:
	PYTHONPATH=src python scripts/09_generate_visual_outputs.py

pipeline: download preprocess markers annotate tasks oracles score calibration visuals test

evidence:
	mkdir -p docs/evidence
	tree -L 4 > docs/evidence/project_tree_latest.txt
	PYTHONPATH=src pytest -q > docs/evidence/pytest_latest.txt

docker-build:
	docker build -t single-cell-marker-benchmark:latest .

docker-test:
	docker run --rm single-cell-marker-benchmark:latest

docker-pipeline-test:
	docker run --rm single-cell-marker-benchmark:latest conda run --no-capture-output -n sc-marker-benchmark bash -lc "make pipeline"

clean:
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
