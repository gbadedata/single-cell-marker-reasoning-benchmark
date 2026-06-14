from scbench.preprocessing import preprocess_pbmc3k


def main() -> None:
    adata = preprocess_pbmc3k()
    print("Processed AnnData:")
    print(adata)
    print("Shape:", adata.shape)
    print("obs columns:", list(adata.obs.columns))
    print("var columns:", list(adata.var.columns))
    print("obsm keys:", list(adata.obsm.keys()))
    print("uns keys:", list(adata.uns.keys()))
    print("Leiden clusters:", sorted(adata.obs["leiden"].unique().tolist()))


if __name__ == "__main__":
    main()
