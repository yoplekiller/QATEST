import time
import pytest
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from project.browser_action import search_product
from project.config import BASE_URL
from project.utilities import take_screenshot


@pytest.fixture
def driver():
    """WebDriver 초기화 및 종료"""
    service_obj = Service(r"C:\Users\jmlim\Desktop\chromedriver-win32\chromedriver.exe")
    driver = webdriver.Chrome(service=service_obj)  # Chrome WebDriver 초기화
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(BASE_URL)
    yield driver
    driver.quit()

#담기 후 취소
def test_cart_cancel(driver):
    search_product(driver, "콜라")
    driver.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[4]/div[1]/main[1]/div[2]/div[2]/div[2]/a[1]/div[2]/button[1]").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,".css-1w3nh5f.e4nu7ef3").click()
    time.sleep(2)

# 담기 > 장바구니 담기 > 카트 click
def test_cart(driver):
    search_product(driver,"콜라")
    driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[4]/div[1]/main[1]/div[2]/div[2]/div[2]/a[1]/div[2]/button[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[@class='css-ahkst0 e4nu7ef3']").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,".css-g25h97.e14oy6dx1").click()
    time.sleep(2)
    take_screenshot(driver,"test_cart")

