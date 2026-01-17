import sqlite3
from datetime import datetime
from typing import Optional, Tuple

DB_NAME = "timetracker.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initialize the database with the tasks table."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_running_task() -> Optional[Tuple[int, str, datetime]]:
    """Return the currently running task if any."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, task_name, start_time FROM tasks WHERE status = 'running'")
    row = c.fetchone()
    conn.close()
    
    if row:
        # sqlite might return string for datetime, let's parse if needed, 
        # but usually using the adapter is auto if configured, or we parse manually.
        # For simplicity, we assume robust string parsing or standard sqlite3 behavior.
        # Actually standard sqlite3 returns string for TIMESTAMP unless parse_decltypes is used.
        # Let's handle string to datetime conversion carefully.
        task_id, name, start_str = row
        try:
            start_dt = datetime.fromisoformat(start_str)
        except ValueError:
            # Fallback for some sqlite versions or formats
            start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S.%f")
            
        return task_id, name, start_dt
    return None

def start_task(task_name: str) -> str:
    """Start a new task. Stop any running task first."""
    conn = get_connection()
    c = conn.cursor()
    
    # Check for running task
    running = get_running_task()
    msg = ""
    if running:
        stop_task() # Stop the previous one
        msg = f"Auto-stopped previous task '{running[1]}'. "
    
    start_time = datetime.now()
    c.execute("INSERT INTO tasks (task_name, start_time, status) VALUES (?, ?, ?)",
              (task_name, start_time, 'running'))
    conn.commit()
    conn.close()
    
    return f"{msg}Started task '{task_name}' at {start_time.strftime('%H:%M')}."

def stop_task() -> str:
    """Stop the currently running task."""
    conn = get_connection()
    c = conn.cursor()
    
    running = get_running_task()
    if not running:
        conn.close()
        return "No task is currently running."
    
    task_id, task_name, start_time = running
    end_time = datetime.now()
    duration = end_time - start_time
    
    # Calculate minutes for display
    minutes = int(duration.total_seconds() / 60)
    
    c.execute("UPDATE tasks SET end_time = ?, status = 'completed' WHERE id = ?",
              (end_time, task_id))
    conn.commit()
    conn.close()
    
    return f"Stopped '{task_name}'. Duration: {minutes} minutes."

def get_today_report():
    """Get summary of tasks for today."""
    conn = get_connection()
    c = conn.cursor()
    
    # Filter by today. SQLite 'date(start_time)' works if format is standard ISO
    today = datetime.now().date().isoformat()
    
    c.execute('''
        SELECT task_name, start_time, end_time 
        FROM tasks 
        WHERE date(start_time) = ? AND status = 'completed'
    ''', (today,))
    
    rows = c.fetchall()
    conn.close()
    
    summary = {}
    for name, start_str, end_str in rows:
        try:
            start = datetime.fromisoformat(start_str)
            end = datetime.fromisoformat(end_str)
        except ValueError:
             # Fallback
            start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S.%f")
            end = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S.%f")
            
        duration = end - start
        if name in summary:
            summary[name] += duration
        else:
            summary[name] = duration
            
    return summary
