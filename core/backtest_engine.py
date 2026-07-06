"""
NEXUS Operating System - Advanced Backtesting Engine
Sourced directly from the optimized historical database matrix.
"""
import sqlite3
from pathlib import Path
from core.logger import Logger

logger = Logger("NEXUS-BACKTEST")

class BacktestEngine:
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0.0
        self.entry_price = 0.0
        self.db_path = Path(__file__).resolve().parent.parent / "data" / "nexus_tfa.db"

    def run_db_test(self, asset: str) -> dict:
        """Veri tabanındaki tüm geçmiş verileri çekerek test simülasyonunu başlatır."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1 Yıllık veriyi çek
        cursor.execute("SELECT price, date FROM historical_prices WHERE asset = ? ORDER BY date ASC", (asset,))
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            logger.error(f"{asset} için geçmiş veri bulunamadı!")
            return {}

        logger.info(f"[📊 DERİN BACKTEST BAŞLADI] Varlık: {asset} | Süre: {len(rows)} Gün")
        trades_count = 0
        successful_trades = 0

        # Simülasyon döngüsü
        for idx, row in enumerate(rows):
            price = row['price']
            date = row['date']
            
            # Strateji: Basit bir momentum/rastgele sinyal simülasyonu 
            # (İleride buraya ajanların gerçek geçmiş tahmin logları bağlanacak)
            if idx % 10 == 0 and self.position == 0:  # Her 10 günde bir ALIM dene
                allocation = self.capital * 0.3
                self.position = allocation / price
                self.entry_price = price
                self.capital -= allocation
                trades_count += 1
                
            elif idx % 15 == 0 and self.position > 0: # Her 15 günde bir SATIM dene
                revenue = self.position * price
                self.capital += revenue
                if price > self.entry_price:
                    successful_trades += 1
                self.position = 0.0

        # Elimizde kalan pozisyon varsa kapat
        if self.position > 0:
            self.capital += self.position * rows[-1]['price']
            self.position = 0.0

        final_roi = ((self.capital - self.initial_capital) / self.initial_capital) * 100
        win_rate = (successful_trades / trades_count * 100) if trades_count > 0 else 0.0

        return {
            "initial_capital": self.initial_capital,
            "final_capital": self.capital,
            "total_roi_pct": final_roi,
            "total_trades": trades_count,
            "win_rate_pct": win_rate
        }