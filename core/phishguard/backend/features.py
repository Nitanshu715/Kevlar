from urllib.parse import urlparse
import re

# ============================================
# PHISHGUARD CORE FEATURES (DO NOT MODIFY)
# These 12 features MUST stay exactly the same
# because your model is trained on them.
# ============================================

def extract_phishguard_features(url):
    parsed = urlparse(url)

    return [
        len(url),
        len(parsed.netloc),
        len(parsed.path),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        url.count('?'),
        url.count('='),
        sum(c.isdigit() for c in url),
        sum(c.isalpha() for c in url),
        1 if parsed.scheme == "https" else 0,
        1 if re.search(r'login|verify|update|secure|account|bank', url.lower()) else 0
    ]


# ============================================
# KEVLAR SECURITY MODULE FEATURES (FUTURE)
# These are NOT used for ML prediction YET.
# ============================================

def extract_security_features(url):
    parsed = urlparse(url)

    features = {
        "has_ip": 1 if re.search(r"(\d{1,3}\.){3}\d{1,3}", url) else 0,
        "suspicious_keywords": 1 if re.search(r"free|offer|click|win|urgent", url.lower()) else 0,
        "shortened_url": 1 if any(x in url.lower() for x in ["bit.ly", "tinyurl", "t.co"]) else 0,
        "at_symbol": 1 if "@" in url else 0
    }

    return features


# ============================================
# KEVLAR PRIVACY MODULE FEATURES (FUTURE)
# ============================================

def extract_privacy_features(url):
    parsed = urlparse(url)

    features = {
        "uses_https": 1 if parsed.scheme == "https" else 0,
        "tracking_keywords": 1 if re.search(r"track|ads|pixel|analytics", url.lower()) else 0
    }

    return features


# ============================================
# KEVLAR AI CHECKER MODULE FEATURES (FUTURE)
# ============================================

def extract_ai_checker_features(text):
    features = {
        "has_urgent_words": 1 if re.search(r"urgent|immediately|suspended|alert", text.lower()) else 0,
        "has_money_words": 1 if re.search(r"bank|card|payment|upi|reward", text.lower()) else 0
    }

    return features


# ============================================
# MASTER FUNCTION USED BY app.py (CURRENT)
# This returns ONLY PhishGuard features for now
# so your current ML model NEVER breaks.
# ============================================

def extract_features(url):
    return extract_phishguard_features(url)
