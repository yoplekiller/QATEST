import allure
import json
import pytest


@pytest.mark.api
@allure.feature("영화 목록 API 테스트")
@allure.story("인기 영화 조회")
@allure.title("인기 영화 목록 조회 - 200 응답 확인")
def test_get_popular_movies(api_env, send_get_request, attach_response):

    API_KEY = api_env.api_key
    
    with allure.step("인기 영화 목록 조회"):
      endpoint = "/movie/popular"
      params = {
          "api_key": API_KEY
      }
      
    with allure.step("GET 요청 전송: /movie/popular"):
      response = send_get_request(endpoint, params)
      data = response.json()
      attach_response(response)

    with allure.step("응답 JSON 전체 첨부"):
      allure.attach(
          body=json.dumps(data, indent=2, ensure_ascii=False),
          name="API 응답 json",
          attachment_type=allure.attachment_type.JSON

    )
    with allure.step("응답 데이터 검증"):
      assert response.status_code == 200
      assert "results" in data
      assert isinstance(data["results"], list) # 테스트 결과 없을 경우를 위한 디버깅
      assert len(data["results"]) > 0

