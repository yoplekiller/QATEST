import allure
import pytest
from selenium.webdriver import Keys
import time
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot

@allure.feature("UI 테스트")
@allure.story("카테고리 기능 테스트")
def test_category(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    try:
      #검색
      search_box = driver.find_element(By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
      search_box.send_keys("제로콜라")
      search_box.send_keys(Keys.RETURN)
      time.sleep(2)


      def click_category(category_name, screenshot_name):
          try:
              category_button = driver.find_element(By.XPATH,f"//a[contains(text(),'{category_name}')]")
              category_button.click()
              time.sleep(2)
              capture_screenshot(driver, screenshot_name, "screenshots_category")
          except Exception as e:
              capture_screenshot(driver,f"{screenshot_name}_실패","screenshots_category")
              allure.attach(driver.get_screenshot_as_png(), name=f"{screenshot_name}_실패",
                            attachment_type=allure.attachment_type.PNG)
              pytest.fail(f"❌ '{category_name}' 클릭 실패: {str(e)}")

      categories =[
          ("추천순", "추천순"),
          ("낮은 가격순", "낮은가격순"),
          ("높은 가격순", "높은가격순"),
          ("판매량순", "판매량순"),
          ("혜택순", "혜택순"),
          ("신상품순", "신상품순"),
      ]
      for category_name, screenshot_name in categories:
          click_category(category_name, screenshot_name)

    except Exception as e:
        capture_screenshot(driver,"카테고리_테스트실패","screenshots_category")
        allure.attach(driver.get_screenshot_as_png(), name="카테고리_테스트실패",
                      attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"❌ 카테고리 테스트 실패: {str(e)}")
















    #카테고리별 버튼
    category_button = driver.find_element(By.XPATH,"//a[contains(text(),'추천순')]")
    category_button.click()
    time.sleep(2)
    capture_screenshot(driver,"추천순","screenshots_category")


    category_button = driver.find_element(By.XPATH, "//a[contains(text(),'낮은 가격순')]")
    category_button.click()
    time.sleep(2)
    capture_screenshot(driver, "낮은가격순", "screenshots_category")


    category_button = driver.find_element(By.XPATH, "//a[contains(text(),'높은 가격순')]")
    category_button.click()
    time.sleep(2)
    capture_screenshot(driver, "높은가격순", "screenshots_category")


    category_button = driver.find_element(By.XPATH, "//a[contains(text(),'판매량순')]")
    category_button.click()
    time.sleep(2)
    capture_screenshot(driver, "판매량순", "screenshots_category")


    category_button = driver.find_element(By.XPATH, "//a[contains(text(),'혜택순')]")
    category_button.click()
    time.sleep(2)
    capture_screenshot(driver, "혜택순", "screenshots_category")


    category_button = driver.find_element(By.XPATH, "//a[contains(text(),'신상품순')]")
    category_button.click()
    time.sleep(2)
    capture_screenshot(driver, "신상품순", "screenshots_category")





