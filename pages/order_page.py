# pages/order_page.py
import allure
from typing import Optional, List
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
        if not metro:
            raise ValueError("metro must be provided")
        input_el = self.find(self.METRO_INPUT, timeout=4)
        self.click_element(input_el)
        try:
            input_el.clear()
        except Exception:
            pass
        input_el.send_keys(metro)
        def _options_present(d):
            opts = d.find_elements(*self.METRO_OPTIONS)
            return opts if opts else False
        opts = self.wait_for(_options_present, timeout=timeout)
        chosen = None
        for opt in opts:
            txt = (opt.text or "").strip()
            if txt and txt.lower() == metro.lower():
                chosen = opt
                break
        if not chosen:
            for opt in opts:
                txt = (opt.text or "").strip()
                if txt and metro.lower() in txt.lower():
                    chosen = opt
                    break
        if not chosen:
            chosen = opts[0]
        # ensure visible and clickable
        try:
            self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", chosen)
        except Exception:
            pass
        self.click_element(chosen)

    @allure.step("Fill phone: {phone}")
    def fill_phone(self, phone: str) -> None:
        self.fill(self.PHONE, phone)

    @allure.step("Click next")
    def click_next(self) -> None:
        self.click(self.NEXT_BUTTON)
        def _date_ready(d):
            if d.find_elements(*self.DATE_INPUT):
                return True
            if d.find_elements(*self.DATE_PICKER_CONTAINER):
                return True
            return False
        self.wait_for(_date_ready, timeout=8)

    @allure.step("Set date by clicking day {day}")
    def set_date_by_click(self, day: int, timeout: float = 8.0) -> None:
        try:
            date_field = self.find(self.DATE_INPUT, timeout=3)
            self.click_element(date_field)
        except Exception:
            def _picker_present(d):
                return d.find_elements(*self.DATE_PICKER_CONTAINER) or False
            self.wait_for(_picker_present, timeout=2)
        def _find_and_click(d):
            for sel in self.DATE_DAY_SELECTORS:
                elems = d.find_elements(By.CSS_SELECTOR, sel)
                for e in elems:
                    txt = (e.text or "").strip()
                    cls = (e.get_attribute("class") or "")
                    if not txt:
                        continue
                    if txt == str(int(day)) and "disabled" not in cls and "outside" not in cls and "react-datepicker__day--outside-month" not in cls:
                        try:
                            d.execute_script("arguments[0].scrollIntoView({block:'center'});", e)
                        except Exception:
                            pass
                        try:
                            e.click()
                            return True
                        except Exception:
                            try:
                                d.execute_script("arguments[0].click();", e)
                                return True
                            except Exception:
                                continue
            return False
        try:
            self.wait_for(_find_and_click, timeout=timeout)
        except Exception:
            self.save_artifacts("date_click_failure")
            raise TimeoutException(f"Не удалось выбрать дату кликом: {day}")

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
        if options:
            self.click_element(options[0])

    @allure.step("Choose color: {color_text}")
    def choose_color(self, color_text: str) -> None:
        labels = self.find_all(self.COLOR_CHECKBOXES, timeout=3)
        for lbl in labels:
            if color_text.lower() in lbl.text.lower():
                self.click_element(lbl)
                return
        if labels:
            self.click_element(labels[0])

    @allure.step("Fill comment")
    def fill_comment(self, comment: str) -> None:
        if comment:
            self.fill(self.COMMENT_INPUT, comment)

    @allure.step("Submit order (open confirm modal)")
    def submit_order(self) -> None:
        # click order button and wait for confirmation modal or confirm button
        self.click(self.ORDER_BUTTON)
        def _confirm_present(d):
            if d.find_elements(*self.CONFIRM_MODAL):
                return True
            if d.find_elements(*self.CONFIRM_YES):
                return True
            try:
                els = d.find_elements(By.XPATH, "//div[contains(text(),'Хотите оформить заказ') or contains(text(),'Хотите оформить')]")
                if els:
                    return True
            except Exception:
                pass
            return False
        try:
            self.wait_for(_confirm_present, timeout=6)
        except Exception:
            self.save_artifacts("confirm_modal_not_shown")
            # do not raise here; caller will assert visibility if needed

    @allure.step("Confirm modal: click Yes")
    def confirm_modal_yes(self) -> None:
        self.click(self.CONFIRM_YES)

    @allure.step("Is confirmation modal visible")
    def is_confirmation_modal_visible(self, timeout: float = 5.0) -> bool:
        try:
            self.wait_visible(self.CONFIRM_MODAL, timeout=timeout)
            return True
        except Exception:
            # try alternative: presence of confirm yes button
            try:
                self.find(self.CONFIRM_YES, timeout=timeout)
                return True
            except Exception:
                return False
