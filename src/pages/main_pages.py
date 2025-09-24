from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.constants import URLs, Timeouts, Selectors

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def search_product(self, keyword):
        search_box = self.wait.until(EC.presence_of_element_located(Selectors.SEARCH_BOX))
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)