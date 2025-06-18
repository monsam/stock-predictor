import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture(scope="session")
def driver():
    """Create a WebDriver instance for the test session."""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    # Use the ChromeDriver from the project's bin directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(current_dir, 'bin', 'chromedriver')
    
    if not os.path.exists(driver_path):
        raise Exception(f"ChromeDriver not found at {driver_path}")
    
    # Create service with explicit binary location
    service = Service(
        executable_path=driver_path,
        log_path=os.path.join(current_dir, 'chromedriver.log')
    )
    
    try:
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        driver.maximize_window()
        driver.implicitly_wait(10)
        yield driver
    finally:
        if 'driver' in locals():
            driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for the demo web shop."""
    return "https://demowebshop.tricentis.com" 