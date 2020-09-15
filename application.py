from flask import Flask, render_template, request
import recommender as rec  # import all objects from recommender.py

app = Flask(__name__)  # tell flask to make this script the center of the application


@app.route('/index')  # whenever user visits HOSTNAME:PORT/index, this function is triggered
@app.route('/') # you can add multiple routes
def hello():
    return render_template('index.html')


@app.route('/recommendations')  # python decorator modifies the function that is defined on the next line
def recommender():
    ratings = dict(request.args)
    # THIS WE NEED TO BUILD OURSELVES NOW:
    recommendations = rec.calculate_best_movies(ratings)
    return render_template('recommendations.html', result_html=ratings.values())
    # passing the back-end python variable to the fron-end (HTML), i. e. the RESPONSE


if __name__ == '__main__':
    # whatever occurs after this line is executred when we run "python application.py"
    # however, whatever occurs after this line is NOT executed when we IMPORT application.py
    app.run(debug=True)  # this will start an infinite process, i. e. serving our web page
    # debug mode displays backend errors to the browser
    # (good for development but bad idea for production)
    # also automatically restarts server upon changes to code
