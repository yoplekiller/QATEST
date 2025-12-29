import allure
import pytest
from utils.data_loader import load_genre_test_data

@pytest.mark.api
@allure.feature("영화 상세 정보 API 테스트")
@allure.story("영화 장르 포함 여부 테스트")
@allure.title("영화 ID {movie_id}의 장르 포함 여부 테스트")
@pytest.mark.parametrize(["movie_id", "expected_genres"], load_genre_test_data())
def test_movie_genre_inclusion(movie_id, expected_genres, send_get_request, allure_attach_response, api_env):
    """특정 영화의 상세 정보에서 장르 포함 여부 테스트"""
    API_KEY = api_env["api_key"]


    with allure.step(f"영화 ID {movie_id}에 대한 상세 정보 조회"):
        endpoint = f"/movie/{movie_id}"
        params = {"api_key": API_KEY}

        response = send_get_request(endpoint, params)
        allure_attach_response(response)
        data = response.json()

        with allure.step("응답 데이터의 장르 포함 여부 검증"):  
            assert "genres" in data, "검색 실패"
            assert [genre["name"] for genre in data["genres"]] == expected_genres


    print(data["genres"])



