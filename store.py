from abc import ABC, abstractmethod

class Store(ABC):
    """
    Abstract base class for store scrapers.
    All store-specific scrapers should inherit from this class.
    """
    
    def __init__(self):
        """
        Default constructor for store scrapers.
        """
        pass
    
    @abstractmethod
    def GetPrice(self, url: str, web_driver):
        """
        Abstract method to extract price from a product page URL.
        Must be implemented by each store-specific scraper.
        
        Args:
            url (str): The URL of the product page to scrape
            web_driver: WebDriver instance to use
            
        Returns:
            str: The extracted price text from the page
        """
        pass 