import open_clip
import os
import torch
from tqdm import tqdm
from PIL import Image

def generate_embeddings(img_src: str, emb_dest: str) -> None: 
    # Note: This code is not specifically designed/optimized to be used with lots and lots of images.
    # In the future, it may be necessary to refactor this to make it work better at scale.

    model, preprocess_train, preprocess_val = open_clip.create_model_and_transforms('hf-hub:imageomics/bioclip-2')
    tokenizer = open_clip.get_tokenizer('hf-hub:imageomics/bioclip-2')

    # First, load in images from location
    if os.path.isdir(img_src):
        image_paths = [os.path.join(img_src, f) for f in os.listdir(img_src) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    else:
        raise ValueError("img_src must be a directory containing images (.png, .jpg, .jpeg).")
    
    if len(image_paths) == 0:
        raise ValueError("No images (.png, .jpg, .jpeg) found in the specified directory.")
    
    all_embeddings = []
    
    # Now, generate embeddings for images and save them to destination
    for img_path in tqdm(image_paths, desc="Embedding images"):
        img = preprocess_val(Image.open(img_path)).unsqueeze(0)
        with torch.no_grad():
            emb = model.encode_image(img)
            
        emb = emb / emb.norm(dim=-1, keepdim=True)
        emb_dest_path = os.path.join(emb_dest, os.path.basename(img_path) + ".pt")

        all_embeddings.append((os.path.basename(img_path), emb))

    torch.save(all_embeddings, os.path.join(emb_dest, "embeddings.pt"))