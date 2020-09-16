# Movie Recommender System
Provides personalised movie recommendations.

## USER STORY

We want to have a web application running on a remote server, that presents five (x) randomly selected movies for the user to rate.
Based on that a machine learning algorithm (NMF) recommends five other movies for the user.

potential future work:
- take user feedback into account in some way
- number of movies to be considered may be defined by the user
- user may also choose which movies are to be considered as input for the recommendation


## TO DO

- development environment: 100K dataset
- deployment environment: 10M dataset

#### 1. Database Creation (Postgres)

INPUT:
- movies.csv - MovieID, Title, Genre
- ratings.csv - UserID, MovieID, Rating, (Timestamp)
- tags.csv - UserID, MovieID, Tag, (Timestamp)
- (links.csv)- MovieID, IMDBID, tmbdID

OUTPUT:
- database "movieratings"
- three tables (movies, ratings, links)

To Do:
- EDA
- Basic Data Wrangling
. Normalization of each user's ratings
- Script for getting data into database (already done by Lara)
- adjusting paths as needed

#### 2. Machine Learning (NMF model/collaborative filtering)

INPUT:
- table "ratings"
- user input from web application: dictionary of the IDs of the movies the user had to rate and their respective ratings by the user which is an integer between 0 and 5

OUTPUT:
- sorted list of five most fitting movies for recommendations

To Do:
- create a crossover matrix of movie_IDs, user_IDs and ratings
- Imputation of NaNs with some sort of average/median value of the dataset
- fit model (Q, P, dotproduct)
- adjust hyperparameters based on model reconstruction error
- take user query and transform it with model to create a sorted list with x most recommended movie IDs
- transform list of movie IDs to list with movie name strings

#### 3. Web Application (Flask)

INPUT:
- sorted list of five most fitting movies for recommendations

To Do:
- TBD - refine as needed with CSS/JS/HTML

#### 4. Project Structure

(MODEL-VIEW-CONTROLLER structure)

- DIR flask-app
    - DIR templates
      - index.html (landing page for the user where they can enter their ratings for five movies, create ouput: dictionary of movieIDs and respective ratings)
      - recommendations.html (- the view code for recommended movies)
    - application.py (- main program that describes how all the other scripts interact with each other)
    - psql.py (- creation of tables, get csv files for input, insertion of data, normalization of users, create deliverable database)
    - recommender.py (- get input data, imputation, ML model, create output)

## Equally important: TO NOT DO!

- anything that's no fun!
