import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def initialize_browser():
    """WebDriver 초기화 및 종료"""
    if os.getenv("CI"):
        # CI 환경에서는 Selenium Grid 사용
        grid_url = "http://localhost:4444/wd/hub"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") #화면 없이 실행
        options.add_argument("--no-sandbox") # 샌드박스 문제 방지
        options.add_argument("--disable-dev-shm-usage")# 메모리 문제 해결

        driver = webdriver.Remote(command_executor=grid_url, options=options)
    else:
        # 로컬 환경에서는 로컬 ChromeDriver 사용
        chrome_driver_path = r"C:\Users\jmlim\Desktop\chromedriver-win32\chromedriver.exe"
        service_obj = Service(chrome_driver_path)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service_obj, options=options)

    driver.maximize_window()
    driver.implicitly_wait(10)
    base_url = os.getenv("BASE_URL", "https://www.kurly.com/")
    driver.get(base_url)
    yield driver
    driver.quit()