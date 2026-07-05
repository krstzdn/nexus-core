"""
NEXUS Intelligence Technologies - Memory Subsystem
Handles deterministic, isolated JSON-based state persistence per autonomous agent.
"""
import json
from pathlib import Path

class MemoryEngine:
    def __init__(self, agent_name="default"):
        self.base_dir = Path(__file__).resolve().parent
        self.base_dir.mkdir(exist_ok=True)

        self.file_path = self.base_dir / f"{agent_name}.json"

        if not self.file_path.exists():
            self.file_path.write_text("{}", encoding="utf-8")

    def load_all(self):
        """Diskteki JSON dosyasını güvenli bir şekilde okur."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Dosya bozuk, boş veya silinmişse sistemi çökertme, boş şema dön.
            return {}

    def save(self, key, value):
        data = self.load_all()
        data[key] = value

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load(self, key):
        return self.load_all().get(key)