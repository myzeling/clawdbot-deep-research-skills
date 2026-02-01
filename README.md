# 🧠 Deep Research Skillset for Clawdbot

## 🤖 System Role & Purpose
**ATTENTION AGENT (Clawdbot/Opus):** This repository is your "External Research Cortex". It allows you to perform deep, evidence-based research without exhausting your own context window or rate limits.

**Your Goal:** Orchestrate the Python worker to gather data, then synthesize a professional, **citation-backed** report.

---

## 🛠️ Prerequisites
Before running, verify Environment Variables:
1. `TAVILY_API_KEY`: Required for search.
2. `GEMINI_API_KEY`: Required for reading (uses Gemini 1.5 Flash for cost-efficiency).

---

## 📜 Standard Operating Procedure (SOP)

When the user asks for **Deep Analysis**, **Company Reports**, or **Due Diligence**, follow this protocol strictly:

### Step 1: Strategy & Query Formulation
Analyze the request. To ensure **authority**, craft specific queries.
* **Standard:** `"Company X business model"`
* **Authoritative:** `"Company X 2025 annual report filetype:pdf financials"` (Adding `filetype:pdf` often yields official docs).

### Step 2: Execute the Worker
Run the script to gather raw data and generate a draft.

```bash
python worker.py --query "[YOUR_QUERY]" --filename "[OUTPUT.md]"
