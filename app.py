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
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=DM+Mono:ital,wght@0,300;0,400;0,500&display=swap');
:root{
  --bg:#05070e;--s1:#090d18;--s2:#0e1420;--s3:#131c2e;--s4:#1a2438;
  --border:#1a2538;--b2:#223047;--b3:#2d3f5a;
  --green:#22c55e;--green2:#16a34a;--red:#ef4444;--amber:#f59e0b;--blue:#3b82f6;--purple:#8b5cf6;
  --green-bg:rgba(34,197,94,0.06);--red-bg:rgba(239,68,68,0.06);
  --amber-bg:rgba(245,158,11,0.06);--blue-bg:rgba(59,130,246,0.06);
  --glow-green:0 0 20px rgba(34,197,94,0.15);
  --text:#f1f5f9;--t2:#94a3b8;--t3:#475569;--t4:#2d3f57;
}
*{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Outfit',sans-serif!important;font-size:15px!important;}
.main .block-container{padding:0.1rem 2rem 3rem!important;max-width:1580px!important;}
.stApp{background:var(--bg)!important;}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#080c16 0%,#060a12 100%)!important;
  border-right:1px solid var(--border)!important;}
section[data-testid="stSidebar"] .block-container{padding:1.4rem 1.1rem!important;}
#MainMenu,footer,header{visibility:hidden!important;}
.stDeployButton{display:none!important;}

/* ── Remove top padding ── */
.block-container{padding-top:0!important;margin-top:0!important;}
[data-testid="stHeader"]{display:none!important;height:0!important;min-height:0!important;}
div[data-testid="stDecoration"]{display:none!important;height:0!important;}
[data-testid="stAppViewBlockContainer"]{padding-top:0!important;}
.stMainBlockContainer{padding-top:0!important;}
.main > div{padding-top:0!important;}
iframe[height="0"]{height:0!important;min-height:0!important;max-height:0!important;
  display:block!important;margin:0!important;padding:0!important;border:none!important;overflow:hidden!important;}
div[data-testid="stCustomComponentV1"]{height:0!important;min-height:0!important;overflow:hidden!important;margin:0!important;}

/* ── Sidebar nav logo ── */
.nav-logo{font-family:'Outfit',sans-serif;font-weight:900;font-size:1.05rem;color:var(--text);
  letter-spacing:-0.03em;padding-bottom:1.1rem;border-bottom:1px solid var(--border);
  margin-bottom:1rem;display:flex;align-items:center;gap:10px;}
.nav-logo .dot{width:7px;height:7px;border-radius:50%;background:var(--green);
  box-shadow:0 0 0 2px rgba(34,197,94,0.2),0 0 12px var(--green);flex-shrink:0;
  animation:pulse-dot 2.4s ease-in-out infinite;}
@keyframes pulse-dot{0%,100%{box-shadow:0 0 0 2px rgba(34,197,94,0.2),0 0 12px var(--green);}
  50%{box-shadow:0 0 0 4px rgba(34,197,94,0.1),0 0 20px var(--green);}}
.nav-logo .sub{font-size:0.55rem;color:var(--t4);font-weight:400;letter-spacing:0.15em;
  text-transform:uppercase;display:block;margin-top:2px;}

/* ── Nav radio ── */
.stRadio>div{gap:1px!important;}
.stRadio>div>label{
  font-family:'Outfit',sans-serif!important;font-size:0.8rem!important;font-weight:500!important;
  color:var(--t3)!important;padding:9px 12px!important;border-radius:7px!important;
  border:none!important;transition:all .18s ease!important;cursor:pointer!important;width:100%!important;}
.stRadio>div>label:hover{color:var(--t2)!important;background:var(--s2)!important;}
.stRadio>div>label>div:first-child{display:none!important;}
.stRadio>div>label p{margin:0!important;font-family:'Outfit',sans-serif!important;
  font-size:0.8rem!important;font-weight:500!important;color:inherit!important;}

.nav-section{font-family:'DM Mono',monospace;font-size:0.52rem;color:var(--t4);
  text-transform:uppercase;letter-spacing:0.16em;margin:1.4rem 0 0.6rem;}
.nav-divider{height:1px;background:var(--border);margin:1.1rem 0;}
.file-pill{font-family:'DM Mono',monospace;font-size:0.58rem;color:var(--t3);
  padding:3px 0;display:flex;align-items:center;gap:7px;}
.file-pill::before{content:'·';color:var(--green);font-size:0.9rem;line-height:1;}

.stButton>button{font-family:'DM Mono',monospace!important;font-size:0.68rem!important;
  color:var(--t3)!important;background:transparent!important;border:1px solid var(--border)!important;
  border-radius:7px!important;padding:7px 12px!important;width:100%;transition:all .18s;}
.stButton>button:hover{color:var(--text)!important;border-color:var(--b3)!important;
  background:var(--s2)!important;}

/* ── Page header ── */
.ph{margin-bottom:1.8rem;padding-top:0;position:relative;}
.ph-eyebrow{font-family:'DM Mono',monospace;font-size:0.6rem;color:var(--green);
  letter-spacing:0.2em;text-transform:uppercase;margin-bottom:6px;opacity:0.8;}
.ph-title{font-family:'Outfit',sans-serif;font-weight:900;font-size:2.1rem;
  color:var(--text);letter-spacing:-0.04em;line-height:1;margin-bottom:6px;
  background:linear-gradient(135deg,#f1f5f9 30%,#94a3b8 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.ph-sub{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--t3);
  letter-spacing:0.1em;text-transform:uppercase;display:flex;align-items:center;gap:10px;}
.ph-sub::before{content:'';display:inline-block;width:20px;height:1px;background:var(--green);opacity:0.5;}
.ph-clock{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--t3);
  margin-left:auto;}

/* ── KPI cards ── */
.kpi-row{display:grid;gap:10px;margin-bottom:1.8rem;}
.kpi{background:var(--s1);border:1px solid var(--border);border-radius:12px;
  padding:18px 20px;position:relative;overflow:hidden;transition:border-color .2s,box-shadow .2s;
  cursor:default;}
.kpi:hover{border-color:var(--b3);box-shadow:0 4px 24px rgba(0,0,0,0.4);}
.kpi::before{content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse at top left,rgba(34,197,94,0.03) 0%,transparent 60%);
  pointer-events:none;}
.kpi-top{height:2px;position:absolute;top:0;left:0;right:0;border-radius:12px 12px 0 0;}
.kpi-lbl{font-family:'DM Mono',monospace;font-size:0.58rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.12em;margin-bottom:10px;}
.kpi-val{font-family:'Outfit',sans-serif;font-size:1.7rem;font-weight:800;
  color:var(--text);line-height:1;margin-bottom:7px;letter-spacing:-0.02em;}
.kpi-d{font-family:'DM Mono',monospace;font-size:0.68rem;}
.kpi-d.g{color:var(--green);}.kpi-d.r{color:var(--red);}.kpi-d.n{color:var(--t3);}

/* ── Section label ── */
.sl{font-family:'DM Mono',monospace;font-size:0.58rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.16em;margin:2rem 0 1.1rem;
  display:flex;align-items:center;gap:12px;}
.sl::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent);}

/* ── Perf cards ── */
.perf-row{display:grid;gap:8px;margin-bottom:1.6rem;}
.perf-c{background:var(--s1);border:1px solid var(--border);border-radius:9px;
  padding:14px 12px;text-align:center;transition:border-color .2s;}
.perf-c:hover{border-color:var(--b3);}
.perf-c.hl{border-color:rgba(245,158,11,0.4);background:var(--amber-bg);}
.perf-lbl{font-family:'DM Mono',monospace;font-size:0.58rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.1em;margin-bottom:5px;}
.perf-lbl.h{color:var(--amber);}
.perf-v{font-family:'Outfit',sans-serif;font-size:1.3rem;font-weight:700;line-height:1;}
.perf-abs{font-family:'DM Mono',monospace;font-size:0.62rem;margin-top:4px;}

/* ── Positions table ── */
.ptable{width:100%;border-collapse:collapse;}
.ptable th{font-family:'DM Mono',monospace;font-size:0.58rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.08em;padding:10px 14px;text-align:right;
  border-bottom:1px solid var(--border);background:var(--s2);}
.ptable th:first-child{text-align:left;}
.ptable td{font-family:'Outfit',sans-serif;font-size:0.87rem;color:var(--t2);
  padding:11px 14px;text-align:right;border-bottom:1px solid rgba(26,37,56,0.6);}
.ptable td:first-child{text-align:left;color:var(--text);font-weight:500;}
.ptable tr:hover td{background:var(--s2);}
.tbadge{font-family:'DM Mono',monospace;font-size:0.6rem;color:var(--blue);
  background:var(--blue-bg);border:1px solid rgba(59,130,246,0.18);
  padding:2px 6px;border-radius:3px;margin-left:7px;}
.pos{color:var(--green)!important;font-weight:600;}
.neg{color:var(--red)!important;font-weight:600;}

/* ── Date inputs ── */
.stDateInput input{background:var(--s2)!important;border:1px solid var(--border)!important;
  color:var(--text)!important;font-family:'DM Mono',monospace!important;
  font-size:0.75rem!important;border-radius:7px!important;}

/* ── Ticker input ── */
.stTextInput input{background:var(--s1)!important;border:1px solid var(--border)!important;
  color:var(--text)!important;font-family:'DM Mono',monospace!important;
  font-size:0.92rem!important;border-radius:10px!important;padding:13px 17px!important;
  letter-spacing:0.04em!important;transition:border-color .2s,box-shadow .2s!important;}
.stTextInput input:focus{border-color:var(--green)!important;
  box-shadow:0 0 0 3px rgba(34,197,94,0.1)!important;}
.stTextInput input::placeholder{color:var(--t4)!important;}

/* ── Stock perf strip ── */
.stock-perf-strip{display:flex;gap:7px;margin:10px 0 16px;flex-wrap:wrap;}
.sp-item{background:var(--s1);border:1px solid var(--border);border-radius:8px;
  padding:8px 14px;text-align:center;flex:1;min-width:80px;transition:border-color .2s;}
.sp-item:hover{border-color:var(--b3);}
.sp-lbl{font-family:'DM Mono',monospace;font-size:0.55rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;}
.sp-val{font-family:'Outfit',sans-serif;font-size:0.92rem;font-weight:700;}

/* ── Criteria rows ── */
.cr{display:flex;align-items:center;padding:12px 16px;border-radius:9px;
  margin:4px 0;border:1px solid transparent;gap:12px;position:relative;
  transition:transform .15s,box-shadow .15s;}
.cr:hover{transform:translateX(2px);}
.cr.g{background:var(--green-bg);border-color:rgba(34,197,94,0.2);}
.cr.r{background:var(--red-bg);border-color:rgba(239,68,68,0.2);}
.cr.y{background:var(--amber-bg);border-color:rgba(245,158,11,0.2);}
.cr.n{background:var(--s1);border-color:var(--border);}
.cr-badge{width:26px;height:26px;border-radius:6px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:0.78rem;font-weight:700;}
.cr-badge.g{background:rgba(34,197,94,0.14);color:var(--green);}
.cr-badge.r{background:rgba(239,68,68,0.14);color:var(--red);}
.cr-badge.y{background:rgba(245,158,11,0.14);color:var(--amber);}
.cr-badge.n{background:var(--s2);color:var(--t3);}
.cr-num{font-family:'DM Mono',monospace;font-size:0.58rem;color:var(--t4);width:18px;flex-shrink:0;}
.cr-name{font-family:'Outfit',sans-serif;font-size:0.86rem;color:var(--text);font-weight:500;flex:1;}
.cr-val{font-family:'DM Mono',monospace;font-size:0.82rem;font-weight:500;width:95px;text-align:right;}
.cr-val.g{color:var(--green);}.cr-val.r{color:var(--red);}
.cr-val.y{color:var(--amber);}.cr-val.n{color:var(--t3);}
.cr-thresh{font-family:'DM Mono',monospace;font-size:0.56rem;color:var(--t3);
  width:130px;text-align:right;line-height:1.9;}
.cr-thresh .tg{color:rgba(34,197,94,0.6);}.cr-thresh .tr{color:rgba(239,68,68,0.6);}
.cr-tip{position:relative;display:flex;align-items:center;flex:1;gap:8px;}
.tip-icon{font-family:'DM Mono',monospace;font-size:0.52rem;color:var(--t3);
  background:var(--s2);border:1px solid var(--border);border-radius:3px;
  padding:1px 5px;cursor:help;flex-shrink:0;transition:color .15s,border-color .15s;}
.cr-tip:hover .tip-icon{color:var(--blue);border-color:rgba(59,130,246,0.4);}
.tip-box{display:none;position:absolute;left:0;top:calc(100% + 6px);z-index:9999;
  background:var(--s3);border:1px solid var(--b2);border-radius:10px;
  padding:12px 15px;width:295px;box-shadow:0 16px 40px rgba(0,0,0,0.7);}
.tip-t{font-family:'Outfit',sans-serif;font-size:0.77rem;font-weight:600;
  color:var(--text);margin-bottom:6px;}
.tip-d{font-family:'Outfit',sans-serif;font-size:0.73rem;color:var(--t2);line-height:1.65;}
.cr-tip:hover .tip-box{display:block;}

/* ── Score ring card ── */
.score-card{background:linear-gradient(145deg,var(--s1) 0%,var(--s2) 100%);
  border:1px solid var(--border);border-radius:14px;
  padding:28px 22px;text-align:center;position:relative;overflow:hidden;}
.score-card::before{content:'';position:absolute;top:-40px;left:50%;transform:translateX(-50%);
  width:160px;height:160px;border-radius:50%;
  background:radial-gradient(circle,rgba(34,197,94,0.06) 0%,transparent 70%);
  pointer-events:none;}
.score-lbl{font-family:'DM Mono',monospace;font-size:0.6rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.12em;margin-bottom:14px;}
.score-ring{position:relative;display:inline-block;margin-bottom:10px;}
.score-ring svg{transform:rotate(-90deg);}
.score-ring-val{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-family:'Outfit',sans-serif;font-size:2.6rem;font-weight:900;line-height:1;
  letter-spacing:-0.03em;}
.score-ring-sub{position:absolute;bottom:18%;left:50%;transform:translateX(-50%);
  font-family:'DM Mono',monospace;font-size:0.52rem;color:var(--t3);white-space:nowrap;}
.score-verdict{font-family:'DM Mono',monospace;font-size:0.65rem;font-weight:600;
  letter-spacing:0.12em;margin-top:2px;}
.score-counts{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-top:12px;}
.sc-pill{font-family:'DM Mono',monospace;font-size:0.62rem;font-weight:500;
  padding:4px 9px;border-radius:5px;border:1px solid transparent;}
.sc-pill.g{background:rgba(34,197,94,0.1);border-color:rgba(34,197,94,0.25);color:var(--green);}
.sc-pill.r{background:rgba(239,68,68,0.1);border-color:rgba(239,68,68,0.25);color:var(--red);}
.sc-pill.y{background:rgba(245,158,11,0.1);border-color:rgba(245,158,11,0.25);color:var(--amber);}
.sc-pill.n{background:var(--s2);border-color:var(--border);color:var(--t3);}
.score-w{font-family:'DM Mono',monospace;font-size:0.57rem;color:var(--t3);line-height:2.1;
  margin-top:14px;border-top:1px solid var(--border);padding-top:12px;text-align:left;}
.score-w span{color:var(--t2);}

/* ── Legend ── */
.legend-strip{display:flex;gap:12px;margin-bottom:0.9rem;flex-wrap:wrap;}
.legend-item{display:flex;align-items:center;gap:6px;
  font-family:'DM Mono',monospace;font-size:0.63rem;color:var(--t2);}
.legend-dot{width:8px;height:8px;border-radius:2px;}

/* ── Company header ── */
.company-header{
  background:linear-gradient(135deg,var(--s1) 0%,var(--s2) 100%);
  border:1px solid var(--border);border-radius:14px;
  padding:22px 28px;margin-bottom:1.5rem;display:flex;align-items:center;gap:28px;flex-wrap:wrap;
  position:relative;overflow:hidden;}
.company-header::after{content:'';position:absolute;right:-20px;top:-20px;
  width:120px;height:120px;border-radius:50%;
  background:radial-gradient(circle,rgba(34,197,94,0.04) 0%,transparent 70%);}
.company-name{font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:800;
  color:var(--text);letter-spacing:-0.02em;}
.company-ticker{font-family:'DM Mono',monospace;font-size:0.68rem;color:var(--green);
  letter-spacing:0.1em;margin-top:3px;}
.company-meta{display:flex;gap:24px;margin-left:auto;align-items:center;flex-wrap:wrap;}
.meta-lbl{font-family:'DM Mono',monospace;font-size:0.55rem;color:var(--t3);
  text-transform:uppercase;letter-spacing:0.1em;margin-bottom:3px;}
.meta-val{font-family:'Outfit',sans-serif;font-size:0.86rem;color:var(--t2);}
.price-box{background:var(--s3);border:1px solid var(--b2);border-radius:10px;
  padding:12px 22px;text-align:center;}
.price-lbl{font-family:'DM Mono',monospace;font-size:0.55rem;color:var(--t3);
  letter-spacing:0.08em;margin-bottom:4px;}
.price-val{font-family:'Outfit',sans-serif;font-size:1.45rem;font-weight:800;color:var(--green);}

/* ── Empty state ── */
.empty-state{background:var(--s1);border:1px solid var(--border);border-radius:14px;
  padding:70px 24px;text-align:center;margin-top:1.5rem;}
.empty-icon{font-size:2.4rem;color:var(--t4);margin-bottom:14px;}
.empty-title{font-family:'Outfit',sans-serif;font-size:1rem;font-weight:600;
  color:var(--t2);margin-bottom:8px;}
.empty-sub{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--t3);line-height:2.1;}

/* ── Expanders ── */
.streamlit-expanderHeader{font-family:'DM Mono',monospace!important;
  font-size:0.65rem!important;color:var(--t3)!important;
  text-transform:uppercase!important;letter-spacing:0.12em!important;}

/* ── Spinner / progress ── */
.stProgress > div > div{background:var(--green)!important;border-radius:4px!important;}
.stProgress > div{background:var(--s2)!important;border-radius:4px!important;}

/* ── Selectbox & multiselect ── */
.stSelectbox > div > div, .stMultiSelect > div > div{
  background:var(--s1)!important;border:1px solid var(--border)!important;
  border-radius:8px!important;color:var(--text)!important;}

/* ── Toggle ── */
.stToggle label{font-family:'DM Mono',monospace!important;font-size:0.7rem!important;color:var(--t2)!important;}

/* ── Screener mini score bar ── */
.mini-score-bar{display:inline-block;width:44px;height:4px;border-radius:2px;
  background:var(--s3);vertical-align:middle;margin-left:4px;overflow:hidden;position:relative;}
