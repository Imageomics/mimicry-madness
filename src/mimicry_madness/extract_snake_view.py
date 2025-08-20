from argparse import ArgumentParser
from pathlib import Path

from PIL import Image
import pandas as pd
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument("--src_dir", type=str)
parser.add_argument("--dest_dir", type=str)
parser.add_argument("--metadata", type=str)
parser.add_argument("--view", type=str, choices=["dorsal", "ventral"], default="dorsal")
args = parser.parse_args()

metadata_df = pd.read_csv(args.metadata)

dest_dir = Path(args.dest_dir)
dest_dir.mkdir(exist_ok=True)

for i, row in tqdm(metadata_df.iterrows(), total=metadata_df.shape[0], desc="Filtering images"):
    coll = row["collection"]
    num = row["number"]
    genus = row["genus"]
    sp_ep = row["specific_epithet"]
    fn = row["filename"]
    
    if row["view"] != args.view:
        continue
    
    if num == "?":
        num = "unknown"
        
    if num == "unknown":
        fn = fn.split(".")[0] + ".JPG.png"
    else: 
        fn = fn.split(".")[0] + ".png"
        
    filename = "_".join([coll, num, genus, sp_ep, fn])
    path = Path(args.src_dir, filename)
    try:
        img = Image.open(path)
        img.save(Path(dest_dir, filename))
    except:
        print(f"Failed loading for: {path}")
    
