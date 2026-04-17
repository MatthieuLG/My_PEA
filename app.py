import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="PEA · Dashboard",
    page_icon="▸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS — injected via components.html script into parent document head
# ══════════════════════════════════════════════════════════════════════════════
components.html("""
<script>
// Force remove top gap immediately and on every render
function removeTopGap() {
    const parent = window.parent.document;
    // Kill the header
    const header = parent.querySelector('[data-testid="stHeader"]');
    if (header) { header.style.cssText = 'display:none!important;height:0!important;min-height:0!important;'; }
    // Kill decoration
    const deco = parent.querySelector('[data-testid="stDecoration"]');
    if (deco) { deco.style.cssText = 'display:none!important;height:0!important;'; }
    // Kill top padding on main container
    const blocks = parent.querySelectorAll('.block-container, [data-testid="stAppViewBlockContainer"], .stMainBlockContainer');
    blocks.forEach(b => { b.style.paddingTop = '0px'; b.style.marginTop = '0px'; });
    // Kill the iframe gap itself
    const iframes = parent.querySelectorAll('iframe');
    iframes.forEach(f => { if(f.height==='0'||f.offsetHeight===0) f.style.cssText='height:0!important;min-height:0!important;max-height:0!important;display:block!important;margin:0!important;padding:0!important;overflow:hidden!important;'; });
}
removeTopGap();
setTimeout(removeTopGap, 100);
setTimeout(removeTopGap, 500);

const css = `
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500&display=swap');
:root{
  --bg:#07090f;--s1:#0c0f1a;--s2:#111827;--s3:#1a2235;
  --border:#1e2a3a;--b2:#26344a;
  --green:#22c55e;--red:#ef4444;--amber:#f59e0b;--blue:#3b82f6;
  --green-bg:rgba(34,197,94,0.07);--red-bg:rgba(239,68,68,0.07);
  --amber-bg:rgba(245,158,11,0.07);--blue-bg:rgba(59,130,246,0.07);
  --text:#f1f5f9;--t2:#94a3b8;--t3:#475569;
}
*{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Outfit',sans-serif!important;font-size:15px!important;}
.main .block-container{padding:0.1rem 2rem 3rem!important;max-width:1560px!important;}
.stApp{background:var(--bg)!important;}
section[data-testid="stSidebar"]{background:var(--s1)!important;border-right:1px solid var(--border)!important;}
section[data-testid="stSidebar"] .block-container{padding:1.25rem 1rem!important;}
#MainMenu,footer,header{visibility:hidden!important;}
.stDeployButton{display:none!important;}

/* ── Remove ALL Streamlit top padding ── */
.block-container{padding-top:0!important;margin-top:0!important;}
[data-testid="stHeader"]{display:none!important;height:0!important;min-height:0!important;}
div[data-testid="stDecoration"]{display:none!important;height:0!important;}
[data-testid="stAppViewBlockContainer"]{padding-top:0!important;}
.stMainBlockContainer{padding-top:0!important;}
.main > div{padding-top:0!important;}
iframe[height="0"]{height:0!important;min-height:0!important;max-height:0!important;
  display:block!important;margin:0!important;padding:0!important;border:none!important;overflow:hidden!important;}
div[data-testid="stCustomComponentV1"]{height:0!important;min-height:0!important;overflow:hidden!important;margin:0!important;}

/* ── Sidebar ── */
.nav-logo{font-family:'Outfit',sans-serif;font-weight:800;font-size:1.1rem;color:var(--text);
  letter-spacing:-0.02em;padding-bottom:1.1rem;border-bottom:1px solid var(--border);
  margin-bottom:1.2rem;display:flex;align-items:center;gap:10px;}
.nav-logo .dot{width:8px;height:8px;border-radius:50%;background:var(--green);
  box-shadow:0 0 8px var(--green);flex-shrink:0;}
.nav-logo .sub{font-size:0.58rem;color:var(--t3);font-weight:400;letter-spacing:0.12em;
  text-transform:uppercase;display:block;margin-top:2px;}

/* ── Nav items (radio styled as sidebar menu) ── */
.stRadio>div{gap:2px!important;}
.stRadio>div>label{
  font-family:'Outfit',sans-serif!important;font-size:0.82rem!important;font-weight:500!important;
  color:var(--t2)!important;padding:9px 12px!important;border-radius:8px!important;
  border:none!important;transition:all .15s!important;cursor:pointer!important;width:100%!important;}
.stRadio>div>label:hover{color:var(--text)!important;background:var(--s2)!important;}
/* Hide only the radio circle svg/input, keep the text */
.stRadio>div>label>div:first-child{display:none!important;}
.stRadio>div>label p{
  margin:0!important;font-family:'Outfit',sans-serif!important;
  font-size:0.82rem!important;font-weight:500!important;color:inherit!important;}

.nav-section{font-family:'DM Mono',monospace;font-size:0.55rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.14em;margin:1.4rem 0 0.5rem;opacity:0.7;}
.nav-divider{height:1px;background:var(--border);margin:1.2rem 0;}

.file-pill{font-family:'DM Mono',monospace;font-size:0.6rem;color:var(--t3);
  padding:2px 0;display:flex;align-items:center;gap:6px;opacity:0.75;}
.file-pill::before{content:'·';color:var(--green);font-size:0.8rem;}

.stButton>button{font-family:'DM Mono',monospace!important;font-size:0.7rem!important;
  color:var(--t3)!important;background:transparent!important;border:1px solid var(--border)!important;
  border-radius:7px!important;padding:6px 12px!important;width:100%;transition:all .15s;}
.stButton>button:hover{color:var(--text)!important;border-color:var(--b2)!important;
  background:var(--s2)!important;}

/* ── Page header ── */
.ph{margin-bottom:1.6rem;padding-top:0;}
.ph-title{font-family:'Outfit',sans-serif;font-weight:800;font-size:2rem;
  color:var(--text);letter-spacing:-0.03em;line-height:1;margin-bottom:5px;}
.ph-sub{font-family:'DM Mono',monospace;font-size:0.68rem;color:var(--t3);
  letter-spacing:0.12em;text-transform:uppercase;}

/* ── KPI cards ── */
.kpi-row{display:grid;grid-template-columns:repeat(5,1fr);gap:11px;margin-bottom:1.8rem;}
.kpi{background:var(--s1);border:1px solid var(--border);border-radius:11px;
  padding:18px 20px;position:relative;overflow:hidden;}
.kpi-top{height:2px;position:absolute;top:0;left:0;right:0;}
.kpi-lbl{font-family:'DM Mono',monospace;font-size:0.62rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;}
.kpi-val{font-family:'Outfit',sans-serif;font-size:1.65rem;font-weight:700;
  color:var(--text);line-height:1;margin-bottom:6px;}
.kpi-d{font-family:'DM Mono',monospace;font-size:0.72rem;}
.kpi-d.g{color:var(--green);}.kpi-d.r{color:var(--red);}.kpi-d.n{color:var(--t3);}

/* ── Section label ── */
.sl{font-family:'DM Mono',monospace;font-size:0.63rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.14em;margin:1.8rem 0 1rem;
  display:flex;align-items:center;gap:10px;}
.sl::after{content:'';flex:1;height:1px;background:var(--border);}

/* ── Perf cards ── */
.perf-row{display:grid;gap:8px;margin-bottom:1.6rem;}
.perf-c{background:var(--s1);border:1px solid var(--border);border-radius:9px;
  padding:15px 12px;text-align:center;}
.perf-c.hl{border-color:var(--amber);background:var(--amber-bg);}
.perf-lbl{font-family:'DM Mono',monospace;font-size:0.6rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;}
.perf-lbl.h{color:var(--amber);}
.perf-v{font-family:'Outfit',sans-serif;font-size:1.3rem;font-weight:700;line-height:1;}
.perf-abs{font-family:'DM Mono',monospace;font-size:0.63rem;margin-top:4px;}

/* ── Positions table ── */
.ptable{width:100%;border-collapse:collapse;}
.ptable th{font-family:'DM Mono',monospace;font-size:0.6rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.08em;padding:10px 14px;text-align:right;
  border-bottom:1px solid var(--border);background:var(--s2);}
.ptable th:first-child{text-align:left;}
.ptable td{font-family:'Outfit',sans-serif;font-size:0.88rem;color:var(--t2);
  padding:12px 14px;text-align:right;border-bottom:1px solid var(--border);}
.ptable td:first-child{text-align:left;color:var(--text);font-weight:500;}
.ptable tr:hover td{background:var(--s2);}
.tbadge{font-family:'DM Mono',monospace;font-size:0.62rem;color:var(--blue);
  background:var(--blue-bg);border:1px solid rgba(59,130,246,0.2);
  padding:2px 6px;border-radius:3px;margin-left:8px;}
.pos{color:var(--green)!important;font-weight:600;}
.neg{color:var(--red)!important;font-weight:600;}

/* ── Date inputs ── */
.stDateInput input{background:var(--s2)!important;border:1px solid var(--border)!important;
  color:var(--text)!important;font-family:'DM Mono',monospace!important;
  font-size:0.75rem!important;border-radius:6px!important;}

/* ── Ticker input ── */
.stTextInput input{background:var(--s1)!important;border:1px solid var(--border)!important;
  color:var(--text)!important;font-family:'DM Mono',monospace!important;
  font-size:0.95rem!important;border-radius:9px!important;padding:12px 16px!important;
  letter-spacing:0.04em!important;}
.stTextInput input:focus{border-color:var(--green)!important;
  box-shadow:0 0 0 2px rgba(34,197,94,0.12)!important;}
.stTextInput input::placeholder{color:var(--t3)!important;}

/* ── Period pills (Page 2 chart) ── */
.period-bar{display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap;}
.period-pill{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--t2);
  background:var(--s1);border:1px solid var(--border);border-radius:5px;
  padding:5px 11px;cursor:pointer;transition:all .15s;user-select:none;}
.period-pill:hover{border-color:var(--b2);color:var(--text);}
.period-pill.active{background:var(--s2);border-color:var(--green);color:var(--green);}

/* ── Stock perf strip (Page 2) ── */
.stock-perf-strip{display:flex;gap:8px;margin:10px 0 16px;flex-wrap:wrap;}
.sp-item{background:var(--s1);border:1px solid var(--border);border-radius:7px;
  padding:8px 14px;text-align:center;flex:1;min-width:80px;}
.sp-lbl{font-family:'DM Mono',monospace;font-size:0.57rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;}
.sp-val{font-family:'Outfit',sans-serif;font-size:0.95rem;font-weight:700;}

/* ── Criteria rows ── */
.cr{display:flex;align-items:center;padding:13px 17px;border-radius:9px;
  margin:5px 0;border:1px solid transparent;gap:13px;position:relative;}
.cr.g{background:var(--green-bg);border-color:rgba(34,197,94,0.25);}
.cr.r{background:var(--red-bg);border-color:rgba(239,68,68,0.25);}
.cr.y{background:var(--amber-bg);border-color:rgba(245,158,11,0.25);}
.cr.n{background:var(--s1);border-color:var(--border);}
.cr-badge{width:28px;height:28px;border-radius:7px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;}
.cr-badge.g{background:rgba(34,197,94,0.15);color:var(--green);}
.cr-badge.r{background:rgba(239,68,68,0.15);color:var(--red);}
.cr-badge.y{background:rgba(245,158,11,0.15);color:var(--amber);}
.cr-badge.n{background:var(--s2);color:var(--t3);}
.cr-num{font-family:'DM Mono',monospace;font-size:0.6rem;color:var(--t3);width:18px;flex-shrink:0;}
.cr-name{font-family:'Outfit',sans-serif;font-size:0.88rem;color:var(--text);font-weight:500;flex:1;}
.cr-val{font-family:'DM Mono',monospace;font-size:0.83rem;font-weight:500;width:95px;text-align:right;}
.cr-val.g{color:var(--green);}.cr-val.r{color:var(--red);}
.cr-val.y{color:var(--amber);}.cr-val.n{color:var(--t3);}
.cr-thresh{font-family:'DM Mono',monospace;font-size:0.58rem;color:var(--t3);
  width:135px;text-align:right;line-height:1.8;}
.cr-thresh .tg{color:rgba(34,197,94,0.65);}.cr-thresh .tr{color:rgba(239,68,68,0.65);}
.cr-tip{position:relative;display:flex;align-items:center;flex:1;gap:8px;}
.tip-icon{font-family:'DM Mono',monospace;font-size:0.55rem;color:var(--t3);
  background:var(--s2);border:1px solid var(--border);border-radius:3px;
  padding:1px 5px;cursor:help;flex-shrink:0;}
.tip-box{display:none;position:absolute;left:0;top:calc(100% + 6px);z-index:9999;
  background:var(--s2);border:1px solid var(--b2);border-radius:9px;
  padding:11px 14px;width:290px;box-shadow:0 10px 28px rgba(0,0,0,0.65);}
.tip-t{font-family:'Outfit',sans-serif;font-size:0.78rem;font-weight:600;
  color:var(--text);margin-bottom:6px;}
.tip-d{font-family:'Outfit',sans-serif;font-size:0.74rem;color:var(--t2);line-height:1.6;}
.cr-tip:hover .tip-box{display:block;}

/* ── Score ── */
.score-card{background:var(--s1);border:1px solid var(--border);border-radius:13px;
  padding:26px 22px;text-align:center;}
.score-lbl{font-family:'DM Mono',monospace;font-size:0.63rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.1em;margin-bottom:9px;}
.score-num{font-family:'Outfit',sans-serif;font-size:3.8rem;font-weight:800;line-height:1;}
.score-verdict{font-family:'DM Mono',monospace;font-size:0.68rem;font-weight:500;
  letter-spacing:0.1em;margin-top:3px;}
.score-bar-bg{background:var(--s2);border-radius:3px;height:5px;overflow:hidden;margin:14px 0 12px;}
.score-bar{height:5px;border-radius:3px;}

/* ── Score counts pill strip ── */
.score-counts{display:flex;gap:7px;justify-content:center;flex-wrap:wrap;margin-top:8px;}
.sc-pill{font-family:'DM Mono',monospace;font-size:0.65rem;font-weight:500;
  padding:4px 10px;border-radius:5px;border:1px solid transparent;}
.sc-pill.g{background:rgba(34,197,94,0.12);border-color:rgba(34,197,94,0.3);color:var(--green);}
.sc-pill.r{background:rgba(239,68,68,0.12);border-color:rgba(239,68,68,0.3);color:var(--red);}
.sc-pill.y{background:rgba(245,158,11,0.12);border-color:rgba(245,158,11,0.3);color:var(--amber);}
.sc-pill.n{background:var(--s2);border-color:var(--border);color:var(--t3);}

.score-w{font-family:'DM Mono',monospace;font-size:0.6rem;color:var(--t3);line-height:2;
  margin-top:14px;border-top:1px solid var(--border);padding-top:13px;text-align:left;}
.score-w span{color:var(--t2);}

/* ── Legend ── */
.legend-strip{display:flex;gap:14px;margin-bottom:1rem;flex-wrap:wrap;}
.legend-item{display:flex;align-items:center;gap:6px;
  font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--t2);}
.legend-dot{width:9px;height:9px;border-radius:2px;}

/* ── Company header ── */
.company-header{background:var(--s1);border:1px solid var(--border);border-radius:13px;
  padding:22px 26px;margin-bottom:1.5rem;display:flex;align-items:center;gap:30px;flex-wrap:wrap;}
.company-name{font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:700;color:var(--text);}
.company-ticker{font-family:'DM Mono',monospace;font-size:0.7rem;color:var(--green);
  letter-spacing:0.1em;margin-top:4px;}
.company-meta{display:flex;gap:26px;margin-left:auto;align-items:center;flex-wrap:wrap;}
.meta-lbl{font-family:'DM Mono',monospace;font-size:0.58rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;}
.meta-val{font-family:'Outfit',sans-serif;font-size:0.88rem;color:var(--t2);}
.price-box{background:var(--s2);border:1px solid var(--b2);border-radius:9px;
  padding:12px 20px;text-align:center;}
.price-lbl{font-family:'DM Mono',monospace;font-size:0.57rem;color:var(--t3);
  letter-spacing:0.08em;margin-bottom:3px;}
.price-val{font-family:'Outfit',sans-serif;font-size:1.4rem;font-weight:700;color:var(--green);}

/* ── Empty state ── */
.empty-state{background:var(--s1);border:1px solid var(--border);border-radius:13px;
  padding:60px 24px;text-align:center;margin-top:1.5rem;}
.empty-icon{font-size:2.2rem;color:var(--t3);margin-bottom:12px;}
.empty-title{font-family:'Outfit',sans-serif;font-size:1.05rem;font-weight:600;
  color:var(--t2);margin-bottom:7px;}
.empty-sub{font-family:'DM Mono',monospace;font-size:0.68rem;color:var(--t3);line-height:2;}

/* ── Expanders ── */
.streamlit-expanderHeader{font-family:'DM Mono',monospace!important;
  font-size:0.68rem!important;color:var(--t3)!important;
  text-transform:uppercase!important;letter-spacing:0.1em!important;}
`;
const st=document.createElement('style');
st.textContent=css;
window.parent.document.head.appendChild(st);

// Global tooltip handler — works because components.html is NOT sanitized
(function setupTooltips(){
  function show(e){
    var tip=e.currentTarget.querySelector('.ftip');
    if(tip){tip.style.opacity='1';tip.style.visibility='visible';}
  }
  function hide(e){
    var tip=e.currentTarget.querySelector('.ftip');
    if(tip){tip.style.opacity='0';tip.style.visibility='hidden';}
  }
  function attach(){
    var P=window.parent.document;
    P.querySelectorAll('.has-ftip').forEach(function(el){
      if(!el._tipBound){
        el.addEventListener('mouseenter',show);
        el.addEventListener('mouseleave',hide);
        el._tipBound=true;
      }
    });
  }
  attach();
  setInterval(attach,800);
})();

// Sidebar radio active state — inject border-left on checked item
(function styleActiveNav(){
  function update(){
    var P=window.parent.document;
    // Only target the sidebar radio (first stRadio in sidebar)
    var sidebar=P.querySelector('[data-testid="stSidebar"]');
    if(!sidebar) return;
    var labels=sidebar.querySelectorAll('.stRadio label');
    labels.forEach(function(lbl){
      var inp=lbl.querySelector('input[type="radio"]');
      if(!inp) return;
      if(inp.checked){
        lbl.style.cssText='color:#f1f5f9!important;background:#111827!important;border-left:2px solid #22c55e!important;padding-left:11px!important;border-radius:8px!important;';
      } else {
        lbl.style.cssText='color:#94a3b8!important;background:transparent!important;border-left:none!important;padding-left:12px!important;border-radius:8px!important;';
      }
      if(!lbl._navBound){
        lbl.addEventListener('click',function(){setTimeout(update,80);});
        lbl._navBound=true;
      }
    });
  }
  update();
  setInterval(update,500);
})();
</script>
""", height=0, scrolling=False)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
HIST_PATH = "Historique.xlsx"
CORR_PATH = "Corrrespondance.xlsx"
VERS_PATH = "Versements.xlsx"

