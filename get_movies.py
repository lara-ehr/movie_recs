'''
Gets 5 films for the user to rate (their rating will then be the input for the recommendation system.)
'''
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import psycopg2
import random

from credentials import *

CONN = f'postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

ENGINE = create_engine(CONN, encoding='latin1', echo=False)

movies_query = '''SELECT DISTINCT title FROM movies;'''

def get_movies():
    movies_proxy = ENGINE.execute(movies_query)
    movies = pd.DataFrame(movies_proxy.fetchall())
    movies.columns = ['title']
    chosen = random.choices(movies['title'], k=5)
    return chosen
