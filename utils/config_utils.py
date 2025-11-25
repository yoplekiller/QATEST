import os
import yaml


# 현재 파일(utils/config_utils.py)의 절대 경로를 구함
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 경로(=utils 상위 디렉토리) 계산
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
# config.yaml의 절대 경로 설정
CONFIG_PATH = os.path.join(PROJECT_ROOT, "src", "config", "config.yaml")


def load_config():
    """config.yaml 파일을 로드하고 기본 환경 설정을 반환"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            
        # 기본 환경 가져오기
        default_env = config.get('default', 'dev')
        env_config = config['env'][default_env]
        
        return env_config
    except Exception as e:
        raise Exception(f"설정 파일 로드 실패: {e}")


def get_current_env():
    """현재 환경 설정을 반환 (load_config와 동일)"""
    return load_config()