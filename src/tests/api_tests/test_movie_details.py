import allure
import pytest
from utils.config_utils import get_current_env
from utils.api_utils import send_get_request, attach_response


@allure.feature("영화 목록")
@allure.story("영화 상세 정보 API 테스트")
@allure.title("유효한 movie_id에 대한 상세 정보 조회 테스트")
@pytest.mark.parametrize(["movie_id","expected_title"],[
        (27025, "The Godfather"),
        (550, "Fight Club"),
        (603, "The Matrix"),
        (157336, "Interstellar")
    ])
def test_get_movie_details(movie_id, expected_title):
    """특정 영화 상세 정보 API 테스트"""

    env = get_current_env()
    BASE_URL = env["base_url"]
    API_KEY = env["api_key"]

    endpoint = f"/movie/{movie_id}"
    params = {
        "api_key": API_KEY
    }

    response = send_get_request(endpoint, params)
    data= response.json()
    attach_response(response)

    assert response.status_code == 200
    assert data["id"] == movie_id
    assert data["title"] == expected_title

