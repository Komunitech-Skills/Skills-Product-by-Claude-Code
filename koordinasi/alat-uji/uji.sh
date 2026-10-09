#!/usr/bin/env bash
# uji.sh HOME SESI KELUAR "pesan"  -> satu giliran agent OpenClaw (lokal, tanpa Telegram); balasan teks ke KELUAR.txt
# Terisolasi (mount namespace): repo, scratchpad, home uji lain, dan transkrip Claude disembunyikan dari agent.
R=/tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-real
HN=$1; S=$2; O=$3; shift 3
H=$R/homes/$HN
mkdir -p $R/hasil
export UJI_H="$H" UJI_MSG="$*" UJI_S="$S" UJI_KEY="$Ninerouter_key"
timeout 900 unshare -m -p -f --mount-proc --propagation private bash -c '
set -e
mkdir -p /opt/ochome
mount --bind "$UJI_H" /opt/ochome
mount -t tmpfs tmpfs /tmp/claude-0
mount -t tmpfs tmpfs /home/user
mount -t tmpfs tmpfs /tmp/uji-openclaw/home
[ -d /root/.claude ] && mount -t tmpfs tmpfs /root/.claude
for d in /usr/local/lib/python3* /usr/lib/python3 /usr/lib/python3.* /root/.local; do [ -d "$d" ] && mount --bind "$d" "$d" && mount -o remount,bind,ro "$d"; done
cd /opt/ochome/.openclaw/workspace
exec env -i HOME=/opt/ochome PATH=/tmp/uji-openclaw/node-v24.21.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  LANG=C.UTF-8 TZ=Asia/Jakarta \
  HTTPS_PROXY="$HTTPS_PROXY" HTTP_PROXY="$HTTP_PROXY" https_proxy="$https_proxy" http_proxy="$http_proxy" NO_PROXY="$NO_PROXY" no_proxy="$no_proxy" \
  NODE_EXTRA_CA_CERTS="${NODE_EXTRA_CA_CERTS:-/root/.ccr/ca-bundle.crt}" SSL_CERT_FILE="$SSL_CERT_FILE" REQUESTS_CA_BUNDLE="$REQUESTS_CA_BUNDLE" \
  NINEROUTER_UJI_KEY="$UJI_KEY" \
  /tmp/uji-openclaw/node_modules/.bin/openclaw agent --local --session-id "$UJI_S" -m "$UJI_MSG" --json --timeout 800
' > $R/hasil/$O.json 2> $R/hasil/$O.err
echo "rc=$?"
unset UJI_KEY
python3 - $R/hasil/$O.json $R/hasil/$O.txt <<'PY'
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
