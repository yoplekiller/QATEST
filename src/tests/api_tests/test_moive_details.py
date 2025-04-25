import allure
import pytest
from config.api_env_config import API_KEY
from utils.api_utils import send_get_request, attach_response


@allure.feature("영화 목록")
@allure.story("영화 상세 정보 API 테스트")
@allure.title("유효한 movie_id에 대한 상세 정보 조회 테스트")
@pytest.mark.parametrize("movie_id", [27025, 550, 603, 157336])
def test_get_movie_details():
    """특정 영화 상세 정보 API 테스트"""

    movie_id = 27205
    endpoint = f"/movie/{movie_id}"
    params = {
        "api_key": API_KEY
    }
    response = send_get_request(endpoint, params)
    data= response.json()
    attach_response(response)

    assert response.status_code == 200
    assert data["id"] == movie_id
    assert data["title"] == "Inception"

