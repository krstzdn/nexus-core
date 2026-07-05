"""
NEXUS Kernel - Operational & Evolutionary Financial Network
Connects intelligence streams, validation engines, and execution protocols.
"""
import datetime
import time
from core.banner import show_banner
from core.registry import AgentRegistry
from core.logger import Logger
from agents.core.fund_agent import FundAgent
from agents.core.corporate_agent import CorporateAgent
from core.validator import ForecastValidator
from core.execution_engine import ExecutionEngine

logger = Logger("NEXUS-CORE")

class Kernel:
    def __init__(self):
        self.started = datetime.datetime.now(datetime.timezone.utc)
        self.registry = AgentRegistry()
        self.validator = ForecastValidator()
        self.executor = ExecutionEngine()
        
        self.fund_agent = FundAgent("fund-agent")
        self.corporate_agent = CorporateAgent("corp-agent")
        
        self.registry.register(self.fund_agent)
        self.registry.register(self.corporate_agent)

    def start(self):
        show_banner()
        logger.info("NEXUS Tam Otonom Ticaret ve Tahmin Çekirdeği ONLINE.")
        
        loop_count = 1
        try:
            while loop_count <= 1:
                logger.info(f"--- 🔄 AI OPERASYONEL DÖNGÜ: #{loop_count} ---")
                
                # 1. Tahmin Aşaması (Zeka)
                self.fund_agent.run("YHS")
                corp_analysis = self.corporate_agent.run()
                
                # 2. İşlem Aşaması (Eylem/Aksiyon)
                self.executor.process_forecasts_and_execute(corp_analysis["forecasts"])
                
                # 3. Denetim Aşaması (Evrimsel Feedback)
                print("-" * 50)
                self.validator.validate_predictions()
                print("-" * 50)
                
                loop_count += 1
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.warning("NEXUS AI Çekirdeği güvenli modda kapatıldı.")

if __name__ == "__main__":
    kernel = Kernel()
    kernel.start()