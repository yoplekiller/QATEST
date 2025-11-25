import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import FailureScreenshot


@allure.feature("UI 테스트")
@allure.story("로그인 > 상품 추가 > 추가 확인 테스트")
@allure.title("로그인 후 상품 추가하고 상품이 장바구니에 담겨 있는지 확인")
def test_ui_product_add_flow(driver):

    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    with FailureScreenshot(driver, "상품추가흐름", "screenshots_product_add_flow"):
        try:
            # 로그인 버튼 클릭
            login_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'로그인')]"))
            )
            login_button.click()

            # ID / PW 입력
            login_username_input = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='아이디를 입력해주세요']"))
            )
            login_password_input = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='비밀번호를 입력해주세요']"))
            )
            login_submit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )

            login_username_input.clear()
            login_password_input.clear()

            login_username_input.send_keys('dlaaslek')
            login_password_input.send_keys('!test132456')

            login_submit_button.click()

        except Exception as e:
            pytest.fail(f"로그인 실패: {e}")

    # 상품 검색
    try:
        search_box = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='검색어를 입력해주세요']"))
        )
        search_box.send_keys("과자")
        search_box.send_keys(Keys.RETURN)

    except Exception as e:
        pytest.fail(f"상품 검색 실패: {e}")

    # 장바구니 추가
    try:
        add_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[3]//div[2]//button[1]"))
        )
        add_button.click()

        quantity_up_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='수량올리기']"))
        )
        quantity_up_button.click()

        cart_add_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='css-ahkst0 e4nu7ef3']"))
        )
        cart_add_button.click()

        cart_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='css-g25h97 e14oy6dx1']"))
        )
        cart_button.click()

    except Exception as e:
        pytest.fail(f"장바구니 추가 실패: {e}")
