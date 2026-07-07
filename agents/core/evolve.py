import sqlite3
import os

DB_PATH = os.path.join("data", "nexus_tfa.db")

class EvolveAgent:
    def __init__(self):
        self.employee_id = "NX-EVOLVE-08"
        self.role = "Kendi Kendini Geliştiren Strateji ve Geri Bildirim Uzmanı"

    def learn_from_performance(self, symbol):
        """
        Veritabanındaki geçmiş kararları inceler.
        Eğer bir BUY sinyalinden sonra fiyat yükselmişse strateji BAŞARILI,
        düşmüşse BAŞARISIZ kabul edilir (Öğrenme mekanizması).
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Son 10 işlemi zaman sırasına göre çekiyoruz
            cursor.execute("""
                SELECT price, decision FROM council_logs 
                WHERE symbol = ? 
                ORDER BY id DESC LIMIT 10
            """, (symbol,))
            rows = cursor.fetchall()
            conn.close()

            if len(rows) < 3:
                return {"status": "Yetersiz Veri", "efficiency_score": 100.0, "feedback": "Öğrenmek için daha fazla trade loguna ihtiyaç var."}

            # Ters kronolojiden düz kronolojiye çeviriyoruz (Eskiden yeniye)
            rows.reverse()
            
            successful_trades = 0
            total_evaluations = 0

            for i in range(len(rows) - 1):
                current_price = rows[i][0]
                current_decision = rows[i][1]
                next_price = rows[i+1][0]

                if current_decision == "BUY":
                    total_evaluations += 1
                    if next_price > current_price:  # Alım sonrası fiyat artmışsa başarılı
                        successful_trades += 1
                elif current_decision == "SELL":
                    total_evaluations += 1
                    if next_price < current_price:  # Satım sonrası fiyat düşmüşse başarılı (Kâr alındı veya short)
                        successful_trades += 1

            if total_evaluations == 0:
                return {"status": "Stabil", "efficiency_score": 100.0, "feedback": "Son işlemler bekleme (HOLD) ağırlıklı, trend stabil."}

            # Strateji Verimlilik Skoru (Yüzdesel)
            efficiency_score = round((successful_trades / total_evaluations) * 100, 2)
            
            feedback = "Strateji optimize çalışıyor."
            if efficiency_score < 50.0:
                feedback = "DİKKAT: Son kararların başarı oranı düştü! Sentinel risk limitlerini sıkılaştırmalı."
            elif efficiency_score > 75.0:
                feedback = "MÜKEMMEL: Alpha trend algoritmaları piyasayı domine ediyor."

            return {
                "employee_id": self.employee_id,
                "efficiency_score": efficiency_score,
                "feedback": feedback,
                "total_analyzed": total_evaluations
            }

        except Exception as e:
            return {"status": "Hata", "efficiency_score": 50.0, "feedback": f"Veri okuma hatası: {str(e)}"}