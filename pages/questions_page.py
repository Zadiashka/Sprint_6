# pages/questions_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class QuestionsPage(BasePage):
    QUESTIONS = (By.CSS_SELECTOR, "div.Home_FAQ__3uVm4 .accordion__item")
    QUESTION_TOGGLE = (By.CSS_SELECTOR, ".accordion__heading")
    ANSWER_PANEL = (By.CSS_SELECTOR, ".accordion__panel")

    def open_question_by_index(self, index: int) -> None:
        questions = self.find_all(self.QUESTIONS, timeout=5)
        if index < 0 or index >= len(questions):
            raise IndexError("Question index out of range")
        q = questions[index]
        self.scroll_into_view(q)
        toggle = q.find_element(*self.QUESTION_TOGGLE)
        self.click_element(toggle)
        WebDriverWait(self._driver, 5).until(
            lambda d: q.find_elements(*self.ANSWER_PANEL)
        )

    def get_answer_text_by_index(self, index: int) -> str:
        questions = self.find_all(self.QUESTIONS, timeout=5)
        if index < 0 or index >= len(questions):
            raise IndexError("Question index out of range")
        panel = questions[index].find_element(*self.ANSWER_PANEL)
        raw = panel.text or ""
        return " ".join(raw.split()).strip()