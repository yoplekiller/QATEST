import time
import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from config.constants import URLs, Timeouts, Selectors, PopupSelectors,ErrorMessages, Buttons

@allure.feature("UI 테스트")
@allure.story("수량 버튼 동작 테스트")
@allure.title("수량 증가/감소 버튼 동작 확인")
def test_ui_quantity(driver):
    driver.get(URLs.KURLY_SNACK)
    driver.maximize_window()


    first_product = driver.find_element(*Buttons.ADD_TO_CART)
    first_product.click()

    up_button = driver.find_element(*Buttons.INCREASE_QUANTITY)
    up_button.click()
    up_button.click()
    time.sleep(2)
    

    down_button = driver.find_element(*Buttons.DECREASE_QUANTITY)
    down_button.click()
    time.sleep(2)

    quantity_input = driver.find_element(By.XPATH, "//div[@class='count css-6m57y0 e1cqr3m41']")
    assert quantity_input.text.strip() == "2", "수량 조절 실패"





