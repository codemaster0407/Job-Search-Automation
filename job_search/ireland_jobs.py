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




def scrape_current_page(driver):
    """
    Extract job information from the current page
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        list: List of dictionaries containing job information from current page
    """
    jobs_data = []
    wait = WebDriverWait(driver, 10)
    
    try:
        # Wait for job listings to appear
        job_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card, .job-item, [class*='job'], article"))
        )
        print(f"  ✅ Found {len(job_elements)} job elements on this page")
    except TimeoutException:
        print("  ⚠️ Timeout waiting for job listings. Attempting fallback...")
        job_elements = driver.find_elements(By.TAG_NAME, "article")
        if not job_elements:
            job_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='job']")
    
    # Extract job information from each element
    for idx, job_elem in enumerate(job_elements, 1):
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
            
            print(f"  📝 Extracted job {idx}: {job_data['title'][:50]}...")
            
        except Exception as e:
            print(f"  ⚠️ Error extracting job {idx}: {str(e)}")
            continue
    
    return jobs_data


def scrape_ireland_jobs(url, max_pages=None):
    """
    Use Selenium to scrape job listings from IrishJobs.ie across multiple pages
    
    Args:
        url (str): The URL of the IrishJobs.ie search page
        max_pages (int, optional): Maximum number of pages to scrape. None = all pages
        
    Returns:
        list: List of dictionaries containing job information from all pages
    """
    # Set up Chrome options for headless browsing
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = None
    all_jobs_data = []
    page = 1
    
    try:
        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=options)
        
        print(f"🌐 Opening URL: {url}")
        driver.get(url)
        
        # Wait for initial page load
        time.sleep(3)
        
        # Main pagination loop
        while True:
            print(f"\n{'='*60}")
            print(f"� Scraping Page {page}")
            print(f"{'='*60}")
            
            # Wait for job listings to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "article, [class*='job']"))
                )
            except TimeoutException:
                print("⚠️ Timeout waiting for jobs to load on this page")
                break
            
            # Scrape current page
            page_jobs = scrape_current_page(driver)
            
            if page_jobs:
                all_jobs_data.extend(page_jobs)
                print(f"  ✅ Extracted {len(page_jobs)} jobs from page {page}")
                print(f"  📊 Total jobs collected so far: {len(all_jobs_data)}")
            else:
                print(f"  ⚠️ No jobs found on page {page}")
                break
            
            # Check if we've reached max_pages
            if max_pages and page >= max_pages:
                print(f"\n✋ Reached maximum page limit ({max_pages})")
                break
            
            # Try to find and click Next button
            try:
                # Wait for Next button to be present
                next_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Next"]'))
                )
                
                # Check if button is disabled (reached last page)
                button_classes = next_button.get_attribute('class') or ''
                parent_element = next_button.find_element(By.XPATH, '..')
                
                # Check if button or parent has disabled state
                if 'disabled' in button_classes or not next_button.is_enabled():
                    print(f"\n🏁 Reached last page (Next button is disabled)")
                    break
                
                # Check if it's actually clickable
                try:
                    # Scroll to button
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                    time.sleep(0.5)
                    
                    # Get current URL to verify page change
                    current_url = driver.current_url
                    
                    # Use JavaScript click to avoid interception issues
                    driver.execute_script("arguments[0].click();", next_button)
                    
                    # Wait for URL to change or new content to load
                    time.sleep(2)
                    
                    # Verify page changed
                    new_url = driver.current_url
                    if current_url == new_url:
                        # URL didn't change, try waiting for content to reload
                        try:
                            WebDriverWait(driver, 5).until(
                                EC.staleness_of(next_button)
                            )
                        except TimeoutException:
                            print(f"\n⚠️ Page didn't change after clicking Next button")
                            break
                    
                    page += 1
                    print(f"\n  ➡️  Navigating to page {page}...")
                    
                except Exception as e:
                    print(f"\n⚠️ Error clicking Next button: {str(e)}")
                    break
                    
            except TimeoutException:
                print(f"\n🏁 No more pages (Next button not found)")
                break
            except NoSuchElementException:
                print(f"\n🏁 No more pages (Next button doesn't exist)")
                break
            except Exception as e:
                print(f"\n⚠️ Error finding Next button: {str(e)}")
                break
        
        print(f"\n{'='*60}")
        print(f"✅ Successfully scraped {page} page(s)")
        print(f"📊 Total jobs extracted: {len(all_jobs_data)}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"❌ Critical error during scraping: {str(e)}")
        
        # If Selenium fails, get the entire page source for fallback
        if driver:
            try:
                page_source = driver.page_source
                all_jobs_data.append({
                    'uuid': 'fallback',
                    'full_page_html': page_source,
                    'note': 'Selenium extraction failed, returning full page source for LLM processing'
                })
                print("⚠️ Returning full page source for LLM processing")
            except:
                pass
    
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")
    
    return all_jobs_data


    


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


