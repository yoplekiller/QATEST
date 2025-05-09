import time
import pytest
import requests
from utils.api_utils import env_data

SLA_SECONDS = 2
API_KEY = env_data["api_key"]

@pytest.mark.parametrize("endpoint", [
    f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}",
    f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}"
])
def test_api_sla(endpoint):
    start_time = time.time()
    response = requests.get(endpoint)
    elapsed_time = time.time() - start_time

    assert response.status_code == 200, f"❌ 응답 실패: {response.status_code}"
    assert elapsed_time < SLA_SECONDS, f"❌ SLA 초과: {elapsed_time:.2f}초"

    print(f"✅ SLA 만족: {elapsed_time:.2f}초")

