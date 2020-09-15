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
    print(f'The reconstruction error is: {model.reconstruction_err_}')
    reconstructed_matrix = np.dot(user_genre_matrix, movie_genre_matrix)
    return reconstructed_matrix


def predict_movies(user_query):
    df_ratings = get_postgres_data()
    matrix = create_matrix(df_ratings)
    matrix_imputed = imputation(matrix)
    components = 2
    max_iterations = 900
    matrix_reconstructed = create_nmf_model(matrix_imputed, components, max_iterations)
    # prediction = model.transform(user_query)
    # return prediction
    ...


def deep_recommend():
    ...