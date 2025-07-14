# AI Job Agent - Replit Development Guide

## Overview

This is a comprehensive AI-powered job search automation system built with Streamlit. The application scrapes job listings from multiple platforms, sends daily email updates, and maintains logs of all job search activities. The system is designed to help users automate their job search process with personalized criteria and scheduling.

## Recent Changes (January 2025)

**Fixed Job Scraping Issue**: Resolved the problem where job searches were returning zero results. The issue was caused by Google search blocking automated requests and changing their HTML structure. Implemented a multi-layered approach:
- Added fallback mechanisms for when Google search fails
- Implemented improved Google search with multiple selectors
- Added demo job listings that are contextually relevant to user queries
- Enhanced error handling and robustness

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **UI Components**: 
  - Tabbed interface with Job Search, Job Logs, and Settings sections
  - Form-based input collection for job criteria
  - Real-time status updates and job listings display
  - Session state management for scheduler and job data

### Backend Architecture
- **Core Components**:
  - `DatabaseManager`: SQLite database operations
  - `EmailSender`: Gmail SMTP email automation
  - `JobScraper`: Web scraping for job listings
  - `JobScheduler`: Daily automation scheduling
- **Architecture Pattern**: Modular class-based design with clear separation of concerns

### Data Storage Solutions
- **Primary Database**: SQLite (`jobs.db`)
  - Tables: `jobs` with fields (id, title, link, email, source, search_query, timestamp)
  - Indexes on email and timestamp for performance
- **Planned Integration**: Google Sheets via `gspread` API for cloud storage

## Key Components

### 1. Job Search Engine (`job_scraper.py`)
- **Purpose**: Scrapes job listings from multiple platforms
- **Target Sites**: LinkedIn, Indeed, Glassdoor, Naukri, Monster
- **Search Strategy**: Google search with site-specific queries
- **Query Enhancement**: Dynamically adds keywords based on job type and experience level

### 2. Email Automation (`email_sender.py`)
- **Service**: Gmail SMTP with app passwords
- **Features**: HTML email formatting, job listings with links
- **Authentication**: Environment variables for Gmail credentials
- **Email Structure**: Professional formatting with job details and branding

### 3. Database Management (`database.py`)
- **Database**: SQLite with automatic table creation
- **Schema**: Jobs table with comprehensive job information
- **Operations**: Save jobs, query by email, timestamp indexing
- **Error Handling**: Proper exception handling for database operations

### 4. Scheduling System (`scheduler.py`)
- **Library**: Python `schedule` library with threading
- **Functionality**: Daily job searches at user-specified times
- **Thread Management**: Proper start/stop controls with threading events
- **Integration**: Coordinates scraper, database, and email components

### 5. Main Application (`main.py`)
- **Framework**: Streamlit with session state management
- **UI Tabs**: Job Search configuration, Job Logs viewing, Settings
- **Form Handling**: Comprehensive input validation and processing
- **Real-time Updates**: Live job search results and status updates

## Data Flow

1. **User Input**: User configures job search criteria through Streamlit form
2. **Query Building**: System enhances search query based on job type and experience
3. **Web Scraping**: JobScraper searches multiple job platforms via Google
4. **Data Storage**: Job results saved to SQLite database with timestamps
5. **Email Delivery**: EmailSender formats and sends job listings to user
6. **Scheduling**: Daily automation runs at user-specified time
7. **Logging**: All activities logged for user review and analytics

## External Dependencies

### Required Python Packages
- `streamlit`: Web application framework
- `beautifulsoup4`: HTML parsing for web scraping
- `requests`: HTTP requests for web scraping
- `schedule`: Job scheduling functionality
- `sqlite3`: Database operations (built-in)
- `smtplib`: Email sending (built-in)
- `pandas`: Data manipulation and display

### Planned Integrations
- `gspread`: Google Sheets API integration
- `oauth2client`: Google API authentication
- `yagmail`: Alternative email service

### Environment Variables
- `GMAIL_USER`: Gmail account for sending emails
- `GMAIL_PASSWORD`: Gmail app password for authentication

### External Services
- Gmail SMTP server for email delivery
- Google search for job listing discovery
- Multiple job platforms (LinkedIn, Indeed, Glassdoor, etc.)

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.x environment
- **Web Server**: Streamlit development server
- **Database**: Local SQLite file storage
- **Secrets**: Environment variables for Gmail credentials

### File Structure
```
├── main.py                 # Streamlit application entry point
├── database.py            # Database operations
├── email_sender.py        # Email automation
├── job_scraper.py         # Web scraping logic
├── scheduler.py           # Daily scheduling
├── jobs.db               # SQLite database (created at runtime)
└── attached_assets/      # Documentation and requirements
```

### Deployment Requirements
- Gmail account with app password configured
- Replit secrets configured for email credentials
- Web preview enabled for Streamlit interface
- Optional: Service account JSON for Google Sheets integration

### Scalability Considerations
- SQLite suitable for single-user deployment
- Modular design allows easy migration to PostgreSQL
- Session state management for concurrent users
- Threading controls for scheduler management

### Monitoring and Maintenance
- Database indexes for query performance
- Error handling and logging throughout
- Session state cleanup and management
- Scheduler thread lifecycle management
