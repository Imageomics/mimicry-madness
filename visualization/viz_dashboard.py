from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from PIL import Image
from tqdm import tqdm
import torch
from glob import glob
from sklearn.manifold import TSNE

app = Dash(__name__)

embedding_options = glob('./data/embeddings/*.pt')
csv_options = glob('./data/*.csv')


if len(embedding_options) == 0:
    raise ValueError("No embedding files found! Please generate embeddings before using this visualization file. See README.md for directions")
if len(csv_options) == 0:
    raise ValueError("No CSV files found! Please ensure corresponding CSVs are in the data folder before using this visualization file.")


app.layout = html.Div([
    html.H2('Interactive PCA'),
    html.P("Select embedding data to load:"),
    dcc.Dropdown(
        id="data_source",
        options=embedding_options,
        value=embedding_options[0],
        clearable=False,
    ),
    html.P("Select corresponding CSV metadata to load:"),
    dcc.Dropdown(
        id="metadata_source",
        options=csv_options,
        value=csv_options[0],
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
    Input("metadata_source", "value"),
    Input("visualization_type", "value"))
def display_embedding(embedding, metadata, viz_type):

    (img_paths, img_features) = torch.load(embedding)

    normalized_features = StandardScaler().fit_transform(img_features)

    if viz_type == "tsne":
        tsne = TSNE(n_components=2, random_state=42)
        values = tsne.fit_transform(normalized_features)
    else:
        # PCA
        pca = PCA()
        values = pca.fit_transform(normalized_features)

    df = pd.read_csv(metadata)
    labels = []
    sci_names = []
    
    if ("mimicry_status" in list(df.columns)) and ("sci_name" in list(df.columns)):
        for filepath in img_paths:
            label = df.loc[df["filepath"] == filepath, "mimicry_status"].values[0]
            sci_name = df.loc[df["filepath"] == filepath, "sci_name"].values[0]
            labels.append(label)
            sci_names.append(sci_name)
    
        fig = px.scatter(x=values[:, 0],
                        y=values[:, 1],
                        color = labels,
                        color_discrete_sequence = px.colors.qualitative.Bold,
                        hover_data={'image': img_paths,
                                    'sci_name': sci_names,
                                    'mimic_stat': labels})
    else:
        for filepath in img_paths:
            label = df.loc[df["filepath"] == filepath, "label"].values[0]
            labels.append(label)
    
        fig = px.scatter(x=values[:, 0],
                        y=values[:, 1],
                        color = labels,
                        color_discrete_sequence = px.colors.qualitative.Bold,
                        hover_data={'image': img_paths,
                                    'label': labels})


    #fig.update_traces(hoverinfo="none", hovertemplate=None)

    """ for img_path, v in zip(img_paths, values):
        fig.add_layout_image(
            x=v[0],
            y=v[1],
            source=Image.open(img_path),
            xanchor="center",
            yanchor="middle",
            sizex=1,
            sizey=1,
        ) """

    return fig


app.run(debug=True)
