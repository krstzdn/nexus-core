import flet as ft
import httpx
import asyncio
import sys
import os
from datetime import datetime

# 1. Kök dizini Python'a tanıtma satırları (Tamamen sol duvara yaslı / Sıfır girinti)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Üst dizinden gelen importlar (Tamamen sol duvara yaslı / Sıfır girinti)
from core.kernel import NexusCore
from data.database import init_db, get_recent_logs_from_db

async def main(page: ft.Page):
    # Bu satırdan itibaren altındaki tüm kodlar İÇERİDE (4 boşluk girintili) başlamalıdır!
    page.title = "NEXUS COGNITIVE TRADING TERMINAL"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.window_width = 1150
    page.window_height = 850

    # AI CEO (Kernel) nesnesi de main'in içinde olduğu için girintili olmalı
    ceo_kernel = NexusCore()

    state = {"current_symbol": "BTC"}
    # ... (Geri kalan Flet kodları aynı girinti seviyesiyle devam edecek)

    background = ft.Container(
        gradient=ft.LinearGradient(colors=["#000428", "#004e92"]),
        expand=True
    )

    def glass_card(content, width, height):
        return ft.Container(
            content=content, width=width, height=height, padding=15,
            bgcolor="#1AFFFFFF", border_radius=20,
        )

    price_title_text = ft.Text("BTC / USDT", size=24, color="white", weight="bold")
    live_price_text = ft.Text("Sinyal Aranıyor...", size=36, color="cyan", weight="bold")
    
    consensus_score_text = ft.Text("Konsensüs Skoru: --", size=20, color="cyan", weight="bold")
    decision_text = ft.Text("KARAR: ANALİZ EDİLİYOR", size=18, color="amber", weight="bold")
    agent_status_text = ft.Text("Ajanlar veri hatlarını optimize ediyor...", size=13, color="white70")
    sentiment_text = ft.Text("Piyasa Duygusu:\nNötr", size=16, color="white", weight="bold")
    db_status_text = ft.Text("Veritabanı: Hazır", size=12, color="green", italic=True)

    history_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Zaman", color="cyan", weight="bold")),
            ft.DataColumn(ft.Text("Fiyat", color="cyan", weight="bold")),
            ft.DataColumn(ft.Text("Konsensüs", color="cyan", weight="bold")),
            ft.DataColumn(ft.Text("Alınan Karar", color="cyan", weight="bold")),
        ],
        rows=[]
    )

    workspace_layout = ft.Column([
        ft.Row([
            glass_card(ft.Column([
                ft.Text("CANLI FIYAT GÖSTERGESI", color="cyan", weight="bold"),
                ft.Divider(color="white24"),
                price_title_text,
                ft.Container(height=10),
                live_price_text
            ], alignment=ft.MainAxisAlignment.START), 300, 220),
            
            glass_card(ft.Column([
                ft.Text("KONSEY OTONOM KARAR MOTORU", size=16, color="cyan", weight="bold"),
                ft.Divider(color="white24"),
                consensus_score_text, decision_text, agent_status_text,
                ft.Container(expand=True), db_status_text
            ], alignment=ft.MainAxisAlignment.START), 420, 220),
            
            glass_card(ft.Column([
                ft.Text("YAPAY ZEKA SENTİMENTİ", color="cyan", weight="bold"),
                ft.Divider(color="white24"),
                sentiment_text
            ]), 220, 220)
        ], alignment=ft.MainAxisAlignment.CENTER),
        
        ft.Container(height=10),
        
        glass_card(ft.Column([
            ft.Text("NEXUS AUDIT LOGS (SON 5 KARAR)", color="cyan", weight="bold", size=14),
            ft.Divider(color="white24"),
            ft.ListView([history_table], expand=True, spacing=5)
        ], scroll=ft.ScrollMode.AUTO), 970, 320)
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def refresh_ui_table(symbol):
        """Veritabanındaki son verileri çekip tabloyu yenileyen yardımcı fonksiyon"""
        history_table.rows.clear()
        db_rows = get_recent_logs_from_db(symbol)
        for row in db_rows:
            d_color = "green" if row[3] == "BUY" else ("red" if row[3] == "SELL" else "amber")
            history_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row[0].split(" ")[1] if " " in row[0] else row[0])),
                        ft.DataCell(ft.Text(f"${row[1]:,.2f}")),
                        ft.DataCell(ft.Text(f"%{row[2]}")),
                        ft.DataCell(ft.Text(row[3], color=d_color, weight="bold")),
                    ]
                )
            )

    def change_asset(e):
        chosen = e.control.content.value.split(" ")[0]
        state["current_symbol"] = chosen
        price_title_text.value = f"{chosen} / USDT"
        live_price_text.value = "Değiştiriliyor..."
        refresh_ui_table(chosen)
        page.update()

    btn_btc = ft.Button(content=ft.Text("BTC PANEL"), on_click=change_asset, bgcolor="#1AFFFFFF", color="white")
    btn_eth = ft.Button(content=ft.Text("ETH PANEL"), on_click=change_asset, bgcolor="#1AFFFFFF", color="white")
    btn_sol = ft.Button(content=ft.Text("SOL PANEL"), on_click=change_asset, bgcolor="#1AFFFFFF", color="white")

    tab_buttons = ft.Row([btn_btc, btn_eth, btn_sol], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    main_layout = ft.Column([
        ft.Text("NEXUS EXECUTIVE TERMINAL", size=28, weight="bold", color="cyan"),
        ft.Container(height=5),
        tab_buttons,
        ft.Container(height=15),
        workspace_layout
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(ft.Stack([background, main_layout], expand=True))

    async def update_data():
        async with httpx.AsyncClient() as client:
            while True:
                active_sym = state["current_symbol"]
                
                # --- YENİ ALTYAPI BİRLEŞMESİ ---
                # Arayüz artık kendi kafasına göre hesap yapmıyor.
                # Veriyi çekmesi ve analiz etmesi için AI CEO'yu (Kernel pipeline'ını) tetikliyor.
                pipeline_data = await ceo_kernel.run_pipeline(client, active_sym)
                
                if pipeline_data and state["current_symbol"] == active_sym:
                    # Canlı Fiyat Güncellemesi
                    live_price_text.value = f"${pipeline_data['live_price']:,.2f}"
                    
                    # Konsensüs Skoru Güncellemesi
                    c_score = pipeline_data["consensus_score"]
                    consensus_score_text.value = f"Konsensüs Skoru: %{c_score}"
                    
                    # Sentiment (ORACLE) Durumu Güncellemesi
                    sentiment_score = pipeline_data["oracle_report"].get("sentiment_score", 50)
                    if sentiment_score > 60:
                        sentiment_text.value = f"{active_sym} Duygusu:\nBOĞA (ALIM)"
                        sentiment_text.color = "green"
                    elif sentiment_score < 40:
                        sentiment_text.value = f"{active_sym} Duygusu:\nAYI (SATIŞ)"
                        sentiment_text.color = "red"
                    else:
                        sentiment_text.value = f"{active_sym} Duygusu:\nNÖTR"
                        sentiment_text.color = "white"

                    # Karar (SENTINEL & ATLAS) ve Dinamik Ajan Durum Metinleri
                    final_dec = pipeline_data["final_decision"]
                    if final_dec == "BUY":
                        decision_text.value = "KARAR: GÜÇLÜ AL (BUY)"
                        decision_text.color = "green"
                        agent_status_text.value = "VECTOR: Fiyat MA altında, anomalik destek onaylandı. PROPHET sinyali iletti."
                    elif final_dec == "SELL":
                        decision_text.value = "KARAR: SAT (SELL)"
                        decision_text.color = "red"
                        agent_status_text.value = "VECTOR: Fiyat MA üzerinde, direnç aşırı şişti. SENTINEL veto yetkisini hazırladı."
                    else:
                        decision_text.value = "KARAR: BEKLE (HOLD)"
                        decision_text.color = "amber"
                        agent_status_text.value = f"Ajanlar trend kırılımı bekliyor. Risk profili: {pipeline_data['portfolio_allocation'].get('risk_profile', 'Dengeli')}"

                    # Veritabanı durumu ve Audit log tablosunun yenilenmesi
                    db_status_text.value = "Veritabanı: Güncelleniyor..."
                    refresh_ui_table(active_sym)
                    db_status_text.value = f"Veritabanı: {active_sym} Senkronize ({datetime.now().strftime('%H:%M:%S')})"
                
                try:
                    page.update()
                except Exception:
                    break
                    
                await asyncio.sleep(2.0)

    page.run_task(update_data)

if __name__ == "__main__":
    init_db()
    ft.run(main)