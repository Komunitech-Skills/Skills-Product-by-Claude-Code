#!/usr/bin/env bash
# wrapper: scrubbed env; only the router key (as NINEROUTER_UJI_KEY) and proxy vars are passed
# Instalasi PRODUKSI terpisah (/tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-prod), jangan pakai /tmp/uji-openclaw (milik alat uji).
R=/tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-real
exec env -i HOME=$R/home PATH=/tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-prod/node-v24.21.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  LANG=C.UTF-8 TZ=Asia/Jakarta \
  HTTPS_PROXY="$HTTPS_PROXY" HTTP_PROXY="$HTTP_PROXY" https_proxy="$https_proxy" http_proxy="$http_proxy" NO_PROXY="$NO_PROXY" no_proxy="$no_proxy" \
  NODE_EXTRA_CA_CERTS="${NODE_EXTRA_CA_CERTS:-/root/.ccr/ca-bundle.crt}" SSL_CERT_FILE="$SSL_CERT_FILE" REQUESTS_CA_BUNDLE="$REQUESTS_CA_BUNDLE" \
  NINEROUTER_UJI_KEY="$Ninerouter_key" ${TG_PASS:+TG_UJI_TOKEN="$bot_token"} \
  /tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-prod/node_modules/.bin/openclaw "$@"
