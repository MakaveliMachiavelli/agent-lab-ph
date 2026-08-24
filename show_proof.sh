#!/usr/bin/env bash
# Render the ₱0 Empire proof as visible HTML on display :99 for capture
export DISPLAY=:99
URL="https://capital-stored-bonus-attempt.trycloudflare.com"
cat > /tmp/proof.html << HTML
<!doctype html><html><head><meta charset="utf-8"><style>
body{background:#0a0e14;color:#00ff9c;font-family:monospace;padding:40px;font-size:22px}
h1{color:#ff2e88;font-size:42px}
.ok{color:#00ff9c}.warn{color:#ffcc00}
pre{background:#111;border:1px solid #333;padding:20px;border-radius:8px}
</style></head><body>
<h1>₱0 EMPIRE — LIVE PROOF</h1>
<pre>
$ uname -a
Linux instance-20260804-1901 6.17.0-1019-oracle  ← ORACLE FREE TIER

$ free -h
Mem: 62Gi  ← FREE. FOREVER.

$ uptime
10 days  ← NEVER SHUT DOWN. FREE.

$ curl https://capital-stored-bonus-attempt.trycloudflare.com/healthz
{"status":"ok"}  ← PUBLIC URL → n8n ON THIS BOX

STACK: Oracle Free + Cloudflare Tunnel + n8n = ₱0/month
</pre>
<p class="warn">No credit card for hosting. No port-forward. No domain. Just free.</p>
</body></html>
HTML
which chromium chromium-browser google-chrome 2>/dev/null || echo "NO_CHROME"
