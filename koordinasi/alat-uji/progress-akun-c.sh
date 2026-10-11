#!/usr/bin/env bash
# Ringkasan progres antrian Akun C (C1–C5) untuk log run otomatis.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PAPAN="$ROOT/koordinasi/papan-tugas.md"
TOTAL=5
DONE=$(grep -E '^\| C[1-5] ' "$PAPAN" | grep -c 'selesai' || true)
PCT=$(( DONE * 100 / TOTAL ))
echo "Akun C antrian: ${DONE}/${TOTAL} (${PCT}%) selesai (C1–C5 di papan-tugas)"
