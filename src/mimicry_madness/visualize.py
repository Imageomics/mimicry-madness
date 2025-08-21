from . import visualization_utils
import matplotlib.pyplot as plt
import os
import torch

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate image embeddings using Bioclip-2 model.")
    parser.add_argument("--emb_src", type=str, help="Source directory containing embeddings.")
    parser.add_argument("--pca_dest", type=str, help="Destination path to save PCA plot.")
    parser.add_argument("--img_size", type=int, default=256)
    parser.add_argument("--keep_aspect_ratio", action="store_true", default=False)

    args = parser.parse_args()

    all_embeddings = torch.load(args.emb_src)

    fig, ax = visualization_utils.create_pca_image_plot(
        all_embeddings[1],
         all_embeddings[0],
         plt_img_size=[args.img_size, args.img_size],
         maintain_aspect_ratio=args.keep_aspect_ratio,
    )

    fig.show()
    plt.savefig(args.pca_dest)