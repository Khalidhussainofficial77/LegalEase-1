import streamlit as st
from agents import agent_orchestrator
from fpdf import FPDF
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="LegalEase Agent", page_icon="⚖️", layout="wide")
st.markdown("## ⚖️ LegalEase Agent")
st.markdown("*AI-powered contract analysis for freelancers, tenants and SMEs in Pakistan*")
st.markdown("**4 Agents:** Orchestrator → Document Parser → Clause Analyser → Draft Generator")
st.divider()

# ─── SAMPLE CONTRACT ───────────────────────────────────────────────────────────
SAMPLE_CONTRACT = """EMPLOYMENT CONTRACT

1. The employer may terminate this contract at any time without notice, reason, or compensation.

2. The employee shall work a minimum of 12 hours per day, 7 days a week, with no overtime pay.

3. Any disputes arising from this contract shall be final and cannot be challenged in any court of law.

4. The employee must give 3 months notice before resigning but the company may terminate the employee immediately without any notice period or reason.

5. The employer owns all work, ideas, and inventions created by the employee, even outside working hours and after employment ends.

6. The employee agrees to a non-compete clause for 10 years after leaving, covering all industries worldwide."""

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "contract_text" not in st.session_state:
    st.session_state.contract_text = ""
if "analysed" not in st.session_state:
    st.session_state.analysed = None
if "rewrites" not in st.session_state:
    st.session_state.rewrites = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─── INPUT SECTION ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("### 📄 Upload Contract PDF")
    uploaded_file = st.file_uploader("Upload a PDF contract", type=["pdf"])

with col2:
    st.markdown("### 📷 Scan Contract Image")
    scanned_image = st.file_uploader("Upload photo of contract", type=["jpg", "jpeg", "png"])

with col3:
    st.markdown("### ✏️ Or Paste Contract Text")

    # Sample contract button
    if st.button("📋 Load Sample Contract", use_container_width=True):
        st.session_state.contract_text = SAMPLE_CONTRACT

    raw_text = st.text_area(
        "Paste contract text here",
        height=200,
        value=st.session_state.contract_text,
        placeholder="Paste any contract clauses here, or click 'Load Sample Contract' above...",
        key="raw_text_input"
    )

st.divider()
run = st.button("🔍 Analyse Contract (4 Agents)", use_container_width=True, type="primary")

# ─── ANALYSIS ──────────────────────────────────────────────────────────────────
if run:
    if not uploaded_file and not raw_text.strip() and not scanned_image:
        st.error("Please upload a PDF, scan an image, or paste contract text first.")
    else:
        status_box = st.empty()
        progress = st.progress(0)
        step = [0]

        def update_status(msg):
            step[0] += 25
            status_box.info(f"Running: {msg}")
            progress.progress(min(step[0], 100))

        if scanned_image:
            status_box.info("Processing scanned image...")
            st.info("✅ Image received! For best results paste the contract text directly.")

        with st.spinner("Running 4-agent pipeline..."):
            analysed, rewrites = agent_orchestrator(
                uploaded_file=uploaded_file if uploaded_file else None,
                raw_text=raw_text if raw_text.strip() else None,
                status_callback=update_status
            )

        progress.progress(100)
        status_box.success("✅ All 4 agents completed!")

        # Save to session state for chatbot
        st.session_state.analysed = analysed
        st.session_state.rewrites = rewrites
        st.session_state.chat_history = []  # reset chat on new analysis

