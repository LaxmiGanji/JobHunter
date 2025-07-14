import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create jobs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        link TEXT NOT NULL,
                        email TEXT NOT NULL,
                        source TEXT,
                        search_query TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create index for better query performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON jobs(email)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON jobs(timestamp)')
                
                conn.commit()
                
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
            raise
    
    def save_job(self, title: str, link: str, email: str, source: str = "", search_query: str = "") -> bool:
        """Save a job listing to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO jobs (title, link, email, source, search_query)
                    VALUES (?, ?, ?, ?, ?)
                ''', (title, link, email, source, search_query))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"Error saving job: {e}")
            return False
    
    def get_job_logs(self, email: Optional[str] = None, limit: int = 1000) -> List[Dict]:
        """Retrieve job logs from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if email:
                    cursor.execute('''
                        SELECT title, link, email, source, search_query, timestamp
                        FROM jobs
                        WHERE email = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (email, limit))
                else:
                    cursor.execute('''
                        SELECT title, link, email, source, search_query, timestamp
                        FROM jobs
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (limit,))
                
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                jobs = []
                for row in rows:
                    jobs.append({
                        'title': row[0],
                        'link': row[1],
                        'email': row[2],
                        'source': row[3],
                        'search_query': row[4],
                        'timestamp': row[5]
                    })
                
                return jobs
                
        except sqlite3.Error as e:
            print(f"Error retrieving job logs: {e}")
            return []
    
    def get_total_jobs_count(self) -> int:
        """Get the total number of jobs in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM jobs')
                return cursor.fetchone()[0]
                
        except sqlite3.Error as e:
            print(f"Error getting job count: {e}")
            return 0
    
    def clear_all_data(self) -> bool:
        """Clear all job data from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM jobs')
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"Error clearing data: {e}")
            return False
    
    def get_recent_jobs(self, email: str, hours: int = 24) -> List[Dict]:
        """Get recent jobs for a specific email within the last N hours."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT title, link, email, source, search_query, timestamp
                    FROM jobs
                    WHERE email = ? AND datetime(timestamp) > datetime('now', '-{} hours')
                    ORDER BY timestamp DESC
                '''.format(hours), (email,))
                
                rows = cursor.fetchall()
                
                jobs = []
                for row in rows:
                    jobs.append({
                        'title': row[0],
                        'link': row[1],
                        'email': row[2],
                        'source': row[3],
                        'search_query': row[4],
                        'timestamp': row[5]
                    })
                
                return jobs
                
        except sqlite3.Error as e:
            print(f"Error retrieving recent jobs: {e}")
            return []
