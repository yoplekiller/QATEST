import os
import datetime
import shutil
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = "failed_screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_name = f"{item.name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot_path = os.path.join(screenshots_dir, screenshot_name)
            driver.save_screenshot(screenshot_path)
<<<<<<< HEAD
            allure.attach.file(
                screenshot_path,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
=======


            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
>>>>>>> main
            )
