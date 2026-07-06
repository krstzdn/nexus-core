"""
NEXUS Operating System - Risk Management Layer
Prevents over-exposure during high market volatility with dynamic SL/TP guardrails.
"""
from core.logger import Logger

logger = Logger("NEXUS-RISK")

class RiskManager:
    def __init__(self):
        self.max_exposure_per_asset = 0.25  # Portföyün max %25'i tek hisseye
        self.volatility_threshold = 0.03    # %3 üzeri oynaklıkta kalkan devreye girer
        self.stop_loss_pct = 0.05           # %5 Stop-Loss
        self.take_profit_pct = 0.15         # %15 Take-Profit

    def calculate_safe_allocation(self, current_cash: float, confidence: float = 1.0, market_volatility: float = 0.02) -> float:
        """Risk seviyesine göre güvenli yatırım tutarını hesaplar."""
        if market_volatility > self.volatility_threshold:
            logger.warning("[⚠️ RİSK KALKANI] Yüksek volatilite algılandı, işlem boyutu düşürülüyor!")
            return (current_cash * 0.10) * confidence  # Kalkan devrede: %10 yerleştir
            
        return (current_cash * self.max_exposure_per_asset) * confidence

    def check_exit_signals(self, current_price: float, entry_price: float) -> str:
        """Pozisyonun kar al veya zarar kes seviyelerine ulaşıp ulaşmadığını denetler."""
        if entry_price == 0:
            return "HOLD"
            
        price_change = (current_price - entry_price) / entry_price
        
        # 🛑 STOP-LOSS KONTROLÜ
        if price_change <= -self.stop_loss_pct:
            return "STOP_LOSS"
            
        # 💰 TAKE-PROFIT KONTROLÜ
        if price_change >= self.take_profit_pct:
            return "TAKE_PROFIT"
            
        return "HOLD"