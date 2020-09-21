"""
Machine-Learning Code that returns movies

INPUT:
- table "ratings"
- user input from web application: dictionary of the IDs of the movies the user
  had to rate and their respective ratings by the user which is an integer
  between 0 and 5

OUTPUT:
- sorted list of five most fitting movies for recommendations
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import NMF
# import os
# import sqlalchemy
from sqlalchemy import create_engine
# import psycopg2
from credentials import *

CONN = f'postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

ratings_query = '''
                SELECT * FROM ratings
                INNER JOIN movies
                USING (movieid);
                '''
movie_number_query = 'SELECT COUNT(DISTINCT movieid) FROM ratings;'


def get_postgres_data():
    """
    reads in movie and ratings data for all users using the postgres database

    Parameters: -
    Returns: dataframe with movie IDs, ratings, user IDs;
    number of unique movies in database
    """
    engine = create_engine(CONN, encoding='latin1', echo=False)
    df_ratings_proxy = engine.execute(ratings_query)
    df_ratings = pd.DataFrame(df_ratings_proxy.fetchall())
    df_ratings.head(50)
    df_ratings.columns = ['movieid',
                          'index',
                          'userid',
                          'rating',
                          'demeaned',
                          'title',
                          'genre']
    df_ratings = df_ratings.drop('index', axis=1)
    # number_of_movies = df_ratings['movieid'].unique().shape[0]
    number_of_movies = engine.execute(movie_number_query).fetchall()[0][0]
    number_of_movies
    return df_ratings, number_of_movies


def create_matrix(df_ratings):
    """
    takes in dataframe and creates a matrix of user ID X movie ID = ratings

    Parameters: dataframe of ratings, user ID, movie ID
    Returns: matrix dataframe
    """
    matrix = df_ratings.set_index(['userid', 'movieid'])['rating'].unstack(0).T
    return matrix


def imputation(matrix, nan_filling):
    """
    takes in matrix dataframe and value for filling in NaNs for imputation

    Parameters: matrix dataframe, NaN filling value
    Returns: imputed matrix dataframe
    """
    matrix.fillna(nan_filling, inplace=True)
    return matrix


def create_nmf_model(matrix, components, max_iterations):
    """
    generates NMF model to recreate matrix with new features
    and predict movies for query

    Parameters: matrix dataframe, model hyperparameters
    Returns: dictionary of five recommended movies
    """
    model = NMF(
                n_components=components,
                init='random',
                max_iter=max_iterations,
                random_state=10)
    model.fit(matrix)
    movie_genre_matrix = model.components_
    # user_genre_matrix = model.transform(matrix)
    print(f'The reconstruction error is: {model.reconstruction_err_}')
    # reconstructed_matrix = np.dot(user_genre_matrix, movie_genre_matrix)
    return model, movie_genre_matrix


def create_prediction(
                    df_ratings,
                    user_query,
                    model,
                    movie_genre_matrix,
                    number_of_movies):
    """
    takes in user query and uses model to create prediction

    Parameters:
    - earlier created NMF model
    - user query as dictionary with five movie IDs and user's rating
    """
    query_ratings = list(user_query.values())
    query_movies = list(user_query.keys())
    indices_movies = [df_ratings[df_ratings['title'] == movie].index[0]
                      for movie in query_movies]
    user = np.zeros(number_of_movies)
    for index, idx_value in enumerate(indices_movies):
        user[idx_value] = query_ratings[index]
    user = [user]
    user_profile = model.transform(user)
    prediction = np.dot(user_profile, movie_genre_matrix)
    return prediction, query_movies


def get_prediction_names(df_ratings, prediction, movies_to_drop):
    '''
    Takes array of predicted ratings for new user
    Returns top n number of films with highest ratings
    Provides list with names of those movies as strings
    '''
    prediction_series = pd.Series(prediction, index=df_ratings['title'].values)
    prediction_series = prediction_series.drop(movies_to_drop)
    list_of_top_recs = prediction_series.sort_values(ascending=False).head(10)
    return list_of_top_recs


COMPONENTS = 2
MAX_ITERATIONS = 900
NAN_FILLING = 0
USER_QUERY_PLACEHOLDER = {
            'Toy Story (1995)': '4',
            'Jumanji (1995)': '3',
            'Casino (1995)': '2',
            'Three Billboards Outside Ebbing, Missouri (2017)': '5',
            'From Dusk Till Dawn (1996)': '0',
            }
DF_RATINGS, NUMBER_OF_MOVIES = get_postgres_data()
NUMBER_OF_MOVIES
MATRIX = create_matrix(DF_RATINGS)
MATRIX_IMPUTED = imputation(MATRIX, NAN_FILLING)
MODEL, MOVIE_GENRE_MATRIX = create_nmf_model(
                                            MATRIX_IMPUTED,
                                            COMPONENTS,
                                            MAX_ITERATIONS)
PREDICTION, MOVIES_TO_DROP = create_prediction(
                                        DF_RATINGS,
                                        USER_QUERY_PLACEHOLDER,
                                        MODEL,
                                        MOVIE_GENRE_MATRIX,
                                        NUMBER_OF_MOVIES)
RECOMMENDATIONS = get_prediction_names(DF_RATINGS, PREDICTION[0], MOVIES_TO_DROP)
