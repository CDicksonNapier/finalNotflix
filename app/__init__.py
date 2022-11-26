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
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://lkzxohmqyzjotd:134acc9a646f5197e27f9f04b3e634b2ee69e2c8267aa45e2452f00a9bfd9ae0@ec2-52-212-228-71.eu-west-1.compute.amazonaws.com:5432/d751j22cahsoj5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

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