# Main init file 
# imports 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app import creds
app=Flask(__name__)
# pulling the Secret Key from the creds file 
app.config['SECRET_KEY']= creds.SECRET_KEY
# app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://chrispg:chrispg@localhost:5432/notflixusers'
app.config['SQLALCHEMY_DATABASE_URI']= creds.DATABASE_URL

uri = creds.DATABASE_URL
# or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

# Setting up the DB connection used Postgresql oringally was going to use sqlite 

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)



# Importing the routes and registering the blueprints 
from app import routes

from .user.routes import user
app.register_blueprint(user)

from .movies.routes import movies
app.register_blueprint(movies)

from .tv.routes import tv
app.register_blueprint(tv)

from .errors.handlers import errors
app.register_blueprint(errors)