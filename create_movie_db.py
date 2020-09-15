import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2


# import data

HOST = ''# ENTER CONNECTION LINK HERE
PORT = '5432'
USER = 'postgres'
PASSWORD = 'YOURPASSWORD' # ENTER PASSWORD
DATABASE = 'movieratings'

PATH_MOVIES = 'YOURPATH_movies'
PATH_RATINGS = 'YOURPATH_ratings'
PATH_LINKS = 'YOURPATH_links'

conn = f'postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

drop_tables_query = '''
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS links;
'''

create_tables_query = '''
CREATE TABLE movies (
movieid SERIAL PRIMARY KEY,
title VARCHAR(250),
genres VARCHAR(150)
);

CREATE TABLE links (
movieid SERIAL PRIMARY KEY,
imdbid VARCHAR(10),
tmdbid BIGINT
);

'''

def scale(df, by):
    '''
    Normalise on min-max scale; then bin result to return new rating in range 1-5
    '''
    groups = df.groupby(by)
    min = groups.transform(np.min)
    max = groups.transform(np.max)
    norm = (df[min.columns] - min) / (max - min)
    return norm['ratings']


ratings = pd.read_csv(PATH_RATINGS)

ratings = ratings.drop('timestamp', axis = 1)

ratings.columns = ['userid', 'movieid', 'ratings']

ratings['norm'] = scale(ratings, 'userid')

def copy_table(path):
    query = '''COPY movies FROM ''' + '\'' + path + '\'' + ''' DELIMITER ',' CSV HEADER;'''
    return query


if __name__ == '__main__':

    engine = create_engine(conn, encoding = 'latin1', echo= False)
    print('created engine')

    # drop tables if needed
    # engine.execute(drop_tables_query)
    # print('dropped pre-existing tables')

    # creating tables
    engine.execute(create_tables_query)
    print('created tables')

    # input movie data
    engine.execute(copy_table(PATH_MOVIES))
    print('created movies table')

    # input ratings data from pandas
    ratings.to_sql('ratings', engine, if_exists='append')

    # input links data
    engine.execute(copy_table(PATH_LINKS))
    print('created links table')
















#
