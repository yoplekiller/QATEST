import allure
from config.api_env_config import API_KEY
from utils.api_utils import send_get_request


@allure.feature("영화 목록")
@allure.story("영화 상세 정보 API 테스트")
@allure.title("영화 상세 정보 노출 되는지 확인")
def test_get_movie_details():
    """특정 영화 상세 정보 API 테스트"""

    movie_id = 27205
    endpoint = f"/movie/{movie_id}"
    params = {
        "api_key": API_KEY
    }
    response = send_get_request(endpoint, params)
    data= response.json()

    assert response.status_code == 200
    assert data["id"] == movie_id
    assert data["title"] == "Inception"