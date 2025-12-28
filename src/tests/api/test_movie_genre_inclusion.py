import allure
import pytest
from utils.api_utils import send_get_request, attach_response
from utils.config_utils import get_current_env
from utils.data_loader import load_genre_test_data

@pytest.mark.api
@pytest.mark.parametrize(["movie_id", "expected_genres"], load_genre_test_data())
def test_movie_genre_inclusion(movie_id, expected_genres):


    env = get_current_env()
    API_KEY = env["api_key"]

    endpoint = f"/movie/{movie_id}"
    params = {"api_key": API_KEY}

    response = send_get_request(endpoint, params)
    attach_response(response)
    data = response.json()


    assert "genres" in data, "검색 실패"
    assert [genre["name"] for genre in data["genres"]] == expected_genres


    print(data["genres"])



