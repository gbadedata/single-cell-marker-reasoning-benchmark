from scbench.annotation import create_annotation_table, add_annotations_to_anndata


def main() -> None:
    annotation_df = create_annotation_table()
    add_annotations_to_anndata()

    print("Cluster annotation table created.")
    print(annotation_df)

    print("\nSaved:")
    print("- results/tables/cluster_annotations.csv")
    print("- data/processed/pbmc3k_annotated.h5ad")


if __name__ == "__main__":
    main()
