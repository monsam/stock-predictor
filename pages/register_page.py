from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RegisterPage:
    # Locators
    EMAIL_FIELD = (By.ID, "Email")
    PASSWORD_FIELD = (By.ID, "Password")
    CONFIRM_PASSWORD_FIELD = (By.ID, "ConfirmPassword")
    REGISTER_BUTTON = (By.ID, "register-button")
    EMAIL_ERROR = (By.CSS_SELECTOR, "span.field-validation-error[data-valmsg-for='Email']")
    PASSWORD_MISMATCH_ERROR = (By.CSS_SELECTOR, "span.field-validation-error[data-valmsg-for='ConfirmPassword']")
    VALIDATION_SUMMARY = (By.CSS_SELECTOR, "div.validation-summary-errors")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_email(self, email):
        try:
            email_field = self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
            email_field.clear()
            email_field.send_keys(email)
        except TimeoutException:
            raise Exception("Email field not found")

    def enter_password(self, password):
        try:
            password_field = self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
            password_field.clear()
            password_field.send_keys(password)
        except TimeoutException:
            raise Exception("Password field not found")

    def enter_confirm_password(self, password):
        try:
            confirm_field = self.wait.until(EC.presence_of_element_located(self.CONFIRM_PASSWORD_FIELD))
            confirm_field.clear()
            confirm_field.send_keys(password)
        except TimeoutException:
            raise Exception("Confirm password field not found")

    def click_register(self):
        try:
            register_button = self.wait.until(EC.element_to_be_clickable(self.REGISTER_BUTTON))
            register_button.click()
        except TimeoutException:
            raise Exception("Register button not found or not clickable")

    def get_email_error(self):
        try:
            # First check for field-specific error
            error = self.wait.until(EC.presence_of_element_located(self.EMAIL_ERROR))
            return error.text
        except TimeoutException:
            try:
                # Then check for validation summary
                summary = self.driver.find_element(*self.VALIDATION_SUMMARY)
                if "email" in summary.text.lower():
                    return summary.text
            except NoSuchElementException:
                pass
        return ""

    def get_password_mismatch_error(self):
        try:
            error = self.wait.until(EC.presence_of_element_located(self.PASSWORD_MISMATCH_ERROR))
            return error.text
        except TimeoutException:
            try:
                # Check validation summary for password mismatch
                summary = self.driver.find_element(*self.VALIDATION_SUMMARY)
                if "password" in summary.text.lower() and "match" in summary.text.lower():
                    return summary.text
            except NoSuchElementException:
                pass
        return "" 