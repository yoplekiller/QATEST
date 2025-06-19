import os
import yaml

# 이 파일이 있는 위치: QATEST/utils/config_utils.py
# → 여기서 QATEST/src/config/config.yaml로 접근해야 함

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CURRENT_DIR, "..", "src", "config", "config.yaml")
CONFIG_PATH = os.path.abspath(CONFIG_PATH)  # 절대 경로화

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_current_env():
    config = load_config()
    current_env = config.get("default", "dev")
    env_data = config["env"].get(current_env, {})

    api_key = os.getenv("TMDB_API_KEY", env_data.get("api_key"))
    return {
        "base_url": env_data.get("base_url"),
        "api_key": api_key
    }
