class AtlasAgent:
    def __init__(self):
        self.employee_id = "NX-ATLAS-04"
        self.role = "Varlık Dağılımı ve Stratejik Fon Yöneticisi"

    def allocation_strategy(self, decision):
        # Alınan karara göre portföy ağırlıklarını belirler
        if decision == "BUY":
            return {"Büyüme Şirketleri/Kripto": 70, "Teknoloji": 15, "Alternatif": 10, "Nakit": 5}
        return {"Hisse": 40, "Tahvil": 20, "Altın": 15, "Kripto": 10, "Nakit": 15}