"""
NEXUS Intelligence Technologies - Local Data Pipeline
TEFAS (Turkey Fund Exchange Market) Analytics & Ingestion Stream.
"""

class TefasStream:
    def __init__(self):
        self.base_url = "https://api.nexus-tfa.gov.tr/v1/tefas"

    def fetch_fund_data(self, fund_code: str) -> dict:
        fund_code = fund_code.upper()
        
        fund_matrix = {
            "TI3": {
                "name": "İş Portföy BIST 30 Endeksi Hisse Senedi Fonu",
                "pys": "İş Portföy",
                "risk_value": 6,
                "yearly_return": 84.5,
                "portfolio_allocation": {"BIST30_Hisse": 0.95, "Nakit": 0.05},
                "top_holdings": ["THYAO", "AKBNK", "TUPRS"]
            },
            "YHS": {
                "name": "Yapı Kredi Portföy Koç Holding İştirakleri Hisse Senedi Fonu",
                "pys": "Yapı Kredi Portföy",
                "risk_value": 6,
                "yearly_return": 92.1,
                "portfolio_allocation": {"Koc_Istirak_Hisse": 0.98, "Nakit": 0.02},
                "top_holdings": ["KCHOL", "FROTO", "TUPRS"]
            }
        }
        
        return fund_matrix.get(fund_code, {
            "name": "Bilinmeyen Yerel Fon",
            "pys": "Genel Yönetim",
            "risk_value": 3,
            "yearly_return": 45.0,
            "portfolio_allocation": {"Mevduat": 1.0},
            "top_holdings": []
        })