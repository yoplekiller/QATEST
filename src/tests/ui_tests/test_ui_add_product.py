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
    try:
      search_box = driver.find_element(By.XPATH, "//input[@id='gnb_search']")
      search_box.send_keys("과자")
      search_box.send_keys(Keys.RETURN)
      time.sleep(3)

      try:
          add_button = driver.find_element(By.XPATH, "//a[3]//div[2]//button[1]")
          add_button.click()
      except Exception as e:
          capture_screenshot(driver,"상품추가 실패","screenshot_add_product")
          pytest.fail(f"❌ 상품 추가 버튼 클릭 실패: {str(e)}")

      try:
          quantity_up_button = driver.find_element(By.XPATH, "//button[@aria-label='수량올리기']")
          for _ in range(2):
              quantity_up_button.click()
          time.sleep(2)
      except Exception as e:
          capture_screenshot(driver,"수량올리기 실패","screenshot_add_product")
          pytest.fail(f"❌ 수량 올리기 실패: {str(e)}")

      try:
          quantity_down_button = driver.find_element(By.XPATH, "//button[@aria-label='수량내리기']")
          for _ in range(2):
              quantity_down_button.click()
          time.sleep(2)
      except Exception as e:
          capture_screenshot(driver,"수량내리기 실패","screenshot_add_product")
          pytest.fail(f"❌ 수량 내리기 실패: {str(e)}")

      try:
          cart_add_button = driver.find_element(By.XPATH, "//button[@class='css-ahkst0 e4nu7ef3']")
          cart_add_button.click()
          time.sleep(2)
      except Exception as e:
          capture_screenshot(driver, "상품 추가", "screenshots_add_product")
          pytest.fail(f"❌ 상품 추가 실패: {str(e)}")

      # 검색 결과 확인
      if "과자" not in driver.page_source:
          screenshot_path = "unexpected_result.png"

          # 스크린샷 저장
          driver.save_screenshot(screenshot_path)

          # Allure Report에 스크린샷 첨부
          with open(screenshot_path, "rb") as image_file:
              allure.attach(image_file.read(), name="Unexpected Search Result", attachment_type=allure.attachment_type.PNG)
          pytest.fail("❌ 검색 결과에서 '과자'가 포함되지 않음.")

    except Exception as e:
        capture_screenshot(driver,"테스트실패","screenshots_add_product")
        pytest.fail(f"❌ 상품 추가 테스트 실패: {str(e)}")