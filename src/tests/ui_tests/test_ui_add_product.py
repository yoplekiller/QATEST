import time
import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import capture_screenshot
from config.constants import URLs, Timeouts, Selectors, PopupSelectors,ErrorMessages, Buttons

@allure.feature("UI 테스트")
@allure.story("상품 추가 테스트")
@allure.title("상품 검색 후 장바구니 추가 기능 동작 확인")
def test_add_product(driver):
    driver.get(URLs.KURLY_MAIN)
    driver.maximize_window()

    try:
      search_box = WebDriverWait(driver, Timeouts.MEDIUM).until(EC.element_to_be_clickable(Selectors.SEARCH_BOX))
      search_box.send_keys("과자")
      search_box.send_keys(Keys.RETURN)
      time.sleep(3)

      try:
          add_button = WebDriverWait(driver, Timeouts.MEDIUM).until(EC.element_to_be_clickable(Buttons.ADD_TO_CART))
          add_button.click()
          driver.implicitly_wait(Timeouts.MEDIUM)

      except Exception as e:
          capture_screenshot(driver,"상품추가 실패","screenshot_add_product")
          pytest.fail(f"❌ 상품 추가 버튼 클릭 실패: {str(e)}")

      try:
          quantity_up_button = driver.find_element(*Buttons.INCREASE_QUANTITY)
          for _ in range(3):
              quantity_up_button.click()
              time.sleep(1)  # 클릭 간 약간의 대기 시간 추가

      except Exception as e:
          capture_screenshot(driver,"수량올리기 실패","screenshot_add_product")
          pytest.fail(f"❌ 수량 올리기 실패: {str(e)}")

      try:
          quantity_down_button = driver.find_element(*Buttons.DECREASE_QUANTITY)
          for _ in range(2):
              quantity_down_button.click()
              time.sleep(1)  # 클릭 간 약간의 대기 시간 추가

      except Exception as e:
          capture_screenshot(driver,"수량내리기 실패","screenshot_add_product")
          pytest.fail(f"❌ 수량 내리기 실패: {str(e)}")

      try:
          cart_add_button = driver.find_element(*Buttons.ADD_TO_CART_2)
          cart_add_button.click()
          time.sleep(1)  # 클릭 간 약간의 대기 시간 추가

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