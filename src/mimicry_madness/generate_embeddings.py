import open_clip
import os
import torch
from tqdm import tqdm
from PIL import Image

def generate_embeddings(img_src: str, emb_dest: str, batch_size: int) -> None: 
    # Note: This code is not specifically designed/optimized to be used with lots and lots of images.
    # In the future, it may be necessary to refactor this to make it work better at scale.

    # First, make folder for embeddings if doesnt exist
    os.makedirs(os.path.dirname(emb_dest), exist_ok=True)


    model, preprocess_train, preprocess_val = open_clip.create_model_and_transforms('hf-hub:imageomics/bioclip-2')
    tokenizer = open_clip.get_tokenizer('hf-hub:imageomics/bioclip-2')

    # First, load in images from location
    if os.path.isdir(img_src):
        image_paths = [os.path.join(img_src, f) for f in os.listdir(img_src) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    else:
        raise ValueError("img_src must be a directory containing images (.png, .jpg, .jpeg).")
    
    if len(image_paths) == 0:
        raise ValueError("No images (.png, .jpg, .jpeg) found in the specified directory.")
    
    all_embeddings = torch.tensor([])

    data_loader = torch.utils.data.DataLoader(image_paths, batch_size=batch_size, shuffle=False)

    # Now, generate embeddings for images and save them to destination
    for img_batch in tqdm(data_loader, desc="Embedding images"):
        imgs = [preprocess_val(Image.open(img_path)).unsqueeze(0) for img_path in img_batch]
        imgs = torch.cat(imgs, dim=0)
        with torch.no_grad():
            embs = model.encode_image(imgs)
            
        embs = embs / embs.norm(dim=1, keepdim=True)

        all_embeddings = torch.cat((all_embeddings, embs), dim=0)

    torch.save((image_paths, all_embeddings), emb_dest)

    return (image_paths, all_embeddings)