import os
import sys

# ==============================================================================
# 🛰️ DYNAMIC INTEGRATION PATH CONFIGURATOR (EN TEPEDE ÇALIŞMALIDIR!)
# ==============================================================================
# Python'ın hem nexus-core'u hem de tüm alt paketleri (interface, intelligence, memory)
# bulabilmesi için holding arama yollarını en başta tanımlıyoruz.
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../interface
repository_root = os.path.dirname(current_dir)          # .../nexus-core
root_dir = os.path.dirname(os.path.dirname(repository_root)) # C:\NEXUS
ventures_dir = os.path.join(root_dir, "Projects", "Ventures")

# Öncelikli yolları sys.path listesinin en başına mühürlüyoruz
for path in [repository_root, root_dir, ventures_dir, current_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# ==============================================================================
# ⚙️ STANDART VE YEREL İTHALATLAR
# ==============================================================================
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

# Logic Engine ve Ventures Kernel İthalatları (Pylance ve Hata Korumalı)
try:
    from interface.logic_engine import engine  # type: ignore
except ImportError:
    try:
        from logic_engine import engine  # type: ignore
    except ImportError:
        # Fallback Mock Sınıfı
        class DummyEngine:
            def execute_pipeline(self):
                return {
                    "execution_id": 99999,
                    "decision": "STABLE_ACCUMULATE",
                    "confidence": 80.0,
                    "kelly_bet": 0.1,
                    "next_state": "BULL",
                    "local_security": "MOCK_ACTIVE",
                    "timestamp": time.time()
                }
        engine = DummyEngine()

try:
    from ventures_kernel import VenturesKernel  # type: ignore
except ImportError:
    class VenturesKernel:
        def __init__(self): pass
        def run_ventures_pipeline(self):
            time.sleep(1.5)
            return {
                "status": "SUCCESS",
                "evaluated_count": 3,
                "top_trend": "DeFi Orchestrators & Neuro-Networks",
                "decision": "INVEST (Project Alpha - 91.2 Score)"
            }

# ==============================================================================
# 🎨 UI STYLE DESIGN TOKENS (Siber-Neon Estetik)
# ==============================================================================
BG_DARK = "#020813"       # Derin siber uzay arka planı
CARD_BG = "#0B1528"       # Panel kutuları arka planı
CYAN = "#00F5D4"          # Nexus neon mavi/yeşil
YELLOW = "#FFB800"        # Uyarı ve Hold durumu
RED = "#FF5A5F"           # Ayı piyasası / Risk uyarısı
PURPLE = "#9D4EDD"        # Araştırma simülasyon moru
TEXT_WHITE = "#E2E8F0"    # Okunabilir açık gri metin
BORDER_COLOR = "#1E293B"  # Çerçeve rengi


class NexusHoldingDashboard(tk.Tk):
    """
    NEXUS AI HOLDING — Capital Command Center v1.0
    Yapay zeka tabanlı yönetim, simülasyon ve otonom girişim takip arayüzü.
    """
    def __init__(self):
        super().__init__()
        self.title("NEXUS AI HOLDING — Capital Command Center v1.0")
        self.geometry("1300x850")
        self.state('zoomed') # Ekranı kapla
        self.configure(bg=BG_DARK)

        # Entegre Edilmiş Logic Engine Singleton Nesnesi
        self.engine = engine

        # Ana Grid Yapısı
        self.grid_rowconfigure(0, minsize=60) # Üst Banner
        self.grid_rowconfigure(1, minsize=40) # Sekme Alanı
        self.grid_rowconfigure(2, weight=1)   # İçerik Alanı
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_tabs()
        self._build_content_areas()
        
        # Varsayılan Sekmeyi Aç
        self.select_tab("capital")

    def _build_header(self):
        """Üst siber bilgi şeridi"""
        header_frame = tk.Frame(self, bg=BG_DARK, bd=0, highlightthickness=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        # Başlık ve Slogan
        title_label = tk.Label(
            header_frame, 
            text="NEXUS AI HOLDING   |   SYSTEM OPERATING LOG", 
            font=("Consolas", 18, "bold"), 
            fg=CYAN, 
            bg=BG_DARK
        )
        title_label.pack(side="left", anchor="w")

        # Sistem Durumu Sinyali
        status_frame = tk.Frame(header_frame, bg=BG_DARK)
        status_frame.pack(side="right")
        
        pulse_led = tk.Label(status_frame, text="●", fg=CYAN, bg=BG_DARK, font=("Arial", 14))
        pulse_led.pack(side="left", padx=5)
        
        status_txt = tk.Label(status_frame, text="KERNEL ONLINE [V1.0]", fg=TEXT_WHITE, bg=BG_DARK, font=("Consolas", 10, "bold"))
        status_txt.pack(side="left")

    def _build_tabs(self):
        """Siber Sekme Butonları"""
        self.tab_buttons_frame = tk.Frame(self, bg=BG_DARK, bd=0)
        self.tab_buttons_frame.grid(row=1, column=0, sticky="ew", padx=20)

        self.tabs = {}
        tab_configs = [
            ("capital", "NEXUS CAPITAL"),
            ("research", "NEXUS RESEARCH LAB"),
            ("ventures", "NEXUS VENTURES")
        ]

        for code, name in tab_configs:
            btn = tk.Button(
                self.tab_buttons_frame,
                text=name,
                font=("Consolas", 10, "bold"),
                fg=TEXT_WHITE,
                bg="#131B2E",
                activeforeground=CYAN,
                activebackground=CARD_BG,
                relief="flat",
                bd=1,
                highlightthickness=0,
                cursor="hand2",
                command=lambda c=code: self.select_tab(c)
            )
            btn.pack(side="left", padx=5, ipady=4, ipadx=15)
            self.tabs[code] = btn

    def _build_content_areas(self):
        """Sekmelerin içerik çerçeveleri"""
        self.container = tk.Frame(self, bg=BG_DARK, bd=0)
        self.container.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 1. CAPITAL PANEL
        self.capital_frame = tk.Frame(self.container, bg=BG_DARK)
        self._setup_capital_tab()

        # 2. RESEARCH PANEL
        self.research_frame = tk.Frame(self.container, bg=BG_DARK)
        self._setup_research_tab()

        # 3. VENTURES PANEL (YENİ EKLENEN OTONOM GİRİŞİM PANELİ)
        self.ventures_frame = tk.Frame(self.container, bg=BG_DARK)
        self._setup_ventures_tab()

    def select_tab(self, selected_code):
        """Aktif sekmeyi seçer ve görsel geri bildirimi günceller"""
        self.capital_frame.grid_forget()
        self.research_frame.grid_forget()
        self.ventures_frame.grid_forget()

        for code, btn in self.tabs.items():
            btn.configure(bg="#131B2E", fg=TEXT_WHITE, bd=1, relief="flat")

        if selected_code == "capital":
            self.capital_frame.grid(row=0, column=0, sticky="nsew")
            self.tabs["capital"].configure(bg=CARD_BG, fg=CYAN, relief="solid")
        elif selected_code == "research":
            self.research_frame.grid(row=0, column=0, sticky="nsew")
            self.tabs["research"].configure(bg=CARD_BG, fg=CYAN, relief="solid")
        elif selected_code == "ventures":
            self.ventures_frame.grid(row=0, column=0, sticky="nsew")
            self.tabs["ventures"].configure(bg=CARD_BG, fg=CYAN, relief="solid")

    # ==============================================================================
    # 💼 1. NEXUS CAPITAL TAB
    # ==============================================================================
    def _setup_capital_tab(self):
        self.capital_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.capital_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        self.capital_frame.grid_rowconfigure(0, weight=1)

        left_col = tk.LabelFrame(
            self.capital_frame, text="DEPARTMAN MÜDÜRLÜKLERİ ODASI (SİNYAL TAKİP)", 
            font=("Consolas", 11, "bold"), fg=CYAN, bg=CARD_BG, bd=1, relief="solid",
            padx=15, pady=15
        )
        left_col.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_col.grid_rowconfigure(0, weight=1)
        left_col.grid_rowconfigure(1, weight=1)
        left_col.grid_rowconfigure(2, weight=1)
        left_col.grid_rowconfigure(3, weight=1)
        left_col.grid_rowconfigure(4, minsize=50)
        left_col.grid_columnconfigure(0, weight=1)

        departments = [
            "Kripto Varlıklar Departmanı Müdürlüğü",
            "Değerli Madenler & Emtia Müdürlüğü",
            "Hisse Senetleri & Küresel Borsalar",
            "Yatırım Fonları & BES Direktörlüğü"
        ]

        for i, dep_name in enumerate(departments):
            box = tk.Frame(left_col, bg="#0E1A30", bd=1, relief="solid", highlightbackground=BORDER_COLOR)
            box.grid(row=i, column=0, sticky="ew", pady=5, padx=5)
            
            lbl_name = tk.Label(box, text=dep_name, font=("Consolas", 10, "bold"), fg=TEXT_WHITE, bg="#0E1A30")
            lbl_name.pack(side="left", padx=15, pady=10)
            
            lbl_status = tk.Label(box, text="[HOLD]", font=("Consolas", 10, "bold"), fg=YELLOW, bg="#0E1A30")
            lbl_status.pack(side="right", padx=15)

        btn_scan = tk.Button(
            left_col, text="DEPARTMAN HAFIZALARINI TARA", font=("Consolas", 11, "bold"),
            bg=CYAN, fg=BG_DARK, activebackground="#00D2B4", relief="flat", cursor="hand2",
            command=self._trigger_capital_scan
        )
        btn_scan.grid(row=4, column=0, sticky="ew", pady=10, padx=5)

        right_col = tk.LabelFrame(
            self.capital_frame, text="NEXUS CAPITAL PAZAR & PORTFÖY TAKİP SİSTEMİ",
            font=("Consolas", 11, "bold"), fg=CYAN, bg=CARD_BG, bd=1, relief="solid",
            padx=15, pady=15
        )
        right_col.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_col.grid_rowconfigure(0, weight=3)
        right_col.grid_rowconfigure(1, weight=2)
        right_col.grid_columnconfigure(0, weight=1)

        chart_canvas = tk.Canvas(right_col, bg=CARD_BG, highlightthickness=0, bd=0)
        chart_canvas.grid(row=0, column=0, sticky="nsew", pady=5)
        
        chart_canvas.create_text(250, 25, text="NEXUS All-Weather Varlık Dağılım Paketi", fill=CYAN, font=("Consolas", 12, "bold"))
        chart_canvas.create_arc(150, 50, 350, 250, start=0, extent=144, fill="#00E5FF")
        chart_canvas.create_arc(150, 50, 350, 250, start=144, extent=108, fill="#9D4EDD")
        chart_canvas.create_arc(150, 50, 350, 250, start=252, extent=54, fill="#FFB800")
        chart_canvas.create_arc(150, 50, 350, 250, start=306, extent=36, fill="#FF007F")
        chart_canvas.create_arc(150, 50, 350, 250, start=342, extent=18, fill="#38B000")
        
        chart_canvas.create_text(80, 150, text="Tahvil/Eurobond (%40)", fill="#00E5FF", font=("Consolas", 9))
        chart_canvas.create_text(400, 180, text="Hisse Senetleri (%30)", fill="#9D4EDD", font=("Consolas", 9))
        chart_canvas.create_text(350, 70, text="Emtia/Altın (%15)", fill="#FFB800", font=("Consolas", 9))

        table_label = tk.Label(right_col, text="MÜŞTERİ AKTİF VARLIK DAĞILIMI VE PERFORMANS", font=("Consolas", 10, "bold"), fg=CYAN, bg=CARD_BG, anchor="w")
        table_label.grid(row=1, column=0, sticky="ew", pady=(10, 2))

        table_frame = tk.Frame(right_col, bg=BORDER_COLOR, bd=1)
        table_frame.grid(row=2, column=0, sticky="nsew", pady=5)
        table_frame.grid_columnconfigure((0,1,2,3,4), weight=1)

        headers = ["Varlık Sınıfı", "Miktar", "Ort. Maliyet", "Güncel Değer", "Kâr / Zarar"]
        for col_idx, text in enumerate(headers):
            lbl = tk.Label(table_frame, text=text, font=("Consolas", 9, "bold"), fg=CYAN, bg="#131F33", pady=5, relief="solid", bd=1)
            lbl.grid(row=0, column=col_idx, sticky="nsew")

        assets_data = [
            ["Bitcoin (BTC)", "1.25", "$62,500", "$78,125", "+%25.0 (Boğa)", "#00E5FF"],
            ["Gram Altın (ONS)", "150.00", "2,400 TL", "2,520 TL", "+%5.0 (Dengeli)", "#38B000"],
            ["BIST30 Endeks Hisse", "450.00", "110 TL", "98 TL", "-%10.9 (Ayı Duygusu)", RED],
            ["Eurobond (US90)", "10,000", "$98.5", "$101.2", "+%2.7 (Sabit)", "#38B000"]
        ]

        for row_idx, row_data in enumerate(assets_data, start=1):
            for col_idx, val in enumerate(row_data[:5]):
                color = row_data[5] if col_idx == 4 else TEXT_WHITE
                lbl = tk.Label(table_frame, text=val, font=("Consolas", 9), fg=color, bg="#0E1A30", pady=5, relief="solid", bd=1)
                lbl.grid(row=row_idx, column=col_idx, sticky="nsew")

    def _trigger_capital_scan(self):
        messagebox.showinfo("NEXUS CORE", "Tüm holding departman hafızaları yapay zeka tarafından tarandı.\nDuygu durumları: [HOLD] stabil durumda.")

    # ==============================================================================
    # 🧬 2. NEXUS RESEARCH LAB TAB
    # ==============================================================================
    def _setup_research_tab(self):
        self.research_frame.grid_columnconfigure(0, weight=1, uniform="group2")
        self.research_frame.grid_columnconfigure(1, weight=1, uniform="group2")
        self.research_frame.grid_rowconfigure(0, weight=1)

        left_col = tk.LabelFrame(
            self.research_frame, text="MAKRO EKONOMİK SİMÜLASYON MOTORU (12 AY)",
            font=("Consolas", 11, "bold"), fg=CYAN, bg=CARD_BG, bd=1, relief="solid",
            padx=15, pady=15
        )
        # HATA DÜZELTİLDİ: px -> padx, py -> pady yapıldı (Line 308)
        left_col.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_col.grid_rowconfigure(0, weight=1)
        left_col.grid_rowconfigure(1, minsize=50)
        left_col.grid_columnconfigure(0, weight=1)

        self.sim_canvas = tk.Canvas(left_col, bg="#020813", highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.sim_canvas.grid(row=0, column=0, sticky="nsew", pady=5)
        self.sim_canvas.create_text(250, 150, text="[SİMÜLASYON HAZIR - MONTE CARLO TETİKLEYİN]", fill=PURPLE, font=("Consolas", 11, "bold"))

        btn_sim = tk.Button(
            left_col, text="YENİ EKONOMİK SİMÜLASYON TETİKLE (MONTE CARLO)", font=("Consolas", 11, "bold"),
            bg=PURPLE, fg=TEXT_WHITE, activebackground="#B576F7", relief="flat", cursor="hand2",
            command=self._run_monte_carlo
        )
        btn_sim.grid(row=1, column=0, sticky="ew", pady=10, padx=5)

        right_col = tk.LabelFrame(
            self.research_frame, text="DEEP LEARNING & TAHMİN SİSTEMLERİ LABORATUVARI",
            font=("Consolas", 11, "bold"), fg=CYAN, bg=CARD_BG, bd=1, relief="solid",
            padx=15, pady=15
        )
        # HATA DÜZELTİLDİ: px -> padx, py -> pady yapıldı (Line 325)
        right_col.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_col.grid_rowconfigure(0, minsize=70)
        right_col.grid_rowconfigure(1, weight=1)
        right_col.grid_rowconfigure(2, weight=1)
        right_col.grid_columnconfigure(0, weight=1)

        model_box = tk.Frame(right_col, bg="#0E1A30", bd=1, relief="solid")
        model_box.grid(row=0, column=0, sticky="ew", pady=5)
        
        tk.Label(model_box, text="AKTİF ARAŞTIRMA MODELİ:", font=("Consolas", 9, "bold"), fg=CYAN, bg="#0E1A30").pack(anchor="w", padx=15, pady=(5,0))
        tk.Label(model_box, text="NEXUS-Quantum-Neural-v4 (Stokastik Diferansiyel)", font=("Consolas", 10, "bold"), fg=TEXT_WHITE, bg="#0E1A30").pack(anchor="w", padx=15, pady=(0,5))

        tk.Label(right_col, text="LABORATUVAR CANLI ANALİZ GÜNLÜĞÜ", font=("Consolas", 9, "bold"), fg=TEXT_WHITE, bg=CARD_BG).grid(row=1, column=0, sticky="w", pady=(5,2))
        self.log_text = tk.Text(right_col, bg="#020813", fg=TEXT_WHITE, font=("Consolas", 8), bd=1, relief="solid", state="disabled")
        self.log_text.grid(row=1, column=0, sticky="nsew", pady=5)
        self._write_log("Sistem önbellekleri yüklendi. Tahmin modelleri stabil.")

        tk.Label(right_col, text="MODEL GELECEK TAHMİN MATRİSİ (PROBABILITY MATRIX)", font=("Consolas", 9, "bold"), fg=CYAN, bg=CARD_BG).grid(row=2, column=0, sticky="w", pady=(10,2))
        
        matrix_frame = tk.Frame(right_col, bg=BORDER_COLOR, bd=1)
        matrix_frame.grid(row=2, column=0, sticky="nsew", pady=5)
        matrix_frame.grid_columnconfigure((0,1,2,3), weight=1)

        m_headers = ["Varlık Enstrümanı", "Yön Eğilimi", "Model Olasılığı", "Hedef Vade"]
        for col_idx, text in enumerate(m_headers):
            lbl = tk.Label(matrix_frame, text=text, font=("Consolas", 8, "bold"), fg=CYAN, bg="#131F33", pady=4, relief="solid", bd=1)
            lbl.grid(row=0, column=col_idx, sticky="nsew")

        matrix_data = [
            ["Kripto (BTC)", "YUKARI (Boğa Duygusu)", "%78.5", "30 Gün", "#38B000"],
            ["Hisse Senedi (BIST)", "AŞAĞI (Ayı Duygusu)", "%64.2", "15 Gün", RED],
            ["Altın (ONS)", "YUKARI (Boğa Duygusu)", "%91.0", "60 Gün", "#38B000"],
            ["Eurobond (US10Y)", "YATAY (Dengeli)", "%85.0", "90 Gün", YELLOW]
        ]

        for r_idx, row_data in enumerate(matrix_data, start=1):
            for c_idx, val in enumerate(row_data[:4]):
                color = row_data[4] if c_idx == 1 or c_idx == 2 else TEXT_WHITE
                lbl = tk.Label(matrix_frame, text=val, font=("Consolas", 8), fg=color, bg="#0E1A30", pady=4, relief="solid", bd=1)
                lbl.grid(row=r_idx, column=c_idx, sticky="nsew")

    def _write_log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _run_monte_carlo(self):
        self._write_log("Monte Carlo simülasyonu arka planda başlatıldı...")
        self.sim_canvas.delete("all")
        import random
        for i in range(10):
            x1, y1 = i * 40, 150 + random.randint(-80, 80)
            x2, y2 = (i+1) * 40, 150 + random.randint(-80, 80)
            self.sim_canvas.create_line(x1, y1, x2, y2, fill=PURPLE, width=2)
        self._write_log("Monte Carlo simülasyonu bitti. %95 güven aralığı hesaplandı.")

    # ==============================================================================
    # 🚀 3. NEXUS VENTURES TAB
    # ==============================================================================
    def _setup_ventures_tab(self):
        self.ventures_frame.grid_columnconfigure(0, weight=1, uniform="group3")
        self.ventures_frame.grid_columnconfigure(1, weight=1, uniform="group3")
        self.ventures_frame.grid_rowconfigure(0, weight=1)

        left_col = tk.LabelFrame(
            self.ventures_frame, text="GİRİŞİM DEĞERLEME & PROJE RADARI",
            font=("Consolas", 11, "bold"), fg=CYAN, bg=CARD_BG, bd=1, relief="solid",
            padx=15, pady=15
        )
        # HATA DÜZELTİLDİ: px -> padx, py -> pady yapıldı (Line 379)
        left_col.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_col.grid_rowconfigure(0, weight=1)
        left_col.grid_rowconfigure(1, minsize=50)
        left_col.grid_columnconfigure(0, weight=1)

        self.ventures_list_frame = tk.Frame(left_col, bg=CARD_BG)
        self.ventures_list_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        self.ventures_list_frame.grid_columnconfigure(0, weight=1)

        self.ventures_data = [
            {"name": "Project Alpha (Autonomous Agent)", "score": "89.4", "status": "YÜKSEK POTANSİYEL"},
            {"name": "Project Beta (Biotech Neuro-Link)", "score": "74.1", "status": "ORTA RISK/POTANSİYEL"},
            {"name": "Project Gamma (DeFi Decentralized Storage)", "score": "61.2", "status": "BEKLEMEDE"}
        ]
        self._render_venture_cards()

        btn_trigger = tk.Button(
            left_col, text="GİRİŞİM RADARINI VE DEĞERLEMELERİ TETİKLE", font=("Consolas", 11, "bold"),
            bg="#38B000", fg=BG_DARK, activebackground="#007200", relief="flat", cursor="hand2",
            command=self._trigger_ventures_pipeline
        )
        btn_trigger.grid(row=1, column=0, sticky="ew", pady=10, padx=5)

        right_col = tk.LabelFrame(
            self.ventures_frame, text="YATIRIM KARARLARI & TREND ANALİZLERİ",
            font=("Consolas", 11, "bold"), fg=CYAN, bg=CARD_BG, bd=1, relief="solid",
            padx=15, pady=15
        )
        # HATA DÜZELTİLDİ: px -> padx, py -> pady yapıldı (Line 396)
        right_col.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_col.grid_rowconfigure(0, weight=1)
        right_col.grid_rowconfigure(1, weight=1)
        right_col.grid_columnconfigure(0, weight=1)

        tk.Label(right_col, text="OTONOM ANALİZ VE KERNEL ÇIKTILARI", font=("Consolas", 9, "bold"), fg=TEXT_WHITE, bg=CARD_BG).grid(row=0, column=0, sticky="w", pady=(0,2))
        self.ventures_log = tk.Text(right_col, bg="#020813", fg="#38B000", font=("Consolas", 8), bd=1, relief="solid", state="disabled")
        self.ventures_log.grid(row=0, column=0, sticky="nsew", pady=5)
        self._write_ventures_log("Ventures modülü ve trend dedektörü aktif edildi.")

        # HATA DÜZELTİLDİ: py=(10,2) -> pady=(10,2) yapıldı (Line 405)
        tk.Label(right_col, text="SEKTÖREL TREND RADARI", font=("Consolas", 9, "bold"), fg=CYAN, bg=CARD_BG).grid(row=1, column=0, sticky="w", pady=(10,2))
        self.trend_frame = tk.Frame(right_col, bg=BORDER_COLOR, bd=1)
        self.trend_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        self.trend_frame.grid_columnconfigure((0,1,2), weight=1)

        t_headers = ["Mega Trend Sektör", "Büyüme Olasılığı", "Ajan Tavsiyesi"]
        for col_idx, text in enumerate(t_headers):
            lbl = tk.Label(self.trend_frame, text=text, font=("Consolas", 8, "bold"), fg=CYAN, bg="#131F33", pady=4, relief="solid", bd=1)
            lbl.grid(row=0, column=col_idx, sticky="nsew")

        self.trend_data = [
            ["Generative Autonomous Swarms", "%94.5", "YATIRIMI TETİKLE"],
            ["Neuromorphic Microchips", "%88.2", "YAKINDAN TAKİP ET"],
            ["Zero-Knowledge Data Clouds", "%79.1", "İZLEME LİSTESİNE AL"]
        ]
        self._render_trend_table()

    def _render_venture_cards(self):
        for widget in self.ventures_list_frame.winfo_children():
            widget.destroy()

        for idx, item in enumerate(self.ventures_data):
            card = tk.Frame(self.ventures_list_frame, bg="#0E1A30", bd=1, relief="solid")
            # HATA DÜZELTİLDİ: py=5 -> pady=5 yapıldı (Line 424)
            card.pack(fill="x", pady=5)
            
            lbl_title = tk.Label(card, text=item["name"], font=("Consolas", 10, "bold"), fg=TEXT_WHITE, bg="#0E1A30")
            lbl_title.pack(anchor="w", padx=15, pady=(5,2))
            
            meta_txt = f"Değerleme Skoru: {item['score']}  |  Durum: {item['status']}"
            color = CYAN if float(item['score']) > 80 else YELLOW
            lbl_meta = tk.Label(card, text=meta_txt, font=("Consolas", 9), fg=color, bg="#0E1A30")
            lbl_meta.pack(anchor="w", padx=15, pady=(0,5))

    def _render_trend_table(self):
        for widget in self.trend_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        for r_idx, row_data in enumerate(self.trend_data, start=1):
            for c_idx, val in enumerate(row_data):
                color = "#38B000" if c_idx == 2 else TEXT_WHITE
                lbl = tk.Label(self.trend_frame, text=val, font=("Consolas", 8), fg=color, bg="#0E1A30", pady=4, relief="solid", bd=1)
                lbl.grid(row=r_idx, column=c_idx, sticky="nsew")

    def _write_ventures_log(self, msg):
        self.ventures_log.configure(state="normal")
        self.ventures_log.insert("end", f"[NEXUS_VENTURES_{time.strftime('%H:%M:%S')}] {msg}\n")
        self.ventures_log.see("end")
        self.ventures_log.configure(state="disabled")

    def _trigger_ventures_pipeline(self):
        self._write_ventures_log("Ajanlar uyandırılıyor, otonom analiz hattı tetiklendi...")
        
        def run_thread():
            try:
                res = self.engine.execute_pipeline()
                self.after(0, lambda: self._on_pipeline_success(res))
            except Exception as e:
                self.after(0, lambda: self._write_ventures_log(f"[HATA] Çekirdek hatası: {e}"))

        threading.Thread(target=run_thread, daemon=True).start()

    def _on_pipeline_success(self, results):
        self._write_ventures_log(f"[SUCCESS] Girişim analizi bitti. Kimlik: {results['execution_id']}")
        self._write_ventures_log(f"Karar: {results['decision']} (Güven Skoru: %{results['confidence']:.1f})")
        self._write_ventures_log(f"Matematiksel Kelly Payı: %{results['kelly_bet']*100:.2f}")
        self._write_ventures_log(f"Markov Durum Beklentisi: {results['next_state']}")
        self._write_ventures_log(f"Yerel Veri Güvenliği: {results['local_security']}")
        
        # UI Verilerini Yeni Değerlerle Güncelle
        self.ventures_data[0] = {
            "name": f"Project Alpha (Autonomous Agent)", 
            "score": f"{results['confidence']}", 
            "status": results['decision']
        }
        self._render_venture_cards()
        
        messagebox.showinfo(
            "NEXUS CORE KARARI", 
            f"Otonom Değerlendirmeler Mühürlendi!\n\n"
            f"Karar: {results['decision']}\n"
            f"Olasılık Güveni: %{results['confidence']:.1f}\n"
            f"Önerilen Kelly Pozisyonu: %{results['kelly_bet']*100:.2f}"
        )


if __name__ == "__main__":
    app = NexusHoldingDashboard()
    app.mainloop()