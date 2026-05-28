from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH = (By.ID, "flash")
    SECURE_HEADING = (By.CSS_SELECTOR, "#content h2")
    LOGOUT = (By.CSS_SELECTOR, "a.button.secondary.radius")

    def load(self) -> "LoginPage":
        self.open("/login")
        return self

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def flash_message(self) -> str:
        return self.text_of(self.FLASH)

    def secure_heading(self) -> str:
        return self.text_of(self.SECURE_HEADING)

    def logout(self) -> None:
        self.click(self.LOGOUT)
