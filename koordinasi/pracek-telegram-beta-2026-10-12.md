# Pra-cek Telegram — skill `beta` (lokal, tanpa kirim)

**Tanggal:** 2026-10-12 UTC  
**Penguji:** Akun C (Cursor Cloud)  
**Metode:** `mk-home.sh` + `run-uji-tg.sh` (`--channel telegram`, tanpa `--deliver`), OpenClaw 2026.9.8, VM `$HOME/komunitech-uji`.

| # | Skill | Versi | Skor katalog | Pesan uji | Karakter | Verdik | Alasan singkat |
|---|--------|-------|--------------|-----------|----------|--------|----------------|
| 1 | slip-gaji-bpjs | 1.0.6 | 9 | S1 — slip 3 karyawan CV Contoh Maju Jaya (sama `examples/01-slip-gaji-3-karyawan.md`) | 1.773 | **GAGAL** | Rekap tabel + setoran BPJS/PPh ada di chat dan angka THP total cocok pola uji lokal; **isi slip per karyawan tidak ditampilkan** (hanya path `payroll/.../slip-gaji-2026-09.md|.html`). Di Telegram pembeli awam bisa mengira jawaban “kosong” bila lampiran file tidak terkirim. Saran pembuat: tampilkan minimal 1 slip contoh utuh di chat + tawarkan “balas kirim file” bila panjang. |
| 2 | pph21-ter | 1.0.5 | 9 | S1 — K/1, gaji 12 jt/bulan, THR 12 jt Maret, iuran JHT+JP 360 rb/bulan (sama `examples/01-setahun-dengan-thr.md`) | 1.596 | **LOLOS** | Tabel 12 bulan + blok hitung ulang Desember + ringkasan setahun **utuh di chat**; total PPh Rp 6.402.000 dan Desember Rp 642.000 cocok uji lokal; tidak mengandalkan path file saja. |

| 3 | hitung-thr | 1.0.9 | 9 | S1 — THR Lebaran 4 karyawan CV Contoh Maju Jaya (sama `examples/01-thr-lebaran-4-karyawan.md`, CSV `karyawan.csv` di workspace) | 3.757 | **LOLOS** | Tabel rekap 4 orang + total THR Rp 16.908.333 / THR diterima Rp 16.241.833 + draf pengumuman grup (tanpa nominal pribadi) **utuh di chat**; angka cocok skrip `thr.py`. Catatan: ada path file rekap di akhir, tapi isi utama tidak mengandalkan lampiran. |

| 4 | kontrak-kerja-pkwt | 1.0.8 | 9 | S1 — toko roti Bandung, 2 pekerja produksi PKWT 1 tahun (sama `examples/01-susun-toko-roti-bandung.md`) | 10.094 | **LOLOS** | Blok hitung kompensasi (Rp 4.150.000/orang, total Rp 8.300.000) + draf PKWT Pasal 1–12 **utuh di chat**; angka kompensasi cocok `hitung_pkwt.py`; peringatan jam kerja/UMK; tidak mengandalkan path file saja. |

| 5 | presentasi-instan | 1.1.5 | 8 | S1 — pitch deck Bersih Kilat laundry (sama `examples/01-pitch-investor-laundry.md`) | 1.761 | **LOLOS** | Cara pakai (browser/PDF/edit) + daftar 13 slide dengan angka traksi & dana (Rp 38 jt, 620 pelanggan, Rp 450 jt / 15% / valuasi Rp 3 m) + asumsi & checklist **di chat**; tidak mengandalkan path file saja; HTML dibuat di workspace tapi ringkasan siap baca untuk pembeli awam di Telegram. |

**Run berikutnya (C9):** `rencana-pelajaran-guru`, `presentasi-data-ke-atasan`, `surat-resmi` (skor 9, output panjang); **C11** `cari-prospek-web` bot asli masih antre.

Output mentah: `$HOME/komunitech-uji/openclaw-real/hasil/sgb-tg-01-out.txt` (tidak di-commit).

