# pages/main_page.py
from typing import Optional
import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage
from config import BASE_URL

class MainPage(BasePage):
    URL: str = BASE_URL

    TOP_ORDER = (By.CSS_SELECTOR, "div.Header_Nav__AGCXC > button.Button_Button__ra12g")
    BOTTOM_ORDER = (By.CSS_SELECTOR, "div.Home_FinishButton__1_cWm > button")
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")
    QUESTIONS_SECTION = (By.CSS_SELECTOR, "div.Home_FAQ__3uVm4")
    LOGO_YANDEX = (By.CSS_SELECTOR, "div.Header_Logo__23yGT a.Header_LogoYandex__3TSOI")
    LOGO_SCOOTER = (By.CSS_SELECTOR, "a.Header_LogoScooter__3lsAR[href='/']")

    @allure.step("Open main page")
    def open_main(self) -> None:
        self.open(self.URL)
        self.wait_visible(self.LOGO_SCOOTER, timeout=6)

    @allure.step("Click top order button")
    def click_top_order(self) -> None:
        self.click(self.TOP_ORDER)

    @allure.step("Click bottom order button")
    def click_bottom_order(self) -> None:
        el = self.find(self.BOTTOM_ORDER, timeout=5)
        try:
            self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        self.click_element(el)

    @allure.step("Accept cookies")
    def accept_cookies(self, timeout: Optional[float] = 3.0) -> None:
        self.wait_visible(self.COOKIE_BUTTON, timeout=timeout)
        self.click(self.COOKIE_BUTTON)

    @allure.step("Open questions section")
    def open_questions_section(self, timeout: float = 6.0) -> None:
        el = self.wait_visible(self.QUESTIONS_SECTION, timeout=timeout)
        try:
            self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
