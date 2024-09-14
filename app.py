from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--window-size=1920,1080")  # Set viewport size
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

# Use ChromeDriver Manager to handle driver
service = Service(ChromeDriverManager().install())

# Start the browser
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the URL
url = "https://www.glassdoor.com/Job/israel-software-engineer-jobs-SRCH_IL.0,6_IN119_KO7,24.htm?sortBy=date_desc"

# Load the page
driver.get(url)


# Function to click the "Show more jobs" button if available
def click_load_more():
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="load-more"]'))
        )
        load_more_button.click()
        print("Clicked the 'Show more jobs' button.")
        time.sleep(2)  # Wait for jobs to load after clicking the button
        return True
    except Exception as e:
        print(f"No 'Show more jobs' button or error clicking it: {e}")
        return False



# Function to handle any pop-up
def handle_pop_up():
    try:
        close_button = WebDriverWait(driver, random.choice([2,2.5,3,3.5,4,4.5,5])).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.CloseButton'))
        )
        if close_button.is_displayed():
            close_button.click()
        print("Closed the pop-up message.")
    except Exception as e:
        # print(f"No pop-up found or error closing pop-up: {e}")
        pass


loads = 2
try:
    for _ in range(loads):
        # Wait for job cards to be present
        job_elements = WebDriverWait(driver, 20).until(
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
                # job.find_element(By.CSS_SELECTOR, 'a[data-test="job-title"]').click()
                job.click()
                # # Wait for the job details to load
                # WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-brandviews="MODULE:n=joblisting-description:eid=1217:jlid=1009438372698"]'))
                # )

                # Wait for job description to be present with dynamic class name
                description_div = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class^="JobDetails_jobDescription"]'))
                )
                description_text = description_div.text
                print(f"Job Description:\n{description_text}")
                
                # Handle the pop-up if it appears after clicking
                handle_pop_up()

                # Extract job description
                # description_div = driver.find_element(By.CSS_SELECTOR, 'div[data-brandviews="MODULE:n=joblisting-description:eid=1217:jlid=1009438372698"]')
                # description_text = description_div.text
                print(f"Job Description:\n{'none'}")

                # Here, you would send `description_text` to GPT for summarization

                # Go back to the job listings page
                # driver.back()
                
                # Wait for the page to reload and job cards to be available again
                # WebDriverWait(driver, 10).until(
                #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-test="jobListing"]'))
                # )

                # Print a separator between jobs
                print("-" * 40)
            except Exception as e:
                print(f"Error extracting job data: {e}")

            # Try to click the "Show more jobs" button, break the loop if not available
        if not click_load_more():
            break

       

finally:
    # Quit the browser after scraping
    driver.quit()
