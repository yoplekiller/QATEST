import allure
import time
import pytest
from utils.utilities import capture_screenshot
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

@allure.feature("UI 테스트")
@allure.story("수량 조절")
@allure.title("수량 올리기/내리기 기능 동작 확인")
def test_quantity_up_down(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()
    try:
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
        search_box.send_keys("과자")
        search_box.send_keys(Keys.RETURN)
        driver.implicitly_wait(3)

        add_button = driver.find_element(By.XPATH, "//a[3]//div[2]//button[1]")
        add_button.click()
        time.sleep(2)

        up_btn = driver.find_element(By.XPATH, "//button[@aria-label='수량올리기']")
        down_btn = driver.find_element(By.XPATH, "//button[@aria-label='수량내리기']")

        up_btn.click()
        time.sleep(2)

        down_btn.click()
        time.sleep(2)

        if

    except Exception as e:
        capture_screenshot(driver, "수량 조절 실패", "screenshot_qty")
        pytest.fail(f"❌ 수량 조절 실패: {str(e)}")



