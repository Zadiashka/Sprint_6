# pages/questions_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class QuestionsPage(BasePage):
    QUESTIONS_CONTAINER = (By.CSS_SELECTOR, "div.Home_FAQ__3uVm4")
    QUESTION_ITEM = (By.CSS_SELECTOR, ".accordion__item")
    QUESTION_HEADING = (By.CSS_SELECTOR, ".accordion__button")
    ANSWER_PANEL = (By.CSS_SELECTOR, ".accordion__panel")
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")

    def accept_cookies(self) -> None:
        self.click(self.COOKIE_BUTTON)

    def open_question_by_index(self, index: int) -> None:
        items = self.find_all(self.QUESTION_ITEM)
        if index < 0 or index >= len(items):
            raise IndexError("Question index out of range")
        heading: WebElement = items[index].find_element(*self.QUESTION_HEADING)
        # Надёжный клик: используем BasePage.click_element
        try:
            self.click_element(heading)
            # дождёмся появления панели ответа для этого индекса (best-effort)
            WebDriverWait(self._driver, 4).until(
                lambda d: len(d.find_elements(*self.ANSWER_PANEL)) > index and d.find_elements(*self.ANSWER_PANEL)[index].is_displayed()
            )
        except TimeoutException:
            # если элемент перекрыт (например картинкой), попробуем JS-клик и повторную проверку
            try:
                self._driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", heading)
                WebDriverWait(self._driver, 3).until(
                    lambda d: len(d.find_elements(*self.ANSWER_PANEL)) > index and d.find_elements(*self.ANSWER_PANEL)[index].is_displayed()
                )
            except Exception:
                # сохраняем артефакты для диагностики и пробрасываем ошибку
                try:
                    self.save_artifacts(f"question_{index}_click_failure")
                except Exception:
                    pass
                raise

    def get_answer_text_by_index(self, index: int) -> str:
        panels = self.find_all(self.ANSWER_PANEL)
        if index < 0 or index >= len(panels):
            raise IndexError("Answer index out of range")
        return panels[index].text
