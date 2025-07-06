from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from store import Store
from bs4 import BeautifulSoup
import time
import re

class RL(Store):
    """
    Price scraper for RamiLevy grocery store website.
    """
    
    def __init__(self):
        """
        Default constructor for RL scraper.
        """
        super().__init__()
        self.wait = None
    
    def GetPrice(self, url: str, web_driver):
        # Try once, then retry once if there's an error
        attempt = 0
        max_attempts = 2
        
        while attempt < max_attempts:
            try:
                if url.strip() == "" or url is None:
                    return "חסר"
                
                # Navigate to the URL
                web_driver.get(url)
                
                # Wait for the main product modal to be present
                if self.wait is None:
                    self.wait = WebDriverWait(web_driver, 7)
                
                # Wait for the main-product-modal to appear
                self.wait.until(
                    EC.presence_of_element_located((By.ID, "main-product-modal"))
                )
                
                # Get the page source after JavaScript has loaded
                page_source = web_driver.page_source
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Find the main product modal
                main_modal = soup.find('div', id='main-product-modal')
                
                if main_modal:
                    # Find the price div within the main modal
                    price_div = main_modal.find('div', class_='xl2-text mr-4 blue line-height-1-2 d-flex align-items-baseline price-text')
                    
                    if price_div:
                        # Find all spans with class "sr-only" within the price div
                        sr_only_spans = price_div.find_all('span', class_='sr-only')
                        
                        # Collect all valid prices
                        prices = []
                        
                        # Check all sr-only spans for price text
                        for sr_span in sr_only_spans:
                            # Get text from the sr_span itself
                            sr_text = sr_span.get_text(strip=True)
                            
                            # Check if the text contains price format (numbers with dot or comma)
                            if re.search(r'\d+[.,]\d+', sr_text):
                                # Clean the price: keep only numbers, comma, and dot
                                cleaned_price = re.sub(r'[^\d,.]', '', sr_text)
                                # Convert to float for comparison (replace comma with dot)
                                try:
                                    price_float = float(cleaned_price.replace(',', '.'))
                                    prices.append(price_float)
                                except ValueError:
                                    continue
                        
                        # Return the lowest price if any found
                        if prices:
                            lowest_price = min(prices)
                            # Format with exactly 2 decimal places
                            return f"{lowest_price:.2f}"
                        else:
                            return "Price span not found"
                    else:
                        return "Price div not found"
                else:
                    return "Main product modal not found"
                
            except Exception as e:
                attempt += 1
                if attempt < max_attempts:  # Still have retries left
                    print(f"Attempt {attempt} failed for URL {url}: {e}")
                    print(f"Waiting 5 seconds before retry {attempt + 1}...")
                    time.sleep(5)
                    continue  # Try again
                else:  # No more retries left
                    return f"Error scraping price: {e}"
    
   