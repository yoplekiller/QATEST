from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import pytest
import allure
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
def best_product(driver):
    element = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().text("베스트"));'
    )
    element.click()


@allure.title("베스트 메뉴 진입 테스트")
@allure.feature("베스트 메뉴")
def test_best_product(driver, best_product):
    # 성공 시 스크린 샷
    try:
        time.sleep(2)
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name="Best Product Screen", attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        # 실패 시 에러 스크린샷 저장
        allure.attach(
            driver.get_screenshot_as_png(),
            name="error_screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        pytest.fail(f"Test failed due to exception: {e}")
        
