# 08 — Uji ulang independen v1.0.3 (Akun B)

- **Tanggal:** 2026-09-25
- **Penguji:** agent penguji independen lintas akun (Akun B, Claude Code, simulasi agent). Bukan pembuat skill maupun pembuat perbaikan v1.0.3. Catatan pembuat (`uji-pembuat/UJI-PEMBUAT-v1.0.3.md`) hanya dibaca sebagai klaim yang diuji, tidak dijadikan dasar nilai.
- **Objek:** `skills/dolibarr-usaha` v1.0.3 (commit `dc401a4`), disalin ke scratchpad `uji-doli/` dan dijalankan dari salinan itu. `HOME` palsu per uji.
- **Lingkungan:** Linux, Python 3.11.15. **Tidak ada Dolibarr asli** di uji ini: server tiruan = turunan kelas `Tiruan` dari `tests/uji_regresi.py` (bentuk respons dari `tests/fixtures/dolibarr-24.0.1.json`; baris invoice dihitung seperti Dolibarr: total baris 2 desimal half-up per baris) ditambah mode buatan penguji: koneksi putus setelah draf dibuat, timeout `POST invoices`, timeout `POST invoices/{id}/lines`, timeout baca ulang akhir. Untuk uji timeout, `BATAS_WAKTU` script diturunkan ke 1,5 detik lewat pembungkus (kode script tidak diubah).
- **Alat penguji (di luar repo):** `scratchpad/uji-doli/uji_b1b2.py` (62 pemeriksaan), `satu.py` (rincian timeout), keluaran `hasil-uji-b1b2.txt`.
- **Hitung ulang independen:** kalkulator penguji memakai `fractions.Fraction` (nilai persis) → total baris half-up ke rupiah, DPP, PPN = floor(DPP × 12% × 11/12) sekali, DPP nilai lain 11/12 (2 desimal, informasi), dan "DPP cara Dolibarr" (half-up ke sen per baris). Tidak memakai fungsi apa pun dari `dolibarr.py`.

## 1. B1 — draf ganda saat DPP bersen

### 1a. Angka (pratinjau, 0 POST) — Komunitech vs kalkulator penguji
| Skenario | Item | Jenis PPN | DPP | PPN (persis → floor) | Total | DPP 11/12 | Dolibarr `total_ht` (tiruan) = DPP cara Dolibarr penguji | Beda |
|---|---|---|---|---|---|---|---|---|
| A (repro asli uji v1.0.2 di Dolibarr asli) | 15 × 62.500 disk 4%; 3 × 87.500 disk 7,5%; 1 × 137.345 | umum | 1.280.158 | 140.817,38 → **140.817** | 1.420.975 | 1.173.478,17 | 1.280.157,50 (= angka Dolibarr asli di `07-…`) | **0** |
| B (repro pembuat) | 3 × 10.333 disk 7,5%; 1 × 15.000,50 | umum | 43.675 | 4.804,25 → **4.804** | 48.479 | 40.035,42 | 43.674,58 | **0** |
| C harga bersen | 3 × 83.333,33; 2,5 × 62.500,50 | mewah | 406.251 | 48.750,12 → **48.750** | 455.001 | – | 406.251,24 | **0** |
| D 10 baris | 10 × (1 × 100,50) | umum | 1.010 | 111,10 → **111** | 1.121 | 925,83 | 1.005,00 (selisih Rp 5) | **0** |
| E jasa | 7 × 33.333,33 disk 12,5% | tanpa | 204.167 | 0 | 204.167 | – | 204.166,65 | **0** |
| F qty desimal | 1,75 × 99.999,99 disk 33,33%; 0,5 × 1 | umum | 116.673 | 12.834,03 → **12.834** | 129.507 | 106.950,25 | 116.672,99 | **0** |

Standar pedoman kurasi Komunitech dipatuhi: PPN dari DPP persis (bukan dari DPP 11/12 yang sudah dibulatkan), dibulatkan ke bawah **sekali**; total baris ke rupiah terdekat. `dpp_cara_dolibarr` script = hitungan sen penguji di keenam skenario, dan untuk skenario A sama dengan angka **Dolibarr 24.0.1 asli** yang dicatat penguji v1.0.2 (1.280.157,50).

### 1b. Idempotensi perintah yang diulang
| Uji | Hasil |
|---|---|
| A–F: `--ya` sekali (kode 0) lalu perintah identik diulang **3×** | ✅ kode `[7,7,7]`, **0 POST tambahan**, tetap 1 draf baru (+ draf fixture PROV4 milik pelanggan yang sama, jumlah lain, tidak ikut tertahan) |
| A–F: urutan item dibalik | ✅ tertahan (kode 7) |
| Batas toleransi: draf 43.674,58 vs item baru 43.675,57 / 43.673,59 | ✅ tertahan (kode 7) |
| … vs 43.675,58 / 43.673,49 | ✅ dibuat (kode 0) — tidak terlalu longgar |
| … vs 43.673,58 (beda tepat Rp 1 dari draf) | ⚠️ tertahan, karena DPP Komunitech item baru = 43.674 dan \|43.674,58 − 43.674\| < 1. Toleransi efektif sampai ± Rp 1,49; aman (hanya meminta konfirmasi `--tetap-buat`) |
| Isi berbeda, DPP sama (1 × 50.000 vs 2 × 25.000) | tertahan (kode 7) — sesuai desain "jumlah sama", agent diminta bertanya dulu |
| Invoice identik yang sudah divalidasi (bukan draf) | ✅ tidak menghalangi (kode 0) |

