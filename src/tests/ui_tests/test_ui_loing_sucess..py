import time
import allure
import pytest
from selenium.webdriver.common.by import By
from utils.utilities import capture_screenshot

@allure.feature("UI 기능 테스트")
@allure.story("올바른 ID,PW 입력")
@allure.title("올바른 ID, PW 입력 시 로그인 되는 지 확인")
def test_login(driver, kurly_id=None, kurly_pw=None):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    try:
        login_button = driver.find_element(By.XPATH, "//a[contains(text(),'로그인')]")
        login_button.click()
        time.sleep(2)

        #아이디 패스워드 입력
        login_username_input = driver.find_element(By.XPATH, "//input[@placeholder='아이디를 입력해주세요']")
        login_password_input = driver.find_element(By.XPATH, "//input[@placeholder='비밀번호를 입력해주세요']")
        login_submit_button = driver.find_element(By.XPATH,"//button[@type='submit']")

        login_username_input.clear()
        login_password_input.clear()

        login_username_input.send_keys(kurly_id)
        login_password_input.send_keys(kurly_pw)
        time.sleep(3)
        login_submit_button.click()
        time.sleep(3)

        success_case = driver.find_element(By.XPATH, "//div[@class='swiper-slide swiper-slide-active']//img[@alt='메인배너'")
        assert success_case.is_displayed(), f"❌ 로그인 실패"

    except Exception as e:
        capture_screenshot(driver, "로그인", "screenshots_login_failed")
        pytest.fail(f"❌ 로그인 실패 :{str(e)}")




















