from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DynamicControlsPage(BasePage):
    CHECKBOX = (By.CSS_SELECTOR, "#checkbox-example input[type='checkbox']")
    REMOVE_ADD_BUTTON = (By.CSS_SELECTOR, "#checkbox-example button")
    INPUT = (By.CSS_SELECTOR, "#input-example input")
    ENABLE_DISABLE_BUTTON = (By.CSS_SELECTOR, "#input-example button")
    MESSAGE = (By.ID, "message")

    def load(self) -> "DynamicControlsPage":
        self.open("/dynamic_controls")
        return self

    def remove_checkbox(self) -> None:
        self.click(self.REMOVE_ADD_BUTTON)
        self.wait_invisible(self.CHECKBOX)

    def add_checkbox(self) -> None:
        self.click(self.REMOVE_ADD_BUTTON)
        self.wait_visible(self.CHECKBOX)

    def message(self) -> str:
        return self.text_of(self.MESSAGE)

    def enable_input(self) -> None:
        self.click(self.ENABLE_DISABLE_BUTTON)
        self.wait_text(self.MESSAGE, "enabled")

    def disable_input(self) -> None:
        self.click(self.ENABLE_DISABLE_BUTTON)
        self.wait_text(self.MESSAGE, "disabled")

    def input_enabled(self) -> bool:
        return self.wait_present(self.INPUT).is_enabled()

    def type_into_input(self, value: str) -> str:
        self.type(self.INPUT, value)
        return self.value_of(self.INPUT)


class DynamicLoadingPage(BasePage):
    START_BUTTON = (By.CSS_SELECTOR, "#start button")
    FINISH_TEXT = (By.CSS_SELECTOR, "#finish h4")

    def load_example(self, example_number: int) -> "DynamicLoadingPage":
        self.open(f"/dynamic_loading/{example_number}")
        return self

    def reveal_text(self) -> str:
        self.click(self.START_BUTTON)
        return self.text_of(self.FINISH_TEXT)
