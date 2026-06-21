from groq import Groq
import fitz
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def agent_document_parser(uploaded_file=None, raw_text=None):
    print("Agent 2 running...")
    if uploaded_file is not None:
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
    elif raw_text:
        text = raw_text
    else:
        return []
    chunks = re.split(r'\n{2,}|(?=\d+[\.\)])', text)
    clauses = [c.strip() for c in chunks if len(c.strip()) > 40]
    print(f"   Extracted {len(clauses)} clauses")
    return clauses

def agent_clause_analyser(clauses):
    print("Agent 3 running...")
    results = []
    for i, clause in enumerate(clauses[:10]):
        prompt = f"You are a legal assistant for Pakistani law. Analyze this contract clause and respond ONLY with a JSON object with these exact fields: clause_number, risk (HIGH/MEDIUM/LOW), reason, urdu_summary. Clause: {clause}"
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a legal assistant. Respond with valid JSON only. No markdown."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            raw = response.choices[0].message.content.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            match = re.search(r'\{.*?\}', raw, re.DOTALL)
            if match:
                raw = match.group()
            data = json.loads(raw)
            data["original"] = clause
            data["clause_number"] = i + 1
            if data.get("risk") not in ("HIGH", "MEDIUM", "LOW"):
                data["risk"] = "MEDIUM"
            results.append(data)
            print(f"   Clause {i+1}: {data.get('risk')} risk")
        except Exception as e:
            print(f"   Error clause {i+1}: {e}")
            results.append({
                "clause_number": i+1,
                "original": clause,
                "risk": "MEDIUM",
                "reason": "This clause needs careful review.",
                "urdu_summary": "اس شق کا غور سے جائزہ لیں۔"
            })
    return results

def agent_draft_generator(analysed_clauses):
    print("Agent 4 running...")
    risky = [c for c in analysed_clauses if c.get("risk") in ("HIGH", "MEDIUM")]
    rewrites = []
    for clause in risky:
        prompt = f"Rewrite this risky clause into a safer version for Pakistani law. Return ONLY the rewritten clause text. Original: {clause['original']}"
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Return only the rewritten clause text, nothing else."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.1
            )
            rewrites.append({
                "clause_number": clause["clause_number"],
                "original": clause["original"],
                "risk": clause["risk"],
                "reason": clause["reason"],
                "urdu_summary": clause["urdu_summary"],
                "safe_version": response.choices[0].message.content.strip()
            })
        except Exception as e:
            print(f"   Error rewriting: {e}")
    return rewrites

def agent_orchestrator(uploaded_file=None, raw_text=None, status_callback=None):
    print("Agent 1 (Orchestrator) starting...")
    if status_callback:
        status_callback("Agent 2: Parsing document...")
    clauses = agent_document_parser(uploaded_file, raw_text)
    if not clauses:
        return None, None
    if status_callback:
        status_callback("Agent 3: Analysing clauses...")
    analysed = agent_clause_analyser(clauses)
    if status_callback:
        status_callback("Agent 4: Drafting safer clauses...")
    rewrites = agent_draft_generator(analysed)
    if status_callback:
        status_callback("Done! Compiling report...")
    print("Pipeline complete!")
    return analysed, rewrites