import time
import pytest
from selenium.webdriver.common.by import By

from utils.utilites import capture_screenshot


@pytest.mark.parametrize("tc_id,username, password, expected", [
    ("TC_001", "dla05711", "", "disabled"),
    ("TC_002", "", "@h$5N(!$aA9-fTd", "disabled"),
    ("TC_003", "", "", "disabled"),
    ("TC_004", "dla05711", "@h$5N(1111111","error"),
    ("TC_005", "dla057111233", "@h$5N(!$aA9-fTd","error")
    # ("TC_006", "dla05711", "@h$5N(!$aA9-fTd","success")
])
def test_login(driver, tc_id, username, password, expected):

    #로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, "//a[contains(text(),'로그인')]")
    login_button.click()
    time.sleep(2)

    #아이디 패스워드 입력
    login_username_input = driver.find_element(By.NAME, "id")
    login_password_input = driver.find_element(By.ID, "pw")
    login_submit_button = driver.find_element(By.ID,"log.login")
    time.sleep(2)

    login_username_input.clear()
    login_password_input.clear()

    login_username_input.send_keys(username)
    login_password_input.send_keys(password)
    login_submit_button.click()
    capture_screenshot(driver,"로그인","screenshots_login")
    time.sleep(3)






    # if expected == "disabled":
    #     assert not login_submit_button.is_enabled(),f"❌ {tc_id} 실패: 버튼이 활성화됨(비활성화 예상)"
    # elif expected == "error":
    #     assert driver.find_element(By.XPATH,"//div[contains(text(),'다시 로그인해 주세요.')]") ,f"❌ {tc_id} 실패: 오류메시지 미노출"
    # elif expected == "success":
    #     assert "네이버+ 스토어" in driver.title ,f"❌ {tc_id} 실패: 로그인 실패"
    #
    # print(f"✅ {tc_id} 테스트 통과!")
    time.sleep(2)



















