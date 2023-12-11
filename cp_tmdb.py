# copy tmdb
import os
import pickle
import concurrent.futures
import time

import downloader
import insert

MOVIE_ID_LIMIT = 1250000
ROOT_PATH = "/media/maxi/mfloto_ext"


def download_movie_details(movie_id: int):
    if os.path.exists(f'{ROOT_PATH}/{movie_id}.pkl'):
        return
    try:
        movie = downloader.get_movie_details(movie_id)
        with open(f'{ROOT_PATH}/{movie_id}.pkl', 'wb') as f:
            pickle.dump(movie, f)
    except Exception as e:
        return


def download_all_movie_details():
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        future_movies = {executor.submit(download_movie_details, movie_id)
                         for movie_id in range(31700, MOVIE_ID_LIMIT + 1)}


def insert_movie_details(directory: str):
    all_movies = []
    for filename in os.listdir(directory):
        if filename.endswith(".pkl"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'rb') as f:
                movie = pickle.load(f)
                all_movies.append(movie)
    print(f"Inserting {len(all_movies)} movies into database")
    insert.insert_movie(all_movies)


def one_pickle(directory: str):
    all_movies = []
    for filename in os.listdir(directory):
        if filename.endswith(".pkl"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'rb') as f:
                movie = pickle.load(f)
                all_movies.append(movie)
    with open(directory + '/all_movies.pkl', 'wb') as f:
        movie = pickle.dump(all_movies, f)
        print(movie)


if __name__ == '__main__':
    #download_all_movie_details()
    #time_start = time.time()
    #insert_movie_details(ROOT_PATH + "/all_movies_tbdm")
    #time_end = time.time()
    #print(f"Inserting movies took {time_end - time_start} seconds to complete")
    one_pickle(ROOT_PATH + "/all_movies_tmdb")
