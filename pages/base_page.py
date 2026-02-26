# pages/base_page.py
import logging
from typing import List, Optional, Tuple, Callable, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class BasePage:
    def __init__(self, driver: WebDriver, default_timeout: int = 8):
        self._driver = driver
        self._timeout = default_timeout

    def open(self, url: str) -> None:
        self._driver.get(url)

    def wait_for(self, condition: Callable[[WebDriver], Any], timeout: Optional[int] = None) -> Any:
        wait = WebDriverWait(self._driver, timeout or self._timeout)
        return wait.until(condition)

    def find(self, locator: Tuple, timeout: Optional[int] = None) -> WebElement:
        wait = WebDriverWait(self._driver, timeout or self._timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: Tuple, timeout: Optional[int] = None) -> List[WebElement]:
        wait = WebDriverWait(self._driver, timeout or self._timeout)
        wait.until(lambda d: d.find_elements(*locator))
        return self._driver.find_elements(*locator)

    def wait_visible(self, locator: Tuple, timeout: Optional[int] = None) -> WebElement:
        wait = WebDriverWait(self._driver, timeout or self._timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: Tuple, timeout: Optional[int] = None) -> None:
        wait = WebDriverWait(self._driver, timeout or self._timeout)
        el = wait.until(EC.element_to_be_clickable(locator))
        self.click_element(el)

    def click_element(self, el: WebElement) -> None:
        """
        Try several click strategies. If all fail, raise the last exception.
        """
        last_exc = None

        # try scroll into view
        try:
            self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            logger.debug("scrollIntoView failed", exc_info=True)

        # try ActionChains click
        try:
            ActionChains(self._driver).move_to_element(el).pause(0.05).click(el).perform()
            return
        except Exception as e:
            last_exc = e
            logger.debug("ActionChains click failed", exc_info=True)

        # try direct click
        try:
            el.click()
            return
        except Exception as e:
            last_exc = e
            logger.debug("Direct element.click failed", exc_info=True)

        # try JS click
        try:
            self._driver.execute_script("arguments[0].click();", el)
            return
        except Exception as e:
            last_exc = e
            logger.exception("All click attempts failed")

        # if we reach here, raise the last exception
        if last_exc:
            raise last_exc

    def fill(self, locator: Tuple, text: str, timeout: Optional[int] = None) -> None:
        el = self.find(locator, timeout=timeout)
        try:
            el.clear()
        except Exception:
            logger.debug("clear() failed", exc_info=True)
        el.send_keys(text)

    def save_artifacts(self, name_prefix: str) -> None:
        try:
            self._driver.save_screenshot(f"{name_prefix}.png")
        except Exception:
            logger.debug("Failed to save screenshot", exc_info=True)
        try:
            with open(f"{name_prefix}.html", "w", encoding="utf-8") as f:
                f.write(self._driver.page_source)
        except Exception:
            logger.debug("Failed to save page source", exc_info=True)
