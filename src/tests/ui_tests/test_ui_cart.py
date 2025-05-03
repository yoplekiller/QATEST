import time
import allure
import pytest
from selenium.webdriver.common.by import By
<<<<<<< HEAD
from utils.utilities import capture_screenshot
=======



from utils.utilites import capture_screenshot
>>>>>>> main

@allure.feature("UI 테스트")
@allure.story("장바구니 화면 체크 테스트")
@allure.title("장바구니 버튼이 동작 하는지 확인")
def test_cart(driver):

    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    try:
      driver.get("https://www.kurly.com/main")
      cart_button = driver.find_element(By.XPATH,"//button[@class='css-g25h97 e14oy6dx1']")
      cart_button.click()
      time.sleep(4)

      assert "컬리 - 마켓컬리/뷰티컬리" in driver.title, "❌ 장바구니 페이지가 열리지 않았습니다!"
      capture_screenshot(driver,"장바구니","screenshots_cart")

    except Exception as e:
        capture_screenshot(driver,"장바구니_실패","screenshots_cart")
        allure.attach(driver.get_screenshot_as_png(), name="장바구니_실패", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"❌ 테스트 실패: {str(e)}")





