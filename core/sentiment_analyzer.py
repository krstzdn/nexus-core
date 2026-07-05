"""
NEXUS Intelligence - News Sentiment Analysis Layer
Evaluates the emotional impact of news headlines on financial assets.
"""
from core.logger import Logger

logger = Logger("NEXUS-SENTIMENT")

class SentimentAnalyzer:
    def __init__(self):
        # Basit bir skorlama sözlüğü (Daha sonra LLM ile değiştirilecek)
        self.keywords = {
            "yükseliş": 0.5, "kar": 0.4, "yatırım": 0.3, "büyüme": 0.6,
            "yeni iş": 0.5, "anlaşma": 0.4, "temettü": 0.3, "rekor": 0.6,
            "düşüş": -0.5, "zarar": -0.6, "risk": -0.3, "kriz": -0.8,
            "enflasyon": -0.4, "belirsizlik": -0.3, "kayıp": -0.7, "borç": -0.4
        }
        

    def analyze(self, headline: str) -> float:
        score = 0.0
        headline_lower = headline.lower()
        for word, val in self.keywords.items():
            if word in headline_lower:
                score += val
        
        # Sınırlandırma
        score = max(-1.0, min(1.0, score))
        logger.info(f"[📊 DUYGU ANALİZİ] Haber: '{headline}' | Duygu Skoru: {score}")
        return score