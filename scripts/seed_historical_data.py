"""
NEXUS OS - Historical Data Seeder
Populates the database with 1 year of synthetic price data for robust backtesting.
"""
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "nexus_tfa.db"

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 🚀 ÖNLEM: Tablo henüz kernel tarafından oluşturulmadıysa burada force ediyoruz
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL,
            UNIQUE(asset, date)
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hist_asset_date ON historical_prices(asset, date)")
    
    # Mevcut verileri temizle
    cursor.execute("DELETE FROM historical_prices")
    
    assets = ["KCHOL", "THYAO", "BTC"]
    start_date = datetime(2025, 7, 6)
    
    for asset in assets:
        # Her varlık için farklı bir başlangıç fiyatı
        if asset == "BTC":
            price = 60000.0
        elif asset == "KCHOL":
            price = 300.0
        else:
            price = 250.0
            
        print(f"[⏳] {asset} için 365 günlük veri üretiliyor...")
        
        for day in range(365):
            current_date = start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Rastgele fiyat hareketleri (% -2 ile % +2.2 arası)
            change = random.uniform(-0.02, 0.022)
            price = price * (1 + change)
            
            cursor.execute("""
                INSERT OR IGNORE INTO historical_prices (asset, price, date)
                VALUES (?, ?, ?)
            """, (asset, round(price, 2), date_str))
            
    conn.commit()
    conn.close()
    print("[🏁] 1 Yıllık derin backtest verisi veri tabanına başarıyla işlendi!")

if __name__ == "__main__":
    seed_data()