# ─── RESULTS ───────────────────────────────────────────────────────────────────
if st.session_state.analysed:
    analysed = st.session_state.analysed
    rewrites = st.session_state.rewrites

    if not analysed:
        st.error("Could not extract clauses. Please check your input.")
    else:
        high   = sum(1 for c in analysed if c.get("risk") == "HIGH")
        medium = sum(1 for c in analysed if c.get("risk") == "MEDIUM")
        low    = sum(1 for c in analysed if c.get("risk") == "LOW")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Clauses", len(analysed))
        m2.metric("🔴 High Risk", high)
        m3.metric("🟡 Medium Risk", medium)
        m4.metric("🟢 Low Risk", low)

        st.divider()
        st.markdown("### 📋 Clause Analysis — Agent 3 Output")
        for clause in analysed:
            risk = clause.get("risk", "LOW")
            icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(risk, "🟢")
            with st.expander(f"{icon} Clause {clause['clause_number']} — {risk} RISK"):
                st.markdown("**Original Clause:**")
                st.info(clause['original'])
                st.markdown(f"**⚠️ Risk Reason:** {clause['reason']}")
                st.markdown(f"**اردو:** {clause['urdu_summary']}")

        if rewrites:
            st.divider()
            st.markdown("### ✏️ Safe Contract Draft — Agent 4 Output")
            for r in rewrites:
                icon = "🔴" if r.get("risk") == "HIGH" else "🟡"
                with st.expander(f"{icon} Clause {r['clause_number']} — Rewritten ({r['risk']} risk fixed)"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**❌ Original (Risky)**")
                        st.error(r["original"])
                    with col_b:
                        st.markdown("**✅ Safe Version**")
                        st.success(r["safe_version"])

            # ─── PDF DOWNLOAD ───────────────────────────────────────────────
            st.divider()
            st.markdown("### 📄 Download Safe Contract")

            pdf = FPDF()
            pdf.set_margins(20, 20, 20)
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=20)

            # Title
            pdf.set_font("Helvetica", "B", 18)
            pdf.cell(0, 14, "LegalEase - Safe Contract Draft", ln=True, align="C")
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 8, "AI-powered contract analysis for Pakistan", ln=True, align="C")
            pdf.ln(8)

            for r in rewrites:
                # Clause header with grey background
                pdf.set_fill_color(230, 230, 230)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Helvetica", "B", 11)
                title = f"Clause {r['clause_number']} | {r['risk']} RISK - Fixed"
                pdf.multi_cell(
                    0, 10,
                    title.encode('latin-1', 'replace').decode('latin-1'),
                    fill=True
                )
                pdf.ln(3)

                # Risk reason in italic
                pdf.set_font("Helvetica", "I", 9)
                reason = f"Risk: {r['reason']}"
                pdf.multi_cell(
                    0, 6,
                    reason.encode('latin-1', 'replace').decode('latin-1')
                )
                pdf.ln(3)

                # Original clause label
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_text_color(150, 0, 0)
                pdf.multi_cell(0, 6, "Original Clause (Risky):")
                pdf.set_font("Helvetica", size=9)
                pdf.set_text_color(80, 80, 80)
                original_clean = r.get("original", "").encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 6, original_clean)
                pdf.ln(3)

                # Safe version label in green
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(0, 120, 0)
                pdf.multi_cell(0, 6, "Safe Version:")

                # Safe version text in black
                pdf.set_font("Helvetica", size=10)
                pdf.set_text_color(0, 0, 0)
                safe_text = r.get("safe_version", "").encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 7, safe_text)
                pdf.ln(4)

                # Divider line
                pdf.set_draw_color(180, 180, 180)
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(6)

            pdf_bytes = pdf.output()
            st.download_button(
                "📄 Download Safe Contract PDF",
                data=bytes(pdf_bytes),
                file_name="legalease_safe_contract.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.success("✅ No risky clauses found — your contract looks safe!")

        # ─── CHATBOT ───────────────────────────────────────────────────────
        st.divider()
        st.markdown("### 💬 Ask LegalEase — Chat About Your Contract")
        st.caption("Ask anything about your contract — in English or Urdu")

        # Build contract context for chatbot
        contract_context = "Here is the analysed contract:\n\n"
        for clause in analysed:
            contract_context += f"Clause {clause['clause_number']} ({clause['risk']} RISK): {clause['original']}\nReason: {clause['reason']}\nUrdu: {clause['urdu_summary']}\n\n"

        if rewrites:
            contract_context += "\nSafe rewrites:\n"
            for r in rewrites:
                contract_context += f"Clause {r['clause_number']} safe version: {r['safe_version']}\n\n"

        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        user_question = st.chat_input("Ask about your contract e.g. 'Is clause 3 safe to sign?' or 'اردو میں سمجھائیں'")

        if user_question:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {
                                    "role": "system",
                                    "content": f"""You are LegalEase, an AI legal assistant for Pakistani law. 
You help freelancers, tenants, and SMEs understand their contracts.
Answer in the same language the user asks (English or Urdu).
Be clear, simple, and helpful. Never give definitive legal advice — always suggest consulting a lawyer for serious matters.

{contract_context}"""
                                },
                                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                            ],
                            max_tokens=500,
                            temperature=0.3
                        )
                        reply = response.choices[0].message.content.strip()
                        st.markdown(reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"Chat error: {e}")

st.divider()
st.caption("⚖️ LegalEase Agent — AI-powered contract analysis for Pakistan")
