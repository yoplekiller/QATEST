import allure
import pytest


@pytest.mark.api
@allure.feature("영화 상세 정보 API 테스트")
@allure.story("영화 비디오 정보 테스트")
@allure.title("영화 ID {movie_id}의 비디오 정보 테스트")
def test_movie_videos(api_env, send_get_request, attach_response):

    API_KEY = api_env.api_key
    
    with allure.step("영화 비디오 정보 조회"):
      movie_id = 550  # 예시로 Fight Club의 ID 사용
      endpoint = f"/movie/{movie_id}/videos"
      params = {"api_key": API_KEY}

    
    with allure.step(f"영화 ID {movie_id}에 대한 비디오 정보 조회"):
      response = send_get_request(endpoint, params)
      attach_response(response)
      data = response.json()

    
    with allure.step("응답 데이터의 비디오 정보 검증"):
      assert "results" in data, "검색 실패"
      assert len(data["results"]) > 0, "비디오 결과가 없습니다"

    with allure.step("비디오 정보 출력"):
      print("\n🎬 비디오 정보")
      for video in data["results"]:
          print(f"📹 제목: {video['name']}, 유형: {video['type']}, 키: {video['key']}")