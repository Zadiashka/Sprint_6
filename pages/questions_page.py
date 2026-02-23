from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

class QuestionsPage:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")
    QUESTION_ITEMS = (By.CSS_SELECTOR, "div.accordion__item")
    QUESTION_BUTTON = (By.CSS_SELECTOR, "div.accordion__button")
    ANSWER_PANEL = (By.CSS_SELECTOR, "div.accordion__panel")
    OVERLAY_IMAGE = (By.CSS_SELECTOR, 'img[src="/assets/scooter.png"]')

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.BASE_URL)

    def accept_cookies(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.COOKIE_BUTTON))
            btn.click()
            self.wait.until(EC.invisibility_of_element_located(self.COOKIE_BUTTON))
        except TimeoutException:
            pass

    def _get_items(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.QUESTION_ITEMS))

    def _wait_overlay_gone(self, timeout: int = 5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(self.OVERLAY_IMAGE))
        except TimeoutException:
            try:
                overlay = self.driver.find_element(*self.OVERLAY_IMAGE)
                self.driver.execute_script("arguments[0].style.pointerEvents='none'; arguments[0].style.visibility='hidden';", overlay)
            except NoSuchElementException:
                pass

    def open_question(self, index: int):
        items = self._get_items()
        if index < 0 or index >= len(items):
            raise IndexError("Question index out of range")
        button = items[index].find_element(*self.QUESTION_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        self._wait_overlay_gone(timeout=3)
        try:
            button.click()
            return
        except ElementClickInterceptedException:
            try:
                self.driver.execute_script("arguments[0].click();", button)
                return
            except Exception:
                try:
                    overlay = self.driver.find_element(*self.OVERLAY_IMAGE)
                    self.driver.execute_script("arguments[0].remove();", overlay)
                except Exception:
                    pass
                try:
                    button.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", button)

    def is_answer_visible(self, index: int) -> bool:
        items = self._get_items()
        if index < 0 or index >= len(items):
            raise IndexError("Question index out of range")
        panel = items[index].find_element(*self.ANSWER_PANEL)
        try:
            return self.wait.until(EC.visibility_of(panel)) is not None
        except TimeoutException:
            return False

    def get_question_text(self, index: int) -> str:
        items = self._get_items()
        if index < 0 or index >= len(items):
            raise IndexError("Question index out of range")
        return items[index].find_element(*self.QUESTION_BUTTON).text.strip()

    def get_answer_text(self, index: int) -> str:
        items = self._get_items()
        if index < 0 or index >= len(items):
            raise IndexError("Question index out of range")
        panel = items[index].find_element(*self.ANSWER_PANEL)
        return panel.text.strip()
