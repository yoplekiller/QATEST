import allure
import pytest

@pytest.mark.api
@allure.feature("TMDB API - Error Handling")
@allure.story("404 Not Found")
@allure.title("TMDB API 오류 처리 테스트")
class ErrorHandlingTests:
              
    @allure.title("존재하지 않는 영화 ID로 조회 시 404 반환")
    def test_movie_not_found(self, api_env, send_get_request_no_raise, attach_response):

        API_KEY = api_env.api_key

        with allure.step("존재하지 않는 영화 ID로 요청 전송"):  
            endpoint = "/movie/0"  # 존재하지 않는 영화 ID
            response = send_get_request_no_raise(endpoint, params={"api_key": API_KEY})
            assert response.status_code == 404, "상태 코드가 404가 아닙니다"
            attach_response(response)

        with allure.step("응답 JSON 파싱"):
             data = response.json()
        
        with allure.step("상세 오류 코드 및 메시지 검증"):
            assert data["status_code"] == 34, "상세 오류 코드가 34가 아닙니다"
            assert data["status_message"] == "The resource you requested could not be found.", "상세 오류 메시지가 일치하지 않습니다"

    @allure.title("빈 API 키로 요청 시 401 반환")
    def test_empty_api_key(self, send_get_request_no_raise, attach_response):
        endpoint = "/movie/popular"

        with allure.step("빈 API 키로 요청 전송"):
            response = send_get_request_no_raise(endpoint, params={"api_key": ""})
        with allure.step("응답 상태 코드 검증"):
            assert response.status_code == 401, "상태 코드가 401이 아닙니다"
            attach_response(response)

    @allure.title("API 키  누락 시 401 반환")
    def test_missing_api_key(self, send_get_request_no_raise, attach_response):
        endpoint = "/movie/popular"

        with allure.step("API 키 누락로 요청 전송"):
            response = send_get_request_no_raise(endpoint)
        with allure.step("응답 상태 코드 검증"):
            assert response.status_code == 401, "상태 코드가 401이 아닙니다"
        attach_response(response)

    @allure.title("잘못된 API 키로 요청 시 401 반환")
    def test_invalid_api_key(self, send_get_request_no_raise, attach_response):
        endpoint = "/movie/popular"
        with allure.step("잘못된 API 키로 요청 전송"):
            response = send_get_request_no_raise(endpoint, params={"api_key": "INVALID_KEY"})
        with allure.step("응답 상태 코드 검증"):
            assert response.status_code == 401, "상태 코드가 401이 아닙니다"
            attach_response(response)

    @allure.title("빈 검색어로 검색 시 빈 결과 반환")
    def test_empty_search_query(self, api_env, send_get_request_no_raise, attach_response):
        API_KEY = api_env["api_key"]
        endpoint = "/search/movie"

        with allure.step("빈 검색어로 검색 전송"):
            response = send_get_request_no_raise(endpoint, params={"api_key": API_KEY, "query": ""})
        with allure.step("응답 상태 코드 검증"):
            assert response.status_code == 200, "상태 코드가 200이 아닙니다"
            attach_response(response)
        with allure.step("응답 JSON 파싱"):
            data = response.json()
        with allure.step("검색 결과 검증"):
            assert data["total_results"] == 0, "검색 결과가 비어있지 않습니다"

            
    @allure.title("잘못된 페이지 번호로 요청 시 422 반환")
    def test_invalied_page_number(self, api_env, send_get_request_no_raise, attach_response):
        API_KEY = api_env["api_key"]
        endpoint = "/movie/popular"
        with allure.step("잘못된 페이지 번호로 요청 전송"):
            response = send_get_request_no_raise(endpoint, params={"api_key": API_KEY, "page": -1})
        with allure.step("응답 상태 코드 검증"):
            assert response.status_code == 422, "상태 코드가 422가 아닙니다"
            attach_response(response)

    @allure.title("잘못된 언어 코드로 요청 시 기본값 반환")
    def test_invalid_language_code(self, api_env, send_get_request, attach_response):
        API_KEY = api_env["api_key"]
        endpoint = "/movie/popular"

        with allure.step("잘못된 언어 코드로 요청 전송"):
            response = send_get_request(endpoint, params={"api_key": API_KEY, "language": "xx-YY"})
        with allure.step("응답 상태 코드 검증"):
            assert response.status_code == 200, "상태 코드가 200이 아닙니다"
            attach_response(response)

    @allure.title("존재하지 않는 엔드포인트로 요청 시 404 반환")
    def test_nonexistent_endpoint(self, api_env, send_get_request_no_raise, attach_response):
        API_KEY = api_env["api_key"]
        endpoint = "/movie/nonexistent_endpoint"
        
        with allure.step("존재하지 않는 엔드포인트로 요청 전송"):
            response = send_get_request_no_raise(endpoint, params={"api_key": API_KEY})

        with allure.step("응답 상태 코드 검증"):
            assert response.status_code == 404, "상태 코드가 404가 아닙니다"
            attach_response(response)