import allure
import pytest
from utils.data_loader import load_movie_test_data


@pytest.mark.api
@allure.feature("영화 목록 API 테스트")
@allure.story("영화 상세 정보 API 테스트")
@allure.title("유효한 movie_id에 대한 상세 정보 조회 테스트")
@pytest.mark.parametrize(["movie_id","expected_title"], load_movie_test_data())
def test_get_movie_details(movie_id, expected_title, api_env, send_get_request, attach_response):
    """특정 영화 상세 정보 API 테스트"""
    
    API_KEY = api_env.api_key
    
    with allure.step(f"영화 ID {movie_id}에 대한 상세 정보 조회"):
        endpoint = f"/movie/{movie_id}"
        params = {
            "api_key": API_KEY
        }

    with allure.step("GET 요청 전송 및 응답 수신"):
      response = send_get_request(endpoint, params)
      data= response.json()
      attach_response(response)
 
    with allure.step("응답 상태 코드 및 데이터 검증"):
        assert response.status_code == 200, 'FAILED'
        assert data["id"] == movie_id, 'FAILED'     
        assert data["title"] == expected_title, 'FAILED'



