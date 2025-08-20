from argparse import ArgumentParser
from pathlib import Path

from tqdm import tqdm
from PIL import Image

from mimicry_madness.utils import tight_crop_rgba_image

parser = ArgumentParser()
parser.add_argument("--src_dir", type=str)
parser.add_argument("--dest_dir", type=str)
args = parser.parse_args()

src_dir = Path(args.src_dir)
dest_dir = Path(args.dest_dir)
dest_dir.mkdir(exist_ok=True)

path_data = []
for root, dirs, paths in src_dir.walk():
    for f in paths:
        path_data.append((root, f))
        
for root, f in tqdm(path_data, desc="Cropping and saving images"):
    img = Image.open(root / f)
    cropped_img = tight_crop_rgba_image(img)
    cropped_img.save(dest_dir / f)