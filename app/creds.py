# Secret Stuff - Wont be included in the GIT Repo!
from dotenv import load_dotenv
import os 
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
API_KEY = os.getenv('API_KEY')

BASE_URL = "https://api.themoviedb.org/3/movie/popular?api_key=" 
TV_URL =" https://api.themoviedb.org/3/tv/top_rated?api_key=" 


