import time
from project.browser_action import search_product
from project.utilities import take_screenshot


def test_search(initialize_browser):
    driver = initialize_browser
    search_product(driver,"콜라")
    time.sleep(5)
    take_screenshot(driver,"test_search")

