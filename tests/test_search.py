import os
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
    chrome_driver_path = "/usr/local/bin/chromedriver" if os.getenv("CI") else r"C:\Users\jmlim\Desktop\chromedriver-win32\chromedriver.exe"
    service_obj = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service_obj)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(BASE_URL)
    yield driver
    driver.quit()

def test_search(driver):
    search_product(driver,"콜라")
    time.sleep(5)
    take_screenshot(driver,"test_search")

