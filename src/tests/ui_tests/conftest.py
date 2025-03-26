import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 웹 실행
@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")  # GUI없는 환경에서도 실행 가능
    chrome_options.add_argument("--disable-dev-shm-usage") #메모리 부족 방지
    chrome_options.add_argument("--no-sandbox") #샌드박스 비활성화
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--window-size=1920,1080")


    service_obj = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service_obj,options=chrome_options)

    driver.get("https://www.kurly.com/main")
    driver.find_element(By.XPATH,"//input[@id='gnb_search']").click()
    driver.implicitly_wait(10)

    yield driver   # 테스트 실행

    driver.quit()  # 모든 테스트 완료 후 브라우저 종료s

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = "failed_screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)










