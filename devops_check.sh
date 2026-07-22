#!/bin/bash
echo "=================================================="
echo "🔍 RUNNING LEFT-SHIFT DEVOPS AUDIT & ENVIRONMENT CHECK"
echo "=================================================="
echo ""

echo "📁 1. WORKSPACE AUDIT (E: Drive)"
echo "--------------------------------"
if [ -d "/e/ME@DevAI/Git/mcore-academy" ]; then
    echo "  ✅ Target Directory Exists: /e/ME@DevAI/Git/mcore-academy"
else
    echo "  ❌ Target Directory Missing: /e/ME@DevAI/Git/mcore-academy"
    mkdir -p /e/ME@DevAI/Git/mcore-academy
    echo "  🔧 Auto-created workspace."
fi

echo ""
echo "⚙️ 2. LOCATING NODE.JS & EXECUTABLES"
echo "------------------------------------"
FOUND_NODE=""
PATHS_TO_SEARCH=(
    "/c/Program Files/nodejs"
    "/c/Program Files (x86)/nodejs"
    "/c/Users/$USER/AppData/Roaming/nvm/current"
    "/c/Users/$USER/AppData/Local/Programs/nodejs"
    "/c/Users/$USER/AppData/Roaming/npm"
)
for p in "${PATHS_TO_SEARCH[@]}"; do
    if [ -f "$p/node.exe" ] || [ -f "$p/node" ]; then
        echo "  ✅ FOUND Node.js at: $p"
        FOUND_NODE="$p"
        break
    fi
done
if [ -z "$FOUND_NODE" ]; then
    WIN_WHERE=$(where.exe node 2>/dev/null | head -n 1)
    if [ -n "$WIN_WHERE" ]; then
        echo "  ✅ FOUND Node.js via system path: $WIN_WHERE"
        FOUND_NODE="SYSTEM_PATH"
    else
        echo "  ❌ CRITICAL ERROR: node.exe was NOT found on this system."
        echo "  👉 Action Needed: Node.js must be installed or added to Windows Environment Variables."
    fi
fi

echo ""
echo "🔑 3. OAUTH & CREDENTIALS CHECK (E: Drive)"
echo "-------------------------------------------"
KEYS_PATH="/e/ME@DevAI/.config/google-drive-mcp/gcp-oauth.keys.json"
if [ -f "$KEYS_PATH" ]; then
    echo "  ✅ OAuth Keys Found: $KEYS_PATH"
    echo "  📄 File Size: $(wc -c < "$KEYS_PATH") bytes"
else
    echo "  ❌ OAuth Keys MISSING: $KEYS_PATH"
    echo "  🔧 Auto-generating OAuth keys file now..."
    mkdir -p /e/ME@DevAI/.config/google-drive-mcp
    cat << 'JSON' > "$KEYS_PATH"
{
  "installed": {
    "client_id": "497317068135-cui4fbrh6jjo49dpfoma5hf7v0dpccai.apps.googleusercontent.com",
    "project_id": "MCore-Academy",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "redirect_uris": ["http://localhost"]
  }
}
JSON
    echo "  ✅ OAuth Keys successfully initialized."
fi

echo ""
echo "=================================================="
echo "📊 AUDIT SUMMARY & RECOMMENDED PLAN"
echo "=================================================="
if [ -n "$FOUND_NODE" ]; then
    echo "  Status: READY FOR AUTHENTICATION 🚀"
    echo "  Detected Node Location: $FOUND_NODE"
else
    echo "  Status: BLOCKED BY MISSING NODE.JS 🛑"
fi
echo "=================================================="
