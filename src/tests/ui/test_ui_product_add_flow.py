# """
# 상품 추가 플로우 테스트 (POM 패턴 적용)
# 로그인 → 상품 검색 → 장바구니 추가 → 확인
# """
# import allure
# import pytest
# from src.pages.kurly_login_page import KurlyLoginPage
# from src.pages.kurly_main_page import KurlyMainPage
# from src.pages.kurly_product_page import KurlyProductPage
# from src.pages.kurly_cart_page import KurlyCartPage
# from utils.config_utils import get_test_credentials


# @pytest.mark.ui
# @allure.feature("E2E 플로우")
# @allure.story("로그인 후 상품 추가")
# @allure.severity(allure.severity_level.CRITICAL)
# class TestProductAddFlow:
#     """
#     전체 플로우 테스트: 로그인 → 상품 추가 → 장바구니 확인 (POM 적용)
#     """
#     @pytest.fixture(autouse=True)
#     def setup(self, driver):
#         """
#         각 테스트 메서드 실행 전 자동으로 실행되는 설정
#         """
#         self.login_page = KurlyLoginPage(driver)
#         self.main_page = KurlyMainPage(driver)
#         self.product_page = KurlyProductPage(driver)
#         self.cart_page = KurlyCartPage(driver)
#         self.credentials = get_test_credentials()

#     @allure.title("로그인 후 상품 추가 및 장바구니 확인")
#     @allure.description("""
#     **목적:** 로그인부터 장바구니 담기까지 전체 플로우가 정상 동작하는지 확인

#     **테스트 단계:**
#     1. 마켓컬리 메인 페이지 접속
#     2. 로그인
#     3. 상품 검색 ('과자')
#     4. 상품 선택 및 장바구니 추가
#     5. 수량 조절
#     6. 장바구니 담기
#     7. 장바구니 페이지로 이동

#     **예상 결과:** 전체 플로우가 성공적으로 완료됨
#     """)
#     def test_full_product_add_flow(self, driver):
#         """
#         로그인 → 상품 검색 → 장바구니 추가 전체 플로우 테스트
#         """
#         # Step 1: 로그인
#         with allure.step("로그인 프로세스"):
#             self.login_page.open_main_page()
#             self.login_page.go_to_login_page()
#             self.login_page.enter_username(self.credentials['username'])
#             self.login_page.enter_password(self.credentials['password'])
#             self.login_page.click_login_button()

#         # Step 2: 상품 검색
#         with allure.step("상품 검색: '과자'"):
#             self.main_page.search_product("과자")

#         # Step 3: 상품 추가
#         with allure.step("세 번째 상품 선택"):
#             self.product_page.click_third_product_add_button()

#         # Step 4: 수량 조절
#         with allure.step("수량 올리기"):
#             self.product_page.increase_quantity(1)

#         # Step 5: 장바구니 담기
#         with allure.step("장바구니 담기"):
#             self.product_page.click_add_to_cart_in_popup()

#         # Step 6: 장바구니로 이동
#         with allure.step("장바구니 페이지로 이동"):
#             self.cart_page.click_cart_icon()

#         # Then: 전체 플로우 성공 확인
#         with allure.step("결과 확인"):
#             self.cart_page.take_screenshot("전체_플로우_완료")

#             allure.attach(
#                 "로그인부터 장바구니 추가까지 전체 플로우가 성공적으로 완료되었습니다",
#                 name="테스트_결과",
#                 attachment_type=allure.attachment_type.TEXT
#             )