.mini-score-fill{height:100%;border-radius:2px;transition:width .3s;}
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
    var sidebar=P.querySelector('[data-testid="stSidebar"]');
    if(!sidebar) return;
    var labels=sidebar.querySelectorAll('.stRadio label');
    labels.forEach(function(lbl){
      var inp=lbl.querySelector('input[type="radio"]');
      if(!inp) return;
      if(inp.checked){
        lbl.style.cssText='color:#f1f5f9!important;background:#0e1420!important;border-left:2px solid #22c55e!important;padding-left:11px!important;border-radius:7px!important;';
      } else {
        lbl.style.cssText='color:#475569!important;background:transparent!important;border-left:none!important;padding-left:12px!important;border-radius:7px!important;';
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

// Live clock + market status in sidebar
(function liveClock(){
  var P=window.parent.document;
  // Create clock element once
  var clockEl=P.getElementById('_pea_clock');
  if(!clockEl){
    clockEl=P.createElement('div');
    clockEl.id='_pea_clock';
    clockEl.style.cssText='font-family:"DM Mono",monospace;font-size:0.58rem;color:#2d3f57;text-align:center;margin-top:auto;padding-top:8px;line-height:2;';
    var sidebar=P.querySelector('[data-testid="stSidebar"] .block-container');
    if(sidebar) sidebar.appendChild(clockEl);
  }
  function tick(){
    var now=new Date();
    var hh=String(now.getHours()).padStart(2,'0');
    var mm=String(now.getMinutes()).padStart(2,'0');
    var ss=String(now.getSeconds()).padStart(2,'0');
    var d=now.toLocaleDateString('fr-FR',{weekday:'short',day:'numeric',month:'short'});
    // Euronext Paris: 09:00-17:30 mon-fri
    var day=now.getDay(); var h=now.getHours(); var m=now.getMinutes();
    var open=(day>=1&&day<=5)&&((h>9||(h===9&&m>=0))&&(h<17||(h===17&&m<30)));
    var status=open?'<span style="color:#22c55e">● OUVERT</span>':'<span style="color:#475569">○ FERMÉ</span>';
    clockEl.innerHTML=hh+':'+mm+':'+ss+'<br>'+d+'<br>Euronext · '+status;
  }
  tick();
  setInterval(tick,1000);
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

# ── Benchmark personnalisable ─────────────────────────────────────────────────
BENCHMARKS_AVAILABLE = {
    "MSCI World (IWDA)":      "IWDA.AS",
    "CAC 40":                 "^FCHI",
    "S&P 500":                "^GSPC",
    "Stoxx Europe 600":       "EXSA.DE",
    "CAC Mid 60":             "^CACMD",
    "Nasdaq 100":             "^NDX",
    "MSCI Emerging Markets":  "EIMI.AS",
}

# ── Persistance locale (fichier JSON) ─────────────────────────────────────────
import json, os

STATE_FILE = "pea_state.json"

def _load_state() -> dict:
    """Charge l'état persistant depuis le fichier JSON local."""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {"journal": [], "alerts": [], "watchlist": [], "benchmark": "MSCI World (IWDA)"}

def _save_state(state: dict):
    """Sauvegarde l'état dans le fichier JSON local."""
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2, default=str)
    except:
        pass

def get_state(key: str, default=None):
    """Lit une valeur depuis le state persistant + session_state."""
    if f"_pstate_{key}" not in st.session_state:
        st.session_state[f"_pstate_{key}"] = _load_state().get(key, default)
    return st.session_state[f"_pstate_{key}"]

def set_state(key: str, value):
    """Écrit une valeur dans session_state + sauvegarde le fichier."""
    st.session_state[f"_pstate_{key}"] = value
    state = _load_state()
    state[key] = value
    _save_state(state)


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

def fix_yield(v):
    """yfinance retourne parfois dividendYield × 100. On normalise toujours en ratio (0.03 = 3%)."""
    f = safe_float(v)
    if f is None: return None
    if f > 1: f = f / 100   # ex: 1.93 → 0.0193
    return min(f, 0.25)     # cap 25% pour données corrompues

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
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">▸ PEA · Fortuneo</div>'
                '<div class="ph-title">Portefeuille</div>'
                '<div class="ph-sub">Valorisation temps réel</div>'
                '</div>',
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
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">◎ Analyse fondamentale</div>'
                '<div class="ph-title">10-Baggers</div>'
                '<div class="ph-sub">Checklist · Score pondéré /100</div>'
                '</div>',
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

    buyback = None
    try:
        bs_tmp = t.balance_sheet
        for field in ["Ordinary Shares Number", "Share Issued", "Common Stock"]:
            if field in bs_tmp.index:
                sh = bs_tmp.loc[field].dropna().sort_index()
                if len(sh) >= 2:
                    buyback = bool(sh.iloc[-1] < sh.iloc[0])
                    break
        if buyback is None:
            cf_tmp = t.cashflow
            for field in ["Repurchase Of Capital Stock", "Common Stock Repurchased",
                          "Repurchase of Common Stock"]:
                if field in cf_tmp.index:
                    val = cf_tmp.loc[field].dropna()
                    if not val.empty:
                        buyback = bool(float(val.iloc[0]) < 0)
                        break
    except:
        buyback = None

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
        # SVG ring parameters
        R = 54; CX = 70; CY = 70; SW = 7
        circumference = 2 * 3.14159 * R
        dash = circumference * sc / 100
        gap  = circumference - dash
        ring_color = sc_c
        # Animated SVG ring
        st.markdown(f"""<div class="score-card">
          <div class="score-lbl">Score de recommandation</div>
          <div class="score-ring">
            <svg width="140" height="140" viewBox="0 0 140 140">
              <circle cx="{CX}" cy="{CY}" r="{R}" fill="none"
                stroke="#1a2538" stroke-width="{SW}"/>
              <circle cx="{CX}" cy="{CY}" r="{R}" fill="none"
                stroke="{ring_color}" stroke-width="{SW}"
                stroke-linecap="round"
                stroke-dasharray="{dash:.1f} {gap:.1f}"
                style="transition:stroke-dasharray 1s ease;filter:drop-shadow(0 0 6px {ring_color}44)"/>
            </svg>
            <div class="score-ring-val" style="color:{ring_color}">{sc}</div>
            <div class="score-ring-sub">/100</div>
          </div>
          <div class="score-verdict" style="color:{ring_color}">{verdict}</div>
          <div class="score-counts">
            <span class="sc-pill g">✓ {greens}</span>
            <span class="sc-pill r">✗ {reds}</span>
            <span class="sc-pill y">◐ {yellows}</span>
            <span class="sc-pill n">○ {nas}</span>
          </div>
          <div class="score-w"><span>Pondérations (/100)</span><br>
            CA 15% · ROIC 15%<br>Marge FCF 12% · FCF 12%<br>
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
    dyield_raw = safe_float(info.get("dividendYield"))
    dyield = (dyield_raw / 100 if dyield_raw and dyield_raw > 1 else dyield_raw)

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
PEA_FR_TICKERS = [
"ALEUP.PA",
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

    # 2. Rachat — plusieurs méthodes de fallback
    buyback = None
    try:
        # Méthode 1 : évolution du nombre d'actions au bilan
        bs = t.balance_sheet
        for field in ["Ordinary Shares Number", "Share Issued", "Common Stock"]:
            if field in bs.index:
                sh = bs.loc[field].dropna().sort_index()
                if len(sh) >= 2:
                    buyback = bool(sh.iloc[-1] < sh.iloc[0])
                    break
        # Méthode 2 : Repurchase Of Capital Stock dans le cashflow
        if buyback is None:
            cf = t.cashflow
            for field in ["Repurchase Of Capital Stock", "Common Stock Repurchased",
                          "Purchase Of Business", "Repurchase of Common Stock"]:
                if field in cf.index:
                    val = cf.loc[field].dropna()
                    if not val.empty:
                        buyback = bool(float(val.iloc[0]) < 0)
                        break
        # Méthode 3 : info yfinance sharesOutstanding vs floatShares trend
        if buyback is None:
            so = info.get("sharesOutstanding")
            if so:
                # On ne peut pas comparer dans le temps ici, on laisse None
                pass
    except:
        buyback = None

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
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">⊞ Screening multi-actions</div>'
                '<div class="ph-title">Screener</div>'
                '<div class="ph-sub">10-Baggers · Comparaison en masse</div>'
                '</div>',
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
            import math
            vals = [r["_raw"].get(key) for r in results if r["_raw"].get(key) is not None]
            vals = [v for v in vals if math.isfinite(v)]
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
        bar = (f'<span class="mini-score-bar">'
               f'<span class="mini-score-fill" style="width:{sc}%;background:{c}"></span>'
               f'</span>')
        return (f'<span style="font-family:Outfit,sans-serif;font-weight:800;'
                f'font-size:1.05rem;color:{c};letter-spacing:-0.02em">{sc}</span>{bar}')

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
# PAGE 4 — INTELLIGENCE DE MARCHÉ
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def get_multi_history(tickers: tuple, period="1y"):
    """Fetch Close prices for multiple tickers, return aligned DataFrame."""
    frames = {}
    for tk in tickers:
        try:
            h = yf.Ticker(tk).history(period=period)["Close"]
            h.index = h.index.tz_localize(None)
            frames[tk] = h
        except:
            pass
    if not frames:
        return pd.DataFrame()
    df = pd.DataFrame(frames)
    df = df.dropna(how="all")
    return df

@st.cache_data(ttl=300)
def get_ticker_signals(ticker: str):
    """Compute technical signals for a single ticker."""
    try:
        h = yf.Ticker(ticker).history(period="1y")
        if h.empty or len(h) < 50:
            return None
        h.index = h.index.tz_localize(None)
        c = h["Close"]; v = h["Volume"]

        last   = float(c.iloc[-1])
        mm20   = float(c.rolling(20).mean().iloc[-1])
        mm50   = float(c.rolling(50).mean().iloc[-1])
        mm200  = float(c.rolling(200).mean().iloc[-1]) if len(c) >= 200 else None
        vol20  = float(v.rolling(20).mean().iloc[-1])
        vol_r  = float(v.iloc[-1]) / vol20 if vol20 > 0 else 1.0

        # RSI 14
        delta  = c.diff()
        gain   = delta.clip(lower=0).rolling(14).mean()
        loss   = (-delta.clip(upper=0)).rolling(14).mean()
        rs     = gain / loss.replace(0, np.nan)
        rsi    = float(100 - 100 / (1 + rs.iloc[-1]))

        # Bollinger
        bb_m   = c.rolling(20).mean()
        bb_s   = c.rolling(20).std()
        bb_u   = float((bb_m + 2*bb_s).iloc[-1])
        bb_l   = float((bb_m - 2*bb_s).iloc[-1])
        bb_pct = (last - bb_l) / (bb_u - bb_l) * 100 if bb_u != bb_l else 50

        # MACD
        ema12  = c.ewm(span=12).mean()
        ema26  = c.ewm(span=26).mean()
        macd   = ema12 - ema26
        signal = macd.ewm(span=9).mean()
        hist   = float((macd - signal).iloc[-1])

        # 52w
        w52_h  = float(c.rolling(252).max().iloc[-1]) if len(c) >= 252 else float(c.max())
        w52_l  = float(c.rolling(252).min().iloc[-1]) if len(c) >= 252 else float(c.min())
        pct_from_high = (last - w52_h) / w52_h * 100

        # Pattern detection
        signals = []
        if mm200 and last > mm200 and last > mm50 and last > mm20:
            signals.append(("TENDANCE HAUSSIÈRE", "g", "Au-dessus MM20/50/200"))
        elif mm200 and last < mm200:
            signals.append(("SOUS MM200", "r", "Tendance baissière LT"))
        if abs(last - mm50) / mm50 < 0.02:
            signals.append(("TEST MM50", "y", f"À {abs(last-mm50)/mm50*100:.1f}% de la MM50"))
        if mm200 and abs(last - mm200) / mm200 < 0.015:
            signals.append(("TEST MM200", "r", f"À {abs(last-mm200)/mm200*100:.1f}% de la MM200"))
        if rsi > 75:
            signals.append(("RSI SURACHETÉ", "r", f"RSI = {rsi:.0f}"))
        elif rsi < 28:
            signals.append(("RSI SURVENDU", "g", f"RSI = {rsi:.0f} — rebond possible"))
        if vol_r > 2.0 and last > c.iloc[-2]:
            signals.append(("BREAKOUT VOLUME", "g", f"Volume ×{vol_r:.1f} · Hausse"))
        elif vol_r > 2.0 and last < c.iloc[-2]:
            signals.append(("VOLUME BAISSIER", "r", f"Volume ×{vol_r:.1f} · Baisse"))
        if bb_pct > 90:
            signals.append(("BB BANDE HAUTE", "r", f"BB% = {bb_pct:.0f}% — retour possible"))
        elif bb_pct < 10:
            signals.append(("BB BANDE BASSE", "g", f"BB% = {bb_pct:.0f}% — rebond possible"))
        if hist > 0 and float(macd.iloc[-2]) < float(signal.iloc[-2]):
            signals.append(("MACD CROISEMENT ↑", "g", "Signal haussier CT"))
        elif hist < 0 and float(macd.iloc[-2]) > float(signal.iloc[-2]):
            signals.append(("MACD CROISEMENT ↓", "r", "Signal baissier CT"))
        if pct_from_high > -5:
            signals.append(("PROCHE SOMMET 52S", "y", f"{pct_from_high:+.1f}% du plus haut"))
        if not signals:
            signals.append(("NEUTRE", "n", "Pas de signal fort détecté"))

        return {
            "last": last, "mm20": mm20, "mm50": mm50, "mm200": mm200,
            "rsi": rsi, "bb_pct": bb_pct, "vol_r": vol_r, "hist": hist,
            "w52_h": w52_h, "w52_l": w52_l, "pct_from_high": pct_from_high,
            "signals": signals,
        }
    except:
        return None


def page_intelligence():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">◈ Analyse avancée</div>'
                '<div class="ph-title">Intelligence de Marché</div>'
                '<div class="ph-sub">Corrélations · Signaux · Alertes · Stress-test · Risque</div>'
                '</div>', unsafe_allow_html=True)

    # ── Chargement du portefeuille ────────────────────────────────────────────
    try:
        df_hist, df_corr, df_vers = load_data()
        df_pos, s = compute_portfolio(df_hist, df_corr, df_vers)
    except Exception as e:
        st.error(f"Fichiers introuvables : {e}")
        return

    if df_pos.empty:
        st.info("Aucune position pour l'analyse.")
        return

    # Tickers du portefeuille (avec cours dispo)
    port_tickers = [r["Ticker"] for _, r in df_pos.iterrows()
                    if r["Ticker"] and r["Ticker"] != "N/A"]
    # Actions seulement (pas ETF) pour les signaux techniques
    action_tickers = [r["Ticker"] for _, r in df_pos.iterrows()
                      if r["Ticker"] and r["Ticker"] != "N/A"
                      and r.get("Type", "Action") == "Action"]

    # Onglets internes
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "  ◫  Corrélations  ",
        "  ⚡  Signaux  ",
        "  🔔  Alertes  ",
        "  💥  Stress-test  ",
        "  ⚖  Concentration  ",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # ONGLET 1 — CORRÉLATIONS
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        section_label("Matrice de corrélations — Portefeuille + Indices")

        BENCHMARKS = {
            "CAC 40": "^FCHI", "MSCI World": "IWDA.AS",
            "S&P 500": "^GSPC", "EUR/USD": "EURUSD=X",
        }
        all_tickers_corr = port_tickers + list(BENCHMARKS.values())

        per_corr = st.radio("Période", ["3 mois", "6 mois", "1 an", "2 ans"],
                            horizontal=True, index=2, key="corr_period")
        period_map = {"3 mois": "3mo", "6 mois": "6mo", "1 an": "1y", "2 ans": "2y"}

        with st.spinner("Calcul des corrélations…"):
            df_prices = get_multi_history(tuple(all_tickers_corr), period_map[per_corr])

        if df_prices.empty or df_prices.shape[1] < 2:
            st.warning("Données insuffisantes pour la matrice.")
        else:
            rets = df_prices.pct_change().dropna()
            corr = rets.corr()

            # Rename benchmark columns
            rev_bench = {v: k for k, v in BENCHMARKS.items()}
            corr.columns = [rev_bench.get(c, c) for c in corr.columns]
            corr.index   = [rev_bench.get(c, c) for c in corr.index]

            # Heatmap
            z    = corr.values.tolist()
            lbls = list(corr.columns)
            n    = len(lbls)

            # Color: -1=red, 0=dark, 1=green
            fig_corr = go.Figure(go.Heatmap(
                z=z, x=lbls, y=lbls,
                colorscale=[
                    [0,   "#ef4444"], [0.35, "#1a2235"],
                    [0.5, "#0e1420"], [0.65, "#1a2235"],
                    [1,   "#22c55e"],
                ],
                zmin=-1, zmax=1,
                text=[[f"{v:.2f}" for v in row] for row in z],
                texttemplate="%{text}",
                textfont=dict(size=10, family="DM Mono"),
                hovertemplate="<b>%{y} × %{x}</b><br>Corrélation : %{z:.3f}<extra></extra>",
                colorbar=dict(thickness=12, len=0.8,
                              tickfont=dict(family="DM Mono", size=9, color="#475569")),
            ))
            fig_corr.update_layout(
                **plotly_base(max(340, n * 38),
                              {"tickfont": {"family": "DM Mono", "size": 9}}))
            fig_corr.update_layout(
                xaxis=dict(tickfont=dict(family="DM Mono", size=9), tickangle=-40,
                           gridcolor="rgba(0,0,0,0)"),
                margin=dict(l=90, r=20, t=20, b=90),
            )
            st.plotly_chart(fig_corr, use_container_width=True)

            # Alerte sur corrélations trop élevées entre positions
            high_corr = []
            for i in range(len(port_tickers)):
                for j in range(i+1, len(port_tickers)):
                    a = rev_bench.get(port_tickers[i], port_tickers[i])
                    b = rev_bench.get(port_tickers[j], port_tickers[j])
                    if a in corr.index and b in corr.columns:
                        v = corr.loc[a, b]
                        if abs(v) > 0.75:
                            high_corr.append((a, b, v))

            if high_corr:
                section_label("⚠ Corrélations élevées entre positions")
                html_hc = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px">'
                for a, b, v in sorted(high_corr, key=lambda x: -abs(x[2])):
                    c = "#ef4444" if v > 0 else "#3b82f6"
                    html_hc += (f'<div style="background:var(--s1);border:1px solid var(--border);'
                                f'border-radius:9px;padding:12px 15px">'
                                f'<div style="font-family:DM Mono,monospace;font-size:0.65rem;'
                                f'color:{c};font-weight:600">{v:+.2f}</div>'
                                f'<div style="font-family:Outfit,sans-serif;font-size:0.82rem;'
                                f'color:var(--text);margin-top:3px">{a} × {b}</div>'
                                f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;'
                                f'color:var(--t3);margin-top:2px">'
                                f'{"Diversification réduite" if v>0 else "Couverture naturelle"}'
                                f'</div></div>')
                html_hc += '</div>'
                st.markdown(html_hc, unsafe_allow_html=True)
            else:
                st.success("✓ Aucune corrélation extrême détectée entre vos positions.")

    # ══════════════════════════════════════════════════════════════════════════
    # ONGLET 2 — SIGNAUX TECHNIQUES
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        section_label("Détection automatique de patterns · Actions uniquement")

        if not action_tickers:
            st.info("Aucune action détectée dans le portefeuille (ETF exclus).")
        else:
            all_signals_data = {}
            with st.spinner("Analyse technique en cours…"):
                for tk in action_tickers:
                    all_signals_data[tk] = get_ticker_signals(tk)

        COLOR_MAP = {"g": "#22c55e", "r": "#ef4444", "y": "#f59e0b", "n": "#475569"}
        BG_MAP    = {"g": "rgba(34,197,94,0.07)", "r": "rgba(239,68,68,0.07)",
                     "y": "rgba(245,158,11,0.07)", "n": "var(--s1)"}

        rows_html = ""
        for tk in action_tickers:
            sig = all_signals_data.get(tk)
            if not sig:
                continue

            pct_52 = sig["pct_from_high"]
            rsi_c  = "#ef4444" if sig["rsi"] > 70 else ("#22c55e" if sig["rsi"] < 30 else "#f59e0b")

            # Signal badges
            badge_html = ""
            for label, cls, detail in sig["signals"][:3]:
                badge_html += (f'<span style="display:inline-block;font-family:DM Mono,monospace;'
                               f'font-size:0.58rem;font-weight:600;color:{COLOR_MAP[cls]};'
                               f'background:{BG_MAP[cls]};border:1px solid {COLOR_MAP[cls]}33;'
                               f'border-radius:4px;padding:2px 7px;margin:2px 2px 2px 0;'
                               f'white-space:nowrap">{label}</span>')

            # RSI bar
            rsi_pct = max(0, min(100, sig["rsi"]))
            rsi_bar = (f'<div style="background:var(--s3);border-radius:3px;height:4px;'
                       f'margin-top:5px;overflow:hidden">'
                       f'<div style="width:{rsi_pct:.0f}%;height:100%;'
                       f'background:{rsi_c};border-radius:3px"></div></div>')

            # 52w bar
            if sig["w52_h"] != sig["w52_l"]:
                pos52 = (sig["last"] - sig["w52_l"]) / (sig["w52_h"] - sig["w52_l"]) * 100
            else:
                pos52 = 50
            bar52 = (f'<div style="background:var(--s3);border-radius:3px;height:4px;'
                     f'margin-top:5px;overflow:hidden">'
                     f'<div style="width:{pos52:.0f}%;height:100%;'
                     f'background:#3b82f6;border-radius:3px"></div></div>')

            rows_html += (
                f'<div style="background:var(--s1);border:1px solid var(--border);'
                f'border-radius:11px;padding:16px 18px;margin-bottom:10px">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'margin-bottom:10px">'
                f'<span style="font-family:DM Mono,monospace;font-size:0.78rem;'
                f'color:#22c55e;font-weight:600">{tk}</span>'
                f'<span style="font-family:Outfit,sans-serif;font-size:0.95rem;'
                f'font-weight:700;color:var(--text)">{sig["last"]:.2f}</span>'
                f'</div>'
                f'<div style="margin-bottom:8px">{badge_html}</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;'
                f'margin-top:10px">'
                f'<div><div style="font-family:DM Mono,monospace;font-size:0.55rem;'
                f'color:var(--t3);text-transform:uppercase;letter-spacing:0.1em">RSI 14</div>'
                f'<div style="font-family:Outfit,sans-serif;font-size:0.9rem;font-weight:600;'
                f'color:{rsi_c}">{sig["rsi"]:.0f}</div>{rsi_bar}</div>'
                f'<div><div style="font-family:DM Mono,monospace;font-size:0.55rem;'
                f'color:var(--t3);text-transform:uppercase;letter-spacing:0.1em">52s pos.</div>'
                f'<div style="font-family:Outfit,sans-serif;font-size:0.9rem;font-weight:600;'
                f'color:{("#22c55e" if pct_52 > -10 else "#f59e0b")}">'
                f'{pct_52:+.1f}%</div>{bar52}</div>'
                f'<div><div style="font-family:DM Mono,monospace;font-size:0.55rem;'
                f'color:var(--t3);text-transform:uppercase;letter-spacing:0.1em">Vol ×moy</div>'
                f'<div style="font-family:Outfit,sans-serif;font-size:0.9rem;font-weight:600;'
                f'color:{("#22c55e" if sig["vol_r"] > 1.5 else "var(--t2)")}">'
                f'×{sig["vol_r"]:.1f}</div></div>'
                f'</div></div>'
            )

        if rows_html:
            st.markdown(rows_html, unsafe_allow_html=True)

            # Résumé global des signaux
            section_label("Vue consolidée — tous signaux")
            all_sig_flat = []
            for tk, sig in all_signals_data.items():
                if sig:
                    for lbl, cls, det in sig["signals"]:
                        all_sig_flat.append((tk, lbl, cls, det))

            greens = [(t,l,d) for t,l,c,d in all_sig_flat if c=="g"]
            reds   = [(t,l,d) for t,l,c,d in all_sig_flat if c=="r"]

            c_g, c_r = st.columns(2)
            def sig_list(items, color, title):
                html = (f'<div style="background:var(--s1);border:1px solid var(--border);'
                        f'border-radius:11px;padding:16px 18px">'
                        f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;'
                        f'color:{color};text-transform:uppercase;letter-spacing:0.1em;'
                        f'margin-bottom:10px">{title}</div>')
                if not items:
                    html += '<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:var(--t3)">Aucun</div>'
                for tk, lbl, det in items:
                    html += (f'<div style="display:flex;justify-content:space-between;'
                             f'padding:6px 0;border-bottom:1px solid var(--border)">'
                             f'<span style="font-family:DM Mono,monospace;font-size:0.65rem;'
                             f'color:{color};font-weight:600">{tk}</span>'
                             f'<span style="font-family:DM Mono,monospace;font-size:0.62rem;'
                             f'color:var(--t2)">{lbl}</span>'
                             f'<span style="font-family:DM Mono,monospace;font-size:0.58rem;'
                             f'color:var(--t3)">{det}</span></div>')
                html += '</div>'
                return html
            with c_g:
                st.markdown(sig_list(greens, "#22c55e", f"✓ Signaux haussiers · {len(greens)}"), unsafe_allow_html=True)
            with c_r:
                st.markdown(sig_list(reds, "#ef4444", f"✗ Signaux baissiers · {len(reds)}"), unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ONGLET 3 — ALERTES
    # ══════════════════════════════════════════════════════════════════════════
    with tab3:
        section_label("Alertes personnalisées")

        st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.68rem;'
                    'color:var(--t3);margin-bottom:1rem">Définissez des seuils de prix ou RSI '
                    '— statut calculé à chaque rafraîchissement.</div>', unsafe_allow_html=True)

        # Init alertes depuis état persistant
        if "alerts" not in st.session_state:
            st.session_state.alerts = get_state("alerts", [])

        # Formulaire ajout
        with st.expander("➕  Ajouter une alerte", expanded=len(st.session_state.alerts) == 0):
            ca, cb, cc, cd = st.columns([2, 2, 2, 1])
            with ca:
                al_ticker = st.selectbox("Ticker", port_tickers + ["Autre…"], key="al_tk")
                if al_ticker == "Autre…":
                    al_ticker = st.text_input("Ticker personnalisé", key="al_tk_custom").upper()
            with cb:
                al_type = st.selectbox("Condition", [
                    "Prix ≤", "Prix ≥", "RSI ≤", "RSI ≥",
                    "% depuis 52s haut ≤", "Volume ×moy ≥",
                ], key="al_type")
            with cc:
                al_val = st.number_input("Seuil", value=0.0, key="al_val", format="%.2f")
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Ajouter", use_container_width=True, key="al_add"):
                    if al_ticker:
                        st.session_state.alerts.append({
                            "ticker": al_ticker, "type": al_type,
                            "val": al_val, "created": datetime.now().strftime("%d/%m %H:%M")
                        })
                        set_state("alerts", st.session_state.alerts)
                        st.rerun()

        if not st.session_state.alerts:
            st.markdown("""<div class="empty-state" style="padding:30px">
              <div class="empty-icon" style="font-size:1.4rem">🔔</div>
              <div class="empty-title">Aucune alerte configurée</div>
              <div class="empty-sub">Ajoutez une alerte ci-dessus.</div>
            </div>""", unsafe_allow_html=True)
        else:
            # Évaluation des alertes
            alert_sigs = {}
            tks_needed = list({a["ticker"] for a in st.session_state.alerts})
            with st.spinner("Vérification des alertes…"):
                for tk in tks_needed:
                    alert_sigs[tk] = get_ticker_signals(tk)

            rows_a = ""
            to_delete = []
            for i, al in enumerate(st.session_state.alerts):
                sig  = alert_sigs.get(al["ticker"])
                atype = al["type"]; aval = al["val"]
                triggered = False; cur_val_str = "—"

                if sig:
                    if atype == "Prix ≤":
                        triggered = sig["last"] <= aval; cur_val_str = f"{sig['last']:.2f}"
                    elif atype == "Prix ≥":
                        triggered = sig["last"] >= aval; cur_val_str = f"{sig['last']:.2f}"
                    elif atype == "RSI ≤":
                        triggered = sig["rsi"] <= aval; cur_val_str = f"{sig['rsi']:.0f}"
                    elif atype == "RSI ≥":
                        triggered = sig["rsi"] >= aval; cur_val_str = f"{sig['rsi']:.0f}"
                    elif atype == "% depuis 52s haut ≤":
                        triggered = sig["pct_from_high"] <= aval; cur_val_str = f"{sig['pct_from_high']:+.1f}%"
                    elif atype == "Volume ×moy ≥":
                        triggered = sig["vol_r"] >= aval; cur_val_str = f"×{sig['vol_r']:.1f}"

                status_c = "#ef4444" if triggered else "#475569"
                status_l = "🔴 DÉCLENCHÉ" if triggered else "○ En attente"
                bg = "rgba(239,68,68,0.06)" if triggered else "var(--s1)"
                border = "rgba(239,68,68,0.3)" if triggered else "var(--border)"

                rows_a += (
                    f'<div style="background:{bg};border:1px solid {border};'
                    f'border-radius:10px;padding:13px 17px;margin-bottom:8px;'
                    f'display:flex;align-items:center;gap:16px">'
                    f'<span style="font-family:DM Mono,monospace;font-size:0.72rem;'
                    f'color:#22c55e;font-weight:600;min-width:70px">{al["ticker"]}</span>'
                    f'<span style="font-family:DM Mono,monospace;font-size:0.68rem;'
                    f'color:var(--t2);flex:1">{atype} <b style="color:var(--text)">{aval}</b></span>'
                    f'<span style="font-family:DM Mono,monospace;font-size:0.65rem;'
                    f'color:var(--t3)">Actuel : <b style="color:var(--t2)">{cur_val_str}</b></span>'
                    f'<span style="font-family:DM Mono,monospace;font-size:0.62rem;'
                    f'color:{status_c};font-weight:600">{status_l}</span>'
                    f'<span style="font-family:DM Mono,monospace;font-size:0.55rem;'
                    f'color:var(--t4)">{al["created"]}</span>'
                    f'</div>'
                )

            st.markdown(rows_a, unsafe_allow_html=True)

            if st.button("🗑  Effacer toutes les alertes", key="al_clear"):
                st.session_state.alerts = []
                set_state("alerts", [])
                st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # ONGLET 4 — STRESS-TEST
    # ══════════════════════════════════════════════════════════════════════════
    with tab4:
        section_label("Stress-test de portefeuille")

        st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.67rem;color:var(--t3);'
                    'margin-bottom:1.2rem">Simulation du P&L si le marché subit un choc.<br>'
                    'Basé sur le bêta réel de chaque position (yfinance).</div>',
                    unsafe_allow_html=True)

        # Fetch betas
        @st.cache_data(ttl=600)
        def get_betas(tickers_tuple):
            betas = {}
            for tk in tickers_tuple:
                try:
                    info = yf.Ticker(tk).info
                    b = info.get("beta")
                    betas[tk] = float(b) if b else 1.0
                except:
                    betas[tk] = 1.0
            return betas

        with st.spinner("Récupération des bêtas…"):
            betas = get_betas(tuple(port_tickers))

        # Scénarios prédéfinis
        SCENARIOS = {
            "Correction normale (-10%)":    -10,
            "Correction sévère (-20%)":     -20,
            "Bear market (-35%)":           -35,
            "Crash 2008 (-50%)":            -50,
            "Flash crash (-15%)":           -15,
            "Rally (+15%)":                 +15,
            "Bull run (+30%)":              +30,
        }

        st.markdown('<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:1.2rem">', unsafe_allow_html=True)
        sc_sel, sc_custom = st.columns([2, 1])
        with sc_sel:
            scenario_name = st.selectbox("Scénario prédéfini", list(SCENARIOS.keys()), key="stress_sc")
            shock_pct = SCENARIOS[scenario_name]
        with sc_custom:
            custom_shock = st.slider("Choc personnalisé (%)", -60, +60, shock_pct, 1, key="stress_custom")
            shock_pct = custom_shock

        # Calcul impact
        val_totale = s["total_valeur"]
        rows_stress = []
        total_impact = 0.0
        for _, r in df_pos.iterrows():
            tk = r["Ticker"]
            if tk == "N/A":
                continue
            beta  = betas.get(tk, 1.0)
            impact_pct = shock_pct * beta
            impact_eur = r["Valeur (€)"] * impact_pct / 100
            new_val    = r["Valeur (€)"] + impact_eur
            total_impact += impact_eur
            rows_stress.append({
                "Titre": r["Titre"], "Ticker": tk,
                "Valeur": r["Valeur (€)"], "Bêta": beta,
                "Choc effectif": impact_pct, "Impact (€)": impact_eur,
                "Valeur post-choc": new_val,
            })
        rows_stress.sort(key=lambda x: x["Impact (€)"])

        # KPIs stress
        new_total    = val_totale + total_impact
        impact_pct_t = total_impact / val_totale * 100 if val_totale > 0 else 0
        shock_c = "#22c55e" if shock_pct > 0 else "#ef4444"
        kpi_s = (
            f'<div class="kpi-row" style="grid-template-columns:repeat(4,1fr)">'
            + kpi_card("Choc marché", f"{shock_pct:+.0f}%",
                       top_color=f"linear-gradient(90deg,{shock_c},transparent)")
            + kpi_card("Impact portefeuille",
                       f"{total_impact:+,.0f} €",
                       f"{impact_pct_t:+.1f}% de la valeur",
                       total_impact >= 0,
                       top_color=f"linear-gradient(90deg,{shock_c},transparent)")
            + kpi_card("Valeur avant", f"{val_totale:,.0f} €",
                       top_color="linear-gradient(90deg,#3b82f6,transparent)")
            + kpi_card("Valeur après", f"{new_total:,.0f} €",
                       top_color=f"linear-gradient(90deg,{shock_c},transparent)")
            + '</div>'
        )
        st.markdown(kpi_s, unsafe_allow_html=True)

        # Tableau
        rows_html_s = ""
        for r in rows_stress:
            ic  = "#ef4444" if r["Impact (€)"] < 0 else "#22c55e"
            sg  = "+" if r["Impact (€)"] >= 0 else ""
            beta_c = "#ef4444" if r["Bêta"] > 1.5 else ("#f59e0b" if r["Bêta"] > 1.0 else "#22c55e")
            rows_html_s += (
                f'<tr>'
                f'<td style="text-align:left">{r["Titre"]}'
                f'<span class="tbadge">{r["Ticker"]}</span></td>'
                f'<td><span style="font-family:DM Mono,monospace;font-size:0.75rem;color:{beta_c}">'
                f'{r["Bêta"]:.2f}</span></td>'
                f'<td>{r["Valeur"]:,.0f} €</td>'
                f'<td><span style="color:{ic};font-weight:600;font-family:DM Mono,monospace;font-size:0.75rem">'
                f'{r["Choc effectif"]:+.1f}%</span></td>'
                f'<td class="{"pos" if r["Impact (€)"]>=0 else "neg"}">'
                f'{sg}{r["Impact (€)"]:,.0f} €</td>'
                f'<td>{r["Valeur post-choc"]:,.0f} €</td>'
                f'</tr>'
            )

        st.markdown(
            f'<div style="background:var(--s1);border:1px solid var(--border);'
            f'border-radius:11px;overflow:hidden;margin-bottom:1.5rem">'
            f'<table class="ptable"><thead><tr>'
            f'<th style="text-align:left">Titre</th>'
            f'<th>Bêta</th><th>Valeur actuelle</th>'
            f'<th>Choc effectif</th><th>Impact €</th><th>Valeur après choc</th>'
            f'</tr></thead><tbody>{rows_html_s}</tbody></table></div>',
            unsafe_allow_html=True
        )

        # Graphique waterfall
        section_label("Cascade d'impact par position")
        sorted_r = sorted(rows_stress, key=lambda x: x["Impact (€)"])
        fig_wf = go.Figure(go.Bar(
            x=[r["Ticker"] for r in sorted_r],
            y=[r["Impact (€)"] for r in sorted_r],
            marker_color=["#22c55e" if r["Impact (€)"] >= 0 else "#ef4444" for r in sorted_r],
            marker_opacity=0.85,
            text=[f"{r['Impact (€)']:+,.0f}€" for r in sorted_r],
            textposition="outside",
            textfont=dict(family="DM Mono", size=9),
            hovertemplate="<b>%{x}</b><br>Impact : %{y:+,.0f} €<extra></extra>",
        ))
        fig_wf.update_layout(**plotly_base(260, {"ticksuffix": " €", "tickformat": ",.0f"}))
        fig_wf.add_hline(y=0, line_color="#2d3f57", line_width=1)
        st.plotly_chart(fig_wf, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ONGLET 5 — CONCENTRATION & RISQUE
    # ══════════════════════════════════════════════════════════════════════════
    with tab5:
        section_label("Analyse de concentration & risque")

        total_v = df_pos["Valeur (€)"].sum()
        df_pos2 = df_pos.copy()
        df_pos2["Poids (%)"] = df_pos2["Valeur (€)"] / total_v * 100
        df_pos2 = df_pos2.sort_values("Poids (%)", ascending=False).reset_index(drop=True)

        # HHI — Herfindahl-Hirschman Index
        hhi = sum((w/100)**2 for w in df_pos2["Poids (%)"])
        n_equiv = 1 / hhi if hhi > 0 else len(df_pos2)
        hhi_score = max(0, min(100, int((1 - hhi) * 100)))
        hhi_c = "#22c55e" if hhi_score >= 70 else ("#f59e0b" if hhi_score >= 45 else "#ef4444")
        hhi_label = "Bien diversifié" if hhi_score >= 70 else ("Concentré" if hhi_score < 45 else "Modéré")

        # Largest position risk
        top_pos = df_pos2.iloc[0]
        top_risk = top_pos["Poids (%)"] > 20

        # Nb actifs > 10%
        heavy = df_pos2[df_pos2["Poids (%)"] > 10]

        kpi_c = (
            f'<div class="kpi-row" style="grid-template-columns:repeat(4,1fr)">'
            + kpi_card("Score diversification",
                       str(hhi_score),
                       hhi_label, hhi_score >= 60,
                       top_color=f"linear-gradient(90deg,{hhi_c},transparent)")
            + kpi_card("Positions équivalentes",
                       f"{n_equiv:.1f}",
                       "positions de poids égal",
                       top_color="linear-gradient(90deg,#3b82f6,transparent)")
            + kpi_card("Plus grosse position",
                       f"{top_pos['Poids (%)']:.1f}%",
                       top_pos["Titre"][:20],
                       not top_risk,
                       top_color=f"linear-gradient(90deg,{'#ef4444' if top_risk else '#22c55e'},transparent)")
            + kpi_card("Positions > 10%",
                       str(len(heavy)),
                       "risque de concentration" if len(heavy) > 3 else "acceptable",
                       len(heavy) <= 3,
                       top_color=f"linear-gradient(90deg,{'#f59e0b' if len(heavy)>2 else '#22c55e'},transparent)")
            + '</div>'
        )
        st.markdown(kpi_c, unsafe_allow_html=True)

        # Graphique treemap de concentration
        section_label("Carte de poids — Treemap")
        fig_tm = go.Figure(go.Treemap(
            labels=df_pos2["Titre"].apply(lambda x: x[:18]).tolist(),
            parents=[""] * len(df_pos2),
            values=df_pos2["Valeur (€)"].tolist(),
            customdata=df_pos2[["Poids (%)", "+/- Value (%)"]].values,
            texttemplate="<b>%{label}</b><br>%{customdata[0]:.1f}%",
            hovertemplate="<b>%{label}</b><br>Valeur : %{value:,.0f} €<br>"
                          "Poids : %{customdata[0]:.1f}%<br>"
                          "P&L : %{customdata[1]:+.1f}%<extra></extra>",
            marker=dict(
                colors=df_pos2["+/- Value (%)"].tolist(),
                colorscale=[[0, "#ef4444"], [0.5, "#1a2235"], [1, "#22c55e"]],
                cmid=0,
                showscale=True,
                colorbar=dict(
                    title=dict(text="P&L %", font=dict(family="DM Mono", size=9)),
                    thickness=10, len=0.7,
                    tickfont=dict(family="DM Mono", size=8),
                ),
            ),
            textfont=dict(family="Outfit", size=11),
        ))
        fig_tm.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            height=340,
        )
        st.plotly_chart(fig_tm, use_container_width=True)

        # Tableau de concentration
        section_label("Détail par position")
        rows_c = ""
        for _, r in df_pos2.iterrows():
            w = r["Poids (%)"]
            bar_w = min(100, w * 4)
            risk_flag = " ⚠" if w > 20 else (" ·" if w > 10 else "")
            pnl_c = "#22c55e" if r["+/- Value (%)"] >= 0 else "#ef4444"
            rows_c += (
                f'<tr>'
                f'<td style="text-align:left">{r["Titre"]}'
                f'<span class="tbadge">{r["Ticker"]}</span>'
                f'<span style="color:#f59e0b;font-size:0.7rem">{risk_flag}</span></td>'
                f'<td>{r["Valeur (€)"]:,.0f} €</td>'
                f'<td><div style="display:flex;align-items:center;gap:8px;justify-content:flex-end">'
                f'<span style="font-family:DM Mono,monospace;font-size:0.75rem;'
                f'color:{"#ef4444" if w>20 else ("var(--amber)" if w>10 else "var(--text)")}">'
                f'{w:.1f}%</span>'
                f'<div style="width:60px;height:5px;background:var(--s3);border-radius:3px;overflow:hidden">'
                f'<div style="width:{bar_w:.0f}%;height:100%;background:'
                f'{"#ef4444" if w>20 else ("#f59e0b" if w>10 else "#22c55e")};border-radius:3px"></div>'
                f'</div></div></td>'
                f'<td class="{"pos" if r["+/- Value (%)"]>=0 else "neg"}">'
                f'{r["+/- Value (%)"]:+.2f}%</td>'
                f'<td>{r.get("Secteur","—")}</td>'
                f'</tr>'
            )
        st.markdown(
            f'<div style="background:var(--s1);border:1px solid var(--border);'
            f'border-radius:11px;overflow:hidden">'
            f'<table class="ptable"><thead><tr>'
            f'<th style="text-align:left">Titre</th>'
            f'<th>Valeur</th><th>Poids</th><th>P&L %</th><th style="text-align:left">Secteur</th>'
            f'</tr></thead><tbody>{rows_c}</tbody></table></div>',
            unsafe_allow_html=True
        )

        # Alertes concentration
        alerts_c = []
        if top_pos["Poids (%)"] > 25:
            alerts_c.append(f"⚠ {top_pos['Titre']} représente {top_pos['Poids (%)']:.1f}% du portefeuille — sur-exposition.")
        if len(heavy) > 4:
            alerts_c.append(f"⚠ {len(heavy)} positions dépassent 10% du portefeuille — risque de concentration élevé.")
        if n_equiv < 4:
            alerts_c.append(f"⚠ Diversification faible : équivalent {n_equiv:.1f} positions de même poids.")
        if not alerts_c:
            st.success("✓ Concentration du portefeuille dans les normes.")
        else:
            for a in alerts_c:
                st.warning(a)



# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — BACKTESTING
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600)
def backtest_strategy(tickers: tuple, start_date: str, score_threshold: int):
    """
    Stratégie naïve : achète équipondéré tous les tickers qui passent le seuil
    de score 10-Baggers. Calcule la perf depuis start_date.
    Retourne DataFrame avec valeur normalisée (base 100).
    """
    results = {}
    for tk in tickers:
        try:
            h = yf.Ticker(tk).history(start=start_date)["Close"]
            h.index = h.index.tz_localize(None)
            if len(h) > 5:
                results[tk] = h / h.iloc[0] * 100
        except:
            pass
    if not results:
        return pd.DataFrame(), pd.DataFrame()

    df = pd.DataFrame(results).dropna(how="all").ffill()
    df["Stratégie"] = df.mean(axis=1)

    # Benchmarks
    benchmarks = {}
    for name, sym in [("CAC 40", "^FCHI"), ("MSCI World", "IWDA.AS")]:
        try:
            h = yf.Ticker(sym).history(start=start_date)["Close"]
            h.index = h.index.tz_localize(None)
            if len(h) > 5:
                benchmarks[name] = h / h.iloc[0] * 100
        except:
            pass
    df_bench = pd.DataFrame(benchmarks).dropna(how="all").ffill()

    return df, df_bench


def page_backtesting():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">⏱ Simulation historique</div>'
                '<div class="ph-title">Backtesting</div>'
                '<div class="ph-sub">Stratégie 10-Baggers · Performance historique simulée</div>'
                '</div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.25);'
        'border-radius:10px;padding:12px 16px;margin-bottom:1.4rem;font-family:DM Mono,monospace;'
        'font-size:0.65rem;color:#f59e0b">⚠ Backtesting naïf — les performances passées ne préjugent '
        'pas des performances futures. Équipondération, sans frais ni fiscalité.</div>',
        unsafe_allow_html=True)

    # ── Configuration ─────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        bt_period = st.selectbox("Période de simulation",
            ["1 an", "2 ans", "3 ans", "5 ans"], index=1, key="bt_period")
        period_days = {"1 an": 365, "2 ans": 730, "3 ans": 1095, "5 ans": 1825}
        start_dt = (datetime.today() - timedelta(days=period_days[bt_period])).strftime("%Y-%m-%d")
    with c2:
        score_thresh = st.slider("Score 10-Baggers minimum", 0, 100, 60, 5, key="bt_thresh")
    with c3:
        default_universe = ", ".join(PEA_FR_TICKERS)
        universe_input = st.text_area("Universe (tickers séparés par virgules)",
            value=default_universe,
            height=80, key="bt_universe", label_visibility="visible")

    run_bt = st.button("▶  Lancer le backtest", type="primary", use_container_width=False, key="bt_run")

    if "bt_results" not in st.session_state:
        st.session_state.bt_results = None

    if run_bt:
        raw_tickers = [t.strip().upper() for t in universe_input.replace(",", " ").split() if t.strip()]

        # Score chaque ticker
        progress = st.progress(0, "Calcul des scores 10-Baggers…")
        scored = []
        for i, tk in enumerate(raw_tickers):
            progress.progress(int(i / len(raw_tickers) * 60), f"Score {tk}…")
            data = compute_10bagger_data(tk)
            if data and data["Score"] >= score_thresh:
                scored.append((tk, data["Score"], data["Nom"]))
        progress.progress(60, "Récupération des historiques…")

        if not scored:
            st.warning(f"Aucun ticker avec score ≥ {score_thresh}. Baisse le seuil ou élargis l'univers.")
            st.session_state.bt_results = None
        else:
            tickers_sel = tuple(tk for tk, _, _ in scored)
            df_strat, df_bench = backtest_strategy(tickers_sel, start_dt, score_thresh)
            progress.progress(100, "Terminé ✓")
            st.session_state.bt_results = {
                "df_strat": df_strat, "df_bench": df_bench,
                "scored": scored, "start_dt": start_dt, "thresh": score_thresh,
            }

    res = st.session_state.bt_results
    if res is None:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">⏱</div>
          <div class="empty-title">Configurez et lancez le backtest</div>
          <div class="empty-sub">Sélectionnez un univers, un seuil de score et une période.</div>
        </div>""", unsafe_allow_html=True)
        return

    df_s   = res["df_strat"]
    df_b   = res["df_bench"]
    scored = res["scored"]

    if df_s.empty:
        st.error("Données insuffisantes pour la période sélectionnée.")
        return

    # ── KPIs ─────────────────────────────────────────────────────────────────
    section_label("Résultats de la stratégie")

    strat_perf = float(df_s["Stratégie"].iloc[-1] - 100) if "Stratégie" in df_s.columns else 0
    cac_perf   = float(df_b["CAC 40"].iloc[-1] - 100) if "CAC 40" in df_b.columns else None
    msci_perf  = float(df_b["MSCI World"].iloc[-1] - 100) if "MSCI World" in df_b.columns else None
    alpha_cac  = strat_perf - cac_perf if cac_perf is not None else None
    n_sel      = len(scored)

    sc = "#22c55e" if strat_perf >= 0 else "#ef4444"
    kpi_bt = (
        f'<div class="kpi-row" style="grid-template-columns:repeat(5,1fr)">'
        + kpi_card("Actions sélectionnées", str(n_sel),
                   f"score ≥ {res['thresh']}",
                   top_color="linear-gradient(90deg,#3b82f6,transparent)")
        + kpi_card("Perf Stratégie", f"{strat_perf:+.1f}%",
                   res["bt_period"] if "bt_period" in res else "",
                   strat_perf >= 0,
                   top_color=f"linear-gradient(90deg,{sc},transparent)")
        + kpi_card("Perf CAC 40",
                   f"{cac_perf:+.1f}%" if cac_perf is not None else "—",
                   top_color="linear-gradient(90deg,#475569,transparent)")
        + kpi_card("Perf MSCI World",
                   f"{msci_perf:+.1f}%" if msci_perf is not None else "—",
                   top_color="linear-gradient(90deg,#475569,transparent)")
        + kpi_card("Alpha vs CAC",
                   f"{alpha_cac:+.1f}%" if alpha_cac is not None else "—",
                   alpha_cac >= 0 if alpha_cac is not None else None,
                   top_color=f"linear-gradient(90deg,{'#22c55e' if (alpha_cac or 0)>=0 else '#ef4444'},transparent)")
        + '</div>'
    )
    st.markdown(kpi_bt, unsafe_allow_html=True)

    # ── Graphique principal ───────────────────────────────────────────────────
    section_label("Évolution de la valeur · Base 100")
    fig_bt = go.Figure()

    # Lignes individuelles (transparentes)
    for col in df_s.columns:
        if col == "Stratégie":
            continue
        fig_bt.add_trace(go.Scatter(
            x=df_s.index, y=df_s[col], name=col,
            line=dict(width=1, color="#1a2538"),
            hovertemplate=f"<b>{col}</b> %{{x|%d %b %Y}}<br>%{{y:.1f}}<extra></extra>",
            opacity=0.5,
        ))

    # Benchmarks
    for bname, bcol in [("CAC 40", "#3b82f6"), ("MSCI World", "#8b5cf6")]:
        if bname in df_b.columns:
            fig_bt.add_trace(go.Scatter(
                x=df_b.index, y=df_b[bname], name=bname,
                line=dict(width=2, color=bcol, dash="dash"),
                hovertemplate=f"<b>{bname}</b> %{{x|%d %b %Y}}<br>%{{y:.1f}}<extra></extra>",
            ))

    # Stratégie en gras
    if "Stratégie" in df_s.columns:
        sc2 = "#22c55e" if strat_perf >= 0 else "#ef4444"
        fig_bt.add_trace(go.Scatter(
            x=df_s.index, y=df_s["Stratégie"], name="Stratégie (équipond.)",
            line=dict(width=3, color=sc2),
            hovertemplate="<b>Stratégie</b> %{x|%d %b %Y}<br>%{y:.1f}<extra></extra>",
        ))

    fig_bt.add_hline(y=100, line_color="#2d3f57", line_width=1, line_dash="dot")
    fig_bt.update_layout(**plotly_base(380, {"ticksuffix": "", "tickformat": ".0f"}))
    st.plotly_chart(fig_bt, use_container_width=True)

    # ── Tableau des actions sélectionnées ─────────────────────────────────────
    section_label(f"Actions sélectionnées · score ≥ {res['thresh']}")
    rows_bt = ""
    for tk, sc_v, nom in sorted(scored, key=lambda x: -x[1]):
        perf = float(df_s[tk].iloc[-1] - 100) if tk in df_s.columns else None
        pc   = "#22c55e" if (perf or 0) >= 0 else "#ef4444"
        sc_c = "#22c55e" if sc_v >= 70 else ("#f59e0b" if sc_v >= 50 else "#ef4444")
        rows_bt += (
            f'<tr>'
            f'<td style="text-align:left"><span style="font-family:DM Mono,monospace;'
            f'font-size:0.75rem;color:#22c55e;font-weight:600">{tk}</span></td>'
            f'<td style="text-align:left;font-size:0.82rem">{nom}</td>'
            f'<td><span style="font-family:DM Mono,monospace;font-size:0.75rem;'
            f'font-weight:700;color:{sc_c}">{sc_v}</span></td>'
            f'<td class="{"pos" if (perf or 0)>=0 else "neg"}">'
            f'{f"{perf:+.1f}%" if perf is not None else "—"}</td>'
            f'</tr>'
        )
    st.markdown(
        f'<div style="background:var(--s1);border:1px solid var(--border);'
        f'border-radius:11px;overflow:hidden">'
        f'<table class="ptable"><thead><tr>'
        f'<th style="text-align:left">Ticker</th>'
        f'<th style="text-align:left">Nom</th>'
        f'<th>Score</th><th>Perf période</th>'
        f'</tr></thead><tbody>{rows_bt}</tbody></table></div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — ACTUALITÉS
# ══════════════════════════════════════════════════════════════════════════════

SENTIMENT_POS = ["hausse","croissance","bénéfice","profit","record","acquiert","dividende",
                 "surperforme","croît","optimiste","beat","strong","growth","rises","gain",
                 "up","positive","buy","upgrade","raise","outperform","beat","exceed"]
SENTIMENT_NEG = ["baisse","perte","risque","avertissement","chute","recul","déçoit","faible",
                 "coupe","inquiétude","warn","loss","cut","down","negative","sell","downgrade",
                 "miss","below","decline","drop","weak","concern","risk","lawsuit","investigation"]

def score_sentiment(text: str) -> str:
    t = text.lower()
    pos = sum(1 for w in SENTIMENT_POS if w in t)
    neg = sum(1 for w in SENTIMENT_NEG if w in t)
    if pos > neg:   return "g"
    if neg > pos:   return "r"
    return "n"

@st.cache_data(ttl=900)
def get_ticker_news(ticker: str, max_items: int = 8):
    """Fetch news from yfinance for a ticker."""
    try:
        raw = yf.Ticker(ticker).news
        if not raw:
            return []
        items = []
        for n in raw[:max_items]:
            title     = n.get("title", "")
            publisher = n.get("publisher", "")
            link      = n.get("link", "#")
            ts        = n.get("providerPublishTime", 0)
            try:
                dt = datetime.fromtimestamp(ts).strftime("%d/%m %H:%M")
            except:
                dt = "—"
            sentiment = score_sentiment(title)
            items.append({"title": title, "publisher": publisher,
                          "link": link, "dt": dt, "sentiment": sentiment})
        return items
    except:
        return []


def page_news():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">📰 Flux d\'informations</div>'
                '<div class="ph-title">Actualités</div>'
                '<div class="ph-sub">Ce matin dans ton portefeuille · Sentiment scoring</div>'
                '</div>', unsafe_allow_html=True)

    try:
        df_hist, df_corr, df_vers = load_data()
        df_pos, _ = compute_portfolio(df_hist, df_corr, df_vers)
    except Exception as e:
        st.error(f"Fichiers introuvables : {e}"); return

    port_tickers_news = [r["Ticker"] for _, r in df_pos.iterrows()
                         if r["Ticker"] and r["Ticker"] != "N/A"]

    # Tickers supplémentaires
    extra = st.text_input("Ajouter des tickers (optionnel)",
                          placeholder="AAPL, MSFT, ASML.AS…", key="news_extra",
                          label_visibility="visible")
    extra_tks = [t.strip().upper() for t in extra.replace(",", " ").split() if t.strip()]
    all_news_tks = list(dict.fromkeys(port_tickers_news + extra_tks))

    SENT_COLOR = {"g": "#22c55e", "r": "#ef4444", "n": "#475569"}
    SENT_BG    = {"g": "rgba(34,197,94,0.06)", "r": "rgba(239,68,68,0.06)", "n": "var(--s1)"}
    SENT_LABEL = {"g": "↑ Positif", "r": "↓ Négatif", "n": "→ Neutre"}

    # Stats globales
    all_articles = []
    with st.spinner("Récupération des actualités…"):
        news_by_ticker = {}
        for tk in all_news_tks:
            items = get_ticker_news(tk)
            news_by_ticker[tk] = items
            all_articles.extend([(tk, it) for it in items])

    n_pos = sum(1 for _, it in all_articles if it["sentiment"] == "g")
    n_neg = sum(1 for _, it in all_articles if it["sentiment"] == "r")
    n_neu = sum(1 for _, it in all_articles if it["sentiment"] == "n")
    total = len(all_articles)
    sentiment_global = "g" if n_pos > n_neg * 1.5 else ("r" if n_neg > n_pos * 1.5 else "n")
    sent_labels = {"g": "AMBIANCE POSITIVE", "r": "AMBIANCE NÉGATIVE", "n": "AMBIANCE NEUTRE"}
    sc_glob = {"g": "#22c55e", "r": "#ef4444", "n": "#f59e0b"}

    kpi_n = (
        f'<div class="kpi-row" style="grid-template-columns:repeat(5,1fr)">'
        + kpi_card("Articles collectés", str(total),
                   top_color="linear-gradient(90deg,#3b82f6,transparent)")
        + kpi_card("Sentiment global", sent_labels[sentiment_global],
                   top_color=f"linear-gradient(90deg,{sc_glob[sentiment_global]},transparent)")
        + kpi_card("↑ Positifs", str(n_pos),
                   f"{n_pos/total*100:.0f}%" if total else "—",
                   True, top_color="linear-gradient(90deg,#22c55e,transparent)")
        + kpi_card("↓ Négatifs", str(n_neg),
                   f"{n_neg/total*100:.0f}%" if total else "—",
                   False, top_color="linear-gradient(90deg,#ef4444,transparent)")
        + kpi_card("→ Neutres", str(n_neu),
                   top_color="linear-gradient(90deg,#475569,transparent)")
        + '</div>'
    )
    st.markdown(kpi_n, unsafe_allow_html=True)

    # Filtre sentiment
    filt_sent = st.radio("Filtrer par sentiment",
                         ["Tous", "↑ Positifs", "↓ Négatifs", "→ Neutres"],
                         horizontal=True, key="news_filt")
    filt_map  = {"Tous": None, "↑ Positifs": "g", "↓ Négatifs": "r", "→ Neutres": "n"}
    filt_code = filt_map[filt_sent]

    # Affichage par ticker
    for tk in all_news_tks:
        items = news_by_ticker.get(tk, [])
        if filt_code:
            items = [it for it in items if it["sentiment"] == filt_code]
        if not items:
            continue

        ticker_pos = sum(1 for it in items if it["sentiment"] == "g")
        ticker_neg = sum(1 for it in items if it["sentiment"] == "r")
        tk_sent    = "g" if ticker_pos > ticker_neg else ("r" if ticker_neg > ticker_pos else "n")

        section_label(f"{tk}  ·  {SENT_LABEL[tk_sent]}  ·  {len(items)} articles")

        cards_html = ""
        for it in items:
            sc = it["sentiment"]
            cards_html += (
                f'<a href="{it["link"]}" target="_blank" style="text-decoration:none">'
                f'<div style="background:{SENT_BG[sc]};border:1px solid {SENT_COLOR[sc]}22;'
                f'border-left:3px solid {SENT_COLOR[sc]};border-radius:9px;'
                f'padding:12px 15px;margin-bottom:7px;transition:border-color .15s;cursor:pointer">'
                f'<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:10px">'
                f'<div style="font-family:Outfit,sans-serif;font-size:0.85rem;font-weight:500;'
                f'color:var(--text);line-height:1.4;flex:1">{it["title"]}</div>'
                f'<span style="font-family:DM Mono,monospace;font-size:0.6rem;font-weight:600;'
                f'color:{SENT_COLOR[sc]};white-space:nowrap;padding:2px 7px;'
                f'background:{SENT_BG[sc]};border:1px solid {SENT_COLOR[sc]}44;'
                f'border-radius:4px">{SENT_LABEL[sc]}</span>'
                f'</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:0.58rem;color:var(--t3);'
                f'margin-top:6px;display:flex;gap:12px">'
                f'<span>{it["publisher"]}</span><span>{it["dt"]}</span>'
                f'</div></div></a>'
            )
        st.markdown(cards_html, unsafe_allow_html=True)

    if not any(news_by_ticker.values()):
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">📰</div>
          <div class="empty-title">Aucune actualité disponible</div>
          <div class="empty-sub">yfinance n'a pas retourné d'articles pour ces tickers.</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — RAPPORT PDF
# ══════════════════════════════════════════════════════════════════════════════

def page_rapport():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">📄 Export</div>'
                '<div class="ph-title">Rapport PDF</div>'
                '<div class="ph-sub">Rapport mensuel · Positions · Signaux · Score 10-Baggers</div>'
                '</div>', unsafe_allow_html=True)

    try:
        df_hist, df_corr, df_vers = load_data()
        df_pos, s = compute_portfolio(df_hist, df_corr, df_vers)
    except Exception as e:
        st.error(f"Fichiers introuvables : {e}"); return

    st.markdown(
        '<div style="font-family:DM Mono,monospace;font-size:0.67rem;color:var(--t3);'
        'margin-bottom:1.4rem">Générez un rapport PDF complet de votre portefeuille PEA '
        'incluant la valorisation, les positions, les scores 10-Baggers et les signaux techniques.</div>',
        unsafe_allow_html=True)

    # Options
    c1, c2 = st.columns(2)
    with c1:
        include_signals  = st.toggle("Inclure les signaux techniques", value=True, key="pdf_sig")
        include_scores   = st.toggle("Inclure les scores 10-Baggers",  value=True, key="pdf_sc")
    with c2:
        include_perf     = st.toggle("Inclure la performance",         value=True, key="pdf_perf")
        report_title_inp = st.text_input("Titre du rapport",
                           value=f"Rapport PEA · {datetime.now().strftime('%B %Y')}",
                           key="pdf_title")

    gen_btn = st.button("📄  Générer le rapport PDF", type="primary", key="pdf_gen")

    if not gen_btn:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">📄</div>
          <div class="empty-title">Prêt à générer</div>
          <div class="empty-sub">Configurez les options et cliquez sur Générer.</div>
        </div>""", unsafe_allow_html=True)
        return

    with st.spinner("Génération du rapport…"):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm
            from reportlab.lib import colors
            from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                            Table, TableStyle, HRFlowable)
            from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
            import io

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                                    leftMargin=2*cm, rightMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)

            # ── Styles ────────────────────────────────────────────────────────
            W, H = A4
            C_BG     = colors.HexColor("#05070e")
            C_GREEN  = colors.HexColor("#22c55e")
            C_RED    = colors.HexColor("#ef4444")
            C_AMBER  = colors.HexColor("#f59e0b")
            C_BLUE   = colors.HexColor("#3b82f6")
            C_TEXT   = colors.HexColor("#f1f5f9")
            C_T2     = colors.HexColor("#94a3b8")
            C_T3     = colors.HexColor("#475569")
            C_BORDER = colors.HexColor("#1e2a3a")
            C_S1     = colors.HexColor("#0c0f1a")
            C_S2     = colors.HexColor("#111827")

            styles = getSampleStyleSheet()

            def sty(name, **kw):
                return ParagraphStyle(name, **kw)

            st_title  = sty("title",  fontName="Helvetica-Bold", fontSize=22,
                            textColor=C_TEXT, spaceAfter=4, leading=26)
            st_sub    = sty("sub",    fontName="Helvetica",      fontSize=9,
                            textColor=C_T3,   spaceAfter=12, leading=12)
            st_h2     = sty("h2",     fontName="Helvetica-Bold", fontSize=13,
                            textColor=C_TEXT, spaceAfter=6, spaceBefore=14, leading=16)
            st_h3     = sty("h3",     fontName="Helvetica-Bold", fontSize=10,
                            textColor=C_T2,   spaceAfter=4, spaceBefore=8,  leading=13)
            st_body   = sty("body",   fontName="Helvetica",      fontSize=8.5,
                            textColor=C_T2,   spaceAfter=4, leading=12)
            st_mono   = sty("mono",   fontName="Courier",        fontSize=8,
                            textColor=C_T3,   spaceAfter=2, leading=11)
            st_green  = sty("green",  fontName="Helvetica-Bold", fontSize=9,
                            textColor=C_GREEN, spaceAfter=2)
            st_red    = sty("red",    fontName="Helvetica-Bold", fontSize=9,
                            textColor=C_RED,   spaceAfter=2)

            def hr():
                return HRFlowable(width="100%", thickness=0.5,
                                  color=C_BORDER, spaceAfter=8, spaceBefore=4)

            def tbl_style(header_color=C_S2):
                return TableStyle([
                    ("BACKGROUND",  (0,0), (-1,0),  header_color),
                    ("TEXTCOLOR",   (0,0), (-1,0),  C_T3),
                    ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
                    ("FONTSIZE",    (0,0), (-1,0),  7),
                    ("TEXTCOLOR",   (0,1), (-1,-1), C_T2),
                    ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
                    ("FONTSIZE",    (0,1), (-1,-1), 7.5),
                    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_BG, C_S1]),
                    ("GRID",        (0,0), (-1,-1), 0.3, C_BORDER),
                    ("LEFTPADDING", (0,0), (-1,-1), 6),
                    ("RIGHTPADDING",(0,0), (-1,-1), 6),
                    ("TOPPADDING",  (0,0), (-1,-1), 5),
                    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
                    ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
                ])

            story = []

            # ── Cover ─────────────────────────────────────────────────────────
            story.append(Spacer(1, 0.5*cm))
            story.append(Paragraph(report_title_inp, st_title))
            story.append(Paragraph(
                f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} · yfinance · PEA Dashboard",
                st_sub))
            story.append(hr())

            # ── KPIs valorisation ──────────────────────────────────────────────
            story.append(Paragraph("Valorisation du portefeuille", st_h2))
            val_totale   = s["total_valeur"] + s["liquidites"]
            gain_vs_vers = val_totale - s["total_verse"]
            pct_vs_vers  = gain_vs_vers / s["total_verse"] * 100 if s["total_verse"] > 0 else 0

            kpi_data = [
                ["Indicateur", "Valeur"],
                ["Capital versé",       f"{s['total_verse']:,.0f} €"],
                ["Investi en titres",   f"{s['total_investi']:,.0f} €"],
                ["+/− Latente titres",  f"{s['total_pv']:+,.0f} €  ({s['total_pv_pct']:+.2f}%)"],
                ["Liquidités",          f"{s['liquidites']:,.0f} €"],
                ["Valeur totale",       f"{val_totale:,.0f} €  ({gain_vs_vers:+,.0f} €  {pct_vs_vers:+.1f}%)"],
            ]
            t = Table(kpi_data, colWidths=[8*cm, 8*cm])
            t.setStyle(tbl_style())
            story.append(t)
            story.append(Spacer(1, 0.4*cm))

            # ── Positions ─────────────────────────────────────────────────────
            story.append(hr())
            story.append(Paragraph("Positions ouvertes", st_h2))
            pos_data = [["Titre", "Ticker", "Qté", "PRU", "Cours", "Valeur", "+/− €", "+/− %"]]
            for _, r in df_pos.sort_values("Valeur (€)", ascending=False).iterrows():
                crs = f"{r['Cours']:.2f}" if r["Cours"] else "—"
                pos_data.append([
                    r["Titre"][:22], r["Ticker"],
                    f"{r['Quantité']:.0f}", f"{r['PRU (€)']:.2f}",
                    crs, f"{r['Valeur (€)']:,.0f}",
                    f"{r['+/- Value (€)']:+,.0f}", f"{r['+/- Value (%)']:+.1f}%",
                ])
            t2 = Table(pos_data, colWidths=[4.5*cm,1.8*cm,1.2*cm,1.8*cm,1.8*cm,2.2*cm,2.2*cm,1.5*cm])
            ts2 = tbl_style()
            for i, r in enumerate(pos_data[1:], 1):
                try:
                    pv = float(r[6].replace("+","").replace(" ","").replace(",",".").replace("€",""))
                    ts2.add("TEXTCOLOR", (6,i),(7,i), C_GREEN if pv>=0 else C_RED)
                    ts2.add("FONTNAME",  (6,i),(7,i), "Helvetica-Bold")
                except: pass
            t2.setStyle(ts2)
            story.append(t2)
            story.append(Spacer(1, 0.4*cm))

            # ── Scores 10-Baggers ──────────────────────────────────────────────
            if include_scores:
                story.append(hr())
                story.append(Paragraph("Scores 10-Baggers — Positions", st_h2))
                story.append(Paragraph(
                    "Score pondéré /100 calculé sur 10 critères fondamentaux.", st_body))

                sc_data = [["Ticker", "Score", "Verdict"]]
                act_tks = [r["Ticker"] for _, r in df_pos.iterrows()
                           if r["Ticker"] != "N/A" and r.get("Type","Action") == "Action"]
                for tk in act_tks[:12]:  # limite 12 pour le PDF
                    d = compute_10bagger_data(tk)
                    if d:
                        verdict = "EXCELLENT" if d["Score"] >= 70 else ("CORRECT" if d["Score"] >= 50 else "INSUFFISANT")
                        sc_data.append([tk, str(d["Score"]), verdict])

                t3 = Table(sc_data, colWidths=[4*cm, 3*cm, 10*cm])
                ts3 = tbl_style()
                for i, r in enumerate(sc_data[1:], 1):
                    try:
                        sc_v = int(r[1])
                        c = C_GREEN if sc_v >= 70 else (C_AMBER if sc_v >= 50 else C_RED)
                        ts3.add("TEXTCOLOR", (1,i),(2,i), c)
                        ts3.add("FONTNAME",  (1,i),(2,i), "Helvetica-Bold")
                    except: pass
                t3.setStyle(ts3)
                story.append(t3)
                story.append(Spacer(1, 0.4*cm))

            # ── Signaux techniques ─────────────────────────────────────────────
            if include_signals:
                story.append(hr())
                story.append(Paragraph("Signaux techniques", st_h2))
                act_tks2 = [r["Ticker"] for _, r in df_pos.iterrows()
                            if r["Ticker"] != "N/A" and r.get("Type","Action") == "Action"]
                sig_data = [["Ticker", "Signal principal", "RSI", "vs 52s haut"]]
                for tk in act_tks2[:10]:
                    sig = get_ticker_signals(tk)
                    if sig:
                        top_sig = sig["signals"][0][0] if sig["signals"] else "—"
                        sig_data.append([tk, top_sig, f"{sig['rsi']:.0f}", f"{sig['pct_from_high']:+.1f}%"])
                t4 = Table(sig_data, colWidths=[3*cm, 8*cm, 2.5*cm, 3.5*cm])
                t4.setStyle(tbl_style())
                story.append(t4)
                story.append(Spacer(1, 0.4*cm))

            # ── Footer ────────────────────────────────────────────────────────
            story.append(hr())
            story.append(Paragraph(
                f"PEA Dashboard · {datetime.now().strftime('%d/%m/%Y')} · "
                "Données yfinance · Document confidentiel",
                st_mono))

            doc.build(story)
            pdf_bytes = buf.getvalue()

            st.success("✓ Rapport généré avec succès !")
            st.download_button(
                label="⬇  Télécharger le rapport PDF",
                data=pdf_bytes,
                file_name=f"rapport_pea_{datetime.now().strftime('%Y%m')}.pdf",
                mime="application/pdf",
                use_container_width=False,
            )

            # Aperçu
            section_label("Aperçu du contenu")
            preview_items = [
                ("Valorisation", f"Capital versé, investi, +/− latente, liquidités, valeur totale"),
                ("Positions", f"{len(df_pos)} lignes · PRU, cours, valeur, P&L"),
                ("Scores 10-Baggers", "Scores fondamentaux /100 pour chaque action" if include_scores else "Non inclus"),
                ("Signaux techniques", "RSI, position 52s, signal principal" if include_signals else "Non inclus"),
            ]
            prev_html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">'
            for title, desc in preview_items:
                prev_html += (f'<div style="background:var(--s1);border:1px solid var(--border);'
                              f'border-radius:9px;padding:12px 15px">'
                              f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;'
                              f'color:var(--green);text-transform:uppercase;letter-spacing:0.1em;'
                              f'margin-bottom:4px">{title}</div>'
                              f'<div style="font-family:Outfit,sans-serif;font-size:0.8rem;'
                              f'color:var(--t2)">{desc}</div></div>')
            prev_html += '</div>'
            st.markdown(prev_html, unsafe_allow_html=True)

        except ImportError:
            st.error("reportlab non installé. Lancez : `pip install reportlab`")
        except Exception as e:
            st.error(f"Erreur génération PDF : {e}")
            import traceback
            st.code(traceback.format_exc())



# ══════════════════════════════════════════════════════════════════════════════
# PAGE — SIMULATEUR D'ÉPARGNE PROGRAMMÉE
# ══════════════════════════════════════════════════════════════════════════════

def page_simulateur():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">💰 Projection financière</div>'
                '<div class="ph-title">Simulateur</div>'
                '<div class="ph-sub">Épargne programmée · Intérêts composés · Scénarios comparés</div>'
                '</div>', unsafe_allow_html=True)

    # ── Récupération capital actuel ───────────────────────────────────────────
    capital_actuel = 0.0
    try:
        df_hist, df_corr, df_vers = load_data()
        df_pos, s = compute_portfolio(df_hist, df_corr, df_vers)
        capital_actuel = s["total_valeur"] + s["liquidites"]
    except:
        pass

    # ══════════════════════════════════════════════════════════════════════════
    # PARAMÈTRES — 3 scénarios côte à côte
    # ══════════════════════════════════════════════════════════════════════════
    section_label("Paramètres des scénarios")

    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:var(--t3);'
                'margin-bottom:1rem">Comparez jusqu\'à 3 scénarios simultanément. '
                'Capital de départ pré-rempli depuis votre portefeuille réel.</div>',
                unsafe_allow_html=True)

    SCENARIO_COLORS = ["#22c55e", "#3b82f6", "#f59e0b"]
    SCENARIO_NAMES  = ["Scénario A", "Scénario B", "Scénario C"]

    col_a, col_b, col_c = st.columns(3)
    scenarios = []

    for i, (col, color, name) in enumerate(zip([col_a, col_b, col_c], SCENARIO_COLORS, SCENARIO_NAMES)):
        with col:
            # Header coloré
            st.markdown(f'<div style="background:rgba({",".join(str(int(color.lstrip("#")[j:j+2],16)) for j in (0,2,4))},0.08);'
                        f'border:1px solid {color}33;border-radius:10px;padding:14px 16px;margin-bottom:12px">'
                        f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:{color};'
                        f'text-transform:uppercase;letter-spacing:0.12em;font-weight:600">{name}</div>'
                        f'</div>', unsafe_allow_html=True)

            capital   = st.number_input("Capital initial (€)", value=round(capital_actuel) if i == 0 else 0,
                                         min_value=0, step=500, key=f"sim_cap_{i}", format="%d")
            versement = st.number_input("Versement mensuel (€)", value=200 + i*100,
                                         min_value=0, step=50, key=f"sim_vers_{i}", format="%d")
            perf_an   = st.slider("Performance annuelle (%)", 0.0, 20.0,
                                   [5.0, 8.0, 12.0][i], 0.5, key=f"sim_perf_{i}")
            duree     = st.slider("Durée (années)", 1, 40,
                                   [10, 15, 20][i], 1, key=f"sim_dur_{i}")
            frais     = st.number_input("Frais annuels (%)", value=0.3, min_value=0.0,
                                         max_value=5.0, step=0.1, key=f"sim_frais_{i}", format="%.1f")
            actif     = st.toggle("Actif", value=True, key=f"sim_on_{i}")

            scenarios.append({
                "name": name, "color": color, "capital": capital,
                "versement": versement, "perf": perf_an, "duree": duree,
                "frais": frais, "actif": actif,
            })

    # ══════════════════════════════════════════════════════════════════════════
    # CALCUL des projections mois par mois
    # ══════════════════════════════════════════════════════════════════════════
    def simulate(capital, versement, perf_an, duree, frais):
        """Simulation mensuelle. Retourne liste de dicts par mois."""
        rate_mensuel = (1 + (perf_an - frais) / 100) ** (1/12) - 1
        rows = []
        val = float(capital)
        total_verse = float(capital)
        total_interets = 0.0

        for mois in range(1, duree * 12 + 1):
            interets = val * rate_mensuel
            val = val + interets + versement
            total_verse    += versement
            total_interets += interets
            rows.append({
                "mois":            mois,
                "annee":           mois / 12,
                "valeur":          val,
                "total_verse":     total_verse,
                "total_interets":  total_interets,
                "interets_mois":   interets,
            })
        return rows

    results = []
    for sc in scenarios:
        if sc["actif"]:
            data = simulate(sc["capital"], sc["versement"], sc["perf"], sc["duree"], sc["frais"])
            results.append({"sc": sc, "data": data})

    if not results:
        st.info("Activez au moins un scénario.")
        return

    # ══════════════════════════════════════════════════════════════════════════
    # KPIs FINAUX
    # ══════════════════════════════════════════════════════════════════════════
    section_label("Résultats finaux")

    kpi_cols = st.columns(len(results))
    for col, res in zip(kpi_cols, results):
        sc   = res["sc"]
        last = res["data"][-1]
        val_finale     = last["valeur"]
        total_verse    = last["total_verse"]
        total_interets = last["total_interets"]
        mult = val_finale / total_verse if total_verse > 0 else 1
        c = sc["color"]

        with col:
            st.markdown(
                f'<div style="background:var(--s1);border:1px solid {c}33;border-radius:13px;'
                f'padding:22px 20px;text-align:center;position:relative;overflow:hidden">'
                f'<div style="position:absolute;top:0;left:0;right:0;height:2px;background:{c}"></div>'
                f'<div style="font-family:DM Mono,monospace;font-size:0.58rem;color:var(--t3);'
                f'text-transform:uppercase;letter-spacing:0.12em;margin-bottom:8px">{sc["name"]}</div>'
                f'<div style="font-family:Outfit,sans-serif;font-size:2.2rem;font-weight:900;'
                f'color:{c};letter-spacing:-0.03em;line-height:1">'
                f'{val_finale:,.0f} €</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:0.62rem;color:var(--t3);'
                f'margin-top:6px">après {sc["duree"]} ans</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:16px">'
                f'<div style="background:var(--s2);border-radius:8px;padding:10px">'
                f'<div style="font-family:DM Mono,monospace;font-size:0.52rem;color:var(--t3);'
                f'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px">Versé</div>'
                f'<div style="font-family:Outfit,sans-serif;font-size:0.95rem;font-weight:700;'
                f'color:var(--t2)">{total_verse:,.0f} €</div></div>'
                f'<div style="background:var(--s2);border-radius:8px;padding:10px">'
                f'<div style="font-family:DM Mono,monospace;font-size:0.52rem;color:var(--t3);'
                f'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px">Intérêts</div>'
                f'<div style="font-family:Outfit,sans-serif;font-size:0.95rem;font-weight:700;'
                f'color:{c}">{total_interets:,.0f} €</div></div>'
                f'</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:{c};'
                f'font-weight:600;margin-top:12px">×{mult:.2f} mise de fonds</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # ══════════════════════════════════════════════════════════════════════════
    # GRAPHIQUES
    # ══════════════════════════════════════════════════════════════════════════
    section_label("Évolution de la valeur du portefeuille")

    view_opt = st.radio("Vue", ["Valeur totale", "Décomposition versé / intérêts", "Intérêts mensuels"],
                        horizontal=True, key="sim_view")

    fig_main = go.Figure()

    for res in results:
        sc   = res["sc"]
        data = res["data"]
        xs   = [d["annee"] for d in data]

        if view_opt == "Valeur totale":
            fig_main.add_trace(go.Scatter(
                x=xs, y=[d["valeur"] for d in data],
                name=f'{sc["name"]} ({sc["perf"]}%/an)',
                line=dict(color=sc["color"], width=2.5),
                hovertemplate=(f'<b>{sc["name"]}</b> — %{{x:.1f}} ans<br>'
                               f'Valeur : %{{y:,.0f}} €<extra></extra>'),
            ))
            # Zone versé en transparence (seulement scénario A)
            if sc["name"] == results[0]["sc"]["name"]:
                fig_main.add_trace(go.Scatter(
                    x=xs, y=[d["total_verse"] for d in data],
                    name="Capital versé", fill="tozeroy",
                    line=dict(color="#1a2538", width=0),
                    fillcolor="rgba(26,37,56,0.5)",
                    hovertemplate='Capital versé : %{y:,.0f} €<extra></extra>',
                ))

        elif view_opt == "Décomposition versé / intérêts":
            fig_main.add_trace(go.Scatter(
                x=xs, y=[d["total_verse"] for d in data],
                name=f'{sc["name"]} — Versé',
                stackgroup=sc["name"],
                line=dict(color="#1a2538", width=0),
                fillcolor=sc["color"] + "33",
                hovertemplate='Versé : %{y:,.0f} €<extra></extra>',
            ))
            fig_main.add_trace(go.Scatter(
                x=xs, y=[d["total_interets"] for d in data],
                name=f'{sc["name"]} — Intérêts',
                stackgroup=sc["name"],
                line=dict(color=sc["color"], width=1.5),
                fillcolor=sc["color"] + "66",
                hovertemplate=f'<b>{sc["name"]}</b> Intérêts : %{{y:,.0f}} €<extra></extra>',
            ))

        else:  # Intérêts mensuels
            fig_main.add_trace(go.Scatter(
                x=xs, y=[d["interets_mois"] for d in data],
                name=f'{sc["name"]} — intérêts/mois',
                line=dict(color=sc["color"], width=2),
                hovertemplate=(f'<b>{sc["name"]}</b> %{{x:.1f}} ans<br>'
                               f'Intérêts ce mois : %{{y:,.0f}} €/mois<extra></extra>'),
            ))

    if view_opt == "Valeur totale":
        yopts = {"ticksuffix": " €", "tickformat": ",.0f"}
    else:
        yopts = {"ticksuffix": " €", "tickformat": ",.0f"}

    fig_main.update_layout(**plotly_base(380, yopts))
    fig_main.update_layout(xaxis=dict(ticksuffix=" ans", gridcolor="#1a2538"))
    st.plotly_chart(fig_main, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # POINT DE BASCULE — quand les intérêts dépassent les versements
    # ══════════════════════════════════════════════════════════════════════════
    section_label("Point de bascule — les intérêts dépassent les versements")

    bascule_html = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">'
    for res in results:
        sc   = res["sc"]
        data = res["data"]
        bascule = None
        for d in data:
            if d["interets_mois"] >= sc["versement"] and sc["versement"] > 0:
                bascule = d
                break
        c = sc["color"]
        if bascule:
            ans   = int(bascule["annee"])
            mois  = int((bascule["annee"] - ans) * 12)
            label = f"{ans} ans {mois} mois"
            val   = f"{bascule['valeur']:,.0f} €"
            sub   = f"Les intérêts ({bascule['interets_mois']:,.0f} €/mois) dépassent les versements ({sc['versement']:,} €/mois)"
        elif sc["versement"] == 0:
            label = "—"
            val   = "Pas de versement"
            sub   = "Sans versement mensuel, pas de point de bascule à calculer"
        else:
            label = f"> {sc['duree']} ans"
            val   = "Hors période"
            sub   = "Augmente la durée ou la performance pour atteindre ce cap"

        bascule_html += (
            f'<div style="background:var(--s1);border:1px solid {c}33;border-radius:11px;'
            f'padding:18px 20px;position:relative;overflow:hidden">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:2px;background:{c}"></div>'
            f'<div style="font-family:DM Mono,monospace;font-size:0.58rem;color:{c};'
            f'text-transform:uppercase;letter-spacing:0.12em;margin-bottom:8px">{sc["name"]}</div>'
            f'<div style="font-family:Outfit,sans-serif;font-size:1.6rem;font-weight:900;'
            f'color:{c};letter-spacing:-0.02em;line-height:1">{label}</div>'
            f'<div style="font-family:Outfit,sans-serif;font-size:0.85rem;color:var(--t2);'
            f'margin-top:4px">{val}</div>'
            f'<div style="font-family:DM Mono,monospace;font-size:0.58rem;color:var(--t3);'
            f'margin-top:8px;line-height:1.6">{sub}</div>'
            f'</div>'
        )
    bascule_html += '</div>'
    st.markdown(bascule_html, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TABLE ANNUELLE DÉTAILLÉE
    # ══════════════════════════════════════════════════════════════════════════
    section_label("Table de projection annuelle")

    # Sélecteur scénario pour la table
    sc_names_actifs = [res["sc"]["name"] for res in results]
    sel_sc_name = st.radio("Scénario à détailler", sc_names_actifs,
                           horizontal=True, key="sim_table_sc")
    sel_res = next(r for r in results if r["sc"]["name"] == sel_sc_name)
    sc_sel  = sel_res["sc"]
    data    = sel_res["data"]

    # Agrège par année
    ann_rows = []
    for annee in range(1, sc_sel["duree"] + 1):
        mois_data = [d for d in data if int(d["annee"]) == annee - 1
                     or (d["mois"] == annee * 12)]
        d_an = next((d for d in data if d["mois"] == annee * 12), data[-1])
        vers_an = sc_sel["versement"] * 12
        int_an  = sum(d["interets_mois"] for d in data
                      if (annee-1)*12 < d["mois"] <= annee*12)
        ann_rows.append({
            "Année":            annee,
            "Valeur fin d'année": d_an["valeur"],
            "Versé (cumul)":    d_an["total_verse"],
            "Intérêts (année)": int_an,
            "Intérêts (cumul)": d_an["total_interets"],
            "Part intérêts":    d_an["total_interets"] / d_an["valeur"] * 100 if d_an["valeur"] else 0,
        })

    rows_t = ""
    for r in ann_rows:
        int_pct = r["Part intérêts"]
        bar_w   = min(100, int(int_pct))
        int_c   = "#22c55e" if int_pct > 50 else ("#f59e0b" if int_pct > 25 else "#3b82f6")

        rows_t += (
            f'<tr>'
            f'<td style="font-family:DM Mono,monospace;font-size:0.72rem;'
            f'color:{sc_sel["color"]};font-weight:600">Année {r["Année"]}</td>'
            f'<td><b>{r["Valeur fin d\'année"]:,.0f} €</b></td>'
            f'<td>{r["Versé (cumul)"]:,.0f} €</td>'
            f'<td style="color:#22c55e">{r["Intérêts (année)"]:+,.0f} €</td>'
            f'<td>{r["Intérêts (cumul)"]:,.0f} €</td>'
            f'<td><div style="display:flex;align-items:center;gap:8px;justify-content:flex-end">'
            f'<span style="font-family:DM Mono,monospace;font-size:0.7rem;color:{int_c}">'
            f'{int_pct:.0f}%</span>'
            f'<div style="width:55px;height:5px;background:var(--s3);border-radius:3px;overflow:hidden">'
            f'<div style="width:{bar_w}%;height:100%;background:{int_c};border-radius:3px"></div>'
            f'</div></div></td>'
            f'</tr>'
        )

    st.markdown(
        f'<div style="background:var(--s1);border:1px solid var(--border);'
        f'border-radius:11px;overflow:hidden;margin-bottom:1.5rem">'
        f'<table class="ptable"><thead><tr>'
        f'<th style="text-align:left">Période</th>'
        f'<th>Valeur totale</th>'
        f'<th>Capital versé</th>'
        f'<th>Intérêts (année)</th>'
        f'<th>Intérêts (cumul)</th>'
        f'<th>Part intérêts</th>'
        f'</tr></thead><tbody>{rows_t}</tbody></table></div>',
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════════════════════════════════════════
    # GRAPHIQUE CAMEMBERT FINAL — versé vs intérêts
    # ══════════════════════════════════════════════════════════════════════════
    section_label("Composition finale du capital")

    pie_cols = st.columns(len(results))
    for col, res in zip(pie_cols, results):
        sc   = res["sc"]
        last = res["data"][-1]
        with col:
            fig_pie = go.Figure(go.Pie(
                labels=["Capital versé", "Intérêts composés"],
                values=[last["total_verse"], max(0, last["total_interets"])],
                hole=0.55,
                marker=dict(colors=["#1a2538", sc["color"]]),
                textfont=dict(family="DM Mono", size=9),
                hovertemplate="<b>%{label}</b><br>%{value:,.0f} €  (%{percent})<extra></extra>",
            ))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=30, b=10),
                height=220,
                showlegend=True,
                legend=dict(orientation="h", x=0.5, xanchor="center",
                            y=-0.1, font=dict(family="DM Mono", size=8),
                            bgcolor="rgba(0,0,0,0)"),
                title=dict(text=sc["name"], font=dict(family="Outfit", size=11,
                           color="#94a3b8"), x=0.5),
                font=dict(family="DM Mono", color="#94a3b8"),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # RÈGLE DES 72 et insights
    # ══════════════════════════════════════════════════════════════════════════
    section_label("Insights & Règle des 72")

    insights_html = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">'
    for res in results:
        sc   = res["sc"]
        last = res["data"][-1]
        c    = sc["color"]
        perf_nette = sc["perf"] - sc["frais"]

        # Règle des 72
        if perf_nette > 0:
            double_years = 72 / perf_nette
            double_str   = f"{double_years:.1f} ans"
        else:
            double_str = "∞"

        # Taux d'effort mensuel (versement / valeur finale)
        effort = sc["versement"] / (last["valeur"] / (sc["duree"] * 12)) if last["valeur"] > 0 else 0

        insights_html += (
            f'<div style="background:var(--s1);border:1px solid {c}22;border-radius:11px;padding:16px 18px">'
            f'<div style="font-family:DM Mono,monospace;font-size:0.58rem;color:{c};'
            f'text-transform:uppercase;letter-spacing:0.12em;margin-bottom:10px">{sc["name"]}</div>'

            f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:var(--t3);margin-bottom:2px">'
            f'Doublement du capital (règle des 72)</div>'
            f'<div style="font-family:Outfit,sans-serif;font-size:1.1rem;font-weight:700;'
            f'color:{c};margin-bottom:10px">{double_str}</div>'

            f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:var(--t3);margin-bottom:2px">'
            f'Performance nette de frais</div>'
            f'<div style="font-family:Outfit,sans-serif;font-size:1.1rem;font-weight:700;'
            f'color:var(--text);margin-bottom:10px">{perf_nette:.1f}%/an</div>'

            f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:var(--t3);margin-bottom:2px">'
            f'Versement total sur la période</div>'
            f'<div style="font-family:Outfit,sans-serif;font-size:1.1rem;font-weight:700;'
            f'color:var(--text);margin-bottom:10px">'
            f'{sc["versement"] * sc["duree"] * 12:,.0f} €</div>'

            f'<div style="font-family:DM Mono,monospace;font-size:0.58rem;color:var(--t3);'
            f'border-top:1px solid var(--border);padding-top:8px;margin-top:4px;line-height:1.8">'
            f'{sc["versement"]:,} €/mois · {sc["perf"]}%/an · {sc["duree"]} ans<br>'
            f'Frais : {sc["frais"]}%/an · Départ : {sc["capital"]:,} €'
            f'</div></div>'
        )
    insights_html += '</div>'
    st.markdown(insights_html, unsafe_allow_html=True)




# ══════════════════════════════════════════════════════════════════════════════
# PAGE — JOURNAL DE TRADING
# ══════════════════════════════════════════════════════════════════════════════

def page_journal():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">📓 Suivi décisionnel</div>'
                '<div class="ph-title">Journal de Trading</div>'
                '<div class="ph-sub">Annotations · Thèses d\'investissement · Historique des décisions</div>'
                '</div>', unsafe_allow_html=True)

    journal = get_state("journal", [])

    # ── Formulaire nouvelle entrée ─────────────────────────────────────────────
    with st.expander("➕  Nouvelle entrée", expanded=len(journal) == 0):
        j1, j2, j3 = st.columns([1, 1, 1])
        with j1:
            j_date   = st.date_input("Date", value=datetime.today(), key="j_date")
            j_ticker = st.text_input("Ticker", placeholder="MC.PA", key="j_ticker").upper()
        with j2:
            j_action = st.selectbox("Action", ["Achat", "Vente", "Renforcement",
                                                "Allègement", "Observation", "Analyse"], key="j_act")
            j_prix   = st.number_input("Prix (€)", value=0.0, min_value=0.0,
                                        step=0.01, format="%.2f", key="j_prix")
        with j3:
            j_emotion = st.selectbox("Contexte émotionnel",
                                      ["Confiant", "Neutre", "Hésitant",
                                       "FOMO", "Panique", "Discipliné"], key="j_emo")
            j_conviction = st.slider("Conviction (1→10)", 1, 10, 7, key="j_conv")

        j_these  = st.text_area("Thèse d'investissement",
                                  placeholder="Pourquoi cette décision ? Quels sont les catalyseurs attendus ?",
                                  height=80, key="j_these")
        j_risques = st.text_area("Risques identifiés",
                                  placeholder="Quels sont les scénarios défavorables ?",
                                  height=60, key="j_risques")

        j_tags = st.multiselect("Tags", ["Fondamental", "Technique", "Macro", "Dividende",
                                          "Croissance", "Value", "Momentum", "Contrarian",
                                          "Long terme", "Court terme"], key="j_tags")

        if st.button("💾  Enregistrer l'entrée", type="primary", key="j_save"):
            if j_ticker and j_these:
                entry = {
                    "id":         len(journal) + 1,
                    "date":       str(j_date),
                    "ticker":     j_ticker,
                    "action":     j_action,
                    "prix":       j_prix,
                    "these":      j_these,
                    "risques":    j_risques,
                    "emotion":    j_emotion,
                    "conviction": j_conviction,
                    "tags":       j_tags,
                    "created_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
                }
                journal.insert(0, entry)
                set_state("journal", journal)
                st.success("✓ Entrée enregistrée !")
                st.rerun()
            else:
                st.warning("Ticker et thèse obligatoires.")

    if not journal:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">📓</div>
          <div class="empty-title">Journal vide</div>
          <div class="empty-sub">Commencez par enregistrer votre première décision d'investissement.<br>
          C'est l'outil le plus puissant pour progresser.</div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Filtres ───────────────────────────────────────────────────────────────
    section_label(f"Entrées · {len(journal)} décisions enregistrées")

    jf1, jf2, jf3 = st.columns(3)
    with jf1:
        filter_tk = st.text_input("Filtrer par ticker", placeholder="MC.PA…", key="jf_tk").upper()
    with jf2:
        filter_act = st.multiselect("Type d'action", ["Achat", "Vente", "Renforcement",
                                                        "Allègement", "Observation", "Analyse"],
                                    key="jf_act")
    with jf3:
        filter_tag = st.multiselect("Tags", ["Fondamental", "Technique", "Macro", "Dividende",
                                              "Croissance", "Value", "Momentum", "Contrarian",
                                              "Long terme", "Court terme"], key="jf_tag")

    filtered_j = journal
    if filter_tk:
        filtered_j = [e for e in filtered_j if filter_tk in e.get("ticker","")]
    if filter_act:
        filtered_j = [e for e in filtered_j if e.get("action") in filter_act]
    if filter_tag:
        filtered_j = [e for e in filtered_j if any(t in e.get("tags",[]) for t in filter_tag)]

    # ── Stats rapides ──────────────────────────────────────────────────────────
    n_achats  = sum(1 for e in journal if e.get("action") in ["Achat","Renforcement"])
    n_ventes  = sum(1 for e in journal if e.get("action") in ["Vente","Allègement"])
    avg_conv  = sum(e.get("conviction",5) for e in journal) / len(journal) if journal else 0
    tickers_u = len({e["ticker"] for e in journal if e.get("ticker")})

    kpi_j = (
        f'<div class="kpi-row" style="grid-template-columns:repeat(4,1fr)">'
        + kpi_card("Entrées totales", str(len(journal)),
                   top_color="linear-gradient(90deg,#3b82f6,transparent)")
        + kpi_card("Achats / Renforts", str(n_achats),
                   top_color="linear-gradient(90deg,#22c55e,transparent)")
        + kpi_card("Ventes / Allègements", str(n_ventes),
                   top_color="linear-gradient(90deg,#ef4444,transparent)")
        + kpi_card("Conviction moyenne", f"{avg_conv:.1f}/10",
                   top_color=f"linear-gradient(90deg,{'#22c55e' if avg_conv>=7 else '#f59e0b'},transparent)")
        + '</div>'
    )
    st.markdown(kpi_j, unsafe_allow_html=True)

    # ── Affichage des entrées ──────────────────────────────────────────────────
    ACTION_COLOR = {
        "Achat": "#22c55e", "Renforcement": "#16a34a",
        "Vente": "#ef4444", "Allègement": "#dc2626",
        "Observation": "#3b82f6", "Analyse": "#8b5cf6",
    }
    EMOTION_ICON = {
        "Confiant": "💪", "Neutre": "😐", "Hésitant": "🤔",
        "FOMO": "😰", "Panique": "😱", "Discipliné": "🎯",
    }

    for i, entry in enumerate(filtered_j):
        ac  = ACTION_COLOR.get(entry.get("action","Observation"), "#475569")
        emo = EMOTION_ICON.get(entry.get("emotion","Neutre"), "😐")
        conv = entry.get("conviction", 5)
        conv_c = "#22c55e" if conv >= 8 else ("#f59e0b" if conv >= 5 else "#ef4444")
        tags_html = "".join(
            f'<span style="font-family:DM Mono,monospace;font-size:0.55rem;color:#3b82f6;'
            f'background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);'
            f'border-radius:3px;padding:1px 6px;margin-right:4px">{t}</span>'
            for t in entry.get("tags", [])
        )

        with st.expander(
            f"{entry.get('date','')}  ·  {entry.get('ticker','')}  ·  "
            f"{entry.get('action','')}  ·  {emo} {entry.get('emotion','')}",
            expanded=(i == 0)
        ):
            ec1, ec2 = st.columns([3, 1])
            with ec1:
                st.markdown(
                    f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:{ac};'
                    f'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">'
                    f'{entry.get("action","")} · {entry.get("ticker","")} '
                    f'{"@ "+str(entry.get("prix",""))+" €" if entry.get("prix",0)>0 else ""}'
                    f'</div>'
                    f'<div style="font-family:Outfit,sans-serif;font-size:0.88rem;'
                    f'color:var(--text);line-height:1.6;margin-bottom:10px">'
                    f'<b style="color:var(--t3);font-size:0.75rem">THÈSE</b><br>'
                    f'{entry.get("these","")}</div>',
                    unsafe_allow_html=True
                )
                if entry.get("risques"):
                    st.markdown(
                        f'<div style="font-family:Outfit,sans-serif;font-size:0.82rem;'
                        f'color:var(--t2);line-height:1.5;margin-bottom:8px">'
                        f'<b style="color:#ef4444;font-size:0.72rem">RISQUES</b><br>'
                        f'{entry.get("risques","")}</div>',
                        unsafe_allow_html=True
                    )
                if tags_html:
                    st.markdown(f'<div style="margin-top:6px">{tags_html}</div>',
                                unsafe_allow_html=True)
            with ec2:
                conv_ring_dash = 2 * 3.14159 * 18 * conv / 10
                conv_ring_gap  = 2 * 3.14159 * 18 - conv_ring_dash
                st.markdown(
                    f'<div style="text-align:center;background:var(--s2);border-radius:10px;'
                    f'padding:14px 10px">'
                    f'<svg width="60" height="60" viewBox="0 0 60 60" style="transform:rotate(-90deg)">'
                    f'<circle cx="30" cy="30" r="18" fill="none" stroke="#1a2538" stroke-width="4"/>'
                    f'<circle cx="30" cy="30" r="18" fill="none" stroke="{conv_c}" stroke-width="4"'
                    f' stroke-linecap="round"'
                    f' stroke-dasharray="{conv_ring_dash:.1f} {conv_ring_gap:.1f}"/>'
                    f'</svg>'
                    f'<div style="font-family:Outfit,sans-serif;font-size:1.2rem;font-weight:800;'
                    f'color:{conv_c};margin-top:-44px;margin-bottom:34px">{conv}</div>'
                    f'<div style="font-family:DM Mono,monospace;font-size:0.52rem;color:var(--t3)'
                    f';text-transform:uppercase;letter-spacing:0.1em">Conviction</div>'
                    f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:var(--t3);'
                    f'margin-top:8px">{entry.get("created_at","")}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            if st.button(f"🗑 Supprimer", key=f"j_del_{i}"):
                journal.pop(journal.index(entry))
                set_state("journal", journal)
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE — DIVIDENDES
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600)
def get_dividends_for(ticker: str, start: str):
    try:
        d = yf.Ticker(ticker).dividends
        if d.empty: return pd.Series(dtype=float)
        d.index = d.index.tz_localize(None)
        return d[d.index >= pd.Timestamp(start)]
    except:
        return pd.Series(dtype=float)

def page_dividendes():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">💸 Revenus passifs</div>'
                '<div class="ph-title">Dividendes</div>'
                '<div class="ph-sub">Historique · Projection · Revenus passifs mensuels</div>'
                '</div>', unsafe_allow_html=True)

    try:
        df_hist, df_corr, df_vers = load_data()
        df_pos, s = compute_portfolio(df_hist, df_corr, df_vers)
    except Exception as e:
        st.error(f"Fichiers introuvables : {e}"); return

    port_tickers_d = [(r["Ticker"], r["Titre"], r["Quantité"], r["Valeur (€)"])
                      for _, r in df_pos.iterrows()
                      if r["Ticker"] and r["Ticker"] != "N/A"]

    # ── Calcul des dates d'entrée par ticker depuis l'historique réel ────────
    corr_fwd = dict(zip(df_corr["Libelle_fortuneo"], df_corr["code_yfinance"]))

    first_buy = {}
    for _, row in df_hist.iterrows():
        op  = str(row.get("Opération","")).strip().lower()
        lib = str(row.get("libellé","")).strip()
        dt  = row.get("Date")
        tk  = corr_fwd.get(lib)
        if "achat" in op and tk and dt is not None:
            ts = pd.Timestamp(dt)
            if tk not in first_buy or ts < first_buy[tk]:
                first_buy[tk] = ts

    # ── Données dividendes ────────────────────────────────────────────────────
    section_label("Dividendes — Historique & Projection")

    per_div = st.radio("Fenêtre d'analyse", ["1 an", "3 ans", "5 ans", "Max"],
                       horizontal=True, key="div_per")
    fenetre_days = {"1 an":365,"3 ans":1095,"5 ans":1825,"Max":7300}[per_div]
    fenetre_start = datetime.today() - timedelta(days=fenetre_days)

    all_divs = {}
    total_div_annuel = 0.0
    div_par_ticker   = {}

    with st.spinner("Récupération des dividendes…"):
        for tk, titre, qty, val in port_tickers_d:
            date_entree = first_buy.get(tk)

            if date_entree is None:
                div_par_ticker[tk] = {"titre": titre, "qty": qty, "val": val,
                                      "divs": pd.Series(dtype=float),
                                      "date_entree": None, "yield": 0}
                continue

            # Borne = MAX(premier achat, début fenêtre) — en tz-naive
            date_debut_reelle = max(date_entree, pd.Timestamp(fenetre_start))
            # S'assurer tz-naive
            if date_debut_reelle.tzinfo is not None:
                date_debut_reelle = date_debut_reelle.tz_localize(None)

            try:
                raw = yf.Ticker(tk).dividends
                if raw.empty:
                    divs_miens = pd.Series(dtype=float)
                else:
                    # Normaliser l'index en tz-naive quel que soit le format yfinance
                    if raw.index.tzinfo is not None or hasattr(raw.index, 'tz') and raw.index.tz is not None:
                        raw.index = raw.index.tz_convert("UTC").tz_localize(None)
                    else:
                        raw.index = pd.to_datetime(raw.index)
                    # Filtre strict : seulement après ton achat réel ET dans la fenêtre
                    divs_miens = raw[raw.index >= date_debut_reelle]
            except Exception:
                divs_miens = pd.Series(dtype=float)

            if not divs_miens.empty:
                all_divs[tk] = divs_miens * qty
            div_par_ticker[tk] = {"titre": titre, "qty": qty, "val": val,
                                  "divs": divs_miens, "date_entree": date_entree, "yield": 0}

    # Yield actuel → projection
    for tk, titre, qty, val in port_tickers_d:
        try:
            info_tk = yf.Ticker(tk).info
            dy_raw = float(info_tk.get("dividendYield", 0) or 0)
            # yfinance retourne parfois le yield × 100 (ex: 1.93 au lieu de 0.0193)
            # Sanity check : un yield >1 (=100%) est impossible → diviser par 100
            if dy_raw > 1:
                dy_raw = dy_raw / 100
            # Cap à 25% max pour éviter les données corrompues
            dy = min(dy_raw, 0.25)
            div_par_ticker.setdefault(tk, {"titre": titre, "qty": qty, "val": val,
                                           "divs": pd.Series(dtype=float),
                                           "date_entree": first_buy.get(tk), "yield": 0})
            div_par_ticker[tk]["yield"] = dy
            total_div_annuel += val * dy
        except:
            pass

    # KPIs
    total_div_hist   = sum(s.sum() for s in all_divs.values()) if all_divs else 0
    div_mensuel_proj = total_div_annuel / 12

    # ── Debug expander pour vérifier les données brutes ───────────────────────
    with st.expander("🔍 Données brutes (debug — cliquer pour vérifier)"):
        for tk, info_d in div_par_ticker.items():
            de = info_d.get("date_entree")
            divs = info_d["divs"]
            st.markdown(f"**{tk}** — achat : `{de.strftime('%d/%m/%Y') if de else 'inconnu'}` "
                        f"— fenêtre : `{fenetre_start.strftime('%d/%m/%Y')}` → aujourd'hui "
                        f"— {len(divs)} versements trouvés après filtre")
            if not divs.empty:
                st.dataframe(divs.reset_index().rename(columns={0:"Dividende/action","index":"Date"}),
                             use_container_width=True, hide_index=True)

    kpi_d = (
        f'<div class="kpi-row" style="grid-template-columns:repeat(4,1fr)">'
        + kpi_card("Dividendes réellement reçus",
                   f"{total_div_hist:,.2f} €" if total_div_hist > 0 else "0 €",
                   "depuis votre date d'achat" if total_div_hist > 0 else "Aucun versement détecté",
                   total_div_hist > 0,
                   top_color="linear-gradient(90deg,#22c55e,transparent)")
        + kpi_card("Revenus annuels projetés", f"{total_div_annuel:,.0f} €",
                   "yield actuel × valeur positions",
                   top_color="linear-gradient(90deg,#3b82f6,transparent)")
        + kpi_card("Revenus mensuels projetés", f"{div_mensuel_proj:,.0f} €/mois",
                   top_color="linear-gradient(90deg,#8b5cf6,transparent)")
        + kpi_card("Yield moyen portefeuille",
                   f"{(total_div_annuel / s['total_valeur'] * 100) if s['total_valeur'] > 0 else 0:.2f}%",
                   top_color="linear-gradient(90deg,#f59e0b,transparent)")
        + '</div>'
    )
    st.markdown(kpi_d, unsafe_allow_html=True)

    if total_div_hist == 0:
        st.markdown(
            '<div style="background:rgba(59,130,246,0.07);border:1px solid rgba(59,130,246,0.2);'
            'border-radius:10px;padding:12px 16px;margin-bottom:1rem;font-family:DM Mono,monospace;'
            'font-size:0.65rem;color:#3b82f6">ℹ Aucun dividende détecté depuis vos dates d\'achat réelles. '
            'Raisons possibles : positions récentes (pas encore passé la date de détachement), '
            'ETF à capitalisation (Acc), ou actions qui ne versent pas de dividende. '
            'La projection est basée sur le yield actuel annoncé par yfinance.</div>',
            unsafe_allow_html=True
        )

    # ── Graphique historique des dividendes ────────────────────────────────────
    if all_divs:
        # Agrège tous les dividendes par mois
        all_series = []
        for tk, divs in all_divs.items():
            df_tmp = divs.reset_index()
            df_tmp.columns = ["Date", "Montant"]
            df_tmp["Ticker"] = tk
            all_series.append(df_tmp)
        df_all_divs = pd.concat(all_series).sort_values("Date")
        df_all_divs["Mois"] = df_all_divs["Date"].dt.to_period("M").dt.to_timestamp()
        df_monthly = df_all_divs.groupby(["Mois","Ticker"])["Montant"].sum().reset_index()

        fig_dh = go.Figure()
        colors_d = P_COLORS * 3
        for ci, tk in enumerate(df_monthly["Ticker"].unique()):
            df_tk = df_monthly[df_monthly["Ticker"] == tk]
            fig_dh.add_trace(go.Bar(
                x=df_tk["Mois"], y=df_tk["Montant"],
                name=tk, marker_color=colors_d[ci % len(colors_d)],
                hovertemplate=f"<b>{tk}</b> %{{x|%b %Y}}<br>%{{y:,.2f}} €<extra></extra>",
            ))
        fig_dh.update_layout(**plotly_base(280, {"ticksuffix":" €","tickformat":",.0f"}))
        fig_dh.update_layout(barmode="stack")
        st.plotly_chart(fig_dh, use_container_width=True)

    # ── Projection revenus futurs ──────────────────────────────────────────────
    section_label("Projection des revenus passifs futurs")

    proj_years = st.slider("Horizon de projection (ans)", 1, 20, 10, key="div_proj")
    growth_rate = st.slider("Croissance annuelle des dividendes (%)", 0.0, 15.0, 5.0, 0.5, key="div_growth")

    fig_proj = go.Figure()
    years = list(range(1, proj_years + 1))

    # Mensuel projeté avec croissance
    monthly_proj = [(total_div_annuel / 12) * ((1 + growth_rate/100) ** y) for y in years]
    annual_proj  = [total_div_annuel * ((1 + growth_rate/100) ** y) for y in years]
    cumul_proj   = [sum(annual_proj[:i+1]) for i in range(len(annual_proj))]

    fig_proj.add_trace(go.Bar(
        x=years, y=annual_proj, name="Revenus annuels",
        marker_color="#22c55e", marker_opacity=0.7,
        hovertemplate="Année %{x}<br>Revenus : %{y:,.0f} €/an<extra></extra>",
    ))
    fig_proj.add_trace(go.Scatter(
        x=years, y=cumul_proj, name="Cumul revenus",
        line=dict(color="#3b82f6", width=2, dash="dash"), yaxis="y2",
        hovertemplate="Année %{x}<br>Cumul : %{y:,.0f} €<extra></extra>",
    ))
    fig_proj.update_layout(
        **plotly_base(300, {"ticksuffix":" €","tickformat":",.0f"}),
        yaxis2=dict(overlaying="y", side="right", tickformat=",.0f",
                    ticksuffix=" €", gridcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_proj, use_container_width=True)

    # ── Tableau par position ───────────────────────────────────────────────────
    section_label("Dividendes par position")
    rows_div = ""
    for tk, info_d in sorted(div_par_ticker.items(),
                              key=lambda x: x[1].get("yield",0), reverse=True):
        dy     = info_d.get("yield", 0) * 100
        rev_a  = info_d["val"] * info_d.get("yield", 0)
        rev_m  = rev_a / 12
        dy_c   = "#22c55e" if dy > 3 else ("#f59e0b" if dy > 1 else "#475569")
        # divs contient les dividendes PAR ACTION → total reçu = sum * qty
        recus  = float(info_d["divs"].sum()) * info_d["qty"] if not info_d["divs"].empty else 0
        de     = info_d.get("date_entree")
        de_str = de.strftime("%d/%m/%Y") if de else "—"
        rows_div += (
            f'<tr>'
            f'<td style="text-align:left">{info_d["titre"][:22]}'
            f'<span class="tbadge">{tk}</span></td>'
            f'<td style="font-family:DM Mono,monospace;font-size:0.65rem;color:var(--t3)">{de_str}</td>'
            f'<td>{info_d["qty"]:.0f}</td>'
            f'<td>{info_d["val"]:,.0f} €</td>'
            f'<td><span style="font-family:DM Mono,monospace;font-size:0.75rem;'
            f'font-weight:600;color:{dy_c}">{dy:.2f}%</span></td>'
            f'<td class="{"pos" if recus>0 else "n"}">{recus:,.2f} €</td>'
            f'<td class="pos">{rev_a:,.0f} €/an</td>'
            f'<td>{rev_m:,.0f} €/mois</td>'
            f'</tr>'
        )
    st.markdown(
        f'<div style="background:var(--s1);border:1px solid var(--border);'
        f'border-radius:11px;overflow:hidden">'
        f'<table class="ptable"><thead><tr>'
        f'<th style="text-align:left">Titre</th>'
        f'<th style="text-align:left">Achat</th>'
        f'<th>Qté</th><th>Valeur</th><th>Yield</th>'
        f'<th>Reçus réels</th><th>Projeté/an</th><th>Projeté/mois</th>'
        f'</tr></thead><tbody>{rows_div}</tbody></table></div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE — TRI PAR POSITION
# ══════════════════════════════════════════════════════════════════════════════

def compute_tri(cash_flows: list) -> float:
    """
    Newton-Raphson pour calculer le TRI annualisé.
    cash_flows = liste de (date, montant) — négatif = sortie, positif = entrée.
    """
    if len(cash_flows) < 2:
        return None
    try:
        dates  = [cf[0] for cf in cash_flows]
        t0     = dates[0]
        t_days = [(d - t0).days for d in dates]
        amounts = [cf[1] for cf in cash_flows]

        def npv(r):
            return sum(amt / (1 + r) ** (t / 365.25)
                       for amt, t in zip(amounts, t_days))

        def npv_prime(r):
            return sum(-amt * (t / 365.25) / (1 + r) ** (t / 365.25 + 1)
                       for amt, t in zip(amounts, t_days))

        r = 0.1
        for _ in range(100):
            f  = npv(r)
            fp = npv_prime(r)
            if abs(fp) < 1e-12: break
            r_new = r - f / fp
            if abs(r_new - r) < 1e-8: break
            r = r_new
            if r <= -0.999: return None
        return r if -1 < r < 100 else None
    except:
        return None


def page_tri():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">📐 Performance réelle</div>'
                '<div class="ph-title">TRI par Position</div>'
                '<div class="ph-sub">Taux de Rentabilité Interne · Performance ajustée au temps</div>'
                '</div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="background:rgba(59,130,246,0.07);border:1px solid rgba(59,130,246,0.2);'
        'border-radius:10px;padding:12px 16px;margin-bottom:1.4rem;font-family:DM Mono,monospace;'
        'font-size:0.65rem;color:#3b82f6">ℹ Le TRI intègre les dates d\'achat et de vente réelles. '
        '20% sur 5 ans = ~3.7%/an. 20% sur 6 mois = ~46%/an. '
        'C\'est la vraie mesure d\'un investisseur.</div>',
        unsafe_allow_html=True
    )

    try:
        df_hist, df_corr, df_vers = load_data()
        _, s = compute_portfolio(df_hist, df_corr, df_vers)
    except Exception as e:
        st.error(f"Fichiers introuvables : {e}"); return

    corr_d = dict(zip(df_corr["Libelle_fortuneo"], df_corr["code_yfinance"]))

    # Groupe les opérations par libellé
    def op_order(row):
        op = str(row["Opération"]).strip().lower()
        return 0 if "achat" in op else (1 if "taxe" in op else 2)
    df_s = df_hist.copy()
    df_s["_ord"] = df_s.apply(op_order, axis=1)
    df_s = df_s.sort_values(["Date","_ord"])

    ops_by_lib = {}
    for _, row in df_s.iterrows():
        lib = str(row["libellé"]).strip()
        op  = str(row["Opération"]).strip().lower()
        qty = float(row["Qté"]) if pd.notna(row["Qté"]) else 0
        net = float(row["Montant net"]) if pd.notna(row["Montant net"]) else 0
        dt  = row["Date"]
        ops_by_lib.setdefault(lib, [])
        if "achat" in op and qty > 0:
            ops_by_lib[lib].append(("buy",  dt, -abs(net), qty))
        elif "vente" in op and qty > 0:
            ops_by_lib[lib].append(("sell", dt, +abs(net), qty))
        elif "taxe" in op:
            ops_by_lib[lib].append(("tax",  dt, -abs(net), 0))

    with st.spinner("Calcul des TRI…"):
        tri_results = []
        for lib, ops in ops_by_lib.items():
            tk = corr_d.get(lib)
            if not tk: continue

            # Cash flows: achats = négatif, ventes = positif
            cfs = [(op[1], op[2]) for op in ops if op[0] in ("buy","sell","tax")]
            if not cfs: continue

            # Valeur actuelle des titres encore détenus
            qty_held = sum(op[3] if op[0]=="buy" else -op[3]
                           for op in ops if op[0] in ("buy","sell"))
            qty_held = max(0.0, qty_held)

            if qty_held > 0.001:
                cur_px = get_current_price(tk)
                if cur_px:
                    cfs.append((datetime.today(), cur_px * qty_held))

            if len(cfs) < 2: continue

            tri = compute_tri(cfs)
            if tri is None: continue

            # Durée de détention
            dt_first = min(cf[0] for cf in cfs)
            dt_last  = max(cf[0] for cf in cfs)
            duree_j  = (dt_last - dt_first).days if hasattr(dt_last - dt_first, "days") else 0

            total_investi = sum(abs(cf[1]) for cf in cfs if cf[1] < 0)
            total_retour  = sum(cf[1] for cf in cfs if cf[1] > 0)
            pnl           = total_retour - total_investi

            tri_results.append({
                "Titre":     lib[:28],
                "Ticker":    tk,
                "TRI/an":    tri * 100,
                "Durée":     duree_j,
                "Investi":   total_investi,
                "Retour":    total_retour,
                "PnL":       pnl,
                "En cours":  qty_held > 0.001,
            })

    if not tri_results:
        st.info("Données d'historique insuffisantes pour calculer les TRI.")
        return

    tri_results.sort(key=lambda x: x["TRI/an"], reverse=True)

    # KPIs globaux
    tris = [r["TRI/an"] for r in tri_results]
    tri_moy = sum(tris) / len(tris) if tris else 0
    tri_max = max(tris) if tris else 0
    tri_min = min(tris) if tris else 0
    n_pos   = sum(1 for t in tris if t > 0)

    kpi_tri = (
        f'<div class="kpi-row" style="grid-template-columns:repeat(4,1fr)">'
        + kpi_card("TRI moyen pondéré", f"{tri_moy:+.1f}%/an",
                   f"{n_pos}/{len(tris)} positions positives",
                   tri_moy > 0,
                   top_color=f"linear-gradient(90deg,{'#22c55e' if tri_moy>0 else '#ef4444'},transparent)")
        + kpi_card("Meilleure position", f"{tri_max:+.1f}%/an",
                   tri_results[0]["Ticker"] if tri_results else "—",
                   True,
                   top_color="linear-gradient(90deg,#22c55e,transparent)")
        + kpi_card("Moins bonne position", f"{tri_min:+.1f}%/an",
                   tri_results[-1]["Ticker"] if tri_results else "—",
                   False,
                   top_color="linear-gradient(90deg,#ef4444,transparent)")
        + kpi_card("Positions analysées", str(len(tri_results)),
                   top_color="linear-gradient(90deg,#3b82f6,transparent)")
        + '</div>'
    )
    st.markdown(kpi_tri, unsafe_allow_html=True)

    # Graphique TRI en barres horizontales
    section_label("TRI annualisé par position")
    tri_sorted = sorted(tri_results, key=lambda x: x["TRI/an"])
    fig_tri = go.Figure(go.Bar(
        x=[r["TRI/an"] for r in tri_sorted],
        y=[f'{r["Ticker"]}' for r in tri_sorted],
        orientation="h",
        marker_color=["#22c55e" if r["TRI/an"] >= 0 else "#ef4444" for r in tri_sorted],
        marker_opacity=0.85,
        text=[f'{r["TRI/an"]:+.1f}%' for r in tri_sorted],
        textposition="outside",
        textfont=dict(family="DM Mono", size=9),
        hovertemplate="<b>%{y}</b><br>TRI : %{x:+.1f}%/an<extra></extra>",
    ))
    fig_tri.add_vline(x=0, line_color="#2d3f57", line_width=1)
    fig_tri.update_layout(**plotly_base(max(280, len(tri_results) * 30),
                                        {"ticksuffix": "%"}))
    fig_tri.update_layout(xaxis=dict(ticksuffix="%", gridcolor="#1a2538"))
    st.plotly_chart(fig_tri, use_container_width=True)

    # Tableau détaillé
    section_label("Détail par position")
    rows_tri = ""
    for r in tri_results:
        tc   = "#22c55e" if r["TRI/an"] >= 0 else "#ef4444"
        pc   = "#22c55e" if r["PnL"] >= 0 else "#ef4444"
        dur  = f"{r['Durée']//365}a {(r['Durée']%365)//30}m" if r["Durée"] > 0 else "—"
        stat = '<span style="color:#22c55e;font-size:0.65rem">● En cours</span>' \
               if r["En cours"] else \
               '<span style="color:#475569;font-size:0.65rem">○ Clôturée</span>'
        rows_tri += (
            f'<tr>'
            f'<td style="text-align:left">{r["Titre"]}'
            f'<span class="tbadge">{r["Ticker"]}</span></td>'
            f'<td><span style="font-family:DM Mono,monospace;font-size:0.8rem;'
            f'font-weight:700;color:{tc}">{r["TRI/an"]:+.1f}%/an</span></td>'
            f'<td>{dur}</td>'
            f'<td>{r["Investi"]:,.0f} €</td>'
            f'<td class="{"pos" if r["PnL"]>=0 else "neg"}">{r["PnL"]:+,.0f} €</td>'
            f'<td>{stat}</td>'
            f'</tr>'
        )
    st.markdown(
        f'<div style="background:var(--s1);border:1px solid var(--border);'
        f'border-radius:11px;overflow:hidden">'
        f'<table class="ptable"><thead><tr>'
        f'<th style="text-align:left">Position</th>'
        f'<th>TRI annualisé</th><th>Durée détention</th>'
        f'<th>Capital investi</th><th>PnL réalisé+latent</th><th>Statut</th>'
        f'</tr></thead><tbody>{rows_tri}</tbody></table></div>',
        unsafe_allow_html=True
    )



# ══════════════════════════════════════════════════════════════════════════════
# PAGE — WATCHLIST
# ══════════════════════════════════════════════════════════════════════════════

def page_watchlist():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">👁 Surveillance</div>'
                '<div class="ph-title">Watchlist</div>'
                '<div class="ph-sub">Cibles à surveiller · Score 10-Baggers · Alertes prix</div>'
                '</div>', unsafe_allow_html=True)

    watchlist = get_state("watchlist", [])

    with st.expander("➕  Ajouter à la watchlist", expanded=len(watchlist) == 0):
        wa, wb, wc, wd = st.columns([2, 1, 1, 1])
        with wa:
            w_ticker = st.text_input("Ticker", placeholder="ASML.AS", key="wl_tk").upper()
        with wb:
            w_target = st.number_input("Prix cible (€)", value=0.0, min_value=0.0,
                                        step=0.5, format="%.2f", key="wl_target")
        with wc:
            w_stop   = st.number_input("Stop-loss (€)", value=0.0, min_value=0.0,
                                        step=0.5, format="%.2f", key="wl_stop")
        with wd:
            w_note   = st.text_input("Note courte", placeholder="Pourquoi ?", key="wl_note")
        if st.button("Ajouter à la watchlist", key="wl_add"):
            if w_ticker:
                watchlist.append({
                    "ticker": w_ticker, "target": w_target, "stop": w_stop,
                    "note": w_note, "added": datetime.now().strftime("%d/%m/%Y")
                })
                set_state("watchlist", watchlist)
                st.rerun()

    if not watchlist:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">👁</div>
          <div class="empty-title">Watchlist vide</div>
          <div class="empty-sub">Ajoutez les tickers que vous surveillez avant d'acheter.</div>
        </div>""", unsafe_allow_html=True)
        return

    section_label(f"Surveillance · {len(watchlist)} titres")

    with st.spinner("Analyse des titres en watchlist…"):
        wl_data = []
        for item in watchlist:
            tk   = item["ticker"]
            sig  = get_ticker_signals(tk)
            sc_d = compute_10bagger_data(tk)
            px   = sig["last"] if sig else None
            wl_data.append({**item, "sig": sig, "sc_d": sc_d, "px": px})

    SIG_C = {"g":"#22c55e","r":"#ef4444","y":"#f59e0b","n":"#475569"}

    for i, item in enumerate(wl_data):
        sig  = item["sig"]
        sc_d = item["sc_d"]
        px   = item["px"]
        tk   = item["ticker"]

        at_target  = px and item["target"] > 0 and px >= item["target"]
        at_stop    = px and item["stop"]   > 0 and px <= item["stop"]
        border_c   = "#22c55e" if at_target else ("#ef4444" if at_stop else "var(--border)")

        score_val = sc_d["Score"] if sc_d else None
        sc_c = "#22c55e" if (score_val or 0) >= 70 else ("#f59e0b" if (score_val or 0) >= 50 else "#ef4444")
        top_sig_label = sig["signals"][0][0] if sig and sig["signals"] else "—"
        top_sig_cls   = sig["signals"][0][1] if sig and sig["signals"] else "n"

        st.markdown(
            f'<div style="background:var(--s1);border:1px solid {border_c};'
            f'border-radius:11px;padding:16px 20px;margin-bottom:10px">'
            f'<div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">'
            f'<div style="min-width:80px"><div style="font-family:DM Mono,monospace;font-size:0.82rem;'
            f'color:#22c55e;font-weight:600">{tk}</div>'
            f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:var(--t3);margin-top:2px">'
            f'{item["added"]}</div></div>'
            f'<div style="min-width:90px"><div style="font-family:DM Mono,monospace;font-size:0.55rem;'
            f'color:var(--t3);text-transform:uppercase;letter-spacing:0.1em">Prix actuel</div>'
            f'<div style="font-family:Outfit,sans-serif;font-size:1.1rem;font-weight:700;color:var(--text)">'
            f'{f"{px:.2f} €" if px else "—"}</div></div>'
            + (f'<div style="min-width:90px"><div style="font-family:DM Mono,monospace;font-size:0.55rem;'
               f'color:var(--t3);text-transform:uppercase;letter-spacing:0.1em">Cible</div>'
               f'<div style="font-family:Outfit,sans-serif;font-size:1rem;font-weight:600;'
               f'color:{"#22c55e" if at_target else "var(--t2)"}">'
               f'{item["target"]:.2f} €{"  ✓" if at_target else ""}</div></div>'
               if item["target"] > 0 else "")
            + (f'<div style="min-width:90px"><div style="font-family:DM Mono,monospace;font-size:0.55rem;'
               f'color:var(--t3);text-transform:uppercase;letter-spacing:0.1em">Stop-loss</div>'
               f'<div style="font-family:Outfit,sans-serif;font-size:1rem;font-weight:600;'
               f'color:{"#ef4444" if at_stop else "var(--t2)"}">'
               f'{item["stop"]:.2f} €{"  ✗" if at_stop else ""}</div></div>'
               if item["stop"] > 0 else "")
            + f'<div style="min-width:70px"><div style="font-family:DM Mono,monospace;font-size:0.55rem;'
            f'color:var(--t3);text-transform:uppercase;letter-spacing:0.1em">Score</div>'
            f'<div style="font-family:Outfit,sans-serif;font-size:1rem;font-weight:700;color:{sc_c}">'
            f'{score_val if score_val is not None else "—"}</div></div>'
            f'<div style="flex:1;min-width:120px"><div style="font-family:DM Mono,monospace;font-size:0.55rem;'
            f'color:var(--t3);text-transform:uppercase;letter-spacing:0.1em">Signal</div>'
            f'<div style="font-family:DM Mono,monospace;font-size:0.68rem;font-weight:600;'
            f'color:{SIG_C[top_sig_cls]}">{top_sig_label}</div></div>'
            + (f'<div style="font-family:Outfit,sans-serif;font-size:0.78rem;color:var(--t3);'
               f'font-style:italic;flex:1">{item["note"]}</div>' if item.get("note") else "")
            + f'</div></div>',
            unsafe_allow_html=True
        )
        col_del, _ = st.columns([1, 6])
        with col_del:
            if st.button("🗑 Retirer", key=f"wl_del_{i}"):
                watchlist.pop(i)
                set_state("watchlist", watchlist)
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE — COMPARAISON PAIR-À-PAIR
# ══════════════════════════════════════════════════════════════════════════════

def page_comparaison():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">⚖ Analyse comparative</div>'
                '<div class="ph-title">Comparaison</div>'
                '<div class="ph-sub">Pair-à-pair · Fondamentaux · Performance · 10-Baggers</div>'
                '</div>', unsafe_allow_html=True)

    # ── Saisie des tickers ────────────────────────────────────────────────────
    try:
        df_hist, df_corr, df_vers = load_data()
        df_pos, _ = compute_portfolio(df_hist, df_corr, df_vers)
        port_suggestions = [r["Ticker"] for _, r in df_pos.iterrows()
                            if r["Ticker"] != "N/A"]
    except:
        port_suggestions = []

    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:var(--t3);'
                'margin-bottom:1rem">Entrez 2 à 5 tickers à comparer côte à côte.</div>',
                unsafe_allow_html=True)

    comp_input = st.text_input("Tickers à comparer (séparés par virgules)",
                                placeholder="AIR.PA, SAF.PA, MTU.DE, HO.PA",
                                key="comp_tickers",
                                value=", ".join(port_suggestions[:3]) if port_suggestions else "")
    run_comp = st.button("▶  Comparer", type="primary", key="comp_run")

    if "comp_results" not in st.session_state:
        st.session_state.comp_results = []

    if run_comp and comp_input:
        tks = [t.strip().upper() for t in comp_input.replace(",", " ").split() if t.strip()][:5]
        with st.spinner("Analyse comparative…"):
            comp_data = []
            prog = st.progress(0)
            for i, tk in enumerate(tks):
                prog.progress(int((i+1)/len(tks)*100), f"Analyse {tk}…")
                d = compute_10bagger_data(tk)
                sig = get_ticker_signals(tk)
                if d:
                    d["sig"] = sig
                    comp_data.append(d)
            st.session_state.comp_results = comp_data

    comp_data = st.session_state.comp_results
    if not comp_data:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">⚖</div>
          <div class="empty-title">Entrez des tickers et lancez la comparaison</div>
          <div class="empty-sub">2 à 5 tickers · Toutes métriques côte à côte.</div>
        </div>""", unsafe_allow_html=True)
        return

    n = len(comp_data)
    COMP_C = ["#22c55e","#3b82f6","#f59e0b","#8b5cf6","#ef4444"]

    # ── Score overview ─────────────────────────────────────────────────────────
    section_label("Vue d'ensemble")
    kpi_comp = f'<div class="kpi-row" style="grid-template-columns:repeat({n},1fr)">'
    for i, d in enumerate(comp_data):
        c   = COMP_C[i % len(COMP_C)]
        sc  = d["Score"]
        sc_c = "#22c55e" if sc>=70 else ("#f59e0b" if sc>=50 else "#ef4444")
        circ = 2*3.14159*22
        dash = circ * sc / 100
        kpi_comp += (
            f'<div style="background:var(--s1);border:1px solid {c}33;border-radius:13px;'
            f'padding:20px 16px;text-align:center;position:relative;overflow:hidden">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:2px;background:{c}"></div>'
            f'<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:{c};'
            f'font-weight:600;margin-bottom:6px">{d["Ticker"]}</div>'
            f'<svg width="60" height="60" viewBox="0 0 60 60" style="transform:rotate(-90deg)">'
            f'<circle cx="30" cy="30" r="22" fill="none" stroke="#1a2538" stroke-width="5"/>'
            f'<circle cx="30" cy="30" r="22" fill="none" stroke="{sc_c}" stroke-width="5"'
            f' stroke-linecap="round"'
            f' stroke-dasharray="{dash:.1f} {circ-dash:.1f}"/></svg>'
            f'<div style="font-family:Outfit,sans-serif;font-size:1.4rem;font-weight:900;'
            f'color:{sc_c};margin-top:-44px;margin-bottom:32px">{sc}</div>'
            f'<div style="font-family:Outfit,sans-serif;font-size:0.75rem;color:var(--t2);'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{d["Nom"][:20]}</div>'
            f'<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:{c};'
            f'margin-top:4px">{d["Cours"]:.2f} €' if d["Cours"] else "—"
            + f'</div></div>'
        )
    kpi_comp += '</div>'
    st.markdown(kpi_comp, unsafe_allow_html=True)

    # ── Tableau comparatif des 10 critères ─────────────────────────────────────
    section_label("Comparaison des 10 critères 10-Baggers")

    CRIT_KEYS = ["CA CAGR","Rachat","ROIC","Marge FCF","Div CAGR",
                 "Payout","FCF CAGR","D/EBITDA","PER","Momentum"]
    STATUS_COLOR2 = {"g":"#22c55e","r":"#ef4444","y":"#f59e0b","n":"#475569"}
    STATUS_ICON2  = {"g":"✓","r":"✗","y":"◐","n":"○"}

    header = '<tr><th style="text-align:left">Critère</th>' + \
             "".join(f'<th style="color:{COMP_C[i%len(COMP_C)]}">{d["Ticker"]}</th>'
                     for i, d in enumerate(comp_data)) + '</tr>'
    rows_cmp = ""
    for ci, crit in enumerate(CRIT_KEYS):
        val_key = [  "CA CAGR","Rachat","ROIC","Marge FCF","Div CAGR",
                     "Payout","FCF CAGR","D/EBITDA","PER","Momentum"][ci]
        row = f'<tr><td style="text-align:left;font-family:DM Mono,monospace;font-size:0.68rem;color:var(--t2)">{crit}</td>'
        for i, d in enumerate(comp_data):
            st_c = d["_st"][ci]
            val  = d.get(val_key, "—")
            row += (f'<td><span style="font-family:DM Mono,monospace;font-size:0.7rem;'
                    f'font-weight:600;color:{STATUS_COLOR2[st_c]}">'
                    f'{STATUS_ICON2[st_c]} {val}</span></td>')
        row += '</tr>'
        rows_cmp += row

    st.markdown(
        f'<div style="background:var(--s1);border:1px solid var(--border);'
        f'border-radius:11px;overflow:hidden">'
        f'<table class="ptable"><thead>{header}</thead>'
        f'<tbody>{rows_cmp}</tbody></table></div>',
        unsafe_allow_html=True
    )

    # ── Radar chart ─────────────────────────────────────────────────────────────
    section_label("Radar des scores pondérés")
    categories = ["CA CAGR","Rachat","ROIC","Marge FCF","Div CAGR",
                  "Payout","FCF CAGR","D/EBITDA","PER","Momentum"]
    WEIGHTS_LIST = [15, 8, 15, 12, 6, 5, 12, 10, 7, 10]

    def hex_to_rgba(hex_color, alpha=0.13):
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return f"rgba({r},{g},{b},{alpha})"

    fig_radar = go.Figure()
    for i, d in enumerate(comp_data):
        vals = []
        for ci, (cat, w) in enumerate(zip(categories, WEIGHTS_LIST)):
            st_c = d["_st"][ci]
            score_v = w if st_c=="g" else (w*0.5 if st_c=="y" else 0)
            vals.append(score_v)
        vals_closed = vals + [vals[0]]
        cats_closed = categories + [categories[0]]
        c = COMP_C[i%len(COMP_C)]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed, theta=cats_closed,
            fill="toself", name=d["Ticker"],
            line=dict(color=c, width=2),
            fillcolor=hex_to_rgba(c, 0.13),
        ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(14,20,32,0.8)",
            radialaxis=dict(visible=True, range=[0, 15],
                            gridcolor="#1a2538", linecolor="#1a2538",
                            tickfont=dict(family="DM Mono", size=7, color="#475569")),
            angularaxis=dict(gridcolor="#1a2538", linecolor="#1a2538",
                             tickfont=dict(family="DM Mono", size=8, color="#94a3b8")),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Mono", size=9, color="#475569"),
        height=400,
        legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center",
                    font=dict(family="DM Mono", size=9)),
        margin=dict(l=40, r=40, t=20, b=40),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # ── Perf historique comparée ────────────────────────────────────────────────
    section_label("Performance historique comparée · Base 100")
    perf_period = st.radio("Période", ["1 an","3 ans","5 ans"], horizontal=True, key="comp_perf")
    perf_map = {"1 an":"1y","3 ans":"3y","5 ans":"5y"}

    with st.spinner("Chargement des historiques…"):
        df_comp_h = get_multi_history(
            tuple(d["Ticker"] for d in comp_data),
            perf_map[perf_period]
        )

    # Add benchmark
    bench_name = get_state("benchmark", "MSCI World (IWDA)")
    bench_sym  = BENCHMARKS_AVAILABLE.get(bench_name, "IWDA.AS")
    try:
        bh = yf.Ticker(bench_sym).history(period=perf_map[perf_period])["Close"]
        bh.index = bh.index.tz_localize(None)
        df_comp_h[bench_name] = bh
    except: pass

    if not df_comp_h.empty:
        df_norm = df_comp_h.apply(lambda col: col / col.dropna().iloc[0] * 100 if not col.dropna().empty else col)
        fig_ch = go.Figure()
        for i, col in enumerate(df_norm.columns):
            is_bench = col == bench_name
            fig_ch.add_trace(go.Scatter(
                x=df_norm.index, y=df_norm[col], name=col,
                line=dict(
                    color=COMP_C[i%len(COMP_C)] if not is_bench else "#475569",
                    width=2.5 if not is_bench else 1.5,
                    dash="solid" if not is_bench else "dash",
                ),
                hovertemplate=f"<b>{col}</b> %{{x|%d %b %Y}}<br>%{{y:.1f}}<extra></extra>",
            ))
        fig_ch.add_hline(y=100, line_color="#2d3f57", line_width=1, line_dash="dot")
        fig_ch.update_layout(**plotly_base(320, {"tickformat":".0f"}))
        st.plotly_chart(fig_ch, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE — PARAMÈTRES
# ══════════════════════════════════════════════════════════════════════════════

def page_parametres():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">⚙ Configuration</div>'
                '<div class="ph-title">Paramètres</div>'
                '<div class="ph-sub">Benchmark · Persistance · Données</div>'
                '</div>', unsafe_allow_html=True)

    # ── Benchmark ─────────────────────────────────────────────────────────────
    section_label("Benchmark de référence")
    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:var(--t3);'
                'margin-bottom:1rem">Utilisé dans les comparaisons de performance, '
                'la page Intelligence et les graphiques momentum.</div>', unsafe_allow_html=True)

    current_bench = get_state("benchmark", "MSCI World (IWDA)")
    bench_options = list(BENCHMARKS_AVAILABLE.keys())
    new_bench = st.selectbox("Benchmark principal", bench_options,
                             index=bench_options.index(current_bench) if current_bench in bench_options else 0,
                             key="param_bench")
    if new_bench != current_bench:
        set_state("benchmark", new_bench)
        st.success(f"✓ Benchmark mis à jour : {new_bench}")

    # ── État de la persistance ─────────────────────────────────────────────────
    section_label("Données persistantes")
    journal   = get_state("journal",   [])
    alerts    = get_state("alerts",    [])
    watchlist = get_state("watchlist", [])

    state_html = (
        f'<div class="kpi-row" style="grid-template-columns:repeat(3,1fr)">'
        + kpi_card("Journal", f"{len(journal)} entrées",
                   top_color="linear-gradient(90deg,#22c55e,transparent)")
        + kpi_card("Alertes", f"{len(alerts)} actives",
                   top_color="linear-gradient(90deg,#f59e0b,transparent)")
        + kpi_card("Watchlist", f"{len(watchlist)} titres",
                   top_color="linear-gradient(90deg,#3b82f6,transparent)")
        + '</div>'
    )
    st.markdown(state_html, unsafe_allow_html=True)

    st.markdown(f'<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:var(--t3);'
                f'margin-top:0.5rem">Fichier de persistance : '
                f'<code style="color:#22c55e">{os.path.abspath(STATE_FILE)}</code></div>',
                unsafe_allow_html=True)

    # Export / Reset
    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        state_export = _load_state()
        st.download_button(
            "⬇  Exporter state.json",
            data=json.dumps(state_export, ensure_ascii=False, indent=2, default=str),
            file_name="pea_state.json", mime="application/json",
        )
    with ec2:
        if st.button("🗑  Vider le journal", key="p_clr_journal"):
            set_state("journal", [])
            st.rerun()
    with ec3:
        if st.button("🗑  Tout réinitialiser", key="p_reset_all"):
            _save_state({"journal":[],"alerts":[],"watchlist":[],"benchmark":"MSCI World (IWDA)"})
            for k in list(st.session_state.keys()):
                if k.startswith("_pstate_"): del st.session_state[k]
            st.success("État réinitialisé.")
            st.rerun()

    # ── Cache ─────────────────────────────────────────────────────────────────
    section_label("Cache & données")
    if st.button("⟳  Vider tout le cache yfinance", type="primary", key="p_cache"):
        st.cache_data.clear()
        st.success("✓ Cache vidé.")



# ══════════════════════════════════════════════════════════════════════════════
# PAGE — CALENDRIER DES ÉVÉNEMENTS
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600)
def get_calendar_data(ticker: str):
    """
    Récupère toutes les données calendrier disponibles pour un ticker.
    Retourne un dict avec les événements trouvés.
    """
    try:
        t    = yf.Ticker(ticker)
        info = t.info or {}
        events = []

        from datetime import timezone

        def ts_to_date(ts):
            """Convertit un timestamp unix en date lisible."""
            try:
                if ts and ts > 0:
                    return datetime.fromtimestamp(int(ts)).date()
            except:
                pass
            return None

        # ── Résultats financiers (Earnings) ───────────────────────────────────
        # Méthode 1 : earningsTimestamp (date précise)
        et = info.get("earningsTimestamp")
        if et:
            d = ts_to_date(et)
            if d and d >= datetime.today().date():
                events.append({
                    "type":    "Résultats",
                    "icon":    "📊",
                    "color":   "#3b82f6",
                    "date":    d,
                    "label":   "Publication résultats",
                    "detail":  f"EPS estimé : {info.get('epsForward', '—')}",
                    "ticker":  ticker,
                    "futur":   True,
                })

        # Méthode 2 : earningsTimestampStart / End (fourchette)
        ets = info.get("earningsTimestampStart")
        ete = info.get("earningsTimestampEnd")
        if ets and not et:
            ds = ts_to_date(ets)
            de = ts_to_date(ete) if ete else ds
            if ds and ds >= datetime.today().date():
                lbl = f"Entre {ds.strftime('%d/%m')} et {de.strftime('%d/%m')}" if de and de != ds else ds.strftime('%d/%m/%Y')
                events.append({
                    "type":    "Résultats",
                    "icon":    "📊",
                    "color":   "#3b82f6",
                    "date":    ds,
                    "label":   "Fourchette résultats",
                    "detail":  lbl,
                    "ticker":  ticker,
                    "futur":   True,
                })

        # Méthode 3 : t.calendar dict
        try:
            cal = t.calendar
            if isinstance(cal, dict):
                ed = cal.get("Earnings Date")
                if ed:
                    # Peut être une liste ou une valeur unique
                    dates_list = ed if isinstance(ed, list) else [ed]
                    for d_raw in dates_list:
                        try:
                            d_parsed = pd.Timestamp(d_raw).date()
                            if d_parsed >= datetime.today().date():
                                events.append({
                                    "type":   "Résultats",
                                    "icon":   "📊",
                                    "color":  "#3b82f6",
                                    "date":   d_parsed,
                                    "label":  "Publication résultats (calendar)",
                                    "detail": f"EPS moy. estimé : {cal.get('Earnings Average','—')}",
                                    "ticker": ticker,
                                    "futur":  True,
                                })
                        except:
                            pass
        except:
            pass

        # Méthode 4 : earnings_dates DataFrame
        try:
            ed_df = t.earnings_dates
            if ed_df is not None and not ed_df.empty:
                ed_df.index = pd.to_datetime(ed_df.index)
                if ed_df.index.tz is not None:
                    ed_df.index = ed_df.index.tz_localize(None)
                future_ed = ed_df[ed_df.index.date >= datetime.today().date()]  # type: ignore
                for dt_idx, row in future_ed.head(4).iterrows():
                    eps_est = row.get("EPS Estimate", None)
                    events.append({
                        "type":   "Résultats",
                        "icon":   "📊",
                        "color":  "#3b82f6",
                        "date":   dt_idx.date(),
                        "label":  "Résultats trimestriels",
                        "detail": f"EPS estimé : {eps_est:.2f}" if eps_est and str(eps_est) != 'nan' else "EPS estimé : —",
                        "ticker": ticker,
                        "futur":  True,
                    })
        except:
            pass

        # ── Ex-Dividende ──────────────────────────────────────────────────────
        exdiv = info.get("exDividendDate")
        if exdiv:
            d = ts_to_date(exdiv)
            if d:
                futur = d >= datetime.today().date()
                div_amt = info.get("lastDividendValue") or info.get("dividendRate", 0) or 0
                if div_amt > 100: div_amt = div_amt / 100  # yfinance parfois × 100
                events.append({
                    "type":   "Ex-Dividende",
                    "icon":   "💸",
                    "color":  "#22c55e",
                    "date":   d,
                    "label":  "Date ex-dividende",
                    "detail": f"Montant : {div_amt:.2f} €/action" if div_amt else "Montant : —",
                    "ticker": ticker,
                    "futur":  futur,
                })

        # ── Date de paiement dividende ────────────────────────────────────────
        divdate = info.get("dividendDate")
        if divdate:
            d = ts_to_date(divdate)
            if d:
                futur = d >= datetime.today().date()
                events.append({
                    "type":   "Paiement Div.",
                    "icon":   "💰",
                    "color":  "#22c55e",
                    "date":   d,
                    "label":  "Paiement dividende",
                    "detail": f"Versement effectif sur le compte",
                    "ticker": ticker,
                    "futur":  futur,
                })

        # ── Fin exercice fiscal ───────────────────────────────────────────────
        fy = info.get("nextFiscalYearEnd")
        if fy:
            d = ts_to_date(fy)
            if d and d >= datetime.today().date():
                events.append({
                    "type":   "Fin exercice",
                    "icon":   "📋",
                    "color":  "#8b5cf6",
                    "date":   d,
                    "label":  "Fin d'exercice fiscal",
                    "detail": "Clôture de l'année comptable",
                    "ticker": ticker,
                    "futur":  True,
                })

        return events
    except:
        return []


def page_calendrier():
    st.markdown('<div class="ph">'
                '<div class="ph-eyebrow">📅 Agenda financier</div>'
                '<div class="ph-title">Calendrier</div>'
                '<div class="ph-sub">Résultats · Ex-dividendes · Paiements · Exercices fiscaux</div>'
                '</div>', unsafe_allow_html=True)

    # ── Chargement du portefeuille ────────────────────────────────────────────
    try:
        df_hist, df_corr, df_vers = load_data()
        df_pos, _ = compute_portfolio(df_hist, df_corr, df_vers)
    except Exception as e:
        st.error(f"Fichiers introuvables : {e}"); return

    port_tickers_cal = [r["Ticker"] for _, r in df_pos.iterrows()
                        if r["Ticker"] and r["Ticker"] != "N/A"]

    # Tickers supplémentaires
    extra_cal = st.text_input("Ajouter des tickers (optionnel)",
                               placeholder="ASML.AS, MSFT, AAPL…",
                               key="cal_extra", label_visibility="visible")
    extra_tks_cal = [t.strip().upper() for t in extra_cal.replace(",", " ").split() if t.strip()]
    all_cal_tks   = list(dict.fromkeys(port_tickers_cal + extra_tks_cal))

    # Filtre type
    type_filter = st.multiselect(
        "Types d'événements",
        ["Résultats", "Ex-Dividende", "Paiement Div.", "Fin exercice"],
        default=["Résultats", "Ex-Dividende", "Paiement Div.", "Fin exercice"],
        key="cal_types"
    )

    # Vue passé/futur
    show_past = st.toggle("Afficher aussi les événements passés", value=False, key="cal_past")

    # ── Récupération ──────────────────────────────────────────────────────────
    all_events = []
    with st.spinner("Récupération du calendrier…"):
        prog = st.progress(0)
        for i, tk in enumerate(all_cal_tks):
            prog.progress(int((i+1)/len(all_cal_tks)*100), f"Calendrier {tk}…")
            evts = get_calendar_data(tk)
            all_events.extend(evts)
        prog.empty()

    # Filtre type et futur/passé
    all_events = [e for e in all_events if e["type"] in type_filter]
    if not show_past:
        all_events = [e for e in all_events if e["futur"]]

    # Déduplique par (ticker, type, date)
    seen = set()
    deduped = []
    for e in all_events:
        key = (e["ticker"], e["type"], str(e["date"]))
        if key not in seen:
            seen.add(key)
            deduped.append(e)
    all_events = sorted(deduped, key=lambda x: x["date"])

    # ── KPIs ──────────────────────────────────────────────────────────────────
    today = datetime.today().date()
    n_res = sum(1 for e in all_events if e["type"] == "Résultats" and e["futur"])
    n_div = sum(1 for e in all_events if e["type"] == "Ex-Dividende" and e["futur"])
    next_evt = all_events[0] if all_events else None
    n_30j   = sum(1 for e in all_events if e["futur"] and (e["date"] - today).days <= 30)

    kpi_cal = (
        f'<div class="kpi-row" style="grid-template-columns:repeat(4,1fr)">'
        + kpi_card("Événements à venir", str(len([e for e in all_events if e["futur"]])),
                   top_color="linear-gradient(90deg,#3b82f6,transparent)")
        + kpi_card("Résultats à venir", str(n_res),
                   top_color="linear-gradient(90deg,#3b82f6,transparent)")
        + kpi_card("Ex-dividendes à venir", str(n_div),
                   top_color="linear-gradient(90deg,#22c55e,transparent)")
        + kpi_card("Dans les 30 prochains jours", str(n_30j),
                   top_color=f"linear-gradient(90deg,{'#f59e0b' if n_30j>0 else '#475569'},transparent)")
        + '</div>'
    )
    st.markdown(kpi_cal, unsafe_allow_html=True)

    if not all_events:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">📅</div>
          <div class="empty-title">Aucun événement trouvé</div>
          <div class="empty-sub">yfinance ne dispose pas de données calendrier pour ces tickers.<br>
          Cela arrive fréquemment pour les actions françaises (.PA) — les données sont plus disponibles<br>
          pour les grandes capitalisations américaines et européennes.</div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Timeline par mois ─────────────────────────────────────────────────────
    section_label("Timeline des événements")

    # Grouper par mois
    from itertools import groupby
    def month_key(e):
        return e["date"].strftime("%B %Y").capitalize()

    # Couleurs par type
    TYPE_COLOR = {
        "Résultats":     "#3b82f6",
        "Ex-Dividende":  "#22c55e",
        "Paiement Div.": "#16a34a",
        "Fin exercice":  "#8b5cf6",
    }
    TYPE_BG = {
        "Résultats":     "rgba(59,130,246,0.07)",
        "Ex-Dividende":  "rgba(34,197,94,0.07)",
        "Paiement Div.": "rgba(22,163,74,0.07)",
        "Fin exercice":  "rgba(139,92,246,0.07)",
    }

    # Groupe par mois
    months = {}
    for e in all_events:
        mk = e["date"].strftime("%Y-%m")
        months.setdefault(mk, []).append(e)

    for mk in sorted(months.keys()):
        evts_month = months[mk]
        month_label_str = datetime.strptime(mk, "%Y-%m").strftime("%B %Y").capitalize()
        is_current = mk == today.strftime("%Y-%m")

        section_label(f"{'📍 ' if is_current else ''}{month_label_str}"
                       + (f"  ·  {len(evts_month)} événement{'s' if len(evts_month)>1 else ''}" ))

        # Grille d'événements
        html_evts = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;margin-bottom:1rem">'
        for e in sorted(evts_month, key=lambda x: x["date"]):
            c      = TYPE_COLOR.get(e["type"], "#475569")
            bg     = TYPE_BG.get(e["type"], "var(--s1)")
            jours  = (e["date"] - today).days
            if jours == 0:
                delai = '<span style="color:#f59e0b;font-weight:600">Aujourd\'hui !</span>'
            elif jours == 1:
                delai = '<span style="color:#f59e0b">Demain</span>'
            elif jours < 0:
                delai = f'<span style="color:#475569">Il y a {-jours}j</span>'
            elif jours <= 7:
                delai = f'<span style="color:#f59e0b">Dans {jours}j</span>'
            elif jours <= 30:
                delai = f'<span style="color:{c}">Dans {jours}j</span>'
            else:
                delai = f'<span style="color:var(--t3)">Dans {jours}j</span>'

            html_evts += (
                f'<div style="background:{bg};border:1px solid {c}33;'
                f'border-left:3px solid {c};border-radius:10px;padding:14px 16px">'

                # Header : icon + type + ticker
                f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">'
                f'<div style="display:flex;align-items:center;gap:8px">'
                f'<span style="font-size:1rem">{e["icon"]}</span>'
                f'<span style="font-family:DM Mono,monospace;font-size:0.6rem;color:{c};'
                f'text-transform:uppercase;letter-spacing:0.1em;font-weight:600">{e["type"]}</span>'
                f'</div>'
                f'<span style="font-family:DM Mono,monospace;font-size:0.65rem;color:#22c55e;'
                f'font-weight:600">{e["ticker"]}</span>'
                f'</div>'

                # Date + délai
                f'<div style="font-family:Outfit,sans-serif;font-size:1.05rem;font-weight:700;'
                f'color:var(--text);margin-bottom:4px">'
                f'{e["date"].strftime("%d %B %Y")}</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:0.62rem;margin-bottom:6px">'
                f'{delai}</div>'

                # Label + détail
                f'<div style="font-family:Outfit,sans-serif;font-size:0.82rem;color:var(--t2);'
                f'margin-bottom:3px">{e["label"]}</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:var(--t3)">'
                f'{e["detail"]}</div>'
                f'</div>'
            )
        html_evts += '</div>'
        st.markdown(html_evts, unsafe_allow_html=True)

    # ── Vue tableau compact ────────────────────────────────────────────────────
    with st.expander("📋  Vue tableau compacte"):
        rows_cal = ""
        for e in all_events:
            c     = TYPE_COLOR.get(e["type"], "#475569")
            jours = (e["date"] - today).days
            urgence_c = "#f59e0b" if 0 <= jours <= 7 else ("#22c55e" if 0 <= jours <= 30 else "#475569")
            rows_cal += (
                f'<tr>'
                f'<td style="text-align:left"><span style="font-family:DM Mono,monospace;'
                f'font-size:0.72rem;color:#22c55e;font-weight:600">{e["ticker"]}</span></td>'
                f'<td style="text-align:left"><span style="font-family:DM Mono,monospace;'
                f'font-size:0.65rem;font-weight:600;color:{c}">{e["icon"]} {e["type"]}</span></td>'
                f'<td style="font-family:DM Mono,monospace;font-size:0.72rem">'
                f'{e["date"].strftime("%d/%m/%Y")}</td>'
                f'<td><span style="font-family:DM Mono,monospace;font-size:0.68rem;color:{urgence_c}">'
                f'{"Passé" if jours < 0 else f"J+{jours}"}</span></td>'
                f'<td style="text-align:left;font-family:Outfit,sans-serif;font-size:0.8rem;'
                f'color:var(--t2)">{e["detail"]}</td>'
                f'</tr>'
            )
        st.markdown(
            f'<div style="background:var(--s1);border:1px solid var(--border);'
            f'border-radius:11px;overflow:hidden">'
            f'<table class="ptable"><thead><tr>'
            f'<th style="text-align:left">Ticker</th>'
            f'<th style="text-align:left">Type</th>'
            f'<th>Date</th><th>Délai</th>'
            f'<th style="text-align:left">Détail</th>'
            f'</tr></thead><tbody>{rows_cal}</tbody></table></div>',
            unsafe_allow_html=True
        )

    # ── Note sur la disponibilité des données ─────────────────────────────────
    st.markdown(
        '<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#2d3f57;'
        'margin-top:1rem;line-height:2">ℹ Données via yfinance · Disponibilité variable selon les tickers · '
        'Actions françaises (.PA) souvent non disponibles · Rafraîchissement toutes les heures</div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""<div class="nav-logo">
      <span class="dot"></span>
      <div>PEA<span class="sub">Dashboard · Finance</span></div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("Navigation",
        options=[
            "▸  Portefeuille",
            "◎  Analyse 10-Baggers",
            "⊞  Screener Multi-Actions",
            "◈  Intelligence de Marché",
            "⏱  Backtesting",
            "💰  Simulateur",
            "📓  Journal",
            "💸  Dividendes",
            "📐  TRI",
            "👁  Watchlist",
            "⚖  Comparaison",
            "📅  Calendrier",
            "📄  Rapport PDF",
            "⚙  Paramètres",
        ],
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

if   "Portefeuille"  in page: page_portfolio()
elif "10-Baggers"    in page: page_10baggers()
elif "Screener"      in page: page_screener()
elif "Intelligence"  in page: page_intelligence()
elif "Backtesting"   in page: page_backtesting()
elif "Simulateur"    in page: page_simulateur()
elif "Journal"       in page: page_journal()
elif "Dividendes"    in page: page_dividendes()
elif "TRI"           in page: page_tri()
elif "Watchlist"     in page: page_watchlist()
elif "Comparaison"   in page: page_comparaison()
elif "Calendrier"    in page: page_calendrier()
elif "Rapport"       in page: page_rapport()
else:                          page_parametres()