import re
from urllib.parse import urlparse

TRACKER_KEYWORDS = [
    "google-analytics", "doubleclick", "ads", "pixel",
    "facebook.com/tr", "analytics", "tracking"
]

def uses_https(url):
    parsed = urlparse(url)
    return parsed.scheme == "https"

def has_tracking_keywords(url):
    return any(keyword in url.lower() for keyword in TRACKER_KEYWORDS)

def run_privacy_checks(url):
    https_flag = uses_https(url)
    tracker_flag = has_tracking_keywords(url)

    if https_flag and not tracker_flag:
        privacy_status = "Good"
    elif https_flag and tracker_flag:
        privacy_status = "Moderate"
    else:
        privacy_status = "Poor"

    return {
        "https_enabled": https_flag,
        "possible_tracking": tracker_flag,
        "privacy_status": privacy_status
    }
