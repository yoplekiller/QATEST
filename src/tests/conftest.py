import os
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from utils.api_utils import APIEnv
from webdriver_manager.chrome import ChromeDriverManager
from src.pages.kurly_main_page import KurlyMainPage
from src.pages.kurly_cart_page import KurlyCartPage
from src.pages.kurly_login_page import KurlyLoginPage
from src.pages.kurly_product_page import KurlyProductPage
from src.pages.kurly_search_page import KurlySearchPage
from utils.config_utils import load_config



# ✅ CI 환경 감지 (GitHub Actions, Docker)
IS_CI = os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    # options.add_argument("--headless") # 헤드리스 모드
    options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 감지 방지
    options.add_argument("--no-sandbox") # 샌드박스 비활성화
    options.add_argument("--disable-dev-shm-usage") # /dev/shm 사용 안함
    options.add_argument("--disable-gpu") # GPU 비활성화
    options.add_argument("--window-size=1920,1080") # 창 크기 설정
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36") # 사용자 에이전트 설정

    # ✅ CI 환경에서는 캐시 삭제로 손상된 드라이버 방지
    if IS_CI:
        cache_dir = os.path.expanduser("~/.wdm")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # ✅ Selenium 감지 우회 (CDP 명령어)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })

    yield driver
    driver.quit()

# =================================
# Page Object Fixtures
# =================================

@pytest.fixture
def kurly_main_page(driver) -> KurlyMainPage:
    """마켓컬리 메인 페이지 객체"""
    return KurlyMainPage(driver)


@pytest.fixture
def kurly_login_page(driver) -> KurlyLoginPage:
    """마켓컬리 로그인 페이지 객체"""
    return KurlyLoginPage(driver)

@pytest.fixture
def kurly_search_page(driver) -> KurlySearchPage:
    """마켓컬리 검색 페이지 객체"""
    return KurlySearchPage(driver)

@pytest.fixture
def kurly_product_page(driver) -> KurlyProductPage:
    """마켓컬리 상품 페이지 객체"""
    return KurlyProductPage(driver)


@pytest.fixture
def kurly_cart_page(driver) -> KurlyCartPage:
    """마켓컬리 장바구니 페이지 객체"""
    return KurlyCartPage(driver)

@pytest.fixture
def test_credentials() -> dict:
    """테스트용 계정 정보 제공"""
    return {
        "username": os.getenv("KURLY_TEST_USERNAME", "testuser"),
        "password": os.getenv("KURLY_TEST_PASSWORD", "testpass")
    }

@pytest.fixture
def test_credentials_invalid() -> dict:
    """테스트용 잘못된 계정 정보 제공"""
    return {
        "username": "invalid_user_12345",
        "password": "wrong_password_67890"
    }

# =================================
# API Fixtures
# =================================

# APIEnv 인스턴스 fixture
@pytest.fixture(scope="session")
def api_env() -> APIEnv:
    """API 테스트용 환경 변수 및 APIEnv 인스턴스 제공"""
    env = load_config()
    return APIEnv()


# APIEnv 인스턴스의 메서드를 fixture로 제공
@pytest.fixture
def send_get_request(api_env) -> callable:
    return api_env.send_get_request

@pytest.fixture
def send_post_request(api_env) -> callable:
    return api_env.send_post_request

@pytest.fixture
def send_get_request_no_raise(api_env) -> callable:
    return api_env.send_get_request_no_raise


# =================================
# ALLURE Fixtures
# =================================
@pytest.fixture
def allure_attach_response(api_env) -> callable:
    return api_env.attach_response

@pytest.fixture
def attach_response(api_env) -> callable:
    return api_env.attach_response
