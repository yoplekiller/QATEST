"""
스크린샷 캡처 기능 테스트 모듈
- 의도적으로 FAIL을 발생시켜, conftest.py의 "자동 실패 스크린샷 캡처"가
  정상 동작하는지 검증하는 테스트
"""

import allure
import pytest
from src.pages.kurly_main_page import KurlyMainPage


@pytest.mark.ui
@allure.feature("UI 테스트")
@allure.story("스크린샷 실패 케이스")
@allure.severity(allure.severity_level.TRIVIAL)
@allure.title("테스트 실패 시 스크린샷 자동 캡처 검증")
def test_fail_screenshot(driver):
    """
    이 테스트의 진짜 목적:
    - test 본문에서 FAIL 발생
    - conftest.py 훅이 그 FAIL 시점에 스크린샷을 자동 저장 + Allure 첨부

    중요:
    - 여기서 take_screenshot()을 직접 호출하면 '자동 캡처' 검증이 흐려짐
    - 따라서 "실패만 만들고", 캡처는 훅에 맡기는 게 핵심
    """
    main_page = KurlyMainPage(driver)

    with allure.step("메인 페이지 접속"):
        main_page.open_main_page()

    with allure.step("고의 실패 유발 (자동 스크린샷 훅 동작 확인)"):
        # 일부러 틀린 조건을 걸어 FAIL 발생
        # 예: 존재할 수 없는 문자열이 title에 포함되어야 한다고 주장
        assert "절대_존재하지_않는_문구" in driver.title, "고의 실패로 자동 스크린샷 캡처 테스트"
