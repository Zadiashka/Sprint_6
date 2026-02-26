
import os
from typing import Optional
import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as GeckoService

def _is_headless() -> bool:
    return os.getenv("HEADLESS", "1").strip().lower() in ("1", "true", "yes")

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None, help="chrome or firefox")

def _browser_choice(request) -> str:
    opt = request.config.getoption("--browser")
    env = os.getenv("BROWSER", "").strip().lower()
    return (opt or env or "firefox").lower()

@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture that returns a Selenium WebDriver.
    - By default creates a local Firefox driver.
    - Honors HEADLESS env var (1/true/yes -> headless).
    - If SELENIUM_REMOTE_URL is set, uses webdriver.Remote instead.
    """
    remote_url = os.getenv("SELENIUM_REMOTE_URL", "").strip()
    browser = _browser_choice(request)
    headless = _is_headless()

    if remote_url:
        
        if browser == "chrome":
            caps = DesiredCapabilities.CHROME.copy()
        else:
            caps = DesiredCapabilities.FIREFOX.copy()
        caps["goog:loggingPrefs"] = {"browser": "ALL"}
        drv = webdriver.Remote(command_executor=remote_url, desired_capabilities=caps)
        try:
            drv.set_window_size(1280, 800)
        except Exception:
            pass
        yield drv
        try:
            drv.quit()
        except Exception:
            pass
        return

    
    if browser != "firefox":
        raise RuntimeError("This conftest is configured for Firefox by default. Set BROWSER=firefox or remove --browser.")

    options = FirefoxOptions()
    if headless:
        
        options.add_argument("-headless")
    
    options.set_preference("dom.webnotifications.enabled", False)

    
    gecko_log = os.getenv("GECKODRIVER_LOG", "geckodriver.log")
    service = GeckoService(log_output=gecko_log)

    try:
        drv = webdriver.Firefox(service=service, options=options)
    except Exception as exc:
        raise RuntimeError("Не удалось создать Firefox WebDriver. Убедитесь, что geckodriver и Firefox установлены и доступны в PATH.") from exc

    try:
        drv.set_window_size(1280, 800)
    except Exception:
        pass

    yield drv

    try:
        drv.quit()
    except Exception:
        pass
