from . import embeddings, viz
import matplotlib.pyplot as plt

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate image embeddings using Bioclip-2 model.")
    parser.add_argument("--img_src", type=str, help="Source directory containing images.")
    parser.add_argument("--emb_dest", type=str, help="Destination directory to save embeddings.")

    args = parser.parse_args()

    all_embeddings = embeddings.generate_embeddings(args.img_src, args.emb_dest)
    fig, ax = viz.create_pca_image_plot(all_embeddings[1], all_embeddings[0])

    fig.show()
    plt.savefig("pca_plot.png")