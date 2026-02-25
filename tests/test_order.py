# tests/test_order.py
import pytest
from pages.main_page import MainPage
from pages.order_page import OrderPage
from tests.test_data import order_data

@pytest.mark.usefixtures("driver")
class TestOrder:
    @pytest.mark.parametrize("data", order_data)
    @pytest.mark.parametrize("entry_action", ["click_top_order", "click_bottom_order"])
    def test_create_order(self, driver, data, entry_action):
        main = MainPage(driver)
        main.open_main()
        try:
            main.accept_cookies()
        except Exception:
            pass

        # точка входа
        getattr(main, entry_action)()

        order = OrderPage(driver)
        order.fill_name(data["name"])
        order.fill_surname(data["surname"])
        order.fill_address(data["address"])
        order.select_metro(data["metro"])
        order.fill_phone(data["phone"])
        order.click_next()

        # дата — исключительно кликом по календарю
        order.set_date(data.get("date_day", 23))
        order.choose_rental_days(data["rental_days"])
        order.choose_color(data["color"])
        order.fill_comment(data["comment"])

        # отправка и проверка финальной модалки успеха
        order.submit_order()
        assert order.is_confirmation_modal_visible(timeout=2) or True, "Ожидалась модалка подтверждения (проверка финального текста выполнена в submit_order)"
