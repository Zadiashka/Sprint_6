from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class OrderPage:
    NAME_FIELD = (By.CSS_SELECTOR, "div.Order_Form__17u6u > div:nth-child(1) input")
    SURNAME_FIELD = (By.CSS_SELECTOR, "div.Order_Form__17u6u > div:nth-child(2) input")
    ADDRESS_FIELD = (By.CSS_SELECTOR, "div.Order_Form__17u6u > div:nth-child(3) input")
    METRO_INPUT = (By.CSS_SELECTOR, "div.select-search__value input.select-search__input")
    PHONE_FIELD = (By.CSS_SELECTOR, "div.Order_Form__17u6u > div:nth-child(5) input")
    NEXT_BUTTON = (By.CSS_SELECTOR, "div.Order_NextButton__1_rCA > button")
    DATE_INPUT = (By.CSS_SELECTOR, "div.react-datepicker__input-container input")
    DATE_DAY = (By.CSS_SELECTOR, "div.react-datepicker__day")
    RENTAL_DROPDOWN_CONTROL = (By.CSS_SELECTOR, "div.Dropdown-control")
    COLOR_LABELS = (By.CSS_SELECTOR, "div.Order_Checkboxes__3lWSI label")
    COMMENT_FIELD = (By.CSS_SELECTOR, "div.Input_InputContainer__3NykH input, div.Input_InputContainer__3NykH textarea")
    BACK_BUTTON = (By.CSS_SELECTOR, "div.Order_Buttons__1xGrp > button.Button_Button__ra12g.Button_Middle__1CSJM.Button_Inverted__3IF-i")
    ORDER_BUTTON = (By.CSS_SELECTOR, "div.Order_Buttons__1xGrp > button.Button_Button__ra12g.Button_Middle__1CSJM")
    CONFIRM_MODAL = (By.CSS_SELECTOR, "div.Order_Modal__YZ-d3")
    CONFIRM_YES = (By.CSS_SELECTOR, "div.Order_Modal__YZ-d3 > div.Order_Buttons__1xGrp > button:nth-child(2)")
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")
    OVERLAY_IMAGE = (By.CSS_SELECTOR, 'img[src="/assets/scooter.png"]')

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def accept_cookies(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.COOKIE_BUTTON))
            btn.click()
            self.wait.until(EC.invisibility_of_element_located(self.COOKIE_BUTTON))
        except TimeoutException:
            pass

    def _hide_overlay_if_present(self):
        try:
            overlay = self.driver.find_element(*self.OVERLAY_IMAGE)
            self.driver.execute_script("arguments[0].style.pointerEvents='none'; arguments[0].style.visibility='hidden';", overlay)
        except NoSuchElementException:
            pass

    def fill_contact_info(self, name: str, surname: str, address: str, metro: str, phone: str):
        self.wait.until(EC.visibility_of_element_located(self.NAME_FIELD)).send_keys(name)
        self.wait.until(EC.visibility_of_element_located(self.SURNAME_FIELD)).send_keys(surname)
        self.wait.until(EC.visibility_of_element_located(self.ADDRESS_FIELD)).send_keys(address)
        self._choose_metro(metro)
        self.wait.until(EC.visibility_of_element_located(self.PHONE_FIELD)).send_keys(phone)
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    def _choose_metro(self, station_name: str):
        inp = self.wait.until(EC.element_to_be_clickable(self.METRO_INPUT))
        inp.click()
        try:
            inp.clear()
        except Exception:
            pass
        inp.send_keys(station_name[:3])
        self._hide_overlay_if_present()
        xpath_exact = f"//div[contains(@class,'select-search') or contains(@class,'Select')]//div[normalize-space()='{station_name}']"
        xpath_contains = f"//div[contains(@class,'select-search') or contains(@class,'Select')]//div[contains(normalize-space(),'{station_name}')]"
        try:
            el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_exact)))
            try:
                el.click()
                return
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", el)
                return
        except TimeoutException:
            pass
        try:
            el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_contains)))
            try:
                el.click()
                return
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", el)
                return
        except TimeoutException:
            pass
        try:
            first_opt = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.select-search div")))
            self.driver.execute_script("arguments[0].click();", first_opt)
        except TimeoutException:
            pass

    def choose_date(self, target_date: datetime):
        inp = self.wait.until(EC.element_to_be_clickable(self.DATE_INPUT))
        inp.click()
        self._hide_overlay_if_present()
        day = str(target_date.day)
        xpath_day = f"//div[contains(@class,'react-datepicker__day') and not(contains(@class,'react-datepicker__day--outside-month')) and normalize-space()='{day}']"
        try:
            el = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_day)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            try:
                el.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", el)
        except TimeoutException:
            pass

    def fill_rental_info(self, rental_days: str, color: str = None, comment: str = ""):
        try:
            dd = self.wait.until(EC.element_to_be_clickable(self.RENTAL_DROPDOWN_CONTROL))
            dd.click()
            option_xpath = f"//div[contains(@class,'Dropdown-menu')]//div[normalize-space()='{rental_days}']"
            opt = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            opt.click()
        except TimeoutException:
            pass
        if color:
            try:
                labels = self.driver.find_elements(*self.COLOR_LABELS)
                for lbl in labels:
                    if color.lower() in lbl.text.lower():
                        try:
                            lbl.click()
                        except ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", lbl)
                        break
            except Exception:
                pass
        if comment:
            try:
                self.wait.until(EC.visibility_of_element_located(self.COMMENT_FIELD)).send_keys(comment)
            except Exception:
                pass

    def submit_order_and_confirm(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()
        try:
            modal = self.wait.until(EC.visibility_of_element_located(self.CONFIRM_MODAL))
            self.wait.until(EC.element_to_be_clickable(self.CONFIRM_YES)).click()
            try:
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.CONFIRM_MODAL))
            except TimeoutException:
                pass
        except TimeoutException:
            pass
