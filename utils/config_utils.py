"""
Configuration Utilities

이 모듈은 테스트 환경 설정 및 환경변수 관리를 담당합니다.

환경변수 로딩 순서:
1. 시스템 환경변수 (os.getenv)
2. .env 파일 (load_dotenv로 로드)
3. config.yaml 파일 (폴백)

주요 함수:
- load_config(): 현재 환경 설정 로드 (base_url, api_key 포함)
- get_current_env(): Deprecated - load_config() 사용 권장
- get_test_credentials(): 테스트 계정 정보 로드 (username, password)

사용 예:
    from utils.config_utils import load_config, get_test_credentials

    # API 설정 로드
    config = load_config()
    api_key = config['api_key']
    base_url = config['base_url']

    # 테스트 계정 정보 로드
    creds = get_test_credentials()
    username = creds['username']
    password = creds['password']
"""
import os
import yaml
import warnings
from dotenv import load_dotenv


# 현재 파일(utils/config_utils.py)의 절대 경로를 구함
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 경로(=utils 상위 디렉토리) 계산
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
# config.yaml의 절대 경로 설정
CONFIG_PATH = os.path.join(PROJECT_ROOT, "src", "config", "config.yaml")
# .env 파일 경로
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

# .env 파일 로드 (존재하는 경우)
load_dotenv(ENV_PATH)


def load_config():
    """
    config.yaml 파일을 로드하고 환경변수와 병합하여 반환
    환경변수가 설정되어 있으면 config.yaml보다 우선적으로 사용
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        # 환경 변수에서 TEST_ENV를 읽거나 기본값 사용
        env_name = os.getenv('TEST_ENV', config.get('default', 'dev'))
        env_config = config['env'][env_name].copy()

        # 환경변수에서 API 키 로드 (우선순위: 환경변수 > config.yaml)
        api_key = os.getenv('TMDB_API_KEY')
        if not api_key:
            api_key = env_config.get('api_key')

        if not api_key:
            raise ValueError(
                "❌ TMDB API 키가 설정되지 않았습니다.\n"
                "다음 중 하나를 수행하세요:\n"
                "1. .env 파일에 TMDB_API_KEY=your_key 추가\n"
                "2. 시스템 환경변수로 TMDB_API_KEY 설정"
            )

        env_config['api_key'] = api_key

        return env_config
    except FileNotFoundError:
        raise Exception(f"❌ 설정 파일을 찾을 수 없습니다: {CONFIG_PATH}")
    except KeyError as e:
        raise Exception(f"❌ 설정 파일에 필수 키가 없습니다: {e}")
    except Exception as e:
        raise Exception(f"❌ 설정 파일 로드 실패: {e}")


def get_current_env() -> str:
    """현재 환경 설정을 반환 (load_config와 동일)"""
    warnings.warn(
        "get_current_env 함수는 곧 deprecated 될 예정입니다. 대신 load_config 함수를 사용하세요.",
        DeprecationWarning
    )
    return load_config()


def get_test_credentials():
    """
    테스트 계정 정보를 환경변수에서 로드
    Returns:
        dict: {'username': str, 'password': str}
    """
    username = os.getenv('KURLY_TEST_USERNAME')
    password = os.getenv('KURLY_TEST_PASSWORD')

    if not username or not password:
        raise ValueError(
            "❌ 테스트 계정 정보가 설정되지 않았습니다.\n"
            ".env 파일에 다음을 추가하세요:\n"
            "KURLY_TEST_USERNAME=your_username\n"
            "KURLY_TEST_PASSWORD=your_password"
        )

    return {
        'username': username,
        'password': password
    }