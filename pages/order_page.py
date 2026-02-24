from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .base_page import BasePage


class OrderPage(BasePage):
    # Локаторы первой страницы заказа (форма)
    NAME = (By.CSS_SELECTOR, "div.Order_Form__17u6u > div:nth-child(1) input")
    SURNAME = (By.CSS_SELECTOR, "div.Order_Form__17u6u > div:nth-child(2) input")
    ADDRESS = (By.CSS_SELECTOR, "div.Order_Form__17u6u > div:nth-child(3) input")
    METRO_INPUT = (By.CSS_SELECTOR, "div.select-search__value input.select-search__input")
    METRO_OPTIONS = (By.CSS_SELECTOR, "div.select-search__option")
    PHONE = (By.CSS_SELECTOR, "div.Order_Form__17u6u > div:nth-child(5) input")
    NEXT_BUTTON = (By.CSS_SELECTOR, "div.Order_NextButton__1_rCA > button")

    # Вторая страница (аренда)
    DATE_INPUT = (By.CSS_SELECTOR, "div.Order_MixedDatePicker__3qiay input")
    DATE_PICKER_MONTH = (By.CSS_SELECTOR, "div.react-datepicker__month")
    RENTAL_DROPDOWN = (By.CSS_SELECTOR, "div.Dropdown-control")
    RENTAL_OPTIONS = (By.CSS_SELECTOR, "div.Dropdown-menu div.Dropdown-option")
    COLOR_CHECKBOXES = (By.CSS_SELECTOR, "div.Order_Checkboxes__3lWSI label")
    COMMENT = (By.CSS_SELECTOR, "div.Input_InputContainer__3NykH input")
    BACK_BUTTON = (By.CSS_SELECTOR, "div.Order_Buttons__1xGrp > button.Button_Inverted__3IF-i")
    ORDER_BUTTON = (By.CSS_SELECTOR, "div.Order_Buttons__1xGrp > button:nth-child(2)")

    # Модалка подтверждения
    CONFIRM_MODAL = (By.CSS_SELECTOR, "div.Order_Modal__YZ-d3")
    CONFIRM_NO = (By.CSS_SELECTOR, "div.Order_Modal__YZ-d3 button.Button_Inverted__3IF-i")
    CONFIRM_YES = (By.CSS_SELECTOR, "div.Order_Modal__YZ-d3 button:nth-child(2)")

    def fill_name(self, name: str) -> None:
        self.fill(self.NAME, name)

    def fill_surname(self, surname: str) -> None:
        self.fill(self.SURNAME, surname)

    def fill_address(self, address: str) -> None:
        self.fill(self.ADDRESS, address)

    def select_metro(self, metro: str) -> None:
        
        self.fill(self.METRO_INPUT, metro)
        
        options = self.find_all(self.METRO_OPTIONS, timeout=5)
        for opt in options:
            if metro.lower() in opt.text.lower():
                opt.click()
                return
        
        if options:
            options[0].click()

    def fill_phone(self, phone: str) -> None:
        self.fill(self.PHONE, phone)

    def click_next(self) -> None:
        self.click(self.NEXT_BUTTON)

    def set_date(self, day: int) -> None:
        
        self.click(self.DATE_INPUT)
        months = self.find_all(self.DATE_PICKER_MONTH, timeout=5)
        for month in months:
            try:
                day_el = month.find_element(By.XPATH, f".//div[contains(@class,'react-datepicker__day') and normalize-space()='{day}']")
                day_el.click()
                return
            except Exception:
                continue
        raise ValueError("Не удалось выбрать дату в календаре")

    def choose_rental_days(self, days_text: str) -> None:
        self.click(self.RENTAL_DROPDOWN)
        options = self.find_all(self.RENTAL_OPTIONS, timeout=5)
        for opt in options:
            if opt.text.strip().lower() == days_text.strip().lower():
                opt.click()
                return
        
        if options:
            options[0].click()

    def choose_color(self, color_text: str) -> None:
        labels = self.find_all(self.COLOR_CHECKBOXES, timeout=3)
        for lbl in labels:
            if color_text.lower() in lbl.text.lower():
                lbl.click()
                return
        
        if labels:
            labels[0].click()

    def fill_comment(self, comment: str) -> None:
        self.fill(self.COMMENT, comment)

    def submit_order(self) -> None:
        self.click(self.ORDER_BUTTON)

    def confirm_modal_yes(self) -> None:
        self.click(self.CONFIRM_YES)

    def is_confirmation_modal_visible(self) -> bool:
        try:
            self.wait_visible(self.CONFIRM_MODAL, timeout=5)
            return True
        except Exception:
            return False
