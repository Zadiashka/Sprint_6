from typing import Optional
from selenium.webdriver.common.by import By
from .base_page import BasePage


class MainPage(BasePage):
    URL: str = "https://qa-scooter.praktikum-services.ru"

    TOP_ORDER = (By.CSS_SELECTOR, "div.Header_Nav__AGCXC > button.Button_Button__ra12g")
    BOTTOM_ORDER = (By.CSS_SELECTOR, "div.Home_FinishButton__1_cWm > button")
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")
    QUESTIONS_SECTION = (By.CSS_SELECTOR, "div.Home_FAQ__3uVm4")
    LOGO_YANDEX = (By.CSS_SELECTOR, "div.Header_Logo__23yGT a.Header_LogoYandex__3TSOI")

    def open_main(self) -> None:
        """Открыть главную страницу и убедиться, что логотип Yandex видим."""
        self.open(self.URL)
        self.wait_visible(self.LOGO_YANDEX, timeout=6)

    def click_top_order(self) -> None:
        """Нажать кнопку заказа в шапке."""
        self.click(self.TOP_ORDER)

    def click_bottom_order(self) -> None:
        """Нажать кнопку заказа внизу страницы; скроллим к элементу перед кликом."""
        try:
            el = self.find(self.BOTTOM_ORDER, timeout=3)
            try:
                self.scroll_into_view(el)
            except Exception:
                try:
                    self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                except Exception:
                    pass
            self.click_element(el)
        except Exception:
            
            try:
                self.click(self.BOTTOM_ORDER)
            except Exception:
                raise

    def accept_cookies(self, timeout: Optional[float] = 3.0) -> None:
        """Принять куки, если кнопка доступна. Бросает исключение при реальной ошибке."""
        self.wait_visible(self.COOKIE_BUTTON, timeout=timeout)
        self.click(self.COOKIE_BUTTON)

    def open_questions_section(self, timeout: float = 6.0) -> None:
        """Дождаться и прокрутить до секции вопросов."""
        el = self.wait_visible(self.QUESTIONS_SECTION, timeout=timeout)
        try:
            self.scroll_into_view(el)
        except Exception:
            try:
                self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            except Exception:
                pass
