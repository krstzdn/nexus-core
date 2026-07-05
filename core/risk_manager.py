"""
NEXUS Operating System - Risk Management Layer
Prevents over-exposure during high market volatility.
"""
from core.logger import Logger

logger = Logger("NEXUS-RISK")

class RiskManager:
    def __init__(self):
        self.max_exposure_per_asset = 0.25 # Portföyün max %25'i tek hisseye
        self.volatility_threshold = 0.03   # %3 üzeri oynaklıkta kalkan devreye girer

    def calculate_safe_allocation(self, current_cash: float, confidence: float, market_volatility: float) -> float:
        """Risk seviyesine göre güvenli yatırım tutarını hesaplar."""
        if market_volatility > self.volatility_threshold:
            logger.warning("[🛡️ RİSK KALKANI] Yüksek volatilite algılandı. İşlem hacmi daraltıldı.")
            return (current_cash * 0.10) * confidence # Kalkan devrede: %20 yerine %10
        
        return (current_cash * 0.20) * confidence

    def check_stop_loss(self, asset: str, current_price: float, entry_price: float) -> bool:
        """Zarar %5'i geçerse satış emrini tetiklemek için kontrol eder."""
        if entry_price > 0 and (entry_price - current_price) / entry_price > 0.05:
            logger.error(f"[💥 STOP-LOSS TETİKLENDİ] {asset} için pozisyon kapatılıyor.")
            return True
        return False