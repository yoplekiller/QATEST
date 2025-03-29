import allure
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

@allure.feature("영화 목록")
@allure.story("영화 상세 정보 API 테스트")
@allure.title("영화 상세 정보 노출 되는지 확인")
def test_get_movie_details():
    """특정 영화 상세 정보 API 테스트"""
    movie_id = 27205
    params = {
        "api_key": API_KEY
    }
    response = requests.get(f"{BASE_URL}/movie/{movie_id}", params=params)

    assert  response.status_code == 200
    data = response.json()

    assert data["id"] == movie_id
    assert data["title"] == "Inception"