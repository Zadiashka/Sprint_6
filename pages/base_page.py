# pages/base_page.py
from typing import Callable
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver: WebDriver):
        self._driver = driver

    def open(self, url: str) -> None:
        self._driver.get(url)

    def find(self, locator: tuple, timeout: float = 5):
        wait = WebDriverWait(self._driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: tuple, timeout: float = 5):
        wait = WebDriverWait(self._driver, timeout)
        return wait.until(lambda d: d.find_elements(*locator))

    def click(self, locator: tuple, timeout: float = 5) -> None:
        el = self.find(locator, timeout=timeout)
        self.click_element(el)

    def click_element(self, element) -> None:
        self.scroll_into_view(element)
        wait = WebDriverWait(self._driver, 5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*")))
        try:
            element.click()
        except Exception:
            self._driver.execute_script("arguments[0].click();", element)

    def scroll_into_view(self, element) -> None:
        self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def wait_visible(self, locator: tuple, timeout: float = 5):
        wait = WebDriverWait(self._driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for(self, condition: Callable, timeout: float = 5):
        wait = WebDriverWait(self._driver, timeout)
        return wait.until(condition)

    def fill(self, locator: tuple, text: str, clear: bool = True) -> None:
        el = self.find(locator)
        if clear:
            try:
                el.clear()
            except Exception:
                pass
        el.send_keys(text)

    def get_current_url(self) -> str:
        return self._driver.current_url

    def get_window_handles(self) -> list:
        return self._driver.window_handles

    def switch_to_window(self, handle: str) -> None:
        self._driver.switch_to.window(handle)