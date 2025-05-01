import os
import yaml

CONFIG_PATH = "config/config.yaml"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_current_env():
    """현재 설정된 환경(dev, staging, prod)에 맞는 base_url과 api_key 가져오기"""
    config = load_config()
    current_env = config.get("default", "dev")
    env_data = config["env"].get(current_env, {})

    api_key = os.getenv("TMDB_API_KEY", env_data.get("api_key"))
    return {
        "base_url":env_data.get("base_url"),
        "api_key": api_key
    }




