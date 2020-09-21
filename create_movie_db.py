import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text

import psycopg2

from credentials import *

# import data

ratings = pd.read_csv(PATH_RATINGS)
ratings = ratings.drop('timestamp', axis = 1)
ratings.columns = ['userid', 'movieid', 'ratings']

CONN = f'postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

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

ratings['mean'] = ratings.groupby('userid').transform('mean')['ratings']
ratings['demeaned'] = ratings['ratings'] - ratings['mean']
ratings = ratings.drop(['mean'], axis=1)


def copy_table(table_name, path):
    '''
    Input: name of table as string, path as variable (defined in separate credentials.py script)
    Output: query string
    '''
    query = f"COPY {table_name} FROM \'{path}\' DELIMITER ',' CSV HEADER; COMMIT;"
    return query


if __name__ == '__main__':

    engine = create_engine(CONN, encoding = 'latin1', echo= False)
    print('created engine')

    # drop tables if needed
    engine.execute(drop_tables_query)
    print('dropped pre-existing tables')

    # creating tables
    engine.execute(create_tables_query)
    print('created tables')

    # input movie data
    engine.execute(copy_table('movies', PATH_MOVIES))
    print('created movies table')

    # input ratings data from pandas
    ratings.to_sql('ratings', engine, if_exists='append')

    # input links data
    engine.execute(copy_table('links', PATH_LINKS))
    print('created links table')
