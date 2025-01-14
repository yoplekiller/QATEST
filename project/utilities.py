import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# 스크린샷
def take_screenshot(driver, test_name, save_dir="screenshots"):
    """ WebDriver로 현재 페이지의 스크린샷을 저장합니다.

    Args:
        driver: WebDriver 인스턴스
        test_name: 테스트 이름 (스크린샷 파일 이름에 포함)
        save_dir: 스크린샷 저장 경로 (기본값: 'screenshots')"""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(save_dir, f"{test_name}_{timestamp}.png")

    #스크린샷 저장
    driver.save_screenshot(file_path)
    print(f"Screenshot saved at: {file_path}")




