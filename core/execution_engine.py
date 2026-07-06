"""
NEXUS Operating System - Multi-Asset Execution Engine
Manages TRY (Equities) and USDT (Crypto) asset allocations simultaneously.
"""
import json
from pathlib import Path
from core.logger import Logger
from core.risk_manager import RiskManager

logger = Logger("NEXUS-EXECUTION")

class ExecutionEngine:
    def __init__(self):
        self.risk_manager = RiskManager()
        self.memory_dir = Path(__file__).resolve().parent.parent / "memory"
        self.portfolio_path = self.memory_dir / "portfolio-agent.json"

    def init_portfolio(self):
        if not self.portfolio_path.exists():
            initial_state = {
                "balances": {"TRY": 100000.0, "USDT": 5000.0, "KCHOL": 0.0, "THYAO": 0.0, "BTC": 0.0},
                "risk_profile": "hybrid_growth",
                "last_updated": "2026-07-06"
            }
            with open(self.portfolio_path, "w", encoding="utf-8") as f:
                json.dump(initial_state, f, indent=4)

    def process_forecasts_and_execute(self, forecasts: dict, asset_type: str = "equity"):
        self.init_portfolio()
        with open(self.portfolio_path, "r", encoding="utf-8") as f:
            portfolio = json.load(f)

            # Risk süzgecinden geçir
        safe_amount = self.risk_manager.calculate_safe_allocation(cash, data["confidence"], 0.04)
        
        # Risk süzgecinden geçir
        # forecasts sözlüğünden ilgili varlığın yön bilgisini çekiyoruz
        asset_forecast = forecasts.get(asset, {})
        direction = asset_forecast.get("direction", "HOLD")
        confidence = asset_forecast.get("confidence", 1.0)
        
        safe_amount = self.risk_manager.calculate_safe_allocation(cash, confidence, 0.04)
        
        if direction == "UP" and cash > 10000:
            allocation = safe_amount # Artık risk yönetimine bağlı
            # ... (geri kalan emir iletim mantığı)

        balances = portfolio["balances"]

        if asset_type == "equity":
            cash = float(balances.get("TRY", 0.0))
            for asset, data in forecasts.items():
                if data["direction"] == "UP" and cash > 10000:
                    allocation = cash * 0.20 * data["confidence"]
                    balances["TRY"] -= allocation
                    shares = round(allocation / 300, 2)
                    balances[asset] = balances.get(asset, 0.0) + shares
                    cash -= allocation
                    logger.info(f"[🛒 BİST EMİR] ALIM -> {asset} | {allocation:,.2f} TRY | Adet: {shares}")
        
        elif asset_type == "crypto":
            usdt_cash = float(balances.get("USDT", 0.0))
            asset = forecasts["asset"]
            data = forecasts["forecast"]
            
            if data["direction"] == "UP" and usdt_cash > 500:
                allocation = usdt_cash * 0.30 * data["confidence"]
                balances["USDT"] -= allocation
                # BTC Simüle fiyat: 62692 USD
                crypto_amount = round(allocation / 62692, 4)
                balances[asset] = balances.get(asset, 0.0) + crypto_amount
                usdt_cash -= allocation
                logger.info(f"[🪙 KRİPTO EMİR] ALIM -> {asset} | ${allocation:,.2f} USDT | Adet: {crypto_amount}")

        portfolio["balances"] = balances
        with open(self.portfolio_path, "w", encoding="utf-8") as f:
            json.dump(portfolio, f, indent=4)