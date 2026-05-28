from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
DOWNLOADS_DIR = ROOT_DIR / "downloads"
ASSETS_DIR = ROOT_DIR / "assets"


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for the UI automation suite."""

    base_url: str = os.getenv("BASE_URL", "https://the-internet.herokuapp.com").rstrip("/")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes", "y"}
    timeout: int = int(os.getenv("TIMEOUT", "12"))
    slow_mo: float = float(os.getenv("SLOW_MO", "0"))
    screenshot_on_fail: bool = os.getenv("SCREENSHOT_ON_FAIL", "true").lower() in {
        "1",
        "true",
        "yes",
        "y",
    }


settings = Settings()
