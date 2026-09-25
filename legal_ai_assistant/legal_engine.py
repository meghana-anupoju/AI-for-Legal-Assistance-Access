import os
import re
from typing import Dict, List, Any

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


def sanitize_document_text(text: str) -> str:
    if text is None:
        return ""

    cleaned = str(text).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.replace("\x00", "")
    return cleaned.strip()


def validate_api_key(api_key: str) -> bool:
    if api_key is None:
        return False

    key = str(api_key).strip()
    if not key:
        return False
    if any(ch.isspace() for ch in key):
        return False
    if key.startswith("sk-") and len(key) >= 16:
        return True
    if key.startswith("gpt-") and len(key) >= 16:
        return True
    return False


def _fallback_law_analysis(text: str) -> Dict[str, Any]:
    summary = generate_summary(text)
    clauses = extract_key_clauses(text)
    checklist = create_checklist(text)
    highlights = [
        "Review payment, termination, and confidentiality clauses closely.",
        "Confirm whether the document creates enforceable obligations or risk for the user.",
        "Ask a qualified legal professional to validate any critical commercial or regulatory terms.",
    ]

    return {
        "summary": summary,
        "key_clauses": clauses,
        "checklist": checklist,
        "highlights": highlights,
        "risk_level": "Medium",
        "source": "local-analysis",
    }


def extract_text_from_file(file_path: str) -> str:
    if not file_path:
        return ""

    lower_path = file_path.lower()

    try:
        if lower_path.endswith(".pdf"):
            try:
                from pypdf import PdfReader
            except ImportError:
                return "PDF support is unavailable because the required dependency is not installed."

            try:
                reader = PdfReader(file_path)
                pages = []
                for page in reader.pages:
                    text = page.extract_text() or ""
                    pages.append(text)
                return "\n".join(pages)
            except Exception:
                return "Unable to read PDF text. Please ensure the file is a valid PDF."

        if lower_path.endswith((".txt", ".md", ".csv", ".json")):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        return "Unsupported file format. Please upload a text-based document."
    except Exception:
        return "Unable to read file. Please check the file path and format."


def analyze_legal_document(text: str, api_key: str = "") -> Dict[str, Any]:
    cleaned_text = sanitize_document_text(text)
    if not cleaned_text:
        return {
            "summary": "No document content provided.",
            "key_clauses": [],
            "checklist": [],
            "highlights": [],
            "risk_level": "Low",
            "source": "local-analysis",
        }

    resolved_api_key = (api_key or os.getenv("OPENAI_API_KEY", "")).strip()
    if validate_api_key(resolved_api_key) and OpenAI is not None:
        try:
            client = OpenAI(api_key=resolved_api_key)
            response = client.responses.create(
                model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
                input=[
                    {
                        "role": "system",
                        "content": "You are a legal analysis assistant. Provide a plain-English summary, identify material clauses, highlight risks, and note that this is not legal advice.",
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this legal document and return JSON with keys: summary, key_clauses, checklist, highlights, risk_level. Document: {cleaned_text}",
                    },
                ],
            )
            content = response.output_text.strip()
            if content:
                return {
                    "summary": content,
                    "key_clauses": extract_key_clauses(cleaned_text),
                    "checklist": create_checklist(cleaned_text),
                    "highlights": ["AI-assisted review completed.", "Confirm any critical terms with a legal professional before acting."],
                    "risk_level": "Medium",
                    "source": "ai-analysis",
                }
        except Exception:
            pass

    return _fallback_law_analysis(cleaned_text)


def extract_key_clauses(text: str) -> List[Dict[str, str]]:
    cleaned_text = sanitize_document_text(text)
    if not cleaned_text:
        return []

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned_text) if s.strip()]
    clauses: List[Dict[str, str]] = []

    for sentence in sentences:
        lowered = sentence.lower()
        if any(keyword in lowered for keyword in [
            "shall",
            "must",
            "may",
            "liability",
            "termination",
            "confidential",
            "payment",
            "notice",
            "indemn",
            "warranty",
            "governing",
            "jurisdiction",
            "breach",
        ]):
            title = sentence[:60].strip()
            if not title.endswith((".", ":")):
                title = title + "."
            summary = "This clause establishes a legal obligation, right, or limitation that should be reviewed carefully."
            clauses.append({"title": title, "summary": summary})

    if not clauses:
        clauses.append({
            "title": "Document overview",
            "summary": "The document appears to be general legal text and may require professional review for specific legal implications.",
        })

    return clauses[:8]


