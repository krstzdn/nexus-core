"""
NEXUS Operating System - Execution & Order Routing Engine
Translates predictive AI signals into concrete financial portfolio allocations.
"""
import json
from pathlib import Path
from core.logger import Logger

logger = Logger("NEXUS-EXECUTION")

class ExecutionEngine:
    def __init__(self):
        self.memory_dir = Path(__file__).resolve().parent.parent / "memory"
        self.portfolio_path = self.memory_dir / "portfolio-agent.json"
        self.init_portfolio()

    def init_portfolio(self):
        """Eğer portföy hafızası yoksa veya bozuksa kurumsal başlangıç durumunu yaratır."""
        try:
            if self.portfolio_path.exists():
                with open(self.portfolio_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "balances" in data:
                        return  # Şema doğru, işlemi atla
            
            # Şema yoksa veya bozuksa yeniden oluştur
            self._create_default_portfolio()
        except (json.JSONDecodeError, KeyError):
            self._create_default_portfolio()

    def _create_default_portfolio(self):
        initial_state = {
            "balances": {"TRY": 100000.0, "KCHOL": 0.0, "THYAO": 0.0},
            "risk_profile": "conservative",
            "last_updated": "2026-07-06"
        }
        self.portfolio_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.portfolio_path, "w", encoding="utf-8") as f:
            json.dump(initial_state, f, indent=4)
        logger.info("[💼 PORTFÖY INITIALIZE] Yeni portföy kasası başarıyla oluşturuldu.")

    def process_forecasts_and_execute(self, forecasts: dict):
        """Tahmin sinyallerini okur, portföy dengesine göre emir çıkarır."""
        self.init_portfolio()  # Çalışma öncesi şema koruma kontrolü

        with open(self.portfolio_path, "r", encoding="utf-8") as f:
            portfolio = json.load(f)

        balances = portfolio["balances"]
        cash = float(balances.get("TRY", 0.0))

        logger.info(f"[💰 PORTFÖY DURUMU] Mevcut Nakit Tamponu: {cash:,.2f} TRY")

        for asset, data in forecasts.items():
            direction = data["direction"]
            confidence = data["confidence"]
            
            # Alım Stratejisi
            if direction == "UP" and cash > 10000:
                allocation = cash * 0.20 * confidence
                balances["TRY"] -= allocation
                shares_bought = round(allocation / 300, 2)
                balances[asset] = balances.get(asset, 0.0) + shares_bought
                cash -= allocation
                
                logger.info(
                    f"[🛒 EMİR TETİKLENDİ] ALIM -> {asset} | İletilen Tutar: {allocation:,.2f} TRY | "
                    f"Alınan Adet: {shares_bought} | Durum: ONAYLANDI"
                )
            
            # Satım Stratejisi
            elif direction == "DOWN" and balances.get(asset, 0.0) > 0:
                shares_to_sell = balances[asset] * 0.50
                revenue = shares_to_sell * 300
                balances[asset] -= shares_to_sell
                balances["TRY"] += revenue
                cash += revenue
                
                logger.warning(
                    f"[💥 EMİR TETİKLENDİ] SATIM -> {asset} | Satılan Adet: {shares_to_sell} | "
                    f"Elde Edilen Likidite: {revenue:,.2f} TRY"
                )

        portfolio["balances"] = balances
        portfolio["last_updated"] = "2026-07-06"
        
        with open(self.portfolio_path, "w", encoding="utf-8") as f:
            json.dump(portfolio, f, indent=4)