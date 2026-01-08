import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Load environment variables
load_dotenv()


def scrape_ireland_jobs(url):
    """
    Use Selenium to scrape job listings from IrishJobs.ie
    
    Args:
        url (str): The URL of the IrishJobs.ie search page
        
    Returns:
        list: List of dictionaries containing job information
    """
    # Set up Chrome options for headless browsing
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = None
    jobs_data = []
    
    try:
        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=options)
        
        print(f"🌐 Opening URL: {url}")
        driver.get(url)
        
        # Wait for the page to load
        time.sleep(3)
        
        # Wait for job listings to appear
        wait = WebDriverWait(driver, 10)
        
        # Try to find job cards/listings
        # Note: You may need to inspect the actual page to get the correct selectors
        try:
            job_elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card, .job-item, [class*='job'], article"))
            )
            print(f"✅ Found {len(job_elements)} potential job elements")
        except TimeoutException:
            print("⚠️ Timeout waiting for job listings. Attempting to extract all content...")
            job_elements = driver.find_elements(By.TAG_NAME, "article")
            if not job_elements:
                job_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='job']")
        
        # Extract job information from each element
        for idx, job_elem in enumerate(job_elements[:20], 1):  # Limit to first 20 jobs
            try:
                job_data = {
                    'uuid': f"job_{idx}_{int(time.time())}",
                    'title': None,
                    'description': None,
                    'application_link': None,
                    'company': None,
                    'location': None,
                    'raw_html': None
                }
                
                # Try to extract title
                try:
                    title_elem = job_elem.find_element(By.CSS_SELECTOR, "h2, h3, [class*='title'], [class*='job-title']")
                    job_data['title'] = title_elem.text.strip()
                except NoSuchElementException:
                    job_data['title'] = "Title not found"
                
                # Try to extract description/summary
                try:
                    desc_elem = job_elem.find_element(By.CSS_SELECTOR, "p, [class*='description'], [class*='summary']")
                    job_data['description'] = desc_elem.text.strip()
                except NoSuchElementException:
                    job_data['description'] = job_elem.text.strip()[:500]  # First 500 chars
                
                # Try to extract application link
                try:
                    link_elem = job_elem.find_element(By.CSS_SELECTOR, "a[href*='job'], a[href*='apply']")
                    job_data['application_link'] = link_elem.get_attribute('href')
                except NoSuchElementException:
                    try:
                        # Try to get any link
                        link_elem = job_elem.find_element(By.TAG_NAME, "a")
                        job_data['application_link'] = link_elem.get_attribute('href')
                    except NoSuchElementException:
                        job_data['application_link'] = "Link not found"
                
                # Store raw HTML for LLM processing
                job_data['raw_html'] = job_elem.get_attribute('outerHTML')
                
                jobs_data.append(job_data)
                
                print(f"📝 Extracted job {idx}: {job_data['title'][:50]}...")
                
            except Exception as e:
                print(f"⚠️ Error extracting job {idx}: {str(e)}")
                continue
        
        print(f"\n✅ Successfully extracted {len(jobs_data)} jobs")
        
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        
        # If Selenium fails, get the entire page source for fallback
        if driver:
            page_source = driver.page_source
            jobs_data.append({
                'uuid': 'fallback',
                'full_page_html': page_source,
                'note': 'Selenium extraction failed, returning full page source for LLM processing'
            })
            print("⚠️ Returning full page source for LLM processing")
    
    finally:
        if driver:
            driver.quit()
    
    return jobs_data


def main():
    """Main function to run the job scraper"""
    # The target URL
    target_url = "https://www.irishjobs.ie/jobs/data-scientist?searchOrigin=membersarea&q=data%20scientist%20"
    
    print(f"🔍 Starting job search for: {target_url}")
    print("-" * 80)
    
    # Perform the scraping
    raw_results = scrape_ireland_jobs(target_url)
    
    if raw_results:
        print("\n" + "=" * 80)
        print("RAW SCRAPING RESULTS (stored in variable)")
        print("=" * 80)
        print(f"\nJobs found: {len(raw_results)}")
        
        # Display a preview of the results
        for idx, job in enumerate(raw_results[:3], 1):
            print(f"\n--- Job {idx} ---")
            print(f"UUID: {job.get('uuid', 'N/A')}")
            print(f"Title: {job.get('title', 'N/A')}")
            print(f"Description: {job.get('description', 'N/A')[:150]}...")
            print(f"Application Link: {job.get('application_link', 'N/A')}")
        
        if len(raw_results) > 3:
            print(f"\n... and {len(raw_results) - 3} more jobs")
        
        print("\n" + "=" * 80)
        print("✅ Results stored in 'raw_results' variable")
        print("📝 Next step: Use LLM to extract and structure the job information")
        print("=" * 80)
        
        return raw_results
    else:
        print("❌ Failed to retrieve job listings")
        return None


if __name__ == "__main__":
    results = main()
