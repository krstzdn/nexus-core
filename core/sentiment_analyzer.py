"""
NEXUS Operating System - Sentiment Analysis Module
Parses global and local financial news headlines to calculate real-time market sentiment scores.
"""
from core.logger import Logger

logger = Logger("NEXUS-SENTIMENT")

class SentimentAnalyzer:
    def __init__(self):
        self.default_score = 0.0  # Nötr bakiye

    def fetch_latest_headlines(self, asset: str) -> list:
        """İlgili varlığa ait en son finansal haber başlıklarını simüle eder (Veya API bağlar)."""
        # Canlı veri pipeline'ı öncesi kararlı haber matrisi
        if asset == "BTC":
            return [
                "Fed hints at potential rate cuts, lifting crypto sentiment",
                "Major exchange faces minor regulatory hurdles in Europe",
                "Bitcoin whale accumulation hits 6-month high"
            ]
        elif asset == "KCHOL":
            return [
                "Koç Holding yeni sürdürülebilirlik yatırımlarını duyurdu",
                "Holding iştiraklerinden rekor çeyrek kar beklentisi",
                "Küresel piyasalardaki yavaşlama sanayi endeksini baskılıyor"
            ]
        return ["Market trading within historical daily average ranges"]

    def analyze_asset_sentiment(self, asset: str) -> float:
        """
        Haber başlıklarını NLP mantığıyla tarar ve -1.0 (Aşırı Negatif) ile +1.0 (Aşırı Pozitif)
        arasında ağırlıklı bir duygu skoru üretir.
        """
        headlines = self.fetch_latest_headlines(asset)
        logger.info(f"[📰 HABER SÜZGECİ] {asset} için {len(headlines)} güncel başlık analiz ediliyor...")
        
        # Basit kelime ağırlıklı NLP / Duygu Skorlama Mantığı
        positive_keywords = ["cut", "high", "accumulation", "kar", "rekor", "yatırım", "pozitif", "growth"]
        negative_keywords = ["hurdle", "baskı", "yavaşlama", "drop", "fall", "risk", "enflasyon"]
        
        total_score = 0.0
        for title in headlines:
            score = 0.0
            words = title.lower().split()
            for word in words:
                if word in positive_keywords:
                    score += 0.3
                if word in negative_keywords:
                    score -= 0.3
            total_score += score
            
        # Skor sınırlandırma (-1.0 ile +1.0 arası)
        final_score = max(min(total_score / len(headlines), 1.0), -1.0)
        logger.info(f"🧠 [DUYGU SKORU] {asset} Net Sentiment: {final_score:+.2f}")
        return round(final_score, 2)