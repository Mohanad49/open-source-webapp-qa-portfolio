from __future__ import annotations

import allure
import pytest

from pages.dynamic_pages import DynamicControlsPage, DynamicLoadingPage


@allure.epic("Open-source web app QA portfolio")
@allure.feature("Dynamic behaviour")
@pytest.mark.dynamic
class TestDynamicBehaviour:
    def test_dynamic_checkbox_can_be_removed(self, driver, base_url, timeout):
        page = DynamicControlsPage(driver, base_url, timeout).load()
        page.remove_checkbox()

        assert "It's gone!" in page.message()

    def test_dynamic_checkbox_can_be_added_back(self, driver, base_url, timeout):
        page = DynamicControlsPage(driver, base_url, timeout).load()
        page.remove_checkbox()
        page.add_checkbox()

        assert "It's back!" in page.message()

    @pytest.mark.smoke
    def test_disabled_input_can_be_enabled_and_used(self, driver, base_url, timeout):
        page = DynamicControlsPage(driver, base_url, timeout).load()
        page.enable_input()

        assert page.input_enabled() is True
        assert page.type_into_input("release-ready") == "release-ready"

    def test_enabled_input_can_be_disabled_again(self, driver, base_url, timeout):
        page = DynamicControlsPage(driver, base_url, timeout).load()
        page.enable_input()
        page.disable_input()

        assert page.input_enabled() is False
        assert "It's disabled!" in page.message()

    @pytest.mark.parametrize("example_number", [1, 2])
    def test_dynamic_loading_examples_reveal_hello_world(self, driver, base_url, timeout, example_number):
        page = DynamicLoadingPage(driver, base_url, timeout).load_example(example_number)

        assert page.reveal_text() == "Hello World!"
