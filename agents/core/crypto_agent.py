"""
NEXUS Operating System - Crypto Predictive Agent
Analyzes global digital assets, order blocks, and on-chain sentiment.
"""
from core.agent import BaseAgent
from data.data_pipeline.global_streams.crypto_stream import CryptoStream
from core.llm_engine import LLMEngine
from data.database import DatabaseEngine

class CryptoAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.stream = CryptoStream()
        self.llm = LLMEngine()
        self.db = DatabaseEngine()

    def run(self, data=None) -> dict:
        self.status = "predictive_crypto_forecasting"
        metrics = self.stream.fetch_live_metrics()
        
        raw_context = f"Varlık: {metrics['asset']} | Fiyat: ${metrics['price_usd']} | Akış: {metrics['net_inflow_24h']} | Özet: {metrics['summary']}"
        forecast = self.llm.analyze_and_forecast("crypto", raw_context)
        
        # SQLite'a kaydet
        self.db.save_forecast(
            agent=self.name,
            asset=metrics['asset'],
            score=forecast["score"],
            direction=forecast["direction"],
            confidence=forecast["confidence"]
        )
        
        self.remember(f"forecast_{metrics['asset']}", forecast)
        self.status = "idle"
        return {"status": "SUCCESS", "forecast": forecast, "asset": metrics['asset']}