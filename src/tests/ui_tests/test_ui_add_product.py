import time
import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils.utilities import capture_screenshot

@allure.feature("UI 테스트")
@allure.story("상품 추가 테스트")
@allure.title("상품 상세 화면의 UI 기능들이 동작 하는지 확인")
def test_add_product(driver):
    """
       상품을 검색 후 추가하는 테스트
       - 수량올리기, 수량내리기 기능 구현
       - 검색 후 상품 선택 후 카트에 추가 구현
       """
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    try:
      driver.get("https://www.kurly.com/main")

      search_box = driver.find_element(By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
      search_box.send_keys("과자")
      search_box.send_keys(Keys.RETURN)
      time.sleep(4)

      try:
          add_button = driver.find_element(By.XPATH, "//a[3]//div[2]//button[1]")
          add_button.click()
          time.sleep(4)

      except Exception as e:
          capture_screenshot(driver,"상품추가 g실패","screenshot_add_product")
          pytest.fail(f"❌ 상품 추가 버튼 클릭 실패: {str(e)}")

      try:
          quantity_up_button = driver.find_element(By.XPATH, "//button[@aria-label='수량올리기']")
          for _ in range(2):
              quantity_up_button.click()
          time.sleep(4)
      except Exception as e:
          capture_screenshot(driver,"수량올리기 실패","screenshot_add_product")
          pytest.fail(f"❌ 수량 올리기 실패: {str(e)}")

      try:
          quantity_down_button = driver.find_element(By.XPATH, "//button[@aria-label='수량내리기']")
          for _ in range(2):
              quantity_down_button.click()
          time.sleep(4)
      except Exception as e:
          capture_screenshot(driver,"수량내리기 실패","screenshot_add_product")
          pytest.fail(f"❌ 수량 내리기 실패: {str(e)}")

      try:
          cart_add_button = driver.find_element(By.XPATH, "//button[@class='css-ahkst0 e4nu7ef3']")
          cart_add_button.click()
          time.sleep(4)
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