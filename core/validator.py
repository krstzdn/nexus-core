"""
NEXUS TFA - Validation & Self-Correcting Engine
Validates past agent predictions against actual market outcomes and updates weights.
"""
from data.database import DatabaseEngine
from core.logger import Logger

logger = Logger("NEXUS-VALIDATOR")

class ForecastValidator:
    def __init__(self):
        self.db = DatabaseEngine()

    def validate_predictions(self):
        """Bekleyen tüm tahminleri inceler ve piyasa gerçekleriyle karşılaştırır."""
        pending = self.db.get_pending_forecasts()
        if not pending:
            logger.info("[🔍 DENETLEYİCİ] Doğrulanacak bekleyen yeni bir tahmin bulunamadı.")
            return

        # Gerçek piyasa fiyat hareketi simülasyonu (İlerleyen fazda market_stream'e bağlanacak)
        # KAP haberleri olumlu olduğu için hisselerin yönünün yukarı (UP) gittiğini varsayıyoruz
        actual_market_movement = {
            "KCHOL": "UP",
            "THYAO": "UP"
        }

        logger.info(f"[🛡️ OTONOM DENETİM] {len(pending)} adet geçmiş tahmin süzgece alınıyor...")
        
        for row in pending:
            f_id = row["id"]
            agent = row["agent_name"]
            asset = row["target_asset"]
            predicted_direction = row["direction"]
            
            actual_direction = actual_market_movement.get(asset, "SIDEWAYS")
            is_correct = (predicted_direction == actual_direction)
            
            status = "SUCCESS" if is_correct else "FAILED"
            self.db.update_forecast_status(f_id, status)
            self.db.update_agent_weight(agent, is_correct)
            
            if is_correct:
                logger.info(f"[🔥 EVRİMSEAL ÖDÜL] {agent} ajanının {asset} tahmini TUTTU. Güven ağırlığı artırıldı.")
            else:
                logger.warning(f"[⚠️ EVRİMSEL CEZA] {agent} ajanının {asset} tahmini YANILDI. Güven ağırlığı düşürüldü.")