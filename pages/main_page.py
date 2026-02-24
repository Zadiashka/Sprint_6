from selenium.webdriver.common.by import By
from .base_page import BasePage


class MainPage(BasePage):
    URL = "https://qa-scooter.praktikum-services.ru"

    TOP_ORDER = (By.CSS_SELECTOR, "div.Header_Nav__AGCXC > button.Button_Button__ra12g")
    BOTTOM_ORDER = (By.CSS_SELECTOR, "div.Home_FinishButton__1_cWm > button")
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")
    QUESTIONS_SECTION = (By.CSS_SELECTOR, "div.Home_FAQ__3uVm4")
    LOGO_YANDEX = (By.CSS_SELECTOR, "div.Header_Logo__23yGT a.Header_LogoYandex__3TSOI")

    def open_main(self) -> None:
        self.open(self.URL)

    def click_top_order(self) -> None:
        self.click(self.TOP_ORDER)

    def click_bottom_order(self) -> None:
        self.click(self.BOTTOM_ORDER)

    def accept_cookies(self) -> None:
       
        self.click(self.COOKIE_BUTTON)

    def is_questions_section_visible(self) -> bool:
        try:
            self.wait_visible(self.QUESTIONS_SECTION, timeout=3)
            return True
        except Exception:
            return False
