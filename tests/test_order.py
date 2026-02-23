import pytest
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from pages.main_page import MainPage
from pages.order_page import OrderPage

order_data = [
    {"name":"Иван","surname":"Иванов","address":"ул. Пушкина, 1","metro":"Тверская","phone":"+79990001111","rental_days":"сутки","color":"чёрный жемчуг","comment":"Позвоните за 10 минут"},
    {"name":"Мария","surname":"Петрова","address":"ул. Ленина, 10","metro":"Пушкинская","phone":"+79990002222","rental_days":"двое суток","color":"серая безысходность","comment":""}
]

@pytest.mark.parametrize("entry_point", ["top","bottom"])
@pytest.mark.parametrize("data", order_data)
def test_create_order_positive(driver, entry_point, data):
    main = MainPage(driver)
    order = OrderPage(driver)
    main.open()
    order.accept_cookies()
    if entry_point == "top":
        main.click_top_order()
    else:
        main.click_bottom_order()
    order.fill_contact_info(data["name"], data["surname"], data["address"], data["metro"], data["phone"])
    target_date = datetime.now() + timedelta(days=1)
    order.choose_date(target_date)
    order.fill_rental_info(data["rental_days"], color=data["color"], comment=data["comment"])
    order.submit_order_and_confirm()
    main.click_logo_scooter()
    assert driver.current_url.startswith(MainPage.BASE_URL)
    main.open()
    order.accept_cookies()
    handles_before = driver.window_handles
    info = main.click_logo_yandex()
    href = info.get("href")
    target = info.get("target")
    assert href and ("yandex" in href or "dzen" in href)
    if target == "_blank":
        WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > len(handles_before))
        assert len(driver.window_handles) > len(handles_before)
