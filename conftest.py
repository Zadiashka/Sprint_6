# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os

@pytest.fixture(scope="function")
def driver():
    gecko_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "geckodriver.exe"))
    # если положил в корень проекта, gecko_path = "./geckodriver.exe"
    service = Service(executable_path=gecko_path)
    options = Options()
    options.add_argument("--width=1280")
    options.add_argument("--height=800")
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
