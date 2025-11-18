from utils.api_utils import send_get_request, attach_response
from utils.config_utils import get_current_env
from utils.csv_utils import get_timestamped_filename, save_movies_to_csv


def test_rated_movie_consistency():
    env = get_current_env()
    API_KEY = env["api_key"]

    endpoint = "/movie/top_rated"
    params = {"api_key": API_KEY, "page": 3}


    response = send_get_request(endpoint, params)
    attach_response(response)
    data = response.json()

    assert "results" in data, "검색 실패"
    assert len(data["results"]) > 0, "최고 평점 영화가 없습니다"

    for movie in data["results"]:
        assert "id" in movie, f"영화 ID가 없습니다: {movie}"
        assert "title" in movie, f"영화 제목이 없습니다: {movie}"

    print("\n🎬 최고 평점 영화 목록")
    for movie in data["results"]:
        print(f"📌 ID: {movie['id']}, 제목: {movie['title']}")


    filename = get_timestamped_filename("top_rated_movies", "csv")
    save_movies_to_csv(data["results"], filename, folder="results")
