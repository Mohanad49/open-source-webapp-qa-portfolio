# Open-Source Web App QA Portfolio

**Live Report Hub**: https://mohanad49.github.io/open-source-webapp-qa-portfolio/ <br>
**Target App**: https://the-internet.herokuapp.com <br>
**Repository**: https://github.com/Mohanad49/open-source-webapp-qa-portfolio

A production-style Selenium + PyTest automation framework targeting Sauce Labs' open-source **The Internet** web app.

## Why this project exists

Most junior QA portfolios are just loose Selenium scripts. This one is intentionally structured like a real QA framework:

- Page Object Model.
- Environment-based configuration.
- Explicit waits.
- PyTest markers and parameterization.
- Failure screenshots and page-source capture.
- PyTest HTML report.
- Allure report integration.
- GitHub Actions CI.
- GitHub Pages-ready report hub.

## Target application

- App: The Internet
- Public URL: `https://the-internet.herokuapp.com`
- Source: `https://github.com/saucelabs/the-internet`

The app is designed for automated acceptance testing and contains realistic browser behaviors: authentication, forms, dynamic loading, tables, JavaScript alerts, file uploads, and multiple windows.

## Design direction

**Aesthetic:** industrial QA war room.

The included `report-hub/` is intentionally dark, sharp, and operational. It is not a generic pastel portfolio page. It is designed to feel like a release-control room where evidence, risk, and defects are tracked before production.

## Project structure

```text
open-source-webapp-qa-portfolio/
├── .github/workflows/qa.yml        # CI + optional GitHub Pages deployment
├── assets/                         # Test fixtures
├── config/settings.py              # Environment-driven runtime settings
├── docs/                           # Strategy, design thinking, defect template
├── pages/                          # Page Object Model classes
├── report-hub/                     # Static portfolio/report landing page
├── scripts/count_tests.py          # Test collection helper
├── tests/                          # PyTest test modules
├── conftest.py                     # Fixtures, WebDriver setup, artifacts
├── pytest.ini                      # PyTest config
├── pyproject.toml                  # Tooling config
├── requirements.txt                # Python dependencies
└── README.md
```

## Coverage summary

The suite contains 70 collected automated checks through direct tests and parameterized cases.

| Area | Coverage |
|---|---|
| Home/navigation | App branding, catalog presence, key links, selected navigation paths |
| Authentication | Valid login, logout, invalid credentials, protected route behavior |
| Forms | Checkboxes, dropdowns, numeric inputs |
| Dynamic behavior | Dynamic controls, delayed loading, explicit waits |
| Add/remove elements | Add, delete, clear dynamic elements |
| Tables | Headers, known records, formatting, sort behavior |
| Browser interactions | Alerts, confirms, prompts, new windows |
| File upload/status codes | Upload confirmation and status-code content |

## Prerequisites

Install these before running the suite:

- Python 3.11+
- Google Chrome or Firefox
- Java 17+ for Allure CLI
- Node.js/npm if you install Allure CLI through npm

Selenium 4 can use Selenium Manager to locate/download browser drivers automatically, but browser and driver availability still depends on your local machine or CI runner.

## Local installation

### macOS/Linux

```bash
cd open-source-webapp-qa-portfolio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

### Windows PowerShell

```powershell
cd open-source-webapp-qa-portfolio
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Run the tests

### Smoke suite

```bash
python -m pytest -m smoke --browser chrome \
  --html=reports/pytest-report.html --self-contained-html \
  --alluredir=reports/allure-results
```

### Full regression suite

```bash
python -m pytest --browser chrome \
  --html=reports/pytest-report.html --self-contained-html \
  --alluredir=reports/allure-results
```

### Run headed for debugging

```bash
python -m pytest -m smoke --browser chrome --headed
```

### Run Firefox

```bash
python -m pytest -m smoke --browser firefox
```

### Count collected tests

```bash
python scripts/count_tests.py
```

## Generate reports

### PyTest HTML

The HTML report is created here:

```text
reports/pytest-report.html
```

Open it directly in your browser.

### Allure report

Install Allure CLI first. One simple option is:

```bash
npm install -g allure-commandline
```

Then generate and open the report:

```bash
allure generate reports/allure-results --clean -o reports/allure-report
allure open reports/allure-report
```

## Configuration

Runtime values can be controlled through `.env` or CLI arguments.

```env
BASE_URL=https://the-internet.herokuapp.com
BROWSER=chrome
HEADLESS=true
TIMEOUT=12
SLOW_MO=0
SCREENSHOT_ON_FAIL=true
```

Examples:

```bash
BASE_URL=https://the-internet.herokuapp.com HEADLESS=true python -m pytest -m smoke
python -m pytest --base-url https://the-internet.herokuapp.com --browser chrome --timeout 15
```

## Next upgrades

- Add browser matrix execution for Chrome + Firefox.
- Add Dockerized local run.
- Add test result trend history.
- Add visual testing with Playwright or Percy.
- Add API checks for a separate open-source API target.