## slip-gaji-bpjs 1.0.7 — pra-cek ulang Akun B (2026-10-12)

**Penguji:** Akun B. **Metode:** `mk-home.sh sgb7-<n> slip-gaji-bpjs` + `uji-tg.sh` (`--channel telegram`, tanpa `--deliver`, tidak ada yang dikirim), OpenClaw bot uji, skill 1.0.7 saja. Angka diverifikasi dengan menjalankan `scripts/payroll.py` pada data yang sama (3 dan 4 karyawan, UMK 5.396.761, JKK 0,54%).

| # | Skill | Versi | Pesan uji | Karakter | Alat | Durasi | Verdik | Alasan singkat |
|---|-------|-------|-----------|----------|------|--------|--------|----------------|
| 1 | slip-gaji-bpjs | 1.0.7 | S1 — 3 karyawan CV Contoh Maju Jaya (data `examples/01`, ditulis sebagai chat awam) | 3.331 | tool_search, read, exec, write | 205 dtk | **LOLOS** | 3 slip utuh teks rata (tanpa tabel/kode) + rekap total, setoran BPJS Kes Rp 1.069.838 / BPJS TK Rp 2.012.940 / PPh Rp 444.350, peringatan UMK Siti, asumsi, disclaimer, ditutup tawaran "kirim file". THP 6.521.091 / 5.264.239 / 10.521.618, biaya total Rp 26.184.076 cocok persis dengan skrip. Tidak ada path/nama file. Skill terpicu. |
| 2 | slip-gaji-bpjs | 1.0.7 | Data sama + karyawan fiktif ke-4 (Rina Wulandari, K/0, Kasir, gapok 5,2 jt, tunj. 300 rb, makan 500 rb, lembur 1+1 jam, kasbon 50 rb) | 2.933 | tool_search, skills_read, tool_call, ls, read, write, exec | 78 dtk | **LOLOS** | 3 slip pertama utuh + satu baris untuk Rina (THP Rp 5.761.761, biaya Rp 6.675.076) + rekap 4 karyawan (biaya total Rp 32.859.152; BPJS Kes Rp 1.344.838; BPJS TK Rp 2.537.640; PPh Rp 507.965) + tawaran "balas kirim file". Semua angka cocok dengan skrip. Tidak ada path (hanya "folder kerja asisten"). Catatan kecil: akhir balasan menawarkan menghapus CSV data karyawan buatannya (tidak mengganggu). |

**Isi run 1:** slip Budi, Siti, Dewi masing-masing berurutan dengan blok PENDAPATAN, POTONGAN, TAKE HOME PAY, dan baris "Ditanggung perusahaan" (plus rincian lembur untuk Budi dan Dewi); lalu rekap total 3 karyawan, tiga setoran, batas upah JP, asumsi, pembulatan, satu peringatan UMK, disclaimer, tawaran "kirim file".

**Isi run 2:** tiga slip utuh (Budi, Siti, Dewi, tanpa rincian lembur), lalu satu baris ringkas Rina, rekap total 4 karyawan, peringatan UMK, asumsi, pembulatan, kalimat bahwa file tersimpan di folder kerja asisten + tawaran "balas kirim file".

**Kesimpulan:** 1.0.7 memperbaiki kegagalan 1.0.6 (slip kini tampil utuh di chat). Layak masuk gelombang Telegram.

Output mentah: `scratchpad/openclaw-real/hasil/sgb7-1-out.txt`, `sgb7-2-out.txt` (tidak di-commit).
Output mentah: `$HOME/komunitech-uji/openclaw-real/hasil/pph21-tg-01.txt` (tidak di-commit).
Output mentah: `$HOME/komunitech-uji/openclaw-real/hasil/pkwt-tg-01-out.txt` (tidak di-commit).
Output mentah: `$HOME/komunitech-uji/openclaw-real/hasil/pins-tg-01-out.txt` (tidak di-commit).
