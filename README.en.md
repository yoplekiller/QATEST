# QA Test Automation Portfolio

[한국어](./README.md) | **English**

[![Test Automation](https://github.com/yoplekiller/QATEST/actions/workflows/Test_Automation.yaml/badge.svg)](https://github.com/yoplekiller/QATEST/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.27-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-8.3-red.svg)](https://pytest.org/)

> UI/API Test Automation for Kurly (Korean E-commerce) Website

[Live Allure Report](https://yoplekiller.github.io/QATEST/)

---

## Project Overview

QA Engineer portfolio — test automation for Kurly, a live e-commerce site, using Python + Selenium for UI tests and TMDB API for API tests.

### Key Features

| Feature | Description |
|---------|-------------|
| **Page Object Model** | 6 page classes for structured automation |
| **Multi-Platform** | Web (Selenium) + API (Requests) |
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
| Database | MySQL + mysql-connector-python |
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
│   │   ├── kurly_product_page.py  # Product details
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
│       ├── api/                   # API tests (9)
│       ├── ui/                    # UI tests (11)
│       └── sql/                   # SQL DB tests (10)
│           ├── conftest.py
│           ├── setup_test_db.py
│           ├── test_data_integrity.py
│           ├── test_data_consistency.py
│           └── test_query_validation.py
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
DB_HOST=localhost                            # For SQL tests
DB_PORT=3306                                 # For SQL tests
DB_USER=root                                 # For SQL tests
DB_PASSWORD=your_db_password                 # For SQL tests
DB_NAME=tmdb_test                            # For SQL tests
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
pytest -m sql

# View Allure report
allure serve ./allure-results
```

## Test Cases

### Kurly UI Tests (22 active / 2 skipped)

| Test | Validation |
|------|------------|
| `test_ui_login` (3) | Valid/invalid login, empty input, page elements |
| `test_ui_search` (7) | Normal search, blank search, special chars, result click |
| `test_ui_cart` (1) | Cart page access |
| `test_ui_add_goods` (1) | Search → quantity adjustment (up ×2, down ×1) → add to cart |
| `test_add_goods_to_cart` (1) | Login → search → quantity adjustment → add to cart flow |
| `test_ui_goods_add_flow` (1) | Login → search → add product → cart navigation E2E |
| `test_cart_management` (2) | Add multiple items to cart, remove item from cart |
| `test_blank_search` (1) | Empty search keyword handling |
| `test_ui_sort_button` (4) | Sort by recommend / new / low price / high price |
| `test_ui_quantity` (1) | ⚠️ skip - cart popup unavailable without login |
| `test_invalid_search` (1) | ⚠️ skip - Kurly no-result message UI changed |

Target: https://www.kurly.com

### TMDB API Tests (9 tests)

| Test | Validation |
|------|------------|
| `test_popular_movie` | Popular movies list (200, results field) |
| `test_search_movie` | Movie search functionality |
| `test_movie_details` | Required fields (id, title, overview) |
| `test_movie_videos` | Video data validation |
| `test_api_sla` | Response time under 2s SLA |
| `test_movie_invalid_api_key` | 401 error handling |
| `test_movie_genre_inclusion` | Genre inclusion check |
| `test_movie_release_date_consistency` | Release date format (YYYY-MM-DD) |
| `test_top_rated_movie_consistency` | Rating range (0-10) |

Target: https://api.themoviedb.org/3

### SQL Database Tests (10 tests)

| Test | Validation |
|------|------------|
| `test_no_null_movie_ids` | No NULL movie IDs |
| `test_no_duplicate_movie_ids` | No duplicate IDs |
| `test_vote_average_range` | Rating within 0-10 range |
| `test_release_date_format` | Date format (YYYY-MM-DD) |
| `test_api_db_movie_count_match` | API result count matches DB row count |
| `test_api_db_movie_title_match` | API title matches DB title |
| `test_api_db_vote_average_match` | API rating matches DB rating |
| `test_top_rated_movies_query` | ORDER BY top-rated movie query |
| `test_movies_by_popularity` | Popularity-based sorting |
| `test_movie_count_by_year` | GROUP BY yearly movie count |

Flow: Fetch TMDB API data → Store in MySQL → Verify data integrity/consistency via SQL queries

---

## Key Implementations

### Page Object Model

```
BasePage (common: open, find_element, click, send_keys, is_displayed, take_screenshot)
  ├── KurlyLoginPage     Login handling
  ├── KurlyMainPage      Search, navigation
  ├── KurlySearchPage    Search results, sorting
  ├── KurlyProductPage   Product details
  └── KurlyCartPage      Shopping cart
```

### CI/CD

- `main`, `develop` branch PR / `feature/*`, `temp/*` push
- 8-hour scheduled runs / Manual execution

```
Checkout → Install deps → Run UI/API tests
→ Generate Allure Report → Deploy to GitHub Pages → Slack notification
```

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
