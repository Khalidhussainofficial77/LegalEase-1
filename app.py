import streamlit as st
from agents import agent_orchestrator
from fpdf import FPDF

st.set_page_config(
    page_title="LegalEase — AI Contract Analysis for Pakistan",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ──
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {padding-top: 0rem; padding-bottom: 0rem; max-width: 100%;}

.navbar {
    background: white;
    border-bottom: 1px solid #e5e7eb;
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.logo-text {font-size: 20px; font-weight: 700; color: #1e40af;}
.logo-sub {font-size: 11px; color: #6b7280; margin-top: -2px;}

.hero-section {
    background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
    padding: 60px 40px;
    text-align: center;
    border-bottom: 1px solid #e5e7eb;
}
.hero-badge {
    display: inline-block;
    background: #dbeafe;
    color: #1e40af;
    font-size: 12px;
    font-weight: 600;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 16px;
}
.hero-title {
    font-size: 36px;
    font-weight: 800;
    color: #111827;
    line-height: 1.2;
    margin-bottom: 14px;
}
.hero-title span {color: #1e40af;}
.hero-sub {
    font-size: 16px;
    color: #6b7280;
    max-width: 560px;
    margin: 0 auto 28px;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin-top: 32px;
}
.hero-stat-num {font-size: 24px; font-weight: 700; color: #1e40af;}
.hero-stat-label {font-size: 12px; color: #6b7280; margin-top: 2px;}

.how-section {
    padding: 48px 40px;
    background: white;
    border-bottom: 1px solid #e5e7eb;
}
.section-label {
    font-size: 12px;
    font-weight: 600;
    color: #1e40af;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
    text-align: center;
}
.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #111827;
    text-align: center;
    margin-bottom: 8px;
}
.section-sub {
    font-size: 14px;
    color: #6b7280;
    text-align: center;
    margin-bottom: 32px;
}

.steps-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    max-width: 900px;
    margin: 0 auto;
}
.step-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
}
.step-num {
    width: 40px; height: 40px;
    background: #1e40af;
    color: white;
    border-radius: 50%;
    font-size: 16px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px;
}
.step-title {font-size: 15px; font-weight: 600; color: #111827; margin-bottom: 6px;}
.step-body {font-size: 13px; color: #6b7280; line-height: 1.5;}

.agents-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    max-width: 900px;
    margin: 0 auto;
}
.agent-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px 16px;
}
.agent-icon {
    width: 40px; height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 12px;
}
.agent-title {font-size: 13px; font-weight: 600; color: #111827; margin-bottom: 4px;}
.agent-body {font-size: 12px; color: #6b7280; line-height: 1.4;}

.analyse-section {
    padding: 40px;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}
.upload-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    max-width: 800px;
    margin: 0 auto 20px;
}
.upload-card {
    background: white;
    border: 2px dashed #d1d5db;
    border-radius: 12px;
    padding: 24px 16px;
    text-align: center;
    cursor: pointer;
}
.upload-icon {font-size: 28px; margin-bottom: 8px;}
.upload-title {font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 4px;}
.upload-sub {font-size: 12px; color: #9ca3af;}

.result-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
}
.risk-high {background: #fef2f2; border-left: 4px solid #ef4444; border-radius: 0 8px 8px 0;}
.risk-medium {background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 0 8px 8px 0;}
.risk-low {background: #f0fdf4; border-left: 4px solid #22c55e; border-radius: 0 8px 8px 0;}

.badge-high {background:#fef2f2;color:#dc2626;font-size:11px;padding:3px 10px;border-radius:20px;font-weight:600;}
.badge-medium {background:#fffbeb;color:#d97706;font-size:11px;padding:3px 10px;border-radius:20px;font-weight:600;}
.badge-low {background:#f0fdf4;color:#16a34a;font-size:11px;padding:3px 10px;border-radius:20px;font-weight:600;}

.pricing-section {
    padding: 48px 40px;
    background: white;
    border-bottom: 1px solid #e5e7eb;
}
.pricing-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    max-width: 800px;
    margin: 0 auto;
}
.pricing-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px;
}
.pricing-card.featured {
    background: #1e40af;
    border-color: #1e40af;
}
.pricing-name {font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 4px;}
.pricing-name.white {color: white;}
.pricing-price {font-size: 28px; font-weight: 800; color: #111827; margin-bottom: 4px;}
.pricing-price.white {color: white;}
.pricing-period {font-size: 12px; color: #6b7280;}
.pricing-period.white {color: #93c5fd;}
.pricing-divider {border: none; border-top: 1px solid #e5e7eb; margin: 16px 0;}
.pricing-divider.white {border-top-color: #3b5bdb;}
.pricing-feature {font-size: 13px; color: #374151; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;}
.pricing-feature.white {color: #bfdbfe;}
.pricing-btn {
    width: 100%;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #d1d5db;
    background: white;
    color: #1e40af;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 16px;
}
.pricing-btn.featured {background: white; color: #1e40af; border: none;}

.footer-bar {
    background: #111827;
    padding: 24px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.footer-logo {font-size: 16px; font-weight: 700; color: white;}
.footer-text {font-size: 12px; color: #9ca3af;}
.footer-links {display: flex; gap: 20px;}
.footer-link {font-size: 12px; color: #9ca3af;}

.metric-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.metric-num {font-size: 28px; font-weight: 700;}
.metric-label {font-size: 12px; color: #6b7280; margin-top: 2px;}
</style>
""", unsafe_allow_html=True)

# ── Session state for page navigation ──
if "page" not in st.session_state:
    st.session_state.page = "home"
if "free_uses" not in st.session_state:
    st.session_state.free_uses = 3

# ── NAVBAR ──
st.markdown("""
<div class="navbar">
    <div>
        <div class="logo-text">⚖️ LegalEase</div>
        <div class="logo-sub">AI Contract Analysis for Pakistan</div>
    </div>
    <div style="display:flex;gap:24px;align-items:center;">
        <span style="font-size:13px;color:#6b7280;">How it works</span>
        <span style="font-size:13px;color:#6b7280;">Pricing</span>
        <span style="font-size:13px;color:#6b7280;">About</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown(f"""
<div class="hero-section">
    <div class="hero-badge">Pakistan's first AI contract checker</div>
    <div class="hero-title">Know what you're signing<br><span>before it's too late</span></div>
    <div class="hero-sub">Upload any contract — LegalEase flags risky clauses, explains them in Urdu and English, and rewrites them into fair versions.</div>
    <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
        <div style="background:#dcfce7;color:#15803d;font-size:12px;padding:5px 14px;border-radius:20px;font-weight:600;">✓ Free for 3 contracts/month</div>
        <div style="background:#dbeafe;color:#1e40af;font-size:12px;padding:5px 14px;border-radius:20px;font-weight:600;">✓ Results in 10 seconds</div>
        <div style="background:#fef3c7;color:#92400e;font-size:12px;padding:5px 14px;border-radius:20px;font-weight:600;">✓ English and Urdu</div>
    </div>
    <div class="hero-stats">
        <div><div class="hero-stat-num">4</div><div class="hero-stat-label">AI agents</div></div>
        <div><div class="hero-stat-num">10s</div><div class="hero-stat-label">Analysis time</div></div>
        <div><div class="hero-stat-num">Rs.0</div><div class="hero-stat-label">vs Rs.15,000 lawyer</div></div>
        <div><div class="hero-stat-num">2</div><div class="hero-stat-label">Languages</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HOW IT WORKS ──
st.markdown("""
<div class="how-section">
    <div class="section-label">The process</div>
    <div class="section-title">3 steps to a safe contract</div>
    <div class="section-sub">No legal knowledge needed. No lawyer fees. No waiting days.</div>
    <div class="steps-grid">
        <div class="step-card">
            <div class="step-num">1</div>
            <div class="step-title">Upload your contract</div>
            <div class="step-body">Upload a PDF, scan a printed contract with your phone camera, or paste the text directly.</div>
        </div>
        <div class="step-card">
            <div class="step-num">2</div>
            <div class="step-title">4 AI agents analyse it</div>
            <div class="step-body">Agents check every clause against Pakistani law and flag HIGH, MEDIUM, or LOW risk in Urdu and English.</div>
        </div>
        <div class="step-card">
            <div class="step-num">3</div>
            <div class="step-title">Download safe contract</div>
            <div class="step-body">Risky clauses are rewritten into fair versions. Download the fixed contract as a PDF instantly.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 4 AGENTS ──
st.markdown("""
<div class="how-section" style="background:#f9fafb;">
    <div class="section-label">Under the hood</div>
    <div class="section-title">Meet your 4 AI agents</div>
    <div class="section-sub">Each agent is a specialist. Together they cover everything.</div>
    <div class="agents-grid">
        <div class="agent-card">
            <div class="agent-icon" style="background:#ede9fe;">🧠</div>
            <div class="agent-title">Agent 1 — Orchestrator</div>
            <div class="agent-body">The manager. Coordinates all agents and assembles the final report.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon" style="background:#dbeafe;">📄</div>
            <div class="agent-title">Agent 2 — Parser</div>
            <div class="agent-body">Reads your PDF or image and breaks it into individual clauses.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon" style="background:#fee2e2;">⚠️</div>
            <div class="agent-title">Agent 3 — Analyser</div>
            <div class="agent-body">Reviews each clause against Pakistani law. Flags risk in English and Urdu.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon" style="background:#dcfce7;">✏️</div>
            <div class="agent-title">Agent 4 — Generator</div>
            <div class="agent-body">Rewrites every risky clause into a fair, balanced version.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── ANALYSE SECTION ──
st.markdown("""
<div class="analyse-section">
    <div class="section-label">Analyse your contract</div>
    <div class="section-title">Try it now — free</div>
    <div class="section-sub">Upload, scan, or paste your contract below.</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    uploaded_file = st.file_uploader("📄 Upload PDF contract", type=["pdf"])
with col2:
    scanned_image = st.file_uploader("📷 Scan contract image", type=["jpg","jpeg","png"])
with col3:
    raw_text = st.text_area("✏️ Paste contract text", height=120,
                            placeholder="Paste any contract clauses here...")

free_left = st.session_state.free_uses
st.markdown(f"""
<div style="text-align:center;margin:8px 0;">
    <span style="font-size:12px;color:#6b7280;">Free analyses remaining this month: </span>
    <span style="font-size:12px;font-weight:700;color:#1e40af;">{free_left}/3</span>
</div>
""", unsafe_allow_html=True)

run = st.button("🔍 Analyse Contract (4 Agents)", use_container_width=True, type="primary")

if run:
    if not uploaded_file and not raw_text.strip() and not scanned_image:
        st.error("Please upload a PDF, scan an image, or paste contract text first.")
    elif st.session_state.free_uses <= 0:
        st.warning("You've used all 3 free analyses this month. Upgrade to Pro for unlimited analyses — Rs. 999/month.")
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
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0;">
                <div class="metric-card"><div class="metric-num" style="color:#111827;">{len(analysed)}</div><div class="metric-label">Total clauses</div></div>
                <div class="metric-card"><div class="metric-num" style="color:#dc2626;">{high}</div><div class="metric-label">High risk</div></div>
                <div class="metric-card"><div class="metric-num" style="color:#d97706;">{medium}</div><div class="metric-label">Medium risk</div></div>
                <div class="metric-card"><div class="metric-num" style="color:#16a34a;">{low}</div><div class="metric-label">Low risk</div></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📋 Clause Analysis — Agent 3 Output")
            for clause in analysed:
                risk = clause.get("risk", "LOW")
                css = {"HIGH": "risk-high", "MEDIUM": "risk-medium", "LOW": "risk-low"}.get(risk, "risk-low")
                badge = {"HIGH": "badge-high", "MEDIUM": "badge-medium", "LOW": "badge-low"}.get(risk, "badge-low")
                with st.expander(f"Clause {clause['clause_number']} — {risk} RISK"):
                    st.markdown(f"**Original clause:**")
                    st.info(clause['original'])
                    st.markdown(f"**⚠️ Risk reason:** {clause['reason']}")
                    st.markdown(f"**اردو:** {clause['urdu_summary']}")

            if rewrites:
                st.markdown("### ✏️ Safe Contract Draft — Agent 4 Output")
                for r in rewrites:
                    with st.expander(f"Clause {r['clause_number']} — Rewritten ({r['risk']} risk fixed)"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown("**❌ Original (risky)**")
                            st.error(r["original"])
                        with col_b:
                            st.markdown("**✅ Safe version**")
                            st.success(r["safe_version"])

                pdf = FPDF()
                pdf.set_margins(10, 10, 10)
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=10)
                pdf.set_font("Helvetica", "B", 18)
                pdf.cell(180, 12, "LegalEase - Safe Contract Draft", ln=True, align="C")
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(180, 8, "AI-powered contract analysis for Pakistan | legalease.pk", ln=True, align="C")
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

# ── PRICING ──
st.markdown("""
<div class="pricing-section">
    <div class="section-label">Pricing</div>
    <div class="section-title">Simple, honest pricing</div>
    <div class="section-sub">Start free. Upgrade when you need more.</div>
    <div class="pricing-grid">
        <div class="pricing-card">
            <div class="pricing-name">Free</div>
            <div class="pricing-price">Rs. 0</div>
            <div class="pricing-period">forever</div>
            <hr class="pricing-divider">
            <div class="pricing-feature">✓ 3 contract analyses/month</div>
            <div class="pricing-feature">✓ Risk detection</div>
            <div class="pricing-feature">✓ English and Urdu</div>
            <div class="pricing-feature">✓ PDF download</div>
            <button class="pricing-btn">Get started free</button>
        </div>
        <div class="pricing-card featured">
            <div class="pricing-name white">Pro ⭐ Most popular</div>
            <div class="pricing-price white">Rs. 999</div>
            <div class="pricing-period white">per month</div>
            <hr class="pricing-divider white">
            <div class="pricing-feature white">✓ Unlimited analyses</div>
            <div class="pricing-feature white">✓ Contract history</div>
            <div class="pricing-feature white">✓ Priority support</div>
            <div class="pricing-feature white">✓ All contract types</div>
            <button class="pricing-btn featured">Upgrade to Pro</button>
        </div>
        <div class="pricing-card">
            <div class="pricing-name">Business</div>
            <div class="pricing-price">Rs. 4,999</div>
            <div class="pricing-period">per month</div>
            <hr class="pricing-divider">
            <div class="pricing-feature">✓ Unlimited analyses</div>
            <div class="pricing-feature">✓ 10 team members</div>
            <div class="pricing-feature">✓ API access</div>
            <div class="pricing-feature">✓ Dedicated support</div>
            <button class="pricing-btn">Contact us</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer-bar">
    <div class="footer-logo">⚖️ LegalEase</div>
    <div class="footer-text">AI-powered contract analysis for Pakistan — Not a substitute for legal advice</div>
    <div class="footer-links">
        <span class="footer-link">Privacy</span>
        <span class="footer-link">Terms</span>
        <span class="footer-link">Contact</span>
    </div>
</div>
""", unsafe_allow_html=True)
