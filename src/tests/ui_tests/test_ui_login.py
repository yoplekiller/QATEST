import time
import allure
import pytest
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot

@allure.feature("UI 테스트")
@allure.story("로그인 테스트")
def test_login(driver):
    try:
        driver.get("https://www.kurly.com/main")
        time.sleep(2)
        login_button = driver.find_element(By.XPATH, "//a[contains(text(),'로그인')]")
        login_button.click()
        time.sleep(2)

        #아이디 패스워드 입력
        login_username_input = driver.find_element(By.NAME, "id")
        login_password_input = driver.find_element(By.ID, "pw")
        login_submit_button = driver.find_element(By.ID,"log.login")
        time.sleep(2)

        login_username_input.clear()
        login_password_input.clear()

        login_username_input.send_keys('boksoon8')
        login_password_input.send_keys('1232133123')
        login_submit_button.click()
        time.sleep(3)
    except Exception as e:
        capture_screenshot(driver, "로그인", "screenshots_login")
        pytest.fail(f"❌ 로그인 실패 :{str(e)}")




















