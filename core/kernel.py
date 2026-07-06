"""
NEXUS AI Operating System - Core Kernel & Consensus Engine
Version: 0.1.0 | Build: Genesis
Coordinates specialized agents and computes weighted consensus for investment decisions.
"""
import sqlite3
from pathlib import Path
from datetime import datetime
from core.logger import Logger

logger = Logger("NEXUS-KERNEL")

class AIKernel:
    def __init__(self):
        self.db_path = Path(__file__).resolve().parent.parent / "data" / "nexus_tfa.db"
        self.version = "0.1.0"
        self.build = "Genesis"

    def get_agent_weights(self) -> dict:
        """Veri tabanından ajanların güncel güvenilirlik ağırlıklarını çeker."""
        weights = {}
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT agent_name, weight FROM agent_weights")
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                weights[row['agent_name']] = row['weight']
        except Exception as e:
            logger.error(f"Ağırlıklar çekilirken hata oluştu: {e}")
            weights = {"corp-agent": 1.5, "crypto-agent": 0.95, "macro-agent": 1.1, "value-agent": 1.2}
        return weights

    def optimize_agent_weights(self, target_asset: str, actual_direction: str, agent_signals: dict):
        """Doğru tahminde bulunan ajanların ağırlığını artırır, hatalı olanları cezalandırır."""
        logger.info(f"[🧬 EVRİMSEL DÖNGÜ] {target_asset} için ajan performansları puanlanıyor...")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            for agent_name, data in agent_signals.items():
                predicted_direction = "HOLD"
                if isinstance(data, dict):
                    sig = data.get("signal", 0.0)
                else:
                    sig = data
                
                if sig > 0: predicted_direction = "UP"
                elif sig < 0: predicted_direction = "DOWN"
                
                is_correct = (predicted_direction == actual_direction)
                cursor.execute("SELECT weight, total_forecasts FROM agent_weights WHERE agent_name = ?", (agent_name,))
                row = cursor.fetchone()
                if row:
                    current_weight, total_forecasts = row
                    new_total_forecasts = total_forecasts + 1
                    new_weight = min(current_weight * 1.05, 3.0) if is_correct else max(current_weight * 0.95, 0.1)
                    cursor.execute("UPDATE agent_weights SET weight = ?, total_forecasts = ? WHERE agent_name = ?", (round(new_weight, 2), new_total_forecasts, agent_name))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Geri besleme döngüsünde hata: {e}")

    def execute_council_session(self, target_asset: str) -> dict:
        """Ajan konseyini toplar, oylama yapar ve konsensüs kararını üretir."""
        logger.info(f"[🏛️ KONSEY TOPLANDI] Hedef Varlık: {target_asset} için karar oturumu başladı.")
        
        # 1. Adım: Global Değişkenleri Başlat (Scope Koruma)
        sentiment_score = 0.0
        direction = "HOLD"
        consensus_score = 0.0
        
        # 2. Adım: Sentiment Analizi İcra Et
        try:
            from core.sentiment_analyzer import SentimentAnalyzer
            analyzer = SentimentAnalyzer()
            sentiment_score = analyzer.analyze_asset_sentiment(target_asset)
        except Exception as e:
            logger.error(f"Sentiment analizi yapılırken hata oluştu: {e}")
            
        # 3. Adım: Canlı Veri Pipeline Entegrasyonu ve Dinamik Ajan Sinyalleri
        from data.data_pipeline import DataPipeline
        pipeline = DataPipeline()
        live_price = pipeline.fetch_and_sync_live_price(target_asset)
        
        # Ajanlar artık canlı fiyata göre dinamik rasyolar üretiyor
        # Simülasyon: Fiyatın son rakamına veya trendine göre ajanlar bağımsız karar veriyor
        import random
        random.seed(int(live_price)) # Fiyata bağlı deterministik üretim
        
        agent_signals = {
            "crypto-agent": {"signal": 1.0 if target_asset == "BTC" else 0.0, "score": round(random.uniform(0.6, 0.9), 2)},
            "macro-agent": {"signal": random.choice([1.0, -1.0, 0.0]), "score": round(random.uniform(0.5, 0.8), 2)},
            "value-agent": {"signal": 1.0 if live_price < 500 else 0.0, "score": round(random.uniform(0.7, 0.95), 2)},
            "corp-agent": {"signal": random.choice([1.0, 0.0]), "score": round(random.uniform(0.6, 0.85), 2)}
        }
            

        # 4. Adım: Güvenli Oylama Döngüsü
        weighted_signal_sum = 0.0
        total_weight = 0.0
        for agent, data in agent_signals.items():
            try:
                eights = self.get_agent_weights()
                if isinstance(data, dict):
                    sig = float(data.get("signal", 0.0))
                    score = float(data.get("score", 1.0))
                else:
                    sig = float(data)
                    score = 1.0
                weighted_signal_sum = 0.0
                total_weight = 0.0
            except Exception as loop_err:
                logger.error(f"Döngü hatası: {loop_err}")

        agent_consensus = weighted_signal_sum / total_weight if total_weight > 0 else 0.0
        
        # 5. Adım: Sentez ve Yön Belirleme
        consensus_score = (agent_consensus * 0.70) + (sentiment_score * 0.30)
        if consensus_score > 0.4: direction = "UP"
        elif consensus_score < -0.4: direction = "DOWN"
        
        # 6. Adım: Veri Tabanına Kaydet
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO forecasts (agent_name, target_asset, score, direction) VALUES (?, ?, ?, ?)", 
                           ("NEXUS-CONSENSUUS", target_asset, round(abs(consensus_score), 2), direction))
            conn.commit()
            conn.close()
            logger.info(f"[⚖️ KONSENSÜS SAĞLANDI] Karar: {direction} | Skor: {abs(consensus_score):.2f}")
        except Exception as e:
            logger.error(f"Konsensüs kaydedilirken hata: {e}")

        # 7. Adım: Canlı Execution Köprüsü
        try:
            from core.execution_engine import ExecutionEngine
            executor = ExecutionEngine()
            mock_forecasts = {target_asset: {"direction": direction, "confidence": round(abs(consensus_score), 2)}}
            asset_type = "crypto" if target_asset == "BTC" else "equity"
            executor.process_forecasts_and_execute(mock_forecasts, asset_type=asset_type)
        except Exception as e:
            logger.error(f"Execution hatası: {e}")

        # 8. Adım: Evrimsel Döngü
        self.optimize_agent_weights(target_asset, direction, agent_signals)

        return {
            "asset": target_asset,
            "consensus_score": abs(consensus_score),
            "final_decision": direction,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }