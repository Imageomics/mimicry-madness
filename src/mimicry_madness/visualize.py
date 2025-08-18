from . import visualization_utils
import matplotlib.pyplot as plt
import os
import torch

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate image embeddings using Bioclip-2 model.")
    parser.add_argument("--emb_src", type=str, help="Source directory containing embeddings.")
    parser.add_argument("--pca_dest", type=str, help="Destination path to save PCA plot.")

    args = parser.parse_args()

    all_embeddings = torch.load(args.emb_src)

    fig, ax = visualization_utils.create_pca_image_plot(all_embeddings[1], all_embeddings[0])

    fig.show()
    plt.savefig(args.pca_dest)