from selenium.webdriver import Keys
import time
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot


def test_category(driver):

    #검색
    search_box = driver.find_element(By.XPATH, "//input[@id='gnb_search']")
    search_box.send_keys("제로콜라")
    search_box.send_keys(Keys.RETURN)

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





