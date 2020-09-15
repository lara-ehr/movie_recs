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


def get_postgres_data():
    df_ratings = pd.read_csv('placeholder/ratings.csv')
    return df_ratings


def get_user_input():
    query = {
            '99': '2',
            '4599': '4',
            '2982': '4',
            '3134': '5',
            '5456': '0',
            }
    return query


def create_matrix(df_ratings):
    matrix = df_ratings.set_index(['userId', 'movieId'])['rating'].unstack(0).T
    return matrix


def imputation(matrix):
    matrix.fillna(3, inplace=True)
    return matrix


def create_nmf_model(matrix, components, max_iterations):
    model = NMF(
                n_components=components,
                init='random',
                max_iter=max_iterations,
                random_state=10)
    model.fit(matrix)
    movie_genre_matrix = model.components_
    user_genre_matrix = model.transform(matrix)

    print(model.reconstruction_err_)

    reconstructed_matrix = np.dot(user_genre_matrix, movie_genre_matrix)
    print(reconstructed_matrix)
    return reconstructed_matrix


def predict_movies(user_query, reconstructed_matrix):
    # prediction = model.transform(query)
    # return prediction
    ...


def deep_recommend():
    ...


# HYPERPARAMETER OPTIMIZATION
COMPONENTS = 2
MAX_ITERATIONS = 900

DF_RATINGS = get_postgres_data()
USER_QUERY = get_user_input()
MATRIX = create_matrix(DF_RATINGS)
MATRIX_IMPUTED = imputation(MATRIX)
MATRIX_RECONSTRUCTED = create_nmf_model(MATRIX_IMPUTED, COMPONENTS, MAX_ITERATIONS)
MOVIE_PREDICTIONS = predict_movies(USER_QUERY, MATRIX_RECONSTRUCTED)
