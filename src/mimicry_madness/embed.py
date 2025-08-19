from . import generate_embeddings

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate image embeddings using Bioclip-2 model.")
    parser.add_argument("--img_src", type=str, help="Source directory containing images.")
    parser.add_argument("--emb_dest", type=str, help="Destination filename to save embeddings.")
    parser.add_argument("-b", "--batch_size", type=int, default=32, help="Batch size for processing images.")

    args = parser.parse_args()

    all_embeddings = generate_embeddings.generate_embeddings(args.img_src, args.emb_dest, args.batch_size)