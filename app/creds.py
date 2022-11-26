# Secret Stuff - Wont be included in the GIT Repo!
from dotenv import load_dotenv
import os 
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
API_KEY = '4b96cadadd63dfa1342c3b257a7f46d0'


BASE_URL = "https://api.themoviedb.org/3/movie/popular?api_key=4b96cadadd63dfa1342c3b257a7f46d0"
TV_URL =" https://api.themoviedb.org/3/tv/top_rated?api_key=4b96cadadd63dfa1342c3b257a7f46d0"



