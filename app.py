import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VelocityTech | Forensic Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── REGISTER CUSTOM PLOTLY TEMPLATE (fixes the to_plotly_json conflict) ───────
vt_template = go.layout.Template()
vt_template.layout = go.Layout(
    paper_bgcolor="#0d1b2a",
    plot_bgcolor="#070d16",
    font=dict(family="Inter, sans-serif", color="#8bb8d4", size=12),
    xaxis=dict(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f",
               linecolor="#1e3a5f", tickfont=dict(color="#6a8ba0")),
    yaxis=dict(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f",
               linecolor="#1e3a5f", tickfont=dict(color="#6a8ba0")),
    colorway=["#00c9ff","#ff4c4c","#4ce87a","#f5a623","#a78bfa","#fb923c"],
    legend=dict(bgcolor="#0d1b2a", bordercolor="#1e3a5f",
                borderwidth=1, font=dict(color="#8bb8d4")),
    margin=dict(l=50, r=30, t=60, b=50),
    hoverlabel=dict(bgcolor="#0d1b2a", bordercolor="#1e3a5f",
                    font=dict(color="#d0e8f0")),
)
pio.templates["velocitytech"] = vt_template

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #070d16; }

  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #0a1520 100%);
    border-right: 1px solid #1e3a5f;
  }
  [data-testid="stSidebar"] label { color: #8bb8d4 !important; font-size: 0.78rem !important; }
  [data-testid="stSidebar"] .stNumberInput input {
    background: #112233 !important; color: #e0f0ff !important;
    border: 1px solid #1e3a5f !important; border-radius: 6px !important;
  }
  #MainMenu, footer, header { visibility: hidden; }

  .kpi-card {
    background: linear-gradient(135deg, #0d1b2a 0%, #112233 100%);
    border: 1px solid #1e3a5f; border-radius: 12px;
    padding: 18px 12px 14px; text-align: center;
    position: relative; overflow: hidden; transition: transform 0.2s;
  }
  .kpi-card:hover { transform: translateY(-2px); border-color: #00c9ff55; }
  .kpi-card::before { content:""; position:absolute; top:0; left:0; right:0; height:3px; }
  .kpi-blue::before  { background: linear-gradient(90deg,#00c9ff,#0088cc); }
  .kpi-red::before   { background: linear-gradient(90deg,#ff4c4c,#cc2200); }
  .kpi-green::before { background: linear-gradient(90deg,#4ce87a,#22aa44); }
  .kpi-amber::before { background: linear-gradient(90deg,#f5a623,#cc7700); }
  .kpi-value { font-size: 1.75rem; font-weight: 800; margin-bottom: 4px; }
  .kpi-label { font-size: 0.68rem; color:#6a8ba0; text-transform:uppercase; letter-spacing:1px; font-weight:600; }
  .kpi-delta { font-size: 0.72rem; margin-top: 6px; font-weight: 600; }
  .blue  { color: #00c9ff; } .red   { color: #ff4c4c; }
  .green { color: #4ce87a; } .amber { color: #f5a623; }
  .grey  { color: #4a6070; }

  .section-hdr {
    background: linear-gradient(90deg,#0d1b2a,#070d16);
    border-left: 4px solid #f5a623;
    padding: 10px 16px; border-radius: 0 8px 8px 0;
    margin: 24px 0 14px;
    font-size: 0.82rem; font-weight: 700; color: #f5a623;
    text-transform: uppercase; letter-spacing: 1.5px;
  }

  .fin-table { width:100%; border-collapse:collapse; font-size:0.81rem; }
  .fin-table th {
    background:#00c9ff15; color:#00c9ff; padding:9px 12px;
    text-align:left; font-weight:700; border-bottom:2px solid #1e3a5f;
    text-transform:uppercase; font-size:0.70rem; letter-spacing:1px;
  }
  .fin-table td { padding:7px 12px; border-bottom:1px solid #0d1b2a44; color:#d0e8f0; }
  .fin-table tr:hover td { background:#0d1b2a88; }
  .total-row td { border-top:2px solid #4ce87a; color:#4ce87a; font-weight:700; }
  .red-row td   { color:#ff4c4c; }
  .amber-row td { color:#f5a623; }
  .right  { text-align:right  !important; }
  .center { text-align:center !important; }
  .grey-cell { color:#4a6070 !important; text-align:center !important; }

  .verdict {
    background:linear-gradient(135deg,#1a0808 0%,#2a0d0d 100%);
    border:2px solid #ff4c4c44; border-radius:12px;
    padding:20px 28px; text-align:center; margin-top:20px;
  }
  .verdict-title { font-size:1.1rem; font-weight:800; color:#ff4c4c; margin-bottom:10px; }
  .verdict-body  { font-size:0.83rem; color:#c0d8e8; line-height:1.8; }

  .badge-red   { background:#ff4c4c22; color:#ff4c4c; border:1px solid #ff4c4c44;
                 border-radius:4px; padding:2px 7px; font-size:0.70rem; font-weight:700; }
  .badge-green { background:#4ce87a22; color:#4ce87a; border:1px solid #4ce87a44;
                 border-radius:4px; padding:2px 7px; font-size:0.70rem; font-weight:700; }
  .badge-amber { background:#f5a62322; color:#f5a623; border:1px solid #f5a62344;
                 border-radius:4px; padding:2px 7px; font-size:0.70rem; font-weight:700; }
  .stPlotlyChart { border-radius:12px; overflow:hidden; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR INPUTS ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px;'>
      <div style='font-size:1.5rem;font-weight:800;color:#00c9ff;'>⚡ VelocityTech</div>
      <div style='font-size:0.68rem;color:#4a6070;letter-spacing:2px;text-transform:uppercase;
           margin-top:4px;'>Forensic Dashboard · Group 8</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    st.markdown("**📥 Income & Cash Flow**")
    col_a, col_b = st.columns(2)
    with col_a:
        rev24   = st.number_input("Rev FY24",   value=3900, step=50)
        ni24    = st.number_input("NI FY24",    value=507,  step=10)
        da24    = st.number_input("D&A FY24",   value=195,  step=5)
        sbc24   = st.number_input("SBC FY24",   value=234,  step=5)
        ar24    = st.number_input("ΔAR FY24",   value=156,  step=5)
        inv24   = st.number_input("ΔInv FY24",  value=78,   step=5)
        ap24    = st.number_input("ΔAP FY24",   value=72,   step=5)
        dr24    = st.number_input("ΔDR FY24",   value=130,  step=5)
        capex24 = st.number_input("CapEx FY24", value=390,  step=10)
    with col_b:
        rev25   = st.number_input("Rev FY25",   value=5200, step=50)
        ni25    = st.number_input("NI FY25",    value=780,  step=10)
        da25    = st.number_input("D&A FY25",   value=260,  step=5)
        sbc25   = st.number_input("SBC FY25",   value=390,  step=5)
        ar25    = st.number_input("ΔAR FY25",   value=320,  step=5)
        inv25   = st.number_input("ΔInv FY25",  value=180,  step=5)
        ap25    = st.number_input("ΔAP FY25",   value=110,  step=5)
        dr25    = st.number_input("ΔDR FY25",   value=200,  step=5)
        capex25 = st.number_input("CapEx FY25", value=650,  step=10)

    st.markdown("**🏦 Balance Sheet**")
    c1, c2 = st.columns(2)
    with c1:
        debt24  = st.number_input("Debt FY24",   value=1200, step=50)
        cash24  = st.number_input("Cash FY24",   value=600,  step=25)
        assets24= st.number_input("Assets FY24", value=5400, step=100)
        shr24   = st.number_input("Shr FY24(M)", value=550,  step=10)
        px24    = st.number_input("Price FY24",  value=38.0, step=1.0, format="%.2f")
    with c2:
        debt25  = st.number_input("Debt FY25",   value=2000, step=50)
        cash25  = st.number_input("Cash FY25",   value=900,  step=25)
        assets25= st.number_input("Assets FY25", value=7800, step=100)
        shr25   = st.number_input("Shr FY25(M)", value=600,  step=10)
        px25    = st.number_input("Price FY25",  value=52.0, step=1.0, format="%.2f")

    st.markdown("**⚙️ Assumptions**")
    acq_rev = st.number_input("Acquired Revenue FY25 ($M)", value=520, step=10)
    just_m  = st.number_input("Justified EV/FCFF Multiple", value=25,  step=1)
    st.divider()
    st.markdown(
        "<div style='color:#4a6070;font-size:0.68rem;text-align:center;'>"
        "All metrics recalculate live<br>on every input change</div>",
        unsafe_allow_html=True)

# ── LIVE CALCULATIONS ─────────────────────────────────────────────────────────
cfo24     = ni24 + da24 + sbc24 - ar24 - inv24 + ap24 + dr24
cfo25     = ni25 + da25 + sbc25 - ar25 - inv25 + ap25 + dr25
fcff24    = cfo24 - capex24
fcff25    = cfo25 - capex25
nb25      = debt25 - debt24
fcfe24    = fcff24
fcfe25    = fcff25 + nb25
adj_ni24  = ni24  - sbc24
adj_ni25  = ni25  - sbc25
adj_cfo24 = cfo24 - sbc24
adj_cfo25 = cfo25 - sbc25
accrual24 = (ni24 - cfo24) / assets24
accrual25 = (ni25 - cfo25) / assets25
ce24      = cfo24 / ni24
ce25      = cfo25 / ni25
sbc_pct24 = sbc24 / ni24
sbc_pct25 = sbc25 / ni25
eps24     = ni24  / shr24
eps25     = ni25  / shr25
adj_eps24 = adj_ni24 / shr24
adj_eps25 = adj_ni25 / shr25
rep_pe24  = px24 / eps24
rep_pe25  = px25 / eps25
adj_pe24  = px24 / adj_eps24
adj_pe25  = px25 / adj_eps25
org_rev25   = rev25 - acq_rev
org_growth  = (org_rev25 - rev24) / rev24
rep_growth  = (rev25 - rev24) / rev24
mktcap25    = shr25 * px25
ev25        = mktcap25 + debt25 - cash25
ev_fcff25   = ev25 / fcff25
impl_ev     = just_m * fcff25
net_debt25  = debt25 - cash25
impl_equity = impl_ev - net_debt25
impl_px     = impl_equity / shr25
overval     = (px25 - impl_px) / impl_px

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(135deg,#070d16 0%,#0d1b2a 60%,#070d16 100%);
     border:1px solid #1e3a5f; border-radius:16px; padding:22px 32px;
     margin-bottom:20px; display:flex; align-items:center; justify-content:space-between;'>
  <div>
    <div style='font-size:2rem;font-weight:900;color:#00c9ff;letter-spacing:-0.5px;'>
      ⚡ VelocityTech Inc.
    </div>
    <div style='font-size:0.88rem;color:#6a8ba0;margin-top:4px;'>
      Free Cash Flow &amp; Earnings Quality &nbsp;·&nbsp;
      Forensic Accounting Dashboard &nbsp;·&nbsp; FY2024 vs FY2025
    </div>
  </div>
  <div style='text-align:right;'>
    <div style='font-size:0.7rem;color:#4a6070;text-transform:uppercase;letter-spacing:2px;'>
      Group 8 · Assignment</div>
    <div style='font-size:0.88rem;color:#f5a623;font-weight:700;margin-top:4px;'>
      Stock: <span style='color:#ff4c4c;'>${px25:.2f}</span> &nbsp;|&nbsp;
      Fair Value: <span style='color:#4ce87a;'>${impl_px:.2f}</span> &nbsp;|&nbsp;
      Overvalued: <span style='color:#ff4c4c;'>{overval*100:.1f}%</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
k = st.columns(8)
kpis = [
    (k[0], "CFO FY25",       f"${cfo25:,.0f}M",   f"↑{(cfo25/cfo24-1)*100:.1f}% YoY",      "blue",  "kpi-blue"),
    (k[1], "Adj NI FY25",    f"${adj_ni25:,.0f}M", f"SBC={sbc_pct25*100:.0f}% of NI 🔴",    "red",   "kpi-red"),
    (k[2], "FCFF FY25",      f"${fcff25:,.0f}M",   f"↑{(fcff25/fcff24-1)*100:.1f}% YoY",    "amber", "kpi-amber"),
    (k[3], "Reported P/E",   f"{rep_pe25:.1f}×",   "Headline multiple",                       "blue",  "kpi-blue"),
    (k[4], "SBC-Adj P/E",    f"{adj_pe25:.1f}×",   f"+{adj_pe25-rep_pe25:.1f}× vs rep 🔴",  "red",   "kpi-red"),
    (k[5], "EV / FCFF",      f"{ev_fcff25:.1f}×",  f"Justified: {just_m}× 🔴",              "red",   "kpi-red"),
    (k[6], "Fair Value/Shr", f"${impl_px:.2f}",     f"vs ${px25:.2f} market",                 "green", "kpi-green"),
    (k[7], "Overvaluation",  f"{overval*100:.1f}%", "🔴 SELL Signal",                         "red",   "kpi-red"),
]
for col, lbl, val, delta, clr, cls in kpis:
    with col:
        st.markdown(f"""
        <div class='kpi-card {cls}'>
          <div class='kpi-value {clr}'>{val}</div>
          <div class='kpi-label'>{lbl}</div>
          <div class='kpi-delta {clr}'>{delta}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Q8.1: CFO BUILD-UP ────────────────────────────────────────────────────────
st.markdown("<div class='section-hdr'>Q8.1 · Cash Flow from Operations — Indirect Method</div>",
            unsafe_allow_html=True)
left, right = st.columns([1.05, 1])

with left:
    cfo_items = [
        ("Net Income",                    ni24,   ni25,   False),
        ("+ Depreciation & Amortisation", da24,   da25,   False),
        ("+ Stock-Based Compensation ⚠",  sbc24,  sbc25,  True),
        ("− Increase in Accounts Rec. ⚠", -ar24,  -ar25,  True),
        ("− Increase in Inventories ⚠",   -inv24, -inv25, True),
        ("+ Increase in Accounts Pay.",   ap24,   ap25,   False),
        ("+ Increase in Deferred Rev.",   dr24,   dr25,   False),
    ]
    rows_html = ""
    for lbl, v24, v25, flag in cfo_items:
        cls = "red-row" if flag else ""
        bdg = "<span class='badge-red'>⚠ Flag</span>" if flag else "<span class='badge-green'>✓ OK</span>"
        rows_html += f"""<tr class='{cls}'>
          <td>{lbl}</td><td class='right'>${v24:,.0f}M</td>
          <td class='right'>${v25:,.0f}M</td><td class='center'>{bdg}</td></tr>"""
    yoy = (cfo25/cfo24-1)*100
    rows_html += f"""<tr class='total-row'>
      <td>✅  CFO Total</td><td class='right'>${cfo24:,.0f}M</td>
      <td class='right'>${cfo25:,.0f}M</td>
      <td class='center'><span class='badge-green'>↑{yoy:.1f}%</span></td></tr>"""
    st.markdown(f"""<table class='fin-table'><thead>
      <tr><th>Component</th><th class='right'>FY2024</th>
          <th class='right'>FY2025</th><th class='center'>Signal</th></tr>
      </thead><tbody>{rows_html}</tbody></table>""", unsafe_allow_html=True)

with right:
    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute","relative","relative","relative",
                 "relative","relative","relative","total"],
        x=["NI","D&A","SBC","−ΔAR","−ΔInv","ΔAP","Def.Rev","CFO"],
        y=[ni25, da25, sbc25, -ar25, -inv25, ap25, dr25, 0],
        text=[f"${v:+,.0f}" if i not in (0,7) else f"${abs(v):,.0f}"
              for i,v in enumerate([ni25,da25,sbc25,-ar25,-inv25,ap25,dr25,0])],
        textposition="outside",
        textfont=dict(size=10),
        connector={"line":{"color":"#1e3a5f","width":1,"dash":"dot"}},
        increasing={"marker":{"color":"#4ce87a","line":{"color":"#4ce87a","width":0}}},
        decreasing={"marker":{"color":"#ff4c4c","line":{"color":"#ff4c4c","width":0}}},
        totals={"marker":{"color":"#00c9ff","line":{"color":"#00c9ff","width":0}}},
    ))
    fig_wf.update_layout(
        template="velocitytech",
        title=dict(text="CFO Build-Up — FY2025 ($M)",
                   font=dict(color="#00c9ff", size=13), x=0.02),
        height=340, showlegend=False,
    )
    st.plotly_chart(fig_wf, use_container_width=True)

# ── DERIVED METRICS ───────────────────────────────────────────────────────────
st.markdown("<div class='section-hdr'>Q8.1 · Free Cash Flow & Quality Metrics</div>",
            unsafe_allow_html=True)
mc = st.columns(4)
mini_kpis = [
    (mc[0], "FCFF",             fcff24,    fcff25,    "blue",  "CFO − CapEx"),
    (mc[1], "FCFE",             fcfe24,    fcfe25,    "amber", "FCFF + Net Borrowing"),
    (mc[2], "Adj Net Income",   adj_ni24,  adj_ni25,  "red",   "NI − SBC (real earnings)"),
    (mc[3], "Adj CFO (ex-SBC)", adj_cfo24, adj_cfo25, "amber", "True economic CFO"),
]
for col, lbl, v24, v25, clr, sub in mini_kpis:
    chg = (v25/v24-1)*100 if v24 != 0 else 0
    with col:
        st.markdown(f"""
        <div class='kpi-card kpi-{"blue" if clr=="blue" else "red" if clr=="red" else "amber"}'>
          <div style='font-size:0.65rem;color:#4a6070;text-transform:uppercase;
               letter-spacing:1px;margin-bottom:4px;'>{lbl}</div>
          <div style='font-size:0.78rem;color:#8bb8d4;'>
            FY24: <span class='grey'>${v24:,.0f}M</span></div>
          <div class='kpi-value {clr}' style='font-size:1.5rem;margin:4px 0;'>${v25:,.0f}M</div>
          <div style='font-size:0.68rem;color:#4a6070;margin-bottom:4px;'>{sub}</div>
          <div class='kpi-delta {"green" if chg>=0 else "red"}'>
            {"↑" if chg>=0 else "↓"} {abs(chg):.1f}% YoY</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
qc1, qc2 = st.columns([1, 1.2])

with qc1:
    q_rows = [
        ("Accrual Ratio = (NI−CFO)/Assets",
         f"{accrual24*100:.2f}%", f"{accrual25*100:.2f}%", "amber", "Trending → 0 ⚠"),
        ("Cash-to-Earnings = CFO/NI",
         f"{ce24:.2f}×", f"{ce25:.2f}×", "red", "Declining = accrual risk ⚠"),
        ("SBC % of Net Income",
         f"{sbc_pct24*100:.1f}%", f"{sbc_pct25*100:.1f}%", "red", "50% NI = SBC 🔴"),
        ("Net Borrowing (FY25 only)",
         "—", f"${nb25:,.0f}M", "blue", "ΔDebt year-over-year"),
    ]
    q_html = ""
    for lbl, v24, v25, clr, note in q_rows:
        q_html += f"""<tr>
          <td>{lbl}</td>
          <td class='right {"grey-cell" if v24=="—" else ""}'>{v24}</td>
          <td class='right {clr}'>{v25}</td>
          <td style='font-size:0.72rem;color:#4a6070;'>{note}</td></tr>"""
    st.markdown(f"""<table class='fin-table'><thead>
      <tr><th>Quality Metric</th><th class='right'>FY2024</th>
          <th class='right'>FY2025</th><th>Note</th></tr>
      </thead><tbody>{q_html}</tbody></table>""", unsafe_allow_html=True)

with qc2:
    cats = ["Net Income","CFO","Adj NI<br>(NI-SBC)","Adj CFO<br>(ex-SBC)","FCFF"]
    v24s = [ni24, cfo24, adj_ni24, adj_cfo24, fcff24]
    v25s = [ni25, cfo25, adj_ni25, adj_cfo25, fcff25]
    fig_qual = go.Figure()
    fig_qual.add_trace(go.Bar(
        name="FY2024", x=cats, y=v24s, marker_color="#00c9ff",
        text=[f"${v:,.0f}" for v in v24s],
        textposition="outside", textfont=dict(size=10, color="#00c9ff"),
    ))
    fig_qual.add_trace(go.Bar(
        name="FY2025", x=cats, y=v25s, marker_color="#ff4c4c",
        text=[f"${v:,.0f}" for v in v25s],
        textposition="outside", textfont=dict(size=10, color="#ff4c4c"),
    ))
    fig_qual.update_layout(
        template="velocitytech",
        title=dict(text="Reported vs SBC-Adjusted Earnings ($M)",
                   font=dict(color="#00c9ff", size=13), x=0.02),
        barmode="group", height=300,
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
        yaxis=dict(gridcolor="#1e3a5f", zeroline=True, zerolinecolor="#1e3a5f"),
    )
    st.plotly_chart(fig_qual, use_container_width=True)

# ── RED FLAGS ─────────────────────────────────────────────────────────────────
st.markdown("<div class='section-hdr'>Red Flag Analysis — Three Quantitative Indicators</div>",
            unsafe_allow_html=True)
rf1, rf2, rf3 = st.columns(3)
flags 
