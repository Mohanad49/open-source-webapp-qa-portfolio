from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AddRemoveElementsPage(BasePage):
    ADD_BUTTON = (By.CSS_SELECTOR, "button[onclick='addElement()']")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "button.added-manually")

    def load(self) -> "AddRemoveElementsPage":
        self.open("/add_remove_elements/")
        return self

    def add(self, count: int = 1) -> None:
        for _ in range(count):
            self.click(self.ADD_BUTTON)

    def delete_first(self) -> None:
        self.find_all(self.DELETE_BUTTONS)[0].click()

    def delete_all(self) -> None:
        for button in list(self.find_all(self.DELETE_BUTTONS)):
            button.click()

    def delete_count(self) -> int:
        return len(self.driver.find_elements(*self.DELETE_BUTTONS))
