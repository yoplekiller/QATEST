import os.path
import datetime
import re
import allure


#테스트 결과 캡쳐
def capture_screenshot(driver, test_case_name, base_path ="screenshots", headless_mode=False, attach_to_allure=False):
    if headless_mode:
        return

    data_str = datetime.datetime.now().strftime("%Y-%m-%d")
    base_path = os.path.join(base_path, data_str)

    #테스트 케이스 이름 정리
    safe_test_name = re.sub(r"[^\w\-_.]", "_", test_case_name)

    #최종 폴더
    test_folder = os.path.join(base_path, safe_test_name)
    os.makedirs(test_folder, exist_ok=True)

    #파일명 생성
    file_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    file_path = os.path.join(test_folder, file_name)

    #스크린샷 저장
    driver.save_screenshot(file_path)
    print(f"📸 스크린샷 저장 완료: {file_path}")

    if attach_to_allure:
        allure.attach.file(
            file_path,
            name="Failure sreenshot",
            attachment_type=allure.attachment_type.PNG
        )




