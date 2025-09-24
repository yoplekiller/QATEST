# QATEST-1 리팩토링 계획서

## 📋 현재 코드 상태 분석

### 🚨 주요 문제점들
1. **하드코딩된 취약한 셀렉터**
   - `//a[3]//div[2]//button[1]` - 구조 변경 시 즉시 실패
   - `//div[@class='count css-6m57y0 e1cqr3m41']` - CSS 클래스 변경 시 실패

2. **불안정한 대기 방식**
   - `time.sleep(3)` 과다 사용
   - 페이지 로딩 시간에 따른 랜덤 실패 가능성

3. **설정 파일 부재**
   - URL, 셀렉터, 테스트 데이터 하드코딩
   - `src/config/constants.py` 파일 없음

4. **Page Object Model 미적용**
   - 테스트 로직과 UI 요소 접근이 섞여있음
   - 코드 재사용성 부족

5. **부분적 에러 처리**
   - 일부 단계만 try-catch 적용
   - 실패 시 디버깅 정보 부족

---

## 🎯 리팩토링 방향 및 우선순위

### 1단계: 기본 구조 개선 (🔴 High Priority)

#### A. 설정 파일 생성
**파일 생성: `src/config/constants.py`**
```python
from selenium.webdriver.common.by import By

class URLs:
    KURLY_BASE = "https://www.kurly.com"
    KURLY_MAIN = f"{KURLY_BASE}/main"
    KURLY_LOGIN = f"{KURLY_BASE}/member/login"
    KURLY_CART = f"{KURLY_BASE}/cart"

class TestData:
    # 테스트용 더미 데이터
    INVALID_USERNAME = "test_invalid_user_123"
    INVALID_PASSWORD = "test_invalid_password_456"
    SEARCH_KEYWORD = "과자"

class Timeouts:
    SHORT = 3
    MEDIUM = 10
    LONG = 20

class Selectors:
    # 로그인 관련
    LOGIN_BUTTON = (By.XPATH, "//a[contains(text(),'로그인')]")
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder*='아이디']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder*='비밀번호']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # 검색 관련
    SEARCH_BOX = (By.CSS_SELECTOR, "input[placeholder*='검색']")

    # 상품 관련 (개선 필요한 부분)
    FIRST_PRODUCT = (By.CSS_SELECTOR, ".product-item:first-child button, [data-testid='product-button']:first-child")

    # 수량 조절
    QUANTITY_UP = (By.CSS_SELECTOR, "button[aria-label*='수량올리기'], button[aria-label*='증가']")
    QUANTITY_DOWN = (By.CSS_SELECTOR, "button[aria-label*='수량내리기'], button[aria-label*='감소']")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[type='number'], .quantity-input")

    # 장바구니
    ADD_TO_CART = (By.CSS_SELECTOR, "button:contains('장바구니'), .cart-button")
    CART_CONFIRM = (By.CSS_SELECTOR, "button:contains('담기'), .cart-confirm")
    GO_TO_CART = (By.CSS_SELECTOR, "button:contains('장바구니'), a[href*='cart']")
```

#### B. 대기 방식 개선
**현재 코드:**
```python
time.sleep(3)  # ❌ 불안정
driver.implicitly_wait(5)  # ❌ 전역 설정
```

**개선 코드:**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, Timeouts.MEDIUM)
element = wait.until(EC.element_to_be_clickable(Selectors.LOGIN_BUTTON))
```

### 2단계: Page Object Model 적용 (🟡 Medium Priority)

#### A. 페이지 객체 생성
**파일 생성: `src/pages/base_page.py`**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.constants import Timeouts
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Timeouts.MEDIUM)

    def click_element(self, locator):
        """안전한 클릭"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return True
        except TimeoutException:
            self._capture_failure_info(f"클릭 실패: {locator}")
            return False

    def send_keys_to_element(self, locator, text):
        """안전한 텍스트 입력"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            return True
        except TimeoutException:
            return False

    def _capture_failure_info(self, action):
        """실패 정보 캡처"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"{action} - 스크린샷",
            attachment_type=allure.attachment_type.PNG
        )
```

