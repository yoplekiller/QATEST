import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utilities import FailureScreenshot


@allure.feature("UI 테스트")
@allure.story("수량 버튼 동작 테스트")
@allure.title("수량 증가/감소 버튼 동작 확인")
def test_ui_quantity(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    with FailureScreenshot(driver, "수량버튼", "screenshots_ui_quantity"):


        search_box = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='검색어를 입력해주세요']"))
        )
        search_box.clear()
        search_box.send_keys("과자")
        search_box.send_keys(Keys.RETURN)

        first_product = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[3]//div[2]//button[1]"))
        )
        first_product.click()


        up_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='수량올리기']"))
        )
        up_button.click()
        up_button.click()

 
        down_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='수량내리기']"))
        )
        down_button.click()

  
        quantity_input = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'count')]")
            )
        )

        quantity_value = quantity_input.text.strip()

        assert quantity_value == "2", f"❌ 수량 조절 실패 (현재 수량: {quantity_value})"

        print(f"✅ 수량 버튼 동작 정상 작동, 현재 수량: {quantity_value}")
