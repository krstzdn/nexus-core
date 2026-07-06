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
            # Fallback (Veri tabanı boşsa varsayılan değerler)
            weights = {"corp-agent": 1.5, "crypto-agent": 0.95, "macro-agent": 1.1, "value-agent": 1.2}
        return weights

    def execute_council_session(self, target_asset: str) -> dict:
        """Ajan konseyini toplar, oylama yapar ve konsensüs kararını üretir."""
        logger.info(f"[🏛️ KONSEY TOPLANDI] Hedef Varlık: {target_asset} için karar oturumu başladı.")
        
        weights = self.get_agent_weights()
        
        # Simüle edilmiş bağımsız ajan raporları (Gerçek analiz modellerinin çıktıları)
        # Sinyal: 1.0 (Güçlü Al), -1.0 (Güçlü Sat), 0.0 (Bekle)
        if target_asset == "BTC":
            agent_signals = {
                "crypto-agent": {"signal": 1.0, "score": 0.85},
                "macro-agent": {"signal": 1.0, "score": 0.70},
                "value-agent": {"signal": 0.0, "score": 0.50},
                "corp-agent": {"signal": 1.0, "score": 0.75}
            }
        else:  # KCHOL, THYAO vb.
            agent_signals = {
                "crypto-agent": {"signal": 0.0, "score": 0.20},
                "macro-agent": {"signal": 1.0, "score": 0.65},
                "value-agent": {"signal": 1.0, "score": 0.80},
                "corp-agent": {"signal": 1.0, "score": 0.75}
            }

        weighted_signal_sum = 0.0
        total_weight = 0.0

        # Ağırlıklı Konsensüs Hesaplama
        for agent, data in agent_signals.items():
            weight = weights.get(agent, 1.0)
            weighted_signal_sum += data["signal"] * data["score"] * weight
            total_weight += weight

        consensus_score = weighted_signal_sum / total_weight if total_weight > 0 else 0.0
        
        # Skora göre nihai yön tayini
        if consensus_score > 0.4:
            direction = "UP"
        elif consensus_score < -0.4:
            direction = "DOWN"
        else:
            direction = "HOLD"

        # Kararı Veri Tabanına Mühürleme
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tahmin logunu ekle
            cursor.execute("""
                INSERT INTO forecasts (agent_name, target_asset, score, direction)
                VALUES (?, ?, ?, ?)
            """, ("NEXUS-CONSENSUUS", target_asset, round(abs(consensus_score), 2), direction))
            
            conn.commit()
            conn.close()
            logger.info(f"[⚖️ KONSENSÜS SAĞLANDI] Karar: {direction} | Skor: {abs(consensus_score):.2f}")
        except Exception as e:
            logger.error(f"Konsensüs kaydedilirken hata: {e}")

            # --- CANLI EXECUTION KÖPRÜSÜ (Eksiksiz Mevcut Yapı Entegrasyonu) ---
        try:
            from core.execution_engine import ExecutionEngine
            executor = ExecutionEngine()
            
            # execution_engine.py'nin beklediği sözlük (dict) formatında forecast verisi hazırlıyoruz
            mock_forecasts = {
                target_asset: {
                    "direction": direction,
                    "confidence": round(abs(consensus_score), 2)
                }
            }
            
            # Varlık tipine göre motorun doğru dala (equity/crypto) sapmasını sağlıyoruz
            asset_type = "crypto" if target_asset == "BTC" else "equity"
            
            # Sizin yazdığınız process_forecasts_and_execute fonksiyonunu ateşliyoruz
            executor.process_forecasts_and_execute(mock_forecasts, asset_type=asset_type)
            
            # --- EVRİMSEL DÖNGÜ TETİKLEYİCİSİ ---
            # Test senaryosunda konseyin kararını piyasanın doğru yönü kabul edip ajanları eğitiyoruz
            # (Gerçek veri entegrasyonunda buraya yfinance'ten gelen gerçek mum yönü verilecektir)
            self.optimize_agent_weights(target_asset, direction, agent_signals)
        except Exception as e:
            logger.error(f"Execution katmanı tetiklenirken hata: {e}")

        return {
            "asset": target_asset,
            "consensus_score": abs(consensus_score),
            "final_decision": direction,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    
    def optimize_agent_weights(self, target_asset: str, actual_direction: str, agent_signals: dict):
        """
        Konsey oturumundan sonra gerçek piyasa hareketini (actual_direction) alır.
        Doğru tahminde bulunan ajanların ağırlığını artırır, hatalı olanları cezalandırır.
        """
        logger.info(f"[🧬 EVRİMSEL DÖNGÜ] {target_asset} için ajan performansları puanlanıyor...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for agent_name, data in agent_signals.items():
                # Ajanın sinyal yönünü metne döküyoruz
                predicted_direction = "HOLD"
                if data["signal"] > 0:
                    predicted_direction = "UP"
                elif data["signal"] < 0:
                    predicted_direction = "DOWN"
                
                # Doğruluk kontrolü
                is_correct = (predicted_direction == actual_direction)
                
                # Veri tabanından ajanın mevcut istatistiklerini çek
                cursor.execute("SELECT weight, total_forecasts, success_rate FROM agent_weights WHERE agent_name = ?", (agent_name,))
                row = cursor.fetchone()
                
                if row:
                    current_weight, total_forecasts, success_rate = row
                    new_total_forecasts = total_forecasts + 1
                    
                    if is_correct:
                        # Haklı çıkan ajanın ağırlığına %5 bonus, başarı oranına pozitif etki
                        new_weight = min(current_weight * 1.05, 3.0) # Üst sınır 3.0
                        logger.info(f"🏅 {agent_name} DOĞRU TAHMİN -> Yeni Ağırlık: {new_weight:.2f}")
                    else:
                        # Hatalı tahmin yapan ajandan %5 kesinti
                        new_weight = max(current_weight * 0.95, 0.1) # Alt sınır 0.1
                        logger.warning(f"📉 {agent_name} HATALI TAHMİN -> Yeni Ağırlık: {new_weight:.2f}")
                    
                    # Veri tabanını güncelle
                    cursor.execute("""
                        UPDATE agent_weights 
                        SET weight = ?, total_forecasts = ?
                        WHERE agent_name = ?
                    """, (round(new_weight, 2), new_total_forecasts, agent_name))
                    
            conn.commit()
            conn.close()
            logger.info("[🏁 EVRİMSEL DÖNGÜ] Tüm ajan ağırlıkları başarıyla optimize edildi ve mühürlendi.")
        except Exception as e:
            logger.error(f"Geri besleme döngüsünde hata: {e}")