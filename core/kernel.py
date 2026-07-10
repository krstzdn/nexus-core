import asyncio
import httpx
from datetime import datetime

# 1. ORTAK YÖNETİM VE DENETİM KADROSU
from agents.core.oracle import OracleAgent
from agents.core.vector import VectorAgent
from agents.core.prophet import ProphetAgent
from agents.core.atlas import AtlasAgent
from agents.core.sentinel import SentinelAgent
from agents.core.evolve import EvolveAgent
from data.database import save_market_state_to_db
from memory import memory_engine

# 2. VARLIK SINIFI UZMANLARI (DEPARTMAN ŞEFLERİ)
from agents.core.commodity_agent import CommodityAgent
from agents.core.fixed_income_agent import FixedIncomeAgent
from agents.core.equity_agent import EquityAgent  # <-- YENİ İŞE ALIM
from agents.core.fund_agent import FundAgent      # <-- YENİ İŞE ALIM

# 3. HOLDİNG ÜRÜN KATMANI
from products.portfolio_manager import AllWeatherPortfolio 

class NexusCore:
    def __init__(self):
        print("[NEXUS CORE] AI CEO -> Tüm Varlık Sınıfları Yönetim Kurulu Aktif.")
        
        # Üst Yönetim
        self.oracle = OracleAgent()
        self.vector = VectorAgent()
        self.prophet = ProphetAgent()
        self.atlas = AtlasAgent()
        self.sentinel = SentinelAgent()
        self.evolve = EvolveAgent()
        
        # Departmanlar
        self.commodity_dept = CommodityAgent()
        self.fixed_income_dept = FixedIncomeAgent()
        self.equity_dept = EquityAgent()
        self.fund_dept = FundAgent()
        
        self.shared_market_state = {
            "current_asset_class": "CRYPTO",
            "current_symbol": "BTC",
            "live_price": 0.0,
            "oracle_report": {},
            "vector_analysis": {},
            "prophet_forecast": {},
            "portfolio_allocation": {},
            "evolve_report": {},
            "department_decision": {},  # Aktif departmanın kararı buraya yazılır
            "final_decision": "HOLD",
            "consensus_score": 50.0
        }

    async def run_pipeline(self, client, symbol, asset_class="CRYPTO"):
        self.shared_market_state["current_asset_class"] = asset_class
        self.shared_market_state["current_symbol"] = symbol
        
        # I. ADIM: Makro İstihbarat (Haber taraması asenkron tetiklenir)
        self.shared_market_state["oracle_report"] = await self.oracle.analyze_news_sentiment(symbol)
        
        # II. ADIM: Fiyat Akış Motoru (Varlık Sınıfına Göre Süzgeç)
        if asset_class == "CRYPTO":
            try:
                url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
                response = await client.get(url, timeout=0.8)
                if response.status_code == 200:
                    self.shared_market_state["live_price"] = float(response.json()['price'])
            except Exception:
                self.shared_market_state["live_price"] = 63000.0 # Fallback stabil fiyat
        else:
            # Emtia, Hisse, Fon veya Tahvil için simüle/fiktif fiyat takibi veya sabit veri girişi
            # Gelecekte buraya TradingView veya Yahoo Finance API entegrasyonu gelecek
            self.shared_market_state["live_price"] = 100.0  # Varsayılan başlangıç birim değeri

        # III. ADIM: İlgili Departmanın Karar Üretmesi
        price = self.shared_market_state["live_price"]
        oracle = self.shared_market_state["oracle_report"]

        if asset_class == "COMMODITY":
            self.shared_market_state["department_decision"] = self.commodity_dept.analyze_asset(symbol, price, oracle)
        elif asset_class == "FIXED_INCOME":
            self.shared_market_state["department_decision"] = self.fixed_income_dept.analyze_asset(symbol, 45.0, oracle)
        elif asset_class == "EQUITY":
            self.shared_market_state["department_decision"] = self.equity_dept.analyze_asset(symbol, price, oracle)
        elif asset_class == "FUND":
            self.shared_market_state["department_decision"] = self.fund_dept.analyze_asset(symbol, price, oracle)
        else:
            self.shared_market_state["department_decision"] = {"focus": "Kripto Altyapısı"}

        # IV. ADIM: Konsensüs, Risk Denetimi ve Kapanış
        self.shared_market_state["vector_analysis"] = self.vector.process_mining(symbol, price)
        
        self.shared_market_state["prophet_forecast"] = self.prophet.generate_forecast(
            self.shared_market_state["vector_analysis"], oracle
        )

        c_score = self.shared_market_state["prophet_forecast"]["consensus_score"]
        risk_report = self.sentinel.check_risk_limits(c_score)
        
        final_decision = risk_report["approved_decision"]
        self.shared_market_state["portfolio_allocation"] = self.atlas.allocation_strategy(final_decision)

        self.shared_market_state["final_decision"] = final_decision
        self.shared_market_state["consensus_score"] = c_score
        self.shared_market_state["evolve_report"] = self.evolve.learn_from_performance(symbol)

        # Arşivleme
        save_market_state_to_db(self.shared_market_state)

        return self.shared_market_state