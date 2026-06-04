import streamlit as st
import pandas as pd
import plotly.graph_objects as px
import time
from engine.matching_engine import MatchingEngine
from analytics.anomaly_engine import AnomalyEngine
from data.market_simulator import MarketSimulator

st.set_page_config(page_title="MicroEngine.io Console", layout="wide", initial_sidebar_state="collapsed")

# Inject Dark Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #e2e8f0; }
    div.stButton > button:first-child { background-color: #1e293b; color: white; border: 1px solid #334155; }
    .metric-card { background-color: #111827; border: 1px solid #1f2937; padding: 20px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ MicroEngine.io")
st.subheader("High-Throughput Limit Order Book & Microstructure Liquidity Monitor")

# Initialize persistent infrastructure state
if 'engine' not in st.session_state:
    st.session_state.engine = MatchingEngine()
    st.session_state.anomaly_engine = AnomalyEngine()
    st.session_state.simulator = MarketSimulator(base_price=280.0)
    st.session_state.anomaly_log = []

# Top Action Control Panel
col_ctrl1, col_ctrl2 = st.columns([1, 4])
with col_ctrl1:
    trigger_shock = st.button("🚨 Trigger Institutional Liquidity Shock")

# Generate fresh micro-burst data ticks
simulator = st.session_state.simulator
engine = st.session_state.engine
anomaly_engine = st.session_state.anomaly_engine

# Generate multiple context orders to form dynamic book depth
ticks = 15 if not trigger_shock else 1
for _ in range(ticks):
    order = simulator.generate_order_stream(systemic_shock=trigger_shock)
    engine.process_order(order)

# Fetch modern metrics state
bids, asks = engine.book.get_depth(levels=10)
anomaly_engine.log_snapshot(bids, asks)
anomaly_report = anomaly_engine.detect_liquidity_hole()

if anomaly_report["status"] != "NORMAL":
    st.session_state.anomaly_log.insert(0, f"[{anomaly_report['timestamp']}] Liquidity Hole Warning! Market depth cratered by {anomaly_report['drop_pct']}%")

# Main Dashboard Layout Grid
m1, m2, m3 = st.columns(3)
with m1:
    best_bid = engine.book.best_bid
    st.metric("Best Bid (Buy Anchor)", f"${best_bid}" if best_bid else "Empty", delta="Highest Buyer")
with m2:
    best_ask = engine.book.best_ask
    st.metric("Best Ask (Sell Anchor)", f"{best_ask}" if best_ask else "Empty", delta="- Lowest Seller", delta_color="inverse")
with m3:
    current_obi = anomaly_engine.history[-1]['obi'] if anomaly_engine.history else 0.0
    st.metric("Order Book Imbalance (OBI)", f"{round(current_obi, 3)}", delta="Buy Pressure Skew" if current_obi > 0 else "Sell Pressure Skew")

st.markdown("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.write("### 📊 Market Depth Structural Chart")
    
    df_bids = pd.DataFrame(bids) if bids else pd.DataFrame(columns=['Price', 'Volume'])
    df_asks = pd.DataFrame(asks) if asks else pd.DataFrame(columns=['Price', 'Volume'])
    
    fig = px.轟 = px.Area()
    fig = graph_objects = px.Area()
    
    # Custom plotting logic for structured asymmetric order books
    fig = px.area(title="Microstructure Depth Volume Map")
    if not df_bids.empty:
        fig.add_scatter(x=df_bids['Price'], y=df_bids['Volume'], fill='tozeroy', name='Bids (Demand)', line_color='#10b981')
    if not df_asks.empty:
        fig.add_scatter(x=df_asks['Price'], y=df_asks['Volume'], fill='tozeroy', name='Asks (Supply)', line_color='#ef4444')
    
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Asset Valuation ($)", yaxis_title="Liquidity Outstanding (Contracts)")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.write("### 🚨 Systemic Anomaly Ledger")
    if anomaly_report["status"] != "NORMAL":
        st.error(f"⚠️ **{anomaly_report['status']}**: Liquidity pool dropped by {anomaly_report['drop_pct']}%")
    else:
        st.success("🟢 System Health: Resilient Depth")
        
    st.text_area("Historical Network Warnings", value="\n".join(st.session_state.anomaly_log[:8]), height=200)

# Real-Time Execution Tape & Ledger Display
st.markdown("---")
col_t1, col_t2 = st.columns(2)
with col_t1:
    st.write("### 📑 Order Book Level Breakdown")
    col_b, col_a = st.columns(2)
    with col_b:
        st.write("**Top Bid Queue**")
        st.dataframe(df_bids, height=200, use_container_width=True)
    with col_a:
        st.write("**Top Ask Queue**")
        st.dataframe(df_asks, height=200, use_container_width=True)

with col_t2:
    st.write("### 🏁 Execution Tape (Last Matched Trades)")
    st.dataframe(pd.DataFrame(engine.trade_history[-10:]).sort_index(ascending=False), height=230, use_container_width=True)

# Auto-Refresh loop hook trigger
time.sleep(0.5)
st.rerun()
