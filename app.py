import streamlit as st
from agents import agent_orchestrator
from fpdf import FPDF

st.set_page_config(
    page_title="LegalEase — AI Contract Analysis for Pakistan",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {padding-top: 0rem; padding-bottom: 0rem; max-width: 100%;}
* {box-sizing: border-box;}

/* NAV */
.navbar {
    background: #0f172a;
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.logo-wrap {display: flex; align-items: center; gap: 10px;}
.logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.logo-name {font-size: 18px; font-weight: 700; color: white;}
.logo-tag {font-size: 10px; color: #94a3b8; margin-top: -2px;}
.nav-links {display: flex; gap: 28px; align-items: center;}
.nav-link {font-size: 13px; color: #94a3b8; cursor: pointer; text-decoration: none; transition: color 0.2s;}
.nav-link:hover {color: white;}
.nav-link.active {color: #60a5fa; font-weight: 500;}
.nav-cta {
    font-size: 13px; font-weight: 600;
    padding: 8px 18px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

/* HERO */
.hero {
    background: #0f172a;
    padding: 70px 40px 60px;
    text-align: center;
    border-bottom: 1px solid #1e293b;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #1e3a5f;
    color: #60a5fa;
    font-size: 12px; font-weight: 600;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
    border: 1px solid #2563eb33;
}
.hero-title {
    font-size: 42px; font-weight: 800;
    color: white;
    line-height: 1.15;
    margin-bottom: 16px;
}
.hero-title span {
    background: linear-gradient(135deg, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 16px; color: #94a3b8;
    max-width: 520px;
    margin: 0 auto 28px;
    line-height: 1.7;
}
.hero-tags {display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 40px;}
.hero-tag {
    font-size: 12px; font-weight: 500;
    padding: 5px 14px;
    border-radius: 20px;
    border: 1px solid;
}
.hero-tag-green {background: #052e16; color: #4ade80; border-color: #166534;}
.hero-tag-blue {background: #1e3a5f; color: #60a5fa; border-color: #1d4ed8;}
.hero-tag-yellow {background: #422006; color: #fbbf24; border-color: #92400e;}
.hero-stats {
    display: flex; justify-content: center; gap: 48px;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 20px 32px;
    max-width: 560px;
    margin: 0 auto;
}
.hero-stat-num {font-size: 26px; font-weight: 800; color: #60a5fa;}
.hero-stat-label {font-size: 11px; color: #64748b; margin-top: 3px;}

/* SECTIONS */
.section {padding: 56px 40px; border-bottom: 1px solid #e5e7eb;}
.section-dark {background: #f8fafc;}
.section-label {
    font-size: 11px; font-weight: 700;
    color: #3b82f6;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-align: center;
    margin-bottom: 8px;
}
.section-title {
    font-size: 28px; font-weight: 700;
    color: #111827;
    text-align: center;
    margin-bottom: 10px;
}
.section-sub {
    font-size: 15px; color: #6b7280;
    text-align: center;
    margin-bottom: 36px;
    max-width: 480px;
    margin-left: auto;
    margin-right: auto;
}

/* STEPS */
.steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    max-width: 860px;
    margin: 0 auto;
}
.step-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 28px 22px;
    text-align: center;
    transition: border-color 0.2s;
}
.step-card:hover {border-color: #3b82f6;}
.step-num {
    width: 44px; height: 44px;
    background: #eff6ff;
    color: #1d4ed8;
    border-radius: 12px;
    font-size: 18px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 16px;
}
.step-title {font-size: 15px; font-weight: 600; color: #111827; margin-bottom: 8px;}
.step-body {font-size: 13px; color: #6b7280; line-height: 1.6;}

/* AGENTS */
.agents-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    max-width: 860px;
    margin: 0 auto;
}
.agent-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 22px 18px;
}
.agent-icon {
    width: 42px; height: 42px;
    border-radius: 10px;
    font-size: 20px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 14px;
}
.agent-num {font-size: 10px; font-weight: 700; color: #9ca3af; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;}
.agent-title {font-size: 13px; font-weight: 600; color: #111827; margin-bottom: 6px;}
.agent-body {font-size: 12px; color: #6b7280; line-height: 1.5;}

/* UPLOAD */
.upload-section {
    background: #f8fafc;
    padding: 48px 40px;
    border-bottom: 1px solid #e5e7eb;
}
.upload-title-wrap {text-align: center; margin-bottom: 28px;}
.upload-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    max-width: 760px;
    margin: 0 auto 24px;
}
.upload-card {
    background: white;
    border: 2px dashed #d1d5db;
    border-radius: 14px;
    padding: 22px 16px;
    text-align: center;
    transition: all 0.2s;
}
.upload-card:hover {border-color: #3b82f6; background: #eff6ff;}
.upload-emoji {font-size: 28px; margin-bottom: 8px;}
.upload-name {font-size: 13px; font-weight: 600; color: #111827; margin-bottom: 3px;}
.upload-hint {font-size: 11px; color: #9ca3af;}
.free-bar {
    text-align: center;
    font-size: 13px; color: #6b7280;
    margin: 12px 0 4px;
}
.free-bar span {font-weight: 700; color: #1d4ed8;}

/* RESULTS */
.results-wrap {max-width: 860px; margin: 0 auto;}
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 24px;
}
.metric-box {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.metric-val {font-size: 28px; font-weight: 700;}
.metric-lbl {font-size: 12px; color: #6b7280; margin-top: 3px;}
.clause-card {
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    border-left: 4px solid;
}
.clause-high {background: #fef2f2; border-color: #ef4444;}
.clause-medium {background: #fffbeb; border-color: #f59e0b;}
.clause-low {background: #f0fdf4; border-color: #22c55e;}
.clause-top {display: flex; align-items: center; gap: 10px; margin-bottom: 8px;}
.risk-pill {
    font-size: 11px; font-weight: 700;
    padding: 3px 10px; border-radius: 20px;
}
.pill-high {background: #fee2e2; color: #dc2626;}
.pill-medium {background: #fef3c7; color: #d97706;}
.pill-low {background: #dcfce7; color: #16a34a;}
.clause-num {font-size: 12px; font-weight: 600; color: #374151;}
.clause-text {font-size: 13px; color: #374151; line-height: 1.5; margin-bottom: 6px;}
.clause-reason {font-size: 12px; color: #6b7280; line-height: 1.4;}
.clause-urdu {font-size: 12px; color: #6b7280; margin-top: 4px; direction: rtl; text-align: right;}

/* REWRITE */
.rewrite-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
}
.rewrite-top {display: flex; align-items: center; gap: 8px; margin-bottom: 12px;}
.rewrite-grid {display: grid; grid-template-columns: 1fr 1fr; gap: 12px;}
.rewrite-box {border-radius: 8px; padding: 12px; font-size: 13px; line-height: 1.5;}
.rewrite-bad {background: #fef2f2; color: #374151; border: 1px solid #fecaca;}
.rewrite-good {background: #f0fdf4; color: #374151; border: 1px solid #bbf7d0;}
.rewrite-label {font-size: 11px; font-weight: 700; margin-bottom: 6px;}
.rewrite-label-bad {color: #dc2626;}
.rewrite-label-good {color: #16a34a;}

/* PRICING */
.pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    max-width: 780px;
    margin: 0 auto;
}
.pricing-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 28px 22px;
}
.pricing-card.featured {
    background: #0f172a;
    border: 2px solid #3b82f6;
}
.pricing-badge {
    display: inline-block;
    font-size: 10px; font-weight: 700;
    padding: 3px 10px; border-radius: 20px;
    background: #dbeafe; color: #1d4ed8;
    margin-bottom: 12px;
}
.pricing-badge.feat {background: #1e3a5f; color: #60a5fa;}
.pricing-name {font-size: 15px; font-weight: 600; color: #111827; margin-bottom: 6px;}
.pricing-name.white {color: white;}
.pricing-price {font-size: 30px; font-weight: 800; color: #111827;}
.pricing-price.white {color: white;}
.pricing-mo {font-size: 13px; color: #6b7280; margin-bottom: 16px;}
.pricing-mo.white {color: #94a3b8;}
.pricing-divider {border: none; border-top: 1px solid #e5e7eb; margin: 16px 0;}
.pricing-divider.dark {border-top-color: #1e293b;}
.pricing-feat {font-size: 13px; color: #374151; margin-bottom: 8px; display: flex; align-items: flex-start; gap: 8px; line-height: 1.4;}
.pricing-feat.white {color: #94a3b8;}
.pricing-btn {
    width: 100%; padding: 10px;
    border-radius: 8px;
    font-size: 13px; font-weight: 600;
    cursor: pointer; margin-top: 16px;
    border: 1px solid #d1d5db;
    background: white; color: #1d4ed8;
}
.pricing-btn.feat {background: #3b82f6; color: white; border: none;}

/* FOOTER */
.footer {
    background: #0f172a;
    padding: 28px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
.footer-logo {font-size: 16px; font-weight: 700; color: white;}
.footer-mid {font-size: 12px; color: #475569; text-align: center;}
.footer-links {display: flex; gap: 20px;}
.footer-link {font-size: 12px; color: #475569;}

@media (max-width: 600px) {
    .hero-title {font-size: 26px;}
    .hero-stats {gap: 20px; padding: 16px;}
    .nav-links {display: none;}
    .section {padding: 36px 20px;}
    .metric-row {grid-template-columns: repeat(2, 1fr);}
    .rewrite-grid {grid-template-columns: 1fr;}
    .footer {flex-direction: column; text-align: center;}
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "free_uses" not in st.session_state:
    st.session_state.free_uses = 3

# NAV
st.markdown("""
<div class="navbar">
    <div class="logo-wrap">
        <div class="logo-icon">⚖️</div>
        <div>
            <div class="logo-name">LegalEase</div>
            <div class="logo-tag">AI Contract Analysis</div>
        </div>
    </div>
    <div class="nav-links">
        <a class="nav-link" href="#how-it-works">How it works</a>
        <a class="nav-link" href="#pricing">Pricing</a>
        <a class="nav-link" href="#analyse">Analyse</a>
        <button class="nav-cta">Try free</button>
    </div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">⚡ Pakistan's first AI contract checker</div>
    <div class="hero-title">Know what you're signing<br><span>before it's too late</span></div>
    <div class="hero-sub">Upload any contract — LegalEase flags risky clauses, explains them in Urdu and English, and rewrites them into fair versions instantly.</div>
    <div class="hero-tags">
        <span class="hero-tag hero-tag-green">✓ Free for 3 contracts/month</span>
        <span class="hero-tag hero-tag-blue">✓ Results in 10 seconds</span>
        <span class="hero-tag hero-tag-yellow">✓ English and Urdu</span>
    </div>
    <div class="hero-stats">
        <div><div class="hero-stat-num">4</div><div class="hero-stat-label">AI agents</div></div>
        <div><div class="hero-stat-num">10s</div><div class="hero-stat-label">Analysis time</div></div>
        <div><div class="hero-stat-num">Rs.0</div><div class="hero-stat-label">vs Rs.15,000 lawyer</div></div>
        <div><div class="hero-stat-num">2</div><div class="hero-stat-label">Languages</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# HOW IT WORKS
st.markdown("""
<div id="how-it-works" class="section section-dark">
    <div class="section-label">The process</div>
    <div class="section-title">3 steps to a safe contract</div>
    <div class="section-sub">No legal knowledge needed. No lawyer fees. No waiting days.</div>
    <div class="steps-grid">
        <div class="step-card">
            <div class="step-num">1</div>
            <div class="step-title">Upload your contract</div>
            <div class="step-body">Upload a PDF, scan a printed contract with your phone camera, or paste the text directly. Any format works.</div>
        </div>
        <div class="step-card">
            <div class="step-num">2</div>
            <div class="step-title">4 AI agents analyse it</div>
            <div class="step-body">Agents check every clause against Pakistani law and flag HIGH, MEDIUM, or LOW risk in Urdu and English.</div>
        </div>
        <div class="step-card">
            <div class="step-num">3</div>
            <div class="step-title">Download safe contract</div>
            <div class="step-body">Risky clauses are rewritten into fair versions. Download the fixed contract as a professional PDF.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4 AGENTS
st.markdown("""
<div class="section">
    <div class="section-label">Under the hood</div>
    <div class="section-title">Meet your 4 AI agents</div>
    <div class="section-sub">Each agent is a specialist. Together they cover everything.</div>
    <div class="agents-grid">
        <div class="agent-card">
            <div class="agent-icon" style="background:#ede9fe;">🧠</div>
            <div class="agent-num">Agent 1</div>
            <div class="agent-title">Orchestrator</div>
            <div class="agent-body">The manager. Coordinates all agents and assembles the final report for you.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon" style="background:#dbeafe;">📄</div>
            <div class="agent-num">Agent 2</div>
            <div class="agent-title">Document parser</div>
            <div class="agent-body">Reads your PDF or image, extracts text, and splits it into individual clauses.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon" style="background:#fee2e2;">⚠️</div>
            <div class="agent-num">Agent 3</div>
            <div class="agent-title">Clause analyser</div>
            <div class="agent-body">Reviews each clause against Pakistani law. Flags risk in English and Urdu.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon" style="background:#dcfce7;">✏️</div>
            <div class="agent-num">Agent 4</div>
            <div class="agent-title">Draft generator</div>
            <div class="agent-body">Rewrites every risky clause into a fair, balanced version that protects you.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ANALYSE SECTION
st.markdown("""
<div id="analyse" class="upload-section">
    <div class="upload-title-wrap">
        <div class="section-label">Analyse your contract</div>
        <div class="section-title">Try it now — it's free</div>
        <div class="section-sub">Upload, scan, or paste your contract below and let 4 AI agents do the work.</div>
    </div>
    <div class="upload-grid">
        <div class="upload-card">
            <div class="upload-emoji">📄</div>
            <div class="upload-name">Upload PDF</div>
            <div class="upload-hint">Drop your contract PDF here</div>
        </div>
        <div class="upload-card">
            <div class="upload-emoji">📷</div>
            <div class="upload-name">Scan image</div>
            <div class="upload-hint">Photo of a printed contract</div>
        </div>
        <div class="upload-card">
            <div class="upload-emoji">✏️</div>
            <div class="upload-name">Paste text</div>
            <div class="upload-hint">Copy and paste clauses directly</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    uploaded_file = st.file_uploader("Upload PDF contract", type=["pdf"], label_visibility="collapsed")
with col2:
    scanned_image = st.file_uploader("Scan contract image", type=["jpg","jpeg","png"], label_visibility="collapsed")
with col3:
    raw_text = st.text_area("Paste contract text", height=100, placeholder="Paste any contract clauses here...", label_visibility="collapsed")

free_left = st.session_state.free_uses
st.markdown(f"""
<div class="free-bar">
    Free analyses remaining this month: <span>{free_left}/3</span>
</div>
""", unsafe_allow_html=True)

run = st.button("🔍 Analyse Contract — 4 Agents", use_container_width=True, type="primary")

if run:
    if not uploaded_file and not raw_text.strip() and not scanned_image:
        st.error("Please upload a PDF, scan an image, or paste contract text first.")
    elif st.session_state.free_uses <= 0:
        st.warning("You've used all 3 free analyses. Upgrade to Pro for unlimited analyses — Rs. 999/month.")
    else:
        st.session_state.free_uses -= 1
        status_box = st.empty()
        progress = st.progress(0)
        step = [0]

        def update_status(msg):
            step[0] += 25
            status_box.info(f"⚙️ {msg}")
            progress.progress(min(step[0], 100))

        if scanned_image:
            from PIL import Image
            status_box.info("Processing scanned image...")

        with st.spinner("Running 4-agent pipeline..."):
            analysed, rewrites = agent_orchestrator(
                uploaded_file=uploaded_file if uploaded_file else None,
                raw_text=raw_text if raw_text.strip() else None,
                status_callback=update_status
            )

        progress.progress(100)
        status_box.success("✅ All 4 agents completed!")

        if not analysed:
            st.error("Could not extract clauses. Please check your input.")
        else:
            high   = sum(1 for c in analysed if c.get("risk") == "HIGH")
            medium = sum(1 for c in analysed if c.get("risk") == "MEDIUM")
            low    = sum(1 for c in analysed if c.get("risk") == "LOW")

            st.markdown(f"""
            <div class="results-wrap">
            <div class="metric-row">
                <div class="metric-box"><div class="metric-val" style="color:#111827;">{len(analysed)}</div><div class="metric-lbl">Total clauses</div></div>
                <div class="metric-box"><div class="metric-val" style="color:#dc2626;">{high}</div><div class="metric-lbl">High risk</div></div>
                <div class="metric-box"><div class="metric-val" style="color:#d97706;">{medium}</div><div class="metric-lbl">Medium risk</div></div>
                <div class="metric-box"><div class="metric-val" style="color:#16a34a;">{low}</div><div class="metric-lbl">Low risk</div></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📋 Clause Analysis — Agent 3")
            for clause in analysed:
                risk = clause.get("risk", "LOW")
                css = {"HIGH": "clause-high", "MEDIUM": "clause-medium", "LOW": "clause-low"}.get(risk, "clause-low")
                pill = {"HIGH": "pill-high", "MEDIUM": "pill-medium", "LOW": "pill-low"}.get(risk, "pill-low")
                st.markdown(f"""
                <div class="clause-card {css}">
                    <div class="clause-top">
                        <span class="risk-pill {pill}">{risk}</span>
                        <span class="clause-num">Clause {clause['clause_number']}</span>
                    </div>
                    <div class="clause-text">{clause['original']}</div>
                    <div class="clause-reason">⚠️ {clause['reason']}</div>
                    <div class="clause-urdu">{clause['urdu_summary']}</div>
                </div>
                """, unsafe_allow_html=True)

            if rewrites:
                st.markdown("### ✏️ Safe Contract Draft — Agent 4")
                for r in rewrites:
                    pill = "pill-high" if r.get("risk") == "HIGH" else "pill-medium"
                    st.markdown(f"""
                    <div class="rewrite-card">
                        <div class="rewrite-top">
                            <span class="risk-pill {pill}">{r['risk']} RISK FIXED</span>
                            <span class="clause-num">Clause {r['clause_number']}</span>
                        </div>
                        <div class="rewrite-grid">
                            <div class="rewrite-box rewrite-bad">
                                <div class="rewrite-label rewrite-label-bad">❌ Original (risky)</div>
                                {r['original']}
                            </div>
                            <div class="rewrite-box rewrite-good">
                                <div class="rewrite-label rewrite-label-good">✅ Safe version</div>
                                {r['safe_version']}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("### 📄 Download Safe Contract")
                pdf = FPDF()
                pdf.set_margins(10, 10, 10)
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=10)
                pdf.set_font("Helvetica", "B", 18)
                pdf.cell(180, 12, "LegalEase - Safe Contract Draft", ln=True, align="C")
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(180, 8, "AI-powered contract analysis for Pakistan", ln=True, align="C")
                pdf.ln(5)
                for r in rewrites:
                    pdf.set_fill_color(240, 240, 240)
                    pdf.set_font("Helvetica", "B", 11)
                    title = f"Clause {r['clause_number']} | {r['risk']} RISK - Fixed"
                    pdf.multi_cell(180, 9, title.encode('latin-1', 'replace').decode('latin-1'), fill=True)
                    pdf.ln(2)
                    pdf.set_font("Helvetica", "I", 9)
                    pdf.multi_cell(180, 6, f"Risk: {r['reason']}".encode('latin-1', 'replace').decode('latin-1'))
                    pdf.ln(2)
                    pdf.set_font("Helvetica", "B", 9)
                    pdf.multi_cell(180, 6, "Safe version:".encode('latin-1', 'replace').decode('latin-1'))
                    pdf.set_font("Helvetica", size=10)
                    pdf.multi_cell(180, 7, r["safe_version"].encode('latin-1', 'replace').decode('latin-1'))
                    pdf.ln(5)
                pdf_bytes = pdf.output()
                st.download_button(
                    "📄 Download Safe Contract PDF",
                    data=bytes(pdf_bytes),
                    file_name="legalease_safe_contract.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

# PRICING
st.markdown("""
<div id="pricing" class="section section-dark">
    <div class="section-label">Pricing</div>
    <div class="section-title">Simple, honest pricing</div>
    <div class="section-sub">Start free. Upgrade when you need more.</div>
    <div class="pricing-grid">
        <div class="pricing-card">
            <div class="pricing-badge">Free forever</div>
            <div class="pricing-name">Free</div>
            <div class="pricing-price">Rs. 0</div>
            <div class="pricing-mo">forever</div>
            <hr class="pricing-divider">
            <div class="pricing-feat">✓ 3 contract analyses/month</div>
            <div class="pricing-feat">✓ Risk detection</div>
            <div class="pricing-feat">✓ English and Urdu</div>
            <div class="pricing-feat">✓ PDF download</div>
            <button class="pricing-btn">Get started free</button>
        </div>
        <div class="pricing-card featured">
            <div class="pricing-badge feat">Most popular</div>
            <div class="pricing-name white">Pro</div>
            <div class="pricing-price white">Rs. 999</div>
            <div class="pricing-mo white">per month</div>
            <hr class="pricing-divider dark">
            <div class="pricing-feat white">✓ Unlimited analyses</div>
            <div class="pricing-feat white">✓ Contract history</div>
            <div class="pricing-feat white">✓ Priority support</div>
            <div class="pricing-feat white">✓ All contract types</div>
            <button class="pricing-btn feat">Upgrade to Pro</button>
        </div>
        <div class="pricing-card">
            <div class="pricing-badge">For companies</div>
            <div class="pricing-name">Business</div>
            <div class="pricing-price">Rs. 4,999</div>
            <div class="pricing-mo">per month</div>
            <hr class="pricing-divider">
            <div class="pricing-feat">✓ Unlimited analyses</div>
            <div class="pricing-feat">✓ 10 team members</div>
            <div class="pricing-feat">✓ API access</div>
            <div class="pricing-feat">✓ Dedicated support</div>
            <button class="pricing-btn">Contact us</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    <div class="footer-logo">⚖️ LegalEase</div>
    <div class="footer-mid">AI-powered contract analysis for Pakistan — Not a substitute for legal advice</div>
    <div class="footer-links">
        <span class="footer-link">Privacy</span>
        <span class="footer-link">Terms</span>
        <span class="footer-link">Contact</span>
    </div>
</div>
""", unsafe_allow_html=True)
