
from GdJobScarpper import JobScraper, generate_url

if __name__ == "__main__":
    scraper = JobScraper(generate_url('software engineer'))
    scraper.start_browser()
    scraper.extract_job_details()
