"""
NEXUS TFA - Central Database Engine (SQLite)
Maintains historical forecasts, real price logs, and dynamic agent weightings.
"""
import sqlite3
from pathlib import Path

class DatabaseEngine:
    def __init__(self):
        self.db_path = Path(__file__).resolve().parent / "nexus_tfa.db"
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            # Tahmin kayıtları tablosu (Eksiksiz Şema)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS forecasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT,
                    target_asset TEXT,
                    score REAL,
                    direction TEXT,
                    confidence REAL,
                    status TEXT DEFAULT 'PENDING',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Ajan performans ve evrimsel ağırlık tablosu
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_weights (
                    agent_name TEXT PRIMARY KEY,
                    weight REAL DEFAULT 1.0,
                    success_rate REAL DEFAULT 100.0,
                    total_forecasts INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def save_forecast(self, agent: str, asset: str, score: float, direction: str, confidence: float):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO forecasts (agent_name, target_asset, score, direction, confidence) VALUES (?, ?, ?, ?, ?)",
                (agent, asset, score, direction, confidence)
            )
            conn.commit()

    def get_pending_forecasts(self):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM forecasts WHERE status = 'PENDING'")
            return cursor.fetchall()

    def update_forecast_status(self, forecast_id: int, status: str):
        with self.get_connection() as conn:
            conn.execute("UPDATE forecasts SET status = ? WHERE id = ?", (status, forecast_id))
            conn.commit()

    def update_agent_weight(self, agent_name: str, is_correct: bool):
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM agent_weights WHERE agent_name = ?", (agent_name,)).fetchone()
            
            if not row:
                conn.execute("INSERT INTO agent_weights (agent_name) VALUES (?)", (agent_name,))
                current_weight = 1.0
                current_total = 0
            else:
                current_weight = row["weight"]
                current_total = row["total_forecasts"]
            
            new_total = current_total + 1
            weight_delta = 0.05 if is_correct else -0.05
            new_weight = max(0.1, min(2.0, current_weight + weight_delta))
            
            conn.execute(
                "UPDATE agent_weights SET weight = ?, total_forecasts = ? WHERE agent_name = ?",
                (new_weight, new_total, agent_name)
            )
            conn.commit()