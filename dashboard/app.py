import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import plotly.express as px
import streamlit as st

from controller.controller import SDNController
from experiments.run_all_experiments import run_all
from monitoring.metrics_collector import collect_metrics
from traffic_generator import generate_workload

st.set_page_config(page_title="ROBO-SDN | QoS Control", page_icon="◈", layout="wide")
st.markdown(
    """
    <style>
    :root { color-scheme: light; }
    html, body, [data-testid="stAppViewContainer"] {
        background: #f3f6fb;
        color: #172b4d;
        font-family: Aptos, "Segoe UI Variable", "Segoe UI", Inter, sans-serif !important;
    }
    [data-testid="stAppViewContainer"] *:not(code):not(pre):not(svg):not(path) {
        font-family: Aptos, "Segoe UI Variable", "Segoe UI", Inter, sans-serif !important;
    }
    [data-testid="stHeader"] { background: rgba(243,246,251,.96); }
    [data-testid="stMain"] .block-container { padding: 2rem 2.5rem 3rem; max-width: 1500px; }
    section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background: #fff; border-right: 1px solid #dbe4ef;
    }
    section[data-testid="stSidebar"] * { color: #233852; }
    h1, h2, h3 { color: #142b48 !important; letter-spacing: -.025em; }
    p, label, [data-testid="stCaptionContainer"] { color: #53657c; }
    [data-testid="stMetric"] {
        background: #fff; border: 1px solid #dce5ef; border-radius: 14px;
        padding: 18px 20px; box-shadow: 0 4px 14px rgba(20,43,72,.055);
    }
    [data-testid="stMetricLabel"] { color: #53657c !important; }
    [data-testid="stMetricValue"] { color: #142b48 !important; font-weight: 700; }
    .stButton > button, section[data-testid="stSidebar"] button,
    button[kind="primary"], button[kind="secondary"] {
        background: #087e8b !important; background-color: #087e8b !important;
        color: #fff !important; -webkit-text-fill-color: #fff !important;
        border: 1px solid #087e8b !important; border-radius: 10px !important;
        font-weight: 650 !important; min-height: 44px; opacity: 1 !important;
        box-shadow: 0 3px 9px rgba(8,126,139,.18);
    }
    button[kind$="FormSubmit"], button[data-testid="stFormSubmitButton"] {
        background: #087e8b !important; background-color: #087e8b !important;
        color: #fff !important; -webkit-text-fill-color: #fff !important;
        border: 1px solid #087e8b !important; border-radius: 10px !important;
        font-weight: 650 !important; min-height: 44px; opacity: 1 !important;
        box-shadow: 0 3px 9px rgba(8,126,139,.18);
    }
    .stButton > button *, section[data-testid="stSidebar"] button * {
        color: #fff !important; -webkit-text-fill-color: #fff !important; opacity: 1 !important;
    }
    button[kind$="FormSubmit"] *, button[data-testid="stFormSubmitButton"] * {
        color: #fff !important; -webkit-text-fill-color: #fff !important; opacity: 1 !important;
    }
    .stButton > button:hover, section[data-testid="stSidebar"] button:hover {
        background: #066873 !important; background-color: #066873 !important;
        border-color: #066873 !important; transform: translateY(-1px);
    }
    button[kind$="FormSubmit"]:hover, button[data-testid="stFormSubmitButton"]:hover {
        background: #066873 !important; background-color: #066873 !important; border-color: #066873 !important;
    }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div {
        background: #fff; border-color: #cbd7e5;
    }
    [data-testid="stDataFrame"], [data-testid="stJson"] {
        background: #fff; border: 1px solid #dce5ef; border-radius: 12px;
    }
    [data-testid="stAlert"] { border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "ctl" not in st.session_state:
    st.session_state.ctl = SDNController()
    st.session_state.metrics = {}
    st.session_state.ran = False

ctl = st.session_state.ctl
st.sidebar.title("◈ ROBO-SDN")
page = st.sidebar.selectbox(
    "Navigation",
    ["Overview", "Custom Simulation", "Network Topology", "Traffic Classification",
     "QoS Management", "Congestion Management", "Performance Analytics", "Failover", "Event Logs"],
)
if st.sidebar.button("Run Demo Mode", type="primary", use_container_width=True):
    st.session_state.exp = run_all()
    st.session_state.demo_complete = True
    st.sidebar.success("Demo runs finished with fresh simulation measurements.")

st.title(page)

if page == "Overview":
    col1, col2, col3, col4 = st.columns(4)
    overall = st.session_state.metrics.get("overall", {})
    col1.metric("Controller", "ONLINE")
    col2.metric("Network", "ACTIVE" if st.session_state.ran else "INACTIVE")
    col3.metric("Throughput", f"{overall.get('throughput_mbps', 0):.3f} Mbps")
    col4.metric("Congestion", ctl.qos.state)
    st.caption("Windows software simulation; no physical OpenFlow switches are connected.")
    if st.button("Start normal traffic", type="primary"):
        ctl.simulator.run(generate_workload(3, 1), 3)
        st.session_state.metrics = collect_metrics(ctl.simulator)
        st.session_state.ran = True
        st.rerun()
    st.json(st.session_state.metrics or {"message": "Run traffic to populate measured counters."})

elif page == "Custom Simulation":
    st.write("Set the workload below. The output is calculated from packets generated and forwarded in this run.")
    with st.form("custom_workload"):
        duration = st.slider("Simulation duration (seconds)", 0.5, 10.0, 3.0, step=0.5)
        mode = st.radio("Forwarding mode", ["Proposed QoS", "Baseline"], horizontal=True)
        st.subheader("Traffic source settings")
        defaults = {"Control": (40, 96), "Telemetry": (80, 160), "Video": (500, 1200), "Bulk": (1200, 1400)}
        rates, sizes = {}, {}
        for traffic, (default_rate, default_size) in defaults.items():
            left, right = st.columns(2)
            rates[traffic.lower()] = left.number_input(
                f"{traffic}: packets per second", min_value=0, max_value=2500,
                value=default_rate, step=10, key=f"rate_{traffic}",
            )
            sizes[traffic.lower()] = right.number_input(
                f"{traffic}: packet size (bytes)", min_value=64, max_value=9000,
                value=default_size, step=64, key=f"size_{traffic}",
            )
        run_custom = st.form_submit_button("Run custom simulation", type="primary")

    if run_custom:
        from simulation.network_simulator import NetworkSimulator
        from traffic_generator.traffic_manager import generate_custom_workload

        with st.spinner("Generating packets and simulating the configured workload..."):
            custom_sim = NetworkSimulator(baseline=(mode == "Baseline"))
            packets = generate_custom_workload(duration, rates, sizes)
            custom_sim.run(packets, duration)
            st.session_state.custom_output = collect_metrics(custom_sim)
            st.session_state.custom_mode = mode
            st.session_state.custom_offered_mbps = sum(p.size_bytes * 8 for p in packets) / duration / 1_000_000

    result = st.session_state.get("custom_output")
    if result:
        st.success(
            f"Run complete · {st.session_state.custom_mode} · "
            f"offered load {st.session_state.custom_offered_mbps:.2f} Mbps"
        )
        cols = st.columns(4)
        for col, cls, label in zip(cols, "ABCD", ["Control", "Telemetry", "Video", "Bulk"]):
            col.metric(f"Class {cls} · {label}", f"{result[cls]['delivered']:,} delivered", f"{result[cls]['loss_pct']:.2f}% loss")
        table = pd.DataFrame([
            {"Class": cls, "Generated": result[cls]["generated"], "Delivered": result[cls]["delivered"],
             "Dropped": result[cls]["dropped"], "Latency (ms)": result[cls]["latency_ms"],
             "Jitter (ms)": result[cls]["jitter_ms"], "Throughput (Mbps)": result[cls]["throughput_mbps"]}
            for cls in "ABCD"
        ])
        st.dataframe(table, use_container_width=True, hide_index=True)
        st.plotly_chart(
            px.bar(table, x="Class", y="Throughput (Mbps)", color="Class",
                   title="Measured throughput by traffic class", template="plotly_white"),
            use_container_width=True,
        )
        st.download_button(
            "Download this run as CSV", table.to_csv(index=False).encode("utf-8"),
            "custom_simulation_results.csv", "text/csv",
        )
    else:
        st.info("Enter the traffic settings and run a simulation to generate output.")

elif page == "Network Topology":
    topology = ctl.topology.topology()
    st.write("Primary route: S1 → S2 → S3 · Backup route: S1 → S4 → S3")
    st.dataframe(pd.DataFrame(topology["links"]), use_container_width=True, hide_index=True)
    st.graphviz_chart("graph {rankdir=LR; R1--S1; R2--S1; R3--S1; C1--S1; Bulk--S1; S1--S2; S2--S3; S1--S4; S4--S3; S3--H1; S3--H2; S3--H3;}")

elif page == "Traffic Classification":
    classes = [
        {"Class": "A", "Traffic": "Critical Control", "DSCP": 46, "Queue": "Q0", "Priority": "Highest"},
        {"Class": "B", "Traffic": "Telemetry", "DSCP": 26, "Queue": "Q1", "Priority": "High"},
        {"Class": "C", "Traffic": "Video / Vision", "DSCP": 34, "Queue": "Q2", "Priority": "Medium"},
        {"Class": "D", "Traffic": "Best Effort / Bulk", "DSCP": 0, "Queue": "Q3", "Priority": "Low"},
    ]
    st.dataframe(pd.DataFrame(classes), use_container_width=True, hide_index=True)
    st.json(st.session_state.metrics)

elif page == "QoS Management":
    st.write("Active policies", ctl.qos.policies)
    queues = [{"Switch": name, "Queue": f"Q{i}", "Received": q.received, "Transmitted": q.transmitted,
               "Dropped": q.dropped, "Average length": q.average_length, "Average wait (s)": q.average_wait}
              for name, switch in ctl.simulator.switches.items() for i, q in enumerate(switch.queues)]
    st.dataframe(pd.DataFrame(queues), use_container_width=True, hide_index=True)

elif page == "Congestion Management":
    st.write(f"State: **{ctl.qos.state}** · congestion threshold 80% · recovery threshold 60%")
    left, right = st.columns(2)
    if left.button("Simulate congestion (95%)", type="primary"):
        ctl.detect_congestion(.95)
        st.rerun()
    if right.button("Clear congestion"):
        ctl.detect_congestion(.5)
        st.rerun()
    st.json(ctl.qos.policies)

elif page == "Performance Analytics":
    result_file = Path(__file__).resolve().parents[1] / "results" / "experiment_results.csv"
    if st.button("Run five experiments", type="primary"):
        st.session_state.exp = run_all()
        st.success("Experiments completed and saved.")
    data = st.session_state.get("exp", pd.read_csv(result_file) if result_file.exists() else pd.DataFrame())
    if not data.empty:
        st.dataframe(data, use_container_width=True, hide_index=True)
        st.plotly_chart(px.bar(data, x="scenario", y="A_latency_ms", color="mode", barmode="group",
                               title="Class A latency · baseline vs proposed", template="plotly_white"),
                        use_container_width=True)
    else:
        st.info("Run the experiments to generate measured analytics.")

elif page == "Failover":
    left, right = st.columns(2)
    if left.button("Fail primary S1–S2 link", type="primary"):
        st.write("Backup path:", ctl.routing.fail_primary())
        st.rerun()
    if right.button("Restore primary"):
        ctl.routing.restore_primary()
        st.rerun()
    st.write("Active path:", "Primary" if ctl.simulator.link("S1", "S2").available else "Backup")

else:
    st.dataframe(pd.DataFrame(ctl.logger.events + ctl.simulator.events), use_container_width=True, hide_index=True)
