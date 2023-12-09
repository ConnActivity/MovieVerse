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


