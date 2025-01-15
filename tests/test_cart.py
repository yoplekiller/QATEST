import time
from selenium.webdriver.common.by import By
from project.browser_action import search_product
from project.utilities import take_screenshot


#담기 후 취소
def test_cart_cancel(initialize_browser):
    driver = initialize_browser
    search_product(driver, "콜라")
    # 담기 버튼
    driver.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[4]/div[1]/main[1]/div[2]/div[2]/div[2]/a[1]/div[2]/button[1]").click()
    time.sleep(2)
    #취소 버튼
    driver.find_element(By.CSS_SELECTOR,".css-1w3nh5f.e4nu7ef3").click()
    time.sleep(2)

# 담기 > 장바구니 담기 > 카트 click
def test_cart(initialize_browser):
    driver = initialize_browser
    search_product(driver,"콜라")
    #담기 버튼
    driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[4]/div[1]/main[1]/div[2]/div[2]/div[2]/a[1]/div[2]/button[1]").click()
    time.sleep(2)
    #장바구니 담기 버튼
    driver.find_element(By.XPATH,"//button[@class='css-ahkst0 e4nu7ef3']").click()
    time.sleep(2)
    #우측 카트 UI
    driver.find_element(By.CSS_SELECTOR,".css-g25h97.e14oy6dx1").click()
    time.sleep(2)
    take_screenshot(driver,"test_cart")

