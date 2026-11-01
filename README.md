# QA 테스트 자동화 포트폴리오

**한국어** | [English](./README.en.md)

[![Test Automation](https://github.com/yoplekiller/QATEST/actions/workflows/Test_Automation.yaml/badge.svg)](https://github.com/yoplekiller/QATEST/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.27-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-8.3-red.svg)](https://pytest.org/)

> 마켓컬리 웹사이트 UI 테스트 자동화 프로젝트
> 총 24개 테스트 케이스 (22개 실행 + 2개 skip)

[Live Allure Report](https://yoplekiller.github.io/QATEST/)

---

## 프로젝트 소개

반복적인 수동 회귀 테스트의 비효율을 개선하고, 실무에서 바로 적용 가능한 자동화 설계 역량을 갖추기 위해 구현한 개인 포트폴리오 프로젝트입니다.

Python + Selenium 기반으로 실제 운영 중인 마켓컬리 웹사이트를 대상으로 UI 테스트를 구성하였습니다.

### 주요 특징

| 특징 | 설명 |
|------|------|
| **Page Object Model** | 6개 페이지 클래스로 구조화 |
| **CI/CD** | GitHub Actions 하루 1회 자동 실행 |
| **Allure Report** | 단계별 실행 과정 시각화, GitHub Pages 자동 배포 |
| **Jira 자동 연동** | 테스트 실패 시 Jira 버그 티켓 자동 생성 |
| **Jira Status Watcher** | Jira 이슈 상태 변경 감지 → Slack 실시간 알림 |
| **환경변수 관리** | .env 기반 계정 정보 보호 |
| **Slack 알림** | 테스트 결과 및 Jira 상태 변경 실시간 알림 |

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| Language | Python 3.11 |
| Web UI | Selenium 4.27 |
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
│   │   ├── kurly_goods_page.py    # 상품 상세
│   │   └── kurly_search_page.py   # 검색 결과
│   │
│   ├── config/
│   │   └── constants.py           # 타임아웃, URL 상수
│   │
│   ├── report/
│   │   └── generate_excel_report.py
│   │
│   └── tests/
│       ├── conftest.py            # Pytest Fixture
│       └── ui/                    # UI 테스트 (22개)
│
├── utils/
│   ├── logger.py
│   └── ...
│
├── .github/workflows/
│   ├── Test_Automation.yaml       # CI/CD 메인 파이프라인
│   └── jira_status_watch.yaml     # Jira 상태 감시 (1시간 주기)
│
├── cache/
│   └── jira_status_cache.json     # Jira 상태 변경 감지용 캐시
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
# .env 파일을 편집하여 계정 정보 입력
```

### 환경변수 (.env)

```env
KURLY_TEST_USERNAME=your_test_username       # 필수
KURLY_TEST_PASSWORD=your_test_password       # 필수
SLACK_WEBHOOK_URL=your_slack_webhook_url     # 선택
```

### 테스트 실행

```bash
# 전체 테스트
pytest --alluredir=./allure-results

# CI 와 같은 방식: 파일 단위 병렬(워커 3) + 실패 시 1회 재시도(재시도 통과는 Flaky 로 따로 집계)
pytest -n 3 --dist loadfile --reruns 1 --reruns-delay 3

# 마커로 실행
pytest -m ui

# Allure 리포트 확인
allure serve ./allure-results
```

## 테스트 케이스

### UI 테스트 (24개: 20개 실행 · 1개 known issue(xfail) · 3개 skip)

| 테스트 | 케이스 수 | 검증 내용 |
|--------|-----------|-----------|
| `test_ui_login` | 3 | 빈 계정 로그인 실패, 로그인 페이지 요소 확인 (잘못된 계정 케이스는 ⚠️ skip - 로그인 봇 탐지) |
| `test_ui_search` | 8 | 유효 검색어 3종(사과/우유/계란), 빈 검색어, 첫 번째 결과 클릭, 특수문자 3종 (`' OR 1=1--` 은 🟡 known issue: 사이트가 에러 페이지 노출) |
| `test_blank_search` | 1 | 빈 검색어 입력 시 '검색어를 입력해주세요' 팝업 확인 |
| `test_ui_cart` | 1 | 장바구니 아이콘 클릭 → 장바구니 페이지 이동 확인 |
| `test_ui_add_goods` | 1 | 상품 검색 → 수량 조절(2회 증가, 1회 감소) → 장바구니 담기 → 담기 완료 토스트 확인 |
| `test_add_goods_to_cart` | 1 | ⚠️ skip - 로그인 필요(로그인 봇 탐지로 자동화 불가) |
| `test_ui_goods_add_flow` | 1 | ⚠️ skip - 로그인 필요(로그인 봇 탐지로 자동화 불가) |
| `test_cart_management` | 2 | 여러 상품(3개) 장바구니 담기 → 개수 3 확인, 1개 담고 삭제 → 개수 1→0 확인 |
| `test_ui_sort_button` | 4 | 추천순 / 신상품순 / 낮은가격순 / 높은가격순 정렬 |
| `test_ui_quantity` | 1 | 상품 선택 팝업 수량 +2 / -1 → 클릭마다 반영 확인 |
| `test_invalid_search` | 1 | 없는 검색어 → 결과 없음 메시지 확인 |

테스트 대상: https://www.kurly.com

---

## 주요 구현

### Page Object Model

```
BasePage (공통: open, find_element, click, send_keys, is_displayed, take_screenshot)
  ├── KurlyLoginPage     로그인 처리
  ├── KurlyMainPage      검색, 네비게이션
  ├── KurlySearchPage    검색 결과, 정렬
  ├── KurlyGoodsPage     상품 상세
  └── KurlyCartPage      장바구니
```

### CI/CD 파이프라인

**트리거 조건**
- `main`, `develop` 브랜치 push / PR
- 하루 1회 스케줄 (`0 0 * * *` UTC)
- 수동 실행 (workflow_dispatch)

**파이프라인 구조**

```
[Push / Schedule / PR]
        │
        ▼
    ui_tests
        │
   ┌────┴──────────┐
   ▼               ▼
 deploy      create_jira_bugs   ← 병렬 실행
(GitHub Pages)  (실패 케이스 Jira 자동 등록)
   └────┬──────────┘
        ▼
  notify_slack
  (테스트 결과 Slack 발송)
```

**concurrency 설정**: 동시 배포 방지 (`cancel-in-progress: true`)

**안정성 · 가시성 (2026-11-01)** — 자세한 내용: [docs/changes/2026-11-01_selenium-flaky-hardening.md](docs/changes/2026-11-01_selenium-flaky-hardening.md)
- `pytest-xdist` 파일 단위 병렬(워커 3), `pytest-rerunfailures` 1회 재시도
- 재시도로 통과한 테스트는 통과로 치지 않고 **Flaky** 로 따로 집계 → Actions 요약 · Slack 에 표시
- 실패 시 스크린샷 · URL · page source · 브라우저 콘솔 로그를 Allure 첨부 + `failure-evidence` artifact 업로드
- 사이트 결함은 `xfail(strict=True)` known issue 로 분리 (고쳐지면 XPASS 로 CI 가 알림)

### Jira 자동 연동

테스트 실패 시 자동으로 Jira 버그 티켓을 생성하고, Jira 이슈 상태 변경을 감지해 Slack으로 알림을 전송합니다.

```
[테스트 실패]
     │
     ▼
create_jira_bugs (GitHub Actions)
     │  test_results_ui.json 파싱
     ▼
Jira 버그 티켓 자동 생성 (utils/create_jira_bugs.py)

[Jira Status Watcher] ← 매 1시간 실행
     │  Jira 이슈 상태 변경 감지 (cache/jira_status_cache.json 비교)
     ▼
Slack 알림 발송 (utils/jira_status_watcher.py)
```


---
## 관련 프로젝트

- [PlaywrightQA](https://github.com/yoplekiller/PlaywrightQA) - Playwright/TypeScript E2E 테스트
- [KurlyApp](https://github.com/yoplekiller/KurlyApp) - Python/Appium 모바일 테스트
- [AutoTC](https://github.com/yoplekiller/AutoTC) - 테스트 케이스 자동 생성 

---

## 작성자

**LIM JAE MIN**
- GitHub: [@YopleKiller](https://github.com/YopleKiller)
- Email: jmlim9244@gmail.com

---

## License

MIT License
