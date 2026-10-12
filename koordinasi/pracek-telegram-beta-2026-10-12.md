# Pra-cek Telegram — skill `beta` (lokal, tanpa kirim)

**Tanggal:** 2026-10-12 UTC  
**Penguji:** Akun C (Cursor Cloud)  
**Metode:** `mk-home.sh` + `run-uji-tg.sh` (`--channel telegram`, tanpa `--deliver`), OpenClaw 2026.9.8, VM `$HOME/komunitech-uji`.

| # | Skill | Versi | Skor katalog | Pesan uji | Karakter | Verdik | Alasan singkat |
|---|--------|-------|--------------|-----------|----------|--------|----------------|
| 1 | slip-gaji-bpjs | 1.0.6 | 9 | S1 — slip 3 karyawan CV Contoh Maju Jaya (sama `examples/01-slip-gaji-3-karyawan.md`) | 1.773 | **GAGAL** | Rekap tabel + setoran BPJS/PPh ada di chat dan angka THP total cocok pola uji lokal; **isi slip per karyawan tidak ditampilkan** (hanya path `payroll/.../slip-gaji-2026-09.md|.html`). Di Telegram pembeli awam bisa mengira jawaban “kosong” bila lampiran file tidak terkirim. Saran pembuat: tampilkan minimal 1 slip contoh utuh di chat + tawarkan “balas kirim file” bila panjang. |

**Run berikutnya (C9):** skill `beta` berikutnya — prioritas output panjang, skor 9: `pph21-ter`, `hitung-thr`, `kontrak-kerja-pkwt`, `presentasi-instan`, `rencana-pelajaran-guru`.

Output mentah: `$HOME/komunitech-uji/openclaw-real/hasil/sgb-tg-01-out.txt` (tidak di-commit).
