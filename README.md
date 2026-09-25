# AI for Legal Assistance & Access

AI-powered legal assistance for understanding, simplifying, and comparing legal documents without replacing professional legal advice.

## Problem
Legal information is often complex, difficult to understand, and challenging to navigate without professional guidance. Many people need help understanding obligations, risks, and key terms in contracts, policies, and agreements.

## Solution
This project provides a GenAI-powered assistant that helps users by:
- simplifying complex legal language into plain English
- identifying important clauses and obligations
- comparing two legal documents or policies side by side
- highlighting risk areas, missing protections, and inconsistencies
- generating a checklist for legal review and next actions
- preparing questions for a legal professional
- working in a local fallback mode when no API key is supplied

## Key Features
- Plain-English summaries of legal text
- Key clause extraction
- Agreement comparison
- Risk and inconsistency highlighting
- Actionable checklist generation
- Question preparation for legal consultation
- PDF and text file support for uploaded documents
- Optional AI-powered legal analysis with a local fallback mode

## Tech Stack
- Python
- Streamlit
- OpenAI / Azure OpenAI compatible API support
- PyPDF
- Pytest

## Example Scenario
A user uploads a SaaS agreement or vendor policy and receives:
- a plain-English summary
- a list of obligations and risk clauses
- a risk score for the document
- a comparison against another agreement
- suggested follow-up questions for a lawyer

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
```

## Run Locally
```bash
git clone https://github.com/meghana-anupoju/AI-for-Legal-Assistance-Access.git
cd AI-for-Legal-Assistance-Access
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Environment Variables
Create a `.env` file with:

```env
OPENAI_API_KEY=your_key_here
MODEL_NAME=gpt-4o-mini
```

If no API key is configured, the app still works in local analysis mode.

## Disclaimer
This project is designed to provide general information and assistance for understanding legal documents. It does not replace professional legal advice and should not be used as a substitute for legal counsel.

## License
MIT
