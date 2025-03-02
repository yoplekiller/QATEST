import time
import pytest
from selenium.webdriver.common.by import By
from utils.utilites import capture_screenshot




def test_login(driver, username, password, expected):

    #로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, "//a[contains(text(),'로그인')]")
    login_button.click()
    time.sleep(2)

    #아이디 패스워드 입력
    login_username_input = driver.find_element(By.NAME, "id")
    login_password_input = driver.find_element(By.NAME, "password")
    login_submit_button = driver.find_element(By.XPATH,"//button[@type='submit']")
    time.sleep(2)

    login_username_input.clear()
    login_password_input.clear()

    login_username_input.send_keys(username)
    login_password_input.send_keys(password)
    login_submit_button.click()
    capture_screenshot(driver,"로그인","screenshots_login")
    time.sleep(3)






















