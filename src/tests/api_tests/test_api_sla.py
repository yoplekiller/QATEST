import time
import pytest
import requests

SLA_SECONDS = 2

@pytest.mark.parametrize("endpoint", [
        "https://api.themoviedb.org/3/movie/popular?api_key=api_key",
        "https://api.themoviedb.org/3/genre/movie/list?api_key=api_key"
])
def test_api_sla(endpoint):
    start_time = time.time()
    response = requests.get(endpoint)
    elapsed_time = time.time() - start_time

    assert response.status_code == 200, f"❌ 응답 실패: {response.status_code}"
    assert response.time < SLA_SECONDS, f"❌ SLA 초과: {elapsed_time:.2f}초"

    print(f"✅ SLA 만족: {elapsed_time:.2f}초")