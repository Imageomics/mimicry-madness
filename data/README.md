# Mimicry Data

This repository explores two different mimicry datasets:

1. [Coral Snake Mimicry Complex](#coral-snake-mimicry-complex)
2. [Moth-Wasp Mimics](#moth-wasp-mimics)

Note that the data and metadata associated with this repository are licensed differently from the code in this repository and from each other; licensing is as indicated with the dataset.

More details about the data associated to each project component are provided below.

## Coral Snake Mimicry Complex

### FUNED Mimic Data

Images of specimens of coral snakes and their mimics from the FUNED natural history collection. These images were taken by Andressa Viol at the Fundação Ezequiel Dias. Each specimen image contains a 40% reflectance light UV standard and a color palette. The metadata file `metadata_FUNED_full.csv` contains the following columns:
- `specimen_id`: Int. ID of specimen in the collection (ID provided by FUNED).
- `filename`: String. Name of the photo file, default from camera.
- `collection`: String. Name of natural history collection (all `FUNED`).
- `view`: String. Position of snake (`dorsal`, `ventral`, or `side`). "dorsal" indicates the image was taken of the snake's back, while "ventral" means the image was taken with the snake lying belly-up, and "side" is a lateral view including both the dorsal and ventral scales.
- `mimicry_status`: String. Category of mimicry defined based on subjective evaluation of mimetic precision for average species phenotype (by Viol). Contains values `mimic`, `model`, and `bad mimic`.
- `genus`: String. Genus to which the specimen belongs, classification provided by the collection.
- `specific_epithet`: String. Species (specific epithet) to which the specimen belongs, classification provided by the collection.
- `image_date`: String. Date image was taken (`MM/DD/YYYY`).
- `notes`: String. Relevant notes about photography or specimen (not all full). May also included subspecies information where available (`venustissimus` is the only subspecies listed).

**License:** TBD

### Snake Mimic Toy Data

The metadata file `metadata_toy_dataset.csv` has a `mimicry_status` column which contains values `mimic`, `model`, `neither`, `bad mimic`.
These labels were added by Andressa Viol. 

Other column additions/modifications are:
- `View`: standardized to `Dorsal` or `Ventral`, where "Dorsal" indicates the image was taken of the snake's back, while "Ventral" means the image was taken with the snake lying belly-up.
- `filepath`: based on creating the embeddings from the repo data folder, so this is `images/snake_images/<Photo.File>_nobg.png`.
- `sci_name`: composed of `<Genus> <Species>` (columns in the original file).

**License:** The original metadata and associated images are from [Neotropical snake photographs](https://doi.org/10.7302/qta3-xs67) dataset[^1]. This data and associated metadata is [CC BY-NC](http://creativecommons.org/licenses/by-nc/4.0/).

## Moth-Wasp Mimics

`mw-metadata.csv` and `mw-nobg-metadata.csv`: metadata associated to the moths, wasps, and flies imaged and collected in Panama by Sol Carolina Parra Santos.

They are subdivided in two folders:
1. `SP_raw/`: Original images, taken of pinned specimens with color standard and scalebar. Associated metadata file is `mw-metadata.csv`.
2. `SP_nobackground/`: Segmented images. These are the original images with the background removed; this was completed by Parra Santos using batch editing on Photoshop.
Associated metadata file is `mw-nobg-metadata.csv`.

An initial metadata file was generated using [sum-buddy](https://github.com/Imageomics/sum-buddy) from the data folder, then separated out by file (using the `segmented` column values). Both metadata files thus have the following columns.
- `filepath`: String. Path to the image from the `data/` directory, includes the `filename`.
- `filename`: String. Filename of the image.
- `md5`: String. MD5 hash of the image, calculated at file generation using [`sum-buddy`](https://github.com/Imageomics/sum-buddy) package.
- `location`: String. Location of specimen collection: `Cerro azul`, `BCI`, `Gamboa`, or `Fortuna`.
- `label`: String. General label for the creature: `wasp`, `moth`, or `fly`.
- `segmented`: Boolean. `True` means these are the segmented images.

**License:**

## References

[^1]: University of Michigan, D. O. H., Davis Rabosky, A. R., Larson, J. G., Moore, T. Y., Curlis, J. D. (2021). _Neotropical snake photographs_ [Data set], University of Michigan - Deep Blue Data. https://doi.org/10.7302/qta3-xs67
