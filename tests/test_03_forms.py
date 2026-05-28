from __future__ import annotations

import allure
import pytest

from pages.form_pages import CheckboxesPage, DropdownPage, InputsPage
from utils.test_data import NUMERIC_INPUTS


@allure.epic("Open-source web app QA portfolio")
@allure.feature("Forms")
@pytest.mark.forms
class TestForms:
    @pytest.mark.smoke
    def test_checkboxes_have_expected_default_states(self, driver, base_url, timeout):
        page = CheckboxesPage(driver, base_url, timeout).load()

        assert page.states() == [False, True]

    @pytest.mark.parametrize("index, expected_state_after_toggle", [(0, True), (1, False)])
    def test_each_checkbox_can_be_toggled(
        self, driver, base_url, timeout, index, expected_state_after_toggle
    ):
        page = CheckboxesPage(driver, base_url, timeout).load()

        assert page.toggle(index) is expected_state_after_toggle

    def test_dropdown_starts_with_placeholder_option(self, driver, base_url, timeout):
        page = DropdownPage(driver, base_url, timeout).load()

        assert page.selected() == "Please select an option"

    def test_dropdown_exposes_two_real_business_options(self, driver, base_url, timeout):
        page = DropdownPage(driver, base_url, timeout).load()

        assert page.options() == ["Please select an option", "Option 1", "Option 2"]

    @pytest.mark.parametrize("option", ["Option 1", "Option 2"])
    def test_dropdown_selection_persists_in_control(self, driver, base_url, timeout, option):
        page = DropdownPage(driver, base_url, timeout).load()
        page.choose(option)

        assert page.selected() == option

    @pytest.mark.parametrize("number", NUMERIC_INPUTS)
    def test_numeric_input_accepts_business_number_values(self, driver, base_url, timeout, number):
        page = InputsPage(driver, base_url, timeout).load()

        assert page.enter_value(number) == number
