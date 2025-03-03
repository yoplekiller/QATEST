import time
import allure
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot

@allure.feature("UI 테스트")
@allure.story("장바구니 화면 체크 테스트")
def test_cart(driver):
    cart_button = driver.find_element(By.XPATH,"//button[@class='css-g25h97 e14oy6dx1']")
    cart_button.click()
    time.sleep(2)
    capture_screenshot(driver,"장바구니","screenshots_cart")




