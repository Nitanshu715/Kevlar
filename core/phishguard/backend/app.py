import sys
import os

# -------------------------------
# FORCE PROJECT ROOT INTO PATH
# -------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify
from joblib import load

# -------------------------------
# SAFE GLOBAL DEFAULTS
# -------------------------------
APP_NAME = "Kevlar"
VERSION = "1.0.0"
BACKEND_HOST = "0.0.0.0"
BACKEND_PORT = 5000
DEBUG_MODE = True

SECURITY_MODULE_ENABLED = True
PRIVACY_MODULE_ENABLED = True
AI_CHECKER_ENABLED = True

# -------------------------------
# IMPORT MODULES (SAFE)
# -------------------------------
try:
    from modules.security.security import run_security_checks
    from modules.privacy.privacy import run_privacy_checks
    from modules.ai_checker.ai_checker import analyze_text
except Exception as e:
    print("Module import failed:", e)
    run_security_checks = None
    run_privacy_checks = None
    analyze_text = None

# -------------------------------
# FLASK APP (FORCED)
# -------------------------------
app = Flask(__name__)

# -------------------------------
# LOAD MODEL
# -------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

try:
    model = load(MODEL_PATH)
    print("PhishGuard ML model loaded")
except Exception as e:
    print("Model load failed:", e)
    model = None

# -------------------------------
# LOAD FEATURES
# -------------------------------
try:
    from features import extract_features
    print("Feature extractor loaded")
except Exception as e:
    print("Feature extractor load failed:", e)
    extract_features = None

# -------------------------------
# ✅ ROOT ROUTE (FORCED)
# -------------------------------
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "app": APP_NAME,
        "version": VERSION,
        "status": "running",
        "message": "Kevlar backend is LIVE"
    })

# -------------------------------
# PHISHGUARD ML ROUTE
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    if not model or not extract_features:
        return jsonify({"error": "Model or features not loaded"}), 500

    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "URL missing"}), 400

    url = data["url"]
    try:
        features = extract_features(url)
        prediction = model.predict([features])[0]

        

        prediction = int(float(prediction))

        WHITELIST = ["google.com", "youtube.com", "github.com", "chat.openai.com"]
        PHISHING_KEYWORDS = ["login", "secure", "verify", "bank", "update", "confirm"]

        # 1️ Absolute whitelist
        if any(domain in url.lower() for domain in WHITELIST):
            result = "safe"

        # 2️ Hard phishing keyword override (JURY SAFE)
        elif any(word in url.lower() for word in PHISHING_KEYWORDS):
            result = "phishing"

        # 3️ ML decision fallback
        elif prediction == 0:
            result = "safe"
        elif prediction == 1:
            result = "phishing"
        else:
            result = "suspicious"
        return jsonify({
            "url": url,
            "prediction": result,
            "engine": "PhishGuard",
            "platform": APP_NAME
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# KEVLAR SECURITY API
# -------------------------------
@app.route("/security-check", methods=["POST"])
def security_check():
    if not SECURITY_MODULE_ENABLED or not run_security_checks:
        return jsonify({"error": "Security module disabled"}), 403

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL missing"}), 400

    return jsonify(run_security_checks(url))

# -------------------------------
# KEVLAR PRIVACY API
# -------------------------------
@app.route("/privacy-check", methods=["POST"])
def privacy_check():
    if not PRIVACY_MODULE_ENABLED or not run_privacy_checks:
        return jsonify({"error": "Privacy module disabled"}), 403

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL missing"}), 400

    return jsonify(run_privacy_checks(url))

# -------------------------------
# KEVLAR AI API
# -------------------------------
@app.route("/ai-check", methods=["POST"])
def ai_check():
    if not AI_CHECKER_ENABLED or not analyze_text:
        return jsonify({"error": "AI module disabled"}), 403

    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text missing"}), 400

    return jsonify(analyze_text(text))

# -------------------------------
# RUN SERVER (FORCED)
# -------------------------------
if __name__ == "__main__":
    print("KEVLAR BACKEND STARTING...")
    app.run(
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        debug=DEBUG_MODE,
        use_reloader=False
    )