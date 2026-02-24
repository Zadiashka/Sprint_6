import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def _create_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,800")
    # options.add_argument("--headless=new")  # включите для CI
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def _create_firefox():
    options = webdriver.FirefoxOptions()
    options.add_argument("--width=1280")
    options.add_argument("--height=800")
    # options.add_argument("-headless")  # включите для CI
    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)


@pytest.fixture(scope="function")
def driver(request):
    browser = os.getenv("BROWSER", "chrome").lower()
    if browser == "firefox":
        drv = _create_firefox()
    else:
        drv = _create_chrome()

    yield drv
    try:
        drv.quit()
    except Exception:
        pass
