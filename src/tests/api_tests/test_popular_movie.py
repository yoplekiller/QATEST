import requests
import allure
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

@allure.feature("영화 목록")
@allure.story("인기 영화 조회")
@allure.title("인기 영화 목록 조회 - 200 응답 확인")
def test_get_popular_movies():
    params = {
        "api_key": API_KEY
    }
    response = requests.get(f"{BASE_URL}/movie/popular", params=params)

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert  len(data["results"]) > 0
