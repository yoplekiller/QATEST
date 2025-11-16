import os
import yaml


# 현재 파일(utils/config_utils.py)의 절대 경로를 구함
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 경로(=utils 상위 디렉토리) 계산
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
# config.yaml의 절대 경로 설정
CONFIG_PATH = os.path.join(PROJECT_ROOT, "src", "config", "config.yaml")