# IMPORTS AND FROMS
from flask import Blueprint, Flask, render_template, flash, redirect, request, session, url_for
from app.forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from app import creds, db, bcrypt
from app.models import User, WatchList
from flask_login import login_user, logout_user, current_user
from app.utils import watch_list
import requests

# Initiating the Blueprint
user = Blueprint('user', __name__)

# User Register  route


@user.route('/user', methods=['GET', 'POST'])
def register():
    #    if the user is logged in then page will redirect to the users account
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))
# However if the User is not registered then the user will be directed to the register page
    form = RegistrationForm()
    if form.validate_on_submit():
        # Using Bcrypt to encrypt the password -
        encrypted_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=encrypted_password)
        user_object = User.query.filter_by(username=form.username.data).first()
        # If the username matches one from the DB then itll flash the message and return the user back to the registration page
        if user_object:
            flash("Someone has this username please try again", category='danger')
            return redirect(url_for('user.register'))
        else:
            # Other wise the User details will be saved to the DB and then redirect to the login form
            db.session.add(user)
            db.session.commit()
            flash(
                f'Account Created for {form.username.data}', category='success')
            return redirect(url_for('user.signin'))
    return render_template('public/register.html', title='Register', form=form)

# User Login form


@user.route('/login', methods=['GET', 'POST'])
def signin():
    #    If the user is already signed in then it will redirect to the User Account page!
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))
    # If the user isnt signed in then redirect to the login form !
    form = LoginForm()
    if form.validate_on_submit():
        # Checking against the  DB for the username
        user = User.query.filter_by(username=form.username.data).first()
        # and checking against the Bcrypt Pass word stored in the DB if all goes well signs the user in and redirects to the homepage.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome Back {form.username.data}", category='success')
            return redirect('/')
        else:
            # other wise will redirect to the Login page and flashes the message
            flash(f"Couldn't log you in ", category='danger')
    return render_template('public/login.html', form=form)

# Logout Function - Logs the user out and redirects to the login form


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.signin'))

# Accounts will dispaly lists from the Watchlist models this is filtered per user


@user.route('/account', methods=['GET', 'POST'])
def account():
    list = WatchList.query.filter_by(user_id=current_user.id).all()
    shows = []
    movies = []
    for item in list:
        if (item.show):
            show_url = f"https://api.themoviedb.org/3/tv/{item.show}?api_key={creds.API_KEY}&language=en-GB"
            show = requests.get(show_url).json()
            shows.append(show)
        elif (item.movie):
            movie_url = f"https://api.themoviedb.org/3/movie/{item.movie}?api_key={creds.API_KEY}&language=en-GB"
            movie = requests.get(movie_url).json()
            movies.append(movie)

    return render_template('public/account.html', title='Account')

# adding a movie or show to the Watch list!


@user.route('/add/<string:m_type>/<int:m_id>')
def add(m_type, m_id):
  # starting with empty lists
  user_movies, user_shows = [], []
  if current_user.is_authenticated:
      user_movies, user_shows = watch_list(current_user.id)
      user = User.query.filter_by(id=current_user.id).first()
      # if the movie is not in the list this adds it and updates the DB
      if m_type == 'movie':
          if m_id not in user_movies:
              mv = WatchList(movie=m_id, user_id=user.id)
              db.session.add(mv)
              db.session.commit()
      else:
          # does the same as movies but for the Shows
          if m_id not in user_shows:
              mv = WatchList(show=m_id, user_id=user.id)
              db.session.add(mv)
              db.session.commit()
    # Refreshes the page
  return redirect(request.referrer)

# Delete Item from Watch List - Clears all the user movies/shows


@user.route('/del/<int:id>', methods=['GET', 'POST'])
def delItem(id):
    if current_user.is_authenticated:
        user_movies, user_shows = watch_list(current_user.id)
        rmv = WatchList.query.delete(id == watch_list(current_user.id))
        # db.session.delete()
        db.session.commit()
    return redirect(url_for('user.account'))


# Delete User Account - have still to add a "are you sure function"
@user.route('/deleteUser/<int:id>', methods=['GET', 'POST'])
def delUser(id):
    if id == current_user.id:
        user_to_delete = User.query.get_or_404(id)
        db.session.delete(user_to_delete)
        db.session.commit()
    return redirect(url_for('user.register'))
