# Calling all the imports - The creds file holds my API and Secret Keys which will be hidden from the GIT Repo
import requests
from flask import Flask, render_template, flash, redirect, request, session, url_for, current_app
from app import app, db
from app import creds
from flask_login import current_user
from app.models import WatchList
from app.utils import watch_list
import json

# Main index page - Ive kept the full links for the TMDB api here but is diferent on other pages. 
@app.route('/', methods=['GET', 'POST'])
def homepage():
    popular = requests.get(f"{creds.BASE_URL}4b96cadadd63dfa1342c3b257a7f46d0&language=en-US&page=1").json()
    top_rated_movies = requests.get(f"https://api.themoviedb.org/3/movie/top_rated?api_key={creds.API_KEY}&language=en-US&page=1").json()
    latest = requests.get(f"https://api.themoviedb.org/3/tv/top_rated?api_key={creds.API_KEY}&language=en-US").json()
    return render_template('public/index.html',title='Homepage',  data=popular, latest=latest, tr_movies=top_rated_movies)
# Becuase of the way the json reads the movies/tv shows i couldnt work out to rendomly show a tv or movie on one page as movies use keyword 'title' and shows 'name'
@app.route('/surprise', methods=['GET', 'POST'])
def surprise():
   randomMovie = requests.get(f"{creds.BASE_URL}&language=en-US&page=1").json()   
   return render_template("public/surprise.html", title="Surprise", data=randomMovie)
# random Tv show
@app.route('/surprisetv', methods=['GET', 'POST'])
def surpriseShows():
   randomTv = requests.get(f"{creds.TV_URL}&language=en-US&page=1").json()   
   return render_template("public/surpriseTv.html", title="SurpriseTv", data=randomTv)