WEIGHTS = {1:15, 2:8, 3:15, 4:12, 5:6, 6:5, 7:12, 8:10, 9:7, 10:10}

DEFINITIONS = {
    1: ("Croissance du chiffre d'affaires",
        "Une entreprise dont le CA croît de +10%/an sur 5 ans conquiert des parts de marché. C'est le moteur principal d'une hausse durable du cours."),
    2: ("Rachat d'actions (Buyback)",
        "Quand une entreprise rachète ses propres actions, chaque titre restant représente une part plus grande des bénéfices futurs. Signal fort de confiance du management."),
    3: ("ROIC — Return On Invested Capital",
        "Mesure l'efficacité à transformer le capital investi en profit. Au-delà de 20%, l'entreprise crée beaucoup de valeur — signe d'un avantage concurrentiel durable (moat)."),
    4: ("Marge de Free Cash-Flow",
        "Part des ventes convertie en cash réel disponible. Une marge >20% indique un modèle rentable, autonome financièrement, capable de croître sans s'endetter."),
    5: ("Croissance du dividende (5 ans)",
        "Un dividende qui croît de +10%/an sur 5 ans révèle un modèle très rentable et une direction qui récompense ses actionnaires avec discipline."),
    6: ("Payout ratio",
        "Part du bénéfice distribuée en dividendes. En dessous de 60%, l'entreprise garde assez de cash pour investir. Un ratio >90% fragilise la durabilité du dividende."),
    7: ("Croissance du Free Cash-Flow (5 ans)",
        "Un FCF qui progresse chaque année montre que l'entreprise génère de plus en plus de ressources réelles — elle peut croître, racheter des actions ou verser des dividendes sans s'endetter."),
    8: ("Dette / EBITDA",
        "Nombre d'années de profits bruts nécessaires pour rembourser la dette. En dessous de 1.5x, l'entreprise peut absorber une crise. Au-delà de 5x, elle est vulnérable."),
    9: ("PER — Price Earnings Ratio",
        "Combien les investisseurs paient pour chaque euro de bénéfice. À comparer toujours à l'historique et aux pairs du secteur. Ni trop haut ni trop bas."),
    10: ("Momentum à 5, 10, 15 ans",
        "Une action qui surperforme régulièrement le MSCI World sur longue période confirme que le marché reconnaît la qualité du business de façon durable."),
}

P_COLORS = ["#22c55e","#f59e0b","#3b82f6","#ef4444","#8b5cf6","#06b6d4","#f97316","#84cc16"]

STOCK_PERIODS = [
    ("Jour",    "1d",  1),
    ("1 sem",   "5d",  7),
    ("1 mois",  "1mo", 30),
    ("3 mois",  "3mo", 91),
    ("6 mois",  "6mo", 182),
    ("1 an",    "1y",  365),
    ("5 ans",   "5y",  365*5),
    ("All Time","max", 365*30),
]

def plotly_base(height=350, yaxis_opts=None, bar=False):
    yax = dict(gridcolor="#1e2a3a", linecolor="#1e2a3a", zeroline=False)
    if yaxis_opts:
        yax.update(yaxis_opts)
    layout = dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(12,15,26,0.97)",
        font=dict(family="DM Mono, monospace", size=10, color="#475569"),
        margin=dict(l=12, r=12, t=30, b=12),
        height=height,
        xaxis=dict(gridcolor="#1e2a3a", linecolor="#1e2a3a", zeroline=False),
        yaxis=yax,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#1a2235", bordercolor="#26344a",
                        font=dict(family="DM Mono, monospace", size=11)),
    )
    if bar:
        layout["barmode"] = "group"
    return layout

# ══════════════════════════════════════════════════════════════════════════════
# DATA LAYER
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=300)
def load_data():
    df_hist = pd.read_excel(HIST_PATH, parse_dates=["Date"])
    df_corr = pd.read_excel(CORR_PATH)
    df_vers = pd.read_excel(VERS_PATH, parse_dates=["Date d'opération"])
    return df_hist, df_corr, df_vers

@st.cache_data(ttl=300)
def get_ticker_info(ticker):
    try: return yf.Ticker(ticker).info
    except: return {}

@st.cache_data(ttl=300)
def get_current_price(ticker):
    try: return yf.Ticker(ticker).fast_info.last_price
    except: return None

@st.cache_data(ttl=300)
def get_price_history_tk(ticker, start):
    try:
        h = yf.Ticker(ticker).history(start=start)["Close"].copy()
        h.index = h.index.tz_localize(None)
        return h
    except: return pd.Series(dtype=float)

@st.cache_data(ttl=300)
def get_stock_history(ticker, period, interval=None):
    """Fetch OHLCV for stock chart on page 2. Handles both tz-aware and naive indexes."""
    try:
        if interval is None:
            if period == "1d":   interval = "1m"
            elif period == "5d": interval = "5m"
            else:                interval = "1d"
        h = yf.Ticker(ticker).history(period=period, interval=interval)
        if h.empty: return pd.DataFrame()
        if h.index.tz is not None:
            h.index = h.index.tz_convert("Europe/Paris").tz_localize(None)
        return h
    except: return pd.DataFrame()

def compute_portfolio(df_hist, df_corr, df_vers):
    """PRU Moyen Pondéré — identique à Fortuneo."""
    corr = dict(zip(df_corr["Libelle_fortuneo"], df_corr["code_yfinance"]))
    pos = {}   # lib -> {qty, pru}

    # Sort: same date → achats d'abord, puis taxes, puis ventes
    def op_order(row):
        op = str(row["Opération"]).strip().lower()
        if "achat" in op: return 0
        if "taxe" in op:  return 1
        return 2
    df_sorted = df_hist.copy()
    df_sorted["_ord"] = df_sorted.apply(op_order, axis=1)
    df_sorted = df_sorted.sort_values(["Date","_ord"], kind="stable")

    for _, row in df_sorted.iterrows():
        lib = str(row["libellé"]).strip()
        op  = str(row["Opération"]).strip().lower()
        qty = float(row["Qté"])  if pd.notna(row["Qté"])  else 0
        net = float(row["Montant net"]) if pd.notna(row["Montant net"]) else 0
        if "achat" in op and qty > 0:
            cpu   = abs(net) / qty
            pos.setdefault(lib, {"qty": 0.0, "pru": 0.0})
            new_q = pos[lib]["qty"] + qty
            pos[lib]["pru"] = (pos[lib]["qty"] * pos[lib]["pru"] + qty * cpu) / new_q
            pos[lib]["qty"] = new_q
        elif "taxe" in op and lib in pos and pos[lib]["qty"] > 0:
            # Taxe = coût d'acquisition → inclus dans le PRU (comme Fortuneo)
            pos[lib]["pru"] += abs(net) / pos[lib]["qty"]
        elif "vente" in op and qty > 0:
            if lib in pos and pos[lib]["qty"] > 0:
                pos[lib]["qty"] = round(max(pos[lib]["qty"] - qty, 0.0), 8)
                # PRU inchangé sur vente

    rows = []
    total_val = total_invest = 0.0
    for lib, p in {k: v for k, v in pos.items() if v["qty"] > 0.001}.items():
        ticker  = corr.get(lib)
        info    = get_ticker_info(ticker) if ticker else {}
        cur_px  = get_current_price(ticker) if ticker else None
        cost    = p["pru"] * p["qty"]
        val_act = (cur_px * p["qty"]) if cur_px else cost
        pv      = val_act - cost
        pv_pct  = (pv / cost * 100) if cost > 0 else 0
        qt  = info.get("quoteType", "").upper()
        typ = "ETF" if qt in ("ETF", "MUTUALFUND") else "Action"
        rows.append({
            "Titre": lib, "Ticker": ticker or "N/A",
            "Type": typ,
            "Secteur": info.get("sector", "—"), "Pays": info.get("country", "—"),
            "Quantité": p["qty"],
            "PRU (€)": round(p["pru"], 3),
            "Cours": round(cur_px, 2) if cur_px else None,
            "Investi (€)": round(cost, 2),
            "Valeur (€)": round(val_act, 2),
            "+/- Value (€)": round(pv, 2),
            "+/- Value (%)": round(pv_pct, 2),
        })
        total_val    += val_act
        total_invest += cost

    df_pos = pd.DataFrame(rows)
    total_verse = float(df_vers["Crédit"].sum()) if "Crédit" in df_vers.columns else 0.0
    cash_flux   = sum(
        float(r["Montant net"]) if pd.notna(r["Montant net"]) else 0
        for _, r in df_hist.iterrows()
    )
    liquidites = max(total_verse + cash_flux, 0.0)
    total_pv   = total_val - total_invest
    return df_pos, {
        "total_investi": round(total_invest, 2),
        "total_valeur":  round(total_val, 2),
        "total_complet": round(total_val + liquidites, 2),
        "total_pv":      round(total_pv, 2),
        "total_pv_pct":  round((total_pv / total_invest * 100) if total_invest > 0 else 0, 2),
        "total_verse":   round(total_verse, 2),
        "liquidites":    round(liquidites, 2),
    }

def build_portfolio_history(df_hist, df_corr, df_vers):
    """Reconstruit la valeur journalière — PRU moyen pondéré."""
    corr = dict(zip(df_corr["Libelle_fortuneo"], df_corr["code_yfinance"]))
    if df_hist.empty: return pd.DataFrame()

    ops = []
    for _, row in df_hist.iterrows():
        lib  = str(row["libellé"]).strip()
        op   = str(row["Opération"]).strip().lower()
        qty  = float(row["Qté"])  if pd.notna(row["Qté"])  else 0
        net  = float(row["Montant net"]) if pd.notna(row["Montant net"]) else 0
        date = row["Date"]
        if "achat" in op and qty > 0:
            ops.append((date, 0, lib, "buy",  qty, abs(net)))
        elif "taxe" in op:
            ops.append((date, 1, lib, "taxe", 0.0, abs(net)))
        elif "vente" in op and qty > 0:
            ops.append((date, 2, lib, "sell", qty, 0.0))
    ops.sort(key=lambda x: (x[0], x[1]))

    all_tickers = {lib: corr[lib] for lib in {o[1] for o in ops} if lib in corr}
    start  = df_hist["Date"].min() - timedelta(days=3)
    dates  = pd.date_range(start, datetime.today(), freq="B")
    prices = {}
    for tk in all_tickers.values():
        s = get_price_history_tk(tk, start)
        if not s.empty: prices[tk] = s

    pos_d  = {}   # lib -> {qty, pru}
    op_idx = 0
    vals   = []
    for d in dates:
        while op_idx < len(ops) and ops[op_idx][0] <= d:
            _, _ord, lib, kind, qty, net = ops[op_idx]
            pos_d.setdefault(lib, {"qty": 0.0, "pru": 0.0})
            if kind == "buy":
                cpu   = net / qty if qty > 0 else 0
                new_q = pos_d[lib]["qty"] + qty
                pos_d[lib]["pru"] = (pos_d[lib]["qty"] * pos_d[lib]["pru"] + qty * cpu) / new_q if new_q > 0 else 0
                pos_d[lib]["qty"] = new_q
            elif kind == "sell":
                pos_d[lib]["qty"] = max(pos_d[lib]["qty"] - qty, 0.0)
            op_idx += 1

        val_d = inv_d = 0.0
        for lib, p in pos_d.items():
            if p["qty"] < 0.001: continue
            cost  = p["pru"] * p["qty"]
            tk    = corr.get(lib)
            inv_d += cost
            if tk and tk in prices:
                idx = prices[tk].index[prices[tk].index <= d]
                val_d += (prices[tk][idx[-1]] * p["qty"]) if len(idx) > 0 else cost
            else:
                val_d += cost

        vers_d  = float(df_vers[df_vers["Date d'opération"] <= d]["Crédit"].sum())
        cf_jour = float(df_vers[df_vers["Date d'opération"].dt.normalize() == d.normalize()]["Crédit"].sum())
        # Liquidités = versements cumulés + TOUS les flux historiques jusqu'à d
        # (achats négatifs + ventes positives + taxes négatives)
        cash_fx = float(df_hist[df_hist["Date"] <= d]["Montant net"].fillna(0).sum())
        liq_d   = max(vers_d + cash_fx, 0.0)
        vals.append({"Date": d, "Versements": vers_d, "Investi": inv_d,
                     "Valeur": val_d, "Complet": val_d + liq_d, "CF_externe": cf_jour})
    df_out = pd.DataFrame(vals)
    if "CF_externe" not in df_out.columns:
        df_out["CF_externe"] = 0.0
    return df_out

