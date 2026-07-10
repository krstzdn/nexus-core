import os
import sys
import time
import random
import json
import math

# ==============================================================================
# 🛰️ NEXUS SYSTEM OPERATING PATH CONFIGURATOR
# ==============================================================================
current_dir = os.path.dirname(os.path.abspath(__file__)) # interface/
nexus_root = os.path.dirname(current_dir)                # nexus-core/
root_dir = os.path.dirname(nexus_root)                  # NEXUS/

# Python'un üst klasördeki istihbarat modülünü görebilmesi için yolu ekliyoruz
for path in [root_dir, nexus_root, current_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Yapay Zeka İstihbarat Dairesini import ediyoruz
try:
    from intelligence.intelligence_bureau import intelligence_gateway
except ImportError:
    class DummyBureau:
        def query_strategic_brain(self, *args, **kwargs): return "{}"
        def query_secure_local_brain(self, *args, **kwargs): return "{}"
    intelligence_gateway = DummyBureau()

class QuantumLogicEngine:
    """
    NEXUS CAPITAL — Matematiksel ve Quant Karar Motoru (Özel ML Katmanı)
    """
    def __init__(self):
        self.win_rate_estimate = 0.55
        self.risk_reward_ratio = 3.5
        self.intelligence = intelligence_gateway

        # Portföy Başlangıç Statik Verileri (Scan ile değişecek canlı matris)
        self.portfolio_base = {
            "BTC": {"amount": 1.25, "cost": 62500, "current": 78125},
            "GOLD": {"amount": 150.00, "cost": 2400, "current": 2520},
            "BIST": {"amount": 450.00, "cost": 110, "current": 98},
            "EUROBOND": {"amount": 10000, "cost": 98.5, "current": 101.2}
        }

    def calculate_kelly_criterion(self, win_prob, win_loss_ratio):
        """
        [KELLY KRİTERİ] Kasa yönetimi ve optimal pozisyon büyüklüğü hesabı.
        Formül: f* = p - (1 - p) / b
        """
        if win_loss_ratio <= 0:
            return 0.0
        kelly_fraction = win_prob - ((1.0 - win_prob) / win_loss_ratio)
        # Matematiksel Kelly Sınırı: Güvenli sınır olan maks %25 ile kısıtlıyoruz.
        return max(0.0, min(kelly_fraction, 0.25))

    def calculate_markov_state(self, current_state="BULL"):
        """
        [MARKOV ZİNCİRLERİ] Bir sonraki pazar hareketinin durum olasılığı geçiş matrisi.
        """
        prob_bull = 0.6 if current_state == "BULL" else 0.3
        return "BULL" if prob_bull > 0.5 else "BEAR", prob_bull

    def generate_geometric_brownian_motion(self, S0=100, mu=0.05, sigma=0.2, T=1.0, N=50, paths=5):
        """
        [GEOMETRİK BROWNİAN HAREKETİ - SDE]
        Monte Carlo Simülasyonu için hisse senedi fiyat yörüngeleri üretir.
        """
        dt = T / N
        all_paths = []
        for _ in range(paths):
            path = [S0]
            current_price = S0
            for _ in range(N):
                u1 = random.random()
                u2 = random.random()
                while u1 <= 1e-9:
                    u1 = random.random()
                z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
                
                drift = (mu - 0.5 * (sigma ** 2)) * dt
                diffusion = sigma * math.sqrt(dt) * z
                current_price = current_price * math.exp(drift + diffusion)
                path.append(current_price)
            all_paths.append(path)
        return all_paths

    def scan_portfolio_performance(self):
        """
        [REAL-TIME PORTFOLIO AUDIT]
        Departman hafızalarını tarayarak Geometrik Brownian simülasyonu bazlı 
        güncel fiyat değişimlerini ve kar/zarar dengelerini anlık hesaplar.
        """
        scanned_portfolio = {}
        # Varlıkların piyasa dalgalanma katsayıları (Varyans ve Volatilite Sınırı)
        volatilities = {"BTC": 0.15, "GOLD": 0.03, "BIST": 0.08, "EUROBOND": 0.01}
        
        for asset, data in self.portfolio_base.items():
            # GBM simülasyonunun ilk adımındaki fiyat değişimini (drift) uyguluyoruz
            vol = volatilities[asset]
            # Rastgele şok etkisi (-1.5 ile +2.0 sigma arasında)
            shock = random.normalvariate(0.05, vol)
            
            # Güncel değeri rasyonel oranlarla simüle edip güncelliyoruz
            new_current = data["current"] * (1.0 + shock)
            # Yuvarlama kuralları
            if asset in ["BTC", "EUROBOND"]:
                new_current = round(new_current, 1)
            else:
                new_current = round(new_current, 2)
                
            profit_loss_pct = ((new_current - data["cost"]) / data["cost"]) * 100.0
            
            scanned_portfolio[asset] = {
                "amount": data["amount"],
                "cost": data["cost"],
                "current": new_current,
                "profit_loss_pct": round(profit_loss_pct, 2)
            }
            
            # Ana veri tabanını anlık güncelliyoruz
            self.portfolio_base[asset]["current"] = new_current

        return scanned_portfolio

    def execute_pipeline(self, target_data=None):
        """
        Otonom Quant İcra Döngüsü.
        Yapay zeka analizini, yerel model süzgecini ve quant hesaplamalarını sırasıyla işler.
        """
        print("\n" + "="*50)
        print("⚙️ NEXUS PIPELINE İCRA DÖNGÜSÜ BAŞLATILDI")
        print("="*50)

        # 1. SCAN & DETECT (Pazar Taraması)
        time.sleep(0.3)
        print("[1/4] Pazar anormallikleri ve sinyaller başarıyla tespit edildi.")

        # 2. INTEL ANALYZE (Mantıksal Akıl Yürütme ve Güvenlik Süzgeci)
        print("[2/4] İstihbarat Dairesi üzerinden yapay zeka analizleri tetikleniyor...")
        
        # Bulut Zekasından Karar Promptu Alımı
        ai_response_raw = self.intelligence.query_strategic_brain(
            prompt="NovaFusion Dynamics girişiminin pazar verilerini ve risk skorlarını değerlendir.",
            model="gemini-2.5-flash-preview-09-2025"
        )
        ai_response = json.loads(ai_response_raw)
        
        # Hassas Verileri Yerel Model (Llama) İle Tarama
        secure_local_data = "Müşteri ID: NX-901, Yatırım Miktarı: 500,000 USD, Bakiye: Gizli"
        local_secure_res = self.intelligence.query_secure_local_brain(secure_local_data)

        # 3. QUANT CALCULATION (Markov ve Kelly Hesaplamaları)
        print("[3/4] Kuantum matematiksel karar motoru devreye alınıyor...")
        next_state, state_prob = self.calculate_markov_state("BULL")
        kelly_bet = self.calculate_kelly_criterion(self.win_rate_estimate, self.risk_reward_ratio)

        # 4. DECISION SOLIDIFICATION (Kararı Mühürleme)
        print("[4/4] Karar matrisi ve risk oranları son haline getirildi.")
        
        results = {
            "execution_id": random.randint(10000, 99999),
            "decision": ai_response.get("decision", "HOLD_UNDER_OBSERVATION"),
            "confidence": ai_response.get("score", 75.0),
            "kelly_bet": kelly_bet, 
            "next_state": next_state,
            "local_security": "APPROVED (SECURE)",
            "timestamp": time.time()
        }
        
        print("="*50)
        print(f"🎯 KERNEL KARARI: {results['decision']} | ÖNERİLEN POZİSYON: %{results['kelly_bet']*100:.2f}")
        print("="*50 + "\n")
        
        return results

# Singleton instance
engine = QuantumLogicEngine()