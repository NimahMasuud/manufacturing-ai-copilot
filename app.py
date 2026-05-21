import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.rag_pipeline import rag_query

st.set_page_config(
    page_title="Manufacturing Co-pilot",
    page_icon="🏭",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    sensor = pd.read_csv("data/sensor_logs.csv")
    downtime = pd.read_csv("data/downtime_events.csv")
    quality = pd.read_csv("data/quality_inspections.csv")
    maintenance = pd.read_csv("data/maintenance_records.csv")
    production = pd.read_csv("data/production_summary.csv")
    return sensor, downtime, quality, maintenance, production

sensor, downtime, quality, maintenance, production = load_data()

# Tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "🤖 AI Co-pilot"])

# ─────────────────────────────────────────────
# TAB 1 — DASHBOARD
# ─────────────────────────────────────────────
with tab1:
    st.title("🏭 Manufacturing Operations Dashboard")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Downtime Events", len(downtime))
    with col2:
        total_downtime_mins = downtime["duration_minutes"].sum()
        st.metric("Total Downtime (mins)", f"{total_downtime_mins:,.0f}")
    with col3:
        avg_efficiency = production["efficiency_pct"].mean()
        st.metric("Avg Efficiency", f"{avg_efficiency:.1f}%")
    with col4:
        total_defects = quality["units_failed"].sum() if "units_failed" in quality.columns else (quality["units_inspected"].sum() - quality["units_passed"].sum())
        st.metric("Total Defect Units", f"{total_defects:,.0f}")

    st.divider()

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⏱ Downtime by Machine")
        dt_by_machine = downtime.groupby("machine_id")["duration_minutes"].sum().reset_index()
        dt_by_machine = dt_by_machine.sort_values("duration_minutes", ascending=False)
        fig = px.bar(dt_by_machine, x="machine_id", y="duration_minutes",
                     color="duration_minutes", color_continuous_scale="Reds",
                     labels={"duration_minutes": "Total Downtime (mins)", "machine_id": "Machine"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🔍 Downtime Causes Breakdown")
        dt_cause = downtime["cause"].value_counts().reset_index()
        dt_cause.columns = ["cause", "count"]
        fig2 = px.pie(dt_cause, names="cause", values="count", hole=0.4,
                      color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🌡 Temperature Trends by Machine")
        fig3 = px.line(sensor.sort_values("timestamp"), x="timestamp", y="temperature_C",
                       color="machine_id",
                       labels={"temperature_C": "Temperature (°C)", "timestamp": "Time"})
        fig3.update_xaxes(showticklabels=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("✅ Quality Pass Rate by Machine")
        quality["pass_rate"] = quality["units_passed"] / quality["units_inspected"] * 100
        pass_rate = quality.groupby("machine_id")["pass_rate"].mean().reset_index()
        fig4 = px.bar(pass_rate, x="machine_id", y="pass_rate",
                      color="pass_rate", color_continuous_scale="Greens",
                      labels={"pass_rate": "Pass Rate (%)", "machine_id": "Machine"})
        fig4.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Target 80%")
        st.plotly_chart(fig4, use_container_width=True)

    # Row 3
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("⚙️ Production Efficiency by Line")
        eff_by_line = production.groupby("production_line")["efficiency_pct"].mean().reset_index()
        fig5 = px.bar(eff_by_line, x="production_line", y="efficiency_pct",
                      color="efficiency_pct", color_continuous_scale="Blues",
                      labels={"efficiency_pct": "Avg Efficiency (%)", "production_line": "Line"})
        fig5.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Target 80%")
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.subheader("🔧 Maintenance Cost by Machine")
        maint_cost = maintenance.groupby("machine_id")["cost_usd"].sum().reset_index()
        maint_cost = maint_cost.sort_values("cost_usd", ascending=False)
        fig6 = px.bar(maint_cost, x="machine_id", y="cost_usd",
                      color="cost_usd", color_continuous_scale="Oranges",
                      labels={"cost_usd": "Total Cost (USD)", "machine_id": "Machine"})
        st.plotly_chart(fig6, use_container_width=True)

    # Row 4 — full width
    st.subheader("📦 Scrap Units Over Time")
    production_sorted = production.sort_values("date") if "date" in production.columns else production
    fig7 = px.area(production_sorted, x=production_sorted.index, y="scrap_units",
                   color="production_line",
                   labels={"scrap_units": "Scrap Units", "index": "Record"})
    st.plotly_chart(fig7, use_container_width=True)


# ─────────────────────────────────────────────
# TAB 2 — AI CO-PILOT CHAT
# ─────────────────────────────────────────────
with tab2:
    st.title("🤖 Manufacturing Operations Co-pilot")
    st.caption("Ask questions about machine performance, downtime, quality, and maintenance")

    with st.sidebar:
        st.header("💡 Try these questions")
        examples = [
            "Which machine has the most downtime events?",
            "What are the top causes of quality defects?",
            "Show me temperature anomalies for MACH-001",
            "What maintenance actions reduced vibration spikes?",
            "Which production line has the lowest efficiency?"
        ]
        for q in examples:
            if st.button(q, use_container_width=True):
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": q})

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about your production data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Searching production data..."):
                answer = rag_query(prompt)
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})