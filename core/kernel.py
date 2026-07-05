"""
NEXUS Kernel - Multi-Asset Hybrid Predictive Network
Orchestrates TR Financial streams and Global Crypto asset prediction/execution.
"""
import datetime
import time
from core.banner import show_banner
from core.registry import AgentRegistry
from core.logger import Logger
from agents.core.fund_agent import FundAgent
from agents.core.corporate_agent import CorporateAgent
from agents.core.crypto_agent import CryptoAgent
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
        self.crypto_agent = CryptoAgent("crypto-agent")
        
        self.registry.register(self.fund_agent)
        self.registry.register(self.corporate_agent)
        self.registry.register(self.crypto_agent)

    def start(self):
        show_banner()
        logger.info("NEXUS Çoklu Varlık Hibrit Tahmin ve Ticaret Çekirdeği ONLINE.")
        
        loop_count = 1
        try:
            while loop_count <= 1:
                logger.info(f"--- 🔄 AI HİBRİT OPERASYONEL DÖNGÜ: #{loop_count} ---")
                
                # 1. FAZ: TR FİNANS AĞI (BİST)
                self.fund_agent.run("YHS")
                corp_analysis = self.corporate_agent.run()
                self.executor.process_forecasts_and_execute(corp_analysis["forecasts"], asset_type="equity")
                
                # 2. FAZ: KÜRESEL DİJİTAL VARLIKLAR (KRİPTO)
                crypto_analysis = self.crypto_agent.run()
                self.executor.process_forecasts_and_execute(crypto_analysis, asset_type="crypto")
                
                # 3. FAZ: ÖZ-DÜZELTME VE DENETİM
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