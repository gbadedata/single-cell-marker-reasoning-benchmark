from scbench.analysis import rank_marker_genes


def main() -> None:
    adata, marker_df, filtered_df = rank_marker_genes()

    print("Marker ranking complete.")
    print(adata)
    print("Raw marker table shape:", marker_df.shape)
    print("Filtered marker table shape:", filtered_df.shape)
    print("Raw marker columns:", list(marker_df.columns))
    print("Clusters:", sorted(marker_df["group"].astype(str).unique().tolist()))

    print("\nTop filtered markers per cluster:")
    for cluster in sorted(filtered_df["group"].astype(str).unique().tolist()):
        genes = filtered_df[filtered_df["group"].astype(str) == cluster]["names"].head(10).tolist()
        print(f"Cluster {cluster}: {', '.join(genes)}")


if __name__ == "__main__":
    main()
