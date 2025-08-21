from collections import defaultdict
import matplotlib.pyplot as plt
import torch
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from PIL import Image
from tqdm import tqdm
import numpy as np
import pandas as pd


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate image embeddings using Bioclip-2 model.")
    parser.add_argument("--emb_src", type=str, help="Source directory containing embeddings.")
    parser.add_argument("--pca_dest", type=str, help="Destination path to save PCA plot.")
    parser.add_argument("--img_size", type=int, default=256)
    parser.add_argument("--metadata", type=str)

    args = parser.parse_args()
    
    df = pd.read_csv(args.metadata)

    data = torch.load(args.emb_src)
    paths, all_embeddings = data

    normalized_features = StandardScaler().fit_transform(all_embeddings)
    pca = PCA()
    pca_values = pca.fit_transform(normalized_features)
    
    pca_x = 0
    pca_y = 1
    
    name_no_ext = df["filename"].str.split(".").str[0].tolist()
    plot_data = defaultdict(list)
    for i, vals in enumerate(pca_values):
        path = paths[i]
        name = path.split(".")[0].split(os.path.sep)[-1]
        index = name_no_ext.index(name)
        mimicry_status = df.iloc[index]["mimicry_status"]
        plot_data[mimicry_status].append(vals)
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    for mimicry_status, pdata in plot_data.items():
        pdata = np.stack(pdata)
        plt.plot(pdata[:, pca_x], pdata[:, pca_y], 'o', markersize=6, alpha=0.5, label=mimicry_status)
    plt.title(f'PCA Plot (PC{pca_x + 1} vs PC{pca_y + 1})')
    plt.xlabel(f"Principal Component {pca_x + 1}")
    plt.ylabel(f"Principal Component {pca_y + 1}")
    plt.grid()
    plt.legend()

    fig.show()
    plt.savefig(args.pca_dest)