from __future__ import annotations

import allure
import pytest

from pages.add_remove_page import AddRemoveElementsPage


@allure.epic("Open-source web app QA portfolio")
@allure.feature("Add/remove elements")
@pytest.mark.regression
class TestAddRemoveElements:
    def test_delete_buttons_are_absent_initially(self, driver, base_url, timeout):
        page = AddRemoveElementsPage(driver, base_url, timeout).load()

        assert page.delete_count() == 0

    @pytest.mark.smoke
    def test_user_can_add_one_delete_button(self, driver, base_url, timeout):
        page = AddRemoveElementsPage(driver, base_url, timeout).load()
        page.add()

        assert page.delete_count() == 1

    @pytest.mark.parametrize("count", [2, 5, 10])
    def test_user_can_add_multiple_delete_buttons(self, driver, base_url, timeout, count):
        page = AddRemoveElementsPage(driver, base_url, timeout).load()
        page.add(count)

        assert page.delete_count() == count

    def test_user_can_delete_first_added_button(self, driver, base_url, timeout):
        page = AddRemoveElementsPage(driver, base_url, timeout).load()
        page.add(3)
        page.delete_first()

        assert page.delete_count() == 2

    def test_user_can_clear_all_added_buttons(self, driver, base_url, timeout):
        page = AddRemoveElementsPage(driver, base_url, timeout).load()
        page.add(4)
        page.delete_all()

        assert page.delete_count() == 0
