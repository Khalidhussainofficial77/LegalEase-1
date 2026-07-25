# LegalEase — AI-Powered Legal Contract Analyser 🇵🇰⚖️

> What used to cost Rs. 15,000 and 3 days now takes 10 seconds and is free.

## 🔗 Live App
**[https://legalease-1-j7mhqwoignxzg9oxwjuksp.streamlit.app](https://legalease-1-j7mhqwoignxzg9oxwjuksp.streamlit.app)**

---

## 📌 The Problem It Solves

In Pakistan, millions of workers, freelancers, and small business owners sign employment and commercial contracts without understanding what they contain. Legal review costs Rs. 10,000–20,000 and takes days — putting justice out of reach for most people.

**LegalEase solves this.** Paste or upload any contract, and in 10 seconds our 4-agent AI pipeline detects risky clauses, explains each one in plain English AND Urdu, rewrites them into safer versions, and lets you download the fixed contract as a PDF — completely free.

---

## ✨ Features

- 📄 **PDF upload or paste raw text** — flexible input
- 🔍 **AI clause extraction** — automatically splits contract into individual clauses
- 🚨 **Risk detection** — flags each clause as HIGH / MEDIUM / LOW risk
- 🧠 **Plain English explanation** — tells you exactly why a clause is dangerous
- 🇵🇰 **Urdu summaries** — accessible to non-English speakers
- ✍️ **Safe clause rewrites** — AI rewrites risky clauses into fair, balanced versions
- 📥 **PDF download** — download the full analysis report
- ⚡ **10-second analysis** — powered by Llama 3.3 70B via Groq

---

## 🤖 The AI Feature — 4-Agent Pipeline

LegalEase uses a **multi-agent architecture** where each agent has a specific role:

| Agent | Role |
|-------|------|
| Agent 1 — Orchestrator | Coordinates the full pipeline and manages status updates |
| Agent 2 — Document Parser | Extracts and chunks clauses from PDF or raw text |
| Agent 3 — Clause Analyser | Analyses each clause for risk level with Urdu summary |
| Agent 4 — Draft Generator | Rewrites HIGH and MEDIUM risk clauses into safer versions |

### System Prompt (Agent 3 — Clause Analyser)

You are a legal assistant for Pakistani law. Analyze this contract clause
and respond ONLY with a JSON object with these exact fields:
clause_number, risk (HIGH/MEDIUM/LOW), reason, urdu_summary.


### System Prompt (Agent 4 — Draft Generator)

Rewrite this risky clause into a safer version for Pakistani law.
Return ONLY the rewritten clause text, nothing else.


---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web app framework |
| Groq API | LLM inference (fast & free) |
| Llama 3.3 70B | AI model for clause analysis |
| PyMuPDF (fitz) | PDF text extraction |
| python-dotenv | Secure API key management |

---

## 📸 Screenshots

![Home Screen](https://raw.githubusercontent.com/Khalidhussainofficial77/LegalEase-1/main/home.png)

![Risk Analysis](https://raw.githubusercontent.com/Khalidhussainofficial77/LegalEase-1/main/analysis.png)

![Safe Draft](https://raw.githubusercontent.com/Khalidhussainofficial77/LegalEase-1/main/draft.png)

---

## 🚀 How to Run

1. Clone the repo:
```bash
git clone https://github.com/Khalidhussainofficial77/LegalEase-1.git
cd LegalEase-1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:

GROQ_API_KEY=your_groq_api_key_here


4. Run the app:
```bash
streamlit run app.py
```

---

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key from [console.groq.com](https://console.groq.com) |

**Never commit your API key.** Add `.env` to `.gitignore`.

---

## 👤 Author

**Khalid Hussain**
Built for the ACT AI Final Project — July 2026
