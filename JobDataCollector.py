import csv


class JobDataCollector:
    def __init__(self, jobs, csv_file_path):
        self.jobs = jobs
        self.csv_file_path = csv_file_path

    def save_to_csv(self):
        if not self.jobs:
            print("No job data to save.")
            return

        # Get headers from the first job entry
        headers = self.jobs[0].keys()

        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for job in self.jobs:
                writer.writerow(job)
        
        print(f"Data saved to {self.csv_file_path}")
