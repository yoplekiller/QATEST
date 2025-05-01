import allure
from utils.config_utils import get_current_env
from utils.api_utils import send_get_request, attach_response
import json

@allure.feature("영화 목록")
@allure.story("인기 영화 조회")
@allure.title("인기 영화 목록 조회 - 200 응답 확인")
def test_get_popular_movies():

    env = get_current_env()
    BASE_URL = env["base_url"]
    API_KEY = env["api_key"]


    endpoint = "/movie/popular"
    params = {
        "api_key": API_KEY
    }
    response = send_get_request(endpoint, params)
    data = response.json()
    attach_response(response)



    # Allure에 응답 JSON 전체 첨부
    allure.attach(
        body=json.dumps(data, indent=2, ensure_ascii=False),
        name="API 응답 json",
        attachment_type=allure.attachment_type.JSON

    )
    assert response.status_code == 200
    assert "results" in data
    assert isinstance(data["results"], list) # 테스트 결과 없을 경우를 위한 디버깅
    assert len(data["results"]) > 0
