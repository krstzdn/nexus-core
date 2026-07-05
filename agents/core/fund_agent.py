"""
NEXUS Operating System - Fund Intelligence Agent
Analyzes TEFAS investment funds, PYŞ metrics, and systemic TR fund allocations.
"""
from core.agent import BaseAgent
# Yeni hiyerarşiye uygun güvenli import hattı
from data.data_pipeline.local_streams.tefas_stream import TefasStream

class FundAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.stream = TefasStream()

    def run(self, data=None) -> dict:
        self.status = "analyzing_tefas_funds"
        fund_code = data if isinstance(data, str) else "YHS"
        
        fund_info = self.stream.fetch_fund_data(fund_code)
        yearly_ret = fund_info.get("yearly_return", 0)
        risk_val = fund_info.get("risk_value", 5)
        efficiency_score = round((yearly_ret / (risk_val * 10)), 2)
        
        self.remember(f"analysis_{fund_code}", {
            "efficiency": efficiency_score,
            "pys": fund_info["pys"],
            "top_holdings": fund_info["top_holdings"]
        })
        
        self.status = "idle"
        return {
            "fund": fund_code,
            "pys": fund_info["pys"],
            "score": efficiency_score,
            "decision": "ACCUMULATE" if efficiency_score > 1.2 else "HOLD"
        }