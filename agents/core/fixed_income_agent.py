from memory.memory_engine import MemoryEngine

class FixedIncomeAgent:
    def __init__(self):
        self.employee_id = "NX-FIXEDINCOME-07"
        self.role = "Tahvil, Bono, Eurobond ve Mevduat Direktörü"
        self.memory = MemoryEngine(agent_name="fixed-income-agent")

    def analyze_asset(self, symbol, rate, oracle_report):
        # Faiz oranları ve sabit getiri makro analizi
        past_decisions = self.memory.load("decision_history") or []
        
        # Faiz oranları tatmin ediciyse nakit koruma amaçlı BUY verilir
        if rate > 45.0:  # Örn: %45 mevduat/tahvil faizi barajı
            decision = "BUY"
        else:
            decision = "HOLD"
            
        past_decisions.append(decision)
        self.memory.save("decision_history", past_decisions[-20:])
        
        return {"employee_id": self.employee_id, "decision": decision, "focus": "Risk-Free Getiri"}