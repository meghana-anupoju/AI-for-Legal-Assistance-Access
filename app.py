import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from legal_ai_assistant.legal_engine import (
    analyze_legal_document,
    assess_document_risk,
    compare_documents,
    create_checklist,
    extract_key_clauses,
    extract_text_from_file,
)

load_dotenv()

st.set_page_config(page_title="Legal AI Assistant", page_icon="⚖️", layout="wide")

st.title("⚖️ Legal AI Assistant")
st.caption("GenAI-powered support for understanding legal documents, comparing terms, and preparing for legal review.")

with st.sidebar:
    st.header("Options")
    st.markdown("This tool provides general information and summaries for educational purposes, not legal advice.")
    use_advanced = st.toggle("Use advanced AI mode", value=False, help="Enable conversational AI review when a valid API key is provided.")
    env_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input(
        "OpenAI API key (optional)",
        type="password",
        value=env_key,
        help="Leave this blank to use the secure local fallback analysis mode.",
    )

st.subheader("1) Upload or paste a legal document")
uploaded_file = st.file_uploader("Upload text or PDF document", type=["txt", "md", "csv", "json", "pdf"], help="Upload a contract, policy, or legal file for summary and risk review.")
legal_text = st.text_area(
    "Legal document text",
    height=240,
    placeholder="Paste agreement terms, policy language, terms of service, or contract clauses here...",
    help="Add the text to review, or upload a document above.",
)

if uploaded_file is not None:
    uploaded_bytes = uploaded_file.read()
    if uploaded_file.name.lower().endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(uploaded_bytes)
            temp_path = temp_file.name
        try:
            legal_text = extract_text_from_file(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        legal_text = uploaded_bytes.decode("utf-8", errors="ignore")

if legal_text:
    analysis = analyze_legal_document(legal_text, api_key=api_key if use_advanced else "")

    st.subheader("Document summary")
    st.write(analysis["summary"])

    if analysis.get("source") == "ai-analysis":
        st.success("AI-assisted legal analysis was used.")
    else:
        st.info("Local legal analysis was used because no API key was configured or AI mode was not enabled.")

    st.subheader("Key clauses")
    clauses = analysis.get("key_clauses") or extract_key_clauses(legal_text)
    for clause in clauses:
        with st.expander(clause["title"]):
            st.write(clause["summary"])

    st.subheader("Action checklist")
    checklist = analysis.get("checklist") or create_checklist(legal_text)
    for item in checklist:
        st.markdown(f"- {item}")

    st.subheader("Risk highlights")
    for item in analysis.get("highlights", []):
        st.markdown(f"- {item}")

    risk = assess_document_risk(legal_text)
    st.subheader("Document risk score")
    st.write(f"Risk score: {risk['score']}/100 | Level: {risk['level']}")
    for item in risk["risks"]:
        st.markdown(f"- {item}")

st.subheader("2) Compare two legal documents")
col1, col2 = st.columns(2)
with col1:
    doc_a = st.text_area("Document A", height=180, placeholder="Paste first agreement or policy...")
with col2:
    doc_b = st.text_area("Document B", height=180, placeholder="Paste second agreement or policy...")

if doc_a and doc_b:
    comparison = compare_documents(doc_a, doc_b)
    st.subheader("Comparison result")
    st.write(comparison["status"])
    st.write(f"Risk level: {comparison['risk_level']}")

    st.markdown("### Highlights")
    for item in comparison["highlights"]:
        st.markdown(f"- {item}")

    st.markdown("### Potential issues to review")
    for clause in comparison["document_a_key_clauses"][:3]:
        st.markdown(f"- A: {clause['title']}")
    for clause in comparison["document_b_key_clauses"][:3]:
        st.markdown(f"- B: {clause['title']}")

st.subheader("3) Prepare for a legal professional")
question_prompt = st.text_area(
    "Add context about your situation",
    height=120,
    placeholder="Example: I am reviewing a SaaS agreement and want to ask about liability limits, data use, and termination rights.",
)

if question_prompt:
    st.markdown("### Suggested questions")
    suggested = [
        "What are the most important risks in this document for my situation?",
        "Which clauses should I negotiate or clarify before signing?",
        "Are there any obligations, liabilities, or termination rights I should pay close attention to?",
        "What documentation or supporting information should I prepare before speaking with counsel?",
    ]
    for item in suggested:
        st.markdown(f"- {item}")

    if question_prompt:
        st.write(f"Context: {question_prompt}")

st.markdown("---")
st.info("This tool is not a substitute for legal advice. It provides educational summaries and structured guidance only.")
