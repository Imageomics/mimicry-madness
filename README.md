# Mimicry Madness

Project repo for mimicry exploration during FuncaPalooza 2025! We're mostly focused on snakes and moths & wasps.

More coming soon!

## Using the package

This package can be utilized entirely from the command line! To generate the embeddings for a set of images, simply run: 

`uv run python -m mimicry_madness.embed ...`

with the following parameters:
- `--img_src`: folder to read images from (either .png, .jpg, or .jpeg format).
- `--emb_dest`: folder to save embedding file to (will be saved to `embeddings.pt`).
- `-b` or `--batch_size`: batch size to read images in.

To visualize the embeddings (in a very simple manner), use:

`uv run python -m mimicry_madness.visualize ...`

with the following parameters:
- `--emb_src`: path to `embeddings.pt` file.
- `--pca_dest`: path to save PCA plot to.

## Interactive Visualization

You can visualize the embeddings interactively by running the following command from the base folder of the repository:

`uv run python visualization/pca_dashboard.py`

You can then select the embeddings file you want to use (must be stored in the `embeddings` folder), and the PCA visualization will appear.
