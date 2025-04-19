import os.path
from datetime import datetime

#테스트 결과 캡쳐
def capture_screenshot(driver, test_case_name, base_path = "screenshots", headless_mode=False):
    if headless_mode:
        return

    test_folder = os.path.join(base_path, test_case_name.replace(" ","_"))
    os.makedirs(test_folder, exist_ok=True)

    #시간 가져오기
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    #파일명 생성
    file_name = f"screenshots_{timestamp}.png"

    #전체 경로
    screenshots_file_path = os.path.join(test_folder, file_name)

    #스크린샷 저장
    driver.save_screenshot(screenshots_file_path)
    print(f"Screenshot saved at: {screenshots_file_path}")

    return screenshots_file_path

