import os.path
from datetime import datetime
import allure


#테스트 결과 캡쳐
def capture_screenshot(driver, test_case_name, base_path = "screenshots", headless_mode=False, attach_to_allure=False):
    if headless_mode:
        return

    test_folder = os.path.join(base_path, test_case_name.replace(" ","_"))
    os.makedirs(test_folder, exist_ok=True)

    #시간 가져오기
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"screenshots_{timestamp}.png"
    screenshots_file_path = os.path.join(test_folder, file_name)


    #스크린샷 저장
    driver.save_screenshot(screenshots_file_path)
    print(f"Screenshot saved at: {screenshots_file_path}")

    # Allure 첨부 선택적으로
    if attach_to_allure:
        allure.attach.file(
          screenshots_file_path,
          name="Failure Screenshot",
          attachment_type=allure.attachment_type.PNG)

    return screenshots_file_path

