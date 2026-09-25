# Legal AI Assistant

A GenAI-powered legal assistance app designed to help users understand, compare, and navigate legal documents without replacing professional legal advice.

## Features

- Simplify dense legal language into plain-English summaries
- Extract key clauses, rights, obligations, and deadlines
- Compare two contracts or policy documents side by side
- Highlight risk areas, inconsistencies, and missing protections
- Generate a practical next-step checklist for legal review
- Help users prepare questions for a legal professional

## Tech stack

- Python
- Streamlit
- Optional Azure OpenAI or OpenAI API integration
- Rule-based legal analysis fallback for local use

## Run locally

```bash
cd legal-ai-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Environment variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_key_here
MODEL_NAME=gpt-4o-mini
```

If no API key is present, the app still works in a local analysis mode.
