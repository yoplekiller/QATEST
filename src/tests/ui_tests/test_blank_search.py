import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.utilities import capture_screenshot
from config.constants import URLs, Timeouts, Selectors, PopupSelectors

@allure.feature("UI 테스트")
@allure.story("검색 실패 케이스")
@allure.title("공백 입력 시, 팝업 노출 확인")
def test_search_invalid_product(driver):  
    # 암시적 대기 설정 (전역)
    driver.implicitly_wait(Timeouts.SHORT)
    
    # 페이지 로드
    driver.get(URLs.KURLY_MAIN)
    driver.maximize_window()
    
    # 명시적 대기를 사용한 검색박스 찾기
    wait = WebDriverWait(driver, Timeouts.MEDIUM)
    
    try:
        search_box = wait.until(EC.element_to_be_clickable(Selectors.SEARCH_BOX))
        
        search_box.send_keys("")
        search_box.send_keys(Keys.RETURN)
        
        # 팝업 출현 대기 (최대 5초)
        try:
            popup = wait.until(
                EC.presence_of_element_located((PopupSelectors.NO_SEARCH_POPUP))
            )
            
            # 팝업 표시 확인
            assert popup.is_displayed(), "❌ 팝업이 표시되지 않았습니다."
            
            # 팝업 텍스트 확인
            popup_text = popup.text
            assert "검색어를 입력해주세요" in popup_text, f"❌ 예기치 않은 팝업 메시지: {popup_text}"
            
            print(f"✅ 테스트 성공: 팝업 메시지 확인됨 - '{popup_text}'")
            
        except TimeoutException:
            capture_screenshot(driver, "팝업 미노출", "screenshot_popup_timeout")
            pytest.fail("❌ 팝업이 5초 내에 나타나지 않았습니다.")
            
    except TimeoutException:
        capture_screenshot(driver, "검색박스 미발견", "screenshot_searchbox_timeout")  
        pytest.fail("❌ 검색박스를 찾을 수 없습니다.")
        
    except Exception as e:
        capture_screenshot(driver, "예외 발생", "screenshot_unexpected_error")
        pytest.fail(f"❌ 예기치 않은 오류: {str(e)}")
