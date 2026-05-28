from __future__ import annotations

import allure
import pytest

from pages.home_page import HomePage
from utils.test_data import NAVIGATION_EXAMPLES


@allure.epic("Open-source web app QA portfolio")
@allure.feature("Home and navigation")
@pytest.mark.smoke
class TestHomeNavigation:
    def test_home_page_has_expected_branding(self, driver, base_url, timeout):
        home = HomePage(driver, base_url, timeout).load()

        assert home.title == "The Internet"
        assert home.heading() == "Welcome to the-internet"
        assert home.subheading() == "Available Examples"

    def test_home_page_exposes_large_acceptance_test_catalog(self, driver, base_url, timeout):
        home = HomePage(driver, base_url, timeout).load()

        assert len(home.example_names()) >= 40

    @pytest.mark.parametrize("link_text, expected_path", NAVIGATION_EXAMPLES)
    def test_key_example_link_points_to_expected_path(self, driver, base_url, timeout, link_text, expected_path):
        home = HomePage(driver, base_url, timeout).load()

        assert home.href_for(link_text).endswith(expected_path)

    @pytest.mark.parametrize(
        "link_text, expected_path",
        [
            ("Add/Remove Elements", "/add_remove_elements/"),
            ("Checkboxes", "/checkboxes"),
            ("Form Authentication", "/login"),
        ],
    )
    def test_selected_example_links_open_their_pages(self, driver, base_url, timeout, link_text, expected_path):
        home = HomePage(driver, base_url, timeout).load()
        home.open_example(link_text)

        assert driver.current_url.endswith(expected_path)