def generate_summary(text: str) -> str:
    cleaned_text = sanitize_document_text(text)
    if not cleaned_text:
        return "No document content provided. Please upload or paste legal text to analyze."

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned_text) if s.strip()]
    key_points = []

    for sentence in sentences:
        lowered = sentence.lower()
        if any(keyword in lowered for keyword in [
            "payment",
            "fee",
            "termination",
            "terminated",
            "breach",
            "confidential",
            "liability",
            "indemn",
            "notice",
            "support",
            "warranty",
            "governing",
            "subscription",
            "software",
            "agreement",
            "contract",
        ]):
            key_points.append(sentence)

    if not key_points:
        key_points = sentences[:3]

    context_sentence = sentences[0]
    if len(context_sentence) > 180:
        context_sentence = context_sentence[:180].rstrip() + "..."

    emphasis = key_points[:3]
    if emphasis:
        summary_text = "; ".join(emphasis)
    else:
        summary_text = context_sentence

    summary = (
        f"This document concerns the terms and obligations described in: {context_sentence} "
        f"The most important issues include payment obligations, termination rights, and support requirements, as reflected in {summary_text}. "
        "It is recommended that the user review these terms with a qualified legal professional before acting on them."
    )
    return summary


def compare_documents(doc_a: str, doc_b: str) -> Dict[str, Any]:
    left_doc = sanitize_document_text(doc_a)
    right_doc = sanitize_document_text(doc_b)
    a_clauses = extract_key_clauses(left_doc)
    b_clauses = extract_key_clauses(right_doc)

    if len(a_clauses) == 0 or len(b_clauses) == 0:
        return {
            "status": "No comparison available",
            "highlights": [],
            "risk_level": "Low",
        }

    risk_level = "Medium"
    if any("liability" in clause["title"].lower() for clause in a_clauses + b_clauses) or any("termination" in clause["title"].lower() for clause in a_clauses + b_clauses):
        risk_level = "High"

    highlights = [
        "Different documents may impose different notice periods or termination rights.",
        "Check whether confidentiality and liability protections are aligned across both documents.",
        "Review any inconsistency before signing or relying on either document.",
    ]

    status = "Documents are somewhat aligned but contain important differences that merit review."
    if doc_a == doc_b:
        status = "Documents appear aligned in meaning and structure."

    return {
        "status": status,
        "highlights": highlights,
        "risk_level": risk_level,
        "document_a_key_clauses": a_clauses,
        "document_b_key_clauses": b_clauses,
    }


def assess_document_risk(text: str) -> Dict[str, Any]:
    cleaned_text = sanitize_document_text(text)
    if not cleaned_text:
        return {
            "score": 0,
            "level": "Low",
            "risks": ["No document content was provided for review."],
        }

    lowered = cleaned_text.lower()
    factors = {
        "liability": "High liability exposure or uncapped damages" if "liability" in lowered or "damages" in lowered else None,
        "termination": "Termination rights without sufficient notice" if "termination" in lowered or "terminate" in lowered else None,
        "indemnity": "Indemnity obligations may create significant risk" if "indemn" in lowered else None,
        "confidentiality": "Confidentiality obligations must be reviewed carefully" if "confidential" in lowered else None,
        "payment": "Payment and fee obligations may affect commercial risk" if "payment" in lowered or "fee" in lowered else None,
    }

    score = 0
    risks = []
    for key, message in factors.items():
        if message:
            risks.append(message)
            score += 15

    if "no notice" in lowered or "without notice" in lowered:
        score += 15
        risks.append("Notice obligations are missing or weak.")

    if "all damages" in lowered or "liable for all damages" in lowered or "caps indemnity at zero" in lowered:
        score += 15
        risks.append("The contract creates unusually severe exposure for damages or indemnity.")

    if any(word in lowered for word in ["must", "shall", "required", "mandatory"]):
        score += 10

    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    return {
        "score": min(score, 100),
        "level": level,
        "risks": risks[:5] if risks else ["No obvious high-risk patterns were detected in the provided text."],
    }


def create_checklist(text: str) -> List[str]:
    cleaned_text = sanitize_document_text(text)
    checklist = [
        "Review key payment, liability, and termination provisions.",
        "Confirm any confidentiality and notice obligations are clear.",
        "Identify any unresolved risks or missing protections.",
        "Prepare questions for a legal professional before signing.",
    ]

    lowered_text = cleaned_text.lower()
    if "indemn" in lowered_text:
        checklist.insert(0, "Confirm indemnification scope and any caps or exceptions.")
    if "governing" in lowered_text or "jurisdiction" in lowered_text:
        checklist.insert(1, "Check governing law and venue terms.")

    return checklist
