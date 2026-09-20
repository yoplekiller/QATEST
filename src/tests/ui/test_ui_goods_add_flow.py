"""
상품 추가 플로우 테스트 (POM 패턴 적용)
로그인 → 상품 검색 → 장바구니 추가 → 확인
"""
import allure
import pytest
import time


@pytest.mark.ui
@allure.feature("E2E 플로우")
@allure.story("로그인 후 상품 추가")
@allure.severity(allure.severity_level.CRITICAL)
class TestGoodAddFlow:
    @allure.title("로그인 후 상품 추가 및 장바구니 확인")
    @allure.description("""
    **목적:** 로그인부터 장바구니 담기까지 전체 플로우가 정상 동작하는지 확인

    **테스트 단계:**
    1. 마켓컬리 메인 페이지 접속
    2. 로그인
    3. 상품 검색 ('과자')
    4. 상품 선택 및 장바구니 추가
    5. 수량 조절
    6. 장바구니 담기
    7. 장바구니 페이지로 이동

    **예상 결과:** 전체 플로우가 성공적으로 완료됨
    """)
    # TC: TC-UI-020, TC-UI-021, TC-UI-022, TC-UI-024 (SC-UI-013)
    @pytest.mark.skip(
        reason=(
            "실사이트 조사로 확인됨: 로그인 폼에 봇 탐지/보안 계층이 새로 추가되어, 유효한 "
            "테스트 계정으로도 자동화된 로그인 시도는 '보안 인증 과정에서 오류가 발생하였습니다' "
            "차단 메시지를 받고 실제 로그인에 도달하지 못함(is_login_successful()의 "
            "USER_MENU 로케이터가 사실상 모든 버튼에 매칭되는 tautology라 이 실패를 숨기고 "
            "있었음 - 실제 로그인 성공 화면을 볼 수 없어 올바른 로케이터로 고칠 근거도 없음). "
            "이 보안 계층을 우회하는 건 범위 밖 - 전용 테스트 환경 없이는 로그인 필요 플로우를 "
            "신뢰성 있게 자동화할 수 없음."
        )
    )
    def test_full_good_add_flow(self, kurly_login_page, kurly_main_page, kurly_search_page, kurly_cart_page, test_credentials):
        """
        로그인 → 상품 검색 → 장바구니 추가 전체 플로우 테스트
        """
        try:
            # Step 1: 로그인
            with allure.step("로그인 프로세스"):
                kurly_login_page.login(test_credentials["username"], test_credentials["password"])

                time.sleep(2)  # 로그인 처리 대기
                assert kurly_login_page.is_login_successful(), "로그인에 실패했습니다"

            # Step 2: 상품 검색
            with allure.step("상품 검색: '과자'"):
                kurly_main_page.search_goods("과자")
                kurly_main_page.wait_until_url_contains("search", timeout=10)

            # Step 3: 상품 추가
            with allure.step("세 번째 상품 선택"):
                kurly_search_page.click_nth_add_button(3)
                
            # Step 4: 수량 조절
            with allure.step("수량 올리기"):
                kurly_search_page.quantity_up_in_alt(1)

            # Step 5: 장바구니 담기
            with allure.step("장바구니 담기"):
                kurly_search_page.add_to_cart_in_alt()
                
            with allure.step("장바구니 페이지로 이동"):
                kurly_cart_page.click_cart_icon()

            # Then: 전체 플로우 성공 확인
            with allure.step("결과 확인"):
                kurly_cart_page.take_screenshot("전체_플로우_완료")

                allure.attach(
                    "로그인부터 장바구니 추가까지 전체 플로우가 성공적으로 완료되었습니다",
                    name="테스트_결과",
                    attachment_type=allure.attachment_type.TEXT
                )
        except Exception as e:
            kurly_cart_page.take_screenshot("전체_플로우_실패")
            raise
