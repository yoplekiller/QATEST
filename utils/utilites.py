import os.path
from datetime import datetime

#테스트 결과 캡쳐
def capture_screenshot(driver, test_case_name, path, headless_mode=False):
    if headless_mode:
        return

    os.makedirs(path, exist_ok=True)

    #시간 가져오기
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    #파일명 생성
    safe_test_name = test_case_name.replace(" ","_")
    file_name = f"{safe_test_name}_{timestamp}.png"

    #전체 경로
    screenshots_file_path = os.path.join(path, file_name)

    #스크린샷 저장
    driver.save_screenshot(screenshots_file_path)
    print(f"Screenshot saved at: {screenshots_file_path}")

