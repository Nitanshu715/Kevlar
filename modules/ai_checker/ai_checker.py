import re

URGENT_WORDS = [
    "urgent", "immediately", "suspended", "alert",
    "limited time", "final warning", "act now"
]

MONEY_WORDS = [
    "bank", "card", "upi", "payment", "reward", "prize", "money", "crypto"
]

LINK_PATTERN = r"(http|https)://"

def analyze_text(text):
    text = text.lower()

    urgent_flag = any(word in text for word in URGENT_WORDS)
    money_flag = any(word in text for word in MONEY_WORDS)
    has_link = bool(re.search(LINK_PATTERN, text))

    risk_score = 0

    if urgent_flag:
        risk_score += 40
    if money_flag:
        risk_score += 40
    if has_link:
        risk_score += 20

    if risk_score >= 80:
        verdict = "High Risk"
    elif risk_score >= 50:
        verdict = "Medium Risk"
    else:
        verdict = "Low Risk"

    return {
        "urgent_language": urgent_flag,
        "financial_language": money_flag,
        "contains_link": has_link,
        "risk_score": risk_score,
        "verdict": verdict
    }
