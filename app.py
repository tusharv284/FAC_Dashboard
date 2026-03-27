import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

st.set_page_config(
    page_title="VelocityTech | Forensic Dashboard",
    page_icon="⚡", layout="wide",
    initial_sidebar_state="expanded"
)

# ── PLOTLY TEMPLATE ───────────────────────────────────────────────────────────
vt = go.layout.Template()
vt.layout = go.Layout(
    paper_bgcolor="#0d1b2a", plot_bgcolor="#070d16",
    font=dict(family="Inter, sans-serif", color="#8bb8d4", size=12),
    xaxis=dict(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f", linecolor="#1e3a5f",
               tickfont=dict(color="#6a8ba0")),
    yaxis=dict(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f", linecolor="#1e3a5f",
               tickfont=dict(color="#6a8ba0")),
    colorway=["#00c9ff","#ff4c4c","#4ce87a","#f5a623","#a78bfa","#fb923c"],
    legend=dict(bgcolor="#0d1b2a", bordercolor="#1e3a5f", borderwidth=1,
                font=dict(color="#8bb8d4")),
    margin=dict(l=50, r=30, t=60, b=50),
    hoverlabel=dict(bgcolor="#0d1b2a", bordercolor="#1e3a5f",
                    font=dict(color="#d0e8f0")),
)
pio.templates["vt"] = vt

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:#070d16;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d1b2a,#0a1520);border-right:1px solid #1e3a5f;}
[data-testid="stSidebar"] label{color:#8bb8d4!important;font-size:0.78rem!important;}
[data-testid="stSidebar"] .stNumberInput input{background:#112233!important;color:#e0f0ff!important;border:1px solid #1e3a5f!important;border-radius:6px!important;}
#MainMenu,footer,header{visibility:hidden;}
.kpi-card{background:linear-gradient(135deg,#0d1b2a,#112233);border:1px solid #1e3a5f;border-radius:12px;padding:18px 10px 14px;text-align:center;position:relative;overflow:hidden;transition:transform .2s;}
.kpi-card:hover{transform:translateY(-2px);border-color:#00c9ff55;}
.kpi-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;}
.kpi-blue::before{background:linear-gradient(90deg,#00c9ff,#0088cc);}
.kpi-red::before{background:linear-gradient(90deg,#ff4c4c,#cc2200);}
.kpi-green::before{background:linear-gradient(90deg,#4ce87a,#22aa44);}
.kpi-amber::before{background:linear-gradient(90deg,#f5a623,#cc7700);}
.kv{font-size:1.7rem;font-weight:800;margin-bottom:4px;}
.kl{font-size:0.66rem;color:#6a8ba0;text-transform:uppercase;letter-spacing:1px;font-weight:600;}
.kd{font-size:0.70rem;margin-top:5px;font-weight:600;}
.blue{color:#00c9ff;}.red{color:#ff4c4c;}.green{color:#4ce87a;}.amber{color:#f5a623;}.grey{color:#4a6070;}
.shdr{background:linear-gradient(90deg,#0d1b2a,#070d16);border-left:4px solid #f5a623;padding:10px 16px;border-radius:0 8px 8px 0;margin:22px 0 14px;font-size:0.80rem;font-weight:700;color:#f5a623;text-transform:uppercase;letter-spacing:1.5px;}
.ftb{width:100%;border-collapse:collapse;font-size:0.80rem;}
.ftb th{background:#00c9ff15;color:#00c9ff;padding:9px 12px;text-align:left;font-weight:700;border-bottom:2px solid #1e3a5f;text-transform:uppercase;font-size:0.68rem;letter-spacing:1px;}
.ftb td{padding:7px 12px;border-bottom:1px solid #0d1b2a55;color:#d0e8f0;}
.ftb tr:hover td{background:#0d1b2a88;}
.tr-tot td{border-top:2px solid #4ce87a;color:#4ce87a;font-weight:700;}
.tr-red td{color:#ff4c4c;}
.r{text-align:right!important;}.c{text-align:center!important;}
.gc{color:#4a6070!important;text-align:center!important;}
.bdr{background:#ff4c4c22;color:#ff4c4c;border:1px solid #ff4c4c55;border-radius:4px;padding:2px 7px;font-size:0.68rem;font-weight:700;}
.bdg{background:#4ce87a22;color:#4ce87a;border:1px solid #4ce87a55;border-radius:4px;padding:2px 7px;font-size:0.68rem;font-weight:700;}
.verdict{background:linear-gradient(135deg,#1a0808,#2a0d0d);border:2px solid #ff4c4c44;border-radius:12px;padding:20px 28px;text-align:center;margin-top:20px;}
.vt{font-size:1.1rem;font-weight:800;color:#ff4c4c;margin-bottom:10px;}
.vb{font-size:0.82rem;color:#c0d8e8;line-height:1.8;}
.flag-card{background:#0d1b2a;border:1px solid #1e3a5f;border-radius:10px;padding:16px;border-top:3px solid #f5a623;height:100%;}
.flag-title{font-size:0.82rem;font-weight:700;color:#f5a623;margin-bottom:10px;}
.flag-body{font-size:0.77rem;color:#8bb8d4;line-height:1.75;}
.hl-red{color:#ff4c4c;font-weight:700;}
.hl-amb{color:#f5a623;font-weight:700;}
.hl-grn{color:#4ce87a;font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:14px 0 6px;'>
      <div style='font-size:1.45rem;font-weight:800;color:#00c9ff;'>⚡ VelocityTech</div>
      <div style='font-size:0.66rem;color:#4a6070;letter-spacing:2px;text-transform:uppercase;margin-top:3px;'>
        Forensic Dashboard · Group 8</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    st.markdown("**📥 Income & Cash Flow**")
    ca, cb = st.columns(2)
    with ca:
        rev24   = st.number_input("Rev FY24",    value=3900, step=50)
        ni24    = st.number_input("NI FY24",     value=507,  step=10)
        da24    = st.number_input("D&A FY24",    value=195,  step=5)
        sbc24   = st.number_input("SBC FY24",    value=234,  step=5)
        ar24    = st.number_input("dAR FY24",    value=156,  step=5)
        inv24   = st.number_input("dInv FY24",   value=78,   step=5)
        ap24    = st.number_input("dAP FY24",    value=72,   step=5)
        dr24    = st.number_input("dDR FY24",    value=130,  step=5)
        capex24 = st.number_input("CapEx FY24",  value=390,  step=10)
    with cb:
        rev25   = st.number_input("Rev FY25",    value=5200, step=50)
        ni25    = st.number_input("NI FY25",     value=780,  step=10)
        da25    = st.number_input("D&A FY25",    value=260,  step=5)
        sbc25   = st.number_input("SBC FY25",    value=390,  step=5)
        ar25    = st.number_input("dAR FY25",    value=320,  step=5)
        inv25   = st.number_input("dInv FY25",   value=180,  step=5)
        ap25    = st.number_input("dAP FY25",    value=110,  step=5)
        dr25    = st.number_input("dDR FY25",    value=200,  step=5)
        capex25 = st.number_input("CapEx FY25",  value=650,  step=10)

    st.markdown("**🏦 Balance Sheet**")
    c1, c2 = st.columns(2)
    with c1:
        debt24   = st.number_input("Debt FY24",   value=1200, step=50)
        cash24   = st.number_input("Cash FY24",   value=600,  step=25)
        assets24 = st.number_input("Assets FY24", value=5400, step=100)
        shr24    = st.number_input("Shares FY24", value=550,  step=10)
        px24     = st.number_input("Price FY24",  value=38.0, step=1.0, format="%.2f")
    with c2:
        debt25   = st.number_input("Debt FY25",   value=2000, step=50)
        cash25   = st.number_input("Cash FY25",   value=900,  step=25)
        assets25 = st.number_input("Assets FY25", value=7800, step=100)
        shr25    = st.number_input("Shares FY25", value=600,  step=10)
        px25     = st.number_input("Price FY25",  value=52.0, step=1.0, format="%.2f")

    st.markdown("**⚙️ Assumptions**")
    acq_rev = st.number_input("Acquired Rev FY25 ($M)", value=520, step=10)
    just_m  = st.number_input("Justified EV/FCFF Mult", value=25,  step=1)
    st.divider()
    st.markdown(
        "<div style='color:#4a6070;font-size:0.67rem;text-align:center;'>"
        "All metrics update live on input change</div>",
        unsafe_allow_html=True)

# ── CALCULATIONS ──────────────────────────────────────────────────────────────
cfo24     = ni24 + da24 + sbc24 - ar24 - inv24 + ap24 + dr24
cfo25     = ni25 + da25 + sbc25 - ar25 - inv25 + ap25 + dr25
fcff24    = cfo24 - capex24
fcff25    = cfo25 - capex25
nb25      = debt25 - debt24
fcfe24    = fcff24
fcfe25    = fcff25 + nb25
adj_ni24  = ni24 - sbc24
adj_ni25  = ni25 - sbc25
adj_cfo24 = cfo24 - sbc24
adj_cfo25 = cfo25 - sbc25
accrual24 = (ni24 - cfo24) / assets24
accrual25 = (ni25 - cfo25) / assets25
ce24      = cfo24 / ni24
ce25      = cfo25 / ni25
sbc_pct24 = sbc24 / ni24
sbc_pct25 = sbc25 / ni25
eps24     = ni24 / shr24
eps25     = ni25 / shr25
adj_eps24 = adj_ni24 / shr24
adj_eps25 = adj_ni25 / shr25
rep_pe24  = px24 / eps24
rep_pe25  = px25 / eps25
adj_pe24  = px24 / adj_eps24
adj_pe25  = px25 / adj_eps25
org_rev25    = rev25 - acq_rev
org_growth   = (org_rev25 - rev24) / rev24
rep_growth   = (rev25 - rev24) / rev24
mktcap25     = shr25 * px25
ev25         = mktcap25 + debt25 - cash25
ev_fcff25    = ev25 / fcff25
impl_ev      = just_m * fcff25
net_debt25   = debt25 - cash25
impl_equity  = impl_ev - net_debt25
impl_px      = impl_equity / shr25
overval      = (px25 - impl_px) / impl_px
ni_overstate = (ni25 / adj_ni25 - 1) * 100 if adj_ni25 != 0 else 0
ar_growth    = (ar25 / ar24 - 1) * 100 if ar24 != 0 else 0
cfo_yoy      = (cfo25 / cfo24 - 1) * 100 if cfo24 != 0 else 0
fcff_yoy     = (fcff25 / fcff24 - 1) * 100 if fcff24 != 0 else 0
adj_ni_yoy   = (adj_ni25 / adj_ni24 - 1) * 100 if adj_ni24 != 0 else 0
adj_cfo_yoy  = (adj_cfo25 / adj_cfo24 - 1) * 100 if adj_cfo24 != 0 else 0
pe_gap       = adj_pe25 - rep_pe25
org_add      = rev25 - acq_rev - rev24

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='background:linear-gradient(135deg,#070d16 0%,#0d1b2a 60%,#070d16 100%);"
    "border:1px solid #1e3a5f;border-radius:16px;padding:22px 32px;margin-bottom:20px;"
    "display:flex;align-items:center;justify-content:space-between;'>"
    "<div>"
    "<div style='font-size:1.9rem;font-weight:900;color:#00c9ff;'>⚡ VelocityTech Inc.</div>"
    "<div style='font-size:0.87rem;color:#6a8ba0;margin-top:4px;'>"
    "Free Cash Flow &amp; Earnings Quality &nbsp;&middot;&nbsp; "
    "Forensic Accounting Dashboard &nbsp;&middot;&nbsp; FY2024 vs FY2025</div>"
    "</div>"
    "<div style='text-align:right;'>"
    "<div style='font-size:0.68rem;color:#4a6070;text-transform:uppercase;letter-spacing:2px;'>Group 8 &middot; Assignment</div>"
    "<div style='font-size:0.85rem;color:#f5a623;font-weight:700;margin-top:4px;'>"
    "Stock: <span style='color:#ff4c4c;'>$" + str(round(px25, 2)) + "</span>"
    " &nbsp;|&nbsp; Fair Value: <span style='color:#4ce87a;'>$" + str(round(impl_px, 2)) + "</span>"
    " &nbsp;|&nbsp; Overvalued: <span style='color:#ff4c4c;'>" + str(round(overval*100, 1)) + "%</span>"
    "</div></div></div>",
    unsafe_allow_html=True
)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
k = st.columns(8)
kpi_list = [
    (k[0], "CFO FY25",     "$"+f"{cfo25:,.0f}"+"M",    "Up "+f"{cfo_yoy:.1f}"+"% YoY",         "blue",  "kpi-blue"),
    (k[1], "Adj NI FY25",  "$"+f"{adj_ni25:,.0f}"+"M", "SBC="+f"{sbc_pct25*100:.0f}"+"% of NI", "red",   "kpi-red"),
    (k[2], "FCFF FY25",    "$"+f"{fcff25:,.0f}"+"M",   "Up "+f"{fcff_yoy:.1f}"+"% YoY",         "amber", "kpi-amber"),
    (k[3], "Rep P/E",      f"{rep_pe25:.1f}"+"x",       "Headline multiple",                      "blue",  "kpi-blue"),
    (k[4], "SBC-Adj P/E",  f"{adj_pe25:.1f}"+"x",       "+"+f"{pe_gap:.1f}"+"x vs rep",           "red",   "kpi-red"),
    (k[5], "EV / FCFF",    f"{ev_fcff25:.1f}"+"x",      "Justified: "+str(just_m)+"x",            "red",   "kpi-red"),
    (k[6], "Fair Val/Shr", "$"+f"{impl_px:.2f}",         "vs $"+f"{px25:.2f}"+" mkt",              "green", "kpi-green"),
    (k[7], "Overvaluation",f"{overval*100:.1f}"+"%",     "SELL Signal",                            "red",   "kpi-red"),
]
for col, lbl, val, delta, clr, cls in kpi_list:
    with col:
        st.markdown(
            "<div class='kpi-card "+cls+"'>"
            "<div class='kv "+clr+"'>"+val+"</div>"
            "<div class='kl'>"+lbl+"</div>"
            "<div class='kd "+clr+"'>"+delta+"</div>"
            "</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Q8.1 CFO BUILD-UP ─────────────────────────────────────────────────────────
st.markdown("<div class='shdr'>Q8.1 &middot; Cash Flow from Operations &mdash; Indirect Method</div>",
            unsafe_allow_html=True)
l, r = st.columns([1.05, 1])

with l:
    cfo_rows = [
        ("Net Income",                        ni24,   ni25,   False),
        ("+ Depreciation &amp; Amortisation", da24,   da25,   False),
        ("+ Stock-Based Compensation",        sbc24,  sbc25,  True),
        ("&minus; Increase in Accounts Rec.", -ar24,  -ar25,  True),
        ("&minus; Increase in Inventories",   -inv24, -inv25, True),
        ("+ Increase in Accounts Pay.",       ap24,   ap25,   False),
        ("+ Increase in Deferred Rev.",       dr24,   dr25,   False),
    ]
    rows_html = ""
    for lbl, v24, v25, is_flag in cfo_rows:
        rc  = "tr-red" if is_flag else ""
        bdg = "<span class='bdr'>&#9888; Flag</span>" if is_flag else "<span class='bdg'>&#10003; OK</span>"
        rows_html += (
            "<tr class='"+rc+"'><td>"+lbl+"</td>"
            "<td class='r'>$"+f"{v24:,.0f}"+"M</td>"
            "<td class='r'>$"+f"{v25:,.0f}"+"M</td>"
            "<td class='c'>"+bdg+"</td></tr>"
        )
    rows_html += (
        "<tr class='tr-tot'><td>&#9989; CFO Total</td>"
        "<td class='r'>$"+f"{cfo24:,.0f}"+"M</td>"
        "<td class='r'>$"+f"{cfo25:,.0f}"+"M</td>"
        "<td class='c'><span class='bdg'>+"+f"{cfo_yoy:.1f}"+"%</span></td></tr>"
    )
    st.markdown(
        "<table class='ftb'><thead><tr>"
        "<th>Component</th><th class='r'>FY2024</th>"
        "<th class='r'>FY2025</th><th class='c'>Signal</th>"
        "</tr></thead><tbody>"+rows_html+"</tbody></table>",
        unsafe_allow_html=True)

with r:
    wf_x  = ["NI","D&A","SBC","-dAR","-dInv","dAP","Def.Rev","CFO"]
    wf_y  = [ni25, da25, sbc25, -ar25, -inv25, ap25, dr25, 0]
    wf_ms = ["absolute","relative","relative","relative","relative","relative","relative","total"]
    wf_tx = []
    for i, v in enumerate(wf_y):
        if i == 0:   wf_tx.append("$"+f"{v:,.0f}")
        elif i == 7: wf_tx.append("$"+f"{cfo25:,.0f}")
        elif v >= 0: wf_tx.append("+$"+f"{v:,.0f}")
        else:        wf_tx.append("-$"+f"{abs(v):,.0f}")

    fig_wf = go.Figure(go.Waterfall(
        orientation="v", measure=wf_ms, x=wf_x, y=wf_y,
        text=wf_tx, textposition="outside", textfont=dict(size=10),
        connector={"line":{"color":"#1e3a5f","width":1,"dash":"dot"}},
        increasing={"marker":{"color":"#4ce87a","line":{"color":"#4ce87a","width":0}}},
        decreasing={"marker":{"color":"#ff4c4c","line":{"color":"#ff4c4c","width":0}}},
        totals={"marker":{"color":"#00c9ff","line":{"color":"#00c9ff","width":0}}},
    ))
    fig_wf.update_layout(
        template="vt",
        title=dict(text="CFO Build-Up FY2025 ($M)", font=dict(color="#00c9ff",size=13), x=0.02),
        height=340, showlegend=False,
    )
    st.plotly_chart(fig_wf, use_container_width=True)

# ── DERIVED METRICS ───────────────────────────────────────────────────────────
st.markdown("<div class='shdr'>Q8.1 &middot; Free Cash Flow &amp; Earnings Quality Metrics</div>",
            unsafe_allow_html=True)
mc = st.columns(4)
mini_kpis = [
    (mc[0], "FCFF = CFO - CapEx",      fcff24,    fcff25,    "blue",  fcff_yoy),
    (mc[1], "FCFE = FCFF + Net Borr.", fcfe24,    fcfe25,    "amber", 0),
    (mc[2], "Adj Net Income (NI-SBC)", adj_ni24,  adj_ni25,  "red",   adj_ni_yoy),
    (mc[3], "Adj CFO (ex-SBC)",        adj_cfo24, adj_cfo25, "amber", adj_cfo_yoy),
]
for col, lbl, v24, v25, clr, yoy in mini_kpis:
    arrow = "Up" if yoy >= 0 else "Dn"
    clr2  = "green" if yoy >= 0 else "red"
    brd   = "kpi-blue" if clr=="blue" else ("kpi-red" if clr=="red" else "kpi-amber")
    with col:
        st.markdown(
            "<div class='kpi-card "+brd+"'>"
            "<div style='font-size:0.63rem;color:#4a6070;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px;'>"+lbl+"</div>"
            "<div style='font-size:0.76rem;color:#8bb8d4;'>FY24: <span class='grey'>$"+f"{v24:,.0f}"+"M</span></div>"
            "<div class='kv "+clr+"' style='font-size:1.45rem;margin:4px 0;'>$"+f"{v25:,.0f}"+"M</div>"
            "<div class='kd "+clr2+"'>"+arrow+" "+f"{abs(yoy):.1f}"+"% YoY</div>"
            "</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
qc1, qc2 = st.columns([1, 1.2])

with qc1:
    qrow_data = [
        ("Accrual Ratio = (NI-CFO)/Assets", f"{accrual24*100:.2f}%", f"{accrual25*100:.2f}%", "amber", "Trending toward 0 - warning"),
        ("Cash-to-Earnings = CFO/NI",       f"{ce24:.2f}x",          f"{ce25:.2f}x",          "red",   "Declining = accrual risk"),
        ("SBC % of Net Income",             f"{sbc_pct24*100:.1f}%", f"{sbc_pct25*100:.1f}%", "red",   "50% in FY25 - critical"),
        ("Net Borrowing (FY25 only)",       "--",                    "$"+f"{nb25:,.0f}"+"M",   "blue",  "Change in total debt"),
    ]
    q_rows_html = ""
    for lbl, v24, v25, clr, note in qrow_data:
        gc = "gc" if v24 == "--" else ""
        q_rows_html += (
            "<tr><td>"+lbl+"</td>"
            "<td class='r "+gc+"'>"+v24+"</td>"
            "<td class='r "+clr+"'>"+v25+"</td>"
            "<td style='font-size:0.71rem;color:#4a6070;'>"+note+"</td></tr>"
        )
    st.markdown(
        "<table class='ftb'><thead><tr>"
        "<th>Quality Metric</th><th class='r'>FY2024</th>"
        "<th class='r'>FY2025</th><th>Note</th>"
        "</tr></thead><tbody>"+q_rows_html+"</tbody></table>",
        unsafe_allow_html=True)

with qc2:
    cats = ["Net Income","CFO","Adj NI","Adj CFO","FCFF"]
    v24s = [ni24, cfo24, adj_ni24, adj_cfo24, fcff24]
    v25s = [ni25, cfo25, adj_ni25, adj_cfo25, fcff25]
    fig_qual = go.Figure()
    fig_qual.add_trace(go.Bar(
        name="FY2024", x=cats, y=v24s, marker_color="#00c9ff",
        text=["$"+f"{v:,.0f}" for v in v24s],
        textposition="outside", textfont=dict(size=10, color="#00c9ff"),
    ))
    fig_qual.add_trace(go.Bar(
        name="FY2025", x=cats, y=v25s, marker_color="#ff4c4c",
        text=["$"+f"{v:,.0f}" for v in v25s],
        textposition="outside", textfont=dict(size=10, color="#ff4c4c"),
    ))
    fig_qual.update_layout(
        template="vt",
        title=dict(text="Reported vs SBC-Adjusted Earnings ($M)",
                   font=dict(color="#00c9ff",size=13), x=0.02),
        barmode="group", height=300,
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
        yaxis=dict(gridcolor="#1e3a5f"),
    )
    st.plotly_chart(fig_qual, use_container_width=True)

# ── RED FLAGS ─────────────────────────────────────────────────────────────────
st.markdown("<div class='shdr'>Red Flag Analysis &mdash; Three Quantitative Indicators</div>",
            unsafe_allow_html=True)

# Pre-compute all strings FIRST — avoids nested f-string NameError
f1_sbc_pct25 = str(round(sbc_pct25 * 100))
f1_sbc_pct24 = str(round(sbc_pct24 * 100))
f1_adj_ni25  = f"{adj_ni25:,.0f}"
f1_ni25      = f"{ni25:,.0f}"
f1_overstate = str(round(ni_overstate))
f2_ar_growth = str(round(ar_growth))
f2_ar24      = str(ar24)
f2_ar25      = str(ar25)
f2_rep_gr    = str(round(rep_growth * 100, 1))
f3_ce24      = f"{ce24:.2f}"
f3_ce25      = f"{ce25:.2f}"
f3_acc24     = f"{accrual24*100:.2f}"
f3_acc25     = f"{accrual25*100:.2f}"

rf1, rf2, rf3 = st.columns(3)

with rf1:
    st.markdown(
        "<div class='flag-card'>"
        "<div class='flag-title'>&#128308; Flag 1: SBC Burden</div>"
        "<div class='flag-body'>"
        "SBC consumes <span class='hl-red'>"+f1_sbc_pct25+"%</span> of Net Income in FY2025 "
        "(FY24: "+f1_sbc_pct24+"%). "
        "Adjusted NI = <span class='hl-amb'>$"+f1_adj_ni25+"M</span> vs "
        "reported $"+f1_ni25+"M. "
        "Net income overstated by <span class='hl-red'>"+f1_overstate+"%</span>."
        "</div></div>", unsafe_allow_html=True)

with rf2:
    st.markdown(
        "<div class='flag-card'>"
        "<div class='flag-title'>&#9888; Flag 2: AR Growing Faster Than Revenue</div>"
        "<div class='flag-body'>"
        "Accounts Receivable jumped <span class='hl-red'>"+f2_ar_growth+"%</span> YoY "
        "($"+f2_ar24+"M to $"+f2_ar25+"M) while revenue grew only "
        "<span class='hl-amb'>"+f2_rep_gr+"%</span>. "
        "Signals aggressive revenue recognition before cash is collected."
        "</div></div>", unsafe_allow_html=True)

with rf3:
    st.markdown(
        "<div class='flag-card'>"
        "<div class='flag-title'>&#9888; Flag 3: Declining Cash Quality</div>"
        "<div class='flag-body'>"
        "Cash-to-Earnings fell from <span class='hl-amb'>"+f3_ce24+"x</span> to "
        "<span class='hl-red'>"+f3_ce25+"x</span>. "
        "Accrual ratio worsening ("+f3_acc24+"% to "+f3_acc25+"%). "
        "Earnings growing <span class='hl-red'>faster</span> than cash confirms "
        "accruals-driven income inflation."
        "</div></div>", unsafe_allow_html=True)

# ── Q8.2 VALUATION ────────────────────────────────────────────────────────────
st.markdown("<div class='shdr'>Q8.2 &middot; Short-Seller Analysis &mdash; Organic Growth, P/E &amp; Fair Value</div>",
            unsafe_allow_html=True)
vl, vr = st.columns([1, 1.15])

with vl:
    val_rows_data = [
        ("Reported Revenue Growth",                            f"{rep_growth*100:.1f}%",                          "amber"),
        ("Organic Growth (ex-$"+str(acq_rev)+"M acquired)",   f"{org_growth*100:.1f}%",                          "green"),
        ("Acquisition Growth Inflation",                       "+"+f"{(rep_growth-org_growth)*100:.1f}"+"pp",     "red"),
        ("EPS Reported FY25",                                  "$"+f"{eps25:.2f}",                                "blue"),
        ("EPS SBC-Adjusted FY25",                             "$"+f"{adj_eps25:.2f}",                             "red"),
        ("Reported P/E  (FY24 / FY25)",                       f"{rep_pe24:.1f}"+"x / "+f"{rep_pe25:.1f}"+"x",   "blue"),
        ("SBC-Adjusted P/E  (FY24 / FY25)",                   f"{adj_pe24:.1f}"+"x / "+f"{adj_pe25:.1f}"+"x",   "red"),
        ("Enterprise Value FY25",                             "$"+f"{ev25:,.0f}"+"M",                             "blue"),
        ("EV / FCFF  (Actual)",                               f"{ev_fcff25:.1f}"+"x",                             "red"),
        ("Justified EV/FCFF  ("+str(just_m)+"x)",            str(just_m)+"x",                                    "green"),
        ("Implied EV",                                        "$"+f"{impl_ev:,.0f}"+"M",                          "amber"),
        ("Net Debt FY25",                                     "$"+f"{net_debt25:,.0f}"+"M",                       "blue"),
        ("Implied Equity Value",                              "$"+f"{impl_equity:,.0f}"+"M",                      "green"),
        ("Implied Fair Value / Share",                        "$"+f"{impl_px:.2f}",                               "green"),
        ("Current Share Price",                               "$"+f"{px25:.2f}",                                  "red"),
        ("Overvaluation Premium",                             f"{overval*100:.1f}"+"%",                           "red"),
    ]
    bold_set = {"Implied Fair Value / Share","Current Share Price","Overvaluation Premium"}
    v_rows_html = ""
    for lbl, val, clr in val_rows_data:
        bld = "font-weight:700;font-size:0.86rem;" if lbl in bold_set else ""
        v_rows_html += (
            "<tr><td>"+lbl+"</td>"
            "<td class='r "+clr+"' style='"+bld+"'>"+val+"</td></tr>"
        )
    st.markdown(
        "<table class='ftb'><thead><tr>"
        "<th>Item</th><th class='r'>Value</th>"
        "</tr></thead><tbody>"+v_rows_html+"</tbody></table>",
        unsafe_allow_html=True)

with vr:
    gauge_max = max(px25 * 1.4, impl_px * 2.0)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=px25,
        delta={"reference": impl_px, "valueformat": ".2f",
               "increasing":{"color":"#ff4c4c"}, "decreasing":{"color":"#4ce87a"}},
        number={"prefix":"$","valueformat":".2f","font":{"color":"#00c9ff","size":34}},
        title={"text":"Price vs Fair Value  |  Fair val: $"+f"{impl_px:.2f}",
               "font":{"color":"#8bb8d4","size":12}},
        gauge={
            "axis":{"range":[0, gauge_max],"tickcolor":"#4a6070",
                    "tickfont":{"color":"#6a8ba0","size":10}},
            "bar":{"color":"#ff4c4c","thickness":0.22},
            "bgcolor":"#0d1b2a","borderwidth":0,
            "steps":[{"range":[0, impl_px],"color":"#0d3320"},
                     {"range":[impl_px, px25],"color":"#2a0d0d"}],
            "threshold":{"line":{"color":"#4ce87a","width":3},
                         "thickness":0.75,"value":impl_px},
        },
    ))
    fig_gauge.update_layout(
        paper_bgcolor="#0d1b2a", font_color="#8bb8d4",
        height=240, margin=dict(l=30,r=30,t=60,b=10)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    pe_x      = ["Rep P/E FY24","Adj P/E FY24","Rep P/E FY25","Adj P/E FY25","EV/FCFF Act","EV/FCFF Just"]
    pe_y      = [rep_pe24, adj_pe24, rep_pe25, adj_pe25, ev_fcff25, float(just_m)]
    pe_colors = ["#00c9ff","#ff4c4c","#00c9ff","#ff4c4c","#ff4c4c","#4ce87a"]
    fig_pe = go.Figure(go.Bar(
        x=pe_x, y=pe_y, marker_color=pe_colors,
        text=[f"{v:.1f}"+"x" for v in pe_y],
        textposition="outside", textfont=dict(size=10),
    ))
    fig_pe.update_layout(
        template="vt",
        title=dict(text="Valuation Multiples vs Justified Benchmark",
                   font=dict(color="#00c9ff",size=13), x=0.02),
        height=270, showlegend=False,
        yaxis=dict(range=[0, max(pe_y)*1.28]),
    )
    st.plotly_chart(fig_pe, use_container_width=True)

# ── REVENUE BRIDGE + DONUT ────────────────────────────────────────────────────
st.markdown("<div class='shdr'>Revenue Bridge &amp; Earnings Composition</div>",
            unsafe_allow_html=True)
rb1, rb2 = st.columns([1.3, 1])

with rb1:
    bridge_x = [
        "FY2024 Revenue",
        "Organic +$"+f"{org_add:,.0f}"+"M",
        "Acquired +$"+f"{acq_rev:,.0f}"+"M",
        "FY2025 Revenue",
    ]
    bridge_y   = [rev24, org_add, acq_rev, 0]
    bridge_ms  = ["absolute","relative","relative","total"]
    bridge_txt = [
        "$"+f"{rev24:,.0f}"+"M",
        "+$"+f"{org_add:,.0f}"+"M ("+f"{org_growth*100:.1f}"+"%)",
        "+$"+f"{acq_rev:,.0f}"+"M (inorganic)",
        "$"+f"{rev25:,.0f}"+"M",
    ]
    fig_bridge = go.Figure(go.Waterfall(
        orientation="v", measure=bridge_ms, x=bridge_x,
        y=bridge_y, text=bridge_txt,
        textposition="outside", textfont=dict(size=10, color="#d0e8f0"),
        connector={"line":{"color":"#1e3a5f","dash":"dot","width":1}},
        increasing={"marker":{"color":"#4ce87a","line":{"color":"#4ce87a","width":0}}},
        totals={"marker":{"color":"#00c9ff","line":{"color":"#00c9ff","width":0}}},
    ))
    fig_bridge.update_layout(
        template="vt",
        title=dict(
            text="Rev Bridge: Reported "+f"{rep_growth*100:.1f}"+"% vs Organic "+f"{org_growth*100:.1f}"+"%",
            font=dict(color="#00c9ff",size=13), x=0.02),
        height=320, showlegend=False,
    )
    st.plotly_chart(fig_bridge, use_container_width=True)

with rb2:
    other_costs = (rev25 - ni25) - sbc25
    fig_donut = go.Figure(go.Pie(
        labels=["SBC (Non-cash cost)","Adj Net Income","All Other Costs"],
        values=[sbc25, adj_ni25, other_costs],
        hole=0.56, pull=[0.04, 0, 0],
        marker_colors=["#ff4c4c","#4ce87a","#1e3a5f"],
        textinfo="label+percent",
        textfont=dict(size=10, color="#d0e8f0"),
        insidetextorientation="radial",
    ))
    fig_donut.update_layout(
        paper_bgcolor="#0d1b2a", font_color="#8bb8d4",
        title=dict(text="FY2025 Revenue Decomposition",
                   font=dict(color="#00c9ff",size=13), x=0.02),
        legend=dict(bgcolor="#0d1b2a", font=dict(color="#8bb8d4",size=10),
                    orientation="h", y=-0.12),
        height=320, margin=dict(l=20,r=20,t=60,b=40),
        annotations=[dict(
            text="$"+f"{rev25/1000:.1f}"+"B<br>Rev",
            x=0.5, y=0.5, font_size=13, showarrow=False, font_color="#00c9ff"
        )]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ── VERDICT ───────────────────────────────────────────────────────────────────
v_sbc    = str(round(sbc_pct25*100))
v_adjni  = f"{adj_ni25:,.0f}"
v_ni     = f"{ni25:,.0f}"
v_over   = str(round(ni_overstate))
v_org    = f"{org_growth*100:.1f}"
v_rep    = f"{rep_growth*100:.1f}"
v_gap    = f"{(rep_growth-org_growth)*100:.1f}"
v_adjpe  = f"{adj_pe25:.1f}"
v_reppe  = f"{rep_pe25:.1f}"
v_fv     = f"{impl_px:.2f}"
v_ov     = f"{overval*100:.1f}"
v_px     = f"{px25:.2f}"
v_jm     = str(just_m)

st.markdown(
    "<div class='verdict'>"
    "<div class='vt'>&#128308; ANALYST VERDICT &mdash; SHORT-SELLER THESIS CONFIRMED</div>"
    "<div class='vb'>"
    "VelocityTech's reported earnings materially overstate economic performance. "
    "SBC consumes <strong style='color:#ff4c4c;'>"+v_sbc+"%</strong> of net income &mdash; "
    "real adjusted earnings are just <strong style='color:#f5a623;'>$"+v_adjni+"M</strong> "
    "vs reported $"+v_ni+"M (overstated by <strong style='color:#ff4c4c;'>"+v_over+"%</strong>). "
    "Organic growth of <strong style='color:#f5a623;'>"+v_org+"%</strong> is far below "
    "headline <strong style='color:#ff4c4c;'>"+v_rep+"%</strong> &mdash; "
    "the "+v_gap+"pp gap is entirely acquisition-driven. "
    "SBC-adjusted P/E of <strong style='color:#ff4c4c;'>"+v_adjpe+"x</strong> "
    "is nearly double the reported "+v_reppe+"x. "
    "At a justified EV/FCFF of "+v_jm+"x, implied fair value is "
    "<strong style='color:#4ce87a;'>$"+v_fv+" per share</strong> &mdash; "
    "<strong style='color:#ff4c4c;'>"+v_ov+"% below the market price of $"+v_px+".</strong>"
    "</div></div>",
    unsafe_allow_html=True
)
