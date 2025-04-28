import requests
import allure


@allure.step("GET 요청 보내기")
def send_get_request(endpoint, params=None, headers=None):
    try:
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        allure.attach(str(e), name="GET 요청 에러", attachment_type=allure.attachment_type.TEXT)
        raise


@allure.step("POST 요청 보내기")
def send_post_request(endpoint, data=None, json=None, headers=None):
    try:
        response = requests.post(endpoint, data=data, json=json, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        allure.attach(str(e), name="POST 요청 에러", attachment_type=allure.attachment_type.TEXT)
        raise
