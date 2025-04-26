import allure
import requests
from config.api_env_config import BASE_URL, API_KEY
import json


def send_get_request(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    default_params = {"api_key": API_KEY}
    if params:
        default_params.update(params)
    return requests.get(url, params=default_params)


@allure.step("API 응답 결과 첨부")
def attach_response(response):
    """Allure 리포트에 API 응답을 JSON 형식으로 첨부"""
    try:
        json_body = json.dumps(response.json(), indent=2, ensure_ascii=False)
        allure.attach(json_body, name="응답 JSON", attachment_type=allure.attachment_type.JSON)
    except Exception:
        allure.attach(response.text, name="응답 본문 (raw)", attachment_type=allure.attachment_type.TEXT)
