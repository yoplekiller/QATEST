import time
import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils.utilities import capture_screenshot
from config.constants import URLs, Selectors, Buttons



@allure.feature("UI 테스트")
@allure.story("로그인 > 상품 추가 > 추가 확인 테스트")
@allure.title("로그인 후 상품 추가하고 상품이 장바구니에 담겨 있는지 확인")
def test_ui_product_add_flow(driver):
    driver.get(URLs.KURLY_MAIN)
    driver.maximize_window()

    # 로그인 단계
    try:
        login_button = driver.find_element(*Buttons.LOGIN_BUTTON)
        login_button.click()
        time.sleep(2)

        login_username_input = driver.find_element(*Buttons.LOGIN_USERNAME_INPUT)
        login_password_input = driver.find_element(*Buttons.LOGIN_PASSWORD_INPUT)
        login_submit_button = driver.find_element(*Buttons.LOGIN_BUTTON_SUBMIT)

        login_username_input.clear()
        login_password_input.clear()

        login_username_input.send_keys('dlaaslek')
        login_password_input.send_keys('!test132456')
        time.sleep(2)

        login_submit_button.click()
        time.sleep(2)

    except Exception as e:
        capture_screenshot(driver, "login_error")
        allure.attach.file("screenshots/login_error.png", name="로그인 실패", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"로그인 실패: {e}")

    # 상품 검색 단계
    try:
        search_box = driver.find_element(*Selectors.SEARCH_BOX)
        search_box.send_keys("과자")
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
    except Exception as e:
        capture_screenshot(driver, "search_error")
        allure.attach.file("screenshots/search_error.png", name="검색 실패", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"상품 검색 실패: {e}")

    # 장바구니 추가 단계
    try:
        add_button = driver.find_element(*Buttons.ADD_TO_CART)
        add_button.click()
        time.sleep(2)

        quantity_up_button = driver.find_element(*Buttons.INCREASE_QUANTITY)
        quantity_up_button.click()
        time.sleep(3)

        cart_add_button = driver.find_element(*Buttons.ADD_TO_CART_2)
        cart_add_button.click()
        time.sleep(2)

        cart_button = driver.find_element(*Buttons.CART_BUTTON)
        cart_button.click()
        time.sleep(2)

    except Exception as e:
        capture_screenshot(driver, "cart_error")
        allure.attach.file("screenshots/cart_error.png", name="장바구니 추가 실패", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"장바구니 추가 실패: {e}")





