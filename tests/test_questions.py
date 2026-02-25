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

        try:
            main.accept_cookies()
        except Exception:
            pass

        # убедиться, что секция вопросов видима на странице
        main.wait_visible(MainPage.QUESTIONS_SECTION, timeout=5)

        page = QuestionsPage(driver)
        page.open_question_by_index(index)

        answer = page.get_answer_text_by_index(index)
        # при пустом ответе сохраняем артефакты для отладки и падаем с понятным сообщением
        if not answer or not answer.strip():
            page.save_artifacts(f"question_{index}_failure")
        assert answer and answer.strip() != "", f"Answer for question {index} should not be empty"
