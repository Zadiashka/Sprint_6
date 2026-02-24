from typing import Optional, Tuple, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


Locator = Tuple[By, str]


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self._driver = driver
        self._timeout = timeout
        self._wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self._driver.get(url)

    def find(self, locator: Locator, timeout: Optional[int] = None):
        wait = self._wait if timeout is None else WebDriverWait(self._driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: Locator, timeout: Optional[int] = None) -> List:
        wait = self._wait if timeout is None else WebDriverWait(self._driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: Locator, timeout: Optional[int] = None) -> None:
        wait = self._wait if timeout is None else WebDriverWait(self._driver, timeout)
        wait.until(EC.element_to_be_clickable(locator))
        el = self.find(locator, timeout)
        el.click()

    def fill(self, locator: Locator, text: str, timeout: Optional[int] = None) -> None:
        el = self.find(locator, timeout)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        el = self.find(locator, timeout)
        return el.text

    def wait_visible(self, locator: Locator, timeout: Optional[int] = None):
        wait = self._wait if timeout is None else WebDriverWait(self._driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_invisible(self, locator: Locator, timeout: Optional[int] = None):
        wait = self._wait if timeout is None else WebDriverWait(self._driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    @property
    def current_url(self) -> str:
        return self._driver.current_url
