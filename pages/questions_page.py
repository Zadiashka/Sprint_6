from selenium.webdriver.common.by import By
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
        # клик по заголовку внутри элемента
        heading = items[index].find_element(*self.QUESTION_HEADING)
        heading.click()

    def get_answer_text_by_index(self, index: int) -> str:
        panels = self.find_all(self.ANSWER_PANEL)
        if index < 0 or index >= len(panels):
            raise IndexError("Answer index out of range")
        return panels[index].text
