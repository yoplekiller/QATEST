import time
from project.browser_action import search_product, click_category_sort_option
from project.utilities import take_screenshot

#카테고리 버튼 기능 테스트
def test_category_filter(initialize_browser):
    driver= initialize_browser
    search_product(driver,"콜라")
    time.sleep(2)
    click_category_sort_option(driver,'탄산·스포츠음료')
    take_screenshot(driver,'탄산·스포츠음료')




