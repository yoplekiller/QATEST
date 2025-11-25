import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import FailureScreenshot

@allure.feature("예외 케이스")
@allure.story("잘못된 ID,PW 입력")
@allure.title("잘못된 ID,PW 입력 시 로그인이 실패하는지 확인")
def test_login(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    with FailureScreenshot(driver, "로그인", "screenshots_login"):
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'로그인')]")))
            login_button.click()
            time.sleep(2)

            #아이디 패스워드 입력
            login_username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='아이디를 입력해주세요']")))
            login_password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='비밀번호를 입력해주세요']")))
            login_submit_button = driver.find_element(By.XPATH,"//button[@type='submit']")

            login_username_input.clear()
            login_password_input.clear()

            login_username_input.send_keys('boksoon8')
            login_password_input.send_keys('1232133123')
            time.sleep(2)
            login_submit_button.click()
            time.sleep(2)

            success_case = driver.find_element(By.XPATH, "//div[@class='css-hj3ig8 e15sbxqa2']")
            assert success_case.is_displayed(), f"❌ 로그인 실패"

        except Exception as e:
            pytest.fail(f"❌ 로그인 실패 :{str(e)}")




















