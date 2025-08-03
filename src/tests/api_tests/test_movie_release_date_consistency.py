import allure
import pytest
from utils.api_utils import send_get_request, attach_response
from utils.config_utils import get_current_env
from utils.csv_utils import get_timestamped_filename, save_movies_to_csv
from utils.data_loader import load_movie_test_data

@allure.title("영화 개봉일 확인")
@pytest.mark.parametrize(["movie_id", "expected_title"], load_movie_test_data())
def test_movie_release_date_consistency(movie_id, expected_title):
    env = get_current_env()
    BASE_URL = env["base_url"]
    API_KEY = env["api_key"]

    endpoint = f"/movie/{movie_id}"
    params = {"api_key": API_KEY}

    response = send_get_request(endpoint, params)
    attach_response(response)
    data = response.json()

    assert "release_date" in data, "검색 실패"
    assert len(data["release_date"]) == 10,  "검색 실패"
    assert data["title"] == expected_title

    print("\n🎬 테스트 결과")
    print(f"📌 기대 제목: {expected_title}")
    print(f"📥 API 응답 제목: {data['title']}")
    print("개봉일:", data["release_date"])
    print("\n")

    # ✅ CSV 저장용 딕셔너리 리스트 구성
    movie_info = [{
        "movie_id": movie_id,
        "title": expected_title,
        "release_date": data["release_date"]
    }]

    filename = get_timestamped_filename("movie_release_date_consistency", "csv")
    save_movies_to_csv(movie_info, filename, folder="release_date")
