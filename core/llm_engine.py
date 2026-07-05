"""
NEXUS Intelligence Technologies - LLM Engine
Performs semantic analysis and predictive forecasting on live financial streams.
"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMEngine:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.is_mock = not self.api_key or "your_openai" in self.api_key
        if not self.is_mock:
            self.client = OpenAI(api_key=self.api_key)

    def analyze_and_forecast(self, perspective: str, raw_data: str) -> dict:
        """
        Gelen canlı veriyi perspektife göre yorumlar ve geleceğe yönelik tahmin üretir.
        Dönen Format: {"score": 0.85, "direction": "UP", "forecast_horizon": "1W", "confidence": 0.90}
        """
        if self.is_mock:
            # Geliştirme ortamı için akıllı fallback mekanizması
            return {
                "score": 0.75 if "ihale" in str(raw_data).lower() or "rekor" in str(raw_data).lower() else 0.55,
                "direction": "UP",
                "forecast_horizon": "1W",
                "confidence": 0.80
            }

        try:
            system_prompt = (
                f"Sen NEXUS AI Holding'in {perspective.upper()} analiz ve tahmin motorusun. "
                "Sana iletilen canlı finansal veriyi incele, geleceğe yönelik (1 haftalık) trend tahmini yap. "
                "Yanıtı kesinlikle sadece şu JSON formatında dön, başka hiçbir metin ekleme:\n"
                '{"score": 0.00, "direction": "UP/DOWN/SIDEWAYS", "forecast_horizon": "1W", "confidence": 0.00}'
            )

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Canlı İstihbarat Akışı: {raw_data}"}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content.strip())
        except Exception:
            return {"score": 0.50, "direction": "SIDEWAYS", "forecast_horizon": "1W", "confidence": 0.50}