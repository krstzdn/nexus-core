from memory.memory_engine import MemoryEngine

class CommodityAgent:
    def __init__(self):
        self.employee_id = "NX-COMMODITY-06"
        self.role = "Değerli Madenler ve Emtia Piyasaları Uzmanı"
        self.memory = MemoryEngine(agent_name="commodity-agent")

    def analyze_asset(self, symbol, current_price, oracle_report):
        # Altın/Gümüş gibi güvenli limanlar jeopolitik risk yükseldikçe (Haber skoru düştükçe) değer kazanır
        risk_score = oracle_report.get("sentiment_score", 50)
        
        past_decisions = self.memory.load("decision_history") or []
        
        # Jeopolitik risk veya makro stres yüksekse emtiaya alım bas
        if risk_score < 45:
            decision = "BUY"
        elif risk_score > 75:
            decision = "SELL"
        else:
            decision = "HOLD"
            
        past_decisions.append(decision)
        self.memory.save("decision_history", past_decisions[-20:])
        
        return {"employee_id": self.employee_id, "decision": decision, "focus": "Güvenli Liman Akışı"}