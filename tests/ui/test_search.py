import time
from project.browser_action import search_product
from project.utilities import take_screenshot

# 검색 기능 테스트
def test_search(initialize_browser):
    driver = initialize_browser
    search_product(driver,"콜라")
    time.sleep(2)
    take_screenshot(driver,"test_search")


