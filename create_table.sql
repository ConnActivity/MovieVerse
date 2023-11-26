CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    original_language VARCHAR(10),
    original_title VARCHAR(100),
    overview TEXT,
    popularity NUMERIC(10,3),
    poster_path VARCHAR(255),
    release_date DATE,
    title VARCHAR(100),
    video BOOLEAN,
    vote_average NUMERIC(3,1),
    vote_count INTEGER
);
CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    gender INTEGER,
    known_for_department VARCHAR(50),
    popularity NUMERIC(10,3),
    profile_path VARCHAR(255),
    adult BOOLEAN
);

CREATE TABLE known_works (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people(id),
    adult BOOLEAN,
    backdrop_path VARCHAR(255),
    title VARCHAR(100),
    original_language VARCHAR(10),
    original_title VARCHAR(100),
    overview TEXT,
    poster_path VARCHAR(255),
    media_type VARCHAR(50),
    popularity NUMERIC(10,3),
    release_date DATE,
    video BOOLEAN,
    vote_average NUMERIC(3,1),
    vote_count INTEGER,
    genre_ids INTEGER[]
);

CREATE TABLE movies_popularity (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id),
    popularity NUMERIC(10,3),
    vote_average NUMERIC(3,1),
    date DATE,
    region VARCHAR(10)
);

CREATE TABLE people_popularity (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people(id),
    popularity NUMERIC(10,3),
    vote_average NUMERIC(3,1),
    date DATE
);