**파일 생성: `src/pages/main_page.py`**
```python
from pages.base_page import BasePage
from config.constants import Selectors, URLs
from selenium.webdriver.common.keys import Keys
import allure

class MainPage(BasePage):
    def navigate_to_main(self):
        """메인 페이지로 이동"""
        with allure.step("메인 페이지 이동"):
            self.driver.get(URLs.KURLY_MAIN)
            self.driver.maximize_window()
            return self._wait_for_page_load()

    def search_product(self, keyword):
        """상품 검색"""
        with allure.step(f"상품 검색: {keyword}"):
            success = self.send_keys_to_element(Selectors.SEARCH_BOX, keyword)
            if success:
                element = self.driver.find_element(*Selectors.SEARCH_BOX)
                element.send_keys(Keys.RETURN)
            return success

    def click_login_button(self):
        """로그인 버튼 클릭"""
        with allure.step("로그인 버튼 클릭"):
            return self.click_element(Selectors.LOGIN_BUTTON)

    def select_first_product(self):
        """첫 번째 상품 선택"""
        with allure.step("첫 번째 상품 선택"):
            return self.click_element(Selectors.FIRST_PRODUCT)
```

**파일 생성: `src/pages/product_page.py`**
```python
from pages.base_page import BasePage
from config.constants import Selectors
import allure

class ProductPage(BasePage):
    def increase_quantity(self, times=1):
        """수량 증가"""
        with allure.step(f"수량 {times}번 증가"):
            for _ in range(times):
                if not self.click_element(Selectors.QUANTITY_UP):
                    return False
            return True

    def decrease_quantity(self, times=1):
        """수량 감소"""
        with allure.step(f"수량 {times}번 감소"):
            for _ in range(times):
                if not self.click_element(Selectors.QUANTITY_DOWN):
                    return False
            return True

    def get_current_quantity(self):
        """현재 수량 확인"""
        try:
            element = self.wait.until(EC.presence_of_element_located(Selectors.QUANTITY_INPUT))
            return int(element.get_attribute("value") or element.text)
        except:
            return None

    def add_to_cart(self):
        """장바구니에 추가"""
        with allure.step("장바구니에 추가"):
            return self.click_element(Selectors.ADD_TO_CART)

    def confirm_cart_addition(self):
        """장바구니 추가 확인"""
        with allure.step("장바구니 추가 확인"):
            return self.click_element(Selectors.CART_CONFIRM)

    def go_to_cart(self):
        """장바구니로 이동"""
        with allure.step("장바구니로 이동"):
            return self.click_element(Selectors.GO_TO_CART)
```

### 3단계: 안정성 향상 (🔴 High Priority)

#### A. 셀렉터 전략 개선
**문제있는 현재 셀렉터들:**
```python
# ❌ 구조 의존적 - 깨지기 쉬움
"//a[3]//div[2]//button[1]"

# ❌ CSS 클래스 의존적 - 스타일 변경시 실패
"//div[@class='count css-6m57y0 e1cqr3m41']"

# ❌ 구체적인 클래스명 - 리팩토링시 실패
"//button[@class='css-ahkst0 e4nu7ef3']"
```

**개선된 셀렉터 전략:**
```python
# ✅ 의미있는 속성 사용
"button[aria-label='수량올리기']"
"input[placeholder*='검색']"

# ✅ 데이터 속성 활용
"[data-testid='product-item']"
"[data-qa='add-to-cart']"

# ✅ 텍스트 기반 (변경 가능성 낮음)
"//button[contains(text(), '장바구니')]"

# ✅ 다중 셀렉터 전략
".product-item:first-child button, [data-testid='product-button']:first-child"
```

#### B. 다중 셀렉터 유틸리티
**파일 생성: `src/utils/element_utils.py`**
```python
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_element_with_fallbacks(driver, selectors, timeout=10):
    """여러 셀렉터를 시도하여 요소 찾기"""
    wait = WebDriverWait(driver, timeout)

    for selector in selectors:
        try:
            return wait.until(EC.presence_of_element_located(selector))
        except TimeoutException:
            continue

    raise NoSuchElementException(f"모든 셀렉터 실패: {selectors}")

def click_with_fallbacks(driver, selectors, timeout=10):
    """여러 셀렉터로 클릭 시도"""
    element = find_element_with_fallbacks(driver, selectors, timeout)
    element.click()
    return True
```

### 4단계: 테스트 코드 리팩토링 (🟡 Medium Priority)

