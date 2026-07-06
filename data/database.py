"""
NEXUS Operating System - Database Architecture
Handles persistent storage for forecasts, telemetry, and agent weights with index optimization.
"""
import sqlite3
from pathlib import Path
from core.logger import Logger

logger = Logger("NEXUS-DATABASE")

class DatabaseEngine:
    def __init__(self):
        self.db_dir = Path(__file__).resolve().parent.parent / "data"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.db_dir / "nexus_tfa.db"
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Veri tabanı tablolarını ve performans indekslerini oluşturur."""
        with self.get_connection() as conn:
            # 1. Tahminler Tablosu
            conn.execute("""
                CREATE TABLE IF NOT EXISTS forecasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    target_asset TEXT NOT NULL,
                    score REAL NOT NULL,
                    direction TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    status TEXT DEFAULT 'PENDING',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    
                )
            """)

            # 2. Ajan Ağırlıkları Tablosu
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_weights (
                    agent_name TEXT PRIMARY KEY,
                    weight REAL DEFAULT 1.0,
                    success_rate REAL DEFAULT 100.0,
                    total_forecasts INTEGER DEFAULT 0
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS historical_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset TEXT NOT NULL,
                    price REAL NOT NULL,
                    date TEXT NOT NULL,
                    UNIQUE(asset, date)
                )
            """)
            
            conn.execute("CREATE INDEX IF NOT EXISTS idx_hist_asset_date ON historical_prices(asset, date)")

            # 🚀 PERFORMANS İNDEKSLERİ (Sorgu hızını milisaniyelere düşürür)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_forecasts_status ON forecasts(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_forecasts_timestamp ON forecasts(timestamp)")
            
            # Varsayılan ajan ağırlıklarını yükle
            conn.execute("INSERT OR IGNORE INTO agent_weights (agent_name, weight) VALUES ('corp-agent', 1.0)")
            conn.execute("INSERT OR IGNORE INTO agent_weights (agent_name, weight) VALUES ('crypto-agent', 1.0)")
            
            conn.commit()
        logger.info("[⚙️ DB OPTİMİZASYON] Tablolar ve performans indeksleri başarıyla mühürlendi.")

    def save_forecast(self, agent: str, asset: str, score: float, direction: str, confidence: float):
        """Ajan tahminini veri tabanına kaydeder."""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO forecasts (agent_name, target_asset, score, direction, confidence)
                VALUES (?, ?, ?, ?, ?)
            """, (agent, asset, score, direction, confidence))
            
            # Toplam tahmin sayısını güncelle
            conn.execute("""
                UPDATE agent_weights 
                SET total_forecasts = total_forecasts + 1 
                WHERE agent_name = ?
            """, (agent,))
            conn.commit()