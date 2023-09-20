from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def fetch_html_selenium(url, timeout=10, additional_wait=5):
    # Set up the driver. This will open a browser window.
    driver = webdriver.Firefox()
    driver.get(url)

    try:
        # Wait for document to be complete
        WebDriverWait(driver, timeout).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # Wait for an additional fixed time to allow dynamic content to load
        time.sleep(additional_wait)
        
        # Retrieve the HTML content
        html_content = driver.page_source

    except TimeoutException:
        print("Timed out waiting for page to load")
        html_content = ""

    finally:
        driver.quit()

    return html_content
