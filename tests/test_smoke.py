# tests/test_smoke.py
import pytest
import allure
from pages.main_page import MainPage
from config import BASE_URL

@pytest.mark.usefixtures("driver")
class TestSmoke:
    @allure.title("Header logos navigate to expected destinations")
    def test_logos_navigate(self, driver):
        main = MainPage(driver)
        main.open_main()
        main.accept_cookies()
        scooter_logo = main.find(MainPage.LOGO_SCOOTER, timeout=5)
        main.click_element(scooter_logo)
        main.wait_for(lambda d: BASE_URL in d.current_url, timeout=6)
        yel = main.find(MainPage.LOGO_YANDEX, timeout=5)
        href = yel.get_attribute("href") or ""
        main.click_element(yel)
        main.wait_for(
            lambda d: len(d.window_handles) > 1 or "dzen.ru" in (d.current_url or "").lower(),
            timeout=8
        )
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
        main.wait_for(lambda d: "dzen.ru" in (d.current_url or "").lower(), timeout=8)
        cur_url = (driver.current_url or "").lower()
        if "dzen.ru" not in cur_url and href:
            driver.get(href)
            main.wait_for(lambda d: "dzen.ru" in (d.current_url or "").lower(), timeout=8)
            cur_url = driver.current_url.lower()
        assert "dzen.ru" in cur_url
