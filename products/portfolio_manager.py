from datetime import datetime

class AllWeatherPortfolio:
    def __init__(self):
        self.product_id = "NX-PROD-ALLWEATHER"
        self.product_name = "NEXUS All-Weather Portfolio"
        
    def generate_balanced_portfolio(self, department_decisions, global_sentiment):
        """Tüm departman şeflerinin kararlarını ortak holding ürününe dönüştürür."""
        allocation = {
            "EQUITY (Hisse)": 30.0,
            "COMMODITY (Altın/Emtia)": 15.0,
            "FIXED_INCOME (Tahvil/Eurobond)": 40.0,
            "FUND / BES": 10.0,
            "CRYPTO (Kripto)": 5.0
        }
        
        if global_sentiment < 40:
            allocation["EQUITY (Hisse)"] -= 10.0
            allocation["CRYPTO (Kripto)"] -= 3.0
            allocation["COMMODITY (Altın/Emtia)"] += 8.0
            allocation["FIXED_INCOME (Tahvil/Eurobond)"] += 5.0
        elif global_sentiment > 70:
            allocation["EQUITY (Hisse)"] += 10.0
            allocation["CRYPTO (Kripto)"] += 5.0
            allocation["FIXED_INCOME (Tahvil/Eurobond)"] -= 12.0
            allocation["COMMODITY (Altın/Emtia)"] -= 3.0

        total = sum(allocation.values())
        for k in allocation:
            allocation[k] = round((allocation[k] / total) * 100, 2)

        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "generation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_allocations": allocation,
            "market_regime": "DEFANSİF" if global_sentiment < 40 else ("AGRESİF" if global_sentiment > 70 else "DENGELİ")
        }