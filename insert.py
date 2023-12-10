import datetime
from typing import List, NamedTuple, Tuple

import psycopg2
from themoviedb.schemas import Movie, Person, Genre, Company
from themoviedb.schemas.countries import Country
from themoviedb.schemas.languages import Language


class MoviePopularity(NamedTuple):
    movie_id: int
    popularity: float
    vote_average: float


class MovieChange(NamedTuple):
    movie_id: int
    datapoint: str
    count: int


class MovieGenre(NamedTuple):
    movie_id: int
    genre_id: int


class MovieProductionCompany(NamedTuple):
    movie_id: int
    production_company_id: int


class MovieProductionCountry(NamedTuple):
    movie_id: int
    iso_3166_1: str


class MovieSpokenLanguage(NamedTuple):
    movie_id: int
    iso_639_1: str


conn = psycopg2.connect(url)
class PersonPopularity(NamedTuple):
    person_id: int
    popularity: float


cursor = conn.cursor()


def insert_movie(movies: List[Movie]):
    sql = """INSERT INTO movies 
            (id, title, original_title, imdb_id, overview, tagline, release_date, runtime, budget, 
            revenue, adult, video, backdrop_path, poster_path, homepage, status, original_language) 
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"""

    movies_data = [(movie.id, movie.title, movie.original_title, movie.imdb_id, movie.overview, movie.tagline,
                    movie.release_date, movie.runtime, movie.budget, movie.revenue, movie.adult, movie.video,
                    movie.backdrop_path, movie.poster_path, movie.homepage, movie.status, movie.original_language)
                   for movie in movies]

    cursor.executemany(sql, movies_data)
    conn.commit()

    # TODO: Should be faster without list comprehension when iterating over movies once
    insert_movie_popularity([MoviePopularity(movie.id, movie.popularity, movie.vote_average) for movie in movies])
    insert_genre([genre for movie in movies for genre in movie.genres])
    insert_movie_genres([MovieGenre(movie.id, genre.id) for movie in movies for genre in movie.genres])

    insert_production_company([company for movie in movies for company in movie.production_companies])
    insert_movie_production_companies(
        [MovieProductionCompany(movie.id, company.id) for movie in movies for company in movie.production_companies])

    insert_country([country for movie in movies for country in movie.production_countries])
    insert_movie_production_countries(
        [MovieProductionCountry(movie.id, country.iso_3166_1) for movie in movies for country in
         movie.production_countries])

    insert_spoken_language([language for movie in movies for language in movie.spoken_languages])
    insert_movie_spoken_languages(
        [MovieSpokenLanguage(movie.id, language.iso_639_1) for movie in movies for language in movie.spoken_languages])


def insert_movie_popularity(popularity_data: List[MoviePopularity]):
    sql = """INSERT INTO movies_popularity 
            (movie_id, popularity, vote_average, date) 
            VALUES 
            (%s, %s, %s, %s) ON CONFLICT (movie_id, date) DO NOTHING"""

    movie_popularity_data = [
        (popularity.movie_id, popularity.popularity, popularity.vote_average, datetime.date.today()) for popularity in
        popularity_data]

    cursor.executemany(sql, movie_popularity_data)
    conn.commit()


def insert_movie_change(movie_id: int, datapoint: str, count: int):
    sql = """INSERT INTO changes 
            (movie_id, datetime, datapoint, count)
            VALUES 
            (%s, %s, %s, %s) ON CONFLICT (movie_id, datetime, datapoint) DO NOTHING"""

    movie_change_data = (movie_id, datetime.date.today(), datapoint, count)

    cursor.execute(sql, movie_change_data)
    conn.commit()


def insert_genre(genres: List[Genre]):
    sql = """INSERT INTO genres 
            (id, name) 
            VALUES 
            (%s, %s) ON CONFLICT (id) DO NOTHING"""

    cursor.executemany(sql, [(genre.id, genre.name) for genre in genres])
    conn.commit()


def insert_movie_genres(movie_genres: List[MovieGenre]):
    sql = """INSERT INTO moviegenres 
            (movie_id, genre_id) 
            VALUES 
            (%s, %s) ON CONFLICT (movie_id, genre_id) DO NOTHING"""

    cursor.executemany(sql, movie_genres)
    conn.commit()


def insert_production_company(companies: List[Company]):
    sql = """INSERT INTO productioncompanies 
            (id, name, logo_path, origin_country) 
            VALUES 
            (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"""

    production_company_data = [(company.id, company.name, company.logo_path, company.origin_country) for company in
                               companies]

    cursor.executemany(sql, production_company_data)
    conn.commit()


def insert_movie_production_companies(companies: List[MovieProductionCompany]):
    sql = """INSERT INTO movieproductioncompanies 
            (movie_id, production_company_id) 
            VALUES 
            (%s, %s) ON CONFLICT (movie_id, production_company_id) DO NOTHING"""

    cursor.executemany(sql, companies)
    conn.commit()


def insert_country(region: List[Country]):
    sql = """INSERT INTO productioncountries 
            (iso_3166_1, name) 
            VALUES 
            (%s, %s) ON CONFLICT (iso_3166_1) DO NOTHING"""

    region_data = [(region.iso_3166_1, region.name) for region in region]

    cursor.executemany(sql, region_data)
    conn.commit()


def insert_movie_production_countries(countries: List[MovieProductionCountry]):
    # country code follows ISO 3166-1
    sql = """INSERT INTO movieproductioncountries 
            (movie_id, iso_3166_1) 
            VALUES 
            (%s, %s) ON CONFLICT (movie_id, iso_3166_1) DO NOTHING"""

    cursor.executemany(sql, countries)
    conn.commit()


def insert_spoken_language(languages: List[Language]):
    sql = """INSERT INTO spokenlanguages 
            (iso_639_1, name, english_name) 
            VALUES 
            (%s, %s, %s) ON CONFLICT (iso_639_1) DO NOTHING"""

    language_data = [(language.iso_639_1, language.name, language.english_name) for language in languages]

    cursor.executemany(sql, language_data)
    conn.commit()


def insert_movie_spoken_languages(languages: List[MovieSpokenLanguage]):
    # language code follows ISO 639-1
    sql = """INSERT INTO moviespokenlanguages 
            (movie_id, iso_639_1) 
            VALUES 
            (%s, %s) ON CONFLICT (movie_id, iso_639_1) DO NOTHING"""

    movie_spoken_language_data = [(language.movie_id, language.iso_639_1) for language in languages]

    cursor.executemany(sql, movie_spoken_language_data)
    conn.commit()


def insert_person(persons: List[Person]):
    sql = """INSERT INTO people 
            (id, name, gender, known_for_department, profile_path, adult)
            VALUES 
            (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"""

    person_data = [(
        person.id, person.name, person.gender, person.known_for_department, person.profile_path, person.adult) for
        person in persons]

    cursor.execute(sql, person_data)
    conn.commit()


def insert_person_popularity(popularity: List[PersonPopularity]):
    sql = """INSERT INTO people_popularity 
            (person_id, popularity, date) 
            VALUES 
            (%s, %s, %s) ON CONFLICT (person_id, date) DO NOTHING"""

    popularity_data = [(person.person_id, person.popularity, datetime.date.today()) for person in popularity]

    cursor.execute(sql, popularity_data)
    conn.commit()


def insert_known_works():
    ...
