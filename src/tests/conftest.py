import os
import datetime
from dotenv import load_dotenv
import shutil
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.pages.kurly_main_page import KurlyMainPage
from src.pages.kurly_login_page import KurlyLoginPage

load_dotenv()

# ✅ CI 환경 감지 (GitHub Actions, Docker)
IS_CI = os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

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

# ========================================
# Page Object Fixtures
# ========================================

@pytest.fixture
def kurly_main_page(driver):
    """마켓컬리 메인 페이지 객체"""
    return KurlyMainPage(driver)


@pytest.fixture
def kurly_login_page(driver):
    """마켓컬리 로그인 페이지 객체"""

    return KurlyLoginPage(driver)


@pytest.fixture
def kurly_product_page(driver):
    """마켓컬리 상품 페이지 객체"""
    from src.pages.kurly_product_page import KurlyProductPage
    return KurlyProductPage(driver)


@pytest.fixture
def kurly_cart_page(driver):
    """마켓컬리 장바구니 페이지 객체"""
    from src.pages.kurly_cart_page import KurlyCartPage
    return KurlyCartPage(driver)


@pytest.fixture
def kurly_search_page(driver):
    """마켓컬리 검색 페이지 객체"""
    from src.pages.kurly_search_page import KurlySearchPage
    return KurlySearchPage(driver)


# ========================================
# Test Data Fixtures
# ========================================

@pytest.fixture
def test_credentials_invalid():
    """잘못된 로그인 자격증명"""
    return {
        "username": "invalid_user@example.com",
        "password": "wrong_password123"
    }


# ========================================
# API Test Fixtures
# ========================================

@pytest.fixture(scope="function")
def api_env():
    """API 환경 설정 객체"""
    from utils.api_utils import APIEnv
    return APIEnv()


@pytest.fixture
def send_get_request(api_env):
    """GET 요청 보내기"""
    return api_env.send_get_request


@pytest.fixture
def attach_response(api_env):
    """API 응답 첨부"""
    return api_env.attach_response


@pytest.fixture
def allure_attach_response(api_env):
    """API 응답 전체 첨부 (상태 코드 포함)"""
    return api_env.allure_attach_response
