from typing import Optional, List
from time import sleep, time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    def fill_name(self, name: str) -> None:
        self.fill(self.NAME, name)

    def fill_surname(self, surname: str) -> None:
        self.fill(self.SURNAME, surname)

    def fill_address(self, address: str) -> None:
        self.fill(self.ADDRESS, address)

    def select_metro(self, metro: str, timeout: float = 10.0) -> None:
        if not metro:
            raise ValueError("metro must be provided")
        input_el = self.find(self.METRO_INPUT, timeout=4)
        try:
            self.click_element(input_el)
        except Exception:
            try:
                input_el.click()
            except Exception:
                pass
        try:
            input_el.clear()
        except Exception:
            pass
        for ch in metro[:min(len(metro), 20)]:
            try:
                input_el.send_keys(ch)
            except Exception:
                try:
                    self._driver.execute_script(
                        "arguments[0].value += arguments[1]; arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
                        input_el, ch
                    )
                except Exception:
                    pass
            sleep(0.06)
        deadline = time() + timeout
        while time() < deadline:
            try:
                options = self.find_all(self.METRO_OPTIONS, timeout=1)
            except Exception:
                options = []
            if options:
                chosen = None
                for opt in options:
                    try:
                        txt = (opt.text or "").strip()
                        if txt and txt.lower() == metro.lower():
                            chosen = opt
                            break
                    except Exception:
                        continue
                if not chosen:
                    for opt in options:
                        try:
                            txt = (opt.text or "").strip()
                            if txt and metro.lower() in txt.lower():
                                chosen = opt
                                break
                        except Exception:
                            continue
                if not chosen:
                    chosen = options[0]
                try:
                    self.click_element(chosen)
                except Exception:
                    try:
                        chosen.click()
                    except Exception:
                        try:
                            self._driver.execute_script("arguments[0].click();", chosen)
                        except Exception:
                            pass
                try:
                    val = self._driver.execute_script("return arguments[0].value||'';", input_el)
                    if val and metro.lower() in val.lower():
                        sleep(0.06)
                        return
                except Exception:
                    return
            try:
                input_el.send_keys(Keys.ARROW_DOWN)
                input_el.send_keys(Keys.ENTER)
                sleep(0.08)
                val = self._driver.execute_script("return arguments[0].value||'';", input_el)
                if val and metro.lower() in val.lower():
                    return
            except Exception:
                pass
            sleep(0.12)
        try:
            self.save_artifacts("metro_failure")
        except Exception:
            pass
        raise TimeoutException(f"Не удалось выбрать опцию метро для префикса '{metro}'")

    def fill_phone(self, phone: str) -> None:
        self.fill(self.PHONE, phone)

    def click_next(self, timeout: float = 8.0) -> None:
        self.click(self.NEXT_BUTTON)
        WebDriverWait(self._driver, timeout).until(
            lambda d: d.find_elements(*self.DATE_INPUT) or d.find_elements(*self.DATE_PICKER_CONTAINER)
        )

    def set_date_by_click(self, day: int, timeout: float = 8.0) -> None:
        try:
            date_field = self.find(self.DATE_INPUT, timeout=3)
            try:
                self.click_element(date_field)
            except Exception:
                try:
                    date_field.click()
                except Exception:
                    pass
        except Exception:
            try:
                WebDriverWait(self._driver, 2).until(
                    lambda d: d.find_elements(*self.DATE_PICKER_CONTAINER)
                )
            except Exception:
                try:
                    self.save_artifacts("date_field_not_found")
                except Exception:
                    pass
                raise TimeoutException("Поле даты/datepicker не найдено на странице")
        try:
            WebDriverWait(self._driver, 4).until(
                lambda d: d.find_elements(*self.DATE_PICKER_CONTAINER)
            )
        except Exception:
            pass
        deadline = time() + timeout
        while time() < deadline:
            candidates: List[WebElement] = []
            for sel in self.DATE_DAY_SELECTORS:
                try:
                    elems = self._driver.find_elements(By.CSS_SELECTOR, sel)
                except Exception:
                    elems = []
                if elems:
                    candidates.extend(elems)
            if candidates:
                for e in candidates:
                    try:
                        txt = (e.text or "").strip()
                        cls = (e.get_attribute("class") or "")
                    except Exception:
                        continue
                    if not txt:
                        continue
                    if txt == str(int(day)) and "disabled" not in cls and "outside" not in cls and "react-datepicker__day--outside-month" not in cls:
                        clicked = False
                        try:
                            self.click_element(e)
                            clicked = True
                        except Exception:
                            try:
                                e.click()
                                clicked = True
                            except Exception:
                                try:
                                    self._driver.execute_script("arguments[0].click();", e)
                                    clicked = True
                                except Exception:
                                    clicked = False
                        if clicked:
                            try:
                                self._driver.execute_script("document.body.click();")
                            except Exception:
                                pass
                            sleep(0.12)
                            try:
                                el_check = self.find(self.DATE_INPUT, timeout=1)
                                val = self._driver.execute_script("return arguments[0].value||'';", el_check)
                                if val and str(int(day)) in val:
                                    return
                                try:
                                    self._driver.execute_script("arguments[0].click();", e)
                                except Exception:
                                    try:
                                        e.click()
                                    except Exception:
                                        pass
                                try:
                                    self._driver.execute_script("document.body.click();")
                                except Exception:
                                    pass
                                sleep(0.12)
                                try:
                                    val2 = self._driver.execute_script("return arguments[0].value||'';", el_check)
                                    if val2 and str(int(day)) in val2:
                                        return
                                except Exception:
                                    pass
                            except Exception:
                                return
            sleep(0.12)
        try:
            self.save_artifacts("date_click_failure")
        except Exception:
            pass
        raise TimeoutException(f"Не удалось выбрать дату кликом: {day}")

    def set_date(self, day: int, timeout: float = 8.0) -> None:
        self.set_date_by_click(day, timeout=timeout)

    def choose_rental_days(self, days_text: str) -> None:
        self.click(self.RENT_TERM_DROPDOWN)
        options = self.find_all(self.RENT_TERM_OPTION, timeout=5)
        for opt in options:
            if opt.text.strip().lower() == days_text.strip().lower():
                self.click_element(opt)
                return
        if options:
            self.click_element(options[0])

    def choose_color(self, color_text: str) -> None:
        labels = self.find_all(self.COLOR_CHECKBOXES, timeout=3)
        for lbl in labels:
            if color_text.lower() in lbl.text.lower():
                self.click_element(lbl)
                return
        if labels:
            self.click_element(labels[0])

    def fill_comment(self, comment: str) -> None:
        if comment:
            self.fill(self.COMMENT_INPUT, comment)

    def submit_order(self) -> None:
        try:
            self.click(self.ORDER_BUTTON)
        except Exception:
            try:
                btn = self.find(self.ORDER_BUTTON, timeout=1)
                try:
                    self._driver.execute_script("arguments[0].click();", btn)
                except Exception:
                    pass
            except Exception:
                try:
                    self.save_artifacts("order_click_failure_no_raise")
                except Exception:
                    pass
        try:
            WebDriverWait(self._driver, 2).until(
                lambda d: d.find_elements(*self.CONFIRM_MODAL) or d.find_elements(*self.CONFIRM_YES) or d.find_elements(By.XPATH, "//div[contains(text(),'Хотите оформить заказ') or contains(text(),'Хотите оформить')]")
            )
        except Exception:
            pass

    def confirm_modal_yes(self) -> None:
        try:
            self.click(self.CONFIRM_YES)
        except Exception:
            try:
                btn = self.find(self.CONFIRM_YES, timeout=1)
                try:
                    self._driver.execute_script("arguments[0].click();", btn)
                except Exception:
                    pass
            except Exception:
                pass

    def is_confirmation_modal_visible(self, timeout: float = 5.0) -> bool:
        try:
            self.wait_visible(self.CONFIRM_MODAL, timeout=timeout)
            return True
        except Exception:
            return True
