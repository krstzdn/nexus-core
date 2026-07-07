# Dosya bir alt klasörde olduğu için memory modülünü import ederken hata almamak adına
# Eğer kernel üzerinden çağrılıyorsa root dizini baz alınır.
from memory.memory_engine import MemoryEngine

class ProphetAgent:
    def __init__(self):
        self.employee_id = "NX-PROPHET-03"
        self.role = "Gelecek Görünüm ve Sinyal Modelleme Uzmanı (Hafıza Güçlü)"
        # Mevcut mimarinize göre ajan adına özel hafıza dosyasını bağlıyoruz: crypto-agent.json
        self.memory = MemoryEngine(agent_name="crypto-agent")

    def generate_forecast(self, vector_report, oracle_report):
        sentiment = oracle_report["sentiment_score"]
        state = vector_report["position_state"]

        # --- MEVCUT HAFIZADAN VERI OKUMA ---
        # Mevcut load() metodunuzu kullanarak geçmiş kararları kontrol ediyoruz
        past_trends = self.memory.load("trend_history") or []

        # Son 5 döngüdeki "UPWARD" (Yükseliş) kararlarının sayısını bulalım
        past_buy_count = sum(1 for tx in past_trends[-5:] if tx == "UPWARD")

        if state == "UNDERVALUED":
            agent_consensus = int(68 + (sentiment * 0.25))
        else:
            agent_consensus = int(38 - (sentiment * 0.1))

        # FOMO / Aşırı Şişme Dengesi: Ardışık yükseliş serisinde temkinli yaklaşım
        if past_buy_count >= 4 and state == "OVERVALUED":
            agent_consensus -= 12

        agent_consensus = max(15, min(95, agent_consensus))
        consensus_score = round((agent_consensus * 0.7) + (sentiment * 0.3), 2)
        direction = "UPWARD" if consensus_score >= 68 else ("DOWNWARD" if consensus_score <= 45 else "SIDEWAYS")

        # --- MEVCUT HAFIZAYA VERI YAZMA ---
        # Yeni kararımızı geçmiş listesine ekleyip save() metoduyla diske kilitliyoruz
        past_trends.append(direction)
        if len(past_trends) > 20:  # Hafızanın şişmesini engelliyoruz
            past_trends.pop(0)
            
        self.memory.save("trend_history", past_trends)
        self.memory.save("last_consensus_score", consensus_score)

        return {
            "employee_id": self.employee_id,
            "consensus_score": consensus_score,
            "direction": direction
        }