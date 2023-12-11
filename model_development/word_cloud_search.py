import os
import gradio as gr
import scipy.spatial
import numpy as np
import psycopg2
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
import scipy.spatial
from sklearn.manifold import TSNE
import plotly.graph_objs as go
import pickle

print("Loading BERT model...")
print('Using CUDA' if torch.cuda.is_available() else 'Using MPS')
# Initialize pre-trained BERT model
embedder = SentenceTransformer('bert-base-nli-mean-tokens', device='cuda' if torch.cuda.is_available() else 'mps')

# Load embeddings from file or calculate them (takes a while)
load_embeddings = True
embeddings_file = 'corpus_embeddings.pkl'
dataframe_file = 'movie_titles.pkl'

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


if load_embeddings:
    # Load embeddings from file
    with open(embeddings_file, 'rb') as file:
        corpus_embeddings = pickle.load(file)

    # Load movies
    with open(dataframe_file, 'rb') as file:
        movie_titles = pickle.load(file)

    corpus = movie_titles['title']
else:
    # Select all movie titles
    sql_query = """
    SELECT title
    FROM movies
    WHERE title IS NOT NULL AND budget > 0 AND revenue > 0 AND runtime >= 20
    """

    movie_titles = query_db(sql_query, conn)

    # Print how many movies are in the database
    print(f"There are {len(movie_titles)} movies in the database.")

    # All movie titles
    corpus = movie_titles['title']
    # Calculate embeddings otherwise
    corpus_embeddings = embedder.encode(corpus, show_progress_bar=True)

    # Save embeddings and movie titles
    with open(embeddings_file, 'wb') as file:
        pickle.dump(corpus_embeddings, file)

    with open(dataframe_file, 'wb') as file:
        pickle.dump(movie_titles, file)


def reduce_dimensions_and_plot(query_embedding, top_n, additional_k, query_title):
    # Indices of the top n similar movies
    distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

    # Sort results
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    # Extract indices
    top_n_indices = [idx for idx, _ in results[1:top_n + 1]]
    additional_indices = [idx for idx, _ in results[top_n + 1:top_n + additional_k + 1]]

    # Combine indices and extract corresponding embeddings
    combined_indices = np.concatenate(([0], top_n_indices, additional_indices))
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
        text=[query_title],
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


def find_similar_movies(movie_title, top_n, additional_k):
    # Embed the query
    query_embedding = embedder.encode(movie_title)

    # Calculate cosine distances
    distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

    # Sort results
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    # Check if the top result is the queried movie itself and adjust the range accordingly
    start_index = 0 if corpus[results[0][0]] != movie_title else 1

    # Create a dictionary for the top n movies with their cosine distances
    similar_movies_dict = {corpus[idx]: 1 - distance for idx, distance in results[start_index:top_n + start_index]}

    # 3D plot
    fig = reduce_dimensions_and_plot(query_embedding, top_n, additional_k, movie_title)

    # Return dictionary of similar movies and the plot
    return similar_movies_dict, fig


# Begin Interface

# Get the total number of movies
total_movies = len(movie_titles)

# Short description of the application
description = """
f## Description
This application allows you to find movies similar to a given title using BERT embeddings and TSNE for visualization.
Just enter a movie title, select the number of similar movies you want to see, and the application will display a list of similar movies along with a 3D plot.
Total number of movies in the database: {total_movies

## Selection of movies
The movies are selected from the database based on the following criteria:
- The movie title is not null
- The movie has a budget > 0
- The movie has a revenue > 0
- The movie has a runtime >= 20 minutes
"""

with gr.Blocks() as iface:
    gr.Markdown("# Movie Similarity Search")
    gr.Markdown(description)

    with gr.Row():
        movie_title = gr.Textbox(label="Enter a Movie Title")
        num_similar = gr.Slider(minimum=5, maximum=25, label="Number of most Similar Movies", step=1, value=5)
        num_additional = gr.Slider(minimum=25, maximum=50, label="Number of Additional Movies", step=1, value=30)
        submit_btn = gr.Button("Submit")

    with gr.Row():
        similar_movies = gr.Label(label="Similar Movies", min_width=300)
        visualization_plot = gr.Plot(label="Visualization Plot", min_width=1000)

    submit_btn.click(find_similar_movies, inputs=[movie_title, num_similar, num_additional], outputs=[similar_movies, visualization_plot])

    iface.launch(share=True)
