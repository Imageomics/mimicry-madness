from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from PIL import Image
from tqdm import tqdm
import torch
from glob import glob

app = Dash(__name__)

embedding_options = glob('./embeddings/*.pt')

app.layout = html.Div([
    html.H4('Interactive PCA'),
    html.P("Select embedding data to load:"),
    dcc.Dropdown(
        id="dropdown",
        options=embedding_options,
        value=embedding_options[0],
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"))
def display_embedding(embedding):


    (img_paths, img_features) = torch.load(embedding)

    normalized_features = StandardScaler().fit_transform(img_features)
    pca = PCA()
    pca_values = pca.fit_transform(normalized_features)

    fig = px.scatter(x=pca_values[:, 0], y=pca_values[:, 1], hover_data={'image': img_paths})
    return fig


app.run(debug=True)
