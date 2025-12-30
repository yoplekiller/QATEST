import allure
import pytest
from utils.csv_utils import get_timestamped_filename, save_movies_to_csv
from utils.data_loader import load_movie_test_data


@pytest.mark.api
@allure.feature("영화 상세 정보 API 테스트")
@allure.story("영화 개봉일 일관성 테스트")
@allure.title("영화 ID {movie_id}의 개봉일 일관성 테스트")
@pytest.mark.parametrize(["movie_id", "expected_title"], load_movie_test_data())
def test_movie_release_date_consistency(movie_id, expected_title, api_env, send_get_request, attach_response):
    API_KEY =  api_env.api_key

    with allure.step(f"영화 ID {movie_id}에 대한 상세 정보 조회"):
      endpoint = f"/movie/{movie_id}"
      params = {"api_key": API_KEY}
      response = send_get_request(endpoint, params)
      attach_response(response)
      data = response.json()


    with allure.step("응답 데이터의 개봉일 및 제목 검증"):
      assert "release_date" in data, "검색 실패"
      assert len(data["release_date"]) == 10,  "검색 실패"
      assert data["title"] == expected_title

    print("\n🎬 테스트 결과")
    print(f"📌 기대 제목: {expected_title}")
    print(f"📥 API 응답 제목: {data['title']}")
    print("개봉일:", data["release_date"])
    print("\n")


    with allure.step("개봉일 정보 CSV로 저장"):
    # ✅ CSV 저장용 딕셔너리 리스트 구성
      movie_info = [{
          "movie_id": movie_id,
          "title": expected_title,
          "release_date": data["release_date"]
      }]

      
    with allure.step("개봉일 정보 CSV로 저장"):
      filename = get_timestamped_filename("movie_release_date_consistency", "csv")
      save_movies_to_csv(movie_info, filename, folder="release_date")