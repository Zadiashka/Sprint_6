# tests/test_questions.py
import pytest
import allure
from pages.main_page import MainPage
from pages.questions_page import QuestionsPage

EXPECTED_ANSWERS = [
    "Сутки — 400 рублей. Оплата курьеру — наличными или картой.",
    "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим.",
    "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30.",
    "Только начиная с завтрашнего дня. Но скоро станем расторопнее.",
    "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010.",
    "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится.",
    "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои.",
    "Да, обязательно. Всем самокатов! И Москве, и Московской области.",
]

@pytest.mark.usefixtures("driver")
class TestQuestions:
    @allure.title("FAQ question opens and shows correct answer")
    @pytest.mark.parametrize("index", list(range(8)))
    def test_question_opens(self, driver, index):
        main = MainPage(driver)
        main.open_main()
        main.accept_cookies()
        main.open_questions_section(timeout=6)
        page = QuestionsPage(driver)
        page.open_question_by_index(index)
        answer = page.get_answer_text_by_index(index)
        assert answer == EXPECTED_ANSWERS[index]