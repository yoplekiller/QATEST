from selenium.webdriver.common.by import By

class URLs:
      KURLY_MAIN = "https://www.kurly.com/main"
      KURLY_LOGIN = "https://www.kurly.com/member/login"
      KURLY_CART = "https://www.kurly.com/shop/cart"
      KURLY_SNACK = "https://www.kurly.com/search?sword=%EA%B3%BC%EC%9E%90&page=1"

class Selectors:
      SEARCH_BOX = (By.CSS_SELECTOR, "input[placeholder*='검색']")
      LOGIN_BUTTON = (By.XPATH, "//a[contains(text(),'로그인')]")
      # 기존: //a[3]//div[2]//button[1] → 개선 필요
      FIRST_PRODUCT = (By.CSS_SELECTOR, ".product-item:first-child button")

class PopupSelectors:
      NO_SEARCH_POPUP = (By.XPATH, "//div[@class='popup-content css-15yaaju e1k5padi2']")
      CONFIRM_BUTTON = (By.XPATH, "//button[text()='확인']")

class ErrorMessages:
      ERROR_MSG = (By.XPATH,"//div[@class='css-1d3w5wq e1oh2pka6']")


class Buttons:
      ADD_TO_CART = (By.XPATH, "(//button[@type='button'][contains(text(),'담기')])[1]")
      INCREASE_QUANTITY = (By.XPATH, "(//button[@aria-label='수량올리기'])[2]")
      DECREASE_QUANTITY = (By.XPATH, "(//button[@aria-label='수량내리기'])[2]")
      ADD_TO_CART_2 = (By.XPATH, "(//button[@class='css-ahkst0 e4nu7ef3'])[1]")
      LOGIN_BUTTON = (By.XPATH, "//a[contains(text(),'로그인')]")
      LOGIN_USERNAME_INPUT = (By.XPATH, "//input[@placeholder='아이디를 입력해주세요']")
      LOGIN_PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='비밀번호를 입력해주세요']")
      LOGIN_BUTTON_SUBMIT = (By.XPATH,"//button[@type='submit']")
      CART_BUTTON = (By.XPATH, "(//button[@class='css-g25h97 e14oy6dx1'])[1]")


class Timeouts:
      SHORT = 3
      MEDIUM = 10
      LONG = 20