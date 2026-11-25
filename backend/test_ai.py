from ai import rule_flags, flag_text
from models import Application

ALL_DOCS = "aadhaar,ration_card,income_affidavit,photo"


def make(income=100000, docs=ALL_DOCS):
    return Application(applicant_name="x", village="y", declared_income=income, documents=docs)


def test_clean_application_has_no_flags():
    assert rule_flags(make()) == []


def test_missing_documents_are_flagged():
    flags = rule_flags(make(docs="aadhaar,photo"))
    assert "missing_doc:ration_card" in flags
    assert "missing_doc:income_affidavit" in flags
    assert "missing_doc:photo" not in flags


def test_high_income_is_flagged():
    assert rule_flags(make(income=900000)) == ["income_high"]


def test_flag_text_in_both_languages():
    assert "Photo" in flag_text("missing_doc:photo", "en")
    assert "ಭಾವಚಿತ್ರ" in flag_text("missing_doc:photo", "kn")
