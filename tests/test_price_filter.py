import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from project.browser_action import search_product, click_sort_option, click_price_sort_option
from project.config import BASE_URL
from project.utilities import take_screenshot


@pytest.fixture
def driver():
    """WebDriver 초기화 및 종료"""
    service_obj = Service(r"C:\Users\jmlim\Desktop\chromedriver-win32\chromedriver.exe")
    driver = webdriver.Chrome(service=service_obj)  # Chrome WebDriver 초기화
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_price_filter(driver):
    driver.get(BASE_URL)
    search_product(driver, "콜라")
    time.sleep(5)

    target = driver.find_element(By.XPATH, "//div[3]//nav[1]//li[3]//a[1]//div[1]")
    driver.execute_script("arguments[0].scrollIntoView(true);", target)
    time.sleep(3)

    click_price_sort_option(driver,'12,270원 미만')
    time.sleep(3)
    take_screenshot(driver,'12,270원 미만')

    click_price_sort_option(driver,'12,270원 ~ 19,990원')
    time.sleep(2)
    take_screenshot(driver, '12,270원 ~ 19,990원')

    click_price_sort_option(driver,'19,990원 ~ 32,756원')
    time.sleep(2)
    take_screenshot(driver, '19,990원 ~ 32,756원')

    click_price_sort_option(driver,'32,756원 이상')
    time.sleep(2)
    take_screenshot(driver, '32,756원 이상')



