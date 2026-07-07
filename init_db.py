"""
NEXUS AI Operating System - Initialization Script
Configures the database schema, default agents, and admin user profiles.
"""
import sqlite3
import hashlib
from pathlib import Path

def initialize_database():
    db_path = Path(__file__).resolve().parent / "data" / "nexus_tfa.db"
    
    # Data klasörünün varlığından emin ol
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Users Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            plan_type TEXT DEFAULT 'STARTER'
        )
    """)
    
    # 2. Agent Weights Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_weights (
            agent_name TEXT PRIMARY KEY,
            weight REAL DEFAULT 1.0,
            total_forecasts INTEGER DEFAULT 0
        )
    """)
    
    # 3. Forecasts Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT,
            target_asset TEXT,
            score REAL,
            direction TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Varsayılan Admin Kullanıcısı (Test için)
    admin_pw = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute("INSERT OR IGNORE INTO users (email, password_hash, plan_type) VALUES (?, ?, ?)", 
                   ("admin@nexus.ai", admin_pw, "WHALE"))
    
    conn.commit()
    conn.close()
    print("✅ NEXUS veritabanı ve altyapı tabloları başarıyla mühürlendi.")

if __name__ == "__main__":
    initialize_database()