def calc_pure_perf(df_hist, df_corr):
    """
    Performance pure all-time : PnL réalisé + PnL latent / coût total investi.
    PRU moyen pondéré — identique à Fortuneo. Aucun biais dépôt/retrait.
    """
    corr = dict(zip(df_corr["Libelle_fortuneo"], df_corr["code_yfinance"]))
    pos      = {}   # lib -> {qty, pru}
    realized = {}   # lib -> {pnl, cost}

    def _op_ord(r):
        op = str(r["Opération"]).strip().lower()
        return 0 if "achat" in op else (1 if "taxe" in op else 2)
    df_s2 = df_hist.copy()
    df_s2["_o"] = df_s2.apply(_op_ord, axis=1)
    df_s2 = df_s2.sort_values(["Date","_o"], kind="stable")

    for _, row in df_s2.iterrows():
        lib = str(row["libellé"]).strip()
        op  = str(row["Opération"]).strip().lower()
        qty = float(row["Qté"])  if pd.notna(row["Qté"])  else 0
        net = float(row["Montant net"]) if pd.notna(row["Montant net"]) else 0
        if "achat" in op and qty > 0:
            cpu = abs(net) / qty
            pos.setdefault(lib, {"qty": 0.0, "pru": 0.0})
            realized.setdefault(lib, {"pnl": 0.0, "cost": 0.0})
            new_q = pos[lib]["qty"] + qty
            pos[lib]["pru"] = (pos[lib]["qty"] * pos[lib]["pru"] + qty * cpu) / new_q
            pos[lib]["qty"] = new_q
        elif "taxe" in op and lib in pos and pos[lib]["qty"] > 0:
            pos[lib]["pru"] += abs(net) / pos[lib]["qty"]
        elif "vente" in op and qty > 0:
            pos.setdefault(lib, {"qty": 0.0, "pru": 0.0})
            realized.setdefault(lib, {"pnl": 0.0, "cost": 0.0})
            qty_sell   = min(qty, pos[lib]["qty"])
            cost_basis = pos[lib]["pru"] * qty_sell
            realized[lib]["pnl"]  += net - cost_basis
            realized[lib]["cost"] += cost_basis
            pos[lib]["qty"] = max(pos[lib]["qty"] - qty_sell, 0.0)

    total_pnl = total_cost = 0.0
    for lib, p in pos.items():
        if p["qty"] < 0.001: continue
        open_cost = p["pru"] * p["qty"]
        ticker    = corr.get(lib)
        cur_px    = get_current_price(ticker) if ticker else None
        cur_val   = cur_px * p["qty"] if cur_px else open_cost
        total_pnl  += cur_val - open_cost
        total_cost += open_cost
    for lib, r in realized.items():
        total_pnl  += r["pnl"]
        total_cost += r["cost"]

    if total_cost <= 0: return None, None
    return total_pnl / total_cost * 100, total_pnl


def perf_between(df_hv, d_start, d_end):
    """
    Modified Dietz — performance pure hors dépôts externes.

    Formule : (V_fin - V_début - ΣCF) / (V_début + Σ(CF × poids))
    - V = Complet (positions au marché + liquidités)
    - CF = versements externes uniquement (pas les achats/ventes)
    - Retourne None si données insuffisantes ou période trop courte
    """
    if df_hv.empty or len(df_hv) < 2: return None, None

    d_start = pd.Timestamp(d_start).normalize()
    d_end   = pd.Timestamp(d_end).normalize()
    dn  = df_hv["Date"].dt.normalize()
    sub = df_hv[(dn >= d_start) & (dn <= d_end)].copy().reset_index(drop=True)
    if len(sub) < 2: return None, None

    val_col = "Complet" if "Complet" in sub.columns else "Valeur"
    cf_col  = "CF_externe" if "CF_externe" in sub.columns else None

    v0 = float(sub.iloc[0][val_col])
    v1 = float(sub.iloc[-1][val_col])

    # Pas assez de données significatives
    if v0 <= 0: return None, None

    n = len(sub)
    total_cf = weighted_cf = 0.0
    if cf_col:
        for i, row in sub.iterrows():
            cf = float(row[cf_col])
            if cf > 0.5 and i > 0:
                weight = (n - 1 - i) / (n - 1) if n > 1 else 0.5
                weighted_cf += cf * weight
                total_cf    += cf

    denom    = v0 + weighted_cf
    if denom <= 0: return None, None

    net_gain = v1 - v0 - total_cf
    pct      = net_gain / denom * 100

    return pct, net_gain

def calc_pure_perf(df_hist, df_corr):
    """
    Performance pure all-time : PnL réalisé + PnL latent / coût total investi.
    PRU moyen pondéré — identique à Fortuneo. Aucun biais dépôt/retrait.
    """
    corr = dict(zip(df_corr["Libelle_fortuneo"], df_corr["code_yfinance"]))
    pos      = {}   # lib -> {qty, pru}
    realized = {}   # lib -> {pnl, cost}

    def _op_ord(r):
        op = str(r["Opération"]).strip().lower()
        return 0 if "achat" in op else (1 if "taxe" in op else 2)
    df_s2 = df_hist.copy()
    df_s2["_o"] = df_s2.apply(_op_ord, axis=1)
    df_s2 = df_s2.sort_values(["Date","_o"], kind="stable")

    for _, row in df_s2.iterrows():
        lib = str(row["libellé"]).strip()
        op  = str(row["Opération"]).strip().lower()
        qty = float(row["Qté"])  if pd.notna(row["Qté"])  else 0
        net = float(row["Montant net"]) if pd.notna(row["Montant net"]) else 0
        if "achat" in op and qty > 0:
            cpu = abs(net) / qty
            pos.setdefault(lib, {"qty": 0.0, "pru": 0.0})
            realized.setdefault(lib, {"pnl": 0.0, "cost": 0.0})
            new_q = pos[lib]["qty"] + qty
            pos[lib]["pru"] = (pos[lib]["qty"] * pos[lib]["pru"] + qty * cpu) / new_q
            pos[lib]["qty"] = new_q
        elif "taxe" in op and lib in pos and pos[lib]["qty"] > 0:
            pos[lib]["pru"] += abs(net) / pos[lib]["qty"]
        elif "vente" in op and qty > 0:
            pos.setdefault(lib, {"qty": 0.0, "pru": 0.0})
            realized.setdefault(lib, {"pnl": 0.0, "cost": 0.0})
            qty_sell   = min(qty, pos[lib]["qty"])
            cost_basis = pos[lib]["pru"] * qty_sell
            realized[lib]["pnl"]  += net - cost_basis
            realized[lib]["cost"] += cost_basis
            pos[lib]["qty"] = max(pos[lib]["qty"] - qty_sell, 0.0)

    total_pnl = total_cost = 0.0
    for lib, p in pos.items():
        if p["qty"] < 0.001: continue
        open_cost = p["pru"] * p["qty"]
        ticker    = corr.get(lib)
        cur_px    = get_current_price(ticker) if ticker else None
        cur_val   = cur_px * p["qty"] if cur_px else open_cost
        total_pnl  += cur_val - open_cost
        total_cost += open_cost
    for lib, r in realized.items():
        total_pnl  += r["pnl"]
        total_cost += r["cost"]

    if total_cost <= 0: return None, None
    return total_pnl / total_cost * 100, total_pnl


def perf_between(df_hv, d_start, d_end):
    """
    Modified Dietz sur la valeur totale (positions + cash).

    - Exclut les dépôts du calcul : gain_net = V_fin - V_début - dépôts_période
    - Les dépôts du PREMIER jour sont exclus car déjà inclus dans v0
    - Dénominateur = V_début + dépôts × poids_temporel
    - Le montant en € = gain_net (euros réellement gagnés/perdus hors dépôts)
    - Signe toujours cohérent entre % et €
    - Retourne None si < 2 points de données dans la période
    """
    if df_hv.empty or len(df_hv) < 2: return None, None
    d_start = pd.Timestamp(d_start).normalize()
    d_end   = pd.Timestamp(d_end).normalize()
    dn  = df_hv["Date"].dt.normalize()
    sub = df_hv[(dn >= d_start) & (dn <= d_end)].copy().reset_index(drop=True)
    if len(sub) < 2: return None, None

    val_col = "Complet" if "Complet" in sub.columns else "Valeur"
    cf_col  = "CF_externe" if "CF_externe" in sub.columns else None

    v0 = float(sub.iloc[0][val_col])
    v1 = float(sub.iloc[-1][val_col])
    if v0 <= 0: return None, None

    n = len(sub)
    weighted_cf = 0.0
    total_cf    = 0.0
    if cf_col:
        for i, row in sub.iterrows():
            cf = float(row[cf_col])
            if cf > 0.5:
                if i == 0:
                    # Versement du premier jour : déjà capturé dans v0, on l'exclut
                    continue
                # Poids Modified Dietz : proportion de la période restante
                weight = (n - 1 - i) / (n - 1)
                weighted_cf += cf * weight
                total_cf    += cf

    denom    = v0 + weighted_cf
    net_gain = v1 - v0 - total_cf   # euros réels gagnés, hors dépôts

    if denom <= 0: return None, None
    pct = net_gain / denom * 100
    return pct, net_gain

def kpi_card(label, value, delta=None, dpos=None, top_color=None):
    top = f"background:{top_color}" if top_color else "background:var(--border)"
    d_html = ""
    if delta is not None:
        cls = "g" if dpos else ("r" if dpos is False else "n")
        d_html = f'<div class="kpi-d {cls}">{delta}</div>'
    return (f'<div class="kpi"><div class="kpi-top" style="{top}"></div>'
            f'<div class="kpi-lbl">{label}</div>'
            f'<div class="kpi-val">{value}</div>{d_html}</div>')

def section_label(txt):
    st.markdown(f'<div class="sl">{txt}</div>', unsafe_allow_html=True)

def fmt_eur(v):
    if v is None: return "—"
    return f"{v:,.0f} €".replace(","," ")

def safe_float(v):
    try: return float(v) if v is not None else None
    except: return None

def fmt_pct_safe(v):
    f = safe_float(v)
    return f"{f*100:.1f}%" if f is not None else "N/A"

def fmt_num(v, d=2):
    f = safe_float(v)
    return f"{f:.{d}f}" if f is not None else "N/A"

