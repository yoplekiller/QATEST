from utils.api_utils import send_get_request, attach_response
from utils.config_utils import get_current_env


def test_movie_videos():
    env = get_current_env()
    BASE_URL = env["base_url"]
    API_KEY = env["api_key"]

    movie_id = 550  # 예시로 Fight Club의 ID 사용
    endpoint = f"/movie/{movie_id}/videos"
    params = {"api_key": API_KEY}

    response = send_get_request(endpoint, params)
    attach_response(response)
    data = response.json()

    assert "results" in data, "검색 실패"
    assert len(data["results"]) > 0, "비디오 결과가 없습니다"

    print("\n🎬 비디오 정보")
    for video in data["results"]:
        print(f"📹 제목: {video['name']}, 유형: {video['type']}, 키: {video['key']}")