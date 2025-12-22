import allure
import requests
import json
import pytest
from utils.api_utils import attach_response
from utils.config_utils import get_current_env


@pytest.mark.api
@allure.feature("영화 목록 API 테스트")
@allure.story("영화 검색 API 테스트")
@allure.title("영화 검색 기능이 잘 동작 하는지 확인")
def test_search_movie():
    env = get_current_env()
    BASE_URL = env["base_url"]
    API_KEY = env["api_key"]
    params = {
        "api_key": API_KEY,
        "query": "Inception"
    }
    response = requests.get(f"{BASE_URL}/search/movie", params=params)

    assert response.status_code == 200
    data = response.json()
    attach_response(response)

    assert "results" in data # 검색 결과 존재 여부 확인
    assert len(data["results"]) > 0 # 최소 1개 이상의 결과가 있어야 함
    assert data["results"][0]["title"] == "Inception" # 첫번째 결과가 인셉션 인지 확인

    print("📦 응답 JSON :")
    print(json.dumps(data, indent=4, ensure_ascii=False))
