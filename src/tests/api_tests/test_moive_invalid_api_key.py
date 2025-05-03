import allure
from utils.api_utils import send_get_request, attach_response


@allure.feature("예외 케이스")
@allure.story("잘못된 API 키")
@allure.title("API 키가 잘못 되었을 때 401 Unauthorized 확인")
def test_movie_invalid_api_key():

    endpoint = "/search/movie"
    params = {
        "api_key": "invalid_key",
        "query": "Inception"
    }
    response = send_get_request(endpoint, params)
    attach_response(response)

    assert  response.status_code == 401