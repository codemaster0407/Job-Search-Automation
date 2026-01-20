import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests


def scrape_url_simple(url):
    """
    Simple HTTP request to get text content (fast but won't handle JavaScript)
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: Cleaned text content from the page (None if failed)
    """
    try:
        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        print(f"🌐 Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        text_cleaned = '\n'.join(line for line in lines if line)
        
        print(f"✅ Extracted {len(text_cleaned)} characters of text")
        
        return text_cleaned
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching URL: {str(e)}")
        return None


def scrape_url_selenium(url, wait_seconds=3):
    """
    Use Selenium to scrape URL (handles JavaScript-rendered content)
    
    Args:
        url (str): The URL to scrape
        wait_seconds (int): Seconds to wait for page to load
        
    Returns:
        str: Cleaned text content from the page (None if failed)
    """
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = None
    
    try:
        print(f"🌐 Opening URL with Selenium: {url}")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        # Wait for page to load
        time.sleep(wait_seconds)
        
        # Get page source
        html = driver.page_source
        
        # Parse with BeautifulSoup for text extraction
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        text_cleaned = '\n'.join(line for line in lines if line)
        
        print(f"✅ Extracted {len(text_cleaned)} characters of text")
        
        return text_cleaned
        
    except Exception as e:
        print(f"❌ Error scraping URL: {str(e)}")
        return None
        
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")


def scrape_url_auto(url, wait_seconds=3):
    """
    Automatically choose the best method (tries simple first, falls back to Selenium)
    
    Args:
        url (str): The URL to scrape
        wait_seconds (int): Seconds to wait for Selenium if used
        
    Returns:
        str: Cleaned text content from the page (None if failed)
    """
    print(f"🔍 Auto-detecting best scraping method for: {url}\n")
    
    # Try simple HTTP request first (faster)
    result = scrape_url_simple(url)
    
    # Check if we got meaningful content
    if result and len(result) > 100:
        print("✅ Simple HTTP request was successful")
        return result
    
    # Fall back to Selenium for JavaScript-heavy sites
    print("\n⚠️ Simple request failed or returned minimal content")
    print("🔄 Switching to Selenium for JavaScript rendering...\n")
    
    return scrape_url_selenium(url, wait_seconds)


def save_scraped_data(data, output_file=None):
    """
    Save scraped data to files
    
    Args:
        data (dict): The scraped data from any scrape function
        output_file (str, optional): Base filename (without extension)
        
    Returns:
        dict: Paths to saved files
    """
    if not data:
        print("❌ No data to save")
        return None
    
    # Generate filename if not provided
    if not output_file:
        from urllib.parse import urlparse
        import re
        parsed = urlparse(data['url'])
        clean_name = re.sub(r'[^\w\s-]', '', parsed.netloc + parsed.path)
        clean_name = re.sub(r'[-\s]+', '_', clean_name)
        output_file = f"scraped_{clean_name}"[:50]  # Limit length
    
    saved_files = {}
    
    # Save HTML
    html_file = f"{output_file}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(data['html'])
    saved_files['html'] = html_file
    print(f"📄 Saved HTML to: {html_file}")
    
    # Save text
    txt_file = f"{output_file}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(data['text'])
    saved_files['text'] = txt_file
    print(f"📝 Saved text to: {txt_file}")
    
    return saved_files


# Example usage
if __name__ == "__main__":
    # Test URL
    test_url = "https://www.irishjobs.ie/ShowJob.aspx?Id=110382341"
    
    print("="*80)
    print("URL SCRAPER - Choose your method:")
    print("="*80)
    print()
    
    # Method 1: Simple (fast)
    print("METHOD 1: Simple HTTP Request")
    print("-"*80)
    result = scrape_url_simple(test_url)
    if result:
        print(f"\n📊 Preview of scraped text (first 500 chars):")
        print(result['text'][:500])
        print("...")
    print()
    
    # Method 2: Selenium (handles JS)
    print("\nMETHOD 2: Selenium (JavaScript-enabled)")
    print("-"*80)
    result_selenium = scrape_url_selenium(test_url)
    if result_selenium:
        print(f"\n📊 Preview of scraped text (first 500 chars):")
        print(result_selenium['text'][:500])
        print("...")
    print()
    
    # Optional: Save to files
    # save_scraped_data(result_selenium, "job_description")
