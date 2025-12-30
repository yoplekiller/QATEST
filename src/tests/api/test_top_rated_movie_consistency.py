import allure
from utils.csv_utils import get_timestamped_filename, save_movies_to_csv
import pytest


@pytest.mark.api
@allure.feature("영화 상세 정보 API 테스트")
@allure.story("특정 페이지의 최고 평점 영화 일관성 테스트")
@allure.title("3페이지 최고 평점 영화 목록 일관성 테스트")
def test_rated_movie_consistency(api_env, send_get_request, attach_response):

    API_KEY = api_env["api_key"]
    
    with allure.step("최고 평점 영화 목록 조회"):
      endpoint = "/movie/top_rated"
      params = {"api_key": API_KEY, "page": 3}

    with allure.step("GET 요청 전송 및 응답 수신"):
      response = send_get_request(endpoint, params)
      attach_response(response)
      data = response.json()

    with allure.step("응답 데이터의 최고 평점 영화 정보 검증"):
      assert "results" in data, "검색 실패"
      assert len(data["results"]) > 0, "최고 평점 영화가 없습니다"


    with allure.step("각 영화 항목에 ID 및 제목 필드 존재 여부 검증"):
      for movie in data["results"]:
          assert "id" in movie, f"영화 ID가 없습니다: {movie}"
          assert "title" in movie, f"영화 제목이 없습니다: {movie}"

    with allure.step("최고 평점 영화 목록 출력"):
      print("\n🎬 최고 평점 영화 목록")
      for movie in data["results"]:
          print(f"📌 ID: {movie['id']}, 제목: {movie['title']}")
 
    with allure.step("최고 평점 영화 목록 CSV로 저장"):
      filename = get_timestamped_filename("top_rated_movies", "csv")
      save_movies_to_csv(data["results"], filename, folder="results")
