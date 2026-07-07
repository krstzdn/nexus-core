class SentinelAgent:
    def __init__(self):
        self.employee_id = "NX-SENTINEL-05"
        self.role = "Risk Limiti ve Maksimum Zarar Denetçisi"

    def check_risk_limits(self, consensus_score):
        # Şirketin batmasını engelleyen, kararları veto yetkisi olan katı filtre
        approved_decision = "HOLD"
        
        if consensus_score >= 68:
            approved_decision = "BUY"
        elif consensus_score <= 45:
            approved_decision = "SELL"

        return {
            "employee_id": self.employee_id,
            "approved_decision": approved_decision,
            "risk_status": "SAFE" if approved_decision == "HOLD" else "ACTION_REQUIRED"
        }