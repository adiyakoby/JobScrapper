from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from re import sub

def generate_url(job_title, location = 'israel'):
    return f"https://www.glassdoor.com/Job/{location}-{sub(' ', '-', job_title)}-jobs-SRCH_IL.0,6_IN119_KO7,24.htm?sortBy=date_desc"

class JobScraper:
    def __init__(self, url):
        # Set up Chrome options
        self.chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-gpu")

        # Use ChromeDriver Manager to handle driver
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.url = url

    def start_browser(self):
        self.driver.get(self.url)

    def handle_pop_up(self):
        try:
            close_button = WebDriverWait(self.driver, random.choice([2,2.5,3,3.5,4,4.5])).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.CloseButton'))
            )
            if close_button.is_displayed():
                close_button.click()
            print("Closed the pop-up message.")
        except Exception:
            pass

    def click_load_more(self):
        try:
            load_more_button = WebDriverWait(self.driver, random.choice([2,2.5,3,3.5,4,4.5])).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="load-more"]'))
            )
            load_more_button.click()
            print("Clicked the 'Show more jobs' button.")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"No 'Show more jobs' button or error clicking it: {e}")
            return False

    def click_show_more_description(self):
        try:
            show_more_button = WebDriverWait(self.driver, random.choice([2,2.5,3,3.5,4,4.5])).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.JobDetails_showMore___Le6L'))
            )
            show_more_button.click()
            print("Clicked the 'Show more' button in the job description.")
            time.sleep(2) # Wait for the description to expand
        except Exception:
            pass

    def extract_job_details(self, pages = 1):
        for _ in range(pages):
            try:
                # Wait for job cards to be present
                job_elements = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-test="jobListing"]'))
                )
                
                print(f"Found {len(job_elements)} job listings.")
                
                for job in job_elements:
                    try:
                        # Extract job title
                        job_title = job.find_element(By.CSS_SELECTOR, 'a[data-test="job-title"]').text
                        print(f"Job Title: {job_title}")

                        # Extract company name
                        company_name = job.find_element(By.CSS_SELECTOR, '.EmployerProfile_compactEmployerName__LE242').text
                        print(f"Company Name: {company_name}")

                        # Extract job location
                        location = job.find_element(By.CSS_SELECTOR, '[data-test="emp-location"]').text
                        print(f"Location: {location}")

                        # Extract job link
                        job_link = job.find_element(By.CSS_SELECTOR, 'a[data-test="job-title"]').get_attribute('href')
                        print(f"Job Link: {job_link}")

                        # Click on the job link
                        job.click()
  
                        self.handle_pop_up()
                        self.click_show_more_description()

                        # Wait for job description to be present with dynamic class name
                        description_div = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class^="JobDetails_jobDescription"]'))
                        )
                        description_text = description_div.text
                        print(f"Job Description:\n{description_text}")

                        # Print a separator between jobs
                        print("-" * 40)
                    except Exception as e:
                        print(f"Error extracting job data: {e}")

                # Try to click the "Show more jobs" button, break the loop if not available
                if not self.click_load_more():
                    break

            finally:
                # Quit the browser after scraping
                self.driver.quit()

if __name__ == "__main__":
    url = "https://www.glassdoor.com/Job/israel-software-engineer-jobs-SRCH_IL.0,6_IN119_KO7,24.htm?sortBy=date_desc"
    scraper = JobScraper(url)
    scraper.start_browser()
    scraper.extract_job_details()
