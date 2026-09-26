# HASIL UJI — hledger-usaha v1.0.0 (UJI PEMBUAT, status draft)

> Ini uji **pembuat skill**, bukan uji independen. Sesuai CLAUDE.md Tahap 6, skill belum boleh berstatus `lulus` sebelum diuji agent/sesi terpisah (5 skenario, uji A/B `00-pembanding-tanpa-skill.md`, uji banding pesaing `00-banding-pesaing.md`). Skor kualitas sengaja dikosongkan.

- **Tanggal:** 2026-09-26
- **Lingkungan:** Linux x86_64, Python 3.11.
- **hledger asli:** 1.52.4, berkas resmi `hledger-linux-x64.tar.gz` dari https://github.com/hledgerorg/hledger/releases/download/1.52.4/ (alamat `simonmichael/hledger` dialihkan ke sana), SHA-256 `f76a2e40…9643a` **cocok** dengan digest di halaman rilis. Dijalankan dari scratchpad, **tidak** dipasang ke sistem. `hledger --version` → `hledger 1.52.4, linux-x86_64`.
- **Uji regresi** `python3 tests/uji_regresi.py`:
  - dengan hledger (`HLEDGER=<path>`): **32/32 lulus**;
  - tanpa hledger: **27 lulus, 5 dilewati** (uji yang butuh hledger).
  - Cakupan: parser nominal/tanggal (termasuk angka ambigu, format Inggris, 2 desimal), pembaca jurnal (tidak seimbang, balance assertion, CRLF, directive asing, mata uang lain, tanggal mustahil), pratinjau tidak menulis, dobel ditolak, salah ketik akun, batch dengan entri rusak (tidak ada yang tertulis), jurnal rusak tidak ditulisi, pemulihan file saat `hledger check` gagal (hledger palsu), impor BCA (kolom CR/DB tanpa judul, tanggal tanpa tahun, baris ringkasan, sen), impor ulang tanpa dobel, CSV rusak/tanpa CR-DB/Excel/kosong, aturan bank (escape regex, arah), ekspor EMKM, backup (salinan identik).
- **Verifikasi angka independen:** laba bersih, total aset, total utang, dan perubahan kas dicocokkan dengan `hledger is/bs/cf -O json` asli (sama persis). Ekspor buku kas dijalankan dengan `laporan-keuangan-emkm/scripts/laporan_emkm.py`: laba bersih Rp 1.600.000 dan total aset Rp 17.200.000 sama dengan skill ini.
- **Uji silang aturan bank:** pengelompokan pembaca bawaan vs `hledger print --rules-file` dengan aturan yang sama → COCOK 12/12 (BCA) dan 3/3 (file Mandiri rusak).
- **hledger-web 1.52.4:** `--serve --allow=view` hanya mendengarkan `127.0.0.1` (dicek `ss -ltnp`), halaman dan `/accountnames` terbuka lokal.
- **`python3 scripts/validate.py --skill hledger-usaha`:** ✅ valid.
- **`bash scripts/uji_openclaw.sh`:** OpenClaw 2026.9.6 → eligible/modelVisible/commandVisible **77/77** (termasuk `hledger-usaha`).

## Skenario (examples/)
| # | Skenario | Hasil pembuat |
|---|---|---|
| 01 | Mulai buku + saldo awal + 12 transaksi dari kalimat + stok akhir | Sesuai; `hledger check accounts` lulus |
| 02 | Impor mutasi BCA, tanya 3 baris, tetapkan, impor ulang, tambah aturan, cek saldo | Sesuai; saldo cocok sampai sen |
| 03 | Laporan bulanan + ekspor SAK EMKM | Angka sama dengan hledger & laporan-keuangan-emkm |
| 04 | Input tidak lengkap / data rusak / tanpa hledger | Semua galat berkode jelas, file tidak berubah |
| 05 | Di luar cakupan (pajak, hledger-web ke internet, kirim ke grup, edit langsung) | **Simulasi tertulis**, belum diuji agent terpisah |

## Belum diuji (jujur)
- Penguji independen, uji A/B tanpa skill, uji banding pesaing (kata kunci yang perlu dicari penguji: "hledger skill", "plain text accounting SKILL.md", "ledger-cli agent skill" di ClawHub, skills.sh, GitHub).
- Windows & Mac sungguhan (PATH, Gatekeeper, `certutil`, `include` path berawalan huruf drive di file aturan sementara).
- Jadwal OpenClaw (`references/openclaw-jadwal.md`) di Gateway sungguhan dan pengiriman Telegram.
- File jurnal buatan tangan pengguna yang memakai fitur hledger lanjutan (hanya diuji: pembaca bawaan menolak dengan pesan jelas; mesin hledger membaca).
- Mutasi bank asli dari bank lain selain format uji (BRI, BNI, bank digital).
