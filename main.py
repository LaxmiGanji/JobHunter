import streamlit as st
import pandas as pd
import sqlite3
import threading
import time
from datetime import datetime, timedelta
import os
import json
from database import DatabaseManager
from email_sender import EmailSender
from job_scraper import JobScraper
from scheduler import JobScheduler

# Initialize session state
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = None
if 'scheduler_thread' not in st.session_state:
    st.session_state.scheduler_thread = None
if 'jobs_found' not in st.session_state:
    st.session_state.jobs_found = []

# Initialize components
db_manager = DatabaseManager()
email_sender = EmailSender()
job_scraper = JobScraper()

def main():
    st.title("🤖 AI Job Agent")
    st.markdown("Your personal AI assistant for finding and tracking job opportunities")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Job Search", "📊 Job Logs", "⚙️ Settings"])
    
    with tab1:
        job_search_tab()
    
    with tab2:
        job_logs_tab()
    
    with tab3:
        settings_tab()

def job_search_tab():
    st.header("Job Search Configuration")
    
    with st.form("job_search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            job_role = st.text_input("🎯 Job Role", placeholder="e.g., AI Full Stack Developer")
            location = st.text_input("🌍 Preferred Location", placeholder="e.g., Remote, India")
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
        
        with col2:
            job_type = st.selectbox("🎓 Job Type", ["Internship", "Fresher Job", "Experience"])
            
            if job_type == "Experience":
                experience_years = st.text_input("Years of Experience", placeholder="e.g., 1-3, 3-5, 5+")
            else:
                experience_years = ""
            
            preferred_time = st.time_input("⏰ Preferred Email Time", value=None)
        
        submit_button = st.form_submit_button("🔍 Search Jobs Now")
        schedule_button = st.form_submit_button("📅 Schedule Daily Search")
        
        if submit_button:
            if job_role and location and email:
                search_jobs_now(job_role, location, job_type, experience_years, email)
            else:
                st.error("Please fill in all required fields (Job Role, Location, Email)")
        
        if schedule_button:
            if job_role and location and email and preferred_time:
                schedule_daily_search(job_role, location, job_type, experience_years, email, preferred_time)
            else:
                st.error("Please fill in all fields including preferred time for scheduling")

def search_jobs_now(job_role, location, job_type, experience_years, email):
    with st.spinner("Searching for jobs..."):
        try:
            # Build search query
            query = job_scraper.build_search_query(job_role, location, job_type, experience_years)
            
            # Search for jobs
            jobs = job_scraper.search_jobs(query)
            
            if jobs:
                st.success(f"Found {len(jobs)} job opportunities!")
                
                # Show note about demo listings
                st.info("💡 **Demo Mode**: These are sample job listings. The links will take you to the job site's search page with your criteria. In production, the system would fetch real job postings from LinkedIn, Indeed, Glassdoor, and other job sites.")
                
                # Display jobs
                for i, job in enumerate(jobs, 1):
                    st.markdown(f"**{i}. {job['title']}**")
                    st.markdown(f"🔗 [Search for Similar Jobs]({job['link']})")
                    st.markdown(f"📍 Source: {job['source']}")
                    st.markdown("---")
                
                # Save to database
                for job in jobs:
                    db_manager.save_job(
                        title=job['title'],
                        link=job['link'],
                        email=email,
                        source=job['source'],
                        search_query=query
                    )
                
                # Send email
                if email_sender.send_job_email(email, jobs, job_role, location):
                    st.success("✅ Job listings sent to your email!")
                else:
                    st.warning("⚠️ Jobs found but email delivery failed. Please check your email settings.")
                
                st.session_state.jobs_found = jobs
                
            else:
                st.warning("No jobs found for your search criteria. Try adjusting your search parameters.")
                
        except Exception as e:
            st.error(f"An error occurred during job search: {str(e)}")

def schedule_daily_search(job_role, location, job_type, experience_years, email, preferred_time):
    try:
        # Stop existing scheduler if running
        if st.session_state.scheduler:
            st.session_state.scheduler.stop()
        
        # Create new scheduler
        scheduler = JobScheduler(
            job_role=job_role,
            location=location,
            job_type=job_type,
            experience_years=experience_years,
            email=email,
            preferred_time=preferred_time,
            db_manager=db_manager,
            email_sender=email_sender,
            job_scraper=job_scraper
        )
        
        # Start scheduler in background thread
        scheduler_thread = threading.Thread(target=scheduler.run, daemon=True)
        scheduler_thread.start()
        
        st.session_state.scheduler = scheduler
        st.session_state.scheduler_thread = scheduler_thread
        
        st.success(f"✅ Daily job search scheduled for {preferred_time.strftime('%H:%M')}!")
        st.info("The scheduler is now running in the background. You'll receive daily job updates at your specified time.")
        
    except Exception as e:
        st.error(f"Failed to schedule daily search: {str(e)}")

def job_logs_tab():
    st.header("📊 Job Search History")
    
    try:
        # Get job logs from database
        logs = db_manager.get_job_logs()
        
        if logs:
            df = pd.DataFrame(logs)
            
            # Display summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Jobs Found", len(df))
            with col2:
                st.metric("Unique Companies", df['source'].nunique())
            with col3:
                st.metric("Search Sessions", df['email'].nunique())
            
            # Display filters
            st.subheader("Filter Results")
            col1, col2 = st.columns(2)
            
            with col1:
                email_filter = st.selectbox("Filter by Email", ["All"] + df['email'].unique().tolist())
            with col2:
                date_filter = st.date_input("Filter by Date", value=None)
            
            # Apply filters
            filtered_df = df.copy()
            if email_filter != "All":
                filtered_df = filtered_df[filtered_df['email'] == email_filter]
            if date_filter:
                filtered_df = filtered_df[pd.to_datetime(filtered_df['timestamp']).dt.date == date_filter]
            
            # Display filtered results
            st.subheader("Job Listings")
            for _, row in filtered_df.iterrows():
                with st.expander(f"{row['title']} - {row['timestamp']}"):
                    st.write(f"**Link:** {row['link']}")
                    st.write(f"**Source:** {row['source']}")
                    st.write(f"**Email:** {row['email']}")
                    st.write(f"**Search Query:** {row['search_query']}")
                    st.write(f"**Timestamp:** {row['timestamp']}")
            
            # Export functionality
            st.subheader("Export Data")
            col1, col2 = st.columns(2)
            
            with col1:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"job_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Convert to Excel bytes
                excel_buffer = pd.io.common.BytesIO()
                filtered_df.to_excel(excel_buffer, index=False)
                excel_data = excel_buffer.getvalue()
                
                st.download_button(
                    label="📥 Download as Excel",
                    data=excel_data,
                    file_name=f"job_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        else:
            st.info("No job search history found. Start by searching for jobs in the 'Job Search' tab!")
            
    except Exception as e:
        st.error(f"Error loading job logs: {str(e)}")

def settings_tab():
    st.header("⚙️ Application Settings")
    
    # Email configuration
    st.subheader("📧 Email Configuration")
    with st.expander("Email Settings"):
        st.markdown("""
        To use the email functionality, you need to configure Gmail SMTP settings:
        
        1. **Gmail App Password**: Create an app password in your Gmail account
        2. **Environment Variables**: Set the following environment variables:
           - `GMAIL_USER`: Your Gmail address
           - `GMAIL_PASSWORD`: Your Gmail app password
        """)
        
        # Test email functionality
        st.subheader("Test Email")
        test_email = st.text_input("Email address to test", placeholder="test@example.com")
        
        if st.button("Send Test Email"):
            if test_email:
                with st.spinner("Sending test email..."):
                    try:
                        success = email_sender.send_test_email(test_email)
                        if success:
                            st.success("Test email sent successfully!")
                        else:
                            st.error("Failed to send test email. Please check your email configuration.")
                    except Exception as e:
                        st.error(f"Error sending test email: {str(e)}")
            else:
                st.warning("Please enter an email address to test")
    
    # Email status
    st.subheader("Current Email Status")
    with st.expander("Email Configuration Status"):
        
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_PASSWORD")
        
        if gmail_user and gmail_password:
            st.success("✅ Email configuration detected")
            st.write(f"Gmail User: {gmail_user}")
        else:
            st.error("❌ Email configuration missing")
            st.write("Please set GMAIL_USER and GMAIL_PASSWORD environment variables")
    
    # Database information
    st.subheader("🗄️ Database Status")
    with st.expander("Database Information"):
        try:
            total_jobs = db_manager.get_total_jobs_count()
            st.metric("Total Jobs in Database", total_jobs)
            
            # Database cleanup option
            if st.button("🗑️ Clear All Job Data", type="secondary"):
                if st.checkbox("I understand this will delete all job data"):
                    db_manager.clear_all_data()
                    st.success("All job data has been cleared")
                    st.rerun()
        except Exception as e:
            st.error(f"Database error: {str(e)}")
    
    # Scheduler status
    st.subheader("⏰ Scheduler Status")
    with st.expander("Scheduler Information"):
        if st.session_state.scheduler:
            st.success("✅ Scheduler is running")
            if st.button("🛑 Stop Scheduler"):
                st.session_state.scheduler.stop()
                st.session_state.scheduler = None
                st.success("Scheduler stopped")
                st.rerun()
        else:
            st.info("No scheduler currently running")
    
    # Application information
    st.subheader("ℹ️ Application Information")
    with st.expander("About This App"):
        st.markdown("""
        **AI Job Agent v1.0**
        
        This application helps you:
        - 🔍 Search for jobs across multiple platforms
        - 📧 Receive daily job updates via email
        - 📊 Track your job search history
        - 📥 Export job data for analysis
        
        **Supported Job Sites:**
        - LinkedIn
        - Indeed
        - Glassdoor
        - Other job search platforms
        
        **Features:**
        - Smart query enhancement based on job type
        - Daily email scheduling
        - SQLite database logging
        - CSV/Excel export functionality
        
        **Important Notes:**
        - Demo mode generates sample job listings with working search links
        - For production use, integrate with job site APIs for real listings
        - Email functionality requires Gmail app password setup
        
        Made with ❤️ using Streamlit
        """)

if __name__ == "__main__":
    main()
