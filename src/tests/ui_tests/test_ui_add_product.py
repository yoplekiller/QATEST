import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot


def test_add_product(driver):

    search_box = driver.find_element(By.XPATH, "//input[@id='gnb_search']")
    search_box.send_keys("과자")
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
