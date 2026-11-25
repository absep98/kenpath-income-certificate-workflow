"""AI assistance, in two layers.

1. rule_flags(): deterministic checks in plain Python. Always works, no network.
2. llm_assist(): a Groq-hosted LLM writes a short case summary and a draft
   reason. Optional: if the key is missing or the call fails, flags still work.

The AI only SUGGESTS. The officer makes the decision.
"""
import json
import os
import urllib.request
from pathlib import Path

REQUIRED_DOCS = ["aadhaar", "ration_card", "income_affidavit", "photo"]

# Illustrative demo threshold, NOT an official limit. Real ceilings are set by
# the department and vary by certificate purpose.
INCOME_REVIEW_CEILING = 300000

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"

DOC_NAMES = {
    "kn": {
        "aadhaar": "ಆಧಾರ್",
        "ration_card": "ರೇಷನ್ ಕಾರ್ಡ್",
        "income_affidavit": "ಆದಾಯ ಪ್ರಮಾಣ ಪತ್ರ (ಅಫಿಡವಿಟ್)",
        "photo": "ಭಾವಚಿತ್ರ",
    },
    "en": {
        "aadhaar": "Aadhaar",
        "ration_card": "Ration card",
        "income_affidavit": "Income affidavit",
        "photo": "Photo",
    },
}


def rule_flags(application):
    """Return flag codes, e.g. ['missing_doc:photo', 'income_high']."""
    flags = []
    have = [d.strip() for d in application.documents.split(",") if d.strip()]

    for doc in REQUIRED_DOCS:
        if doc not in have:
            flags.append(f"missing_doc:{doc}")

    if application.declared_income > INCOME_REVIEW_CEILING:
        flags.append("income_high")
    return flags


def flag_text(code, lang="kn"):
    """Turn a flag code into a sentence in the officer's language."""
    lang = lang if lang in DOC_NAMES else "kn"
    if code.startswith("missing_doc:"):
        doc = code.split(":", 1)[1]
        name = DOC_NAMES[lang].get(doc, doc)
        return f"ದಾಖಲೆ ಕಾಣೆಯಾಗಿದೆ: {name}" if lang == "kn" else f"Missing document: {name}"
    if code == "income_high":
        return (
            f"ಘೋಷಿತ ಆದಾಯ ₹{INCOME_REVIEW_CEILING:,} ಕ್ಕಿಂತ ಹೆಚ್ಚು. ಹೆಚ್ಚುವರಿ ಪರಿಶೀಲನೆ ಅಗತ್ಯ"
            if lang == "kn"
            else f"Declared income is above ₹{INCOME_REVIEW_CEILING:,}. Check more carefully"
        )
    return code


def _api_key():
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    # Look next to this file, then one folder up (the repo root).
    for folder in (Path(__file__).parent, Path(__file__).parent.parent):
        env_file = folder / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("GROQ_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"')
    return None


def llm_assist(application, history, flags, lang="kn"):
    """Ask the LLM for {summary, suggested_reason}. Returns None on any failure."""
    key = _api_key()
    if not key:
        return None

    language = "Kannada" if lang == "kn" else "English"
    steps = "; ".join(f"{h.role}: {h.action} ({h.reason})" for h in history) or "none yet"
    facts = (
        f"Applicant: {application.applicant_name}, village {application.village}, "
        f"occupation {application.occupation}, family members {application.family_members}, "
        f"declared annual income Rs {application.declared_income}, "
        f"documents provided: {application.documents or 'none'}, "
        f"current stage: {application.status.value}, "
        f"rule-check flags: {', '.join(flags) or 'none'}, previous steps: {steps}."
    )
    prompt = (
        "You assist a government officer reviewing an income certificate application. "
        f"Write in simple {language}. Use ONLY the facts given; do not invent anything. "
        "Reply as JSON with two keys: 'summary' (2-3 short sentences about the case, "
        "mentioning anything that needs attention) and 'suggested_reason' (one short sentence "
        "the officer could use as the note for their decision). You only suggest; "
        f"the officer decides.\n\nFacts: {facts}"
    )
    body = json.dumps({
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    }).encode("utf-8")
    req = urllib.request.Request(
        GROQ_URL, data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            # Groq's CDN rejects Python's default urllib User-Agent (error 1010).
            "User-Agent": "workflow-demo/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        out = json.loads(data["choices"][0]["message"]["content"])
        return {
            "summary": str(out.get("summary", "")),
            "suggested_reason": str(out.get("suggested_reason", "")),
        }
    except Exception:
        return None
