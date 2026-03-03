# pages/order_page.py
import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

class OrderPage(BasePage):
    NAME = (By.CSS_SELECTOR, "input[placeholder='* Имя']")
    SURNAME = (By.CSS_SELECTOR, "input[placeholder='* Фамилия']")
    ADDRESS = (By.CSS_SELECTOR, "input[placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.CSS_SELECTOR, "input.select-search__input")
    METRO_OPTIONS = (By.CSS_SELECTOR, ".select-search__option")
    PHONE = (By.CSS_SELECTOR, "input[placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.CSS_SELECTOR, "div.Order_NextButton__1_rCA > button")

    DATE_INPUT = (By.CSS_SELECTOR, "div.Order_MixedDatePicker__3qiay input")
    RENT_TERM_DROPDOWN = (By.CSS_SELECTOR, "div.Dropdown-root")
    RENT_TERM_OPTION = (By.CSS_SELECTOR, "div.Dropdown-menu .Dropdown-option")
    COLOR_BLACK = (By.CSS_SELECTOR, "div.Order_Checkboxes__3lWSI > label:nth-child(2)")
    COLOR_GREY = (By.CSS_SELECTOR, "div.Order_Checkboxes__3lWSI > label:nth-child(4)")
    COMMENT_INPUT = (By.CSS_SELECTOR, "input[placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.CSS_SELECTOR, "div.Order_Content__bmtHS > div.Order_Buttons__1xGrp > button:nth-child(2)")

    CONFIRM_MODAL = (By.XPATH, "//div[contains(@class,'Order_Modal__YZ-d3') and .//div[contains(text(),'Хотите оформить заказ')]]")
    CONFIRM_MODAL_HEADER = (By.CSS_SELECTOR, "div.Order_ModalHeader__3FDaJ")
    CONFIRM_YES = (By.CSS_SELECTOR, "div.Order_Modal__YZ-d3 > div.Order_Buttons__1xGrp > button:nth-child(2)")
    CONFIRM_NO = (By.CSS_SELECTOR, "div.Order_Modal__YZ-d3 > div.Order_Buttons__1xGrp > button:nth-child(1)")
    ORDER_SUCCESS_TEXT = (By.CSS_SELECTOR, "div.Order_ModalHeader__3FDaJ")

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
                (opt for opt in d.find_elements(*self.METRO_OPTIONS)
                 if metro.lower() in (opt.text or "").strip().lower()),
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
        self.wait_for(
            lambda d: bool(d.find_elements(*self.DATE_INPUT)),
            timeout=8
        )

    @allure.step("Set date by clicking day {day}")
    def set_date(self, day: int, timeout: float = 8.0) -> None:
        date_field = self.find(self.DATE_INPUT, timeout=3)
        self.click_element(date_field)

        chosen = self.wait_for(
            lambda d: next(
                (
                    e for e in d.find_elements(By.CSS_SELECTOR, ".react-datepicker__day")
                    if (e.text or "").strip() == str(day)
                    and "outside-month" not in (e.get_attribute("class") or "")
                    and "disabled" not in (e.get_attribute("class") or "")
                ),
                False
            ),
            timeout=timeout
        )
        self.click_element(chosen)

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
        if "чёрн" in color_text.lower() or "черн" in color_text.lower():
            self.click(self.COLOR_BLACK)
        else:
            self.click(self.COLOR_GREY)

    @allure.step("Fill comment")
    def fill_comment(self, comment: str) -> None:
        if comment:
            self.fill(self.COMMENT_INPUT, comment)

    @allure.step("Submit order (open confirm modal)")
    def submit_order(self) -> None:
        self.click(self.ORDER_BUTTON)
        self.wait_visible(self.CONFIRM_MODAL_HEADER, timeout=8)

    @allure.step("Confirm modal: click Yes")
    def confirm_modal_yes(self) -> None:
        self.click(self.CONFIRM_YES)

    @allure.step("Is confirmation modal visible")
    def is_confirmation_modal_visible(self, timeout: float = 5.0) -> bool:
        try:
            self.wait_visible(self.CONFIRM_MODAL, timeout=timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Is order successful")
    def is_order_successful(self, timeout: float = 5.0) -> bool:
        try:
            self.wait_visible(self.ORDER_SUCCESS_TEXT, timeout=timeout)
            return True
        except TimeoutException:
            return False