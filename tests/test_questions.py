# tests/test_questions.py
import pytest
from pages.main_page import MainPage
from pages.questions_page import QuestionsPage

@pytest.mark.usefixtures("driver")
class TestQuestions:
    @pytest.mark.parametrize("index", [0, 1, 2, 3, 4, 5])
    def test_question_opens(self, driver, index):
        main = MainPage(driver)
        main.open_main()

        main.accept_cookies()

        main.open_questions_section(timeout=6)

        page = QuestionsPage(driver)
        page.open_question_by_index(index)

        answer = page.get_answer_text_by_index(index)
        assert answer and answer.strip() != "", f"Answer for question {index} should not be empty"
