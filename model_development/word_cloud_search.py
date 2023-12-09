import os
import gradio as gr
import scipy.spatial
import numpy as np
import psycopg2
import pandas as pd
from sentence_transformers import SentenceTransformer
import scipy.spatial
from sklearn.manifold import TSNE
import plotly.graph_objs as go
import pickle

# Initialize pre-trained BERT model
embedder = SentenceTransformer('bert-base-nli-mean-tokens')

# Load embeddings from file or calculate them (takes a while)
load_embeddings = True
embeddings_file = 'corpus_embeddings.pkl'

# Database connection parameters
db_params = {
    'dbname': 'movie_db',
    'user': 'postgres',
    'password': os.environ['POSTGRES_PASSWORD'],
    'host': '49.13.1.33',
    'port': '5333'
}

# Connection
conn = psycopg2.connect(**db_params)


def query_db(sql_query, conn):
    return pd.read_sql_query(sql_query, conn)


# Select all movie titles
sql_query = """
SELECT title
FROM movies
"""
movie_titles = query_db(sql_query, conn)

# Corpus with example sentences
corpus = movie_titles['title']

if load_embeddings:
    # Load embeddings from file
    with open(embeddings_file, 'rb') as file:
        corpus_embeddings = pickle.load(file)
else:
    # Calculate embeddings
    corpus_embeddings = embedder.encode(corpus)

    # Save embeddings to file
    with open(embeddings_file, 'wb') as file:
        pickle.dump(corpus_embeddings, file)


def reduce_dimensions_and_plot(query_embedding, top_n, additional_k):
    # Indices of the top n similar movies
    distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    # Queried movie(s)
    query_id = results[0:1][0][0]

    # Correctly extract top_n_indices and additional_indices
    top_n_indices = [idx for idx, _ in results[1:top_n + 1]]
    additional_indices = [idx for idx, _ in results[top_n + 1:top_n + additional_k + 1]]

    # Combine indices and extract corresponding embeddings
    combined_indices = np.concatenate(([query_id], top_n_indices, additional_indices))  # 0 is for the queried movie
    combined_embeddings = np.vstack((query_embedding, corpus_embeddings[combined_indices]))

    # Reduce dimensions
    tsne = TSNE(n_components=3, random_state=0)
    reduced_embeddings = tsne.fit_transform(combined_embeddings)

    # Extract titles for the plot
    titles = [corpus[i] for i in combined_indices]

    # Plotting with Plotly
    trace_query = go.Scatter3d(
        x=[reduced_embeddings[0, 0]],
        y=[reduced_embeddings[0, 1]],
        z=[reduced_embeddings[0, 2]],
        mode='markers+text',
        marker=dict(size=10, color='purple'),
        name='Queried Movie',
        text=[titles[0]],
        textposition='top center'
    )

    trace_similar = go.Scatter3d(
        x=reduced_embeddings[1:top_n + 1, 0],
        y=reduced_embeddings[1:top_n + 1, 1],
        z=reduced_embeddings[1:top_n + 1, 2],
        mode='markers+text',
        marker=dict(size=8, color='red'),
        name=f'{top_n} Similar Movies',
        text=titles[1:top_n + 1],
        textposition='top center'
    )

    trace_additional = go.Scatter3d(
        x=reduced_embeddings[top_n + 1:, 0],
        y=reduced_embeddings[top_n + 1:, 1],
        z=reduced_embeddings[top_n + 1:, 2],
        mode='markers+text',
        marker=dict(size=6, color='blue'),
        name='Additional Movies',
        text=titles[top_n + 1:],
        textposition='top center'
    )

    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(title='TSNE 1'),
            yaxis=dict(title='TSNE 2'),
            zaxis=dict(title='TSNE 3')
        )
    )

    fig = go.Figure(data=[trace_query, trace_similar, trace_additional], layout=layout)

    return fig


