# AI for Legal Assistance & Access

AI-powered legal assistance application that helps users understand, compare, and navigate legal documents in a clear and accessible way.

## Problem
Legal information is often complex, difficult to understand, and challenging to navigate without professional guidance. Many people need help understanding obligations, risks, and key terms in contracts, policies, and agreements.

## Solution
This project provides a GenAI-powered assistant that:
- simplifies complex legal language into plain English
- extracts key clauses and obligations
- compares two legal documents or policies
- highlights risk areas, inconsistencies, and important terms
- generates checklists and questions for legal review
- helps users prepare for meaningful discussion with a legal professional

## Features
- Plain-English summaries of legal text
- Key clause extraction
- Agreement comparison
- Risk and inconsistency highlighting
- Actionable checklist generation
- Question preparation for legal consultation
- Local fallback analysis when no API key is provided

## Tech Stack
- Python
- Streamlit
- OpenAI / Azure OpenAI compatible API support
- Pytest

## Project Structure
```bash
legal-ai-assistant/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── legal_ai_assistant/
│   ├── __init__.py
│   └── legal_engine.py
└── tests/
    └── test_legal_engine.py

##Installation
git clone https://github.com/meghana-anupoju/AI-for-Legal-Assistance-Access.git
cd AI-for-Legal-Assistance-Access
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

Environment Variables
Create a .env file:
OPENAI_API_KEY=your_key_here
MODEL_NAME=gpt-4o-mini

If no API key is configured, the app still works in local analysis mode.

Disclaimer
This project is designed to provide general information and assistance for understanding legal documents. It does not replace professional legal advice and should not be used as a substitute for legal counsel.

License
MIT
