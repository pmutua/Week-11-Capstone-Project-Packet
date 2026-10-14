"""Week 9 Tuesday redaction patterns (week9_tuesday/redact.py), reused here
so triage logs never carry a bearer token, phone number, M-Pesa code, or
Kenyan national ID, even in this capstone's stub mode.

Order matters: PHONE runs before KENYA_ID so a phone number's last eight
digits are not left recognisable after the ID pattern already matched.
"""
import re

BEARER = re.compile(r"Bearer\s+\S+", re.I)
KENYA_ID = re.compile(r"\b\d{8}\b")
PHONE = re.compile(r"(?:\+254|0)7\d{8}\b")
MPESA = re.compile(r"\b[A-Z][A-Z0-9]{9}\b")

EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")


def redact(text: str) -> str:
    text = BEARER.sub("Bearer [REDACTED]", text)
    text = PHONE.sub("[REDACTED_PHONE]", text)
    text = MPESA.sub("[REDACTED_MPESA]", text)
    text = KENYA_ID.sub("[REDACTED_ID]", text)
    text = EMAIL.sub("[REDACTED_EMAIL]", text)
    return text
