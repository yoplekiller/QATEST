import requests
import allure
from config.api_env_config import API_KEY, BASE_URL



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
