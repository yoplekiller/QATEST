import time
import allure
import pytest
import requests
from utils.config_utils import get_current_env

env_data = get_current_env()
API_KEY = env_data["api_key"]
BASE_URL = env_data["base_url"]

SLA_SECONDS = 2


@pytest.mark.api
@allure.feature("영화 목록 API 테스트")
@allure.story("영화 페이지 SLA 응답 시간 테스트")
@allure.title("SLA 응답 시간 테스트 - 2초 미만")
@allure.step("SLA 응답 시간 테스트: {endpoint}")
@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/movie/popular?api_key={API_KEY}",
    f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
])
def test_api_sla(endpoint):
    start_time = time.time()
    response = requests.get(endpoint)
    elapsed_time = time.time() - start_time

    print(f"📡 요청 주소: {endpoint}")
    print(f"✅ 응답 시간: {elapsed_time:.2f}초")
    print(f"✅ 응답 코드: {response.status_code}")

    assert response.status_code == 200, f"❌ 응답 실패: {response.status_code}"
    assert elapsed_time < SLA_SECONDS, f"❌ SLA 초과: {elapsed_time:.2f}초"

