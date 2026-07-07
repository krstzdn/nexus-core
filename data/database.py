import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "nexus_tfa.db")

def init_db():
    """Şirket ilk açıldığında veritabanını ve tabloları hazırlar."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Konsey kararlarını, sentiment skorlarını ve varlık bilgilerini tutan ana tablo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS council_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            price REAL,
            consensus_score REAL,
            decision TEXT,
            sentiment_score REAL
        )
    """)
    conn.commit()
    conn.close()
    print("[DATABASE] nexus_tfa.db başarıyla senkronize edildi ve hazır.")

def save_market_state_to_db(state):
    """
    Kernel'dan (CEO) gelen shared_market_state paketini alır 
    and veritabanına kalıcı olarak arşivler.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        symbol = state["current_symbol"]
        price = state["live_price"]
        c_score = state["consensus_score"]
        decision = state["final_decision"]
        # Oracle ajanımızın ürettiği sentiment skoru
        sentiment = state["oracle_report"].get("sentiment_score", 50.0)
        
        cursor.execute("""
            INSERT INTO council_logs (timestamp, symbol, price, consensus_score, decision, sentiment_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, symbol, price, c_score, decision, sentiment))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB WRITE ERROR] Veri arşive kaydedilemedi: {str(e)}")

def get_recent_logs_from_db(symbol, limit=5):
    """Arayüzün (Dashboard) ekranı güncellerken okuyacağı son kararlar."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, price, consensus_score, decision 
            FROM council_logs 
            WHERE symbol = ?
            ORDER BY id DESC LIMIT ?
        """, (symbol, limit))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB READ ERROR] Arşiv okunurken hata çıktı: {str(e)}")
        return []