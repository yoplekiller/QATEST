import allure
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

@allure.feature("API 테스트")
@allure.story("영화 검색 및 특정 영화 상세 정보 API 테스트")
def test_search_movie():
    """영화 검색 테스트"""
    params = {
        "api_key": API_KEY,
        "query": "Inception"
    }
    response = requests.get(f"{BASE_URL}/search/movie", params=params)

    assert response.status_code == 200
    data = response.json()

    assert "results" in data # 검색 결과 존재 여부 확인
    assert len(data["results"]) > 0 # 최소 1개 이상의 결과가 있어야 함
    assert data["results"][0]["title"] == "Inception" # 첫번째 결과 인셉션 인지 확인

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