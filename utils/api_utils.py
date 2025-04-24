import requests
from config.api_env_config import BASE_URL, API_KEY


def send_get_request(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    default_params = {"api_key": API_KEY}
    if params:
        default_params.update(params)
    return requests.get(url, params=default_params)