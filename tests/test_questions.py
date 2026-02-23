import pytest
from pages.questions_page import QuestionsPage

@pytest.mark.parametrize("index", [0, 1, 2, 3, 4, 5])
def test_question_opens(driver, index):
    page = QuestionsPage(driver)
    page.open()
    page.accept_cookies()
    page.open_question(index)
    assert page.is_answer_visible(index)
