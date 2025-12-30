import requests
import allure
import json
from utils.config_utils import load_config


class APIEnv:
    def __init__(self):
        env_data = load_config()
        self.base_url = env_data["base_url"]
        self.api_key = env_data["api_key"]

    @allure.step("GET 요청 보내기")
    def send_get_request(self, endpoint, params=None, headers=None):
        try:
            full_url = self.base_url + endpoint
            response = requests.get(full_url, params=params, headers=headers)
            self.attach_response(response)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            allure.attach(str(e), name="GET 요청 에러", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("POST 요청 보내기")
    def send_post_request(self, endpoint, data=None, json_data=None, headers=None):
        try:
            full_url = self.base_url + endpoint
            response = requests.post(full_url, data=data, json=json_data, headers=headers)
            self.attach_response(response)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            allure.attach(str(e), name="POST 요청 에러", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("GET 요청 보내기 (상태 코드 확인하지 않음)")
    def send_get_request_no_raise(self, endpoint, params=None, headers=None):
        """상태 코드를 확인하지 않고 응답을 반환하는 GET 요청 함수"""
        full_url = self.base_url + endpoint
        response = requests.get(full_url, params=params, headers=headers)
        self.attach_response(response)
        return response

    @allure.step("API 응답 결과 첨부")
    def attach_response(self, response):
        try:
            json_body = json.dumps(response.json(), indent=2, ensure_ascii=False)
            allure.attach(json_body, name="응답 JSON", attachment_type=allure.attachment_type.JSON)
        except Exception:
            allure.attach(response.text, name="응답 본문 (raw)", attachment_type=allure.attachment_type.TEXT)
            

    @allure.step("API 응답 상태 코드 첨부")
    def allure_attach_status_code(self, response):
        try:
            status_code_info = f"응답 상태 코드: {response.status_code}"
            allure.attach(status_code_info, name="응답 상태 코드", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(str(e), name="상태 코드 첨부 에러", attachment_type=allure.attachment_type.TEXT)

    @allure.step("API 응답 전체 첨부")
    def allure_attach_response(self, response):
        try:
            self.allure_attach_status_code(response)
            self.attach_response(response)
        except Exception as e:
            allure.attach(str(e), name="응답 첨부 에러", attachment_type=allure.attachment_type.TEXT)