import json
import os
import re
from dotenv import load_dotenv
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from src.pages.kurly_main_page import KurlyMainPage
from src.pages.kurly_login_page import KurlyLoginPage
from src.pages.kurly_search_page import KurlySearchPage
from src.pages.kurly_cart_page import KurlyCartPage
from src.pages.kurly_goods_page import KurlyGoodsPage

load_dotenv()

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless") # 헤드리스 모드
    options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 감지 방지
    options.add_argument("--no-sandbox") # 샌드박스 비활성화
    options.add_argument("--disable-dev-shm-usage") # /dev/shm 사용 안함
    options.add_argument("--disable-gpu") # GPU 비활성화
    options.add_argument("--window-size=1920,1080") # 창 크기 설정
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36") # 사용자 에이전트 설정
    # 실패 증거로 브라우저 콘솔 로그를 남기기 위해 수집 활성화
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    # 드라이버 바이너리는 Selenium 내장 Selenium Manager 가 설치된 Chrome 버전에 맞춰 찾는다.
    # 예전에는 CI 에서 driver 픽스처가 만들어질 때마다 ~/.wdm 캐시를 지우고 webdriver-manager 로
    # 다시 설치했는데, xdist 병렬에서는 한 워커가 다음 모듈을 시작하며 공유 캐시를 지우는 순간
    # 다른 워커들의 chromedriver 세션이 함께 끊겼다(2026-11-01 CI: Connection refused 로 8건 실패).
    driver = webdriver.Chrome(service=Service(), options=options)

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
def kurly_main_page(driver) -> KurlyMainPage:
    """마켓컬리 메인 페이지 객체"""
    return KurlyMainPage(driver)


@pytest.fixture
def kurly_login_page(driver) -> KurlyLoginPage:
    """마켓컬리 로그인 페이지 객체"""
    return KurlyLoginPage(driver)

@pytest.fixture
def kurly_search_page(driver):
    """마켓컬리 검색 페이지 객체"""
    return KurlySearchPage(driver)

@pytest.fixture
def kurly_goods_page(driver) -> KurlyGoodsPage:
    """마켓컬리 상품 페이지 객체"""
    return KurlyGoodsPage(driver)


@pytest.fixture
def kurly_cart_page(driver) -> KurlyCartPage:
    """마켓컬리 장바구니 페이지 객체"""
    return KurlyCartPage(driver)


@pytest.fixture
def test_credentials():
    """테스트용 계정 정보 제공"""
    return {
        "username": os.getenv("KURLY_TEST_USERNAME", "testuser"),
        "password": os.getenv("KURLY_TEST_PASSWORD", "testpass")
    }

@pytest.fixture
def test_credentials_invalid():
    """테스트용 잘못된 계정 정보 제공"""
    return {
        "username": "invalid_user@example.com",
        "password": "wrong_password123"
    }

# ========================================
# 실패 증거 자동 수집
# ========================================

EVIDENCE_DIR = "test-evidence"


def _driver_of(item):
    """테스트가 쓴 WebDriver 찾기 (driver 픽스처 또는 page object 의 .driver)"""
    funcargs = getattr(item, "funcargs", {}) or {}
    if "driver" in funcargs:
        return funcargs["driver"]
    for value in funcargs.values():
        driver = getattr(value, "driver", None)
        if driver is not None:
            return driver
    return None


def _collect_evidence(item, driver) -> None:
    """
    실패 시점의 스크린샷 / 현재 URL / page source / 브라우저 콘솔 로그를
    Allure 첨부 + test-evidence/<테스트>/ 파일로 남긴다(CI artifact 업로드용).

    증거 수집이 실패해도 원래 실패를 가리면 안 되므로 항목별로 예외를 삼킨다.
    """
    safe_name = re.sub(r"[^0-9A-Za-z가-힣._-]+", "_", item.nodeid)[-150:]
    folder = os.path.join(EVIDENCE_DIR, safe_name)
    os.makedirs(folder, exist_ok=True)

    collectors = {
        "screenshot.png": lambda: driver.get_screenshot_as_png(),
        "url.txt": lambda: driver.current_url,
        "page_source.html": lambda: driver.page_source,
        "console.log": lambda: "\n".join(
            f"[{entry.get('level')}] {entry.get('message')}" for entry in driver.get_log("browser")
        ),
    }
    allure_types = {
        "screenshot.png": allure.attachment_type.PNG,
        "url.txt": allure.attachment_type.TEXT,
        "page_source.html": allure.attachment_type.HTML,
        "console.log": allure.attachment_type.TEXT,
    }
    for filename, collect in collectors.items():
        try:
            data = collect()
        except Exception as e:  # 세션이 죽었거나 드라이버가 로그를 지원하지 않는 경우
            data = f"수집 실패: {type(e).__name__}: {e}"
            filename = filename.rsplit(".", 1)[0] + "_error.txt"
        mode, payload = ("wb", data) if isinstance(data, bytes) else ("w", str(data))
        with open(os.path.join(folder, filename), mode, **({} if mode == "wb" else {"encoding": "utf-8"})) as f:
            f.write(payload)
        try:
            allure.attach(
                payload,
                name=f"실패 증거 - {filename}",
                attachment_type=allure_types.get(filename, allure.attachment_type.TEXT),
            )
        except Exception:
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # call 단계 실패만 (xfail 로 예상된 실패는 report.failed 가 아니라 skipped 로 온다)
    if report.when != "call" or not report.failed:
        return
    driver = _driver_of(item)
    if driver is not None:
        _collect_evidence(item, driver)


# ========================================
# Flaky 가시화: 재시도(--reruns)로 통과한 테스트를 따로 집계
# ========================================

_rerun_nodeids: set = set()
_final_outcome: dict = {}


def pytest_runtest_logreport(report):
    """
    pytest-rerunfailures 는 재시도 전 실패를 outcome='rerun' 으로 보고한다.
    xdist 를 쓰면 워커의 리포트가 컨트롤러로 전달돼 여기서 함께 집계된다.
    """
    if report.outcome == "rerun":
        _rerun_nodeids.add(report.nodeid)
        return
    if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
        _final_outcome[report.nodeid] = report.outcome


def _flaky_summary() -> dict:
    flaky = sorted(n for n in _rerun_nodeids if _final_outcome.get(n) == "passed")
    still_failed = sorted(n for n in _rerun_nodeids if _final_outcome.get(n) == "failed")
    return {"flaky_passed_on_rerun": flaky, "failed_after_rerun": still_failed}


def pytest_terminal_summary(terminalreporter):
    if hasattr(terminalreporter.config, "workerinput"):
        return
    summary = _flaky_summary()
    if summary["flaky_passed_on_rerun"]:
        terminalreporter.section("FLAKY (재시도 후 통과 - 통과로 치지 말고 원인 확인 필요)", yellow=True)
        for nodeid in summary["flaky_passed_on_rerun"]:
            terminalreporter.line(f"  ⚠️ {nodeid}")


def pytest_sessionfinish(session):
    # xdist 워커는 쓰지 않고 컨트롤러(또는 단일 프로세스)만 결과 파일을 쓴다
    if hasattr(session.config, "workerinput"):
        return
    with open("test_results_flaky.json", "w", encoding="utf-8") as f:
        json.dump(_flaky_summary(), f, ensure_ascii=False, indent=2)
