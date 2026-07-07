from memory.memory_engine import MemoryEngine

class FundAgent:
    def __init__(self):
        self.employee_id = "NX-FUND-05"
        self.role = "Yatırım Fonları ve BES Portföy Yönetim Uzmanı"
        self.memory = MemoryEngine(agent_name="fund-agent")

    def analyze_asset(self, symbol, current_price, oracle_report):
        """Fon dünyasını makro risk dengesine göre analiz eder."""
        sentiment = oracle_report.get("sentiment_score", 50)
        
        past_decisions = self.memory.load("decision_history") or []
        
        # Fonlar genelde daha defansiftir. Piyasa çok belirsizken (Nötr-Negatif) dengeli fon alımı kollanır.
        if 45 <= sentiment <= 60:
            decision = "BUY"
        elif sentiment < 35:
            decision = "SELL"  # Nakde geçiş sinyali
        else:
            decision = "HOLD"
            
        past_decisions.append(decision)
        self.memory.save("decision_history", past_decisions[-20:])
        
        return {
            "employee_id": self.employee_id, 
            "decision": decision, 
            "focus": "Fon Sepeti & BES Tahsisi"
        }