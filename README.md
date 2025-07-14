# JobHunter


##  Overview

**Job Hunter** is a fully automated, intelligent job search assistant that helps you find jobs effortlessly. It scrapes listings from multiple platforms, delivers personalized job emails daily, and logs your job search activity locally. Designed for professionals and students alike, it simplifies and streamlines the job-hunting process.

---

##  Features

-  Multi-platform scraping (LinkedIn, Indeed, Glassdoor, Naukri, Monster)
-  Daily job updates sent directly to your email
-  Intuitive Streamlit-based UI with tabbed navigation
-  Local SQLite database to track job history
-  Optional Google Sheets sync (planned)

---

##  System Architecture

### Frontend
- Built with **Streamlit**
- Real-time updates and session state management
- Tabs: **Job Search**, **Job Logs**, **Settings**

### Backend
- Modular Python architecture using class-based design
- Core components:
  - `JobScraper`: Searches job platforms via enhanced Google queries
  - `DatabaseManager`: Handles job storage using SQLite
  - `EmailSender`: Sends job listings via Gmail SMTP
  - `JobScheduler`: Automates the daily job search and email dispatch

---

##  File Structure

```
├── main.py               # Streamlit UI and workflow handler
├── database.py           # SQLite DB logic
├── email_sender.py       # Email automation
├── job_scraper.py        # Job search scraping logic
├── scheduler.py          # Daily scheduling module
└── jobs.db               # Local job log database (auto-generated)
```

---

##  Data Flow

```
User Input → Enhanced Query → Job Scraper → Database → Email Sender
                         ↘                          ↘
                       Scheduler             Job Logs UI
```

---

##  Tech Stack & Dependencies

- `streamlit`
- `beautifulsoup4`
- `requests`
- `schedule`
- `pandas`
- `sqlite3` (built-in)
- `smtplib` (built-in)

Install with:
```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Create a `.env` file or use environment secrets to store:

| Variable         | Description                            |
|------------------|----------------------------------------|
| `GMAIL_USER`     | Your Gmail address                     |
| `GMAIL_PASSWORD` | App-specific password (Gmail settings) |

---

## ⏱ Scheduler Logic

- Uses `schedule` and Python threading
- Triggers job search + email at user-defined time
- Robust error handling and thread lifecycle management

---

##  Email Output Example

> **Subject**:  10 New Remote Python Jobs  
>  
> Hello!  
> Here are your personalized jobs for *"Remote Python Developer"*:
>  
> - [Python Developer – TechCorp](https://techcorp.com/job1)  
> - [Backend Engineer – DevStart](https://devstart.com/job2)  
>  
> Best,  
> *AI Job Agent*

---

##  Smart Features

- Dynamic query enrichment (e.g. adds keywords like "fresher", "remote")
- Multiple fallback scraping selectors to bypass minor site structure changes
- HTML-based email styling for better readability
- Timestamped job tracking for analytics

---

##  Optional Google Sheets Sync (Planned)

- Log jobs to a Google Sheet using `gspread`
- Authenticate via `oauth2client` service account
- Enables cloud storage for tracking job history across devices

---

##  Getting Started

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Configure Gmail
- Enable 2-Step Verification
- Generate an **App Password**
- Set the environment variables

### 3. Launch the App
```bash
streamlit run main.py
```

---

##  Future Enhancements

- Multi-user login system
- Telegram job alerts
- PDF/Excel export of job logs
- REST API integration for job platforms
- AI-driven job filtering & ranking

---

##  Author

**Laxmi Ganji**  
 Full Stack Developer | AI Enthusiast  
 [LinkedIn](https://linkedin.com) • [GitHub](https://github.com)

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
