# pages/questions_page.py
import allure
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .base_page import BasePage

class QuestionsPage(BasePage):
    QUESTIONS_SECTION = (By.CSS_SELECTOR, "div.Home_FAQ__3uVm4")
    QUESTION_ITEM_SELECTORS = [
        ".accordion__item",
        ".accordion-item",
        ".faq__item",
        ".Home_FAQ__3uVm4 .accordion__item",
        ".Home_FAQ__3uVm4 .accordion-item",
        ".Home_FAQ__3uVm4 .faq__item"
    ]
    QUESTION_TITLE_SELECTORS = [
        ".accordion__button",
        ".accordion__heading",
        ".accordion__trigger",
        "button"
    ]
    QUESTION_ANSWER_SELECTORS = [
        ".accordion__panel",
        ".accordion__content",
        ".accordion__answer",
        ".faq__answer",
        ".answer"
    ]

    def _collect_items(self) -> List[WebElement]:
        try:
            section = self.find(self.QUESTIONS_SECTION, timeout=5)
        except Exception:
            items = []
            for sel in self.QUESTION_ITEM_SELECTORS:
                items = self._driver.find_elements(By.CSS_SELECTOR, sel)
                if items:
                    return items
            return []
        for sel in self.QUESTION_ITEM_SELECTORS:
            items = section.find_elements(By.CSS_SELECTOR, sel)
            if items:
                return items
        return section.find_elements(By.CSS_SELECTOR, "div")

    @allure.step("Open question by index {index}")
    def open_question_by_index(self, index: int) -> None:
        items = self._collect_items()
        if index < 0 or index >= len(items):
            raise IndexError("Question index out of range")
        el = items[index]

        # try to click the button inside the item (preferred .accordion__button)
        for title_sel in self.QUESTION_TITLE_SELECTORS:
            try:
                title = el.find_element(By.CSS_SELECTOR, title_sel)
            except Exception:
                continue

            # scroll into view
            try:
                self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", title)
            except Exception:
                pass

            # try to remove overlay at click point (temporary pointer-events:none)
            try:
                self._driver.execute_script("""
                    const target = arguments[0];
                    const r = target.getBoundingClientRect();
                    const cx = Math.floor(r.left + r.width/2);
                    const cy = Math.floor(r.top + r.height/2);
                    const top = document.elementFromPoint(cx, cy);
                    if (top && top !== target) { top.setAttribute('data-prev-pe', top.style.pointerEvents || ''); top.style.pointerEvents = 'none'; }
                """, title)
            except Exception:
                pass

            # click using robust method
            try:
                self.ensure_clickable_and_click(title)
            except Exception:
                try:
                    self._driver.execute_script("arguments[0].click();", title)
                except Exception:
                    # restore pointer-events if we changed it (best-effort)
                    try:
                        self._driver.execute_script("""
                            const target = arguments[0];
                            const r = target.getBoundingClientRect();
                            const cx = Math.floor(r.left + r.width/2);
                            const cy = Math.floor(r.top + r.height/2);
                            const top = document.elementFromPoint(cx, cy);
                            if (top && top.getAttribute && top.getAttribute('data-prev-pe') !== null) { top.style.pointerEvents = top.getAttribute('data-prev-pe'); top.removeAttribute('data-prev-pe'); }
                        """, title)
                    except Exception:
                        pass
                    continue

            # wait until panel becomes visible: either aria-expanded true or panel hidden removed
            try:
                panel_id = title.get_attribute("aria-controls")
                if panel_id:
                    panel_locator = (By.ID, panel_id)
                    def _panel_shown(d):
                        try:
                            p = d.find_element(*panel_locator)
                            # panel may have attribute hidden="" or hidden present; consider shown when hidden is absent
                            return p.get_attribute("hidden") in (None, "false")
                        except Exception:
                            return False
                    self.wait_for(_panel_shown, timeout=5)
                else:
                    # fallback: wait for aria-expanded
                    def _expanded(d):
                        try:
                            return title.get_attribute("aria-expanded") == "true"
                        except Exception:
                            return False
                    self.wait_for(_expanded, timeout=5)
            except Exception:
                # ignore wait failures — we'll still try to read text
                pass

            # restore pointer-events if we changed it (best-effort)
            try:
                self._driver.execute_script("""
                    const target = arguments[0];
                    const r = target.getBoundingClientRect();
                    const cx = Math.floor(r.left + r.width/2);
                    const cy = Math.floor(r.top + r.height/2);
                    const top = document.elementFromPoint(cx, cy);
                    if (top && top.getAttribute && top.getAttribute('data-prev-pe') !== null) { top.style.pointerEvents = top.getAttribute('data-prev-pe'); top.removeAttribute('data-prev-pe'); }
                """, title)
            except Exception:
                pass

            return

        # last resort: click the whole item
        try:
            self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        self.click_element(el)

    @allure.step("Get answer text by index {index}")
    def get_answer_text_by_index(self, index: int) -> str:
        items = self._collect_items()
        if index < 0 or index >= len(items):
            raise IndexError("Question index out of range")
        el = items[index]

        # first try: panel inside the item
        for ans_sel in self.QUESTION_ANSWER_SELECTORS:
            try:
                panel = el.find_element(By.CSS_SELECTOR, ans_sel)
                text = (panel.text or "").strip()
                if text:
                    return text
            except Exception:
                continue

        # fallback: collect all panels in section and pick by index
        try:
            section = self.find(self.QUESTIONS_SECTION, timeout=3)
            panels = []
            for sel in self.QUESTION_ANSWER_SELECTORS:
                panels = section.find_elements(By.CSS_SELECTOR, sel)
                if panels:
                    break
            if panels and index < len(panels):
                return (panels[index].text or "").strip()
        except Exception:
            pass

        return ""
