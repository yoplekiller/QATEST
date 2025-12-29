import pytest
import allure


@pytest.mark.api
@allure.title("영화 목록 페이지네이션 테스트")
@allure.story("영화 API 테스트")
class TestMoviePagination:
    @allure.title("페이지 1 조회 - 기본 페이지네이션")
    @allure.description("영화 목록의 첫 번째 페이지를 조회하여 정상 동작을 확인합니다.")
    def test_movie_pagination_page_1(self, send_get_request,  api_env):

        api_env = load_config()
        API_KEY = api_env["api_key"]

        endpoint = "/movie/popular"
        params = {"api_key": API_KEY, "page": 1}

        with allure.step("GET 요청 전송: /movie/popular?page=1"):
            response = send_get_request(endpoint, params=params)

        with allure.step("응답 상태 코드 확인"):
            assert response.status_code == 200, "응답 코드가 200이 아닙니다."

        data = response.json()

        with allure.step("페이지 번호 검증"):
            assert data["page"] == 1, "페이지 번호가 1이 아닙니다."

        with allure.step("총 페이지 수 검증"):
            assert data["total_pages"] >= 1, "총 페이지 수가 1보다 작습니다."

        with allure.step("총 결과 검증 수"):
            assert data["total_results"] >= 1, "총 결과 수가 1보다 작습니다."

        with allure.step("결과 배열 검증"):
            assert len(data["results"]) > 0, "영화 결과가 없습니다"
            assert len(data["results"]) <= 20, "한 페이지에 20개 이상의 결과가 있습니다."



    @allure.title("페이지 2 조회 - 페이지네이션 테스트")
    @allure.description("영화 목록의 두 번째 페이지를 조회하여 첫 페이지와 다른 결과를 반환하는지 검증.")
    def test_movie_pagination_page_2(self):
        endpoint = "/movie/popular"
        
        with allure.step("페이지 1 조회"):
            param_page_1 = {"api_key": API_KEY, "page": 1}
            response_page_1 = send_get_request(endpoint, params=param_page_1)
            assert response_page_1.status_code == 200, "페이지 1 응답 코드가 200이 아닙니다."
            data_page_1 = response_page_1.json()

        with allure.step("페이지 2 조회"):
            param_page_2 = {"api_key": API_KEY, "page": 2}
            response_page_2 = send_get_request(endpoint, params=param_page_2)
            assert response_page_2.status_code == 200, "페이지 2 응답 코드가 200이 아닙니다."
            data_page_2 = response_page_2.json()
        
        with allure.step("페이지 번호 검증"):
            assert data_page_2["page"] == 2, "페이지 번호가 2이 아닙니다."

        with allure.step("총 페이지/결과 수 일관 "):
            assert data_page_2["total_pages"] == data_page_1["total_pages"], "총 페이지 수가 일치하지 않습니다."
            assert data_page_2["total_results"] == data_page_1["total_results"], "총 결과 수가 일치하지 않습니다."

        with allure.step("페이지 1과 페이지 2 결과 비교"):
            ids_page_1 = {movie["id"] for movie in data_page_1["results"]}
            ids_page_2 = {movie["id"] for movie in data_page_2["results"]}
            assert not ids_page_1.intersection(ids_page_2), "페이지 1과 페이지 2에 중복된 영화가 있습니다."


    @allure.title("잘못된 페이지 번호 - 0 이하")
    @allure.description("페이지 번호가 0 이하일 때 에러 처리 또는 기본값으로 처리되는지 검증")
    def test_pagination_invalid_page_zero(self):
        """페이지 번호 0 요청 시 처리"""
        endpoint = "/movie/popular"
        params = {
            "api_key": API_KEY,
            "page": 0
        }

        with allure.step("GET 요청: page=0"):
            response = send_get_request(endpoint, params=params)

        data = response.json()

        with allure.step("응답 검증 (페이지 1로 처리되거나 에러)"):
            # TMDB API는 page=0을 page=1로 처리함
            assert data["page"] >= 1, "페이지는 1 이상이어야 합니다"


    @allure.title("범위 초과 페이지 번호")
    @allure.description("존재하지 않는 큰 페이지 번호 요청 시 처리 검증")
    def test_pagination_out_of_range(self):
        """범위를 초과한 페이지 번호 요청"""
        endpoint = "/movie/popular"
        params = {
            "api_key": API_KEY,
            "page": 99999
        }

        with allure.step("GET 요청: page=99999"):
            response = send_get_request(endpoint, params=params)

        data = response.json()

        with allure.step("응답 검증"):
            # 범위 초과 시 빈 결과 또는 마지막 페이지 반환
            assert response.status_code == 200, "상태 코드는 200이어야 합니다"
            # 결과가 비어있거나 마지막 페이지를 반환
            if data["results"]:
                assert data["page"] <= data["total_pages"], \
                    "페이지 번호는 총 페이지 수를 초과할 수 없습니다"

        with allure.step("결과 항목 수 검증"):
            assert "results" in data, "검색 실패"
            assert len(data["results"]) > 0, "영화 결과가 없습니다"