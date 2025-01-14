import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from project.browser_action import search_product
from project.config import BASE_URL
from project.utilities import take_screenshot


@pytest.fixture
def driver():
    """WebDriver 초기화 및 종료"""
    service_obj = Service(r"C:\Users\jmlim\Desktop\chromedriver-win32\chromedriver.exe")
    driver = webdriver.Chrome(service=service_obj)  # Chrome WebDriver 초기화
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(BASE_URL)
    yield driver
    driver.quit()


def test_search(driver):
    search_product(driver,"콜라")
    time.sleep(5)
    take_screenshot(driver,"test_search")

