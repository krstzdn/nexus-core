import flet as ft
import sqlite3
import hashlib
import threading
from core.kernel import AIKernel

class AuthManager:
    @staticmethod
    def verify_login(email, password):
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect("data/nexus_tfa.db")
        cursor = conn.cursor()
        cursor.execute("SELECT plan_type FROM users WHERE email=? AND password_hash=?", (email, pw_hash))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None

def main(page: ft.Page):
    page.title = "NEXUS AI - PRO TERMINAL"
    page.window_width = 450
    page.window_height = 800
    page.bgcolor = "#050505"
    page.theme_mode = ft.ThemeMode.DARK

    kernel = AIKernel()

    def build_terminal(plan):
        # Renkleri string olarak tanımlıyoruz (Hata almamak için)
        result = ft.Text("SİSTEM HAZIR", size=20, color="white")
        
        def run_council(e):
            btn.disabled = True
            page.update()
            def task():
                res = kernel.execute_council_session("BTC")
                result.value = f"KARAR: {res['final_decision']}\nGÜÇ: %{int(res['consensus_score']*100)}"
                btn.disabled = False
                page.update()
            threading.Thread(target=task).start()

        btn = ft.ElevatedButton("OTONOM KONSEYİ BAŞLAT", on_click=run_council)
        
        return ft.Column([
            ft.Text(f"NEXUS {plan} TERMİNALİ", color="cyan", size=24),
            result, btn
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def login_click(e):
        plan = AuthManager.verify_login(email_field.value, pass_field.value)
        if plan:
            page.clean()
            page.add(build_terminal(plan))
        else:
            page.show_snack_bar(ft.SnackBar(ft.Text("Hatalı giriş!")))

    email_field = ft.TextField(label="E-posta", border_color="cyan")
    pass_field = ft.TextField(label="Şifre", password=True, border_color="cyan")
    
    page.add(
        ft.Text("NEXUS GİRİŞ", size=28, color="cyan"),
        email_field, 
        pass_field,
        ft.ElevatedButton("GİRİŞ YAP", on_click=login_click)
    )

ft.app(target=main)