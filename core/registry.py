"""
NEXUS Agent Registry System
Tracks and manages lifetimes of active autonomous entities.
"""
from core.logger import Logger

class AgentRegistry:
    def __init__(self):
        self.agents = {}
        self.logger = Logger("REGISTRY")

    def register(self, agent):
        self.agents[agent.name] = agent
        self.logger.info(f"Agent registered: {agent.name}")

    def get(self, name: str):
        return self.agents.get(name)

    def run_all(self, data=None):
        for agent in self.agents.values():
            self.logger.info(f"Running agent: {agent.name}")
            agent.run(data)