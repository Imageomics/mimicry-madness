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
    parser.add_argument("--pca_1", type=int, default=0)
    parser.add_argument("--pca_2", type=int, default=1)
    parser.add_argument("--metadata", type=str)

    args = parser.parse_args()
    
    df = pd.read_csv(args.metadata)

    data = torch.load(args.emb_src)
    paths, all_embeddings = data

    normalized_features = StandardScaler().fit_transform(all_embeddings)
    pca = PCA()
    pca_values = pca.fit_transform(normalized_features)
    
    pca_x = args.pca_1
    pca_y = args.pca_2
    
    name_no_ext = df["filename"].str.split(".").str[0].tolist()
    plot_data = defaultdict(list)
    for i, vals in enumerate(pca_values):
        path = paths[i]
        name = path.split(".")[0].split(os.path.sep)[-1]
        try:
            index = name_no_ext.index(name)
        except:
            print(f"{name} failed to find metadata.")
        label = df.iloc[index]["label"]
        plot_data[label].append(vals)
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    for label, pdata in plot_data.items():
        pdata = np.stack(pdata)
        plt.plot(pdata[:, pca_x], pdata[:, pca_y], 'o', markersize=6, alpha=0.5, label=label)
    plt.title(f'PCA Plot (PC{pca_x + 1} vs PC{pca_y + 1})')
    plt.xlabel(f"Principal Component {pca_x + 1}")
    plt.ylabel(f"Principal Component {pca_y + 1}")
    plt.grid()
    plt.legend()

    fig.show()
    plt.savefig(args.pca_dest)