import allure
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

@allure.feature("예외 케이스")
@allure.story("잘못된 API 키")
@allure.title("API 키가 잘못되었을 때 401 Unauthorized 확인")
def test_movie_invalid_api_key():
    params = {
        "api_key": "invalid_key",
        "query": "Inception"
    }
    response = requests.get(f"{BASE_URL}/search/movie", params=params)

    assert  response.status_code == 401