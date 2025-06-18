import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pages.register_page import RegisterPage
from pages.product_page import ProductPage
from pages.search_page import SearchPage
import os

@pytest.fixture
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Use the ChromeDriver from the project's bin directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    driver_path = os.path.join(current_dir, 'bin', 'chromedriver')
    
    if not os.path.exists(driver_path):
        raise Exception(f"ChromeDriver not found at {driver_path}")
    
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def register_page(driver):
    return RegisterPage(driver)

@pytest.fixture
def product_page(driver):
    return ProductPage(driver)

@pytest.fixture
def search_page(driver):
    return SearchPage(driver) 