from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from store import Store
import time
import re

class HH(Store):
    """
    Price scraper for HH grocery store website.
    """
    
    def __init__(self):
        """
        Default constructor for HH scraper.
        """
        super().__init__()
        self.wait = None
    
    def GetPrice(self, url: str, web_driver):
        try:
            if url.strip() == "" or url is None:
                return "חסר"
            
            # Navigate to the URL
            web_driver.get(url)
            
            # Wait for the price element to be present (reduced timeout)
            if self.wait is None:
                self.wait = WebDriverWait(web_driver, 7)  # Reduced from 10 to 7 seconds
            price_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.price-title span"))
            )
            
            # Extract the price text
            price_text = price_element.text.strip()
            
            # Clean the price: keep only numbers, comma, and dot
            cleaned_price = re.sub(r'[^\d,.]', '', price_text)
            
            return cleaned_price
            
        except Exception as e:
            return f"Error scraping price: {e}" 