### 1c. Idempotensi saat timeout / koneksi putus (baru, tidak diuji pembuat)
| Kejadian (server tiruan) | Perintah 1 | Ulang perintah yang sama | Hasil |
|---|---|---|---|
| Timeout saat baca ulang akhir (`GET invoices/{id}`) | kode 3 "tidak menjawab… coba lagi"; draf lengkap sudah ada | kode **7** (tertahan) | ✅ tidak ganda |
| Koneksi putus setelah Dolibarr membuat draf (`POST invoices`) | kode 3 "coba lagi"; draf **kosong Rp 0** sudah ada | kode 0 → draf kedua dibuat | ❌ **draf kosong yatim** + draf baru; pesan pertama tidak menyebut kemungkinan draf sudah dibuat |
| Timeout `POST invoices` (server tetap membuat) | sama seperti di atas | kode 0 | ❌ sama |
| Timeout `POST invoices/{id}/lines` baris 1 (server tetap menambah baris) | **kode 0**; teks "baris 1 gagal ditambahkan… Draf berisi baris sebelumnya saja", padahal Dolibarr menunjukkan baris 1 **ada** (DPP 900.000); disertai penjelasan "Selisih DPP: … sen" untuk selisih Rp 380.158 dan penutup "periksa draf > Validasi" | kode 0 → draf kedua | ⚠️/❌ draf sebagian + draf baru |

Kesimpulan B1: **perbaikan inti terbukti** (perintah identik yang diulang tidak lagi membuat draf ganda, untuk 6 pola bersen termasuk repro asli). **Belum idempoten terhadap timeout/putus** di tengah pembuatan (temuan baru **C1**, di bawah).

## 2. B2 — ENV `DOLIBARR_API_KEY` vs `--kunci-file`
Kunci uji palsu dari `tests/uji_regresi.py` (tidak ada kunci nyata). Server tiruan mencatat header `DOLAPIKEY` setiap permintaan.

| Uji | Hasil |
|---|---|
| ENV = kunci tulis, `--kunci-file` = kunci baca, opsi di **depan** dan **belakang** | ✅ semua permintaan memakai kunci file; stderr `PERINGATAN: ENV DOLIBARR_API_KEY juga terisi, tetapi DIABAIKAN…` |
| ENV sama persis dengan isi file | ✅ tetap diberi PERINGATAN (tidak masalah) |
| `--kunci-file` vs ENV `DOLIBARR_API_KEY_FILE` | ✅ `--kunci-file` menang |
| Tanpa `--kunci-file`: ENV KEY vs ENV KEY_FILE | ✅ ENV KEY menang, tanpa peringatan (sesuai urutan di SKILL.md) |
| ENV hanya spasi + `--kunci-file` | ✅ tanpa peringatan palsu |
| Perintah tulis (`invoice buat --ya`) dengan kunci baca di file + kunci tulis di ENV | ✅ ditolak Dolibarr (403 → kode 5), tidak diam-diam memakai kunci tulis; `--json` tetap JSON sah |
| Data rusak di `--kunci-file`: izin 644, 2 baris, biner, path folder, path hilang, `~/` hilang | ✅ kode 5, **0 permintaan** ke Dolibarr (tidak jatuh ke kunci ENV), 0 traceback |
| ENV multi-baris diabaikan karena `--kunci-file` | ✅ tidak tercetak, tidak pernah dikirim ke server |
| `--kunci-file ""` (string kosong) | ⚠️ dianggap tidak diisi → diam-diam memakai ENV (kode 5 dari 401 pada uji ini); kosmetik |
| `--json` + perintah gagal | ⚠️ `peringatan_kunci` hanya di stderr, tidak ada di JSON galat; kosmetik |
| Kebocoran: 72 keluaran (stdout+stderr) seluruh uji B1/B2 | ✅ **0** kunci utuh, 0 potongan baris kedua kunci rusak, 0 `Traceback` |

Kesimpulan B2: **beres**; urutan terdokumentasi (SKILL.md Persiapan 2, docstring, `--help`) dipatuhi dan ada peringatan.

