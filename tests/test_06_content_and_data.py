from __future__ import annotations

import allure
import pytest

from pages.content_pages import HoversPage, StatusCodesPage, TablesPage
from utils.test_data import STATUS_CODES


@allure.epic("Open-source web app QA portfolio")
@allure.feature("Content and data validation")
@pytest.mark.regression
class TestContentAndData:
    @pytest.mark.parametrize("user_number", [1, 2, 3])
    def test_hover_card_reveals_expected_user_profile(self, driver, base_url, timeout, user_number):
        page = HoversPage(driver, base_url, timeout).load()
        name, link = page.reveal_caption(user_number)

        assert name == f"name: user{user_number}"
        assert link.endswith(f"/users/{user_number}")

    @pytest.mark.tables
    def test_table_exposes_expected_headers(self, driver, base_url, timeout):
        page = TablesPage(driver, base_url, timeout).load()

        assert page.headers() == ["Last Name", "First Name", "Email", "Due", "Web Site", "Action"]

    @pytest.mark.tables
    def test_table_contains_known_customer_record(self, driver, base_url, timeout):
        page = TablesPage(driver, base_url, timeout).load()

        assert {
            "last_name": "Smith",
            "first_name": "John",
            "email": "jsmith@gmail.com",
            "dues": "$50.00",
            "website": "http://www.jsmith.com",
            "actions": "edit delete",
        } in page.rows()

    @pytest.mark.tables
    def test_table_dues_values_use_currency_format(self, driver, base_url, timeout):
        page = TablesPage(driver, base_url, timeout).load()

        assert all(row["dues"].startswith("$") for row in page.rows())

    @pytest.mark.tables
    def test_table_email_values_are_valid_email_like_strings(self, driver, base_url, timeout):
        page = TablesPage(driver, base_url, timeout).load()

        assert all("@" in row["email"] and "." in row["email"] for row in page.rows())

    @pytest.mark.tables
    @pytest.mark.parametrize("header", ["Last Name", "First Name", "Email", "Due"])
    def test_table_headers_are_sortable(self, driver, base_url, timeout, header):
        page = TablesPage(driver, base_url, timeout).load()
        before = page.rows()
        page.sort_by_header(header)
        after = page.rows()

        assert after != before

    @pytest.mark.parametrize("status_code", STATUS_CODES)
    def test_status_code_page_explains_returned_code(self, driver, base_url, timeout, status_code):
        page = StatusCodesPage(driver, base_url, timeout).load_code(status_code)

        assert f"This page returned a {status_code} status code." in page.status_message()
