import time
import allure
import pytest
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot

@allure.feature("예외 케이스")
@allure.story("잘못된 ID,PW 입력")
@allure.title("잘못된 ID,PW 입력 시 로그인이 실패하는지 확인")
def test_login(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    try:
        # 로그인 버튼 클릭
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




















