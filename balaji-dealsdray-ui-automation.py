import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os
import re
from datetime import datetime

# Function to sanitize URL for use in filenames
def sanitize_filename(url):
    sanitized = re.sub(r'https?://', '', url)
    sanitized = re.sub(r'[<>:"/\\|?*]', '', sanitized)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized

# Function to get current date and time
def get_current_datetime():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# Fetch the XML content from the sitemap URL
sitemap_url = 'https://www.getcalley.com/page-sitemap.xml'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(sitemap_url, headers=headers)

if response.status_code == 200:
    root = ET.fromstring(response.content)
    urls = [loc.text for loc in root.findall(".//{*}loc")]
    valid_urls = [url for url in urls if not url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf'))]
    top_five_urls = valid_urls[:5]
    
    # Define resolutions for desktop and mobile
    desktop_resolutions = [(1920, 1080), (1366, 768), (1536, 864)]
    mobile_resolutions = [(360, 640), (414, 896), (375, 667)]
    
    # Create directories for screenshots
    for res in desktop_resolutions:
        width, height = res
        os.makedirs(f'screenshots/desktop/{width}x{height}/chrome', exist_ok=True)
        os.makedirs(f'screenshots/desktop/{width}x{height}/firefox', exist_ok=True)
    for res in mobile_resolutions:
        width, height = res
        os.makedirs(f'screenshots/mobile/{width}x{height}/chrome', exist_ok=True)
        os.makedirs(f'screenshots/mobile/{width}x{height}/firefox', exist_ok=True)
    
    for i, url in enumerate(top_five_urls):
        sanitized_url = sanitize_filename(url)
        current_datetime = get_current_datetime()
        
        # Desktop Screenshots
        chrome_desktop_options = ChromeOptions()
        firefox_desktop_options = FirefoxOptions()
        
        chrome_desktop_service = ChromeService(ChromeDriverManager().install())
        firefox_desktop_service = FirefoxService(GeckoDriverManager().install())
        
        chrome_desktop_driver = webdriver.Chrome(service=chrome_desktop_service, options=chrome_desktop_options)
        firefox_desktop_driver = webdriver.Firefox(service=firefox_desktop_service, options=firefox_desktop_options)
        
        for res in desktop_resolutions:
            width, height = res
            
            # Open URL in Chrome and capture screenshot (Desktop)
            chrome_desktop_driver.set_window_size(width, height)
            chrome_desktop_driver.get(url)
            chrome_screenshot_path = f'screenshots/desktop/{width}x{height}/chrome/{sanitized_url}_{current_datetime}.png'
            chrome_desktop_driver.save_screenshot(chrome_screenshot_path)
            
            # Open URL in Firefox and capture screenshot (Desktop)
            firefox_desktop_driver.set_window_size(width, height)
            firefox_desktop_driver.get(url)
            firefox_screenshot_path = f'screenshots/desktop/{width}x{height}/firefox/{sanitized_url}_{current_datetime}.png'
            firefox_desktop_driver.save_screenshot(firefox_screenshot_path)
            
            print(f'Desktop screenshots saved for {url} at resolution {width}x{height}')
        
        chrome_desktop_driver.quit()
        firefox_desktop_driver.quit()
        
        # Mobile Screenshots
        chrome_mobile_options = ChromeOptions()
        firefox_mobile_options = FirefoxOptions()
        
        chrome_mobile_options.add_argument(f'user-agent=Mozilla/5.0 (Windows Phone; Android {height}; {width}x{height}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36')
        firefox_mobile_options.set_preference("general.useragent.override", f"Mozilla/5.0 (Windows Phone; Android {height}; {width}x{height}) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Mobile Safari/537.36")
        
        chrome_mobile_service = ChromeService(ChromeDriverManager().install())
        firefox_mobile_service = FirefoxService(GeckoDriverManager().install())
        
        chrome_mobile_driver = webdriver.Chrome(service=chrome_mobile_service, options=chrome_mobile_options)
        firefox_mobile_driver = webdriver.Firefox(service=firefox_mobile_service, options=firefox_mobile_options)
        
        for res in mobile_resolutions:
            width, height = res
            
            # Open URL in Chrome and capture screenshot (Mobile)
            chrome_mobile_driver.set_window_size(width, height)
            chrome_mobile_driver.get(url)
            chrome_screenshot_path = f'screenshots/mobile/{width}x{height}/chrome/{sanitized_url}_{current_datetime}.png'
            chrome_mobile_driver.save_screenshot(chrome_screenshot_path)
            
            # Open URL in Firefox and capture screenshot (Mobile)
            firefox_mobile_driver.set_window_size(width, height)
            firefox_mobile_driver.get(url)
            firefox_screenshot_path = f'screenshots/mobile/{width}x{height}/firefox/{sanitized_url}_{current_datetime}.png'
            firefox_mobile_driver.save_screenshot(firefox_screenshot_path)
            
            print(f'Mobile screenshots saved for {url} at resolution {width}x{height}')
        
        chrome_mobile_driver.quit()
        firefox_mobile_driver.quit()

else:
    print(f"Failed to retrieve sitemap: {response.status_code}")
