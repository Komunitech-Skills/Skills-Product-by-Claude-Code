# Uji konteks Telegram — skenario 1 (Bu Sri)

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (independen)
- **Versi skill:** 1.0.0
- **Cara:** `mk-home.sh` + `run-uji-tg.sh` (VM Cursor, tanpa `unshare`), OpenClaw 2026.9.8, model router `claude-sonnet-5`, `--channel telegram` tanpa `--deliver`.

## Pesan uji
Sama dengan skenario 01 di `00-openclaw-sebelum-sesudah.md` (warung Dapur Bu Sri, Semarang).

## Hasil
- **Panjang jawaban:** 7.955 karakter (lokal tanpa Telegram pada run yang sama: ±9,5 rb — selisih wajar, tidak terpotong).
- **Format:** header skill `# Persiapan Jual/Wariskan Usaha — Dapur Bu Sri`, tabel/angka laba, range harga, checklist persiapan, 3 pertanyaan singkat di akhir (bukan mode “balas kirim file”).
- **Alat:** `read`, `ls`, `exec` (script hitung dipakai).
- **Verdik pra-cek Telegram:** **OK untuk pilot** — isi utuh di chat, struktur konsisten dengan uji lokal; tidak perlu revisi khusus kanal Telegram untuk panjang jawaban S1.

## Catatan
- `uji.sh` / `uji-tg.sh` bawaan gagal `unshare` di VM Cursor; gunakan `run-uji-tg.sh` dari `koordinasi/alat-uji/`.
