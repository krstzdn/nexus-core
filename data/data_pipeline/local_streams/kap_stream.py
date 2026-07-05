"""
NEXUS Intelligence Technologies - Local Data Pipeline
KAP (Public Disclosure Platform) Semantic Notification Stream.
"""

class KapStream:
    def __init__(self):
        self.source = "KAP Live RSS/XML"

    def fetch_latest_disclosures(self) -> list:
        """KAP'a düşen en son kurumsal şirket bildirimlerini döner."""
        return [
            {
                "ticker": "KCHOL",
                "company": "Koç Holding A.Ş.",
                "type": "Yeni İş İlişkisi",
                "summary": "Yenilenebilir enerji iştirakinin devasa bir küresel ihracat ihalesi kazandığı açıklandı."
            },
            {
                "ticker": "THYAO",
                "company": "Türk Hava Yolları AO",
                "type": "Trafik Sonuçları",
                "summary": "Yıllık yolcu doluluk oranlarında rekor büyüme kaydedildi."
            }
        ]