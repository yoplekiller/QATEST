import os
from datetime import datetime
import allure


def capture_screenshot(driver, test_name, base_path="screenshots"):
    """스크린샷 저장 + Allure 첨부"""
    folder = os.path.join(base_path, test_name.replace(" ", "_"))
    os.makedirs(folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(folder, f"screenshot_{timestamp}.png")
    
    driver.save_screenshot(file_path)
    
    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=test_name,
            attachment_type=allure.attachment_type.PNG
        )
    except Exception:
        pass  # Allure 없어도 테스트는 계속
    
    return file_path


class FailureScreenshot:
    """실패 시에만 자동 스크린샷1"""
    def __init__(self, driver, test_name, base_path="screenshots"):
        self.driver = driver
        self.test_name = test_name
        self.base_path = base_path
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            capture_screenshot(self.driver, f"{self.test_name}_실패", self.base_path)
        return False

