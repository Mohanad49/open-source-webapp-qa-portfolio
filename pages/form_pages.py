from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckboxesPage(BasePage):
    CHECKBOXES = (By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")

    def load(self) -> "CheckboxesPage":
        self.open("/checkboxes")
        return self

    def states(self) -> list[bool]:
        return [box.is_selected() for box in self.find_all(self.CHECKBOXES)]

    def toggle(self, zero_based_index: int) -> bool:
        box = self.find_all(self.CHECKBOXES)[zero_based_index]
        box.click()
        return box.is_selected()


class DropdownPage(BasePage):
    DROPDOWN = (By.ID, "dropdown")

    def load(self) -> "DropdownPage":
        self.open("/dropdown")
        return self

    def choose(self, visible_text: str) -> None:
        self.select_by_visible_text(self.DROPDOWN, visible_text)

    def selected(self) -> str:
        return self.selected_text(self.DROPDOWN)

    def options(self) -> list[str]:
        return self.select_options(self.DROPDOWN)


class InputsPage(BasePage):
    NUMBER_INPUT = (By.CSS_SELECTOR, "input[type='number']")

    def load(self) -> "InputsPage":
        self.open("/inputs")
        return self

    def enter_value(self, value: str) -> str:
        self.type(self.NUMBER_INPUT, value)
        return self.value_of(self.NUMBER_INPUT)
