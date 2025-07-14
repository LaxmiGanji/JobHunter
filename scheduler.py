import schedule
import time
import threading
from datetime import datetime, time as dt_time
from typing import Optional
from database import DatabaseManager
from email_sender import EmailSender
from job_scraper import JobScraper

class JobScheduler:
    def __init__(self, job_role: str, location: str, job_type: str, experience_years: str, 
                 email: str, preferred_time: dt_time, db_manager: DatabaseManager, 
                 email_sender: EmailSender, job_scraper: JobScraper):
        self.job_role = job_role
        self.location = location
        self.job_type = job_type
        self.experience_years = experience_years
        self.email = email
        self.preferred_time = preferred_time
        self.db_manager = db_manager
        self.email_sender = email_sender
        self.job_scraper = job_scraper
        self.is_running = False
        self.stop_event = threading.Event()
        
    def schedule_job(self):
        """Schedule the daily job search."""
        # Clear any existing scheduled jobs
        schedule.clear()
        
        # Schedule the job for the specified time
        time_str = self.preferred_time.strftime("%H:%M")
        schedule.every().day.at(time_str).do(self.run_job_search)
        
        print(f"Job search scheduled for {time_str} daily")
    
    def run_job_search(self):
        """Run the job search and send email."""
        try:
            print(f"Running scheduled job search for {self.email}")
            
            # Build search query
            query = self.job_scraper.build_search_query(
                self.job_role, self.location, self.job_type, self.experience_years
            )
            
            # Search for jobs
            jobs = self.job_scraper.search_jobs(query)
            
            if jobs:
                # Save jobs to database
                for job in jobs:
                    self.db_manager.save_job(
                        title=job['title'],
                        link=job['link'],
                        email=self.email,
                        source=job['source'],
                        search_query=query
                    )
                
                # Send email
                success = self.email_sender.send_job_email(
                    self.email, jobs, self.job_role, self.location
                )
                
                if success:
                    print(f"Successfully sent {len(jobs)} jobs to {self.email}")
                else:
                    print(f"Failed to send email to {self.email}")
            else:
                print(f"No jobs found for {self.email}")
                
                # Send empty results email
                self.email_sender.send_job_email(
                    self.email, [], self.job_role, self.location
                )
                
        except Exception as e:
            print(f"Error in scheduled job search: {e}")
    
    def run(self):
        """Main scheduler loop."""
        self.is_running = True
        self.schedule_job()
        
        print("Scheduler started...")
        
        while not self.stop_event.is_set():
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"Scheduler error: {e}")
                time.sleep(60)
        
        print("Scheduler stopped")
        self.is_running = False
    
    def stop(self):
        """Stop the scheduler."""
        self.stop_event.set()
        schedule.clear()
        print("Scheduler stop signal sent")
    
    def get_next_run_time(self) -> Optional[datetime]:
        """Get the next scheduled run time."""
        jobs = schedule.get_jobs()
        if jobs:
            return jobs[0].next_run
        return None
    
    def is_scheduled(self) -> bool:
        """Check if a job is currently scheduled."""
        return len(schedule.get_jobs()) > 0
    
    def get_schedule_info(self) -> dict:
        """Get information about the current schedule."""
        return {
            'is_running': self.is_running,
            'is_scheduled': self.is_scheduled(),
            'next_run': self.get_next_run_time(),
            'job_role': self.job_role,
            'location': self.location,
            'job_type': self.job_type,
            'email': self.email,
            'preferred_time': self.preferred_time.strftime("%H:%M")
        }
