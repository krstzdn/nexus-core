"""
NEXUS Operating System - Intelligence Control Panel
Gathers telemetry, agent weights, and backtesting validation under a unified UI.
"""
import streamlit as st
import sqlite3
from pathlib import Path
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

# Projenin kök dizinini (nexus-core) Python arama yollarına (sys.path) zorla mühürlüyoruz
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
# Diğer mevcut importlarınız bu satırdan sonra güvenle devam edebilir...

# Sayfa Genişlik Ayarları
st.set_page_config(page_title="NEXUS Intelligence Dashboard", layout="wide")

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "nexus_tfa.db"

def get_db_data(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn, params=params)

# --- SIDEBAR OPERASYONLARI ---
with st.sidebar:
    st.title("🧠 System Operations")
    st.markdown("Execute or synchronize the underlying NEXUS AI Core.")
    
    # Hedef varlık seçimi ekliyoruz
    target_asset = st.selectbox("🎯 Target Asset for Council", ["KCHOL", "THYAO", "BTC"])
    
    if st.button("🚀 Run AI Council (Kernel)", use_container_width=True):
        from core.kernel import AIKernel  # .py takısı tamamen kaldırıldı
        
        kernel = AIKernel()
        
        kernel = AIKernel()
        with st.spinner("Council is debating..."):
            session_result = kernel.execute_council_session(target_asset)
            
        if session_result:
            st.success(f" Oylama Tamamlandı!")
            st.metric("Final Decision", session_result["final_decision"])
            st.metric("Consensus Strength", f"{session_result['consensus_score']:.2f}")
            st.toast(f"{target_asset} için karara varıldı!", icon="🏛️")

# --- ANA PANEL ---
st.title("🌌 NEXUS Intelligence Dashboard")
st.markdown("---")

# Üst Metrik Kartları (Canlı Portföy Durumu)
col1, col2, col3 = st.columns(3)
col1.metric("TRY Cash", "49,787.14", "+1.2%")
col2.metric("KCHOL Holdings", "90.96 Units", "-0.4%")
col3.metric("THYAO Holdings", "76.41 Units", "+3.5%")

st.markdown("---")

# Orta Panel: Grafik ve Loglar
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🧠 Evolutionary Agent Weights")
    try:
        df_weights = get_db_data("SELECT agent_name, weight, success_rate, total_forecasts FROM agent_weights")
        if not df_weights.empty:
            st.dataframe(df_weights, use_container_width=True, hide_index=True)
            fig = px.bar(df_weights, x="agent_name", y="weight", color="agent_name")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No agent weights found in database.")
    except Exception as e:
        st.error(f"Weights Error: {e}")

with right_col:
    st.subheader("📜 Historical Forecast Logs")
    try:
        df_logs = get_db_data("SELECT id, agent_name, target_asset, score, direction FROM forecasts ORDER BY id DESC LIMIT 10")
        if not df_logs.empty:
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
        else:
            st.warning("No historical forecasts found.")
    except Exception as e:
        st.error(f"Logs Error: {e}")

# --- EN ALT PANEL: GEÇMİŞE DÖNÜK TEST SANDBOX'I ---
st.markdown("---")
st.header("📈 Historical Backtesting Sandbox")

if st.button("📊 Run Historical Strategy Analysis", use_container_width=True):
    import sys
    
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
        
    from core.backtest_engine import BacktestEngine
    
    engine = BacktestEngine()
    # 365 Günlük derin veri tabanı simülasyonunu KCHOL için tetikler
    results = engine.run_db_test("KCHOL")
    
    if results:
        b_col1, b_col2, b_col3 = st.columns(3)
        b_col1.metric("Final Capital (1 Year)", f"{results['final_capital']:,.2f} TRY")
        b_col2.metric("1-Year Depth ROI", f"%{results['total_roi_pct']:.2f}")
        b_col3.metric("Win Rate", f"%{results['win_rate_pct']:.2f}")
    else:
        st.error("Please run the seeder script first: python -m scripts.seed_historical_data")