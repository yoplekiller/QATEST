# QA Test Automation Portfolio

[한국어](./README.md) | **English**

[![Test Automation](https://github.com/yoplekiller/QATEST/actions/workflows/Test_Automation.yaml/badge.svg)](https://github.com/yoplekiller/QATEST/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.27-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-8.3-red.svg)](https://pytest.org/)

> UI Test Automation for Kurly (Korean E-commerce) Website
> Total 24 test cases (22 active + 2 skipped)

[Live Allure Report](https://yoplekiller.github.io/QATEST/)

---

## Project Overview

QA Engineer portfolio — test automation for Kurly, a live e-commerce site, using Python + Selenium for UI tests.

### Key Features

| Feature | Description |
|---------|-------------|
| **Page Object Model** | 6 page classes for structured automation |
| **CI/CD** | GitHub Actions with 4-hour scheduled runs |
| **Allure Report** | Step-by-step execution visualization, auto-deployed to GitHub Pages |
| **Jira Auto Integration** | Auto-creates a Jira bug ticket on test failure |
| **Jira Status Watcher** | Detects Jira issue status changes → real-time Slack alert |
| **Environment Variables** | .env-based credential protection |
| **Slack Notifications** | Real-time test result and Jira status alerts |

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| Web UI | Selenium 4.27 |
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
│   │   └── constants.py           # Timeouts, URL constants
│   │
│   ├── report/
│   │   └── generate_excel_report.py
│   │
│   └── tests/
│       ├── conftest.py            # Pytest Fixtures
│       └── ui/                    # UI tests (24)
│
├── utils/
│   ├── logger.py
│   └── ...
│
├── .github/workflows/
│   ├── Test_Automation.yaml       # CI/CD main pipeline
│   └── jira_status_watch.yaml     # Jira status watcher (hourly)
│
├── cache/
│   └── jira_status_cache.json     # Cache for Jira status change detection
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
# Edit .env with actual credentials
```

### Environment Variables (.env)

```env
KURLY_TEST_USERNAME=your_test_username       # Required
KURLY_TEST_PASSWORD=your_test_password       # Required
SLACK_WEBHOOK_URL=your_slack_webhook_url     # Optional
```

### Running Tests

```bash
# All tests
pytest --alluredir=./allure-results

# By marker
pytest -m ui

# View Allure report
allure serve ./allure-results
```

## Test Cases

### UI Tests (22 active / 2 skipped)

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

**Trigger conditions**
- PR to `main`, `develop` branches
- Push to `main` branch
- 4-hour scheduled runs (`0 */4 * * *` UTC)
- Manual execution (workflow_dispatch)

**Pipeline structure**

```
[Push / Schedule / PR]
        │
        ▼
    ui_tests
        │
   ┌────┴──────────┐
   ▼               ▼
 deploy      create_jira_bugs   ← runs in parallel
(GitHub Pages)  (auto-create Jira ticket for failures)
   └────┬──────────┘
        ▼
  notify_slack
  (send test results to Slack)
```

**concurrency**: prevents overlapping deployments (`cancel-in-progress: true`)

### Jira Auto Integration

Automatically creates a Jira bug ticket on test failure, and watches Jira issue status changes to notify Slack.

```
[Test failure]
     │
     ▼
create_jira_bugs (GitHub Actions)
     │  parses test_results_ui.json
     ▼
Auto-create Jira bug ticket (utils/create_jira_bugs.py)

[Jira Status Watcher] ← runs hourly
     │  detects status change (compares cache/jira_status_cache.json)
     ▼
Send Slack alert (utils/jira_status_watcher.py)
```

## Demo

[Kurly Order Flow Automation (YouTube)](https://www.youtube.com/watch?v=TqsvT2RsYEs)

## Related Projects

- [PlaywrightQA](https://github.com/yoplekiller/PlaywrightQA) - Playwright/TypeScript E2E Testing
- [KurlyApp](https://github.com/yoplekiller/KurlyApp) - Python/Appium Mobile Testing
- [AutoTC](https://github.com/yoplekiller/AutoTC) - AI-based Test Case Generation

---

## Author

**LIM JAE MIN**
- GitHub: [@YopleKiller](https://github.com/YopleKiller)
- Email: jmlim9244@gmail.com

---

## License

MIT License
