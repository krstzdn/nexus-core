"""
NEXUS Operating System - Fund Agent
Revised with Sentiment Analysis Integration.
"""
from core.agent import BaseAgent
from core.sentiment_analyzer import SentimentAnalyzer

class FundAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.sentiment = SentimentAnalyzer()

    def run(self, asset: str) -> dict:
        # Haber simülasyonu (İleride web scrape edilecek)
        news_headline = "Şirket yeni yatırım kararı ile büyüme hedeflerini güncelledi."
        
        # Duygu analizi uygula
        sentiment_score = self.sentiment.analyze(news_headline)
        
        # Temel tahmini duygu skoru ile modifiye et
        base_score = 0.75
        final_score = base_score + (sentiment_score * 0.2)
        
        return {
            "direction": "UP" if final_score > 0 else "DOWN",
            "score": final_score,
            "confidence": 0.85
        }