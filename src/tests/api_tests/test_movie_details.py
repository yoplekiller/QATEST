import allure
import pytest
import json
from utils.config_utils import get_current_env
from utils.api_utils import send_get_request, attach_response
from utils.data_loader import load_movie_test_data


@allure.feature("영화 목록 API 테스트")
@allure.story("영화 상세 정보 API 테스트")
@allure.title("유효한 movie_id에 대한 상세 정보 조회 테스트")
@pytest.mark.parametrize(["movie_id","expected_title"], load_movie_test_data())
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

    assert response.status_code == 200, 'FAILED'
    assert data["id"] == movie_id, 'FAILED'
    assert data["title"] == expected_title, 'FAILED'

    # print("\n🎬 테스트 결과")
    # print(f"📌 기대 제목: {expected_title}")
    # print(f"📥 API 응답 제목: {data['title']}")
    # print("개봉일:", data["release_date"])
    # print("\n")

    print("📦 응답 JSON :")
    print(json.dumps(data, indent=4, ensure_ascii=False))

