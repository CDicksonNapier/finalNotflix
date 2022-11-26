# DB models - kept the watch list basic. 
# Calling the imports 
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# User Information - with watchlists as its relationship each user will have diferent tastes etc 
# Ive added an image to this but havent incorperated it into the user accounts it is something id like to add in the future have the user be able to add a profile pic
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(80), nullable=False )
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    watchlists = db.relationship("WatchList",backref="user", cascade="all, delete, delete-orphan", lazy=True)
    def __repr__(self):
     return f'{self.username} : {self.email} : {self.date_created.strftime("%d/%m/%Y, %H:%M:%S")}'

# #  Watch list model for the DB 
# #  Kept minimal 
class WatchList(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  movie = db.Column(db.Integer)
  show = db.Column(db.Integer)
  User= db.relationship('User', backref="watchlist")
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)