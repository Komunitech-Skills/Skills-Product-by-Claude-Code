#!/usr/bin/env bash
# run-uji.sh — VM Cursor: sama intinya dengan uji.sh tanpa unshare (mount namespace tidak diizinkan).
# HOME SESI KELUAR "pesan" → hasil di $R/hasil/$KELUAR.{json,txt,err}
R="$(cd "$(dirname "$0")" && pwd)"
BASE="${BASE:-$HOME/komunitech-uji}"
OC="$BASE/openclaw-prod/node_modules/.bin/openclaw"
NODE_BIN="$BASE/node-v24.21.0-linux-x64/bin"
HN=$1; S=$2; O=$3; shift 3
H=$R/homes/$HN
mkdir -p "$R/hasil"
cd "$H/.openclaw/workspace"
timeout 900 env -i HOME="$H" PATH="$NODE_BIN:/usr/local/bin:/usr/bin:/bin" LANG=C.UTF-8 TZ=Asia/Jakarta \
  HTTPS_PROXY="${HTTPS_PROXY:-}" HTTP_PROXY="${HTTP_PROXY:-}" NO_PROXY="${NO_PROXY:-}" \
  NODE_EXTRA_CA_CERTS="${NODE_EXTRA_CA_CERTS:-}" SSL_CERT_FILE="${SSL_CERT_FILE:-}" \
  NINEROUTER_UJI_KEY="${Ninerouter_key:-}" TAVILY_API_KEY="${TAVILY_API_KEY:-${tavily:-}}" \
  "$OC" agent --local --session-id "$S" -m "$*" --json --timeout 800 \
  > "$R/hasil/$O.json" 2> "$R/hasil/$O.err"
echo "rc=$?"
python3 - "$R/hasil/$O.json" "$R/hasil/$O.txt" <<'PY'
import json, sys
t = open(sys.argv[1]).read()
try:
    d = json.loads(t[t.find("{") :])
    pl = d.get("payloads") or d.get("result", {}).get("payloads") or []
    txt = "\n\n".join(p.get("text", "") for p in pl if p.get("text"))
    m = d.get("meta", {}).get("agentMeta", {})
    tools = (m.get("terminalReceipt") or {}).get("successfulToolNames")
    open(sys.argv[2], "w").write(txt)
    print("tools:", tools, "| chars:", len(txt))
except Exception as ex:
    print("parse gagal", ex, t[:300])
PY
