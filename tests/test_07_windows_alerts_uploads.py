from __future__ import annotations

import allure
import pytest

from config.settings import ASSETS_DIR
from pages.content_pages import FileUploadPage, JavaScriptAlertsPage, WindowsPage


@allure.epic("Open-source web app QA portfolio")
@allure.feature("Browser-level interactions")
@pytest.mark.windows
class TestWindowsAlertsUploads:
    @pytest.mark.smoke
    def test_new_window_opens_expected_content(self, driver, base_url, timeout):
        page = WindowsPage(driver, base_url, timeout).load()

        assert page.open_new_window() == "New Window"

    def test_js_alert_accept_flow(self, driver, base_url, timeout):
        page = JavaScriptAlertsPage(driver, base_url, timeout).load()
        alert = page.click_alert_button("Click for JS Alert")
        alert.accept()

        assert page.result() == "You successfully clicked an alert"

    def test_js_confirm_cancel_flow(self, driver, base_url, timeout):
        page = JavaScriptAlertsPage(driver, base_url, timeout).load()
        alert = page.click_alert_button("Click for JS Confirm")
        alert.dismiss()

        assert page.result() == "You clicked: Cancel"

    def test_js_prompt_accept_flow_records_user_text(self, driver, base_url, timeout):
        page = JavaScriptAlertsPage(driver, base_url, timeout).load()
        alert = page.click_alert_button("Click for JS Prompt")
        alert.send_keys("QA evidence")
        alert.accept()

        assert page.result() == "You entered: QA evidence"

    @pytest.mark.upload
    @pytest.mark.smoke
    def test_file_upload_confirms_uploaded_filename(self, driver, base_url, timeout):
        page = FileUploadPage(driver, base_url, timeout).load()
        fixture_file = ASSETS_DIR / "upload_sample.txt"

        heading, uploaded_name = page.upload(fixture_file)

        assert heading == "File Uploaded!"
        assert uploaded_name == fixture_file.name
