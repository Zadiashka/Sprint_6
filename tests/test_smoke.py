# tests/test_smoke.py
import pytest
import allure
from pages.main_page import MainPage
from config import BASE_URL

@pytest.mark.usefixtures("driver")
class TestSmoke:
    @allure.title("Scooter logo navigates to home")
    def test_scooter_logo_navigates_home(self, driver):
        main = MainPage(driver)
        main.open_main()
        main.accept_cookies()
        main.click(MainPage.LOGO_SCOOTER)
        main.wait_for(lambda d: BASE_URL in (main.get_current_url() or ""), timeout=6)
        assert BASE_URL in main.get_current_url()

    @allure.title("Yandex logo opens Dzen in new window")
    def test_yandex_logo_opens_dzen(self, driver):
        main = MainPage(driver)
        main.open_main()
        main.accept_cookies()
        yel = main.find(MainPage.LOGO_YANDEX, timeout=5)
        main.click_element(yel)
        main.wait_for(lambda d: len(main.get_window_handles()) > 1, timeout=8)
        main.switch_to_window(main.get_window_handles()[-1])
        main.wait_for(lambda d: "dzen.ru" in main.get_current_url().lower(), timeout=8)
        assert "dzen.ru" in main.get_current_url().lower()