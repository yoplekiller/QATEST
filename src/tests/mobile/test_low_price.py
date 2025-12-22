import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time


@pytest.fixture
def driver():
    caps = {
        "platformName": "Android",
        "deviceName": "R3CX70ALSLB",
        "appPackage": "com.dbs.kurly.m2",
        "appActivity": ".a_new_presentation.start.AppStarterActivity",
        "automationName": "UiAutomator2",
    }
    options = UiAutomator2Options().load_capabilities(caps)
    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()

@pytest.fixture
def lowest_price_navigation(driver):
    # 최저가도전 버튼 찾기
    for _ in range(5):
        try:
            element = driver.find_element(By.XPATH, "//*[@text='최저가도전']")
            element.click()
            break
        except NoSuchElementException:
            driver.swipe(start_x=500, start_y=1500, end_x=500, end_y=500, duration=500)
            time.sleep(1)

    driver.get_screenshot_as_file("after_lowest_price.png")
    time.sleep(2)