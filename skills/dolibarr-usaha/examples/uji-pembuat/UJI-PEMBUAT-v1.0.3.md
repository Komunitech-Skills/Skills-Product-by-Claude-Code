# Catatan pembuat — dolibarr-usaha v1.0.3 (2026-09-25)

- **Penulis:** pembuat/perbaikan (Claude Code, agent pembuat). **Bukan** uji independen; skor kualitas tidak diberikan di sini. Status katalog: `uji` (menunggu uji ulang independen).
- **Lingkungan:** Linux, Python 3.11.15, server Dolibarr **tiruan** dari `tests/uji_regresi.py` (bentuk respons dari rekaman asli 24.0.1). **Tidak** diuji ulang di Dolibarr asli pada versi ini.
- **Data uji:** scratchpad sesi (di luar repo): skrip reproduksi `repro.py`, keluaran `repro-v1.0.2.txt` / `repro-v1.0.3.txt`, salinan skrip v1.0.2 untuk membuktikan tes regresi gagal pada versi lama.
- **Sumber temuan:** `HASIL-UJI.md` bagian "Uji ulang v1.0.2" (B1, B2).

## B1 — draf invoice ganda saat DPP bersen

**Reproduksi (v1.0.2, server tiruan):** pelanggan ID 1, `--item "Kain|3|10.333|7,5" --item "Ongkir|1|15000,50" --ya` dua kali → dua draf, `(PROV101)` dan `(PROV102)`, keduanya kode 0. Seharusnya percobaan kedua ditahan (kode 7).

**Akar masalah:** pencegah dobel membandingkan `total_ht` draf yang sudah ada di Dolibarr **secara persis** dengan DPP Komunitech. Keduanya memakai aturan pembulatan berbeda:
- Dolibarr menyimpan total per baris dengan **2 desimal** (sen): 3 × 10.333 × 92,5% = 28.674,075 → 28.674,08; ongkir 15.000,50 → total_ht **43.674,58**.
- Standar Komunitech (pedoman kurasi Komunitech Tahap 4) membulatkan total baris ke **rupiah terdekat**: 28.674 + 15.001 = **43.675**.

`43.674,58 ≠ 43.675`, jadi draf lama tidak pernah dikenali sebagai kembar setiap kali ada baris bersen (diskon, harga ,50, harga produk Rp 83.333,33). DPP bulat tetap tertahan karena kedua cara menghasilkan angka sama.

**Perbaikan (`scripts/dolibarr.py`):**
- Fungsi baru `dpp_cara_dolibarr(items)`: jumlah total baris yang dibulatkan ke 2 desimal (half-up) per baris, meniru angka yang disimpan Dolibarr. Hanya dipakai untuk mengenali kembar; **tidak** mengubah hitungan DPP/PPN/total Komunitech.
- Fungsi baru `draf_kembar(draf, items, dpp)`: draf dianggap kembar bila `total_ht` berselisih **kurang dari Rp 1** dari DPP Komunitech **atau** dari DPP cara Dolibarr. Dua acuan dibutuhkan karena selisih pembulatan menumpuk per baris (10 baris × Rp 100,50: Dolibarr 1.005,00 vs Komunitech 1.010, selisih Rp 5); toleransi < Rp 1 menutup pengaturan "Maks. desimal harga total" yang berbeda.
- Standar pembulatan tidak berubah: total baris ke rupiah terdekat, PPN dari DPP persis lalu dibulatkan ke bawah sekali (cek: 10 × 100,50 → DPP 1.010, PPN floor(111,10) = 111).

**Hasil setelah perbaikan:** repro yang sama → percobaan kedua `DRAF INVOICE TIDAK DIBUAT (kemungkinan dobel)`, kode 7, tanpa POST tambahan; `--tetap-buat` tetap bisa membuat `(PROV102)`.

## B2 — ENV `DOLIBARR_API_KEY` diam-diam mengalahkan `--kunci-file`

**Reproduksi (v1.0.2):** ENV `DOLIBARR_API_KEY` = kunci tulis, `cek --kunci-file <file berisi kunci baca>` → semua permintaan memakai kunci **tulis** (ENV), keluaran "dari ENV DOLIBARR_API_KEY", stderr kosong.

**Akar masalah:** `baca_kunci()` selalu memeriksa ENV `DOLIBARR_API_KEY` lebih dulu dan langsung kembali bila terisi; argumen `--kunci-file` baru dipakai jika ENV kosong. Nilai eksplisit pengguna kalah dari nilai lingkungan yang mungkin lupa dikosongkan, sehingga pemisahan kunci baca/draf (panduan §6) bisa jebol tanpa tanda.

