"""
NEXUS Operating System - Advanced Backtesting Engine
Integrated with real-time risk mitigation guardrails (Stop-Loss & Take-Profit).
"""
import sqlite3
from pathlib import Path
from core.logger import Logger
from core.risk_manager import RiskManager

logger = Logger("NEXUS-BACKTEST")

class BacktestEngine:
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0.0
        self.entry_price = 0.0
        self.db_path = Path(__file__).resolve().parent.parent / "data" / "nexus_tfa.db"
        self.risk_manager = RiskManager()

    def run_db_test(self, asset: str) -> dict:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT price, date FROM historical_prices WHERE asset = ? ORDER BY date ASC", (asset,))
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            logger.error(f"{asset} için geçmiş veri bulunamadı!")
            return {}

        logger.info(f"[📊 RISK KORUMALI BACKTEST BAŞLADI] Varlık: {asset} | Süre: {len(rows)} Gün")
        trades_count = 0
        successful_trades = 0

        for idx, row in enumerate(rows):
            price = row['price']
            date = row['date']
            
            # 🚨 RISK DENETİMİ (Kar Al / Zarar Kes Kontrolü)
            if self.position > 0:
                risk_status = self.risk_manager.check_exit_signals(price, self.entry_price)
                
                if risk_status in ["STOP_LOSS", "TAKE_PROFIT"]:
                    revenue = self.position * price
                    self.capital += revenue
                    
                    if risk_status == "TAKE_PROFIT":
                        successful_trades += 1
                        logger.info(f"[{date}] 💰 HEDEF YAKALANDI (TAKE_PROFIT) -> Fiyat: {price} TRY")
                    else:
                        logger.warning(f"[{date}] 🛑 SERMAYE KORUNDU (STOP_LOSS) -> Fiyat: {price} TRY")
                        
                    self.position = 0.0
                    self.entry_price = 0.0
                    continue

            # ALIM STRATEJİSİ (Dinamik Risk Onaylı Kasa Boyutu)
            if idx % 10 == 0 and self.position == 0:
                # Rastgele volatilite simüle ediyoruz (Örn: 0.02)
                allocation = self.risk_manager.calculate_safe_allocation(self.capital, confidence=1.0, market_volatility=0.02)
                
                if allocation > self.capital:
                    allocation = self.capital
                    
                self.position = allocation / price
                self.entry_price = price
                self.capital -= allocation
                trades_count += 1

        # Kalan pozisyonu son gün kapat
        if self.position > 0:
            self.capital += self.position * rows[-1]['price']
            if rows[-1]['price'] > self.entry_price:
                successful_trades += 1
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