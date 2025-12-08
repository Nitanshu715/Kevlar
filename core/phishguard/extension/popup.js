document.addEventListener("DOMContentLoaded", () => {
  const label = document.getElementById("label");
  const urlDiv = document.getElementById("url");
  const scoreDiv = document.getElementById("score");

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs.length) {
      label.textContent = "No active tab";
      return;
    }

    const currentUrl = tabs[0].url;
    urlDiv.textContent = currentUrl;
    label.textContent = "Scanning with Kevlar...";

    // ========================
    // 1️⃣ PHISHGUARD ML SCAN
    // ========================
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: currentUrl })
    })
    .then(res => res.json())
    .then(phishData => {
      const phishResult = phishData.prediction.toUpperCase();

      // ========================
      // 2️⃣ SECURITY MODULE
      // ========================
      return fetch("http://127.0.0.1:5000/security-check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: currentUrl })
      })
      .then(res => res.json())
      .then(secData => ({ phishResult, secData }));
    })

    .then(({ phishResult, secData }) => {
      // ========================
      // 3️⃣ PRIVACY MODULE
      // ========================
      return fetch("http://127.0.0.1:5000/privacy-check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: currentUrl })
      })
      .then(res => res.json())
      .then(privData => ({ phishResult, secData, privData }));
    })

    .then(({ phishResult, secData, privData }) => {
      // ========================
      // ✅ FINAL DISPLAY
      // ========================
      label.textContent = `PhishGuard: ${phishResult}`;

      scoreDiv.innerHTML = `
      <b>Security Risk:</b> ${secData.verdict}<br>
      <b>Privacy Status:</b> ${privData.privacy_status}
`;
    })

    .catch(err => {
      console.error("Kevlar Error:", err);
      label.textContent = "❌ Backend not reachable";
      scoreDiv.textContent = "Make sure backend is running.";
    });
  });
});
