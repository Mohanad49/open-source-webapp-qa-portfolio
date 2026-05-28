from __future__ import annotations

from pathlib import Path

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HoversPage(BasePage):
    FIGURES = (By.CSS_SELECTOR, ".figure")

    def load(self) -> "HoversPage":
        self.open("/hovers")
        return self

    def reveal_caption(self, one_based_index: int) -> tuple[str, str]:
        figure = self.find_all(self.FIGURES)[one_based_index - 1]
        self.hover(figure)
        caption = figure.find_element(By.CSS_SELECTOR, ".figcaption")
        name = caption.find_element(By.TAG_NAME, "h5").text.strip()
        link = caption.find_element(By.TAG_NAME, "a").get_attribute("href") or ""
        return name, link


class TablesPage(BasePage):
    TABLE_TWO_ROWS = (By.CSS_SELECTOR, "#table2 tbody tr")
    TABLE_TWO_HEADERS = (By.CSS_SELECTOR, "#table2 thead th")

    def load(self) -> "TablesPage":
        self.open("/tables")
        return self

    def headers(self) -> list[str]:
        return [header.text.strip() for header in self.find_all(self.TABLE_TWO_HEADERS)]

    def rows(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for row in self.find_all(self.TABLE_TWO_ROWS):
            result.append(
                {
                    "last_name": row.find_element(By.CSS_SELECTOR, ".last-name").text.strip(),
                    "first_name": row.find_element(By.CSS_SELECTOR, ".first-name").text.strip(),
                    "email": row.find_element(By.CSS_SELECTOR, ".email").text.strip(),
                    "dues": row.find_element(By.CSS_SELECTOR, ".dues").text.strip(),
                    "website": row.find_element(By.CSS_SELECTOR, ".web-site").text.strip(),
                    "actions": row.find_element(By.CSS_SELECTOR, ".action").text.strip(),
                }
            )
        return result

    def sort_by_header(self, header_text: str) -> None:
        self.click((By.XPATH, f"//table[@id='table2']//th[normalize-space()='{header_text}']"))


class JavaScriptAlertsPage(BasePage):
    RESULT = (By.ID, "result")

    def load(self) -> "JavaScriptAlertsPage":
        self.open("/javascript_alerts")
        return self

    def click_alert_button(self, label: str) -> Alert:
        self.click((By.XPATH, f"//button[normalize-space()='{label}']"))
        return self.driver.switch_to.alert

    def result(self) -> str:
        return self.text_of(self.RESULT)


class WindowsPage(BasePage):
    CLICK_HERE = (By.LINK_TEXT, "Click Here")
    NEW_WINDOW_HEADING = (By.CSS_SELECTOR, "h3")

    def load(self) -> "WindowsPage":
        self.open("/windows")
        return self

    def open_new_window(self) -> str:
        existing = self.driver.window_handles
        self.click(self.CLICK_HERE)
        self.switch_to_newest_window(existing)
        return self.text_of(self.NEW_WINDOW_HEADING)


class FileUploadPage(BasePage):
    FILE_INPUT = (By.ID, "file-upload")
    SUBMIT = (By.ID, "file-submit")
    HEADING = (By.CSS_SELECTOR, "#content h3")
    UPLOADED_FILES = (By.ID, "uploaded-files")

    def load(self) -> "FileUploadPage":
        self.open("/upload")
        return self

    def upload(self, file_path: Path) -> tuple[str, str]:
        self.upload_file(self.FILE_INPUT, file_path)
        self.click(self.SUBMIT)
        return self.text_of(self.HEADING), self.text_of(self.UPLOADED_FILES)


class StatusCodesPage(BasePage):
    def load_code(self, code: int) -> "StatusCodesPage":
        self.open(f"/status_codes/{code}")
        return self

    def status_message(self) -> str:
        return self.body_text()
