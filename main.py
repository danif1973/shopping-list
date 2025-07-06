import csv
import logging
from hh_scraper import HH
from rl_scraper import RL
from browser_manager import BrowserManager
from price_matrix import PriceMatrix
from store_items import StoreItems
from item import Item

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

SCRAPER_MAP = {
    'hh': HH,
    'rl': RL,
}

HH_TEST_URL = "https://shop.hazi-hinam.co.il/catalog/products/267914/4230364/%D7%9E%D7%A7%D7%9C%D7%95%D7%AA-%D7%91%D7%95%D7%A8%D7%A7%D7%A1-%D7%A4%D7%99%D7%9C%D7%95-%D7%92%D7%91%D7%99%D7%A0%D7%94-%D7%91%D7%A1%D7%92%D7%A0%D7%95%D7%9F-%D7%A6%D7%A8%D7%A4%D7%AA%D7%99"
#RL_TEST_URL = "https://www.rami-levy.co.il/he/online/search?item=7290000056845"
RL_TEST_URL = "https://www.rami-levy.co.il/he/online/search?item=100"

def main():
    browser_manager = None
    try:
        logging.info("Starting price comparison scraping process")
        
        # Initialize the browser manager
        logging.info("Initializing browser manager")
        browser_manager = BrowserManager()
        driver = browser_manager.initialize_driver()
        logging.info("Browser manager initialized successfully")

        # Read data.csv
        logging.info("Loading data from data.csv")
        with open('data.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            store_names = [col for col in reader.fieldnames if col not in ['Product', 'hh_order']]
            logging.info(f"Found stores: {store_names}")
            
            # Prepare StoreItems for each store
            store_objects = {store: StoreItems(store) for store in store_names}
            logging.info(f"Created StoreItems objects for {len(store_names)} stores")
            
            # Prepare scrapers for each store
            scrapers = {store: SCRAPER_MAP[store]() for store in store_names if store in SCRAPER_MAP}
            logging.info(f"Initialized scrapers for stores: {list(scrapers.keys())}")
            
            # Process each row (product)
            row_count = 0
            for row in reader:
                row_count += 1
                product_name = row['Product']
                hh_order = row.get('hh_order', '')
                if hh_order and hh_order.strip():
                    try:
                        hh_order = int(hh_order)
                    except ValueError:
                        hh_order = None
                else:
                    hh_order = None
                logging.info(f"Processing product {row_count}: {product_name} (order: {hh_order})")
                
                for store in store_names:
                    url = row[store].strip()
                    price = None
                    
                    if url and store in scrapers:
                        logging.info(f"Scraping {store} for product '{product_name}' - URL: {url}")
                        price = scrapers[store].GetPrice(url, driver)
                        logging.info(f"Scraper result for {store} - Product: '{product_name}' - Price: {price}")
                    else:
                        if not url:
                            logging.warning(f"No URL provided for {store} - Product: '{product_name}'")
                        if store not in scrapers:
                            logging.warning(f"No scraper available for store: {store}")
                    
                    item = Item(product_name, price, hh_order)
                    store_objects[store].add_item(item)
                    logging.info(f"Added item to {store}: {product_name} = {price} (order: {hh_order})")
            
            logging.info(f"Completed processing {row_count} products")
        
        # Build PriceMatrix
        logging.info("Building price matrix")
        price_matrix = PriceMatrix()
        for store in store_names:
            price_matrix.add_store(store_objects[store])
        logging.info(f"Price matrix built with {len(store_names)} stores")
        
        # Print and save results
        price_matrix.Print()
        
        logging.info("Saving results to prices.csv")
        price_matrix.Save()
        logging.info("Results saved successfully")
               
    except Exception as e:
        logging.error(f"Error during scraping process: {e}")
        print(f"Error: {e}")
    finally:
        # Close the driver when done
        if browser_manager:
            logging.info("Closing browser manager")
            browser_manager.close_driver()
            logging.info("Browser manager closed")

if __name__ == "__main__":
    main() 