def perf_color(pct):
    return "#22c55e" if pct >= 0 else "#ef4444"

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — PORTEFEUILLE
# ══════════════════════════════════════════════════════════════════════════════
def page_portfolio():
    st.markdown('<div class="ph"><div class="ph-title">Portefeuille PEA</div>'
                '<div class="ph-sub">▸ Valorisation temps réel · Fortuneo</div></div>',
                unsafe_allow_html=True)

    try:
        df_hist, df_corr, df_vers = load_data()
    except Exception as e:
        st.error(f"Fichiers introuvables : {e}")
        st.info("Placez Historique.xlsx, Corrrespondance.xlsx et Versements.xlsx dans le même dossier.")
        return

    with st.spinner("Synchronisation des cours…"):
        df_pos, s = compute_portfolio(df_hist, df_corr, df_vers)
        df_hv     = build_portfolio_history(df_hist, df_corr, df_vers)

    # ── KPI ───────────────────────────────────────────────────────────────────
    pv_pos = s["total_pv"] >= 0
    g_top  = "linear-gradient(90deg,#22c55e,transparent)"
    r_top  = "linear-gradient(90deg,#ef4444,transparent)"
    a_top  = "linear-gradient(90deg,#f59e0b,transparent)"
    b_top  = "linear-gradient(90deg,#3b82f6,transparent)"

    # Valeur portefeuille = titres valorisés + liquidités
    val_totale   = s["total_valeur"] + s["liquidites"]
    gain_vs_vers = val_totale - s["total_verse"]
    pct_vs_vers  = (gain_vs_vers / s["total_verse"] * 100) if s["total_verse"] > 0 else 0
    gvv_pos      = gain_vs_vers >= 0
    pv_tot_pos   = s["total_pv"] >= 0
    cards = (
        kpi_card("Capital versé",      fmt_eur(s["total_verse"]),    top_color=a_top) +
        kpi_card("+/− Latente titres",
         f"{s['total_pv']:+,.0f} €",
         f"{s['total_pv_pct']:+.2f}% sur investi", pv_tot_pos,
         g_top if pv_tot_pos else r_top) +
        kpi_card("Liquidités dispo",   fmt_eur(s["liquidites"]),     top_color=a_top) +
        kpi_card("Valeur totale", fmt_eur(val_totale),
                f"{gain_vs_vers:+,.0f} €  ·  {pct_vs_vers:+.2f}% vs versé",
                gvv_pos, g_top if gvv_pos else r_top)
    )
    st.markdown(f'<div class="kpi-row" style="grid-template-columns:repeat(4,1fr)">{cards}</div>', unsafe_allow_html=True)

    # ── Sélecteur de période pour le graphique ───────────────────────────────
    d_min = df_hv["Date"].min().date() if not df_hv.empty else (datetime.today()-timedelta(days=365)).date()
    d_max = datetime.today().date()

    c1, c2, _ = st.columns([1, 1, 4])
    with c1: d_from = st.date_input("Depuis",   value=d_min, min_value=d_min, max_value=d_max, key="df")
    with c2: d_to   = st.date_input("Jusqu'à",  value=d_max, min_value=d_min, max_value=d_max, key="dt")

        # ── Graphique ─────────────────────────────────────────────────────────────
    section_label("Évolution du portefeuille")

    if not df_hv.empty:
        df_plot = df_hv[(df_hv["Date"]>=pd.Timestamp(d_from))&(df_hv["Date"]<=pd.Timestamp(d_to))]
        if df_plot.empty: df_plot = df_hv

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_plot["Date"], y=df_plot["Versements"],
            name="Versements cumulés", fill="tozeroy",
            line=dict(color="#1e2a3a", width=0), fillcolor="rgba(30,42,58,0.6)",
            hovertemplate="<b>Versements</b> · %{x|%d %b %Y}<br>%{y:,.0f} €<extra></extra>"))
        fig.add_trace(go.Scatter(x=df_plot["Date"], y=df_plot["Investi"],
            name="Capital investi", line=dict(color="#3b82f6", width=2.5),
            hovertemplate="<b>Capital investi</b> · %{x|%d %b %Y}<br>%{y:,.0f} €<extra></extra>"))
        fig.add_trace(go.Scatter(x=df_plot["Date"], y=df_plot["Valeur"],
            name="Valeur portefeuille", line=dict(color="#22c55e", width=2.5),
            hovertemplate="<b>Portefeuille</b> · %{x|%d %b %Y}<br>%{y:,.0f} €<extra></extra>"))
        fig.add_trace(go.Scatter(x=df_plot["Date"], y=df_plot["Complet"],
            name="Total + liquidités", line=dict(color="#f59e0b", width=1.8, dash="dash"),
            hovertemplate="<b>Total + cash</b> · %{x|%d %b %Y}<br>%{y:,.0f} €<extra></extra>"))

        # ── Annotations achat / vente ────────────────────────────────────────
        corr_d = dict(zip(df_corr["Libelle_fortuneo"], df_corr["code_yfinance"]))
        for _, row in df_hist.iterrows():
            op  = str(row.get("Opération","")).strip().lower()
            d_r = pd.Timestamp(row["Date"]).normalize()
            if d_r < pd.Timestamp(d_from) or d_r > pd.Timestamp(d_to):
                continue
            lib     = str(row.get("libellé","")).strip()
            tk_lbl  = corr_d.get(lib, lib)[:6]
            if "achat" in op:
                fig.add_vline(x=d_r, line_width=1, line_dash="dot",
                              line_color="rgba(34,197,94,0.35)")
                fig.add_annotation(x=d_r, y=1.0, yref="paper",
                    text=f"<b>▲</b> {tk_lbl}", showarrow=False,
                    font=dict(size=8, color="#22c55e", family="DM Mono"),
                    textangle=-90, xanchor="left", yanchor="top",
                    bgcolor="rgba(34,197,94,0.08)", borderpad=2)
            elif "vente" in op:
                fig.add_vline(x=d_r, line_width=1, line_dash="dot",
                              line_color="rgba(239,68,68,0.35)")
                fig.add_annotation(x=d_r, y=1.0, yref="paper",
                    text=f"<b>▼</b> {tk_lbl}", showarrow=False,
                    font=dict(size=8, color="#ef4444", family="DM Mono"),
                    textangle=-90, xanchor="left", yanchor="top",
                    bgcolor="rgba(239,68,68,0.08)", borderpad=2)

        fig.update_layout(**plotly_base(380, {"ticksuffix":" €","tickformat":",.0f"}))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Historique insuffisant pour tracer l'évolution.")

    # ── Positions ─────────────────────────────────────────────────────────────
    section_label("Positions ouvertes")

    if not df_pos.empty:
        rows_html = ""
        for _, r in df_pos.iterrows():
            pcls = "pos" if r["+/- Value (€)"] >= 0 else "neg"
            sg   = "+" if r["+/- Value (€)"] >= 0 else ""
            crs  = f"{r['Cours']:.2f} €" if r["Cours"] else "—"
            rows_html += (
                f'<tr><td>{r["Titre"]} <span class="tbadge">{r["Ticker"]}</span></td>'
                f'<td>{r["Quantité"]:.0f}</td><td>{r["PRU (€)"]:.3f} €</td><td>{crs}</td>'
                f'<td>{r["Investi (€)"]:,.2f} €</td><td>{r["Valeur (€)"]:,.2f} €</td>'
                f'<td class="{pcls}">{sg}{r["+/- Value (€)"]:,.2f} €</td>'
                f'<td class="{pcls}">{sg}{r["+/- Value (%)"]:.2f}%</td></tr>'
            )
        st.markdown(
            f'<div style="background:var(--s1);border:1px solid var(--border);'
            f'border-radius:11px;overflow:hidden;margin-bottom:1.5rem;">'
            f'<table class="ptable"><thead><tr>'
            f'<th style="text-align:left">Titre</th><th>Qté</th><th>PRU</th><th>Cours</th>'
            f'<th>Investi</th><th>Valeur</th><th>+/− €</th><th>+/− %</th>'
            f'</tr></thead><tbody>{rows_html}</tbody></table></div>',
            unsafe_allow_html=True)

        # ── 4 Répartitions ────────────────────────────────────────────────────
        section_label("Répartition")
        total_porto = df_pos["Valeur (€)"].sum()

        def make_pie(df_data, val_col, name_col, title, colors, show_pct_porto=False):
            """Build a donut pie. If show_pct_porto, show % of total portfolio."""
            pie_layout = plotly_base(320)
            pie_layout.update({
                "showlegend": True,
                "legend": {"font":{"size":8}, "bgcolor":"rgba(0,0,0,0)",
                           "orientation":"h","x":0.5,"xanchor":"center",
                           "y":-0.12,"yanchor":"top","traceorder":"normal"},
                "margin": {"l":8,"r":8,"t":28,"b":60},
                "title": {"text":title,"font":{"size":11,"color":"#94a3b8"},
                          "x":0,"xanchor":"left"},
            })
            if df_data.empty:
                return None
            # Add poids dans le portefeuille as custom data
            df_data = df_data.copy()
            df_data["poids"] = df_data[val_col] / total_porto * 100
            fig = px.pie(df_data, values=val_col, names=name_col, hole=0.52,
                         color_discrete_sequence=colors)
            if show_pct_porto:
                fig.update_traces(
                    textposition="inside", textinfo="percent",
                    customdata=df_data["poids"].values,
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "%{value:,.0f} €<br>"
                        "%{percent} du groupe<br>"
                        "<span style='color:#94a3b8'>%{customdata:.1f}% du portefeuille</span>"
                        "<extra></extra>"
                    )
                )
            else:
                fig.update_traces(
                    textposition="inside", textinfo="percent",
                    hovertemplate="<b>%{label}</b><br>%{value:,.0f} €<br>%{percent}<extra></extra>"
                )
            fig.update_layout(**pie_layout)
            return fig

        c1, c2, c3, c4 = st.columns(4)

        # Donut 1 : ETF vs Actions
        with c1:
            if "Type" in df_pos.columns:
                df_type = df_pos.groupby("Type")["Valeur (€)"].sum().reset_index()
                f1 = make_pie(df_type, "Valeur (€)", "Type",
                              "ETF vs Actions",
                              ["#3b82f6","#22c55e"])
                if f1: st.plotly_chart(f1, use_container_width=True)

        # Donut 2 : ETFs (avec poids dans le portefeuille)
        with c2:
            df_etf = df_pos[df_pos.get("Type","Action") == "ETF"] if "Type" in df_pos.columns else df_pos[df_pos["Ticker"].str.contains("ETF|UCITS|Acc", case=False, na=False)]
            if not df_etf.empty:
                # Shorten title for display
                df_etf2 = df_etf[["Titre","Valeur (€)"]].copy()
                df_etf2["Label"] = df_etf2["Titre"].apply(
                    lambda x: x[:22]+"…" if len(x)>22 else x)
                f2 = make_pie(df_etf2, "Valeur (€)", "Label",
                              "Répartition ETFs",
                              P_COLORS[2:]+P_COLORS[:2], show_pct_porto=True)
                if f2: st.plotly_chart(f2, use_container_width=True)
            else:
                st.caption("Aucun ETF détecté")

        # Donut 3 : Actions (avec poids dans le portefeuille)
        with c3:
            df_act = df_pos[df_pos.get("Type","ETF") == "Action"] if "Type" in df_pos.columns else df_pos
            if not df_act.empty:
                df_act2 = df_act[["Titre","Valeur (€)"]].copy()
                df_act2["Label"] = df_act2["Titre"].apply(
                    lambda x: x[:20]+"…" if len(x)>20 else x)
                f3 = make_pie(df_act2, "Valeur (€)", "Label",
                              "Répartition Actions",
                              [P_COLORS[3]]+P_COLORS[4:]+P_COLORS[:3], show_pct_porto=True)
                if f3: st.plotly_chart(f3, use_container_width=True)
            else:
                st.caption("Aucune action détectée")

        # Donut 4 : Secteurs
        with c4:
            df_sec = df_pos.groupby("Secteur")["Valeur (€)"].sum().reset_index()
            df_sec = df_sec[df_sec["Secteur"] != "—"]
            if not df_sec.empty:
                f4 = make_pie(df_sec, "Valeur (€)", "Secteur",
                              "Secteurs",
                              P_COLORS[1:]+P_COLORS[:1])
                if f4: st.plotly_chart(f4, use_container_width=True)
            else:
                st.caption("Secteurs non disponibles")
    else:
        st.info("Aucune position ouverte détectée.")

    with st.expander("HISTORIQUE DES OPÉRATIONS"):
        st.dataframe(df_hist.sort_values("Date", ascending=False),
                     use_container_width=True, hide_index=True)
    with st.expander("HISTORIQUE DES VERSEMENTS"):
        st.dataframe(df_vers.sort_values("Date d'opération", ascending=False),
                     use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ANALYSE 10-BAGGERS
# ══════════════════════════════════════════════════════════════════════════════
def page_10baggers():
    st.markdown('<div class="ph"><div class="ph-title">Analyse 10-Baggers</div>'
                '<div class="ph-sub">▸ Checklist fondamentale · Score pondéré /100</div></div>',
                unsafe_allow_html=True)

    ticker_input = st.text_input("Ticker", "",
        placeholder="Ticker yfinance  ·  MC.PA  ·  AIR.PA  ·  AAPL  ·  ASML.AS",
        label_visibility="collapsed")

    if not ticker_input:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">◎</div>
          <div class="empty-title">Entrez un ticker pour lancer l'analyse</div>
          <div class="empty-sub">MC.PA · EL.PA · AIR.PA · AAPL · MSFT · ASML.AS</div>
        </div>""", unsafe_allow_html=True)
        return

    ticker = ticker_input.strip().upper()

    with st.spinner(f"Analyse de {ticker}…"):
        try:
            t    = yf.Ticker(ticker)
            info = t.info
        except Exception as e:
            st.error(f"Erreur : {e}"); return

    if not info:
        st.error("Ticker introuvable."); return

    cur_px  = info.get("currentPrice") or info.get("regularMarketPrice")
    name    = info.get("longName") or info.get("shortName") or ticker
    sector  = info.get("sector", "—")
    country = info.get("country", "—")
    mktcap  = info.get("marketCap")
    mc_str  = (f"{mktcap/1e9:.1f}B €" if mktcap and mktcap>=1e9
               else (f"{mktcap/1e6:.0f}M €" if mktcap else "—"))

    st.markdown(f"""<div class="company-header">
      <div>
        <div class="company-name">{name}</div>
        <div class="company-ticker">▸ {ticker}</div>
      </div>
      <div class="company-meta">
        <div><div class="meta-lbl">Secteur</div><div class="meta-val">{sector}</div></div>
        <div><div class="meta-lbl">Pays</div><div class="meta-val">{country}</div></div>
        <div><div class="meta-lbl">Market Cap</div><div class="meta-val">{mc_str}</div></div>
        <div class="price-box">
          <div class="price-lbl">Cours actuel</div>
          <div class="price-val">{f"{cur_px:.2f}" if cur_px else "—"}</div>
        </div>
      </div></div>""", unsafe_allow_html=True)

    # ── Data extraction ────────────────────────────────────────────────────────
    def get_5y_cagr(series):
        try:
            s = series.dropna().sort_index()
            if len(s) < 2: return None
            n = min(5, len(s)-1)
            v0, v1 = s.iloc[-n-1], s.iloc[-1]
            return (v1/v0)**(1/n)-1 if v0 > 0 else None
        except: return None

    try:
        rev_cagr = get_5y_cagr(t.financials.loc["Total Revenue"]) if "Total Revenue" in t.financials.index else None
    except: rev_cagr = None

    try:
        sh = t.balance_sheet.loc["Ordinary Shares Number"].dropna().sort_index()
        buyback = (sh.iloc[-1] < sh.iloc[0]) if len(sh) >= 2 else None
    except: buyback = None

    try:
        fin  = t.financials; bs = t.balance_sheet
        ebit = safe_float(fin.loc["EBIT"].iloc[0]) if "EBIT" in fin.index else None
        tax  = safe_float(info.get("effectiveTaxRate")) or 0.25
        nopat = ebit*(1-tax) if ebit else None
        ta    = safe_float(bs.loc["Total Assets"].iloc[0])     if "Total Assets"       in bs.index else None
        cl    = safe_float(bs.loc["Current Liabilities"].iloc[0]) if "Current Liabilities" in bs.index else None
        cap   = ta - cl if ta and cl else None
        roic  = (nopat/cap) if nopat and cap and cap>0 else safe_float(info.get("returnOnEquity"))
    except: roic = safe_float(info.get("returnOnEquity"))

    try:
        cf  = t.cashflow
        fcf = safe_float(cf.loc["Free Cash Flow"].iloc[0]) if "Free Cash Flow" in cf.index else None
        rev = safe_float(t.financials.loc["Total Revenue"].iloc[0]) if "Total Revenue" in t.financials.index else None
        fcf_margin = (fcf/rev) if fcf and rev and rev>0 else None
    except: fcf_margin = None

    try:
        div = t.dividends
        if len(div) > 0:
            div.index = div.index.tz_localize(None)
            div_cagr = get_5y_cagr(div.resample("YE").sum())
        else: div_cagr = None
    except: div_cagr = None

    payout = safe_float(info.get("payoutRatio"))

    try:
        fcf_ser  = t.cashflow.loc["Free Cash Flow"] if "Free Cash Flow" in t.cashflow.index else None
        fcf_cagr = get_5y_cagr(fcf_ser) if fcf_ser is not None else None
    except: fcf_cagr = None

    try:
        debt    = safe_float(info.get("totalDebt")) or 0
        ebitda  = safe_float(info.get("ebitda"))
        d_ebitda = (debt/ebitda) if ebitda and ebitda>0 else None
    except: d_ebitda = None

    per = safe_float(info.get("trailingPE")) or safe_float(info.get("forwardPE"))

    # Momentum — fetch once for all periods
    try:
        hist_all = t.history(period="max")
        hist_all.index = hist_all.index.tz_localize(None)
        ref_all  = yf.Ticker("IWDA.AS").history(period="max")
        ref_all.index = ref_all.index.tz_localize(None)

        def sp(years):
            cut = datetime.today() - timedelta(days=365*years)
            sub = hist_all[hist_all.index >= pd.Timestamp(cut)]
            return (sub["Close"].iloc[-1]/sub["Close"].iloc[0]-1)*100 if len(sub)>5 else None
        def rp(years):
            cut = datetime.today() - timedelta(days=365*years)
            sub = ref_all[ref_all.index >= pd.Timestamp(cut)]
            return (sub["Close"].iloc[-1]/sub["Close"].iloc[0]-1)*100 if len(sub)>5 else None

        s5,s10,s15 = sp(5), sp(10), sp(15)
        r5,r10,r15 = rp(5), rp(10), rp(15)
        if s10 and r10:   mom_ok=s10>r10; mom_str=f"+{s10:.0f}% vs +{r10:.0f}% MSCI (10A)"
        elif s5 and r5:   mom_ok=s5>r5;   mom_str=f"+{s5:.0f}% vs +{r5:.0f}% MSCI (5A)"
        else: mom_ok=None; mom_str=None
    except: hist_all=pd.DataFrame(); s5=s10=s15=r5=r10=r15=None; mom_ok=None; mom_str=None

    # ── Evaluate ──────────────────────────────────────────────────────────────
    def evaluate(val, good, bad, higher=True):
        v = safe_float(val)
        if v is None: return "○","n",None
        if higher:
            if v >= good: return "✓","g",v
            if v <= bad:  return "✗","r",v
            return "◐","y",v
        else:
            if v <= good: return "✓","g",v
            if v >= bad:  return "✗","r",v
            return "◐","y",v

    checklist = []
    ic,cl,vv = evaluate(rev_cagr, 0.10, 0.03)
    checklist.append((1,"Croissance CA (5 ans)",ic,cl,fmt_pct_safe(vv),"✓ > 10%","✗ < 3%"))

    if buyback is True:    ic2,cl2 = "✓","g"
    elif buyback is False: ic2,cl2 = "✗","r"
    else:                  ic2,cl2 = "○","n"
    checklist.append((2,"Rachat d'actions",ic2,cl2,
        "Rachète" if buyback is True else ("Émet" if buyback is False else "N/A"),
        "✓ Rachète","✗ Émet"))

    ic,cl,vv = evaluate(roic, 0.20, 0.05)
    checklist.append((3,"ROIC",ic,cl,fmt_pct_safe(vv),"✓ > 20%","✗ < 5%"))
    ic,cl,vv = evaluate(fcf_margin, 0.20, 0.03)
    checklist.append((4,"Marge Free Cash-Flow",ic,cl,fmt_pct_safe(vv),"✓ > 20%","✗ < 3%"))
    ic,cl,vv = evaluate(div_cagr, 0.10, 0.03)
    checklist.append((5,"Croissance dividende (5 ans)",ic,cl,fmt_pct_safe(vv),"✓ > 10%","✗ < 3%"))
    ic,cl,vv = evaluate(payout, 0.60, 0.90, higher=False)
    checklist.append((6,"Payout ratio",ic,cl,fmt_pct_safe(vv),"✓ < 60%","✗ > 90%"))
    ic,cl,vv = evaluate(fcf_cagr, 0.10, 0.03)
    checklist.append((7,"Croissance FCF (5 ans)",ic,cl,fmt_pct_safe(vv),"✓ > 10%","✗ < 3%"))
    ic,cl,vv = evaluate(d_ebitda, 1.5, 5.0, higher=False)
    checklist.append((8,"Dette / EBITDA",ic,cl,fmt_num(vv),"✓ < 1.5","✗ > 5"))
    ic,cl,vv = evaluate(per, 20, 40, higher=False)
    checklist.append((9,"PER",ic,cl,fmt_num(vv,1),"✓ < 20","✗ > 40"))

    if mom_ok is True:    ic10,cl10 = "✓","g"
    elif mom_ok is False: ic10,cl10 = "✗","r"
    else:                 ic10,cl10 = "○","n"
    checklist.append((10,"Momentum vs MSCI World",ic10,cl10,
        mom_str if mom_str else "N/A","✓ > indice","✗ < indice"))

    # ── Score ─────────────────────────────────────────────────────────────────
    score100 = 0.0
    for num,_,_,cl,_,_,_ in checklist:
        w = WEIGHTS[num]
        if cl == "g": score100 += w
        elif cl == "y": score100 += w * 0.5

    greens  = sum(1 for c in checklist if c[3]=="g")
    reds    = sum(1 for c in checklist if c[3]=="r")
    yellows = sum(1 for c in checklist if c[3]=="y")
    nas     = sum(1 for c in checklist if c[3]=="n")
    sc      = int(round(score100))
    sc_c    = "#22c55e" if sc>=70 else ("#f59e0b" if sc>=50 else "#ef4444")
    verdict = "EXCELLENT" if sc>=70 else ("CORRECT" if sc>=50 else "INSUFFISANT")

    # ── Legend ────────────────────────────────────────────────────────────────
    st.markdown("""<div class="legend-strip">
      <div class="legend-item"><div class="legend-dot" style="background:#22c55e"></div>Critère validé</div>
      <div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div>Critère refusé</div>
      <div class="legend-item"><div class="legend-dot" style="background:#f59e0b"></div>Entre les bornes</div>
      <div class="legend-item"><div class="legend-dot" style="background:#475569"></div>Données N/A</div>
    </div>""", unsafe_allow_html=True)

    col_sc, col_cr = st.columns([1, 2])

    with col_sc:
        st.markdown(f"""<div class="score-card">
          <div class="score-lbl">Score de recommandation</div>
          <div class="score-num" style="color:{sc_c}">{sc}</div>
          <div class="score-verdict" style="color:{sc_c}">/100 · {verdict}</div>
          <div class="score-bar-bg">
            <div class="score-bar" style="width:{sc}%;background:{sc_c}"></div>
          </div>
          <div class="score-counts">
            <span class="sc-pill g">✓ {greens} validés</span>
            <span class="sc-pill r">✗ {reds} refusés</span>
            <span class="sc-pill y">◐ {yellows} neutres</span>
            <span class="sc-pill n">○ {nas} N/A</span>
          </div>
          <div class="score-w"><span>Pondérations (/100)</span><br>
            CA 15% · ROIC 15%<br>Marge FCF 12% · Croiss. FCF 12%<br>
            D/EBITDA 10% · Momentum 10%<br>Rachat 8% · PER 7%<br>
            Dividende 6% · Payout 5%
          </div></div>""", unsafe_allow_html=True)

    with col_cr:
        rows_html = ""
        for num,name_c,ic,cl,val_str,good,bad in checklist:
            tip_t, tip_d = DEFINITIONS.get(num, (name_c,"—"))
            rows_html += (
                f'<div class="cr {cl}">'
                f'<div class="cr-badge {cl}">{ic}</div>'
                f'<span class="cr-num">{num:02d}</span>'
                f'<div class="cr-tip">'
                f'<span class="cr-name">{name_c}</span>'
                f'<span class="tip-icon">?</span>'
                f'<div class="tip-box"><div class="tip-t">{tip_t}</div>'
                f'<div class="tip-d">{tip_d}</div></div>'
                f'</div>'
                f'<span class="cr-val {cl}">{val_str}</span>'
                f'<span class="cr-thresh">'
                f'<span class="tg">{good}</span><br>'
                f'<span class="tr">{bad}</span></span>'
                f'</div>'
            )
        st.markdown(rows_html, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # DONNÉES FINANCIÈRES CLÉS
    # ════════════════════════════════════════════════════════════════════════
    section_label("Données financières clés")

    def fmt_bn(v):
        if v is None: return "N/A"
        try:
            v = float(v)
            if abs(v) >= 1e12: return f"{v/1e12:.2f}T"
            if abs(v) >= 1e9:  return f"{v/1e9:.2f}B"
            if abs(v) >= 1e6:  return f"{v/1e6:.1f}M"
            return f"{v:.2f}"
        except: return "N/A"

    def fmt_p2(v):
        if v is None: return "N/A"
        try: return f"{float(v)*100:.1f}%"
        except: return "N/A"

    def clr(v, good, bad, up=True):
        f = safe_float(v)
        if f is None: return "var(--t2)"
        if up:  return "#22c55e" if f>=good else ("#ef4444" if f<=bad else "#f59e0b")
        else:   return "#22c55e" if f<=good else ("#ef4444" if f>=bad else "#f59e0b")

    def card(lbl, val, sub="", tip="", vc=None):
        c = vc if vc else ("var(--t2)" if str(val) in ("N/A","—","") else "var(--text)")
        if tip:
            tip_div = (
                '<div class="ftip" style="position:absolute;bottom:calc(100%+6px);left:0;'
                'z-index:9999;background:#0c0f1a;border:1px solid #3b82f6;border-radius:10px;'
                'padding:12px 14px;width:255px;box-shadow:0 12px 32px rgba(0,0,0,.92);'
                'pointer-events:none;white-space:normal;opacity:0;visibility:hidden;'
                'transition:opacity .18s">'
                '<div style="font-family:Outfit,sans-serif;font-size:.72rem;color:#94a3b8;line-height:1.6">'
                + tip + '</div></div>'
            )
            icon = ('<span style="position:absolute;top:8px;right:9px;font-family:DM Mono,monospace;'
                    'font-size:.52rem;color:#3b82f6;background:rgba(59,130,246,.1);'
                    'border:1px solid rgba(59,130,246,.3);border-radius:3px;padding:0 4px;line-height:1.5">?</span>')
            wrap = 'class="has-ftip" style="background:var(--s1);border:1px solid var(--border);border-radius:8px;padding:13px 15px;position:relative;cursor:help"'
        else:
            tip_div = icon = ""
            wrap = 'style="background:var(--s1);border:1px solid var(--border);border-radius:8px;padding:13px 15px;position:relative"'
        sub_h = (f'<div style="font-family:DM Mono,monospace;font-size:.54rem;color:var(--t3);margin-top:2px">{sub}</div>') if sub else ""
        return (
            f'<div {wrap}>'
            + tip_div + icon
            + '<div style="font-family:DM Mono,monospace;font-size:.59rem;color:var(--t3);'
            'text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px">' + lbl + '</div>'
            '<div style="font-family:Outfit,sans-serif;font-size:1.05rem;font-weight:600;color:'
            + c + '">' + str(val) + '</div>'
            + sub_h + '</div>'
        )

    def row(*cards, cols=5):
        return (
            '<div style="display:grid;grid-template-columns:repeat(' + str(cols) + ',1fr);gap:8px;margin-bottom:8px">'
            + "".join(cards) + '</div>'
        )

    def sec(title):
        return (
            '<div style="font-family:DM Mono,monospace;font-size:.58rem;color:var(--t3);'
            'text-transform:uppercase;letter-spacing:.12em;margin:14px 0 7px;padding:5px 0;'
            'border-bottom:1px solid var(--border)">▸ ' + title + '</div>'
        )

    fcf_v  = safe_float(info.get("freeCashflow"))
    rev_v  = safe_float(info.get("totalRevenue"))
    fcfm_v = (fcf_v/rev_v) if fcf_v and rev_v and rev_v!=0 else None
    tgt    = safe_float(info.get("targetMeanPrice"))
    upside = (fmt_p2((tgt/(cur_px or 1))-1)+" upside") if tgt and cur_px else ""
    reco   = (info.get("recommendationKey") or "").lower()
    dyield = safe_float(info.get("dividendYield"))

    html = ""

    html += sec("Valorisation")
    html += row(
        card("PER (TTM)",    fmt_num(info.get("trailingPE"),1),    "",
             "Price/Earnings 12 mois. Combien paie-t-on pour 1€ de bénéfice.<br>✓ &lt;20 raisonnable · ✗ &gt;40 cher",
             clr(info.get("trailingPE"),20,40,up=False)),
        card("PER Forward",  fmt_num(info.get("forwardPE"),1),     "bénéf. estimés N+1",
             "PER sur bénéfices estimés. Plus fiable pour sociétés en forte croissance.<br>✓ &lt;15 · ✗ &gt;35",
             clr(info.get("forwardPE"),15,35,up=False)),
        card("PEG",          fmt_num(info.get("pegRatio"),2),      "",
             "PER / Croissance BPA. Intègre la croissance dans la valorisation.<br>✓ &lt;1 = sous-évalué vs croissance · ✗ &gt;2 = trop cher",
             clr(info.get("pegRatio"),1.0,2.0,up=False)),
        card("P/Sales",      fmt_num(info.get("priceToSalesTrailing12Months"),2), "",
             "Prix / CA. Utile pour sociétés non rentables.<br>✓ &lt;3 · ✗ &gt;10",
             clr(info.get("priceToSalesTrailing12Months"),3,10,up=False)),
        card("P/Book",       fmt_num(info.get("priceToBook"),2),   "",
             "Prix / Valeur comptable.<br>✓ &lt;1 = potentiellement sous-valorisé · &gt;5 = prime élevée"),
    )

    html += sec("Rentabilité")
    html += row(
        card("Marge brute",  fmt_p2(info.get("grossMargins")),  "",
             "CA - Coût ventes / CA. Mesure le pricing power.<br>✓ &gt;40% · ✗ &lt;15%",
             clr(info.get("grossMargins"),0.40,0.15)),
        card("Marge opé.",   fmt_p2(info.get("operatingMargins")), "",
             "Bénéfice opérationnel / CA. Efficacité avant impôts.<br>✓ &gt;15% · ✗ &lt;5%",
             clr(info.get("operatingMargins"),0.15,0.05)),
        card("Marge nette",  fmt_p2(info.get("profitMargins")), "",
             "Bénéfice net / CA. Ce qui reste après tout.<br>✓ &gt;10% · ✗ &lt;3%",
             clr(info.get("profitMargins"),0.10,0.03)),
        card("Marge FCF",    fmt_p2(fcfm_v),                   "",
             "Free Cash Flow / CA. Cash réellement généré.<br>✓ &gt;20% · ✗ &lt;3%",
             clr(fcfm_v,0.20,0.03)),
        card("ROE",          fmt_p2(info.get("returnOnEquity")), "",
             "Return on Equity. Rentabilité fonds propres.<br>✓ &gt;15% · ✗ &lt;5%",
             clr(info.get("returnOnEquity"),0.15,0.05)),
    )

    html += sec("Bilan & Dette")
    html += row(
        card("Dette/EBITDA", fmt_num(d_ebitda),                  "",
             "Années de profits bruts pour rembourser la dette.<br>✓ &lt;1.5 · ✗ &gt;5",
             clr(d_ebitda,1.5,5.0,up=False)),
        card("D/E ratio",    fmt_num(info.get("debtToEquity"),2) if info.get("debtToEquity") else "N/A", "",
             "Dette / Fonds propres.<br>✓ &lt;1 peu endetté · ✗ &gt;3 très endetté",
             clr(info.get("debtToEquity"),1.0,3.0,up=False)),
        card("Current ratio",fmt_num(info.get("currentRatio"),2) if info.get("currentRatio") else "N/A",
             "actif/passif CT",
             "Actif court terme / Passif court terme.<br>✓ &gt;1.5 solvable · ✗ &lt;1 risque liquidité",
             clr(info.get("currentRatio"),1.5,1.0)),
        card("Trésorerie",   fmt_bn(info.get("totalCash")),      "",
             "Cash disponible. Indicateur de résilience."),
        card("FCF",          fmt_bn(info.get("freeCashflow")),   "cash libre annuel",
             "Free Cash Flow annuel. Cash après investissements.",
             "#22c55e" if (fcf_v or 0)>0 else "#ef4444"),
    )

    html += sec("Marché & Analystes")
    html += row(
        card("Bêta",         fmt_num(info.get("beta"),2),        "vs indice",
             "Volatilité vs marché. =1 suit l'indice · &gt;1 plus volatile · &lt;0 inversement corrélé"),
        card("52s Haut",     fmt_bn(info.get("fiftyTwoWeekHigh")), "",
             "Plus haut 52 semaines. Zone de résistance si le cours s'en approche."),
        card("52s Bas",      fmt_bn(info.get("fiftyTwoWeekLow")),  "",
             "Plus bas 52 semaines. Zone de support si le cours s'en approche."),
        card("Obj. analystes",fmt_bn(tgt) if tgt else "N/A",    upside,
             "Prix cible moyen des analystes.",
             "#22c55e" if (tgt and cur_px and tgt>cur_px) else ("#ef4444" if tgt and cur_px else None)),
        card("Recommandation",
             (info.get("recommendationKey") or "N/A").upper().replace("_"," "),
             str(info.get("numberOfAnalystOpinions","?"))+" analystes",
             "Consensus : Strong Buy &gt; Buy &gt; Hold &gt; Sell &gt; Strong Sell",
             "#22c55e" if reco in ("buy","strong_buy") else ("#ef4444" if reco in ("sell","strong_sell") else "#f59e0b")),
    )

    html += sec("Dividende & Capital")
    html += row(
        card("Dividende",    fmt_bn(info.get("dividendRate")),
             fmt_p2(dyield)+" yield" if dyield else "aucun dividende",
             "Dividende annuel / action. Croissance régulière = signe de solidité.",
             "#22c55e" if (dyield or 0)>0.02 else None),
        card("Payout ratio", fmt_p2(info.get("payoutRatio")),   "",
             "Part du bénéfice versée en dividende.<br>✓ &lt;60% durable · ✗ &gt;90% fragile",
             clr(info.get("payoutRatio"),0.60,0.90,up=False)),
        card("EPS TTM",      fmt_bn(info.get("trailingEps")),   "bénéf/action 12m",
             "Earnings Per Share 12 mois. Croissance = bon signe. Négatif = non rentable."),
        card("EPS Forward",  fmt_bn(info.get("forwardEps")),    "estimé N+1",
             "EPS estimé par les analystes. EPS fwd &gt; EPS TTM = croissance attendue."),
        card("CA (TTM)",     fmt_bn(info.get("totalRevenue")),  "chiffre d'affaires",
             "CA des 12 derniers mois. Base de toute valorisation."),
    )

    st.markdown(html, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # INDICATEURS TECHNIQUES
    # ════════════════════════════════════════════════════════════════════════
    section_label("Indicateurs techniques")

    hist_tech = get_stock_history(ticker, "1y")
    if not hist_tech.empty and len(hist_tech) >= 50:
        cl = hist_tech["Close"]
        hi = hist_tech["High"]
        lo = hist_tech["Low"]
        vo = hist_tech["Volume"]
        cp = float(cl.iloc[-1])

        # Moving Averages
        ma20  = cl.rolling(20).mean()
        ma50  = cl.rolling(50).mean()
        ma100 = cl.rolling(100).mean() if len(cl)>=100 else None
        ma200 = cl.rolling(200).mean() if len(cl)>=200 else None

        def ma_card(label, ma_ser):
            if ma_ser is None or ma_ser.dropna().empty:
                return card(label, "N/A", "", "Pas assez de données")
            v = float(ma_ser.iloc[-1])
            d = (cp - v) / v * 100
            sig = "▲ Au-dessus" if cp > v else "▼ En-dessous"
            c = "#22c55e" if cp > v else "#ef4444"
            n = label[2:]
            return card(label, f"{v:.2f}", f"{d:+.1f}%  {sig}",
                f"Moyenne Mobile {n}j. Cours &gt; MM = tendance haussière.<br>Cours &lt; MM = tendance baissière.", c)

        # RSI 14
        delta = cl.diff()
        gain  = delta.clip(lower=0).rolling(14).mean()
        loss  = (-delta.clip(upper=0)).rolling(14).mean()
        rsi_v = float((100 - 100/(1+gain/loss)).iloc[-1])
        rsi_c = "#ef4444" if rsi_v>70 else ("#22c55e" if rsi_v<30 else "#f59e0b")
        rsi_l = "Suracheté ⚠" if rsi_v>70 else ("Survendu 🎯" if rsi_v<30 else "Neutre")

        # MACD (12,26,9)
        e12   = cl.ewm(span=12,adjust=False).mean()
        e26   = cl.ewm(span=26,adjust=False).mean()
        macd  = e12 - e26
        msig  = macd.ewm(span=9,adjust=False).mean()
        mv    = float(macd.iloc[-1])
        ms    = float(msig.iloc[-1])
        mh    = mv - ms
        mc    = "#22c55e" if mv>ms else "#ef4444"

        # Bollinger Bands (20, 2σ)
        bm    = cl.rolling(20).mean()
        bs    = cl.rolling(20).std()
        bu    = float((bm+2*bs).iloc[-1])
        bl    = float((bm-2*bs).iloc[-1])
        bpct  = (cp-bl)/(bu-bl)*100 if bu!=bl else 50
        bc    = "#ef4444" if bpct>80 else ("#22c55e" if bpct<20 else "#f59e0b")
        blbl  = "Haut bande ⚠" if bpct>80 else ("Bas bande 🎯" if bpct<20 else "Zone centrale")

        # Stochastique %K (14)
        lo14  = lo.rolling(14).min()
        hi14  = hi.rolling(14).max()
        stk   = float(((cl-lo14)/(hi14-lo14)*100).iloc[-1])
        sc    = "#ef4444" if stk>80 else ("#22c55e" if stk<20 else "#f59e0b")
        slbl  = "Suracheté" if stk>80 else ("Survendu" if stk<20 else "Neutre")

        # ATR 14
        tr    = pd.concat([hi-lo,(hi-cl.shift()).abs(),(lo-cl.shift()).abs()],axis=1).max(axis=1)
        atr_v = float(tr.rolling(14).mean().iloc[-1])

        # Volume
        va20  = float(vo.rolling(20).mean().iloc[-1])
        vc_v  = float(vo.iloc[-1])
        vr    = vc_v/va20 if va20>0 else 1
        vrc   = "#22c55e" if vr>1.5 else ("#ef4444" if vr<0.5 else "var(--t2)")

        tech = ""

        tech += sec("Moyennes mobiles (MM)")
        tech += row(
            ma_card("MM20",  ma20),
            ma_card("MM50",  ma50),
            ma_card("MM100", ma100),
            ma_card("MM200", ma200),
            card("ATR (14)", f"{atr_v:.2f}", f"{atr_v/cp*100:.1f}% du cours",
                 "Average True Range : volatilité quotidienne moyenne sur 14j.<br>Élevé = marché agité · Faible = marché calme"),
        )

        tech += sec("Oscillateurs")
        tech += row(
            card("RSI (14)",    f"{rsi_v:.1f}",  rsi_l,
                 "Relative Strength Index sur 14j.<br>✓ 30-70 = zone neutre<br>&gt;70 = suracheté (attention)<br>&lt;30 = survendu (opportunité)", rsi_c),
            card("MACD",        f"{mv:.2f}",     "Haussier ▲" if mv>ms else "Baissier ▼",
                 "MACD (12,26,9) = EMA12 - EMA26.<br>MACD &gt; Signal = momentum haussier.<br>Croisement = signal d'achat/vente.", mc),
            card("MACD Signal", f"{ms:.2f}",     f"Hist: {mh:+.2f}",
                 "Signal Line = EMA9 du MACD.<br>Histogramme positif et croissant = accélération haussière.",
                 "#22c55e" if mh>0 else "#ef4444"),
            card("Bollinger %", f"{bpct:.0f}%",  blbl,
                 "Position dans les Bandes de Bollinger (20j, 2σ).<br>&gt;80% = proche bande haute (retour possible)<br>&lt;20% = proche bande basse (rebond possible)", bc),
            card("Stoch %K",    f"{stk:.1f}",    slbl,
                 "Stochastique 14j. Similaire au RSI mais plus réactif.<br>&gt;80 = suracheté · &lt;20 = survendu", sc),
        )

        tech += sec("Volume & Bandes de Bollinger")
        tech += row(
            card("Vol / Moy20", f"{vr:.2f}x",    f"moy: {fmt_bn(va20)}",
                 "Volume actuel vs moyenne 20j.<br>&gt;1.5x = signal fort (breakout fiable)<br>&lt;0.5x = volume faible (signal peu fiable)", vrc),
            card("Volume",      fmt_bn(vc_v),    "dernier jour",
                 "Volume échangé lors de la dernière séance."),
            card("BB Haut",     f"{bu:.2f}",     "résistance",
                 "Bande haute de Bollinger. Zone de résistance dynamique."),
            card("BB Bas",      f"{bl:.2f}",     "support",
                 "Bande basse de Bollinger. Zone de support dynamique."),
            card("BB Milieu",   f"{float(bm.iloc[-1]):.2f}", "MM20",
                 "Milieu des bandes = MM20. Au-dessus = tendance haussière CT."),
        )

        st.markdown(tech, unsafe_allow_html=True)

    else:
        st.info("Données historiques insuffisantes pour les indicateurs techniques (min. 50 jours).")

    # ════════════════════════════════════════════════════════════════════════
    # GRAPHIQUE avec MMs
    # ════════════════════════════════════════════════════════════════════════
    section_label("Cours de l'action")

    period_labels = [p[0] for p in STOCK_PERIODS]
    cr1, cr2 = st.columns([4, 1])
    with cr1:
        sel_period = st.radio("Période", period_labels,
                              index=period_labels.index("5 ans"), horizontal=True,
                              key="stock_period", label_visibility="collapsed")
    with cr2:
        chart_type = st.radio("Type", ["Courbe", "Bougies"], horizontal=True,
                              key="chart_type", label_visibility="collapsed")

    yf_period, _ = {p[0]: (p[1], p[2]) for p in STOCK_PERIODS}[sel_period]

    with st.spinner("Chargement…"):
        hist_chart = get_stock_history(ticker, yf_period)

    if not hist_chart.empty and len(hist_chart) >= 2:
        pct_sel   = (hist_chart["Close"].iloc[-1] - hist_chart["Close"].iloc[0]) / hist_chart["Close"].iloc[0] * 100
        abs_sel   = hist_chart["Close"].iloc[-1] - hist_chart["Close"].iloc[0]
        pct_color = perf_color(pct_sel)
    else:
        pct_sel = abs_sel = None; pct_color = "#475569"

    # Perf strip toutes périodes
    strip = '<div class="stock-perf-strip">'
    for lbl2, yf_p2, _ in STOCK_PERIODS:
        try:
            h2 = get_stock_history(ticker, yf_p2)
            if not h2.empty and len(h2) >= 2:
                p2 = (h2["Close"].iloc[-1]-h2["Close"].iloc[0])/h2["Close"].iloc[0]*100
                c2 = perf_color(p2)
                strip += f'<div class="sp-item"><div class="sp-lbl">{lbl2}</div><div class="sp-val" style="color:{c2}">{"+" if p2>=0 else ""}{p2:.1f}%</div></div>'
            else:
                strip += f'<div class="sp-item"><div class="sp-lbl">{lbl2}</div><div class="sp-val" style="color:var(--t3)">—</div></div>'
        except:
            strip += f'<div class="sp-item"><div class="sp-lbl">{lbl2}</div><div class="sp-val" style="color:var(--t3)">—</div></div>'
    strip += '</div>'
    st.markdown(strip, unsafe_allow_html=True)

    if not hist_chart.empty:
        hc   = hist_chart["Close"]
        lc   = perf_color(pct_sel) if pct_sel else "#3b82f6"
        fc   = "rgba(34,197,94,0.05)" if (pct_sel or 0)>=0 else "rgba(239,68,68,0.05)"
        ymn  = float(hc.min()); ymx = float(hc.max())
        ypad = max((ymx-ymn)*0.15, ymx*0.005)
        is_intra = sel_period in ("Jour", "1 sem")
        hfmt = "<b>%{x|%d %b %Y %H:%M}</b> · %{y:.2f}<extra></extra>" if is_intra else "<b>%{x|%d %b %Y}</b> · %{y:.2f}<extra></extra>"

        fig2 = go.Figure()

        if chart_type == "Bougies" and all(c in hist_chart.columns for c in ["Open","High","Low","Close"]):
            ymn = float(hist_chart["Low"].min()); ymx = float(hist_chart["High"].max())
            ypad = max((ymx-ymn)*0.12, ymx*0.005)
            fig2.add_trace(go.Candlestick(
                x=hist_chart.index,
                open=hist_chart["Open"], high=hist_chart["High"],
                low=hist_chart["Low"],   close=hist_chart["Close"],
                name="Cours",
                increasing_line_color="#22c55e", increasing_fillcolor="rgba(34,197,94,0.7)",
                decreasing_line_color="#ef4444", decreasing_fillcolor="rgba(239,68,68,0.7)",
                hovertext=None,
            ))
            # MAs sur bougies
            if len(hc) >= 5:
                for ma_n, ma_c, ma_d in [(20,"#f59e0b","dot"),(50,"#3b82f6","dash"),(100,"#8b5cf6","longdash"),(200,"#ef4444","longdashdot")]:
                    if len(hc) >= ma_n:
                        ma = hc.rolling(ma_n).mean()
                        fig2.add_trace(go.Scatter(x=hist_chart.index, y=ma, name=f"MM{ma_n}",
                            line=dict(color=ma_c, width=1.2, dash=ma_d),
                            hovertemplate=f"<b>MM{ma_n}</b> %{{x|%d %b %Y}} · %{{y:.2f}}<extra></extra>"))
        else:
            fig2.add_trace(go.Scatter(x=hist_chart.index, y=hc, name="Cours",
                line=dict(color=lc, width=2), fill="tozeroy", fillcolor=fc, hovertemplate=hfmt))
            # Overlay MAs
            if len(hc) >= 5:
                for ma_n, ma_c, ma_d in [(20,"#f59e0b","dot"),(50,"#3b82f6","dash"),(100,"#8b5cf6","longdash"),(200,"#ef4444","longdashdot")]:
                    if len(hc) >= ma_n:
                        ma = hc.rolling(ma_n).mean()
                        fig2.add_trace(go.Scatter(x=hist_chart.index, y=ma, name=f"MM{ma_n}",
                            line=dict(color=ma_c, width=1.2, dash=ma_d),
                            hovertemplate=f"<b>MM{ma_n}</b> %{{x|%d %b %Y}} · %{{y:.2f}}<extra></extra>"))

        if pct_sel is not None:
            sg = "+" if pct_sel >= 0 else ""
            fig2.add_annotation(x=0.01, y=0.96, xref="paper", yref="paper",
                text=f"{sg}{pct_sel:.2f}%  ({sg}{abs_sel:.2f})",
                showarrow=False, font=dict(size=14, color=pct_color, family="Outfit"),
                bgcolor="rgba(12,15,26,.8)", bordercolor=pct_color, borderwidth=1, borderpad=5)

        layout_opts = {"range":[ymn-ypad,ymx+ypad],"tickformat":".2f"}
        base = plotly_base(340, layout_opts)
        if chart_type == "Bougies":
            base["xaxis"]["rangeslider"] = {"visible": False}
        fig2.update_layout(**base)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Momentum bar ──────────────────────────────────────────────────────────
    if any(v is not None for v in [s5, s10, s15]):
        section_label("Momentum · Performance vs MSCI World")
        plbls, svals, rvals = [], [], []
        for lbl, sv, rv in [("5 ans",s5,r5),("10 ans",s10,r10),("15 ans",s15,r15)]:
            if sv is not None:
                plbls.append(lbl); svals.append(sv); rvals.append(rv or 0)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name=ticker, x=plbls, y=svals,
            marker_color="#22c55e", marker_opacity=0.85,
            hovertemplate=f"<b>{ticker}</b> %{{x}}<br>%{{y:+.1f}}%<extra></extra>"))
        fig3.add_trace(go.Bar(name="MSCI World", x=plbls, y=rvals,
            marker_color="#3b82f6", marker_opacity=0.7,
            hovertemplate="<b>MSCI World</b> %{x}<br>%{y:+.1f}%<extra></extra>"))
        fig3.update_layout(**plotly_base(250, {"ticksuffix":"%"}, bar=True))
        st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SCREENER MULTI-ACTIONS
# ══════════════════════════════════════════════════════════════════════════════

# Liste complète de tickers PEA français (.PA) — Euronext Paris
PEA_FR_TICKERS = ["ALEUP.PA",
 "ALIBR.PA",
 "ALHAF.PA",
 "ALSRS.PA",
 "WLN.PA",
 "ALO.PA",
 "ALHPI.PA",
 "TTE.PA",
 "LAT.PA",
 "ORA.PA",
 "STLAP.PA",
 "ALNEV.PA",
 "ENGI.PA",
 "ACA.PA",
 "ALNRG.PA",
 "AF.PA",
 "CS.PA",
 "ALDBT.PA",
 "ALAGO.PA",
 "ETL.PA",
 "ALALO.PA",
 "ALSEN.PA",
 "STMPA.PA",
 "ALTD.PA",
 "ALCPB.PA",
 "DSY.PA",
 "BNP.PA",
 "ML.PA",
 "CA.PA",
 "ALHG.PA",
 "VIV.PA",
 "GLE.PA",
 "VIE.PA",
 "SAN.PA",
 "ALKAL.PA",
 "ALMKT.PA",
 "SGO.PA",
 "BOL.PA",
 "GLX03-PRO-FE.NX",
 "UBI.PA",
 "AIR.PA",
 "S30.PA",
 "FR.PA",
 "ALBPS.PA",
 "DG.PA",
 "VLA.PA",
 "NACON.PA",
 "AC.PA",
 "RNO.PA",
 "EKI.PA",
 "BN.PA",
 "SU.PA",
 "ALCBI.PA",
 "ALRIB.PA",
 "EN.PA",
 "BVI.PA",
 "ALTHO.PA",
 "SOI.PA",
 "FRVIA.PA",
 "AI.PA",
 "ALTOO.PA",
 "DBV.PA",
 "EL.PA",
 "VK.PA",
 "PUB.PA",
 "RI.PA",
 "EDEN.PA",
 "ALGAE.PA",
 "AYV.PA",
 "MC.PA",
 "OR.PA",
 "SAF.PA",
 "ALTME.PA",
 "GET.PA",
 "LR.PA",
 "CAP.PA",
 "ALCLS.PA",
 "POXEL.PA",
 "SESG.PA",
 "ALPRG.PA",
 "FDJU.PA",
 "RXL.PA",
 "ELIOR.PA",
 "MAU.PA",
 "VANTI.PA",
 "LI.PA",
 "ALVIO.PA",
 "ALJXR.PA",
 "SIGHT.PA",
 "ALDRV.PA",
 "TFI.PA",
 "TE.PA",
 "IPS.PA",
 "ALSGD.PA",
 "ALCBX.PA",
 "RUI.PA",
 "XFAB.PA",
 "IPH.PA",
 "AL2SI.PA",
 "ELIS.PA",
 "URW.PA",
 "KER.PA",
 "ALCLA.PA",
 "ADOC.PA",
 "AB.PA",
 "CRUDP.PA",
 "CLARI.PA",
 "ALVAL.PA",
 "SCR.PA",
 "SW.PA",
 "ALCOX.PA",
 "BIG.PA",
 "CO.PA",
 "HO.PA",
 "OVH.PA",
 "ALMDT.PA",
 "GFC.PA",
 "ALROC.PA",
 "COV.PA",
 "MEMS.PA",
 "NXI.PA",
 "AKE.PA",
 "ALKKO.PA",
 "ALMIB.PA",
 "TEP.PA",
 "ALKLH.PA",
 "FGR.PA",
 "IVA.PA",
 "ERF.PA",
 "ENX.PA",
 "ALATA.PA",
 "ICAD.PA",
 "SPIE.PA",
 "VAC.PA",
 "EMEIS.PA",
 "GNFT.PA",
 "DEC.PA",
 "MERY.PA",
 "IB1T.PA",
 "ALNMG.PA",
 "COFA.PA",
 "ALAGR.PA",
 "ALCJ.PA",
 "NEX.PA",
 "ALAIR.PA",
 "ALWIN.PA",
 "VMX.PA",
 "ALFOR.PA",
 "ALPUL.PA",
 "MMT.PA",
 "BIM.PA",
 "ALTAO.PA",
 "ALOKW.PA",
 "ATO.PA",
 "PLX.PA",
 "MDM.PA",
 "ALNLF.PA",
 "PLNW.PA",
 "ABNX.PA",
 "EXA.PA",
 "RMS.PA",
 "NANO.PA",
 "ALKLK.PA",
 "RF.PA",
 "EGR.PA",
 "ALIMP.PA",
 "AVT.PA",
 "IPN.PA",
 "OPM.PA",
 "PARRO.PA",
 "ADP.PA",
 "SMCP.PA",
 "DBG.PA",
 "AMUN.PA",
 "PROAC.PA",
 "ABVX.PA",
 "ALNOV.PA",
 "EAPI.PA",
 "GTT.PA",
 "ATE.PA",
 "ALREW.PA",
 "OSE.PA",
 "SFPI.PA",
 "ALSPW.PA",
 "ALGID.PA",
 "EXENS.PA",
 "CARM.PA",
 "ALLPL.PA",
 "BEN.PA",
 "ALLOG.PA",
 "ALPWG.PA",
 "ALTHX.PA",
 "3EUS.PA",
 "NK.PA",
 "ALCAT.PA",
 "MEDCL.PA",
 "MF.PA",
 "DIM.PA",
 "VU.PA",
 "ALHRS.PA",
 "SK.PA",
 "ALBPK.PA",
 "TKO.PA",
 "MAAT.PA",
 "NRO.PA",
 "ALNFL.PA",
 "ALTHE.PA",
 "ALDVI.PA",
 "ALINS.PA",
 "AM.PA",
 "ALLIX.PA",
 "ALMAR.PA",
 "ABCA.PA",
 "ANTIN.PA",
 "OREGE.PA",
 "ALNXT.PA",
 "LBIRD.PA",
 "SOP.PA",
 "ALCRB.PA",
 "FPG.PA",
 "ALAFY.PA",
 "MHM.PA",
 "QQQS.PA",
 "ERA.PA",
 "NGASP.PA",
 "ALARF.PA",
 "MRN.PA",
 "VLTSA.PA",
 "FII.PA",
 "DPT.PA",
 "VCT.PA",
 "ALNN6.PA",
 "ITP.PA",
 "ALSEM.PA",
 "ARAMI.PA",
 "KOF.PA",
 "ALWTR.PA",
 "QDT.PA",
 "ALMEX.PA",
 "ALESA.PA",
 "VIRI.PA",
 "ALEXP.PA",
 "RCO.PA",
 "ALXIL.PA",
 "TNG.PA",
 "FDE.PA",
 "VRLA.PA",
 "FGA.PA",
 "NAE.PA",
 "PRC.PA",
 "LOIL.PA",
 "ALMDG.PA",
 "ALTRA.PA",
 "BB.PA",
 "EQS.PA",
 "BRNT.PA",
 "HCO.PA",
 "LHYFE.PA",
 "FNAC.PA",
 "ALOPM.PA",
 "ALDMS.PA",
 "SWP.PA",
 "CVX.PA",
 "CDA.PA",
 "GOLD-EUR.PA",
 "ALHGR.PA",
 "LSS.PA",
 "GLO.PA",
 "ALSTI.PA",
 "ALESE.PA",
 "MLPRX.PA",
 "RMAU.PA",
 "ALREA.PA",
 "GBT.PA",
 "BON.PA",
 "ALRPD.PA",
 "ATEME.PA",
 "WAVE.PA",
 "ALAMA.PA",
 "MTU.PA",
 "ALTUV.PA",
 "ALMAS.PA",
 "WETH.PA",
 "AELIS.PA",
 "ALENT.PA",
 "ARG.PA",
 "ALECP.PA",
 "ALMIN.PA",
 "ALTAI.PA",
 "LOCAL.PA",
 "74SW.PA",
 "ASY.PA",
 "ALNTG.PA",
 "ALKLN.PA",
 "SLNC.PA",
 "CSDA.PA",
 "ALGIL.PA",
 "AIGAP.PA",
 "MLNMA.PA",
 "CBOT.PA",
 "FIPP.PA",
 "MMB.PA",
 "ALTA.PA",
 "ALMUN.PA",
 "AUB.PA",
 "VIRP.PA",
 "PEUG.PA",
 "ACAN.PA",
 "AKW.PA",
 "ALLGO.PA",
 "VIL.PA",
 "ALHYP.PA"]
# Déduplique et trie
PEA_FR_TICKERS = sorted(list(set(PEA_FR_TICKERS)))

DEFAULT_SCREENER_TICKERS = ["AIR.PA", "MC.PA", "RNL.PA", "CDI.PA", "AL2SI.PA", "FDJU.PA", "EM.PA"]

CRITERIA_LABELS = [
    "Croissance CA",
    "Rachat actions",
    "ROIC",
    "Marge FCF",
    "Croissance Div.",
    "Payout ratio",
    "Croissance FCF",
    "Dette/EBITDA",
    "PER",
    "Momentum",
]

def compute_10bagger_data(ticker_str):
    """
    Calcule les 10 critères 10-bagger pour un ticker.
    Retourne un dict avec toutes les valeurs brutes + statuts + score.
    """
    try:
        t    = yf.Ticker(ticker_str)
        info = t.info
    except:
        return None

    if not info:
        return None

    def get_5y_cagr(series):
        try:
            s = series.dropna().sort_index()
            if len(s) < 2: return None
            n = min(5, len(s)-1)
            v0, v1 = s.iloc[-n-1], s.iloc[-1]
            return (v1/v0)**(1/n)-1 if v0 > 0 else None
        except: return None

    # 1. CA CAGR
    try:
        rev_cagr = get_5y_cagr(t.financials.loc["Total Revenue"]) if "Total Revenue" in t.financials.index else None
    except: rev_cagr = None

    # 2. Rachat
    try:
        sh = t.balance_sheet.loc["Ordinary Shares Number"].dropna().sort_index()
        buyback = (sh.iloc[-1] < sh.iloc[0]) if len(sh) >= 2 else None
    except: buyback = None

    # 3. ROIC
    try:
        fin  = t.financials; bs = t.balance_sheet
        ebit = safe_float(fin.loc["EBIT"].iloc[0]) if "EBIT" in fin.index else None
        tax  = safe_float(info.get("effectiveTaxRate")) or 0.25
        nopat = ebit*(1-tax) if ebit else None
        ta    = safe_float(bs.loc["Total Assets"].iloc[0])        if "Total Assets"       in bs.index else None
        cl    = safe_float(bs.loc["Current Liabilities"].iloc[0]) if "Current Liabilities" in bs.index else None
        cap   = ta - cl if ta and cl else None
        roic  = (nopat/cap) if nopat and cap and cap>0 else safe_float(info.get("returnOnEquity"))
    except: roic = safe_float(info.get("returnOnEquity"))

    # 4. Marge FCF
    try:
        cf  = t.cashflow
        fcf = safe_float(cf.loc["Free Cash Flow"].iloc[0]) if "Free Cash Flow" in cf.index else None
        rev = safe_float(t.financials.loc["Total Revenue"].iloc[0]) if "Total Revenue" in t.financials.index else None
        fcf_margin = (fcf/rev) if fcf and rev and rev>0 else None
    except: fcf_margin = None

    # 5. Croissance dividende
    try:
        div = t.dividends
        if len(div) > 0:
            div.index = div.index.tz_localize(None)
            div_cagr = get_5y_cagr(div.resample("YE").sum())
        else: div_cagr = None
    except: div_cagr = None

    # 6. Payout
    payout = safe_float(info.get("payoutRatio"))

    # 7. Croissance FCF
    try:
        fcf_ser  = t.cashflow.loc["Free Cash Flow"] if "Free Cash Flow" in t.cashflow.index else None
        fcf_cagr = get_5y_cagr(fcf_ser) if fcf_ser is not None else None
    except: fcf_cagr = None

    # 8. Dette/EBITDA
    try:
        debt    = safe_float(info.get("totalDebt")) or 0
        ebitda  = safe_float(info.get("ebitda"))
        d_ebitda = (debt/ebitda) if ebitda and ebitda>0 else None
    except: d_ebitda = None

    # 9. PER
    per = safe_float(info.get("trailingPE")) or safe_float(info.get("forwardPE"))

    # 10. Momentum
    try:
        hist_all = t.history(period="max")
        hist_all.index = hist_all.index.tz_localize(None)
        ref_all  = yf.Ticker("IWDA.AS").history(period="max")
        ref_all.index = ref_all.index.tz_localize(None)
        def sp(years):
            cut = datetime.today() - timedelta(days=365*years)
            sub = hist_all[hist_all.index >= pd.Timestamp(cut)]
            return (sub["Close"].iloc[-1]/sub["Close"].iloc[0]-1)*100 if len(sub)>5 else None
        def rp(years):
            cut = datetime.today() - timedelta(days=365*years)
            sub = ref_all[ref_all.index >= pd.Timestamp(cut)]
            return (sub["Close"].iloc[-1]/sub["Close"].iloc[0]-1)*100 if len(sub)>5 else None
        s5,s10 = sp(5), sp(10)
        r5,r10 = rp(5), rp(10)
        if s10 and r10:   mom_ok = s10>r10; mom_str = f"+{s10:.0f}% vs +{r10:.0f}%"
        elif s5 and r5:   mom_ok = s5>r5;   mom_str = f"+{s5:.0f}% vs +{r5:.0f}%"
        else: mom_ok = None; mom_str = None
    except: mom_ok = None; mom_str = None; s5 = s10 = r5 = r10 = None

    # Evaluate
    def evaluate(val, good, bad, higher=True):
        v = safe_float(val)
        if v is None: return "n"
        if higher:
            if v >= good: return "g"
            if v <= bad:  return "r"
            return "y"
        else:
            if v <= good: return "g"
            if v >= bad:  return "r"
            return "y"

    statuses = [
        evaluate(rev_cagr, 0.10, 0.03),
        "g" if buyback is True else ("r" if buyback is False else "n"),
        evaluate(roic, 0.20, 0.05),
        evaluate(fcf_margin, 0.20, 0.03),
        evaluate(div_cagr, 0.10, 0.03),
        evaluate(payout, 0.60, 0.90, higher=False),
        evaluate(fcf_cagr, 0.10, 0.03),
        evaluate(d_ebitda, 1.5, 5.0, higher=False),
        evaluate(per, 20, 40, higher=False),
        "g" if mom_ok is True else ("r" if mom_ok is False else "n"),
    ]

    score100 = 0.0
    for i, (num, w) in enumerate(WEIGHTS.items()):
        cl = statuses[i]
        if cl == "g":   score100 += w
        elif cl == "y": score100 += w * 0.5

    name    = info.get("longName") or info.get("shortName") or ticker_str
    cur_px  = info.get("currentPrice") or info.get("regularMarketPrice")
    sector  = info.get("sector", "—")

    return {
        "Ticker":  ticker_str,
        "Nom":     name[:35] + ("…" if len(name) > 35 else ""),
        "Secteur": sector,
        "Cours":   cur_px,
        "Score":   int(round(score100)),
        # Valeurs brutes
        "CA CAGR":      fmt_pct_safe(rev_cagr),
        "Rachat":       "Oui" if buyback is True else ("Non" if buyback is False else "N/A"),
        "ROIC":         fmt_pct_safe(roic),
        "Marge FCF":    fmt_pct_safe(fcf_margin),
        "Div CAGR":     fmt_pct_safe(div_cagr),
        "Payout":       fmt_pct_safe(payout),
        "FCF CAGR":     fmt_pct_safe(fcf_cagr),
        "D/EBITDA":     fmt_num(d_ebitda),
        "PER":          fmt_num(per, 1),
        "Momentum":     mom_str if mom_str else "N/A",
        # Statuts (g/r/y/n)
        "_st": statuses,
        # Valeurs brutes numériques pour le filtre
        "_raw": {
            "rev_cagr": rev_cagr, "roic": roic, "fcf_margin": fcf_margin,
            "div_cagr": div_cagr, "payout": payout, "fcf_cagr": fcf_cagr,
            "d_ebitda": d_ebitda, "per": per,
        }
    }


def page_screener():
    st.markdown('<div class="ph"><div class="ph-title">Screener Multi-Actions</div>'
                '<div class="ph-sub">▸ Analyse 10-Baggers · Comparaison en masse</div></div>',
                unsafe_allow_html=True)

    # ── Initialisation session state ──────────────────────────────────────────
    if "screener_results" not in st.session_state:
        st.session_state.screener_results = []
    if "screener_tickers_text" not in st.session_state:
        st.session_state.screener_tickers_text = ", ".join(DEFAULT_SCREENER_TICKERS)
    if "screener_view" not in st.session_state:
        st.session_state.screener_view = "Statuts (OK/Neutre/Non)"

    # ── Panneau de configuration ──────────────────────────────────────────────
    col_cfg, col_opt = st.columns([3, 1])

    with col_cfg:
        ticker_text = st.text_area(
            "Tickers à analyser (séparés par virgules ou espaces)",
            value=st.session_state.screener_tickers_text,
            height=80,
            key="screener_ticker_input",
            label_visibility="collapsed",
            placeholder="AIR.PA, MC.PA, RNL.PA, CDI.PA, …",
        )
        st.session_state.screener_tickers_text = ticker_text

    with col_opt:
        if st.button("⊞  Charger tous les tickers PEA .PA", use_container_width=True):
            st.session_state.screener_tickers_text = ", ".join(PEA_FR_TICKERS)
            st.rerun()
        if st.button("↺  Réinitialiser la liste", use_container_width=True):
            st.session_state.screener_tickers_text = ", ".join(DEFAULT_SCREENER_TICKERS)
            st.rerun()

    # Parse tickers
    raw = ticker_text.replace(",", " ").replace(";", " ").split()
    tickers_to_run = [t.strip().upper() for t in raw if t.strip()]

    c1, c2 = st.columns([1, 2])
    with c1:
        run_btn = st.button("▶  Lancer le calcul", use_container_width=True, type="primary")
    with c2:
        view_mode = st.radio(
            "Affichage",
            ["Statuts (OK/Neutre/Non)", "Valeurs brutes"],
            horizontal=True,
            key="view_mode_radio",
            label_visibility="collapsed",
        )
        st.session_state.screener_view = view_mode

    # ── Calcul ────────────────────────────────────────────────────────────────
    if run_btn and tickers_to_run:
        results = []
        progress_bar = st.progress(0, text="Initialisation…")
        status_text  = st.empty()

        for i, tk in enumerate(tickers_to_run):
            pct = int((i / len(tickers_to_run)) * 100)
            progress_bar.progress(pct, text=f"Analyse {tk}…  ({i+1}/{len(tickers_to_run)})")
            status_text.markdown(
                f'<div style="font-family:DM Mono,monospace;font-size:0.68rem;color:var(--t2)">'
                f'⟳ Récupération · <span style="color:var(--green)">{tk}</span></div>',
                unsafe_allow_html=True,
            )
            data = compute_10bagger_data(tk)
            if data:
                results.append(data)

        progress_bar.progress(100, text="Terminé ✓")
        status_text.empty()
        st.session_state.screener_results = results

    results = st.session_state.screener_results

    if not results:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">⊞</div>
          <div class="empty-title">Configurez votre liste et lancez le calcul</div>
          <div class="empty-sub">Les données sont récupérées une par une depuis yfinance.<br>
          Comptez ~3-5 sec par action.</div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Filtres ───────────────────────────────────────────────────────────────
    section_label("Filtres")

    col_sf, col_sf2, col_sf3, col_sf4 = st.columns(4)
    with col_sf:
        min_score = st.slider("Score minimum", 0, 100, 0, 5, key="filter_score")
    with col_sf2:
        filter_sector = st.selectbox(
            "Secteur",
            ["Tous"] + sorted(list({r["Secteur"] for r in results if r["Secteur"] != "—"})),
            key="filter_sector",
        )
    with col_sf3:
        sort_by = st.selectbox("Trier par", ["Score ↓", "Score ↑", "Ticker A→Z"], key="sort_by")
    with col_sf4:
        accept_na     = st.toggle("Accepter N/A",    value=True,  key="accept_na")
        accept_neutre = st.toggle("Accepter Neutre", value=True,  key="accept_neutre")

    # Filtres sur critères (mode statuts)
    if view_mode == "Statuts (OK/Neutre/Non)":
        filter_criteria = st.multiselect(
            "Critères obligatoirement ✓ OK (les actions ne respectant pas ces critères sont exclues)",
            CRITERIA_LABELS, key="filter_criteria",
        )
    else:
        filter_criteria = []

    # Filtres valeurs brutes numériques (mode valeurs brutes)
    if view_mode == "Valeurs brutes":
        # Collect available ranges
        raw_keys = {
            "CA CAGR (%)":     ("rev_cagr",   -50, 100, True),
            "ROIC (%)":        ("roic",        -50, 100, True),
            "Marge FCF (%)":   ("fcf_margin",  -50, 100, True),
            "Div CAGR (%)":    ("div_cagr",    -50, 100, True),
            "Payout (%)":      ("payout",        0, 200, False),
            "FCF CAGR (%)":    ("fcf_cagr",    -50, 100, True),
            "D/EBITDA":        ("d_ebitda",      0,  30, False),
            "PER":             ("per",           0, 100, False),
        }
        raw_filters = {}
        rw_cols = st.columns(4)
        col_i = 0
        for lbl, (key, vmin, vmax, is_pct) in raw_keys.items():
            vals = [r["_raw"].get(key) for r in results if r["_raw"].get(key) is not None]
            if not vals:
                continue
            scale = 100 if is_pct else 1
            actual_min = max(vmin, int(min(vals)*scale) - 5)
            actual_max = min(vmax, int(max(vals)*scale) + 5)
            if actual_min >= actual_max:
                continue
            with rw_cols[col_i % 4]:
                sel_range = st.slider(
                    lbl, actual_min, actual_max, (actual_min, actual_max),
                    key=f"raw_filter_{key}"
                )
                raw_filters[key] = (sel_range[0] / scale, sel_range[1] / scale, is_pct)
            col_i += 1

        # Filter Rachat selectbox
        with rw_cols[col_i % 4]:
            filter_rachat = st.selectbox("Rachat", ["Tous", "Oui", "Non", "N/A"], key="filter_rachat")
        col_i += 1
    else:
        raw_filters  = {}
        filter_rachat = "Tous"

    # ── Application des filtres ───────────────────────────────────────────────
    filtered = [r for r in results if r["Score"] >= min_score]
    if filter_sector != "Tous":
        filtered = [r for r in filtered if r["Secteur"] == filter_sector]

    # Filtre critères (statuts)
    if filter_criteria:
        def passes_criteria(r):
            for label in filter_criteria:
                idx = CRITERIA_LABELS.index(label)
                st_code = r["_st"][idx]
                if st_code == "g":
                    pass  # OK
                elif st_code == "n" and accept_na:
                    pass  # N/A accepté
                elif st_code == "y" and accept_neutre:
                    pass  # Neutre accepté
                else:
                    return False
            return True
        filtered = [r for r in filtered if passes_criteria(r)]

    # Filtre valeurs brutes
    for key, (lo, hi, is_pct) in raw_filters.items():
        def _rf(r, k=key, l=lo, h=hi):
            v = r["_raw"].get(k)
            if v is None:
                return accept_na
            return l <= v <= h
        filtered = [r for r in filtered if _rf(r)]
    if filter_rachat != "Tous":
        filtered = [r for r in filtered if r["Rachat"] == filter_rachat]

    # Tri
    if sort_by == "Score ↓":
        filtered = sorted(filtered, key=lambda x: x["Score"], reverse=True)
    elif sort_by == "Score ↑":
        filtered = sorted(filtered, key=lambda x: x["Score"])
    else:
        filtered = sorted(filtered, key=lambda x: x["Ticker"])

    # ── Résumé ────────────────────────────────────────────────────────────────
    n_excellent = sum(1 for r in filtered if r["Score"] >= 70)
    n_correct   = sum(1 for r in filtered if 50 <= r["Score"] < 70)
    n_insuf     = sum(1 for r in filtered if r["Score"] < 50)

    kpi_html = (
        '<div class="kpi-row" style="grid-template-columns:repeat(4,1fr)">'
        + kpi_card("Actions analysées", str(len(results)), top_color="linear-gradient(90deg,#3b82f6,transparent)")
        + kpi_card("Affichées", str(len(filtered)), top_color="linear-gradient(90deg,#8b5cf6,transparent)")
        + kpi_card("Score ≥ 70 · Excellent", str(n_excellent), top_color="linear-gradient(90deg,#22c55e,transparent)")
        + kpi_card("Score 50–69 · Correct", str(n_correct), top_color="linear-gradient(90deg,#f59e0b,transparent)")
        + '</div>'
    )
    st.markdown(kpi_html, unsafe_allow_html=True)

    section_label(f"Résultats — {len(filtered)} actions")

    # ── Tableau ───────────────────────────────────────────────────────────────
    STATUS_ICON  = {"g": "✓", "r": "✗", "y": "◐", "n": "○"}
    STATUS_COLOR = {"g": "#22c55e", "r": "#ef4444", "y": "#f59e0b", "n": "#475569"}
    STATUS_LABEL = {"g": "OK", "r": "Non", "y": "Neutre", "n": "N/A"}

    def score_badge(sc):
        c = "#22c55e" if sc >= 70 else ("#f59e0b" if sc >= 50 else "#ef4444")
        return (f'<span style="font-family:Outfit,sans-serif;font-weight:700;'
                f'font-size:1rem;color:{c}">{sc}</span>')

    def status_cell(st_code):
        ic  = STATUS_ICON[st_code]
        col = STATUS_COLOR[st_code]
        lbl = STATUS_LABEL[st_code]
        return (f'<span style="font-family:DM Mono,monospace;font-size:0.68rem;'
                f'font-weight:600;color:{col}">{ic} {lbl}</span>')

    def raw_cell(val):
        return f'<span style="font-family:DM Mono,monospace;font-size:0.72rem;color:var(--t2)">{val}</span>'

    # Header
    crit_headers = "".join(f"<th>{lbl}</th>" for lbl in CRITERIA_LABELS)
    thead = (
        '<thead><tr>'
        '<th style="text-align:left">Ticker</th>'
        '<th style="text-align:left">Nom</th>'
        '<th style="text-align:left">Secteur</th>'
        '<th>Cours</th>'
        '<th>Score</th>'
        + crit_headers +
        '</tr></thead>'
    )

    tbody = ""
    for r in filtered:
        cours_str = f"{r['Cours']:.2f} €" if r["Cours"] else "—"
        sc_c = "#22c55e" if r["Score"] >= 70 else ("#f59e0b" if r["Score"] >= 50 else "#ef4444")

        if view_mode == "Valeurs brutes":
            vals = [r["CA CAGR"], r["Rachat"], r["ROIC"], r["Marge FCF"],
                    r["Div CAGR"], r["Payout"], r["FCF CAGR"], r["D/EBITDA"],
                    r["PER"], r["Momentum"]]
            crit_cells = "".join(f"<td>{raw_cell(v)}</td>" for v in vals)
        else:
            crit_cells = "".join(
                f'<td>{status_cell(s)}</td>'
                for s in r["_st"]
            )

        tbody += (
            f'<tr>'
            f'<td style="text-align:left"><span style="font-family:DM Mono,monospace;'
            f'font-size:0.78rem;color:#22c55e;font-weight:600">{r["Ticker"]}</span></td>'
            f'<td style="text-align:left;font-size:0.82rem;max-width:180px;white-space:nowrap;'
            f'overflow:hidden;text-overflow:ellipsis">{r["Nom"]}</td>'
            f'<td style="text-align:left;font-size:0.72rem;color:var(--t3)">{r["Secteur"]}</td>'
            f'<td><span style="font-family:DM Mono,monospace;font-size:0.78rem">{cours_str}</span></td>'
            f'<td>{score_badge(r["Score"])}</td>'
            + crit_cells +
            f'</tr>'
        )

    table_html = (
        '<div style="overflow-x:auto;background:var(--s1);border:1px solid var(--border);'
        'border-radius:11px;margin-bottom:2rem">'
        f'<table class="ptable" style="min-width:1200px">{thead}<tbody>{tbody}</tbody></table>'
        '</div>'
    )
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Export CSV ────────────────────────────────────────────────────────────
    if filtered:
        rows_export = []
        for r in filtered:
            row_d = {
                "Ticker": r["Ticker"], "Nom": r["Nom"], "Secteur": r["Secteur"],
                "Cours": r["Cours"], "Score": r["Score"],
                "CA CAGR": r["CA CAGR"], "Rachat": r["Rachat"], "ROIC": r["ROIC"],
                "Marge FCF": r["Marge FCF"], "Div CAGR": r["Div CAGR"],
                "Payout": r["Payout"], "FCF CAGR": r["FCF CAGR"], "D/EBITDA": r["D/EBITDA"],
                "PER": r["PER"], "Momentum": r["Momentum"],
            }
            rows_export.append(row_d)
        df_export = pd.DataFrame(rows_export)
        csv_data  = df_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇  Exporter CSV",
            data=csv_data,
            file_name="screener_10baggers.csv",
            mime="text/csv",
            use_container_width=False,
        )


# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""<div class="nav-logo">
      <span class="dot"></span>
      <div>PEA<span class="sub">Dashboard · Finance</span></div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("Navigation",
        options=["▸  Portefeuille", "◎  Analyse 10-Baggers", "⊞  Screener Multi-Actions"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-section">Sources de données</div>', unsafe_allow_html=True)
    for f in ["Historique.xlsx", "Corrrespondance.xlsx", "Versements.xlsx"]:
        st.markdown(f'<div class="file-pill">{f}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⟳  Rafraîchir les données", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.52rem;color:#2d3f55;'
                'margin-top:1.8rem;line-height:2.2;text-align:center">yfinance · cache 5 min</div>',
                unsafe_allow_html=True)

if "Portefeuille" in page:
    page_portfolio()
elif "10-Baggers" in page:
    page_10baggers()
else:
    page_screener()