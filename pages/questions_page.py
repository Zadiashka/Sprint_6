# pages/questions_page.py
import allure
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .base_page import BasePage

class QuestionsPage(BasePage):
    QUESTION = (By.XPATH, "//div[contains(@id, 'accordion__heading-')]")
    ANSWER = (By.XPATH, "//div[contains(@id, 'accordion__panel-')]//p")
    QUESTIONS_SECTION = (By.CSS_SELECTOR, "div.Home_FAQ__3uVm4")

    def _collect_questions(self) -> List[WebElement]:
        return self.find_all(self.QUESTION, timeout=5)

    def _collect_answers(self) -> List[WebElement]:
        return self.find_all(self.ANSWER, timeout=5)

    @allure.step("Open question by index {index}")
    def open_question_by_index(self, index: int) -> None:
        questions = self._collect_questions()
        if index < 0 or index >= len(questions):
            raise IndexError("Question index out of range")
        q = questions[index]
        self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", q)
        self.click_element(q)
        def _answer_visible(d):
            answers = d.find_elements(*self.ANSWER)
            return len(answers) > index and (answers[index].text or "").strip() != ""
        self.wait_for(_answer_visible, timeout=6)

    @allure.step("Get answer text by index {index}")
    def get_answer_text_by_index(self, index: int) -> str:
        answers = self._collect_answers()
        if index < 0 or index >= len(answers):
            raise IndexError("Answer index out of range")
        return (answers[index].text or "").strip()
