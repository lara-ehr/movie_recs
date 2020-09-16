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

import sqlalchemy
from sqlalchemy import create_engine
import psycopg2




def get_postgres_data():
    """
    reads in movie ratings data for all users using the postgres database

    Parameters: -
    Returns: dataframe with movie IDs, ratings, user IDs
    """
    df_ratings = pd.read_csv('placeholder/ratings.csv')
    return df_ratings


def create_matrix(df_ratings):
    """
    takes in dataframe and creates a matrix of user ID X movie ID = ratings

    Parameters: dataframe of ratings, user ID, movie ID
    Returns: matrix dataframe
    """
    matrix = df_ratings.set_index(['userId', 'movieId'])['rating'].unstack(0).T
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
    user_genre_matrix = model.transform(matrix)
    print(f'The reconstruction error is: {model.reconstruction_err_}')
    reconstructed_matrix = np.dot(user_genre_matrix, movie_genre_matrix)
    return model


def create_model():
    """
    runs all functions needed to create the NMF model on movie data

    Parameters: -
    Returns: NMF model
    """
    components = 2
    max_iterations = 900
    nan_filling = 3
    df_ratings = get_postgres_data()
    matrix = create_matrix(df_ratings)
    matrix_imputed = imputation(matrix, nan_filling)
    model = create_nmf_model(matrix_imputed, components, max_iterations)
    return model


def create_prediction(model, user_query):
    """
    takes in user query and uses model to create prediction

    Parameters: earlier created NMF model
    user query as dictionary with five movie IDs and user's rating
    """
    prediction = model.transform(user_query)
    return prediction


def deep_recommend():
    ...
