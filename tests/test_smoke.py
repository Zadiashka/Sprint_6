
import pytest
from pages.main_page import MainPage

@pytest.mark.usefixtures("driver")
class TestSmoke:
    def test_main_page_has_order_buttons(self, driver):
        main = MainPage(driver)
        main.open_main()
        try:
            main.accept_cookies()
        except Exception:
            pass
        main.wait_visible(MainPage.TOP_ORDER, timeout=5)
        main.wait_visible(MainPage.BOTTOM_ORDER, timeout=5)
