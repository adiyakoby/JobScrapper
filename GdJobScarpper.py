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
    loc_len = len(location)
    title_len = len(job_title)
    return f"https://www.glassdoor.com/Job/{location}-{sub(' ', '-', job_title)}-jobs-SRCH_IL.0,{loc_len}_IN119_KO{loc_len+1},{loc_len+1+title_len}.htm?sortBy=date_desc"


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
            close_button = WebDriverWait(self.driver, random.randrange(1, 3)).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.CloseButton'))
            )
            if close_button.is_displayed():
                close_button.click()
            print("Closed the pop-up message.")
        except Exception:
            pass

    def click_load_more(self):
        try:
            load_more_button = WebDriverWait(self.driver, random.randrange(1, 3)).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="load-more"]'))
            )
            load_more_button.click()
            # print("Clicked the 'Show more jobs' button.")
            time.sleep(random.random()+1)
            return True
        except Exception as e:
            print(f"No 'Show more jobs' button or error clicking it: {e}")
            return False

    def click_show_more_description(self):
        try:
            show_more_button = WebDriverWait(self.driver, random.randrange(1, 3)).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class^='JobDetails_showMore']"))
            ) 
            show_more_button.click()
            print("Clicked the 'Show more' button in the job description.")
            time.sleep(random.random()+1) # Wait for the description to expand
        except Exception:
            pass

    def extract_job_details(self, pages = 1):
        jobs_data = []

        for _ in range(pages):
            try:
                # Wait for job cards to be present
                job_elements = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-test="jobListing"]'))
                )
                
                print(f"Found {len(job_elements)} job listings.")
                
                for job in job_elements:
                    try:
                        job_title = job.find_element(By.CSS_SELECTOR, 'a[data-test="job-title"]').text
                        company_name = job.find_element(By.CSS_SELECTOR, 'div[class^="EmployerProfile_employerNameContainer"]').text
                        location = job.find_element(By.CSS_SELECTOR, '[data-test="emp-location"]').text
                        job_link = job.find_element(By.CSS_SELECTOR, 'a[data-test="job-title"]').get_attribute('href')
                        job_age = job.find_element(By.CSS_SELECTOR, 'div[class^="JobCard_listingAge"]').text

                        job.click()
                        self.handle_pop_up()
                        self.click_show_more_description()

                        description_div = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class^="JobDetails_jobDescription"]'))
                        )
                        description_text = description_div.text

                        job_data = {
                            "Job Title": job_title,
                            "Company Name": company_name,
                            "Location": location,
                            "Job Link": job_link,
                            "Job Age": job_age,
                            "Job Description": description_text
                        }

                        jobs_data.append(job_data)

                         # Print job details
                        # print(f"Job Title: {job_title}")
                        # print(f"Company Name: {company_name}")
                        # print(f"Location: {location}")
                        # print(f"Job Link: {job_link}")
                        # print(f"Job Description:\n{description_text}")
                        # print("-" * 60)
            
                    except Exception as e:
                        print(f"Error extracting job data: {e}")


                # Try to click the "Show more jobs" button, break the loop if not available
                if not self.click_load_more():
                    break

            finally:
                # Quit the browser after scraping
                self.driver.quit()
                return jobs_data
        return jobs_data

