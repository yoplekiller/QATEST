import time
import allure
import pytest


SLA_SECONDS = 2

@pytest.mark.api
@allure.feature("영화 목록 API 테스트")
@allure.story("영화 페이지 SLA 응답 시간 테스트")
@allure.title("SLA 응답 시간 테스트 - 2초 미만")
@pytest.mark.parametrize("endpoint", [
    "/movie/popular",
    "/genre/movie/list"
])
def test_api_sla(api_env, send_get_request, endpoint):


    api_key = api_env.api_key
    base_url = api_env.base_url
    endpoint = f"{base_url}{endpoint}?api_key={api_key}"
    
    with allure.step(f"요청 보내기: {endpoint}"):
        start_time = time.time()
        response = send_get_request(endpoint)
        elapsed_time = time.time() - start_time

    with allure.step("응답 시간 첨부"):
      allure.attach(f"응답 시간: {elapsed_time:.2f}초", name="Response Time", attachment_type=allure.attachment_type.TEXT)

    with allure.step("SLA 응답 시간 및 상태 코드 검증"):
        # 200(OK)뿐만 아니라 204(No Content)도 성공으로 간주하도록 수정
        assert response.status_code in [200, 204], f"❌ 응답 실패: {response.status_code}"
        assert elapsed_time < SLA_SECONDS, f"❌ SLA 초과: {elapsed_time:.2f}초"

