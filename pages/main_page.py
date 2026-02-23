from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class MainPage:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    TOP_ORDER_BUTTON = (By.CSS_SELECTOR, "div.Header_Nav__AGCXC > button.Button_Button__ra12g")
    BOTTOM_ORDER_BUTTON = (By.CSS_SELECTOR, "div.Home_FinishButton__1_cWm > button")
    LOGO_SCOOTER = (By.CSS_SELECTOR, "a.Header_LogoScooter__3lsAR")
    LOGO_YANDEX = (By.CSS_SELECTOR, "a.Header_LogoYandex__3TSOI")

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.BASE_URL)

    def click_top_order(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.TOP_ORDER_BUTTON))
        btn.click()

    def click_bottom_order(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.BOTTOM_ORDER_BUTTON))
        btn.click()

    def click_logo_scooter(self):
        el = self.wait.until(EC.element_to_be_clickable(self.LOGO_SCOOTER))
        el.click()

    def click_logo_yandex(self):
        try:
            el = self.wait.until(EC.presence_of_element_located(self.LOGO_YANDEX))
        except TimeoutException:
            raise TimeoutException("Logo Yandex not found")
        try:
            href = el.get_attribute("href")
        except Exception:
            href = None
        try:
            target = el.get_attribute("target")
        except Exception:
            target = None
        try:
            self.wait.until(EC.element_to_be_clickable(self.LOGO_YANDEX)).click()
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", el)
            except Exception:
                raise TimeoutException("Logo Yandex not clickable")
        return {"href": href, "target": target}
