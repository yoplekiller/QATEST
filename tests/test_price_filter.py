import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from project.browser_action import search_product, click_sort_option, click_price_sort_option
from project.config import BASE_URL
from project.utilities import take_screenshot


def test_price_filter(initialize_browser):
    driver = initialize_browser
    search_product(driver, "콜라")
    time.sleep(5)

    target = driver.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[4]/div[1]/main[1]/div[2]/div[1]/div[2]/div[4]/nav[1]/li[2]/a[1]/div[1]/button[1]")
    driver.execute_script("arguments[0].scrollIntoView(true);", target)
    time.sleep(3)

    click_price_sort_option(driver,'12,280원 미만')
    time.sleep(3)
    take_screenshot(driver,'12,280원 미만')

    click_price_sort_option(driver,'12,280원 ~ 19,995원')
    time.sleep(2)
    take_screenshot(driver, '12,280원 ~ 19,995원')

    click_price_sort_option(driver,'19,995원 ~ 32,756원')
    time.sleep(2)
    take_screenshot(driver, '19,995원 ~ 32,756원')

    click_price_sort_option(driver,'32,756원 이상')
    time.sleep(2)
    take_screenshot(driver, '32,756원 이상')



