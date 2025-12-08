# ================================
# Kevlar Global Configuration
# ================================

APP_NAME = "Kevlar"
VERSION = "1.0.0"

# ================================
# MODULE ENABLE/DISABLE SWITCHES
# ================================

PHISHGUARD_ENABLED = True
SECURITY_MODULE_ENABLED = True
PRIVACY_MODULE_ENABLED = True
AI_CHECKER_ENABLED = True

# ================================
# BACKEND SETTINGS
# ================================

BACKEND_HOST = "0.0.0.0"
BACKEND_PORT = 5000
DEBUG_MODE = True

# ================================
# SECURITY MODULE THRESHOLDS
# ================================

SECURITY_HIGH_RISK_THRESHOLD = 70
SECURITY_MEDIUM_RISK_THRESHOLD = 40

# ================================
# PRIVACY MODULE SETTINGS
# ================================

REQUIRE_HTTPS = True
TRACKER_BLOCKING_ENABLED = True

# ================================
# AI CHECKER SETTINGS
# ================================

AI_HIGH_RISK_THRESHOLD = 80
AI_MEDIUM_RISK_THRESHOLD = 50

# ================================
# EXTENSION SETTINGS
# ================================

AUTO_SCAN_ENABLED = True
AUTO_BLOCK_ENABLED = False  # Future use

# ================================
# LOGGING SETTINGS
# ================================

ENABLE_LOGGING = True
LOG_FILE = "kevlar.log"
