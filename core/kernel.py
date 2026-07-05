"""
NEXUS Kernel - Evolutionary Predictive TR Financial Network
Incorporates self-correcting validation loops and dynamic agent weightings.
"""
import datetime
import time
from core.banner import show_banner
from core.registry import AgentRegistry
from core.logger import Logger
from agents.core.fund_agent import FundAgent
from agents.core.corporate_agent import CorporateAgent
from core.validator import ForecastValidator

logger = Logger("NEXUS-CORE")

class Kernel:
    def __init__(self):
        self.started = datetime.datetime.now(datetime.timezone.utc)
        self.registry = AgentRegistry()
        self.validator = ForecastValidator()
        
        self.fund_agent = FundAgent("fund-agent")
        self.corporate_agent = CorporateAgent("corp-agent")
        
        self.registry.register(self.fund_agent)
        self.registry.register(self.corporate_agent)

    def start(self):
        show_banner()
        logger.info("NEXUS Evrimsel Tahmin ve Karar Motoru Aktif. Öz-Düzeltme Döngüsü Devrede.")
        
        loop_count = 1
        try:
            while loop_count <= 2:
                logger.info(f"--- 🔄 AI EVRİMSEL OTURUMU: #{loop_count} ---")
                
                # 1. Tahminleri Üret
                fund_analysis = self.fund_agent.run("YHS")
                corp_analysis = self.corporate_agent.run()
                
                local_scores = []
                for ticker, forecast in corp_analysis["forecasts"].items():
                    logger.info(
                        f"[🔮 TAHMİN] Varlık: {ticker} | Yön: {forecast['direction']} | "
                        f"Sinyal: {forecast['score']:.2f} | Güven: %{forecast['confidence']*100:.0f}"
                    )
                    local_scores.append(forecast['score'])
                
                # 2. Döngü Sonunda Otonom Denetleyiciyi Tetikle (Öz-Düzeltme / Feedback Loop)
                print("-" * 40)
                self.validator.validate_predictions()
                print("-" * 40)
                
                loop_count += 1
                time.sleep(2)
                
        except KeyboardInterrupt:
            logger.warning("NEXUS AI Çekirdeği kapatıldı.")

if __name__ == "__main__":
    kernel = Kernel()
    kernel.start()