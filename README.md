<p align="center">

<div align="center">

# 🛡️ Kevlar - Modular Browser Security Suite

</div>

</p>

<p align="center">
  <img src="core/phishguard/extension/KevlarLogo.PNG" alt="Kevlar Logo">
</p>

> **Kevlar** is a next‑generation browser security platform that evolved from the original **PhishGuard** prototype into a **multi‑layer, modular security suite**.  
> It combines **machine learning**, **rule‑based security checks**, **privacy analysis**, and **AI‑style scam detection**, all exposed via a clean backend and a live Chrome extension.

---

## ✨ Highlights

- 🔐 **Real‑time phishing detection** using the PhishGuard ML engine (Random Forest on 95k+ URLs)
- 🛡 **Security risk analysis** for URLs (shorteners, IP‑based URLs, scammy keywords)
- 🔒 **Privacy module** that evaluates HTTPS usage and tracker‑style patterns
- 🤖 **AI Safety Checker** for scammy messages / emails (urgency, money, malicious links)
- 🌐 **Chrome extension** that scans the **currently open tab** and shows results instantly
- 🧩 **Modular architecture** with independent security, privacy, AI, and ML layers
- ⚙️ **Config‑driven backend** (feature flags & thresholds via `shared/config.py`)

---

## 🧩 Kevlar Modules Overview

Kevlar is built around **4 core modules**, all wired into a single backend:

1. **PhishGuard Core (ML Engine)**
   - Random Forest model trained on ~96,000 URLs
   - Feature engineering includes:
     - URL length, domain length, path length
     - Special character counts (`.`, `-`, `@`, `?`, `=`)
     - Counts of digits & letters
     - HTTPS flag
     - Presence of phishing keywords (`login`, `secure`, `verify`, `bank`, etc.)
   - REST endpoint: `POST /predict`

2. **Security Module**
   - Rule‑based URL risk analysis
   - Detects:
     - Shortened URLs (`bit.ly`, `tinyurl`, `t.co`, etc.)
     - IP‑based URLs
     - High‑risk phishing keywords in the URL
   - Returns a **risk score** and **verdict**: `Low / Medium / High`
   - REST endpoint: `POST /security-check`

3. **Privacy Module**
   - Checks if the site uses **HTTPS**
   - Scans for common **tracking / analytics patterns**
   - Returns `https_enabled`, `possible_tracking`, and `privacy_status`:  
     `Good / Moderate / Poor`
   - REST endpoint: `POST /privacy-check`

4. **AI Safety Checker**
   - Lightweight rule‑based “AI‑style” analyzer for text:
     - Urgent language (`urgent`, `immediately`, `final warning`, etc.)
     - Financial bait (`bank`, `card`, `UPI`, `reward`, `prize`, `crypto`, etc.)
     - Presence of links
   - Returns a **risk score** and **verdict**: `Low / Medium / High`
   - REST endpoint: `POST /ai-check`

---

## 🏗️ Project Structure

```bash
Kevlar/
├── core/
│   └── phishguard/
│       ├── backend/
│       │   ├── app.py              # Kevlar backend + all API routes
│       │   ├── features.py         # Feature extraction for PhishGuard
│       │   ├── model.pkl           # Trained Random Forest model
│       │   └── ...                 # Helper files / env, etc.
│       │
│       ├── extension/
│       │   ├── manifest.json       # Chrome extension manifest (MV3)
│       │   ├── popup.html          # Kevlar popup UI
│       │   ├── popup.js            # Calls /predict, /security-check, /privacy-check
│       │   ├── background.js       # Background service worker (future hooks)
│       │   └── KevlarLogo.png      # Extension icon / branding
│       │
│       └── ml/
│           ├── train_model.py      # Model training pipeline
│           └── urlset.csv          # URL dataset (features + labels)
│
├── modules/
│   ├── security/
│   │   └── security.py             # URL risk analysis logic
│   ├── privacy/
│   │   └── privacy.py              # HTTPS + tracking analysis
│   └── ai_checker/
│       └── ai_checker.py           # Text risk analysis logic
│
└── shared/
    └── config.py                   # Global config, feature flags, thresholds
```

---

## 🛠️ Tech Stack

**Backend**
- Python
- Flask (REST APIs)
- Joblib (model loading)
- Scikit‑learn (Random Forest)
- Pandas / NumPy (data handling for training)

**Frontend (Extension)**
- HTML, CSS, JavaScript
- Chrome Extensions (Manifest V3)
- `chrome.tabs` & `fetch` APIs

**Model**
- RandomForestClassifier
- ~96k rows, 12 numerical features
- ~95–96% test accuracy

