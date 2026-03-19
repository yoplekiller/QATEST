# QA Test Automation Portfolio

[한국어](./README.md) | **English**

[![Test Automation](https://github.com/yoplekiller/QATEST/actions/workflows/Test_Automation.yaml/badge.svg)](https://github.com/yoplekiller/QATEST/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.27-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-8.3-red.svg)](https://pytest.org/)

> UI / API Test Automation for Kurly (Korean E-commerce) Website
> Total 50 test cases (UI 22 active + 2 skipped, API 26)

[Live Allure Report](https://yoplekiller.github.io/QATEST/)

---

## Project Overview

QA Engineer portfolio — test automation for Kurly, a live e-commerce site, using Python + Selenium for UI tests and TMDB API for API tests.

### Key Features

| Feature | Description |
|---------|-------------|
| **Page Object Model** | 6 page classes for structured automation |
| **Multi-Platform** | Web UI (Selenium) + API (Requests) |
| **CI/CD** | GitHub Actions with 8-hour scheduled runs |
| **Allure Report** | Step-by-step execution visualization |
| **Environment Variables** | .env-based API key/credential protection |
| **Slack Notifications** | Real-time test result alerts |

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| Web UI | Selenium 4.27 |
| API | Requests 2.32 |
| Framework | Pytest 8.3 |
| Reporting | Allure Report |
| CI/CD | GitHub Actions + GitHub Pages |

---

## Project Structure

```
QATEST/
├── src/
│   ├── pages/                     # Page Object Model
│   │   ├── base_page.py           # Common methods
│   │   ├── kurly_login_page.py    # Login
│   │   ├── kurly_main_page.py     # Main (search, navigation)
│   │   ├── kurly_cart_page.py     # Shopping cart
│   │   ├── kurly_goods_page.py    # Product details
│   │   └── kurly_search_page.py   # Search results
│   │
│   ├── config/
│   │   ├── config.yaml            # API endpoint config
│   │   └── constants.py           # Timeouts, URL constants
│   │
│   ├── report/
│   │   └── generate_excel_report.py
│   │
│   └── tests/
│       ├── conftest.py            # Pytest Fixtures
│       ├── api/                   # API tests (26)
│       └── ui/                    # UI tests (24)
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
│   └── Test_Automation.yaml       # CI/CD config
│
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md
```

## Installation & Execution

```bash
# Clone repository
git clone https://github.com/yoplekiller/QATEST.git
cd QATEST

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with actual API keys and credentials
```

### Environment Variables (.env)

```env
TMDB_API_KEY=your_tmdb_api_key              # Required
KURLY_TEST_USERNAME=your_test_username       # Required
KURLY_TEST_PASSWORD=your_test_password       # Required
SLACK_WEBHOOK_URL=your_slack_webhook_url     # Optional
```

### Running Tests

```bash
# All tests
pytest --alluredir=./allure-results

# By test suite
pytest src/tests/api --alluredir=./allure-results
pytest src/tests/ui --alluredir=./allure-results
# By marker
pytest -m api
pytest -m ui

# View Allure report
allure serve ./allure-results
```

## Test Cases

### Kurly UI Tests (22 active / 2 skipped)

| Test | Cases | Validation |
|------|-------|------------|
| `test_ui_login` | 3 | Invalid login, empty credentials, login page elements |
| `test_ui_search` | 8 | Valid keywords ×3 (사과/우유/계란), empty search, click first result, special chars ×3 |
| `test_blank_search` | 1 | Empty keyword → '검색어를 입력해주세요' popup |
| `test_ui_cart` | 1 | Cart icon click → cart page navigation |
| `test_ui_add_goods` | 1 | Search → quantity adjustment (up ×2, down ×1) → add to cart |
| `test_add_goods_to_cart` | 1 | Login → search → quantity adjustment → add to cart flow |
| `test_ui_goods_add_flow` | 1 | Login → search → add product → cart navigation E2E |
| `test_cart_management` | 2 | Add 3 items to cart, remove item from cart |
| `test_ui_sort_button` | 4 | Sort by recommend / new / low price / high price |
| `test_ui_quantity` | 1 | ⚠️ skip - cart popup unavailable without login |
| `test_invalid_search` | 1 | ⚠️ skip - Kurly no-result message UI changed |

Target: https://www.kurly.com

### TMDB API Tests (26 tests)

| Test | Cases | Validation |
|------|-------|------------|
| `test_get_popular_movies` | 1 | Popular movies list (200, results field) |
| `test_search_movie` | 1 | Search Inception, verify first result title |
| `test_get_movie_details` | 3 | Fight Club / The Matrix / Interstellar id & title |
| `test_movie_videos` | 1 | Fight Club video data exists |
| `test_api_sla` | 2 | /movie/popular, /genre/movie/list response under 2s |
| `test_movie_genre_inclusion` | 3 | Genre inclusion for 3 movies |
| `test_movie_release_date_consistency` | 3 | Release date format (YYYY-MM-DD) for 3 movies |
| `test_movie_pagination_page_1` | 1 | Page 1 results count validation |
| `test_movie_pagination_page_2` | 1 | No duplicate results between page 1 and 2 |
| `test_pagination_invalid_page_zero` | 1 | Page 0 request → 400 error |
| `test_pagination_out_of_range` | 1 | Page >500 request → 400 error |
| `test_movie_not_found` | 1 | Non-existent movie ID → 404 |
| `test_empty_api_key` | 1 | Empty API key → 401 |
| `test_missing_api_key` | 1 | Missing API key → 401 |
| `test_invalid_api_key` | 1 | Invalid API key → 401 |
| `test_empty_search_query` | 1 | Empty search query → 0 results |
| `test_invalid_page_number` | 1 | Page -1 → 422 error |
| `test_invalid_language_code` | 1 | Invalid language code → default response |
| `test_nonexistent_endpoint` | 1 | Non-existent endpoint → 404 |

Target: https://api.themoviedb.org/3

---

## Key Implementations

### Page Object Model

```
BasePage (common: open, find_element, click, send_keys, is_displayed, take_screenshot)
  ├── KurlyLoginPage     Login handling
  ├── KurlyMainPage      Search, navigation
  ├── KurlySearchPage    Search results, sorting
  ├── KurlyGoodsPage     Product details
  └── KurlyCartPage      Shopping cart
```

### CI/CD

- `main`, `develop` branch PR / `feature/*`, `temp/*` push
- 8-hour scheduled runs / Manual execution

```
Checkout → Install deps → Run UI/API tests
→ Generate Allure Report → Deploy to GitHub Pages → Slack notification
```

## Screenshots

### Allure Report
![Allure Report](./docs/screenshots/allure_report.png)

### GitHub Actions CI/CD
![GitHub Actions](./docs/screenshots/github_actions.png)

### Slack Notifications
![Slack](./docs/screenshots/slack_notification.png)

---

## Demo

[Kurly Order Flow Automation (YouTube)](https://www.youtube.com/watch?v=TqsvT2RsYEs)

## Related Projects

- [PlaywrightQA](https://github.com/yoplekiller/PlaywrightQA) - Playwright/TypeScript E2E Testing
- [woongjinAppTest](https://github.com/yoplekiller/woongjinAppTest) - Python/Appium Mobile Testing

---

## Author

**LIM JAE MIN**
- GitHub: [@YopleKiller](https://github.com/YopleKiller)
- Email: jmlim9244@gmail.com

---

## License

MIT License
