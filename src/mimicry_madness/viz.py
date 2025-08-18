import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from PIL import Image
from tqdm import tqdm

def create_pca_image_plot(img_features, image_paths, pca_x=0, pca_y=1, plt_img_size=(256, 256), zoom=0.1):

    normalized_features = StandardScaler().fit_transform(img_features)
    pca = PCA()
    pca_values = pca.fit_transform(normalized_features)

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    plt.plot(pca_values[:, pca_x], pca_values[:, pca_y], 'o', markersize=2, alpha=0.5)
    plt.title(f'PCA Plot (PC{pca_x + 1} vs PC{pca_y + 1})')
    plt.xlabel(f"Principal Component {pca_x + 1}")
    plt.ylabel(f"Principal Component {pca_y + 1}")
    plt.grid()

    for i, path in tqdm(enumerate(image_paths), "Plotting PCA images"):
        image = Image.open(path)
        imagebox = OffsetImage(image.resize(plt_img_size), zoom=zoom)
        ab = AnnotationBbox(imagebox, (pca_values[i, pca_x], pca_values[i, pca_y]),
                            frameon=False, pad=0.5)
        plt.gca().add_artist(ab)

    return fig, ax