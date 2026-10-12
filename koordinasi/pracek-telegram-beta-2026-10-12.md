# Pra-cek Telegram — skill `beta` (lokal, tanpa kirim)

**Tanggal:** 2026-10-12 UTC  
**Penguji:** Akun C (Cursor Cloud)  
**Metode:** `mk-home.sh` + `run-uji-tg.sh` (`--channel telegram`, tanpa `--deliver`), OpenClaw 2026.9.8, VM `$HOME/komunitech-uji`.

| # | Skill | Versi | Skor katalog | Pesan uji | Karakter | Verdik | Alasan singkat |
|---|--------|-------|--------------|-----------|----------|--------|----------------|
| 1 | slip-gaji-bpjs | 1.0.6 | 9 | S1 — slip 3 karyawan CV Contoh Maju Jaya (sama `examples/01-slip-gaji-3-karyawan.md`) | 1.773 | **GAGAL** | Rekap tabel + setoran BPJS/PPh ada di chat dan angka THP total cocok pola uji lokal; **isi slip per karyawan tidak ditampilkan** (hanya path `payroll/.../slip-gaji-2026-09.md|.html`). Di Telegram pembeli awam bisa mengira jawaban “kosong” bila lampiran file tidak terkirim. Saran pembuat: tampilkan minimal 1 slip contoh utuh di chat + tawarkan “balas kirim file” bila panjang. |
| 2 | pph21-ter | 1.0.5 | 9 | S1 — K/1, gaji 12 jt/bulan, THR 12 jt Maret, iuran JHT+JP 360 rb/bulan (sama `examples/01-setahun-dengan-thr.md`) | 1.596 | **LOLOS** | Tabel 12 bulan + blok hitung ulang Desember + ringkasan setahun **utuh di chat**; total PPh Rp 6.402.000 dan Desember Rp 642.000 cocok uji lokal; tidak mengandalkan path file saja. |

**Run berikutnya (C9):** `hitung-thr`, `kontrak-kerja-pkwt`, `presentasi-instan`, `rencana-pelajaran-guru` (skor 9, output panjang).

Output mentah: `$HOME/komunitech-uji/openclaw-real/hasil/pph21-tg-01.txt` (tidak di-commit).
