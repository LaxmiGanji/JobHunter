import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.gmail_user = os.getenv("GMAIL_USER", "")
        self.gmail_password = os.getenv("GMAIL_PASSWORD", "")
    
    def send_job_email(self, recipient_email: str, jobs: List[Dict], job_role: str, location: str) -> bool:
        """Send job listings via email."""
        if not self.gmail_user or not self.gmail_password:
            print("Gmail credentials not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = recipient_email
            msg['Subject'] = f"🤖 Daily Job Updates: {job_role} in {location}"
            
            # Create email body
            body = self._create_email_body(jobs, job_role, location)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_user, self.gmail_password)
                server.send_message(msg)
            
            print(f"Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _create_email_body(self, jobs: List[Dict], job_role: str, location: str) -> str:
        """Create HTML email body with job listings."""
        current_date = datetime.now().strftime("%B %d, %Y")
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #f4f4f4; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .job-item {{ border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px; }}
                .job-title {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }}
                .job-link {{ color: #3498db; text-decoration: none; }}
                .job-link:hover {{ text-decoration: underline; }}
                .job-source {{ color: #7f8c8d; font-size: 14px; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🤖 Your Daily Job Updates</h2>
                <p><strong>Search:</strong> {job_role} in {location}</p>
                <p><strong>Date:</strong> {current_date}</p>
                <p><strong>Jobs Found:</strong> {len(jobs)}</p>
            </div>
        """
        
        if jobs:
            html_body += "<h3>📋 Job Listings:</h3>"
            
            for i, job in enumerate(jobs, 1):
                html_body += f"""
                <div class="job-item">
                    <div class="job-title">{i}. {job['title']}</div>
                    <p><a href="{job['link']}" class="job-link" target="_blank">🔗 View Job Application</a></p>
                    <p class="job-source">📍 Source: {job['source']}</p>
                </div>
                """
        else:
            html_body += """
            <div class="job-item">
                <p>No new job listings found for your search criteria today.</p>
                <p>Try adjusting your search parameters or check back tomorrow!</p>
            </div>
            """
        
        html_body += """
            <div class="footer">
                <p>Sent by your AI Job Agent 🤖</p>
                <p>This is an automated email. Please do not reply.</p>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def send_test_email(self, recipient_email: str) -> bool:
        """Send a test email to verify configuration."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = recipient_email
            msg['Subject'] = "🤖 AI Job Agent - Test Email"
            
            body = """
            <html>
            <body>
                <h2>Test Email from AI Job Agent</h2>
                <p>This is a test email to verify that your email configuration is working correctly.</p>
                <p>If you received this email, your AI Job Agent is ready to send you job updates!</p>
                <br>
                <p>Sent by your AI Job Agent 🤖</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_user, self.gmail_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending test email: {e}")
            return False
