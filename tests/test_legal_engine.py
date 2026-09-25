import pytest

from legal_ai_assistant.legal_engine import (
    extract_key_clauses,
    generate_summary,
    compare_documents,
    analyze_legal_document,
    extract_text_from_file,
)


def test_extract_key_clauses_returns_actionable_highlights():
    text = """
    1. Termination. Either party may terminate this agreement for material breach.
    2. Confidentiality. The Vendor shall keep all client data confidential.
    3. Limitation of Liability. The Supplier's liability is capped at $50,000.
    """

    result = extract_key_clauses(text)

    assert len(result) >= 3
    assert any("Termination" in clause["title"] for clause in result)
    assert any("Confidentiality" in clause["title"] for clause in result)
    assert all("summary" in clause for clause in result)


def test_generate_summary_is_short_and_contains_key_points():
    text = """
    This agreement governs a software subscription. The customer pays annual fees.
    The supplier must provide support. The agreement can be terminated for non-payment.
    """

    summary = generate_summary(text)

    assert isinstance(summary, str)
    assert len(summary) > 50
    assert "software" in summary.lower()
    assert "termination" in summary.lower()


def test_compare_documents_reveals_risk_and_alignment():
    doc_a = "The company may terminate for material breach and must provide 30 days notice."
    doc_b = "The company may terminate for convenience with no notice and no obligation to provide support."

    comparison = compare_documents(doc_a, doc_b)

    assert "aligned" in comparison["status"].lower() or "different" in comparison["status"].lower()
    assert comparison["highlights"]
    assert "risk" in comparison["risk_level"].lower() or "medium" in comparison["risk_level"].lower() or "low" in comparison["risk_level"].lower()


def test_analyze_legal_document_works_without_api_key():
    result = analyze_legal_document(
        "This agreement requires annual payment and permits termination for non-payment. Confidential information must be protected.",
        api_key="",
    )

    assert result["summary"]
    assert "termination" in result["summary"].lower() or "payment" in result["summary"].lower()
    assert isinstance(result["highlights"], list)


def test_extract_text_from_file_reads_text_files(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("This contract requires payment and includes termination rights.")

    content = extract_text_from_file(str(file_path))

    assert "payment" in content.lower()
    assert "termination" in content.lower()
