from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    HEADING = (By.CSS_SELECTOR, "h1.heading")
    SUBHEADING = (By.CSS_SELECTOR, "h2")
    EXAMPLE_LINKS = (By.CSS_SELECTOR, "#content ul li a")

    def load(self) -> "HomePage":
        self.open("/")
        return self

    def heading(self) -> str:
        return self.text_of(self.HEADING)

    def subheading(self) -> str:
        return self.text_of(self.SUBHEADING)

    def example_names(self) -> list[str]:
        return [link.text.strip() for link in self.find_all(self.EXAMPLE_LINKS)]

    def href_for(self, link_text: str) -> str:
        locator = (By.LINK_TEXT, link_text)
        return self.wait_visible(locator).get_attribute("href") or ""

    def open_example(self, link_text: str) -> None:
        self.click((By.LINK_TEXT, link_text))
