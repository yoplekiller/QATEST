from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

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

def new_product(driver):
    for _ in range(5):
        try:
            element = driver.find_element(By.XPATH, "//*[@text='신상품']")
            element.click()
            return
        except NoSuchElementException:
            driver.swipe(start_x=500, start_y=1500, end_x=500, end_y=500, duration=500)
            time.sleep(1)
    raise Exception("신상품 메뉴를 찾을 수 없습니다.")

@allure.title("신상품 메뉴 진입 테스트")
@allure.feature("신상품 메뉴")
def test_new_product(driver):
    try:
        time.sleep(2)
        new_product(driver)
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name="New Product Screen", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="error_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        pytest.fail(f"Test failed due to exception: {e}")
        