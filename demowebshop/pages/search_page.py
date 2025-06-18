from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage

class SearchPage(BasePage):
    # Locators
    SEARCH_BOX = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "input.button-1.search-box-button")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "div.product-grid")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "div.no-result")
    PRODUCT_TITLES = (By.CSS_SELECTOR, "h2.product-title a")
    SEARCH_TERM = (By.CSS_SELECTOR, "div.search-term")
    SEARCH_INPUT = (By.ID, "small-searchterms")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def enter_search_term(self, term):
        try:
            search_box = self.wait.until(EC.presence_of_element_located(self.SEARCH_BOX))
            search_box.clear()
            search_box.send_keys(term)
        except TimeoutException:
            raise Exception("Search box not found")

    def perform_search(self):
        try:
            search_button = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
            search_button.click()
            # Wait for either results or no results message
            try:
                self.wait.until(EC.any_of(
                    EC.presence_of_element_located(self.SEARCH_RESULTS),
                    EC.presence_of_element_located(self.NO_RESULTS_MESSAGE)
                ))
            except TimeoutException:
                pass  # Continue even if no results are found
        except TimeoutException:
            raise Exception("Search button not found or not clickable")

    def get_search_results(self):
        try:
            results = self.wait.until(EC.presence_of_element_located(self.SEARCH_RESULTS))
            return results.text
        except TimeoutException:
            return ""

    def get_no_results_message(self):
        try:
            message = self.wait.until(EC.presence_of_element_located(self.NO_RESULTS_MESSAGE))
            return message.text
        except TimeoutException:
            return ""

    def get_result_titles(self):
        try:
            titles = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_TITLES))
            return [title.text.lower() for title in titles]
        except TimeoutException:
            return []

    def get_search_term(self):
        try:
            # First try to get the search term from the search term display
            term = self.wait.until(EC.presence_of_element_located(self.SEARCH_TERM))
            return term.text
        except TimeoutException:
            try:
                # If not found, get it from the search input
                search_input = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
                return search_input.get_attribute("value")
            except TimeoutException:
                return "" 