import allure
import pytest


@pytest.mark.api
@allure.feature("영화 목록 API 테스트")
@allure.story("영화 검색 기능 테스트")
@allure.title("영화 검색 기능이 잘 동작 하는지 확인")
def test_search_movie(api_env, send_get_request, attach_response):

    API_KEY = api_env.api_key

    with allure.step("영화 검색 API 호출 - Inception"):
        endpoint = "/search/movie"
        params = {
            "api_key": API_KEY,
            "query": "Inception"
        }

    with allure.step("GET 요청 전송: /search/movie?query=Inception"):
      response = send_get_request(endpoint, params=params)
      assert response.status_code == 200
      data = response.json()
      attach_response(response)
    
    with allure.step("응답 데이터 검증"):
      assert "results" in data # 검색 결과 존재 여부 확인
      assert len(data["results"]) > 0 # 최소 1개 이상의 결과가 있어야 함
      assert data["results"][0]["title"] == "Inception" # 첫번째 결과가 인셉션 인지 확인

