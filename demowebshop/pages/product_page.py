from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage

class ProductPage(BasePage):
    # Locators
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "input.button-1.add-to-cart-button")
    OUT_OF_STOCK_MESSAGE = (By.CSS_SELECTOR, "div.out-of-stock")
    CART_QUANTITY = (By.CSS_SELECTOR, "span.cart-qty")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product-name")
    NOTIFICATION_MESSAGE = (By.CSS_SELECTOR, "div.bar-notification")
    DISABLED_ADD_TO_CART = (By.CSS_SELECTOR, "input.button-1.add-to-cart-button[disabled]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def is_out_of_stock(self):
        try:
            # Check for out of stock message
            self.wait.until(EC.presence_of_element_located(self.OUT_OF_STOCK_MESSAGE))
            return True
        except TimeoutException:
            try:
                # Check for disabled add to cart button
                self.wait.until(EC.presence_of_element_located(self.DISABLED_ADD_TO_CART))
                return True
            except TimeoutException:
                return False

    def add_to_cart(self):
        try:
            add_button = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON))
            if not add_button.is_enabled():
                return False
            add_button.click()
            # Wait for notification
            self.wait.until(EC.presence_of_element_located(self.NOTIFICATION_MESSAGE))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_cart_quantity(self):
        try:
            quantity_element = self.wait.until(EC.presence_of_element_located(self.CART_QUANTITY))
            return quantity_element.text.strip('()')
        except (TimeoutException, NoSuchElementException):
            return "0"

    def get_product_title(self):
        return self.get_text(*self.PRODUCT_TITLE)

    def is_add_to_cart_enabled(self):
        try:
            add_button = self.wait.until(EC.presence_of_element_located(self.ADD_TO_CART_BUTTON))
            return add_button.is_enabled()
        except (TimeoutException, NoSuchElementException):
            return False 