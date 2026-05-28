from __future__ import annotations

from pathlib import Path
from typing import Iterable

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains, Keys, Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Shared Selenium primitives with explicit waits and readable assertions."""

    def __init__(self, driver: Remote, base_url: str, timeout: int = 12) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def open(self, path: str = "") -> None:
        self.driver.get(f"{self.base_url}/{path.lstrip('/')}")

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def title(self) -> str:
        return self.driver.title

    def wait_visible(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))

    def wait_present(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def wait_clickable(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator: tuple[str, str]) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(EC.invisibility_of_element_located(locator))

    def wait_text(self, locator: tuple[str, str], expected_text: str) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.text_to_be_present_in_element(locator, expected_text)
        )

    def wait_url_contains(self, fragment: str) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(EC.url_contains(fragment))

    def click(self, locator: tuple[str, str]) -> None:
        self.wait_clickable(locator).click()

    def type(self, locator: tuple[str, str], value: str, clear: bool = True) -> None:
        element = self.wait_visible(locator)
        if clear:
            element.clear()
        element.send_keys(value)

    def press(self, locator: tuple[str, str], key: str | Keys) -> None:
        self.wait_visible(locator).send_keys(key)

    def text_of(self, locator: tuple[str, str]) -> str:
        return self.wait_visible(locator).text.strip()

    def value_of(self, locator: tuple[str, str]) -> str:
        return self.wait_visible(locator).get_attribute("value") or ""

    def find_all(self, locator: tuple[str, str]) -> list[WebElement]:
        self.wait_present(locator)
        return list(self.driver.find_elements(*locator))

    def is_visible(self, locator: tuple[str, str]) -> bool:
        try:
            return self.wait_visible(locator).is_displayed()
        except TimeoutException:
            return False

    def select_by_visible_text(self, locator: tuple[str, str], text: str) -> None:
        Select(self.wait_visible(locator)).select_by_visible_text(text)

    def selected_text(self, locator: tuple[str, str]) -> str:
        return Select(self.wait_visible(locator)).first_selected_option.text.strip()

    def select_options(self, locator: tuple[str, str]) -> list[str]:
        return [option.text.strip() for option in Select(self.wait_visible(locator)).options]

    def hover(self, element: WebElement) -> None:
        ActionChains(self.driver).move_to_element(element).perform()

    def upload_file(self, locator: tuple[str, str], file_path: Path) -> None:
        self.wait_present(locator).send_keys(str(file_path.resolve()))

    def switch_to_newest_window(self, existing_handles: Iterable[str]) -> None:
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: len(set(d.window_handles) - set(existing_handles)) == 1
        )
        new_handle = (set(self.driver.window_handles) - set(existing_handles)).pop()
        self.driver.switch_to.window(new_handle)

    def body_text(self) -> str:
        return self.wait_visible((By.TAG_NAME, "body")).text
