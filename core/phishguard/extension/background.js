// ==============================
// Kevlar Background Service
// ==============================

console.log("Kevlar background service started");

// Listen for tab updates (future: auto-scan, auto-block)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    console.log("Kevlar monitoring:", tab.url);

    // 🔮 Future use:
    // - Auto scan URLs
    // - Auto block malicious pages
    // - Trigger privacy protections
  }
});

// Handle messages from popup or content scripts (future use)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "KEVLAR_PING") {
    sendResponse({ status: "Kevlar is active" });
  }

  // 🔮 Future:
  // if (request.type === "AUTO_SCAN") { ... }
  // if (request.type === "BLOCK_SITE") { ... }
});
