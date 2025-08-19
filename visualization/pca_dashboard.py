from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from PIL import Image
from tqdm import tqdm
import torch
from glob import glob
from sklearn.manifold import TSNE

app = Dash(__name__)

embedding_options = glob('./embeddings/*.pt')


if len(embedding_options) == 0:
    raise ValueError("No embedding files found! Please generate embeddings before using this visualization file. See README.md for directions")

app.layout = html.Div([
    html.H2('Interactive PCA'),
    html.P("Select embedding data to load:"),
    dcc.Dropdown(
        id="data_source",
        options=embedding_options,
        value=embedding_options[0],
        clearable=False,
    ),
    dcc.Dropdown(
        id="visualization_type",
        options=[
            {"label": "PCA", "value": "pca"},
            {"label": "t-SNE", "value": "tsne"},
        ],
        value="pca",
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("data_source", "value"),
    Input("visualization_type", "value"))
def display_embedding(embedding, viz_type):

    (img_paths, img_features) = torch.load(embedding)

    normalized_features = StandardScaler().fit_transform(img_features)

    if viz_type == "tsne":
        tsne = TSNE(n_components=2, random_state=42)
        values = tsne.fit_transform(normalized_features)
    else:
        # PCA
        pca = PCA()
        values = pca.fit_transform(normalized_features)

    fig = px.scatter(x=values[:, 0], y=values[:, 1], hover_data={'image': img_paths})


    fig.update_traces(hoverinfo="none", hovertemplate=None)

    for img_path, v in zip(img_paths, values):
        fig.add_layout_image(
            x=v[0],
            y=v[1],
            source=Image.open(img_path),
            xanchor="center",
            yanchor="middle",
            sizex=1,
            sizey=1,
        )

    return fig


app.run(debug=True)
