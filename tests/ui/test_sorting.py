import time
from project.browser_action import search_product, click_sort_option
from project.utilities import take_screenshot


#분류 기능 테스트
def test_sorting_new(initialize_browser):
    driver = initialize_browser
    search_product(driver, "콜라")
    time.sleep(5)
    click_sort_option(driver,'신상품순')
    time.sleep(5)
    take_screenshot(driver,"test_sorting_new")

def test_sorting_sale(initialize_browser):
    driver = initialize_browser
    search_product(driver, "콜라")
    time.sleep(5)
    click_sort_option(driver, '판매량순')
    time.sleep(5)
    take_screenshot(driver, "test_sorting_sale")

def test_sorting_bonus(initialize_browser):
    driver = initialize_browser
    search_product(driver, "콜라")
    time.sleep(5)
    click_sort_option(driver, '혜택순')
    time.sleep(5)
    take_screenshot(driver, "test_sorting_bonus")

def test_sorting_cheap(initialize_browser):
    driver = initialize_browser
    search_product(driver, "콜라")
    time.sleep(5)
    click_sort_option(driver, '낮은 가격순')
    time.sleep(5)
    take_screenshot(driver, "test_sorting_cheap")

def test_sorting_expensive(initialize_browser):
    driver = initialize_browser
    search_product(driver, "콜라")
    time.sleep(5)
    click_sort_option(driver, '높은 가격순')
    time.sleep(5)
    take_screenshot(driver, "test_sorting_expensive")




