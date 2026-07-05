"""
NEXUS Operating System - Intelligence Control Dashboard
Live portfolio distribution, agent weights, and interactive kernel orchestrator.
"""
import streamlit as st
import json
import sqlite3
from pathlib import Path
import pandas as pd
import subprocess

# Sayfa Yapılandırması
st.set_page_config(page_title="NEXUS Intelligence Dashboard", page_icon="🔮", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "nexus_tfa.db"
PORTFOLIO_PATH = BASE_DIR / "memory" / "portfolio-agent.json"

st.title("🔮 NEXUS AI Operating System — Control Center")
st.subheader("Real-time Multi-Asset Portfolio & Evolutionary Agent Performance")
st.markdown("---")

# YAN PANEL: SİSTEM YÖNETİMİ (KERNEL CONTROLLER)
st.sidebar.header("🕹️ System Operations")
st.sidebar.markdown("Execute or synchronize the underlying NEXUS AI Core.")

if st.sidebar.button("🚀 Run AI Council (Kernel)", use_container_width=True):
    st.sidebar.info("Kernel execution requested...")
    try:
        # Arka planda kernel.py'ı tetikler ve çıktısını yakalar
        result = subprocess.run(["python", "-m", "core.kernel"], capture_output=True, text=True, check=True)
        st.sidebar.success("AI Council Session Executed Successfully!")
        # Çalışma logunu küçük bir alanda göster
        with st.sidebar.expander("See Execution Logs"):
            st.code(result.stdout[-1000:]) # Son 1000 karakteri bas
    except subprocess.CalledProcessError as e:
        st.sidebar.error(f"Kernel Error: {e}")
        with st.sidebar.expander("See Error Details"):
            st.code(e.stderr)

st.sidebar.markdown("---")
st.sidebar.caption("NEXUS OS v0.1.0 - Build: Genesis")

# 1. KATMAN: PORTFÖY DURUMU VE BAKİYELER
st.header("💼 Executive Portfolio Status")
if PORTFOLIO_PATH.exists():
    with open(PORTFOLIO_PATH, "r", encoding="utf-8") as f:
        portfolio = json.load(f)
    
    balances = portfolio.get("balances", {})
    cols = st.columns(len(balances))
    for idx, (asset, amount) in enumerate(balances.items()):
        with cols[idx]:
            if "TRY" in asset or "USDT" in asset:
                st.metric(label=f"{asset} Cash", value=f"{amount:,.2f}")
            else:
                st.metric(label=f"{asset} Holdings", value=f"{amount:,.2f} Units")
else:
    st.warning("Portfolio metrics not initialized yet. Run the kernel first.")

st.markdown("---")

# 2. KATMAN: EVRİMSEL AJAN AĞIRLIKLARI VE GEÇMİŞ TAHMİNLER
col_left, col_right = st.columns(2)

with col_left:
    st.header("🧠 Evolutionary Agent Weights")
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        df_weights = pd.read_sql_query("SELECT * FROM agent_weights", conn)
        conn.close()
        
        if not df_weights.empty:
            st.dataframe(df_weights, use_container_width=True)
            st.bar_chart(data=df_weights, x="agent_name", y="weight", color="#FF4B4B")
        else:
            st.info("No agent performance data recorded yet.")
    else:
        st.info("Database matrix pending creation.")

with col_right:
    st.header("📜 Historical Forecast Logs")
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        df_forecasts = pd.read_sql_query("SELECT id, agent_name, target_asset, score, direction, status, timestamp FROM forecasts ORDER BY id DESC LIMIT 10", conn)
        conn.close()
        
        if not df_forecasts.empty:
            st.dataframe(df_forecasts, use_container_width=True)
        else:
            st.info("No forecasts archived yet.")
    else:
        st.info("Database log stream offline.")