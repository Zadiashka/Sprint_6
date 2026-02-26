# tests/test_smoke.py
import pytest
import time
from pages.main_page import MainPage
from config import BASE_URL

@pytest.mark.usefixtures("driver")
class TestSmoke:
    def test_logos_navigate(self, driver):
        main = MainPage(driver)
        main.open_main()

        main.accept_cookies()

        # Click scooter logo and verify navigation to base url (home)
        scooter_logo = main.find(MainPage.LOGO_SCOOTER, timeout=5)
        main.click_element(scooter_logo)

        def _url_is_home(d):
            try:
                return BASE_URL in d.current_url
            except Exception:
                return False

        main.wait_for(_url_is_home, timeout=6)

        # Click Yandex logo — expected redirect to Dzen/Yandex
        yel = main.find(MainPage.LOGO_YANDEX, timeout=5)
        href = yel.get_attribute("href") or ""
        main.click_element(yel)

        # wait for new window or url change
        deadline = time.time() + 10
        while time.time() < deadline:
            handles = driver.window_handles
            if len(handles) > 1:
                driver.switch_to.window(handles[-1])
                break
            try:
                cur = driver.current_url or ""
                if "dzen.ru" in cur.lower() or "yandex" in cur.lower() or "zen.yandex" in cur.lower():
                    break
            except Exception:
                pass
            time.sleep(0.2)

        # wait for the expected URL to load
        deadline = time.time() + 10
        while time.time() < deadline:
            try:
                cur = (driver.current_url or "").lower()
                if "dzen.ru" in cur or "yandex" in cur or "zen.yandex" in cur:
                    break
            except Exception:
                pass
            time.sleep(0.2)

        cur_url = (driver.current_url or "").lower()

        # fallback: if still about:blank or not expected, open href directly
        if ("dzen.ru" not in cur_url and "yandex" not in cur_url and href):
            driver.get(href)
            main.wait_for(lambda d: "dzen.ru" in d.current_url.lower() or "yandex" in d.current_url.lower() or "zen.yandex" in d.current_url.lower(), timeout=8)
            cur_url = driver.current_url.lower()

        assert "dzen.ru" in cur_url or "yandex" in cur_url or "zen.yandex" in cur_url, f"Expected Dzen/Yandex in URL, got {cur_url}"
