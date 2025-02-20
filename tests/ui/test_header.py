import time
from project.browser_action import click_category_sort_option
from project.utilities import take_screenshot
from tests.ui.conftest import initialize_browser



def test_header_new(initialize_browser):
    driver = initialize_browser
    click_category_sort_option(driver,'신상품')
    time.sleep(2)
    take_screenshot(driver,"test_header_new")

def test_header_best(initialize_browser):
    driver = initialize_browser
    click_category_sort_option(driver, '베스트')
    time.sleep(2)
    take_screenshot(driver, "test_header_best")

def test_header_saving_shopping(initialize_browser):
    driver = initialize_browser
    click_category_sort_option(driver, '알뜰쇼핑')
    time.sleep(2)
    take_screenshot(driver, "test_header_saving_shopping")

def test_header_special(initialize_browser):
    driver = initialize_browser
    click_category_sort_option(driver, '특가/혜택')
    time.sleep(2)
    take_screenshot(driver, "test_header_special")




