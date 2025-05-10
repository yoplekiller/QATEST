import time
import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

@allure.feature("UI 테스트")
@allure.story("수량 버튼 동작 테스트")
@allure.title("수량 증가/감소 버튼 동작 확인")
def test_ui_quantity(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    search_box = driver.find_element(By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
    search_box.send_keys("과자")
    search_box.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)


    first_product = driver.find_element(By.XPATH, "//a[3]//div[2]//button[1]")
    first_product.click()

    up_button = driver.find_element(By.XPATH,"//button[@aria-label='수량올리기']")
    up_button.click()
    up_button.click()

    down_button = driver.find_element(By.XPATH, "//button[@aria-label='수량내리기']")
    down_button.click()
    time.sleep(3)

    quantity_input = driver.find_element(By.XPATH, "//div[@class='count css-6m57y0 e1cqr3m41']")
    assert quantity_input.text.strip() == "2", "수량 조절 실패"





