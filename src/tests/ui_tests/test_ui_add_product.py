import time
import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot

@allure.feature("UI 테스트")
@allure.story("상품 추가 테스트")
def test_add_product(driver):
    """
       상품을 검색 후 추가하는 테스트
       - 수량올리기, 수량내리기 기능 구현
       - 검색 후 상품 선택 후 카트에 추가 구현
       """

    search_box = driver.find_element(By.XPATH, "//input[@id='gnb_search']")
    search_box.send_keys("과1자")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    add_button = driver.find_element(By.XPATH, "//a[3]//div[2]//button[1]")
    add_button.click()

    quantity_up_button = driver.find_element(By.XPATH, "//button[@aria-label='수량올리기']")
    for _ in range(2):
      quantity_up_button.click()
    time.sleep(2)


    quantity_down_button = driver.find_element(By.XPATH, "//button[@aria-label='수량내리기']")
    for _ in range(2):
        quantity_down_button.click()
    time.sleep(2)

    cart_add_button = driver.find_element(By.XPATH, "//button[@class='css-ahkst0 e4nu7ef3']")
    cart_add_button.click()
    time.sleep(2)

    capture_screenshot(driver,"상품 추가","screenshots_add_product")

    if "과자" not in driver.page_source:
        screenshot_path = "unexpected_result.png"

        # 스크린샷 저장
        driver.save_screenshot(screenshot_path)

        # Allure Report에 스크린샷 첨부
        with open(screenshot_path, "rb") as image_file:
            allure.attach(image_file.read(), name="Unexpected Search Result",
                          attachment_type=allure.attachment_type.PNG)

        pytest.fail("검색 결과가 기대와 다릅니다.")