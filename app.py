
from GdJobScarpper import JobScraper, generate_url
from JobDataCollector import JobDataCollector

if __name__ == "__main__":
    scraper = JobScraper(generate_url('software engineer'))
    
    scraper.start_browser()
    jobs = scraper.extract_job_details()
    data_colletor = JobDataCollector(jobs)
    data_colletor.save_to_csv()