#### A. test_ui_quantity.py 개선
```python
import allure
import pytest
from config.constants import URLs, TestData
from pages.main_page import MainPage
from pages.product_page import ProductPage

@allure.feature("UI 테스트")
@allure.story("수량 버튼 동작 테스트")
@allure.title("수량 증가/감소 버튼 동작 확인")
def test_ui_quantity(driver):
    """수량 조절 버튼 동작 테스트"""

    # Page Objects 초기화
    main_page = MainPage(driver)
    product_page = ProductPage(driver)

    # 1. 메인 페이지 이동
    assert main_page.navigate_to_main(), "메인 페이지 이동 실패"

    # 2. 상품 검색
    assert main_page.search_product(TestData.SEARCH_KEYWORD), "상품 검색 실패"

    # 3. 첫 번째 상품 선택
    assert main_page.select_first_product(), "상품 선택 실패"

    # 4. 수량 조절 테스트
    assert product_page.increase_quantity(2), "수량 증가 실패"
    assert product_page.decrease_quantity(1), "수량 감소 실패"

    # 5. 수량 확인
    current_quantity = product_page.get_current_quantity()
    assert current_quantity == 2, f"예상 수량: 2, 실제 수량: {current_quantity}"
```

#### B. test_ui_product_add_flow.py 개선
```python
import allure
import pytest
from config.constants import URLs, TestData
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

@allure.feature("UI 테스트")
@allure.story("로그인 > 상품 추가 > 추가 확인 테스트")
@allure.title("로그인 후 상품 추가하고 상품이 장바구니에 담겨 있는지 확인")
def test_ui_product_add_flow(driver):
    """로그인 후 상품을 장바구니에 추가하는 플로우 테스트"""

    # Page Objects 초기화
    main_page = MainPage(driver)
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    # 1. 메인 페이지 이동
    assert main_page.navigate_to_main(), "메인 페이지 이동 실패"

    # 2. 로그인 시도 (더미 데이터로 실패 예상)
    main_page.click_login_button()
    login_result = login_page.login(TestData.INVALID_USERNAME, TestData.INVALID_PASSWORD)

    # 3. 메인으로 돌아가서 상품 검색
    main_page.navigate_to_main()
    assert main_page.search_product(TestData.SEARCH_KEYWORD), "상품 검색 실패"

    # 4. 상품 선택 및 장바구니 추가
    assert main_page.select_first_product(), "상품 선택 실패"

    product_page.increase_quantity(1)
    assert product_page.add_to_cart(), "장바구니 추가 실패"
    product_page.confirm_cart_addition()

    # 5. 장바구니로 이동
    success = product_page.go_to_cart()
    if success:
        allure.attach("장바구니 이동 성공", name="결과", attachment_type=allure.attachment_type.TEXT)
```

### 5단계: 고급 기능 추가 (🟢 Low Priority)

#### A. 스마트 대기 유틸리티
#### B. 테스트 병렬화 고려
#### C. Docker 환경 최적화

---

## 🚀 실행 순서 (권장)

### Day 1: 기반 구조
1. `src/config/constants.py` 생성
2. `src/pages/base_page.py` 생성
3. `src/utils/element_utils.py` 생성

### Day 2: 페이지 객체
1. `src/pages/main_page.py` 생성
2. `src/pages/product_page.py` 생성
3. `src/pages/login_page.py` 생성

### Day 3: 테스트 리팩토링
1. `test_ui_quantity.py` 개선
2. `test_ui_product_add_flow.py` 개선
3. 기타 테스트 파일들 순차 적용

### Day 4: 검증 및 최적화
1. 전체 테스트 실행
2. 실패 케이스 분석 및 수정
3. 성능 최적화

---

## 📝 주의사항

1. **점진적 적용**: 한 번에 모든 걸 바꾸지 말고 단계별로 진행
2. **기존 기능 보존**: 현재 동작하는 기능을 깨뜨리지 않도록 주의
3. **셀렉터 검증**: 새로운 셀렉터가 실제 사이트에서 작동하는지 확인
4. **CI 환경 고려**: headless 모드에서도 정상 동작하는지 테스트

---

## 🔧 즉시 수정 가능한 부분

### 1. time.sleep() 제거
```python
# Before
time.sleep(3)

# After
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable(locator))
```

### 2. 하드코딩된 URL 제거
```python
# Before
driver.get("https://www.kurly.com/main")

# After
driver.get(URLs.KURLY_MAIN)
```

### 3. 취약한 셀렉터 우선 교체
```python
# Before
"//a[3]//div[2]//button[1]"

# After
"button[aria-label*='장바구니'], .add-to-cart-button"
```

이 계획서를 바탕으로 차근차근 리팩토링하면 훨씬 안정적이고 유지보수하기 쉬운 코드가 될 거야!