from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def test_ui_quantity(driver):
    driver.get("https://www.kurly.com/main")
    driver.maximize_window()

    search_box = driver.find_element(By.XPATH, "//input[@placeholder='검색어를 입력해주세요']")
    search_box.send_keys("과자")
    search_box.send_keys(Keys.RETURN)

    driver.implicitly_wait(3)
    first_product = driver.find_element(By.XPATH, "//a[3]//div[2]//button[1]")
    first_product.click()

    up_button = driver.find_element(By.XPATH,"//button[@aria-label='수량올리기']")
    up_button.click()
    up_button.click()

    down_button = driver.find_element(By.XPATH, "//button[@aria-label='수량내리기']")
    down_button.click()

    quantity_input = driver.find_element(By.XPATH, "//button[@aria-label='수량올리기']")
    assert quantity_input.get_attribute("value") == "2", "수량 조정 실패"





