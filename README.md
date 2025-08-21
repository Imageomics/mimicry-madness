# Mimicry Madness

Project repo for mimicry exploration during FuncaPalooza 2025! We're mostly focused on snakes and moths & wasps.

More coming soon!

## Installation

Before using this package, please install uv (directions for doing so can be found [here](https://docs.astral.sh/uv/getting-started/installation/)).

All necessary packages should be automatically installed when `uv run` is used for the first time. 

## Using the package

This package can be utilized entirely from the command line! To generate the embeddings for a set of images, simply run: 

`uv run python -m mimicry_madness.embed ...`

with the following parameters:
- `--img_src`: folder to read images from (either .png, .jpg, or .jpeg format).
- `--emb_dest`: filepath to save embedding file to.
- `-b` or `--batch_size`: batch size to read images in.

To visualize the embeddings (in a very simple manner), use:

`uv run python -m mimicry_madness.visualize ...`

with the following parameters:
- `--emb_src`: path to `embeddings.pt` file.
- `--pca_dest`: path to save PCA plot to.

## Interactive Visualization

You can visualize the embeddings interactively by running the following command from the base folder of the repository:

`uv run python visualization/viz_dashboard.py`

Note that there must be an `embeddings/` directory within your local copy of the `data/` directory. Embeddings can be generated using the instructions above ([Using the package](#using-the-package)). You can then select the embeddings file you want to use (must be stored in the `embeddings` folder), and the PCA visualization will appear.