---

## ⚙️ Setup & Installation

> 💡 All commands assume you are inside the project root: `Kevlar/`

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/Kevlar.git
cd Kevlar
```

### 2️⃣ Create & Activate Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux / macOS
```

### 3️⃣ Install Backend Dependencies

```bash
pip install flask pandas scikit-learn joblib
```

### 4️⃣ Train the PhishGuard ML Model

```bash
cd core/phishguard/ml
python train_model.py
```

This will:

- Load `urlset.csv`
- Clean and preprocess the data
- Train a Random Forest model
- Evaluate accuracy
- Save the model to:

```text
core/phishguard/backend/model.pkl
```

### 5️⃣ Run the Kevlar Backend

```bash
cd ../backend
python app.py
```

Backend will be available at:

```text
http://127.0.0.1:5000/
```

You can test it with:

```bash
curl http://127.0.0.1:5000/
```

---

## 🌐 Load the Chrome Extension

1. Open Chrome and go to:

   ```text
   chrome://extensions/
   ```

2. Enable **Developer mode** (top‑right)
3. Click **Load unpacked**
4. Select the folder:

   ```text
   core/phishguard/extension
   ```

5. Pin **Kevlar** from the extensions menu to your toolbar

Now:
- Open any website (e.g. Google, GitHub, a test phishing URL)
- Click the **Kevlar icon**
- You’ll see, for the active tab:
  - `PhishGuard: SAFE / PHISHING`
  - `Security Risk: Low / Medium / High`
  - `Privacy Status: Good / Moderate / Poor`

All of these are powered by calls from the extension to your local Kevlar backend.

---

## 🔌 API Reference (Local)

Base URL (local dev):

```text
http://127.0.0.1:5000
```

### `POST /predict` — PhishGuard ML Detection

**Body:**

```json
{
  "url": "https://example.com"
}
```

**Response:**

```json
{
  "url": "https://example.com",
  "prediction": "safe | phishing | suspicious",
  "engine": "PhishGuard",
  "platform": "Kevlar"
}
```

---

### `POST /security-check` — URL Security Analysis

**Body:**

```json
{
  "url": "https://bit.ly/some-link"
}
```

**Example Response:**

```json
{
  "contains_ip": false,
  "shortened_url": true,
  "suspicious_keywords": true,
  "risk_score": 80,
  "verdict": "High Risk"
}
```

---

### `POST /privacy-check` — Privacy Exposure Check

**Body:**

```json
{
  "url": "http://example.com"
}
```

**Example Response:**

```json
{
  "https_enabled": false,
  "possible_tracking": false,
  "privacy_status": "Poor"
}
```

---

### `POST /ai-check` — Text / Email Scam Analysis

**Body:**

```json
{
  "text": "Urgent! Your bank account is suspended. Click this link to verify immediately."
}
```

**Example Response:**

```json
{
  "urgent_language": true,
  "financial_language": true,
  "contains_link": true,
  "risk_score": 100,
  "verdict": "High Risk"
}
```

---

## 🎯 Example Demo Flow

1. Start backend: `python app.py`
2. Test health:

   ```bash
   curl http://127.0.0.1:5000/
   ```

3. Test safe URL:

   ```bash
   curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"url\":\"https://google.com\"}"
   ```

4. Test phishing URL:

   ```bash
   curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"url\":\"http://login-secure-bank-verification.com\"}"
   ```

5. Test URL Security & Privacy:

   ```bash
   curl -X POST http://127.0.0.1:5000/security-check -H "Content-Type: application/json" -d "{\"url\":\"https://bit.ly/test\"}"

   curl -X POST http://127.0.0.1:5000/privacy-check -H "Content-Type: application/json" -d "{\"url\":\"http://example.com\"}"
   ```

6. Test AI Safety Checker:

   ```bash
   curl -X POST http://127.0.0.1:5000/ai-check -H "Content-Type: application/json" -d "{\"text\":\"Urgent! Your bank account is suspended. Click immediately.\"}"
   ```

7. Show the Chrome extension scanning live websites.

---

## 🚀 Future Scope

- Deploy Kevlar as a **cloud‑hosted API** (e.g. AWS / Render / Railway)
- Package and publish the extension on the **Chrome Web Store**
- Plug in a real **LLM/AI model** for richer scam & phishing text analysis
- Add **per‑user dashboards** and **threat analytics**
- Extend support to other browsers (Firefox, Edge)

---

## 📌 Credits

Kevlar is built as an evolution of the original **PhishGuard** prototype — upgrading it from a single‑feature phishing detector into a complete, modular browser security platform with ML + rules + privacy + AI layers.

