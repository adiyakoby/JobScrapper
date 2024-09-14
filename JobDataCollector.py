import csv
import os
from re import sub

class JobDataCollector:
    def __init__(self, job_title , jobs, csv_file_path=None):
        self.jobs = jobs
        # Default to 'jobs_data.csv' in the current directory if no path is provided
        self.csv_file_path = csv_file_path or sub(' ', '-', job_title) + '-jobs_data.csv'

    def save_to_csv(self):
        if not self.jobs:
            print("No job data to save.")
            return

        # Get headers from the first job entry
        headers = self.jobs[0].keys()

        # Check if the file already exists
        file_exists = os.path.isfile(self.csv_file_path)

        with open(self.csv_file_path, 'a' if file_exists else 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            if not file_exists:
                writer.writeheader()  # Write header only if the file is newly created
            for job in self.jobs:
                writer.writerow(job)

        print(f"Data saved to {self.csv_file_path}")