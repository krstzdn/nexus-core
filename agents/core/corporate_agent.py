"""
NEXUS Operating System - Corporate Predictive Agent
"""
from core.agent import BaseAgent
from data.data_pipeline.local_streams.kap_stream import KapStream
from core.llm_engine import LLMEngine
from data.database import DatabaseEngine

class CorporateAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.stream = KapStream()
        self.llm = LLMEngine()
        self.db = DatabaseEngine()

    def run(self, data=None) -> dict:
        self.status = "predictive_kap_forecasting"
        disclosures = self.stream.fetch_latest_disclosures()
        
        corporate_forecasts = {}
        for item in disclosures:
            ticker = item["ticker"]
            
            # Zeka ve Veri Derinliğinin Birleşimi: Canlı LLM Tahmini
            raw_context = f"Şirket: {item['company']} | Tip: {item['type']} | Özet: {item['summary']}"
            forecast = self.llm.analyze_and_forecast("corporate", raw_context)
            
            # Veri Tabanına Mühürleme
            self.db.save_forecast(
                agent=self.name,
                asset=ticker,
                score=forecast["score"],
                direction=forecast["direction"],
                confidence=forecast["confidence"]
            )
            
            corporate_forecasts[ticker] = forecast
            self.remember(f"forecast_{ticker}", forecast)
            
        self.status = "idle"
        return {"status": "SUCCESS", "forecasts": corporate_forecasts}