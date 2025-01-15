import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

@pytest.fixture
def initialize_browser():
    """WebDriver 초기화 및 종료"""
    if os.getenv("CI"):
        # CI 환경에서는 Selenium Grid 사용
        grid_url = "http://localhost:4444/wd/hub"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        capabilities = DesiredCapabilities.CHROME.copy()
        driver = webdriver.Remote(command_executor=grid_url, options=options, desired_capabilities=capabilities)
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