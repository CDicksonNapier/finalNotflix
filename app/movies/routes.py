# Imports 
import requests 
from flask import Blueprint, render_template, flash, redirect, url_for
from app import creds
from flask_login import current_user

# Creating the Blueprint 
movies = Blueprint('movies', __name__)
# Movies route - pulling the Json data from the API 
@movies.route('/movies')
def movie():
    popular = requests.get(f"{creds.BASE_URL}&language=en-US&page=1").json()
    comedy = requests.get(f"{creds.BASE_URL}&with_genres=35&language=en-GB").json()
    horror = requests.get(f"{creds.BASE_URL}&with_genres=27,53&language=en-G").json()
    ada = requests.get(f"{creds.BASE_URL}&with_genres=28,12&language=en-G").json()
    scifi = requests.get(f"{creds.BASE_URL}&with_genres=878,10752&language=en-G").json()
    return render_template('public/movies.html', popular =popular, comedy=comedy, horror=horror, ada=ada, scifi=scifi )
# pulling a movie by ID from the API if the user is not signed in then will be redirected to the login page
@movies.route("/movie/<int:movie_id>")
def current_movie(movie_id):   
    if current_user.is_authenticated ==False:
        flash(f"You have to log in to view the content!", category='danger')
        return redirect(url_for('user.signin'))
    else:
        movies_Url = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={creds.API_KEY}&language=en-US&append-to-response=videos").json() 
    return render_template("public/currentMovie.html", movie=movies_Url)