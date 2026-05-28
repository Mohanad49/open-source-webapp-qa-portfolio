from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage
from utils.test_data import INVALID_PASSWORD, INVALID_USER, VALID_PASSWORD, VALID_USER


@allure.epic("Open-source web app QA portfolio")
@allure.feature("Authentication")
@pytest.mark.auth
class TestAuthentication:
    @pytest.mark.smoke
    def test_valid_user_can_log_in(self, driver, base_url, timeout):
        login = LoginPage(driver, base_url, timeout).load()
        login.login(VALID_USER, VALID_PASSWORD)

        assert "secure" in login.current_url
        assert login.secure_heading() == "Secure Area"
        assert "You logged into a secure area!" in login.flash_message()

    def test_valid_user_can_log_out(self, driver, base_url, timeout):
        login = LoginPage(driver, base_url, timeout).load()
        login.login(VALID_USER, VALID_PASSWORD)
        login.logout()

        assert driver.current_url.endswith("/login")
        assert "You logged out of the secure area!" in login.flash_message()

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [
            (INVALID_USER, VALID_PASSWORD, "Your username is invalid!"),
            (VALID_USER, INVALID_PASSWORD, "Your password is invalid!"),
            ("", VALID_PASSWORD, "Your username is invalid!"),
            (VALID_USER, "", "Your password is invalid!"),
        ],
    )
    def test_invalid_credentials_show_actionable_error(
        self, driver, base_url, timeout, username, password, expected_message
    ):
        login = LoginPage(driver, base_url, timeout).load()
        login.login(username, password)

        assert expected_message in login.flash_message()

    def test_secure_area_requires_authenticated_session(self, driver, base_url, timeout):
        login = LoginPage(driver, base_url, timeout)
        login.open("/secure")

        assert driver.current_url.endswith("/login")
        assert "You must login to view the secure area!" in login.flash_message()
