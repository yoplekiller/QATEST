import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

@pytest.fixture
def driver():
    caps = {
        "platformName": "Android",
        "deviceName": "R3CX70ALSLB",
        "appPackage": "com.dbs.kurly.m2",
        "appActivity": ".a_new_presentation.start.AppStarterActivity",
        "automationName": "UiAutomator2",
        "noReset": True
    }
    options = UiAutomator2Options().load_capabilities(caps)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    # 팝업 처리
    _handle_popups(driver)
    yield driver
    driver.quit()

def _handle_popups(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(("id", "com.android.permissioncontroller:id/permission_allow_button"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        pass

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(("id", "com.dbs.kurly.m2:id/okButton"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        pass

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(("id", "android:id/button1"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        pass
