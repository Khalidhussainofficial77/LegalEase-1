import streamlit as st
from agents import agent_orchestrator
from fpdf import FPDF
from auth import sign_in, sign_up, sign_out, get_analyses_remaining, increment_analyses
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", "")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

.navbar {background: #0f172a; padding: 14px 32px; display: flex; align-items: center; justify-content: space-between;}
.logo-wrap {display: flex; align-items: center; gap: 10px;}
.logo-icon {width: 36px; height: 36px; background: #3b82f6; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px;}
.logo-name {font-size: 18px; font-weight: 700; color: white;}
.logo-tag {font-size: 10px; color: #94a3b8; margin-top: -2px;}
.nav-links {display: flex; gap: 8px; align-items: center;}
.nav-btn-ghost {font-size: 13px; color: #94a3b8; background: transparent; border: none; cursor: pointer; padding: 7px 14px; border-radius: 8px;}
.nav-btn-ghost:hover {background: #1e293b; color: white;}
.nav-btn-active {font-size: 13px; color: white; background: #1e293b; border: none; cursor: pointer; padding: 7px 14px; border-radius: 8px; font-weight: 500;}
.nav-btn-upgrade {font-size: 13px; color: white; background: #3b82f6; border: none; cursor: pointer; padding: 7px 14px; border-radius: 8px; font-weight: 600;}
.nav-user {font-size: 12px; color: #64748b; padding: 7px 14px;}

.hero {background: #0f172a; padding: 70px 40px 60px; text-align: center; border-bottom: 1px solid #1e293b;}
.hero-badge {display: inline-flex; align-items: center; gap: 6px; background: #1e3a5f; color: #60a5fa; font-size: 12px; font-weight: 600; padding: 5px 14px; border-radius: 20px; margin-bottom: 20px; border: 1px solid #2563eb33;}
.hero-title {font-size: 42px; font-weight: 800; color: white; line-height: 1.15; margin-bottom: 16px;}
.hero-title span {color: #60a5fa;}
.hero-sub {font-size: 16px; color: #94a3b8; max-width: 520px; margin: 0 auto 28px; line-height: 1.7;}
.hero-tags {display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 40px;}
.hero-tag {font-size: 12px; font-weight: 500; padding: 5px 14px; border-radius: 20px; border: 1px solid;}
.hero-tag-green {background: #052e16; color: #4ade80; border-color: #166534;}
.hero-tag-blue {background: #1e3a5f; color: #60a5fa; border-color: #1d4ed8;}
.hero-tag-yellow {background: #422006; color: #fbbf24; border-color: #92400e;}
.hero-stats {display: flex; justify-content: center; gap: 48px; background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 20px 32px; max-width: 560px; margin: 0 auto;}
.hero-stat-num {font-size: 26px; font-weight: 800; color: #60a5fa;}
.hero-stat-label {font-size: 11px; color: #64748b; margin-top: 3px;}

.section {padding: 56px 40px; border-bottom: 1px solid #e5e7eb; background: #ffffff;}
.section-label {font-size: 11px; font-weight: 700; color: #3b82f6; text-transform: uppercase; letter-spacing: 0.1em; text-align: center; margin-bottom: 8px;}
.section-title {font-size: 28px; font-weight: 700; color: #111827; text-align: center; margin-bottom: 10px;}
.section-sub {font-size: 15px; color: #6b7280; text-align: center; margin-bottom: 36px; max-width: 480px; margin-left: auto; margin-right: auto;}

.steps-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; max-width: 860px; margin: 0 auto;}
.step-card {background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 28px 22px; text-align: center;}
.step-num {width: 44px; height: 44px; background: #eff6ff; color: #1d4ed8; border-radius: 12px; font-size: 18px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px;}
.step-title {font-size: 15px; font-weight: 600; color: #111827; margin-bottom: 8px;}
.step-body {font-size: 13px; color: #6b7280; line-height: 1.6;}

.agents-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; max-width: 860px; margin: 0 auto;}
.agent-card {background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 22px 18px;}
.agent-icon {width: 42px; height: 42px; border-radius: 10px; font-size: 20px; display: flex; align-items: center; justify-content: center; margin-bottom: 14px;}
.agent-num {font-size: 10px; font-weight: 700; color: #9ca3af; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;}
.agent-title {font-size: 13px; font-weight: 600; color: #111827; margin-bottom: 6px;}
.agent-body {font-size: 12px; color: #6b7280; line-height: 1.5;}

.upload-section {background: #ffffff; padding: 48px 40px; border-bottom: 1px solid #e5e7eb;}
.upload-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; max-width: 760px; margin: 0 auto 24px;}
.upload-card {background: white; border: 2px dashed #d1d5db; border-radius: 14px; padding: 22px 16px; text-align: center;}
.upload-emoji {font-size: 28px; margin-bottom: 8px;}
.upload-name {font-size: 13px; font-weight: 600; color: #111827; margin-bottom: 3px;}
.upload-hint {font-size: 11px; color: #9ca3af;}
.free-bar {text-align: center; font-size: 13px; color: #6b7280; margin: 12px 0 4px;}
.free-bar span {font-weight: 700; color: #1d4ed8;}

.dash-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; max-width: 900px; margin: 0 auto 24px;}
.dash-card {background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 22px 20px;}
.dash-card-title {font-size: 12px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;}
.dash-card-val {font-size: 30px; font-weight: 800; color: #111827;}
.dash-card-sub {font-size: 12px; color: #9ca3af; margin-top: 4px;}
.dash-card.blue {border-top: 3px solid #3b82f6;}
.dash-card.green {border-top: 3px solid #22c55e;}
.dash-card.yellow {border-top: 3px solid #f59e0b;}
.dash-card.purple {border-top: 3px solid #a855f7;}

.history-item {background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px 20px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;}
.history-date {font-size: 12px; color: #9ca3af;}
.history-title {font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 3px;}
.history-meta {display: flex; gap: 8px; align-items: center;}
.history-badge {font-size: 11px; padding: 2px 8px; border-radius: 20px; font-weight: 600;}
.hb-high {background: #fee2e2; color: #dc2626;}
.hb-medium {background: #fef3c7; color: #d97706;}
.hb-low {background: #dcfce7; color: #16a34a;}

.metric-row {display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px;}
.metric-box {background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; text-align: center;}
.metric-val {font-size: 28px; font-weight: 700;}
.metric-lbl {font-size: 12px; color: #6b7280; margin-top: 3px;}

.clause-card {border-radius: 12px; padding: 16px 18px; margin-bottom: 10px; border-left: 4px solid;}
.clause-high {background: #fef2f2; border-color: #ef4444;}
.clause-medium {background: #fffbeb; border-color: #f59e0b;}
.clause-low {background: #f0fdf4; border-color: #22c55e;}
.clause-top {display: flex; align-items: center; gap: 10px; margin-bottom: 8px;}
.risk-pill {font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px;}
.pill-high {background: #fee2e2; color: #dc2626;}
.pill-medium {background: #fef3c7; color: #d97706;}
.pill-low {background: #dcfce7; color: #16a34a;}
.clause-num {font-size: 12px; font-weight: 600; color: #374151;}
.clause-text {font-size: 13px; color: #374151; line-height: 1.5; margin-bottom: 6px;}
.clause-reason {font-size: 12px; color: #6b7280; line-height: 1.4;}
.clause-urdu {font-size: 12px; color: #6b7280; margin-top: 4px; direction: rtl; text-align: right;}

.rewrite-card {background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px 18px; margin-bottom: 10px;}
.rewrite-top {display: flex; align-items: center; gap: 8px; margin-bottom: 12px;}
.rewrite-grid {display: grid; grid-template-columns: 1fr 1fr; gap: 12px;}
.rewrite-box {border-radius: 8px; padding: 12px; font-size: 13px; line-height: 1.5;}
.rewrite-bad {background: #fef2f2; color: #374151; border: 1px solid #fecaca;}
.rewrite-good {background: #f0fdf4; color: #374151; border: 1px solid #bbf7d0;}
.rewrite-label {font-size: 11px; font-weight: 700; margin-bottom: 6px;}
.rewrite-label-bad {color: #dc2626;}
.rewrite-label-good {color: #16a34a;}

.pricing-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; max-width: 780px; margin: 0 auto;}
.pricing-card {background: white; border: 1px solid #e5e7eb; border-radius: 16px; padding: 28px 22px;}
.pricing-card.featured {background: #0f172a; border: 2px solid #3b82f6;}
.pricing-badge {display: inline-block; font-size: 10px; font-weight: 700; padding: 3px 10px; border-radius: 20px; background: #dbeafe; color: #1d4ed8; margin-bottom: 12px;}
.pricing-badge.feat {background: #1e3a5f; color: #60a5fa;}
.pricing-name {font-size: 15px; font-weight: 600; color: #111827; margin-bottom: 6px;}
.pricing-name.white {color: white;}
.pricing-price {font-size: 30px; font-weight: 800; color: #111827;}
.pricing-price.white {color: white;}
.pricing-mo {font-size: 13px; color: #6b7280; margin-bottom: 16px;}
.pricing-mo.white {color: #94a3b8;}
.pricing-divider {border: none; border-top: 1px solid #e5e7eb; margin: 16px 0;}
.pricing-divider.dark {border-top-color: #1e293b;}
.pricing-feat {font-size: 13px; color: #374151; margin-bottom: 8px;}
.pricing-feat.white {color: #94a3b8;}
.pricing-btn {width: 100%; padding: 10px; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; margin-top: 16px; border: 1px solid #d1d5db; background: white; color: #1d4ed8;}
.pricing-btn.feat {background: #3b82f6; color: white; border: none;}

.payment-form {background: white; border: 1px solid #e5e7eb; border-radius: 16px; padding: 32px; max-width: 500px; margin: 0 auto;}
.payment-title {font-size: 22px; font-weight: 700; color: #111827; margin-bottom: 6px;}
.payment-sub {font-size: 13px; color: #6b7280; margin-bottom: 24px;}
.payment-plan {background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; padding: 14px 16px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;}
.payment-plan-name {font-size: 14px; font-weight: 600; color: #1d4ed8;}
.payment-plan-price {font-size: 18px; font-weight: 800; color: #1d4ed8;}

.footer {background: #0f172a; padding: 28px 40px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;}
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

# ── Session state ──
for key, default in [("user", None), ("email", None), ("plan", "free"),
                     ("analyses_used", 0), ("current_page", "home")]:
    if key not in st.session_state:
        st.session_state[key] = default

user = st.session_state.user

# ── NAVBAR ──
if user:
    st.markdown(f"""
    <div class="navbar">
        <div class="logo-wrap">
            <div class="logo-icon">⚖️</div>
            <div><div class="logo-name">LegalEase</div><div class="logo-tag">AI Contract Analysis</div></div>
        </div>
        <div class="nav-links">
            <span class="nav-user">👤 {st.session_state.email}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav1, nav2, nav3, nav4, nav5 = st.columns([2,1,1,1,1])
    with nav2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with nav3:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    with nav4:
        if st.button("📁 History", use_container_width=True):
            st.session_state.current_page = "history"
            st.rerun()
    with nav5:
        if st.button("⭐ Upgrade", use_container_width=True, type="primary"):
            st.session_state.current_page = "upgrade"
            st.rerun()

    _, signout_col = st.columns([5,1])
    with signout_col:
        if st.button("Sign out", use_container_width=True):
            sign_out()
            st.session_state.current_page = "home"
            st.rerun()
else:
    st.markdown("""
    <div class="navbar">
        <div class="logo-wrap">
            <div class="logo-icon">⚖️</div>
            <div><div class="logo-name">LegalEase</div><div class="logo-tag">AI Contract Analysis</div></div>
        </div>
        <div class="nav-links">
            <a class="nav-link" href="#how-it-works" style="font-size:13px;color:#94a3b8;">How it works</a>
            <a class="nav-link" href="#pricing" style="font-size:13px;color:#94a3b8;margin-left:20px;">Pricing</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.current_page

# ══════════════════════════════════════
# DASHBOARD PAGE
# ══════════════════════════════════════
if page == "dashboard" and user:
    remaining = get_analyses_remaining()
    plan = st.session_state.plan
    used = st.session_state.analyses_used

    st.markdown("""
    <div style="padding: 40px 40px 0;">
        <div style="font-size:24px;font-weight:700;color:#111827;margin-bottom:4px;">📊 Dashboard</div>
        <div style="font-size:14px;color:#6b7280;margin-bottom:28px;">Welcome back! Here's your account overview.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding: 0 40px;">
    <div class="dash-grid">
        <div class="dash-card blue">
            <div class="dash-card-title">Current Plan</div>
            <div class="dash-card-val" style="font-size:20px;">{plan.upper()}</div>
            <div class="dash-card-sub">{'Unlimited analyses' if plan != 'free' else 'Free tier'}</div>
        </div>
        <div class="dash-card green">
            <div class="dash-card-title">Analyses Remaining</div>
            <div class="dash-card-val" style="color:#16a34a;">{'∞' if plan != 'free' else remaining}</div>
            <div class="dash-card-sub">{'Resets monthly' if plan == 'free' else 'Unlimited'}</div>
        </div>
        <div class="dash-card yellow">
            <div class="dash-card-title">Analyses Used</div>
            <div class="dash-card-val" style="color:#d97706;">{used}</div>
            <div class="dash-card-sub">This month</div>
        </div>
        <div class="dash-card purple">
            <div class="dash-card-title">Account</div>
            <div class="dash-card-val" style="font-size:14px;margin-top:6px;">{st.session_state.email}</div>
            <div class="dash-card-sub">Verified</div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    if plan == "free":
        st.markdown("""
        <div style="padding: 20px 40px;">
            <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); border-radius: 16px; padding: 28px 32px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
                <div>
                    <div style="font-size: 18px; font-weight: 700; color: white; margin-bottom: 6px;">Upgrade to Pro</div>
                    <div style="font-size: 13px; color: #bfdbfe;">Get unlimited analyses, contract history and priority support for Rs. 999/month</div>
                </div>
                <div style="font-size: 24px; font-weight: 800; color: white;">Rs. 999/month</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⭐ Upgrade to Pro Now", use_container_width=True, type="primary"):
            st.session_state.current_page = "upgrade"
            st.rerun()

# ══════════════════════════════════════
# HISTORY PAGE
# ══════════════════════════════════════
elif page == "history" and user:
    st.markdown("""
    <div style="padding: 40px 40px 20px;">
        <div style="font-size:24px;font-weight:700;color:#111827;margin-bottom:4px;">📁 Contract History</div>
        <div style="font-size:14px;color:#6b7280;margin-bottom:28px;">Your past contract analyses.</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        user_id = str(st.session_state.user.id)
        history = supabase.table("contract_history").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()

        if history.data:
            st.markdown("<div style='padding: 0 40px;'>", unsafe_allow_html=True)
            for item in history.data:
                high = item.get("high_risk", 0)
                medium = item.get("medium_risk", 0)
                low = item.get("low_risk", 0)
                date = item.get("created_at", "")[:10]
                st.markdown(f"""
                <div class="history-item">
                    <div>
                        <div class="history-title">Contract analysed on {date}</div>
                        <div class="history-meta">
                            <span class="history-badge hb-high">🔴 {high} High</span>
                            <span class="history-badge hb-medium">🟡 {medium} Medium</span>
                            <span class="history-badge hb-low">🟢 {low} Low</span>
                        </div>
                    </div>
                    <div class="history-date">{date}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:60px;color:#6b7280;">
                <div style="font-size:48px;margin-bottom:16px;">📭</div>
                <div style="font-size:18px;font-weight:600;color:#111827;margin-bottom:8px;">No contracts yet</div>
                <div style="font-size:14px;">Analyse your first contract to see history here.</div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div style="text-align:center;padding:60px;color:#6b7280;">
            <div style="font-size:48px;margin-bottom:16px;">📭</div>
            <div style="font-size:18px;font-weight:600;color:#111827;margin-bottom:8px;">No contracts yet</div>
            <div style="font-size:14px;">Analyse your first contract to see history here.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════
# UPGRADE PAGE
# ══════════════════════════════════════
elif page == "upgrade" and user:
    st.markdown("""
    <div style="padding: 40px; background: #ffffff; min-height: 80vh;">
        <div style="font-size:24px;font-weight:700;color:#111827;margin-bottom:4px;text-align:center;">⭐ Upgrade to Pro</div>
        <div style="font-size:14px;color:#6b7280;margin-bottom:32px;text-align:center;">Get unlimited contract analyses for Rs. 999/month</div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        st.markdown("""
        <div class="payment-form">
            <div class="payment-title">Complete your upgrade</div>
            <div class="payment-sub">Fill in your details to upgrade to Pro</div>
            <div class="payment-plan">
                <div class="payment-plan-name">⭐ Pro Plan — Unlimited</div>
                <div class="payment-plan-price">Rs. 999/mo</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        full_name = st.text_input("Full name", placeholder="Muhammad Ali")
        phone = st.text_input("Phone number (JazzCash/Easypaisa)", placeholder="03XX-XXXXXXX")
        payment_method = st.selectbox("Payment method", ["JazzCash", "Easypaisa", "Bank Transfer"])

        st.markdown("""
        <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:12px 14px;margin:12px 0;font-size:13px;color:#92400e;">
            ⚠️ Online payment coming soon! After submitting we will contact you within 24 hours to complete payment manually.
        </div>
        """, unsafe_allow_html=True)

        if st.button("Submit Upgrade Request", use_container_width=True, type="primary"):
            if full_name and phone:
                st.success(f"✅ Request received! We'll contact you at {phone} within 24 hours to complete your upgrade to Pro.")
                st.info("📧 You can also email us at khalidhussainabbasi77@gmail.com")
            else:
                st.error("Please fill in all fields.")

# ══════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════
else:
    # HERO
    st.markdown("""
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

    # AUTH
    if not user:
        st.markdown("<div style='padding: 40px; background: #fffdf7; border-bottom: 1px solid #e5e7eb;'>", unsafe_allow_html=True)
        col_l, col_m, col_r = st.columns([1,2,1])
        with col_m:
            st.markdown("""
            <div style="background:white;border:1px solid #e5e7eb;border-radius:16px;padding:32px;">
                <div style="font-size:22px;font-weight:700;color:#111827;text-align:center;margin-bottom:6px;">⚖️ Get started free</div>
                <div style="font-size:13px;color:#6b7280;text-align:center;margin-bottom:24px;">Sign in or create an account to analyse contracts</div>
            </div>
            """, unsafe_allow_html=True)
            mode = st.radio("", ["Login", "Sign up"], horizontal=True, label_visibility="collapsed")
            email = st.text_input("Email address", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            if mode == "Login":
                if st.button("Login to LegalEase", use_container_width=True, type="primary"):
                    if email and password:
                        success, msg = sign_in(email, password)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Please enter email and password.")
            else:
                if st.button("Create free account", use_container_width=True, type="primary"):
                    if email and password:
                        if len(password) < 6:
                            st.error("Password must be at least 6 characters.")
                        else:
                            success, msg = sign_up(email, password)
                            if success:
                                st.success(msg)
                            else:
                                st.error(msg)
                    else:
                        st.error("Please enter email and password.")
        st.markdown("</div>", unsafe_allow_html=True)

    # HOW IT WORKS
    st.markdown("""
    <div id="how-it-works" class="section">
        <div class="section-label">The process</div>
        <div class="section-title">3 steps to a safe contract</div>
        <div class="section-sub">No legal knowledge needed. No lawyer fees. No waiting days.</div>
        <div class="steps-grid">
            <div class="step-card"><div class="step-num">1</div><div class="step-title">Upload your contract</div><div class="step-body">Upload a PDF, scan a printed contract with your phone camera, or paste the text directly.</div></div>
            <div class="step-card"><div class="step-num">2</div><div class="step-title">4 AI agents analyse it</div><div class="step-body">Agents check every clause against Pakistani law and flag HIGH, MEDIUM, or LOW risk in Urdu and English.</div></div>
            <div class="step-card"><div class="step-num">3</div><div class="step-title">Download safe contract</div><div class="step-body">Risky clauses are rewritten into fair versions. Download the fixed contract as a professional PDF.</div></div>
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
            <div class="agent-card"><div class="agent-icon" style="background:#ede9fe;">🧠</div><div class="agent-num">Agent 1</div><div class="agent-title">Orchestrator</div><div class="agent-body">The manager. Coordinates all agents and assembles the final report.</div></div>
            <div class="agent-card"><div class="agent-icon" style="background:#dbeafe;">📄</div><div class="agent-num">Agent 2</div><div class="agent-title">Document parser</div><div class="agent-body">Reads your PDF or image and splits it into individual clauses.</div></div>
            <div class="agent-card"><div class="agent-icon" style="background:#fee2e2;">⚠️</div><div class="agent-num">Agent 3</div><div class="agent-title">Clause analyser</div><div class="agent-body">Reviews each clause against Pakistani law. Flags risk in English and Urdu.</div></div>
            <div class="agent-card"><div class="agent-icon" style="background:#dcfce7;">✏️</div><div class="agent-num">Agent 4</div><div class="agent-title">Draft generator</div><div class="agent-body">Rewrites every risky clause into a fair balanced version.</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ANALYSE SECTION
    st.markdown("""
    <div id="analyse" class="upload-section">
        <div style="text-align:center;margin-bottom:28px;">
            <div class="section-label">Analyse your contract</div>
            <div class="section-title">Try it now</div>
            <div class="section-sub">Upload, scan, or paste your contract below.</div>
        </div>
        <div class="upload-grid">
            <div class="upload-card"><div class="upload-emoji">📄</div><div class="upload-name">Upload PDF</div><div class="upload-hint">Drop your contract PDF here</div></div>
            <div class="upload-card"><div class="upload-emoji">📷</div><div class="upload-name">Scan image</div><div class="upload-hint">Photo of a printed contract</div></div>
            <div class="upload-card"><div class="upload-emoji">✏️</div><div class="upload-name">Paste text</div><div class="upload-hint">Copy and paste clauses directly</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not user:
        st.markdown("""
        <div style="text-align:center;padding:40px;background:white;border-radius:14px;border:2px dashed #d1d5db;max-width:760px;margin:0 auto;">
            <div style="font-size:40px;margin-bottom:16px;">🔒</div>
            <div style="font-size:18px;font-weight:700;color:#111827;margin-bottom:8px;">Sign in to analyse contracts</div>
            <div style="font-size:14px;color:#6b7280;">Create a free account to get 3 analyses per month. Scroll up to sign in.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
        with col2:
            scanned_image = st.file_uploader("Scan image", type=["jpg","jpeg","png"], label_visibility="collapsed")
        with col3:
            raw_text = st.text_area("Paste text", height=100, placeholder="Paste any contract clauses here...", label_visibility="collapsed")

        remaining = get_analyses_remaining()
        plan = st.session_state.plan
        st.markdown(f"""
        <div class="free-bar">
            {'Unlimited analyses — Pro plan' if plan != 'free' else f'Free analyses remaining: <span>{remaining}/3</span>'}
        </div>
        """, unsafe_allow_html=True)

        run = st.button("🔍 Analyse Contract — 4 Agents", use_container_width=True, type="primary")

        if run:
            if not uploaded_file and not raw_text.strip() and not scanned_image:
                st.error("Please upload a PDF, scan an image, or paste contract text first.")
            elif get_analyses_remaining() <= 0:
                st.warning("You've used all 3 free analyses this month. Upgrade to Pro for unlimited analyses.")
                if st.button("⭐ Upgrade to Pro", type="primary"):
                    st.session_state.current_page = "upgrade"
                    st.rerun()
            else:
                increment_analyses()
                status_box = st.empty()
                progress = st.progress(0)
                step = [0]

                def update_status(msg):
                    step[0] += 25
                    status_box.info(f"⚙️ {msg}")
                    progress.progress(min(step[0], 100))

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

                    # Save to history
                    try:
                        supabase.table("contract_history").insert({
                            "user_id": str(st.session_state.user.id),
                            "high_risk": high,
                            "medium_risk": medium,
                            "low_risk": low,
                            "total_clauses": len(analysed)
                        }).execute()
                    except:
                        pass

                    st.markdown(f"""
                    <div style="max-width:860px;margin:16px auto;">
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
                            <div class="clause-top"><span class="risk-pill {pill}">{risk}</span><span class="clause-num">Clause {clause['clause_number']}</span></div>
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
                                <div class="rewrite-top"><span class="risk-pill {pill}">{r['risk']} RISK FIXED</span><span class="clause-num">Clause {r['clause_number']}</span></div>
                                <div class="rewrite-grid">
                                    <div class="rewrite-box rewrite-bad"><div class="rewrite-label rewrite-label-bad">❌ Original</div>{r['original']}</div>
                                    <div class="rewrite-box rewrite-good"><div class="rewrite-label rewrite-label-good">✅ Safe version</div>{r['safe_version']}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("### 📄 Download Safe Contract")
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_margins(20, 20, 20)
                        pdf.set_auto_page_break(auto=True, margin=20)
                        page_width = pdf.w - pdf.l_margin - pdf.r_margin
                        pdf.set_font("Helvetica", "B", 20)
                        pdf.cell(0, 12, "LegalEase - Safe Contract Draft", ln=True, align="C")
                        pdf.set_font("Helvetica", "I", 10)
                        pdf.cell(0, 8, "AI-powered contract analysis for Pakistan", ln=True, align="C")
                        pdf.ln(8)
                        for r in rewrites:
                            pdf.set_fill_color(254, 226, 226)
                            pdf.set_text_color(220, 38, 38)
                            pdf.set_font("Helvetica", "B", 10)
                            pdf.cell(0, 8, f"  Clause {r['clause_number']}  |  {r['risk']} RISK - Fixed", ln=True, fill=True)
                            pdf.set_text_color(0, 0, 0)
                            pdf.ln(3)
                            pdf.set_font("Helvetica", "I", 9)
                            pdf.set_text_color(107, 114, 128)
                            pdf.multi_cell(page_width, 6, f"Risk: {r['reason']}".encode('latin-1', 'replace').decode('latin-1'))
                            pdf.set_text_color(0, 0, 0)
                            pdf.ln(3)
                            pdf.set_font("Helvetica", "B", 10)
                            pdf.set_text_color(22, 163, 74)
                            pdf.cell(0, 7, "Safe Version:", ln=True)
                            pdf.set_text_color(0, 0, 0)
                            pdf.set_font("Helvetica", size=10)
                            safe = r["safe_version"].encode('latin-1', 'replace').decode('latin-1')
                            safe = ' '.join(safe.split())
                            pdf.multi_cell(page_width, 7, safe)
                            pdf.ln(6)
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
    <div id="pricing" class="section">
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
            <span class="footer-link" style="color:#60a5fa;">📧 khalidhussainabbasi77@gmail.com</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
