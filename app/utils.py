# Importing the models and flask_login to pull the current User 
# from app.models import User, WatchList
# from flask_login import current_user
# # Defining the Wath list and appending the user selections to it 
# def watch_list(user_id):
#     shows = WatchList.query.filter_by(user_id=user_id).all()
#     show_list, movie_list = [], []
#     for item in shows:
#         if item.show:
#             show_list.append(item.show)
#         else:
#             movie_list.append(item.movie)
#     return [movie_list, show_list]