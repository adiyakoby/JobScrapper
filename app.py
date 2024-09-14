
from GdJobScarpper import JobScraper, generate_url
from JobDataCollector import JobDataCollector

if __name__ == "__main__":
    job_titles = ['software engineer', 'fullstack', 'fullstack developer', 'junior', 'junior developer']

    # for job_title in job_titles:
    #     scraper = JobScraper(generate_url(job_title))
    
    #     scraper.start_browser()
    #     jobs = scraper.extract_job_details()
    #     data_colletor = JobDataCollector(job_title,jobs)
    #     data_colletor.save_to_csv()
    scraper = JobScraper(generate_url(job_titles[1]))

    scraper.start_browser()
    jobs = scraper.extract_job_details()
    data_colletor = JobDataCollector(job_titles[1],jobs)
    data_colletor.save_to_csv()