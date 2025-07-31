from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3, os, traceback

app = FastAPI()

# --- 1. Enable CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow Django frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. DB Path ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "frontend_django", "db.sqlite3")

# --- 3. Response Models ---
class LeaderboardEntry(BaseModel):
    user: str
    total_duration: int

class AnalyticsResponse(BaseModel):
    total_tasks: int
    total_duration: int
    leaderboard: List[LeaderboardEntry]

# --- 4. API Endpoint ---
@app.get("/analytics")
def analytics():
    try:
        print("Using DB:", DB_PATH)

        # Connect to SQLite DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Total tasks
        cursor.execute("SELECT COUNT(*) FROM tasks_task")
        total_tasks = cursor.fetchone()[0]

        # Total duration
        cursor.execute("SELECT SUM(duration) FROM tasks_task")
        total_duration = cursor.fetchone()[0] or 0

        # Leaderboard
        cursor.execute("""
            SELECT auth_user.username, SUM(tasks_task.duration)
            FROM tasks_task
            JOIN auth_user ON tasks_task.user_id = auth_user.id
            GROUP BY tasks_task.user_id
            ORDER BY SUM(tasks_task.duration) DESC
            LIMIT 5
        """)
        rows = cursor.fetchall()
        leaderboard = [{"user": row[0], "total_duration": row[1]} for row in rows]

        conn.close()
        return {
            "total_tasks": total_tasks,
            "total_duration": total_duration,
            "leaderboard": leaderboard
        }

    except Exception as e:
        # Print error in FastAPI logs
        print("Error in /analytics:", e)
        traceback.print_exc()
        # Return error in JSON (so frontend sees it)
        return {"error": str(e)}
