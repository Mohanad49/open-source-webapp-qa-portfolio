from __future__ import annotations

import time
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.settings import DOWNLOADS_DIR, REPORTS_DIR, SCREENSHOTS_DIR, settings


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default=settings.browser, choices=["chrome", "firefox"])
    parser.addoption("--base-url", action="store", default=settings.base_url)
    parser.addoption("--headed", action="store_true", help="Run with a visible browser window.")
    parser.addoption("--timeout", action="store", type=int, default=settings.timeout)


@pytest.fixture(scope="session", autouse=True)
def create_artifact_dirs() -> None:
    for path in (REPORTS_DIR, SCREENSHOTS_DIR, DOWNLOADS_DIR):
        path.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    return str(pytestconfig.getoption("--base-url")).rstrip("/")


@pytest.fixture(scope="session")
def timeout(pytestconfig: pytest.Config) -> int:
    return int(pytestconfig.getoption("--timeout"))


@pytest.fixture()
def driver(pytestconfig: pytest.Config):
    browser = pytestconfig.getoption("--browser")
    headless = not pytestconfig.getoption("--headed") and settings.headless

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": str(DOWNLOADS_DIR),
                "download.prompt_for_download": False,
                "safebrowsing.enabled": True,
            },
        )
        if headless:
            options.add_argument("--headless=new")
        browser_driver = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", str(DOWNLOADS_DIR))
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain,application/octet-stream")
        if headless:
            options.add_argument("-headless")
        browser_driver = webdriver.Firefox(options=options)

    browser_driver.set_page_load_timeout(35)
    yield browser_driver
    browser_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if not browser or not settings.screenshot_on_fail:
        return

    safe_name = item.nodeid.replace("/", "_").replace("::", "__").replace("[", "_").replace("]", "")
    timestamp = int(time.time())
    screenshot_path = SCREENSHOTS_DIR / f"{safe_name}_{timestamp}.png"

    try:
        browser.save_screenshot(str(screenshot_path))
        allure.attach.file(
            str(screenshot_path),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            browser.page_source,
            name="page-source",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as exc:  # pragma: no cover - defensive reporting path
        print(f"Could not capture failure artifact: {exc}")
