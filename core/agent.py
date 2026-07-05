"""
NEXUS Operating System - Base Agent Framework
Polymorphic base for all core intelligence entities.
"""
from abc import ABC, abstractmethod
from memory.memory_engine import MemoryEngine

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.status = "idle"
        # Her ajanın kendi hafıza dosyasını (örn: memory/dummy-agent.json) izole oluşturması sağlanır
        self.memory = MemoryEngine(self.name)

    @abstractmethod
    def run(self, data=None):
        pass

    def remember(self, key, value):
        """Ajanın ürettiği veriyi kendi izole JSON kasasına mühürler."""
        self.memory.save(key, value)

    def recall(self, key):
        """Ajanın kendi izole JSON kasasından geçmiş veriyi çağırır."""
        return self.memory.load(key)

    def log(self):
        return f"[AGENT:{self.name}] status={self.status}"