#!/usr/bin/env bash
# Rekam ulang tests/fixtures/umami-3.4.0.json dari Umami ASLI di 127.0.0.1:3000 (hanya pengembang Komunitech).
# Pakai: bash tests/rekam_semua.sh <file-kunci-view-only> <file-kunci-admin>
# Prasyarat: Umami 3.4.0 berisi data tests/isi_data_fiktif.py + 1 tautan pelacak (lihat examples/uji-pembuat/).
set -euo pipefail
D="$(cd "$(dirname "$0")/.." && pwd)"; S="$D/scripts/umami.py"; KB="$1"; KA="$2"
rm -f "$D/tests/fixtures/umami-3.4.0.json"
python3 "$D/tests/rekam_fixture.py" --kunci-baca "$KB" --kunci-admin "$KA" --detik 60 &
sleep 1.5
U="--url http://127.0.0.1:3996"; N="--sekarang 2026-09-29T16:00"
export HOME="$(mktemp -d)" UMAMI_API_KEY_FILE="$KB"
for P in minggu-lalu minggu-ini kemarin hari-ini 7hari 30hari bulan-ini bulan-lalu; do python3 "$S" ringkasan $U $N --periode $P >/dev/null; done
python3 "$S" ringkasan $U $N --dari 2026-09-21 --sampai 2026-09-27 >/dev/null
python3 "$S" cek $U >/dev/null; python3 "$S" situs $U >/dev/null
for c in "halaman" "halaman --jenis masuk" "halaman --jenis keluar" "sumber" "utm" "pengunjung --semua" "konversi" "laporan-mingguan"; do
  python3 "$S" $c $U $N --periode minggu-lalu >/dev/null
done
python3 "$S" ekspor-csv $U $N --periode minggu-lalu --keluaran "$HOME/r.csv" >/dev/null
python3 "$S" banding $U $N >/dev/null; python3 "$S" laporan-mingguan $U $N >/dev/null
python3 "$S" konversi $U $N --periode minggu-ini >/dev/null; python3 "$S" utm $U $N --periode minggu-ini >/dev/null
python3 "$S" tautan $U --sekarang 2026-09-29T17:00 >/dev/null
UMAMI_API_KEY_FILE="$KA" python3 "$S" ringkasan $U $N 2>/dev/null || true
UMAMI_API_KEY_FILE="$KA" python3 "$S" ringkasan --situs batik $U $N --periode 30hari >/dev/null
UMAMI_API_KEY_FILE="$KA" python3 "$S" cek $U >/dev/null
UMAMI_API_KEY_FILE= UMAMI_API_KEY=umami_salahsalahsalahsalahsalahsalah12 python3 "$S" ringkasan $U $N 2>/dev/null || true
# 401 website di luar akses (Toko Batik Laras milik admin, bukan tim)
curl -s --noproxy '*' "http://127.0.0.1:3996/api/websites/9a6ec2d7-668a-4e66-a2ea-85c6484bc2e2/stats?startAt=1789923600000&endAt=1790528399999&timezone=Asia%2FJakarta" \
  -H "Authorization: Bearer $(cat "$KB")" >/dev/null
wait
