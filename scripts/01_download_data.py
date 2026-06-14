from pathlib import Path
import scanpy as sc


def main() -> None:
    raw_path = Path("data/raw/pbmc3k_raw.h5ad")
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    print("Downloading/loading PBMC3k via scanpy.datasets.pbmc3k()...")
    adata = sc.datasets.pbmc3k()

    print(f"Loaded AnnData shape: {adata.shape}")
    print(f"obs columns: {list(adata.obs.columns)}")
    print(f"var columns: {list(adata.var.columns)}")

    adata.write_h5ad(raw_path)
    print(f"Saved raw dataset to: {raw_path}")


if __name__ == "__main__":
    main()