## 3. `docs/panduan-dolibarr.md` §2.4 "Pengamanan wajib" vs perilaku script (baca saja)
| Butir | Panduan | Perilaku script (diuji) | Status |
|---|---|---|---|
| Hanya komputer ini / jangan ke internet | §2.4 langkah 2–3, §10.1 | `http://192.168.1.10` ditolak tanpa `--izinkan-url-luar` (kode 2); alamat internet `http://` ditolak walau diizinkan; `user:pw@` di URL ditolak; `127.0.0.2.nip.io` dianggap luar | ✅ konsisten |
| HTTPS untuk akses dari luar | §2.4 langkah 3, §10.1 | wajib `https://` untuk alamat publik; LAN `http` hanya dengan opt-in + PERINGATAN | ✅ |
| Izin minimum kunci API | §6 (dirujuk §10.4), bukan §2.4 | kunci baca untuk jadwal, kunci draf terpisah via `--kunci-file`; B2 kini menjamin `--kunci-file` tidak dikalahkan ENV | ✅ (B2 menutup celah yang dulu membuat pemisahan ini bisa jebol) |
| Kunci tidak di repo / riwayat shell | §7 (`simpan-kunci`, kunci ditempel tak terlihat), larangan tempel di chat | `simpan-kunci` membaca lewat `getpass`/stdin (tidak lewat argumen → tidak masuk riwayat shell), file `~/.komunitech/…` 600/folder 700 di luar folder skill; file 644 ditolak; tidak ada string mirip kunci di folder skill/panduan | ✅ |
| Sandi DB `changeme`, firewall, uji HP | §2.4 langkah 1–2 | di luar jangkauan script (tidak diklaim script memeriksa) | ✅ tidak ada klaim palsu |
- Catatan kecil: §7 langkah 1 menyebut user `api_komunitech`, padahal §6 menamai `api_baca`/`api_draf` (sudah ada sejak versi awal). SKILL.md menyebut "Alternatif: ENV `DOLIBARR_API_KEY`" tanpa pengingat bahwa mengetik kunci di `setx`/`export` bisa masuk riwayat shell; panduan sendiri tidak menyarankan cara itu.
- Langkah Windows §2.4 tidak bisa diverifikasi di sini (jujur ditandai "belum dicoba langsung" di panduan).

## 4. Tes otomatis
- `python3 tests/uji_regresi.py` (di salinan scratchpad): **77 tes OK** (1 dilewati: tes khusus repo pengembang, wajar di salinan).
- `python3 scripts/validate.py --skill dolibarr-usaha` (root repo): **✅ 1 skill valid, 68 baris katalog sesuai**.
- `bash scripts/uji_openclaw.sh`: tidak dijalankan (sesuai instruksi; dijalankan penguji pimpinan Akun B).

## 5. Temuan
| ID | Keparahan | Lokasi | Temuan & saran |
|---|---|---|---|
| **C1** | Sedang-rendah (baru terlihat karena B1 kini beres) | `dolibarr.py` `cmd_invoice_buat` (±895–925), pesan timeout `Dolibarr.minta` | Timeout/putus **setelah** Dolibarr membuat draf (`POST invoices`) → kode 3 dengan saran "coba lagi"; draf kosong Rp 0 tertinggal dan tidak dikenali saat diulang → draf kedua. Timeout saat menambah baris → kode 0, teks "baris N gagal… berisi baris sebelumnya saja" bisa keliru (baris itu mungkin sudah masuk), penjelasan "selisih sen" dan penutup "Validasi" tidak cocok untuk draf sebagian. Saran: (1) sebelum membuat, anggap juga draf pelanggan yang sama ber-`total_ht` 0 / bercatatan "Draf dibuat oleh skill dolibarr-usaha" yang dibuat beberapa menit terakhir sebagai kemungkinan dobel; atau setelah galat koneksi pada POST, baca ulang daftar draf dan laporkan; (2) pesan galat koneksi pada perintah tulis: "draf mungkin sudah terbuat, cek Dolibarr sebelum mengulang"; (3) draf sebagian → kode bukan 0 dan tanpa kalimat "Validasi". |
| K-a | Kosmetik | `baca_kunci` | `--kunci-file ""` dianggap tidak diisi → pakai ENV tanpa peringatan. |
| K-b | Kosmetik | `main` | `peringatan_kunci` tidak masuk JSON galat (`--json` + gagal). |
| K-c | Kosmetik | `draf_kembar` | Toleransi efektif s.d. ± Rp 1,49 terhadap draf (karena salah satu acuan adalah DPP yang dibulatkan); SKILL.md menyebut "< Rp 1". Dampak hanya meminta konfirmasi. |
| K-d | Kosmetik | panduan §7 | `api_komunitech` vs `api_baca`/`api_draf`. |

## 6. Batasan uji
Tanpa Dolibarr asli: toleransi B1 diperiksa terhadap aturan pembulatan tiruan (2 desimal per baris), yang cocok dengan satu data asli (skenario A). Pengaturan Dolibarr "Maks. desimal harga total" selain 2, diskon global, dan DoliWamp Windows tidak diuji. Perilaku timeout disimulasikan (server menunda/menutup koneksi), bukan diamati di Dolibarr asli.
