import re
from urllib.parse import urlparse

SHORT_URL_SERVICES = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly"
]

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "account", "update",
    "free", "offer", "win", "urgent", "bank", "confirm"
]

def contains_ip_address(url):
    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"
    return bool(re.search(ip_pattern, url))

def is_shortened_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    return any(service in domain for service in SHORT_URL_SERVICES)

def has_suspicious_keywords(url):
    return any(keyword in url.lower() for keyword in SUSPICIOUS_KEYWORDS)

def run_security_checks(url):
    ip_flag = contains_ip_address(url)
    short_flag = is_shortened_url(url)
    keyword_flag = has_suspicious_keywords(url)

    risk_score = 0
    if ip_flag:
        risk_score += 40
    if short_flag:
        risk_score += 30
    if keyword_flag:
        risk_score += 30

    if risk_score >= 70:
        verdict = "High Risk"
    elif risk_score >= 40:
        verdict = "Medium Risk"
    else:
        verdict = "Low Risk"

    return {
        "contains_ip": ip_flag,
        "shortened_url": short_flag,
        "suspicious_keywords": keyword_flag,
        "risk_score": risk_score,
        "verdict": verdict
    }
