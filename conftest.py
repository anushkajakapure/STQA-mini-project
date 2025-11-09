import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to initialize and teardown WebDriver
    Scope: function - creates new driver for each test
    """
    # Chrome options
    chrome_options = Options()
    # Uncomment the line below to run in headless mode
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize Chrome driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Implicit wait
    driver.implicitly_wait(10)
    
    yield driver
    
    # Teardown - close browser after test
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def test_setup():
    """
    Session-level setup and teardown
    Runs once before all tests and once after all tests
    """
    print("\n========== TEST SUITE STARTED ==========")
    yield
    print("\n========== TEST SUITE COMPLETED ==========")


# Pytest configuration
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "functional: marks tests as functional tests"
    )
    config.addinivalue_line(
        "markers", "ui: marks tests as UI/UX tests"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests"
    )
    config.addinivalue_line(
        "markers", "security: marks tests as security tests"
    )