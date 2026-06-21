

import streamlit as st
from agents import agent_orchestrator
from fpdf import FPDF

st.set_page_config(page_title="LegalEase Agent", page_icon="⚖️", layout="wide")
st.markdown("## ⚖️ LegalEase Agent")
st.markdown("*AI-powered contract analysis for freelancers, tenants and SMEs in Pakistan*")
st.markdown("**4 Agents:** Orchestrator → Document Parser → Clause Analyser → Draft Generator")
st.divider()

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("### 📄 Upload Contract PDF")
    uploaded_file = st.file_uploader("Upload a PDF contract", type=["pdf"])
with col2:
    st.markdown("### 📷 Scan Contract Image")
    scanned_image = st.file_uploader("Upload photo of contract", type=["jpg", "jpeg", "png"])
with col3:
    st.markdown("### ✏️ Or Paste Contract Text")
    raw_text = st.text_area("Paste contract text here", height=200,
                            placeholder="Paste any contract clauses here...")

st.divider()
run = st.button("🔍 Analyse Contract (4 Agents)", use_container_width=True, type="primary")

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

        # Process scanned image if uploaded
        if scanned_image:
            import pytesseract
            from PIL import Image
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            status_box.info("Scanning image and extracting text...")
            image = Image.open(scanned_image)
            extracted_text = pytesseract.image_to_string(image)
            st.info(f"✅ Scanned text extracted: {len(extracted_text)} characters")
            if not raw_text.strip():
                raw_text = extracted_text

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

                st.divider()
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
                    reason = f"Risk: {r['reason']}"
                    pdf.multi_cell(180, 6, reason.encode('latin-1', 'replace').decode('latin-1'))
                    pdf.ln(2)
                    pdf.set_font("Helvetica", "B", 9)
                    pdf.multi_cell(180, 6, "Safe Version:")
                    pdf.set_font("Helvetica", size=10)
                    safe_text = r["safe_version"].encode('latin-1', 'replace').decode('latin-1')
                    pdf.multi_cell(180, 7, safe_text)
                    pdf.ln(5)
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

st.divider()
st.caption("⚖️ LegalEase Agent — AI-powered contract analysis for Pakistan — Powered by Groq AI")
