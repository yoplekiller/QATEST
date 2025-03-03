import requests


def test_kurly_search():
    url = "https://api.kurly.com/search/v4/sites/market/normal-search"
    params = {"keyword": "과자", "sortType": 4, "page": 1}

    response = requests.get(url, params=params)

    assert response.status_code == 200, f"❌ API 요청 실패 (상태 코드: {response.status_code})"
    assert "products" in response.json()["data"], "❌ 상품 데이터가 응답에 없음"

    print("✅ API 테스트 성공")