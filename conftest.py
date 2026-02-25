# conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def _is_headless() -> bool:
    return os.getenv("HEADLESS", "1").strip() in ("1", "true", "True")

def _browser_choice(request) -> str:
    opt = request.config.getoption("--browser")
    env = os.getenv("BROWSER", "").strip().lower()
    return (opt or env or "firefox").lower()

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None, help="chrome or firefox")

@pytest.fixture(scope="function")
def driver(request):
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

    if browser == "chrome":
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,800")
        try:
            drv = webdriver.Chrome(options=options)
        except Exception as exc:
            raise RuntimeError("Не удалось создать Chrome WebDriver. Убедитесь, что chromedriver в PATH.") from exc
    else:
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        options = FirefoxOptions()
        if headless:
            options.headless = True
        try:
            drv = webdriver.Firefox(options=options)
            drv.set_window_size(1280, 800)
        except Exception as exc:
            raise RuntimeError("Не удалось создать Firefox WebDriver. Убедитесь, что geckodriver и Firefox установлены в раннере.") from exc

    yield drv

    try:
        drv.quit()
    except Exception:
        pass
