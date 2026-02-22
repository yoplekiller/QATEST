# QA 테스트 자동화 포트폴리오

**한국어** | [English](./README.en.md)

[![Test Automation](https://github.com/yoplekiller/QATEST/actions/workflows/Test_Automation.yaml/badge.svg)](https://github.com/yoplekiller/QATEST/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.27-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-8.3-red.svg)](https://pytest.org/)

> 마켓컬리 웹사이트 UI/API 테스트 자동화 프로젝트

[Live Allure Report](https://yoplekiller.github.io/QATEST/)

---

## 프로젝트 소개

QA 엔지니어 포트폴리오 프로젝트입니다. Python + Selenium 기반으로 실제 운영 중인 마켓컬리 웹사이트를 대상으로 UI 테스트를, TMDB API를 대상으로 API 테스트를 구성하였습니다.

### 주요 특징

| 특징 | 설명 |
|------|------|
| **Page Object Model** | 6개 페이지 클래스로 구조화 |
| **다중 플랫폼** | Web (Selenium) + Mobile (Appium) + API (Requests) |
| **CI/CD** | GitHub Actions 8시간 주기 자동 실행 |
| **Allure Report** | 단계별 실행 과정 시각화 |
| **환경변수 관리** | .env 기반 API 키/계정 정보 보호 |
| **Slack 알림** | 테스트 결과 실시간 알림 |

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| Language | Python 3.11 |
| Web UI | Selenium 4.27 |
| Mobile | Appium + UiAutomator2 |
| API | Requests 2.32 |
| Framework | Pytest 8.3 |
| Reporting | Allure Report |
| CI/CD | GitHub Actions + GitHub Pages |

---

## 프로젝트 구조

```
QATEST/
├── src/
│   ├── pages/                     # Page Object Model
│   │   ├── base_page.py           # 공통 메서드
│   │   ├── kurly_login_page.py    # 로그인
│   │   ├── kurly_main_page.py     # 메인 (검색, 네비게이션)
│   │   ├── kurly_cart_page.py     # 장바구니
│   │   ├── kurly_product_page.py  # 상품 상세
│   │   └── kurly_search_page.py   # 검색 결과
│   │
│   ├── config/
│   │   ├── config.yaml            # API 엔드포인트 설정
│   │   └── constants.py           # 타임아웃, URL 상수
│   │
│   ├── report/
│   │   └── generate_excel_report.py
│   │
│   └── tests/
│       ├── conftest.py            # Pytest Fixture
│       ├── api/                   # API 테스트 (9개)
│       ├── ui/                    # UI 테스트 (11개)
│       └── mobile/                # Mobile 테스트 (3개)
│
├── utils/
│   ├── logger.py
│   ├── api_utils.py
│   ├── config_utils.py
│   └── ...
│
├── testdata/
│   ├── genre_expectations.csv
│   └── movie_list.csv
│
├── .github/workflows/
│   └── Test_Automation.yaml       # CI/CD 설정
│
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md
```

## 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/yoplekiller/QATEST.git
cd QATEST

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 편집하여 API 키 및 계정 정보 입력
```

### 환경변수 (.env)

```env
TMDB_API_KEY=your_tmdb_api_key              # 필수
KURLY_TEST_USERNAME=your_test_username       # 필수
KURLY_TEST_PASSWORD=your_test_password       # 필수
SLACK_WEBHOOK_URL=your_slack_webhook_url     # 선택
```

### 테스트 실행

```bash
# 전체 테스트
pytest --alluredir=./allure-results

# 테스트 스위트별 실행
pytest src/tests/api --alluredir=./allure-results
pytest src/tests/ui --alluredir=./allure-results
pytest src/tests/mobile --alluredir=./allure-results

# 마커로 실행
pytest -m api
pytest -m ui
pytest -m mobile

# Allure 리포트 확인
allure serve ./allure-results
```

## 테스트 케이스

### 마켓컬리 UI 테스트 (11개)

| 테스트 | 검증 내용 |
|--------|-----------|
| `test_ui_login` | 유효/무효 로그인, 빈 입력 처리 |
| `test_ui_search` | 정상 검색, 빈 검색, 특수문자, 결과 클릭 |
| `test_ui_cart` | 장바구니 접근 및 확인 |
| `test_ui_add_product` | 상품 담기 → 수량 조절 → 장바구니 |
| `test_ui_product_add_flow` | 로그인 → 검색 → 추가 → 장바구니 E2E |
| `test_ui_quantity` | 수량 증가/감소 버튼 |
| `test_ui_sort_button` | 상품 정렬 기능 |

테스트 대상: https://www.kurly.com

### TMDB API 테스트 (9개)

| 테스트 | 검증 내용 |
|--------|-----------|
| `test_popular_movie` | 인기 영화 목록 조회 (200, results 필드) |
| `test_search_movie` | 영화 검색 기능 |
| `test_movie_details` | 필수 필드 검증 (id, title, overview) |
| `test_movie_videos` | 비디오 데이터 검증 |
| `test_api_sla` | 응답 시간 2초 미만 SLA |
| `test_movie_invalid_api_key` | 401 에러 처리 |
| `test_movie_genre_inclusion` | 장르 포함 여부 |
| `test_movie_release_date_consistency` | 개봉일 형식 (YYYY-MM-DD) |
| `test_top_rated_movie_consistency` | 평점 범위 (0-10) |

테스트 대상: https://api.themoviedb.org/3

### Mobile 테스트 (3개)

| 테스트 | 검증 내용 |
|--------|-----------|
| `test_best_product` | 베스트 메뉴 진입 |
| `test_low_price` | 저가 필터 기능 |
| `test_new_product` | 신상품 표시 |

테스트 대상: 마켓컬리 앱 (Appium + UiAutomator2)

## 주요 구현

### Page Object Model

```
BasePage (공통: open, find_element, click, send_keys, is_displayed, take_screenshot)
  ├── KurlyLoginPage     로그인 처리
  ├── KurlyMainPage      검색, 네비게이션
  ├── KurlySearchPage    검색 결과, 정렬
  ├── KurlyProductPage   상품 상세
  └── KurlyCartPage      장바구니
```

### CI/CD

- `main`, `develop` 브랜치 PR / `feature/*`, `temp/*` push
- 8시간 주기 스케줄 / 수동 실행

```
Checkout → 의존성 설치 → UI/API 테스트 실행
→ Allure Report 생성 → GitHub Pages 배포 → Slack 알림
```

## 데모 영상

[마켓컬리 주문 플로우 자동화 (YouTube)](https://www.youtube.com/watch?v=TqsvT2RsYEs)

## 관련 프로젝트

- [PlaywrightQA](https://github.com/yoplekiller/PlaywrightQA) - Playwright/TypeScript E2E 테스트
- [woongjinAppTest](https://github.com/yoplekiller/woongjinAppTest) - Python/Appium 모바일 테스트

---

## 작성자

**LIM JAE MIN**
- GitHub: [@YopleKiller](https://github.com/YopleKiller)
- Email: jmlim9244@gmail.com

---

## License

MIT License
