from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import tempfile
import uuid

class BrowserManager:
    """
    Manages Chrome WebDriver instance for web scraping.
    """
    
    def __init__(self):
        """
        Initialize the BrowserManager.
        """
        self.driver = None
        self.user_data_dir = None
    
    def initialize_driver(self):
        """
        Initialize the Chrome WebDriver.
        """
        if self.driver is None:
            # Set environment variables to suppress Chrome logging
            os.environ['WDM_LOG_LEVEL'] = '0'
            os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
            
            # Create unique user data directory for this instance
            self.user_data_dir = os.path.join(tempfile.gettempdir(), f"chrome_profile_{uuid.uuid4().hex[:8]}")
            
            # Set up Chrome options for headless browsing
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Use unique user data directory
            chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")
            
            # GPU and graphics suppression
            chrome_options.add_argument("--disable-gpu-sandbox")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-gpu-compositing")
            chrome_options.add_argument("--disable-gpu-rasterization")
            chrome_options.add_argument("--disable-gpu-process-crash-limit")
            chrome_options.add_argument("--disable-gpu-process")
            chrome_options.add_argument("--disable-accelerated-2d-canvas")
            chrome_options.add_argument("--disable-accelerated-jpeg-decoding")
            chrome_options.add_argument("--disable-accelerated-mjpeg-decode")
            chrome_options.add_argument("--disable-accelerated-video-decode")
            chrome_options.add_argument("--disable-accelerated-video-encode")
            chrome_options.add_argument("--disable-gpu-memory-buffer-compositor-resources")
            chrome_options.add_argument("--disable-gpu-memory-buffer-video-frames")
            chrome_options.add_argument("--disable-gpu-vsync")
            chrome_options.add_argument("--disable-oop-rasterization")
            chrome_options.add_argument("--disable-zero-copy")
            
            # Suppress warnings and log messages
            chrome_options.add_argument("--log-level=3")  # Only show fatal errors
            chrome_options.add_argument("--silent")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--disable-remote-fonts")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript-harmony-shipping")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            
            # Disable Google services that cause warnings
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--disable-translate")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            
            # Additional suppression options
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
            chrome_options.add_argument("--disable-site-isolation-trials")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-background-networking")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-client-side-phishing-detection")
            chrome_options.add_argument("--disable-component-extensions-with-background-pages")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-domain-reliability")
            chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")
            chrome_options.add_argument("--disable-hang-monitor")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            chrome_options.add_argument("--disable-prompt-on-repost")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--force-color-profile=srgb")
            chrome_options.add_argument("--metrics-recording-only")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--password-store=basic")
            chrome_options.add_argument("--use-mock-keychain")
            
            # Add experimental options to suppress logging
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option('detach', True)
            
            # Set up Chrome service with local chromedriver
            chromedriver_path = os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe")
            service = Service(executable_path=chromedriver_path, log_output=os.devnull)
            
            # Initialize the WebDriver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return self.driver
    
    def get_driver(self):
        """
        Get the current driver instance.
        """
        if self.driver is None:
            return self.initialize_driver()
        return self.driver
    
    def close_driver(self):
        """
        Close the WebDriver instance and clean up user data directory.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
            
            # Clean up the user data directory
            if self.user_data_dir and os.path.exists(self.user_data_dir):
                try:
                    import shutil
                    shutil.rmtree(self.user_data_dir)
                except Exception as e:
                    # Log but don't fail if cleanup fails
                    print(f"Warning: Could not clean up user data directory {self.user_data_dir}: {e}") 