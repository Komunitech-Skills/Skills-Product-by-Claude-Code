#!/usr/bin/env bash
# run-uji.sh — sama intent dengan uji.sh, tanpa unshare (VM Cursor Cloud / container tanpa user namespace).
# Folder scratchpad sesi (wajib): export SCRATCHPAD=$HOME/komunitech-uji
SP=${SCRATCHPAD:?isi SCRATCHPAD dengan folder scratchpad sesi}
R=$SP/openclaw-real
NODE_DIR="$SP/node-v24.21.0-linux-x64"
OC="$SP/openclaw-prod/node_modules/.bin/openclaw"
HN=$1; S=$2; O=$3; shift 3
H=$R/homes/$HN
mkdir -p "$R/hasil"
cd "$H/.openclaw/workspace"
timeout 900 env -i HOME="$H" PATH="$NODE_DIR/bin:/usr/local/bin:/usr/bin:/bin" \
  LANG=C.UTF-8 TZ=Asia/Jakarta \
  HTTPS_PROXY="${HTTPS_PROXY:-}" HTTP_PROXY="${HTTP_PROXY:-}" NO_PROXY="${NO_PROXY:-}" \
  NODE_EXTRA_CA_CERTS="${NODE_EXTRA_CA_CERTS:-}" SSL_CERT_FILE="${SSL_CERT_FILE:-}" \
  NINEROUTER_UJI_KEY="${Ninerouter_key:-}" \
  "$OC" agent --local --session-id "$S" -m "$*" --json --timeout 800 \
  > "$R/hasil/$O.json" 2> "$R/hasil/$O.err"
echo "rc=$?"
python3 - "$R/hasil/$O.json" "$R/hasil/$O.txt" <<'PY'
import json,sys
t=open(sys.argv[1]).read()
try:
  d=json.loads(t[t.find('{'):])
  pl=d.get('payloads') or d.get('result',{}).get('payloads') or []
  txt="\n\n".join(p.get('text','') for p in pl if p.get('text'))
  m=d.get('meta',{}).get('agentMeta',{})
  tools=(m.get('terminalReceipt') or {}).get('successfulToolNames')
  open(sys.argv[2],'w').write(txt)
  print('tools:',tools,'| chars:',len(txt))
except Exception as ex: print('parse gagal',ex,t[:300])
PY
