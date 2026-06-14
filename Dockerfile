FROM condaforge/miniforge3:latest

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends make tree && \
    rm -rf /var/lib/apt/lists/*

COPY environment.yml /app/environment.yml

RUN mamba env create -f environment.yml && \
    mamba clean --all --yes

SHELL ["conda", "run", "-n", "sc-marker-benchmark", "/bin/bash", "-c"]

COPY . /app

ENV PYTHONPATH=/app/src

CMD ["conda", "run", "--no-capture-output", "-n", "sc-marker-benchmark", "pytest", "-q", "-m", "not integration"]
