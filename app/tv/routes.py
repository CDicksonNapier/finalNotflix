# Imports 
import requests 
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from app import creds
# Setting up the Blueprint
tv = Blueprint("tv", __name__)

# Creating the tv routes- calls on the creds file for the tv show links !
@tv.route('/tv')
def shows():
    latest = requests.get(f"{creds.TV_URL}&language=en-GB").json()
    comedy = requests.get(
        f"{creds.TV_URL}&with_genres=35&language=en-GB").json()
    adventure = requests.get(
        f"{creds.TV_URL}&with_genres=10759&language=en-GB").json()
    drama = requests.get(f"{creds.TV_URL}&with_genres=18&language=en-G").json()
    scifi = requests.get(
        f"{creds.TV_URL}&with_genres=10765&language=en-GB").json()

    return render_template('public/tvShows.html',title='Tv Shows', latest=latest, comedy=comedy, adventure=adventure, drama=drama, scifi=scifi)

# If the user wants to view an item this will open it 
@tv.route("/tv/<int:tv_id>")
def current_show(tv_id):
    # if the user isnt logged in will redirect to the login - havent worked out how to redirect them to the item that they wanted to view originally
    if current_user.is_authenticated ==False:
      flash(f"You have to log in to view the content!", category='danger')
      return redirect(url_for('user.signin'))
    else:
        # if they are logged in will show the Item in detail on a seperate page
        show_url = requests.get(
        f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={creds.API_KEY}&language=en-US").json()
    return render_template("public/currentShow.html", title=show_url['name'], show=show_url)