**Perbaikan:**
- Urutan baru: `--kunci-file` (eksplisit, selalu menang) → ENV `DOLIBARR_API_KEY` → ENV `DOLIBARR_API_KEY_FILE` → file default.
- Bila `--kunci-file` dan ENV sama-sama ada: stderr `PERINGATAN: ENV DOLIBARR_API_KEY juga terisi, tetapi DIABAIKAN karena --kunci-file diberikan. Kunci yang dipakai: file …`; pada `--json` juga ada field `peringatan_kunci` (stdout tetap JSON sah).
- Isi ENV yang diabaikan tetap didaftarkan sebagai rahasia (tidak pernah tercetak), tetapi tidak divalidasi (ENV rusak tidak menggagalkan perintah).
- `--kunci-file` yang tidak ada atau kosong → kode 5 dengan pesan jelas; **tidak** jatuh ke kunci ENV/default dan tidak menghubungi Dolibarr.
- Tanpa `--kunci-file`, perilaku lama tidak berubah (ENV menang atas `DOLIBARR_API_KEY_FILE`, tanpa peringatan).

## Tes regresi baru (7) — `tests/uji_regresi.py`
| Tes | Isi |
|---|---|
| `test_b1_draf_ganda_dpp_bersen_ditahan` | Repro asli: DPP kita 43.675 vs Dolibarr 43.674,58; ulangan → kode 7, 0 POST; `--tetap-buat` → `(PROV102)` |
| `test_b1_harga_produk_bersen_dan_diskon_setengah` | 3 × 83.333,33; 25.001 diskon 50%; 10 baris × 100,50 (selisih Rp 5) → semua ditahan |
| `test_b1_jumlah_berbeda_tidak_dianggap_kembar` | Selisih ≥ Rp 1 atau pelanggan lain → tetap dibuat (tidak terlalu ketat) |
| `test_b2_kunci_file_eksplisit_menang_atas_env` | Opsi di depan & belakang: semua permintaan pakai kunci file + PERINGATAN; perintah tulis dengan kunci baca ditolak Dolibarr, bukan diam-diam memakai kunci tulis ENV |
| `test_b2_json_memuat_peringatan_dan_stdout_tetap_json` | `--json`: `peringatan_kunci` ada, stdout tetap JSON |
| `test_b2_kunci_file_hilang_tidak_jatuh_ke_env` | File hilang/kosong → kode 5, 0 permintaan ke Dolibarr |
| `test_b2_tanpa_kunci_file_env_tetap_dipakai_tanpa_peringatan` | Perilaku lama tanpa `--kunci-file`; ENV rusak + `--kunci-file` → tidak tercetak |

- Pada skrip **v1.0.2**: 6 dari 7 tes baru gagal (5 FAIL, 1 ERROR). Yang lolos adalah `test_b1_jumlah_berbeda_tidak_dianggap_kembar`, penjaga agar perbaikan tidak terlalu longgar.
- Pada **v1.0.3**: `python3 tests/uji_regresi.py` → **77 tes OK** (70 lama + 7 baru).
- `python3 scripts/validate.py` → **65 skill valid, 65 baris katalog sesuai**.

## Dokumentasi
- `docs/panduan-dolibarr.md`: bagian baru **2.4 Pengamanan wajib** (ganti sandi database bawaan `changeme`, pastikan hanya bisa dibuka dari komputer sendiri/localhost + uji dari HP di Wi-Fi yang sama, jangan buka ke internet; jasa setup Komunitech sebagai opsi); catatan Linux/macOS; §10 dan penutup merujuk 2.4; kalimat tidak berafiliasi dengan Dolibarr. Langkah Windows ditandai jujur "belum dicoba langsung".
- `README.md`: status 1.0.3, rujukan ke pengamanan 2.4, kalimat tidak berafiliasi.
- `SKILL.md`: versi 1.0.3, urutan sumber kunci, arti "jumlah sama" (toleransi < Rp 1), dua baris baru di tabel galat.
- `scripts/dolibarr.py`: `VERSI_SKRIP = "1.0.3"`, bantuan `--kunci-file`.

## Belum dilakukan / untuk penguji independen
- Uji ulang B1 di **Dolibarr asli** (draf 3 baris dengan diskon 4% & 7,5% + ongkir bersen dari `07-uji-ulang-v1.0.2.md`, diulang `--ya`).
- Uji B2 dengan dua user API asli (kunci baca di file, kunci draf di ENV).
- Uji muat OpenClaw (`scripts/uji_openclaw.sh`) tidak dijalankan ulang oleh pembuat pada versi ini.
- Kosmetik lain dari uji v1.0.2 (metavar `_T0_…`, `simpan-kunci` tidak membaca `DOLIBARR_API_KEY_FILE`, dll.) belum disentuh.
