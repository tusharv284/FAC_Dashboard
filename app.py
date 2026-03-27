
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VelocityTech | Forensic Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .stApp { background: #070d16; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #0a1520 100%);
    border-right: 1px solid #1e3a5f;
  }
  [data-testid="stSidebar"] label { color: #8bb8d4 !important; font-size: 0.78rem !important; }
  [data-testid="stSidebar"] .stNumberInput input {
    background: #112233 !important; color: #e0f0ff !important;
    border: 1px solid #1e3a5f !important; border-radius: 6px !important;
  }

  /* Hide default header */
  #MainMenu, footer, header { visibility: hidden; }

  /* KPI Cards */
  .kpi-card {
    background: linear-gradient(135deg, #0d1b2a 0%, #112233 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 18px 16px 14px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
  }
  .kpi-card:hover { transform: translateY(-2px); border-color: #00c9ff55; }
  .kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  }
  .kpi-blue::before   { background: linear-gradient(90deg, #00c9ff, #0088cc); }
  .kpi-red::before    { background: linear-gradient(90deg, #ff4c4c, #cc2200); }
  .kpi-green::before  { background: linear-gradient(90deg, #4ce87a, #22aa44); }
  .kpi-amber::before  { background: linear-gradient(90deg, #f5a623, #cc7700); }
  .kpi-value { font-size: 1.9rem; font-weight: 800; margin-bottom: 4px; }
  .kpi-label { font-size: 0.72rem; color: #6a8ba0; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
  .kpi-delta { font-size: 0.75rem; margin-top: 6px; font-weight: 600; }
  .blue  { color: #00c9ff; }
  .red   { color: #ff4c4c; }
  .green { color: #4ce87a; }
  .amber { color: #f5a623; }
  .grey  { color: #4a6070; }

  /* Section headers */
  .section-hdr {
    background: linear-gradient(90deg, #0d1b2a, #070d16);
    border-left: 4px solid #f5a623;
    padding: 10px 16px; border-radius: 0 8px 8px 0;
    margin: 24px 0 16px;
    font-size: 0.85rem; font-weight: 700; color: #f5a623;
    text-transform: uppercase; letter-spacing: 1.5px;
  }

  /* Tables */
  .fin-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  .fin-table th {
    background: #00c9ff22; color: #00c9ff; padding: 9px 12px;
    text-align: left; font-weight: 700; border-bottom: 2px solid #1e3a5f;
    text-transform: uppercase; font-size: 0.72rem; letter-spacing: 1px;
  }
  .fin-table td { padding: 8px 12px; border-bottom: 1px solid #0d1b2a; color: #d0e8f0; }
  .fin-table tr:hover td { background: #0d1b2a88; }
  .fin-table .total-row td { border-top: 2px solid #4ce87a; color: #4ce87a; font-weight: 700; font-size: 0.88rem; }
  .fin-table .red-row td   { color: #ff4c4c; }
  .fin-table .amber-row td { color: #f5a623; }
  .fin-table .grey-cell    { color: #4a6070; text-align: center; }
  .right { text-align: right !important; }
  .center { text-align: center !important; }

  /* Verdict banner */
  .verdict {
    background: linear-gradient(135deg, #1a0808 0%, #2a0d0d 100%);
    border: 2px solid #ff4c4c44;
    border-radius: 12px; padding: 20px 24px;
    text-align: center; margin-top: 16px;
  }
  .verdict-title { font-size: 1.15rem; font-weight: 800; color: #ff4c4c; margin-bottom: 8px; }
  .verdict-body  { font-size: 0.85rem; color: #c0d8e8; line-height: 1.7; }

  /* Red flag badge */
  .badge-red   { background:#ff4c4c22; color:#ff4c4c; border:1px solid #ff4c4c44; border-radius:4px; padding:2px 8px; font-size:0.72rem; font-weight:700; }
  .badge-green { background:#4ce87a22; color:#4ce87a; border:1px solid #4ce87a44; border-radius:4px; padding:2px 8px; font-size:0.72rem; font-weight:700; }
  .badge-amber { background:#f5a62322; color:#f5a623; border:1px solid #f5a62344; border-radius:4px; padding:2px 8px; font-size:0.72rem; font-weight:700; }

  .stPlotlyChart { border-radius: 12px; overflow: hidden; }
  div[data-testid="stHorizontalBlock"] > div { gap: 12px; }
</style>
""", unsafe_allow_html=True)

# ── PLOTLY DARK TEMPLATE ──────────────────────────────────────────────────────
TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor='#0d1b2a', plot_bgcolor='#070d16',
        font=dict(family='Inter', color='#8bb8d4', size=12),
        xaxis=dict(gridcolor='#1e3a5f', zerolinecolor='#1e3a5f', linecolor='#1e3a5f'),
        yaxis=dict(gridcolor='#1e3a5f', zerolinecolor='#1e3a5f', linecolor='#1e3a5f'),
        colorway=['#00c9ff','#ff4c4c','#4ce87a','#f5a623','#a78bfa','#fb923c'],
        legend=dict(bgcolor='#0d1b2a', bordercolor='#1e3a5f', borderwidth=1),
        margin=dict(l=50, r=30, t=60, b=50),
    )
)

# ── SIDEBAR INPUTS ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
      <div style='font-size:1.6rem; font-weight:800; color:#00c9ff;'>⚡ VelocityTech</div>
      <div style='font-size:0.72rem; color:#4a6070; letter-spacing:2px; text-transform:uppercase;'>Forensic Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("**📥 Income & Cash Flow Inputs**")
    rev24  = st.number_input("Revenue FY2024 ($M)",      value=3900, step=50)
    rev25  = st.number_input("Revenue FY2025 ($M)",      value=5200, step=50)
    ni24   = st.number_input("Net Income FY2024 ($M)",   value=507,  step=10)
    ni25   = st.number_input("Net Income FY2025 ($M)",   value=780,  step=10)
    da24   = st.number_input("D&A FY2024 ($M)",          value=195,  step=5)
    da25   = st.number_input("D&A FY2025 ($M)",          value=260,  step=5)
    sbc24  = st.number_input("SBC FY2024 ($M)",          value=234,  step=5)
    sbc25  = st.number_input("SBC FY2025 ($M)",          value=390,  step=5)
    ar24   = st.number_input("Δ Accounts Rec. FY2024",   value=156,  step=5)
    ar25   = st.number_input("Δ Accounts Rec. FY2025",   value=320,  step=5)
    inv24  = st.number_input("Δ Inventories FY2024",     value=78,   step=5)
    inv25  = st.number_input("Δ Inventories FY2025",     value=180,  step=5)
    ap24   = st.number_input("Δ Accounts Pay. FY2024",   value=72,   step=5)
    ap25   = st.number_input("Δ Accounts Pay. FY2025",   value=110,  step=5)
    dr24   = st.number_input("Δ Deferred Rev. FY2024",   value=130,  step=5)
    dr25   = st.number_input("Δ Deferred Rev. FY2025",   value=200,  step=5)
    capex24= st.number_input("CapEx FY2024 ($M)",        value=390,  step=10)
    capex25= st.number_input("CapEx FY2025 ($M)",        value=650,  step=10)

    st.markdown("**🏦 Balance Sheet**")
    debt24 = st.number_input("Total Debt FY2024 ($M)",   value=1200, step=50)
    debt25 = st.number_input("Total Debt FY2025 ($M)",   value=2000, step=50)
    cash24 = st.number_input("Cash FY2024 ($M)",         value=600,  step=25)
    cash25 = st.number_input("Cash FY2025 ($M)",         value=900,  step=25)
    assets24=st.number_input("Total Assets FY2024 ($M)", value=5400, step=100)
    assets25=st.number_input("Total Assets FY2025 ($M)", value=7800, step=100)

    st.markdown("**📊 Market Data**")
    shr24  = st.number_input("Shares Out. FY2024 (M)",   value=550,  step=10)
    shr25  = st.number_input("Shares Out. FY2025 (M)",   value=600,  step=10)
    px24   = st.number_input("Share Price FY2024 ($)",   value=38.0, step=1.0)
    px25   = st.number_input("Share Price FY2025 ($)",   value=52.0, step=1.0)

    st.markdown("**⚙️ Q8.2 Assumptions**")
    acq_rev= st.number_input("Acquired Revenue FY25 ($M)", value=520, step=10)
    just_m = st.number_input("Justified EV/FCFF Multiple", value=25,  step=1)

    st.divider()
    st.markdown("<div style='color:#4a6070;font-size:0.7rem;text-align:center;'>Group 8 | Corporate Finance<br>VelocityTech Forensic Analysis</div>", unsafe_allow_html=True)

# ── CALCULATIONS ──────────────────────────────────────────────────────────────
cfo24 = ni24 + da24 + sbc24 - ar24 - inv24 + ap24 + dr24
cfo25 = ni25 + da25 + sbc25 - ar25 - inv25 + ap25 + dr25
fcff24 = cfo24 - capex24
fcff25 = cfo25 - capex25
net_borr25 = debt25 - debt24
fcfe24 = fcff24
fcfe25 = fcff25 + net_borr25
adj_ni24 = ni24 - sbc24
adj_ni25 = ni25 - sbc25
adj_cfo24 = cfo24 - sbc24
adj_cfo25 = cfo25 - sbc25
accrual24 = (ni24 - cfo24) / assets24
accrual25 = (ni25 - cfo25) / assets25
ce24 = cfo24 / ni24
ce25 = cfo25 / ni25
sbc_pct24 = sbc24 / ni24
sbc_pct25 = sbc25 / ni25

eps24 = ni24 / shr24
eps25 = ni25 / shr25
adj_eps24 = adj_ni24 / shr24
adj_eps25 = adj_ni25 / shr25
rep_pe24 = px24 / eps24
rep_pe25 = px25 / eps25
adj_pe24 = px24 / adj_eps24
adj_pe25 = px25 / adj_eps25

org_rev25 = rev25 - acq_rev
org_growth = (org_rev25 - rev24) / rev24
rep_growth = (rev25 - rev24) / rev24

mktcap25 = shr25 * px25
ev25 = mktcap25 + debt25 - cash25
ev_fcff25 = ev25 / fcff25
impl_ev = just_m * fcff25
net_debt25 = debt25 - cash25
impl_equity = impl_ev - net_debt25
impl_px = impl_equity / shr25
overval = (px25 - impl_px) / impl_px

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,#070d16 0%,#0d1b2a 50%,#070d16 100%);
     border:1px solid #1e3a5f; border-radius:16px; padding:24px 32px; margin-bottom:24px;
     display:flex; align-items:center; justify-content:space-between;'>
  <div>
    <div style='font-size:2rem;font-weight:900;color:#00c9ff;letter-spacing:-0.5px;'>
      ⚡ VelocityTech Inc.
    </div>
    <div style='font-size:0.9rem;color:#6a8ba0;margin-top:4px;'>
      Free Cash Flow &amp; Earnings Quality · Forensic Accounting Dashboard · FY2024 vs FY2025
    </div>
  </div>
  <div style='text-align:right;'>
    <div style='font-size:0.72rem;color:#4a6070;text-transform:uppercase;letter-spacing:2px;'>Group 8</div>
    <div style='font-size:0.85rem;color:#f5a623;font-weight:700;margin-top:2px;'>Forensic Analyst Report</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ROW ─────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5,k6,k7,k8 = st.columns(8)
kpi_data = [
    (k1, "CFO FY25",         f"${cfo25:,.0f}M",  f"↑{(cfo25/cfo24-1)*100:.1f}% YoY", "blue",  "kpi-blue"),
    (k2, "Adj NI FY25",      f"${adj_ni25:,.0f}M",f"SBC eats {sbc_pct25*100:.0f}% of NI","red","kpi-red"),
    (k3, "FCFF FY25",        f"${fcff25:,.0f}M",  f"↑{(fcff25/fcff24-1)*100:.1f}% YoY","amber","kpi-amber"),
    (k4, "Rep P/E FY25",     f"{rep_pe25:.1f}×",  "Headline multiple",       "blue",  "kpi-blue"),
    (k5, "SBC-Adj P/E FY25", f"{adj_pe25:.1f}×",  f"+{adj_pe25-rep_pe25:.1f}× vs rep P/E","red","kpi-red"),
    (k6, "EV/FCFF",          f"{ev_fcff25:.1f}×",  f"Justified: {just_m}×",  "red",   "kpi-red"),
    (k7, "Fair Value/Shr",   f"${impl_px:.2f}",    f"vs ${px25:.2f} market",  "green", "kpi-green"),
    (k8, "Overvaluation",    f"{overval*100:.1f}%", "🔴 SELL Signal",         "red",   "kpi-red"),
]
for col, label, val, delta, color, cls in kpi_data:
    with col:
        st.markdown(f"""
        <div class='kpi-card {cls}'>
          <div class='kpi-value {color}'>{val}</div>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-delta {color}'>{delta}</div>
        </div>""", unsafe_allow_html=True)

# ── Q8.1: CFO BUILD-UP + CHART ────────────────────────────────────────────────
st.markdown("<div class='section-hdr'>Q8.1 · Cash Flow from Operations — Indirect Method</div>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.05, 1])

with col_left:
    cfo_rows = [
        ("Net Income",               ni24,   ni25,   False),
        ("+ Depreciation & Amortisation", da24, da25, False),
        ("+ Stock-Based Compensation ⚠", sbc24, sbc25, True),
        ("− Increase in Accounts Rec. ⚠", -ar24, -ar25, True),
        ("− Increase in Inventories ⚠",  -inv24,-inv25, True),
        ("+ Increase in Accounts Pay.",   ap24,  ap25, False),
        ("+ Increase in Deferred Revenue",dr24,  dr25, False),
    ]
    rows_html = ""
    for lbl, v24, v25, is_flag in cfo_rows:
        row_cls = "red-row" if is_flag else ""
        flag = "<span class='badge-red'>⚠ Flag</span>" if is_flag else "<span class='badge-green'>✓</span>"
        rows_html += f"""<tr class='{row_cls}'>
          <td>{lbl}</td>
          <td class='right'>${v24:,.0f}M</td>
          <td class='right'>${v25:,.0f}M</td>
          <td class='center'>{flag}</td>
        </tr>"""
    yoy = (cfo25/cfo24-1)*100
    rows_html += f"""<tr class='total-row'>
      <td>✅ CFO Total</td>
      <td class='right'>${cfo24:,.0f}M</td>
      <td class='right'>${cfo25:,.0f}M</td>
      <td class='center'><span class='badge-green'>↑{yoy:.1f}%</span></td>
    </tr>"""
    st.markdown(f"""
    <table class='fin-table'>
      <thead><tr><th>Component</th><th class='right'>FY2024</th><th class='right'>FY2025</th><th class='center'>Signal</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>""", unsafe_allow_html=True)

with col_right:
    # Waterfall chart for CFO build-up FY2025
    wf_labels = ["Net Income","D&A","SBC","−ΔAR","−ΔInv","ΔAP","Def.Rev","CFO"]
    wf_values = [ni25, da25, sbc25, -ar25, -inv25, ap25, dr25, 0]
    wf_measure = ["absolute","relative","relative","relative","relative","relative","relative","total"]
    wf_colors  = ["#00c9ff","#4ce87a","#f5a623","#ff4c4c","#ff4c4c","#4ce87a","#4ce87a","#00c9ff"]

    fig_wf = go.Figure(go.Waterfall(
        name="CFO Bridge",
        orientation="v",
        measure=wf_measure,
        x=wf_labels,
        y=wf_values,
        text=[f"${v:+,.0f}" if m=="relative" else f"${abs(v):,.0f}" for v,m in zip(wf_values,wf_measure)],
        textposition="outside",
        connector={"line":{"color":"#1e3a5f","width":1,"dash":"dot"}},
        increasing={"marker":{"color":"#4ce87a"}},
        decreasing={"marker":{"color":"#ff4c4c"}},
        totals={"marker":{"color":"#00c9ff"}},
    ))
    fig_wf.update_layout(
        **TEMPLATE['layout'].to_plotly_json(),
        title=dict(text="CFO Bridge FY2025 ($M)", font=dict(color="#00c9ff", size=14), x=0.02),
        showlegend=False, height=340,
    )
    st.plotly_chart(fig_wf, use_container_width=True)

# ── DERIVED METRICS TABLE ─────────────────────────────────────────────────────
st.markdown("<div class='section-hdr'>Q8.1 · Derived Metrics — Free Cash Flow & Earnings Quality</div>", unsafe_allow_html=True)

dc1, dc2, dc3, dc4 = st.columns(4)
metric_cards = [
    (dc1, "FCFF",         fcff24, fcff25, "$", "M",  "blue",  "CFO − CapEx"),
    (dc2, "FCFE",         fcfe24, fcfe25, "$", "M",  "amber", "FCFF + Net Borrowing"),
    (dc3, "Adj Net Income", adj_ni24, adj_ni25, "$","M","red","NI − SBC (real earnings)"),
    (dc4, "Adj CFO (ex-SBC)", adj_cfo24, adj_cfo25, "$","M","amber","True economic CFO"),
]
for col, lbl, v24, v25, pre, suf, clr, sub in metric_cards:
    chg = (v25/v24-1)*100 if v24!=0 else 0
    arrow = "↑" if chg>0 else "↓"
    with col:
        st.markdown(f"""
        <div class='kpi-card kpi-{"blue" if clr=="blue" else "red" if clr=="red" else "amber"}'>
          <div style='font-size:0.68rem;color:#4a6070;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>{lbl}</div>
          <div style='font-size:0.8rem;color:#8bb8d4;'>FY24: <span class='grey'>{pre}{v24:,.0f}{suf}</span></div>
          <div class='kpi-value {clr}' style='font-size:1.5rem;margin:4px 0;'>{pre}{v25:,.0f}{suf}</div>
          <div style='font-size:0.7rem;color:#4a6070;'>{sub}</div>
          <div class='kpi-delta {"green" if chg>0 else "red"}'>{arrow} {abs(chg):.1f}% YoY</div>
        </div>""", unsafe_allow_html=True)

# Quality ratio table + bar chart
st.markdown("<br>", unsafe_allow_html=True)
qc1, qc2 = st.columns([1, 1.2])

with qc1:
    quality_rows = [
        ("Accrual Ratio = (NI−CFO)/Assets", f"{accrual24*100:.2f}%", f"{accrual25*100:.2f}%",
         "amber", "Trending toward 0 ⚠"),
        ("Cash-to-Earnings = CFO/NI",       f"{ce24:.2f}×",          f"{ce25:.2f}×",
         "red",   "Declining = accrual risk ⚠"),
        ("SBC % of Net Income",             f"{sbc_pct24*100:.1f}%", f"{sbc_pct25*100:.1f}%",
         "red",   "50% — critical red flag 🔴"),
        ("Net Borrowing (FY25 only)",        "—",                    f"${net_borr25:,.0f}M",
         "blue",  "ΔDebt FY24→FY25"),
    ]
    q_html = ""
    for lbl, v24, v25, clr, note in quality_rows:
        q_html += f"""<tr>
          <td>{lbl}</td>
          <td class='right {"grey-cell" if v24=="—" else ""}'>{v24}</td>
          <td class='right {clr}'>{v25}</td>
          <td style='font-size:0.75rem;color:#4a6070;'>{note}</td>
        </tr>"""
    st.markdown(f"""
    <table class='fin-table'>
      <thead><tr><th>Quality Metric</th><th class='right'>FY2024</th><th class='right'>FY2025</th><th>Interpretation</th></tr></thead>
      <tbody>{q_html}</tbody>
    </table>""", unsafe_allow_html=True)

with qc2:
    fig_qual = go.Figure()
    cats = ["Net Income","CFO","Adj NI<br>(NI−SBC)","Adj CFO<br>(ex-SBC)","FCFF"]
    v24s = [ni24, cfo24, adj_ni24, adj_cfo24, fcff24]
    v25s = [ni25, cfo25, adj_ni25, adj_cfo25, fcff25]
    fig_qual.add_trace(go.Bar(name="FY2024", x=cats, y=v24s, marker_color="#00c9ff",
                              text=[f"${v:,.0f}" for v in v24s], textposition="outside",
                              textfont=dict(size=10, color="#00c9ff")))
    fig_qual.add_trace(go.Bar(name="FY2025", x=cats, y=v25s, marker_color="#ff4c4c",
                              text=[f"${v:,.0f}" for v in v25s], textposition="outside",
                              textfont=dict(size=10, color="#ff4c4c")))
    fig_qual.update_layout(
        **TEMPLATE['layout'].to_plotly_json(),
        title=dict(text="Reported vs SBC-Adjusted Earnings ($M)", font=dict(color="#00c9ff",size=13), x=0.02),
        barmode="group", height=300,
        legend=dict(orientation='h', y=1.12, x=0.5, xanchor='center',
                    bgcolor='rgba(0,0,0,0)', font=dict(color="#8bb8d4")),
        yaxis=dict(gridcolor='#1e3a5f', zeroline=True, zerolinecolor='#1e3a5f'),
    )
    st.plotly_chart(fig_qual, use_container_width=True)

# ── RED FLAG ANALYSIS ─────────────────────────────────────────────────────────
st.markdown("<div class='section-hdr'>Red Flag Analysis — Is Reported Net Income Overstating Performance?</div>", unsafe_allow_html=True)

rf1, rf2, rf3 = st.columns(3)
flags = [
    (rf1, "🔴 Flag 1: SBC Burden",
     f"SBC consumes <span class='red'>{sbc_pct25*100:.0f}%</span> of Net Income in FY2025 "
     f"(up from {sbc_pct24*100:.0f}% in FY2024). Adj NI of <span class='amber'>${adj_ni25:,.0f}M</span> "
     f"vs reported ${ni25:,.0f}M — earnings are overstated by <span class='red'>{(ni25/adj_ni25-1)*100:.0f}%</span>."),
    (rf2, "⚠️ Flag 2: AR Growing Faster Than Revenue",
     f"Accounts Receivable increase jumped <span class='red'>{(ar25/ar24-1)*100:.0f}%</span> YoY "
     f"(${ar24}M → ${ar25}M) while revenue grew only <span class='amber'>{rep_growth*100:.1f}%</span>. "
     f"Suggests aggressive revenue recognition before cash is collected."),
    (rf3, "⚠️ Flag 3: Declining Cash Quality",
     f"Cash-to-Earnings fell from <span class='amber'>{ce24:.2f}×</span> to <span class='red'>{ce25:.2f}×</span>. "
     f"Earnings growing <span class='red'>faster</span> than real cash. "
     f"Accrual ratio worsening toward zero ({accrual24*100:.2f}% → {accrual25*100:.2f}%)."),
]
for col, title, body in flags:
    with col:
        st.markdown(f"""
        <div style='background:#0d1b2a;border:1px solid #1e3a5f;border-radius:10px;
             padding:16px;height:100%;border-top:3px solid #f5a623;'>
          <div style='font-size:0.85rem;font-weight:700;color:#f5a623;margin-bottom:10px;'>{title}</div>
          <div style='font-size:0.8rem;color:#8bb8d4;line-height:1.7;'>{body}</div>
        </div>""", unsafe_allow_html=True)

# ── Q8.2: VALUATION ───────────────────────────────────────────────────────────
st.markdown("<div class='section-hdr'>Q8.2 · Short-Seller Allegations — Organic Growth, P/E & Valuation</div>", unsafe_allow_html=True)

v_left, v_right = st.columns([1, 1.1])

with v_left:
    val_rows = [
        ("Reported Revenue Growth",         f"{rep_growth*100:.1f}%",  "amber"),
        (f"Organic Rev Growth (ex-${acq_rev}M acq.)", f"{org_growth*100:.1f}%","green"),
        ("Acquisition Revenue Inflation",    f"+{(rep_growth-org_growth)*100:.1f}pp","red"),
        ("EPS Reported FY25",               f"${eps25:.2f}",           "blue"),
        ("EPS SBC-Adjusted FY25",           f"${adj_eps25:.2f}",        "red"),
        ("Reported P/E FY24 / FY25",        f"{rep_pe24:.1f}× / {rep_pe25:.1f}×","blue"),
        ("SBC-Adj P/E FY24 / FY25",         f"{adj_pe24:.1f}× / {adj_pe25:.1f}×","red"),
        ("Enterprise Value (FY25)",         f"${ev25:,.0f}M",           "blue"),
        ("EV/FCFF (Actual)",                f"{ev_fcff25:.1f}×",        "red"),
        (f"Justified EV/FCFF ({just_m}×)",  f"{just_m}×",              "green"),
        ("Implied EV",                      f"${impl_ev:,.0f}M",        "amber"),
        ("Net Debt (FY25)",                 f"${net_debt25:,.0f}M",     "blue"),
        ("Implied Equity Value",            f"${impl_equity:,.0f}M",    "green"),
        ("Implied Fair Value per Share",    f"${impl_px:.2f}",          "green"),
        ("Current Share Price",             f"${px25:.2f}",             "red"),
        ("Overvaluation Premium",           f"{overval*100:.1f}%",      "red"),
    ]
    v_html = ""
    for lbl, val, clr in val_rows:
        bold = "font-weight:700;" if lbl in ["Implied Fair Value per Share","Overvaluation Premium","Current Share Price"] else ""
        v_html += f"<tr><td>{lbl}</td><td class='right {clr}' style='{bold}'>{val}</td></tr>"
    st.markdown(f"""
    <table class='fin-table'>
      <thead><tr><th>Item</th><th class='right'>Value</th></tr></thead>
      <tbody>{v_html}</tbody>
    </table>""", unsafe_allow_html=True)

with v_right:
    # Gauge: Overvaluation
    gauge_val = min(overval * 100, 200)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=px25,
        delta={"reference": impl_px, "valueformat": ".2f",
               "increasing": {"color": "#ff4c4c"}, "decreasing": {"color": "#4ce87a"}},
        number={"prefix": "$", "valueformat": ".2f", "font": {"color": "#00c9ff", "size": 36}},
        title={"text": "Current Price vs Fair Value<br><span style='font-size:0.75em;color:#6a8ba0;'>Fair value: ${:.2f}</span>".format(impl_px),
               "font": {"color": "#8bb8d4", "size": 13}},
        gauge={
            "axis": {"range": [0, max(px25*1.3, impl_px*1.5)],
                     "tickcolor": "#4a6070", "tickfont": {"color": "#6a8ba0"}},
            "bar": {"color": "#ff4c4c", "thickness": 0.25},
            "bgcolor": "#0d1b2a",
            "borderwidth": 0,
            "steps": [
                {"range": [0, impl_px], "color": "#0d3320"},
                {"range": [impl_px, px25], "color": "#2a0d0d"},
            ],
            "threshold": {"line": {"color": "#4ce87a", "width": 3},
                          "thickness": 0.8, "value": impl_px},
        },
    ))
    fig_gauge.update_layout(
        paper_bgcolor="#0d1b2a", font_color="#8bb8d4",
        height=250, margin=dict(l=30, r=30, t=60, b=10)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    # P/E Comparison chart
    pe_labels = ["Rep P/E<br>FY24", "Adj P/E<br>FY24", "Rep P/E<br>FY25", "Adj P/E<br>FY25",
                 f"EV/FCFF<br>Actual", f"EV/FCFF<br>Justified"]
    pe_vals   = [rep_pe24, adj_pe24, rep_pe25, adj_pe25, ev_fcff25, just_m]
    pe_colors = ["#00c9ff","#ff4c4c","#00c9ff","#ff4c4c","#ff4c4c","#4ce87a"]

    fig_pe = go.Figure(go.Bar(
        x=pe_labels, y=pe_vals,
        marker_color=pe_colors,
        text=[f"{v:.1f}×" for v in pe_vals],
        textposition="outside",
        textfont=dict(size=11),
    ))
    fig_pe.update_layout(
        **TEMPLATE['layout'].to_plotly_json(),
        title=dict(text="Valuation Multiples vs Justified (FY25)", font=dict(color="#00c9ff",size=13), x=0.02),
        height=280, showlegend=False,
        yaxis=dict(gridcolor='#1e3a5f', range=[0, max(pe_vals)*1.25]),
    )
    st.plotly_chart(fig_pe, use_container_width=True)

# Revenue bridge
st.markdown("<div class='section-hdr'>Revenue Bridge — Organic vs Acquisition-Driven Growth</div>", unsafe_allow_html=True)
rb1, rb2 = st.columns([1.3, 1])

with rb1:
    fig_bridge = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute","relative","relative","total"],
        x=["FY2024 Revenue", f"Organic Growth<br>+${rev25-acq_rev-rev24:,.0f}M",
           f"Acquired Revenue<br>+${acq_rev:,.0f}M", "FY2025 Revenue"],
        y=[rev24, rev25-acq_rev-rev24, acq_rev, 0],
        text=[f"${rev24:,.0f}M",
              f"+${rev25-acq_rev-rev24:,.0f}M ({org_growth*100:.1f}%)",
              f"+${acq_rev:,.0f}M (inorganic)",
              f"${rev25:,.0f}M"],
        textposition="outside",
        connector={"line":{"color":"#1e3a5f","dash":"dot"}},
        increasing={"marker":{"color":"#4ce87a"}},
        totals={"marker":{"color":"#00c9ff"}},
        textfont=dict(size=11, color="#d0e8f0"),
    ))
    fig_bridge.update_layout(
        **TEMPLATE['layout'].to_plotly_json(),
        title=dict(text=f"Revenue Bridge: Reported {rep_growth*100:.1f}% vs Organic {org_growth*100:.1f}%",
                   font=dict(color="#00c9ff",size=13), x=0.02),
        height=320, showlegend=False,
        yaxis=dict(gridcolor='#1e3a5f', tickformat="$,.0f"),
    )
    st.plotly_chart(fig_bridge, use_container_width=True)

with rb2:
    # Donut: SBC vs Adj NI vs Other costs
    fig_donut = go.Figure(go.Pie(
        labels=["SBC (Non-cash cost)", "Adj Net Income", "All Other Costs"],
        values=[sbc25, adj_ni25, rev25 - ni25 - (ni25 - adj_ni25)],
        hole=0.55,
        marker_colors=["#ff4c4c","#4ce87a","#1e3a5f"],
        textinfo="label+percent",
        textfont=dict(size=11, color="#d0e8f0"),
        insidetextorientation="radial",
    ))
    fig_donut.update_layout(
        paper_bgcolor="#0d1b2a", font_color="#8bb8d4",
        title=dict(text="Revenue Decomposition FY2025",
                   font=dict(color="#00c9ff",size=13), x=0.02),
        legend=dict(bgcolor="#0d1b2a", font=dict(color="#8bb8d4", size=10),
                    orientation="h", y=-0.15),
        height=320,
        annotations=[dict(text=f"Rev<br>${rev25/1000:.1f}B", x=0.5, y=0.5,
                          font_size=14, showarrow=False, font_color="#00c9ff")]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ── VERDICT ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='verdict'>
  <div class='verdict-title'>🔴 ANALYST VERDICT — SHORT-SELLER THESIS CONFIRMED</div>
  <div class='verdict-body'>
    VelocityTech's reported earnings significantly overstate economic performance.
    SBC consumes <strong style='color:#ff4c4c;'>{sbc_pct25*100:.0f}%</strong> of net income, 
    real adjusted earnings are just <strong style='color:#f5a623;'>${adj_ni25:,.0f}M</strong> vs reported ${ni25:,.0f}M.
    Organic revenue growth of <strong style='color:#f5a623;'>{org_growth*100:.1f}%</strong> is materially lower than the headline 
    <strong style='color:#ff4c4c;'>{rep_growth*100:.1f}%</strong> — the gap is entirely acquisition-driven.
    The SBC-adjusted P/E of <strong style='color:#ff4c4c;'>{adj_pe25:.1f}×</strong> is nearly double the reported {rep_pe25:.1f}×.
    At a justified EV/FCFF of {just_m}×, the implied fair value is 
    <strong style='color:#4ce87a;'>${impl_px:.2f} per share</strong> — 
    <strong style='color:#ff4c4c;'>{overval*100:.1f}% below the current market price of ${px25:.2f}.</strong>
  </div>
</div>
""", unsafe_allow_html=True)
