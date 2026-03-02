# pages/order_page.py
import allure
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

class OrderPage(BasePage):
    NAME = (By.CSS_SELECTOR, "input[placeholder='* Имя']")
    SURNAME = (By.CSS_SELECTOR, "input[placeholder='* Фамилия'], input[name='surname']")
    ADDRESS = (By.CSS_SELECTOR, "input[placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.CSS_SELECTOR, "div.select-search__value input.select-search__input, input[placeholder='* Станция метро'], input[name='metro']")
    METRO_OPTIONS = (By.CSS_SELECTOR, ".select-search__option, ul.select-search__options li, .select-search li")
    PHONE = (By.CSS_SELECTOR, "input[placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.CSS_SELECTOR, "button.Button_Button__ra12g.Button_Middle__1CSJM, button.Button_Middle__1CSJM")
    DATE_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Когда привезти самокат'], input[name='date'], input[type='date']")
    DATE_PICKER_CONTAINER = (By.CSS_SELECTOR, ".react-datepicker, .DatePicker, .Calendar")
    DATE_DAY_SELECTORS = [".react-datepicker__day", ".DatePicker-day", ".calendar-day", ".datepicker-day"]
    RENT_TERM_DROPDOWN = (By.CSS_SELECTOR, ".Dropdown-root, .Dropdown-control, .Dropdown")
    RENT_TERM_OPTION = (By.CSS_SELECTOR, ".Dropdown-menu div, .Dropdown-option")
    COLOR_CHECKBOXES = (By.CSS_SELECTOR, "div.Order_Checkboxes__3lWSI label")
    COMMENT_INPUT = (By.CSS_SELECTOR, "input[placeholder='Комментарий для курьера'], textarea[placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.CSS_SELECTOR, "button.Button_Button__ra12g.Button_Middle__1CSJM, button.Button_Middle__1CSJM")
    CONFIRM_MODAL = (By.CSS_SELECTOR, "div.Order_Modal__YZ-d3, .Order_Modal__title, .Order_ModalHeader__3FDaJ")
    CONFIRM_YES = (By.CSS_SELECTOR, "div.Order_Modal__YZ-d3 button:nth-child(2), button.Button_Button__ra12g.Button_Middle__1CSJM")
    ORDER_SUCCESS_TEXT = (By.CSS_SELECTOR, ".Order_ModalHeader__3FDaJ, .Order_Modal__title, .Order_ModalHeader")

    @allure.step("Fill name: {name}")
    def fill_name(self, name: str) -> None:
        self.fill(self.NAME, name)

    @allure.step("Fill surname: {surname}")
    def fill_surname(self, surname: str) -> None:
        self.fill(self.SURNAME, surname)

    @allure.step("Fill address: {address}")
    def fill_address(self, address: str) -> None:
        self.fill(self.ADDRESS, address)

    @allure.step("Select metro: {metro}")
    def select_metro(self, metro: str, timeout: float = 10.0) -> None:
        input_el = self.find(self.METRO_INPUT, timeout=4)
        self.click_element(input_el)
        input_el.clear()
        input_el.send_keys(metro)

        chosen = self.wait_for(
            lambda d: next(
                (
                    opt
                    for opt in d.find_elements(*self.METRO_OPTIONS)
                    if (opt.text or "").strip().lower() == metro.lower()
                ),
                False
            ),
            timeout=timeout
        )

        if not chosen:
            chosen = self.wait_for(
                lambda d: next(
                    (
                        opt
                        for opt in d.find_elements(*self.METRO_OPTIONS)
                        if metro.lower() in (opt.text or "").strip().lower()
                    ),
                    False
                ),
                timeout=timeout
            )

        self.click_element(chosen)

    @allure.step("Fill phone: {phone}")
    def fill_phone(self, phone: str) -> None:
        self.fill(self.PHONE, phone)

    @allure.step("Click next")
    def click_next(self) -> None:
        self.click(self.NEXT_BUTTON)
        self.wait_for(lambda d: bool(d.find_elements(*self.DATE_INPUT) or d.find_elements(*self.DATE_PICKER_CONTAINER)), timeout=8)

    @allure.step("Set date by clicking day {day}")
    def set_date_by_click(self, day: int, timeout: float = 8.0) -> None:
        date_field = self.find(self.DATE_INPUT, timeout=3)
        self.click_element(date_field)

        chosen = self.wait_for(
            lambda d: next(
                (
                    e
                    for sel in self.DATE_DAY_SELECTORS
                    for e in d.find_elements(By.CSS_SELECTOR, sel)
                    if (e.text or "").strip() == str(int(day))
                    and "disabled" not in (e.get_attribute("class") or "")
                    and "outside" not in (e.get_attribute("class") or "")
                    and "react-datepicker__day--outside-month" not in (e.get_attribute("class") or "")
                ),
                False
            ),
            timeout=timeout
        )

        self.click_element(chosen)

    @allure.step("Set date {day}")
    def set_date(self, day: int, timeout: float = 8.0) -> None:
        self.set_date_by_click(day, timeout=timeout)

    @allure.step("Choose rental days: {days_text}")
    def choose_rental_days(self, days_text: str) -> None:
        self.click(self.RENT_TERM_DROPDOWN)
        options = self.find_all(self.RENT_TERM_OPTION, timeout=5)
        for opt in options:
            if opt.text.strip().lower() == days_text.strip().lower():
                self.click_element(opt)
                return
        self.click_element(options[0])

    @allure.step("Choose color: {color_text}")
    def choose_color(self, color_text: str) -> None:
        labels = self.find_all(self.COLOR_CHECKBOXES, timeout=3)
        for lbl in labels:
            if color_text.lower() in lbl.text.lower():
                self.click_element(lbl)
                return
        self.click_element(labels[0])

    @allure.step("Fill comment")
    def fill_comment(self, comment: str) -> None:
        if comment:
            self.fill(self.COMMENT_INPUT, comment)

    @allure.step("Submit order (open confirm modal)")
    def submit_order(self) -> None:
        self.click(self.ORDER_BUTTON)
        self.wait_for(
            lambda d: bool(
                d.find_elements(*self.CONFIRM_MODAL)
                or d.find_elements(*self.CONFIRM_YES)
                or d.find_elements(By.XPATH, "//div[contains(text(),'Хотите оформить заказ') or contains(text(),'Хотите оформить')]")
            ),
            timeout=6
        )

    @allure.step("Confirm modal: click Yes")
    def confirm_modal_yes(self) -> None:
        self.click(self.CONFIRM_YES)

    @allure.step("Is confirmation modal visible")
    def is_confirmation_modal_visible(self, timeout: float = 5.0) -> bool:
        try:
            self.wait_visible(self.CONFIRM_MODAL, timeout=timeout)
            return True
        except TimeoutException:
            try:
                self.find(self.CONFIRM_YES, timeout=timeout)
                return True
            except TimeoutException:
                return False
