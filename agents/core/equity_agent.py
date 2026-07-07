from memory.memory_engine import MemoryEngine

class EquityAgent:
    def __init__(self):
        self.employee_id = "NX-EQUITY-04"
        self.role = "Hisse Senetleri ve Küresel Borsalar Direktörü"
        # Mevcut memory yapınıza uygun olarak kendi dosyasını yönetir
        self.memory = MemoryEngine(agent_name="equity-agent")

    def analyze_asset(self, symbol, current_price, oracle_report):
        """Hisse senetlerini endeks eğilimi ve haber duyarlılığına göre analiz eder."""
        sentiment = oracle_report.get("sentiment_score", 50)
        
        past_decisions = self.memory.load("decision_history") or []
        
        # Hisse senetleri ekonomik büyüme ve pozitif haber akışından (Boğa sentimenti) beslenir
        if sentiment > 65:
            decision = "BUY"
        elif sentiment < 40:
            decision = "SELL"
        else:
            decision = "HOLD"
            
        past_decisions.append(decision)
        # Hafızayı son 20 işlemle sınırlandırıp kaydediyoruz
        self.memory.save("decision_history", past_decisions[-20:])
        
        return {
            "employee_id": self.employee_id, 
            "decision": decision, 
            "focus": "Hisse & Endeks Stratejisi"
        }