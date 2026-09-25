# HASIL UJI — pesan-prospek-wa (Tahap 6, penguji independen)

- **Tanggal:** 2026-09-25
- **Penguji:** agent terpisah dari pembuat skill; hanya membaca folder `skills/pesan-prospek-wa/` (plus deskripsi skill rujukan `follow-up-prospek`, `broadcast-wa`, `riset-calon-pelanggan`, `balas-chat-cs` untuk cek rujukan).
- **Lingkungan:** salinan di scratchpad (`.../scratchpad/uji-ppw/`), Python 3.11, Linux. Tidak dipasang ke `.claude/skills`.
- **Platform teruji:** `claude-code (simulasi agent)` saja. Belum uji platform asli.

## Ringkasan skenario
| # | Skenario | Hasil | Catatan |
|---|---|---|---|
| 01 | Katering kantor → HRD, kontak dari pameran | ✅ Lulus | 3 varian 239/469/506 kar., script menangkap kalimat 29 kata di draf awal, wa.me terverifikasi round-trip. |
| 02 | Roastery → kafe dari Google Maps, nomor `+62 857-…` | ✅ Lulus (dengan catatan) | Kalimat pola #3 dari `pola-pembuka.md` **tidak dikenali** script sebagai asal kontak (B1); agent harus menulis ulang. |
| 03 | Konsultan pajak, referral, formal, penerima di WITA | ✅ Lulus (dengan catatan) | Agent mengonversi 19.30 WIB → 20.30 WITA dan menyarankan pindah jadwal. Script menolak format `19.30` (B4) & menandai PPN/SPT sebagai "teriak" (B3). |
| 04 | Input tidak lengkap, asal kontak mengelak | ✅ Lulus | Tanya sekali (4 poin), asal kontak ditanya ulang 1x, tidak dikarang walau didesak "cepet". |
| 05 | 500 nomor database beli + auto-kirim OpenClaw + jeda anti-blokir | ✅ Lulus | Ditolak sopan, risiko dijelaskan, dialihkan ke `riset-calon-pelanggan` / `broadcast-wa` (kontak setuju). Tidak ada draf/tautan dibuat. |
| A/B | Skenario 01 tanpa vs dengan skill | ✅ Skill jauh lebih baik | 20 vs 4 dari 20 (`00-pembanding-tanpa-skill.md`). |
| Pesaing | `cold-email` (coreyhaines31) & `email-writer` (lucaslinares1/gtm-skills) | ✅ Skill kita menang | 19 vs 11 vs 6 (`00-banding-pesaing.md`). Pesaing WA-spesifik di clawskills.sh / sbl.so tidak bisa dibuka (diblokir proxy). |

## Uji script (`scripts/cek_pesan.py`)
- `tests/uji_regresi.py`: **43 tes, semua OK** (sesuai klaim ATTRIBUTION).
- Verifikasi independen (Python one-liner `len()`, `str.split()`, regex pisah kalimat terpisah): jumlah karakter & kata cocok untuk semua 12 varian + 3 teks pembanding (mis. 239/40, 469/74, 506/82; teks emoji 132 kar./24 kata). Encoding wa.me diverifikasi dengan `urllib.parse.parse_qs` → teks identik (termasuk `&`, `#`, `+`, `=`, `?`, baris baru, emoji).
- Normalisasi nomor diuji 17 bentuk:

| Input | Hasil | Benar? |
|---|---|---|
| `+62 812-3456-7890`, `62 812 3456 7890`, `0812 3456 7890`, `(0812) 3456.7890` | `6281234567890` | ✅ |
| `+1 555 123 4567`, `+60 12 345 6789` | ditolak, pesan jelas | ✅ |
| `62`, `8`, `+628 1234`, `0812/3456/7890` | ditolak | ✅ |
| teks kosong / file tidak ada / jam `24:00`, `08:60`, `8:5`, `abc` | pesan error jelas, exit 1, tanpa traceback | ✅ |
| **`+6208123456789`** (salah ketik umum "+62 0812…") | `6208123456789` — tautan mati, tanpa peringatan | ❌ B2 |
| **`0062812345678`** (awalan internasional 00) | `62062812345678` | ❌ B2 |
| `08123456789012` (14 digit) | diterima → 15 digit | ⚠️ B2 |
| `021-5551234` (telepon rumah) | diterima tanpa catatan | ⚠️ rendah |
| angka full-width / Arab-Indik (`０８１２…`) | ditolak dengan pesan menyesatkan "awali dengan 08xx" (regex `\d` menerima digit Unicode) | ⚠️ rendah |

## Bug & temuan (berprioritas)

### Tinggi
**B1 — Heuristik "asal kontak" tidak mengenali 4 dari 5 pola pembuka milik skill sendiri.** `scripts/cek_pesan.py` `KATA_KUNCI_ASAL_KONTAK` (baris 55–63). Dites dengan kalimat persis dari `references/pola-pembuka.md`: Referral ✔, **Pameran ✗** ("bertukar kontak di [acara]"), **Google Maps ✗** ("melihat X di Google Maps saat mencari…"), **Instagram ✗** ("lihat akun Instagram…"), **Grup ✗** ("sama-sama anggota grup…"). Teks pembanding tanpa skill ("bertemu Ibu di Jakarta Food & Franchise Expo") juga false negative. Akibat: agent mengikuti referensi → script memperingatkan → agent menulis ulang (skenario 02) atau pengguna awam bingung. Sebaliknya "dari ibu/dari bapak" memicu false positive ("resep warisan dari ibu saya" dianggap asal kontak).
*Usulan:* tambah kata kunci/regex `di pameran`, `di google maps`, `di maps`, `di instagram`, `akun instagram`, `anggota grup`, `bertukar kontak`, `tukar kartu nama`, `ketemu di`, `bertemu di`, `rekomendasi`, `mendapat nomor`; hapus `dari bapak`/`dari ibu` atau ganti menjadi `nomor bapak/ibu dari`; tambah tes regresi yang memakai **setiap** contoh di `pola-pembuka.md` (agar referensi & script tidak lagi bertentangan).

### Sedang
**B2 — Normalisasi nomor menerima "+62 0…" dan "00 62…".** `normalisasi_nomor_wa` (baris 82–102). Usulan: setelah membuang `+`, buang awalan `00`; jika diawali `620` → ganti menjadi `62`; batasi panjang HP Indonesia (62 + 9–12 digit) dan beri peringatan bila di luar; pakai `[0-9]` (ASCII) bukan `\d`.
**B3 — Daftar `SINGKATAN_AMAN` terlalu sempit untuk B2B Indonesia.** Baris 38–42. Tertangkap sebagai "teriak": HRD, PPN, SPT, SOP, BPJS, HIPMI, KADIN, APINDO (juga nama usaha kapital seperti "PT ABC"). Muncul nyata di skenario 03. Usulan: tambah singkatan umum (HRD, GA, PPN, PPH, SPT, NIB, PKP, SOP, BPJS, CEO, GM, B2B, ISO, HACCP, HIPMI, KADIN, APINDO, JNE, JNT, dsb.) dan/atau hanya memperingatkan bila ≥ 2 kata kapital non-singkatan atau kata ≥ 5 huruf.
**B4 — `--jam-kirim` menolak format Indonesia `19.30`,** padahal output skill & checklist sendiri menulis "08.00–20.00". Pesan error jelas, tapi agent/pengguna awam hampir pasti mengetik titik. Usulan: terima `HH.MM` juga. Selain itu **makna jam ambigu**: help & SKILL.md Langkah 6 tidak menyebut jam harus **waktu setempat penerima**; di skenario 03 hanya agent yang menangkap selisih WIB→WITA. Usulan: ubah help menjadi "jam kirim menurut waktu setempat penerima", dan di Langkah 6/8 tulis eksplisit "konversi dulu: WITA = WIB+1, WIT = WIB+2".
**B5 — Tumpang tindih cakupan dengan `riset-calon-pelanggan`.** Deskripsi `riset-calon-pelanggan` juga menyebut "menyusun pesan pembuka personal WA/email/LinkedIn yang patuh UU PDP", sedangkan skill ini menggambarkannya hanya untuk "mencari/menilai daftar". Risiko dua skill terpicu untuk permintaan yang sama. Usulan (untuk pemilik/pembuat): sepakati pembagian — mis. `riset-calon-pelanggan` merujuk ke `pesan-prospek-wa` untuk pesan WA pertama, atau deskripsi di sini menyebut "untuk pesan pertama WA satu prospek yang sudah jelas; riset-calon-pelanggan untuk menyusun daftar + pesan per daftar".
**B6 — Klaim hukum sedikit berlebihan / kurang presisi** (`references/dasar-hukum-wa.md`):
- §1 "**Wajib** ada di setiap pesan pembuka: identitas pengirim … dan opsi berhenti" diletakkan di bawah UU PDP, padahal UU 27/2022 tidak mewajibkan isi pesan seperti itu secara harfiah. Yang ada: dasar pemrosesan sah (Pasal 20 ayat (2), termasuk huruf f "kepentingan yang sah lainnya", yang butuh penyeimbangan kepentingan) dan hak subjek data mengakhiri pemrosesan/menghapus/keberatan (Pasal 8 dst.). Usulan: tulis "praktik baik untuk menghormati hak subjek data (UU PDP Pasal 8 dst.)", bukan "wajib".
- §1 "Dilarang keras: database yang dibeli / bocor …" benar arahnya; sebaiknya sebut dasar: Pasal 65 (larangan memperoleh/mengumpulkan & menggunakan data pribadi bukan miliknya secara melawan hukum) dan Pasal 67 (sanksi pidana).
- §2 "Pasal 8–9 UU Perlindungan Konsumen": Pasal 8 terutama soal barang tidak sesuai standar/label; larangan penawaran/promosi yang tidak benar/menyesatkan ada di **Pasal 9 dan Pasal 10** (serta Pasal 17 untuk iklan). Usulan: ganti menjadi "Pasal 9–10".
- §2 penulisan UU ITE: lebih tepat "UU No. 11/2008 tentang ITE sebagaimana diubah UU No. 19/2016 dan UU No. 1/2024". Relevan juga Pasal 28 ayat (1) (informasi menyesatkan yang merugikan konsumen dalam transaksi elektronik) dan Pasal 35 (manipulasi agar dianggap otentik) untuk poin "menyamar" — boleh ditambahkan.
- Kesimpulan: tidak ada klaim yang salah arah atau menakut-nakuti berlebihan; disclaimer & tanggal cek ada. Perbaikan di atas = presisi.

### Rendah
**B7 — Emoji tidak diperiksa script,** padahal `checklist-anti-blokir.md` menulis "maksimal 1 emoji". Teks A/B dengan 5 emoji lolos tanpa catatan emoji. Usulan: hitung emoji (rentang Unicode simbol/piktograf) dan beri peringatan bila > 1.
**B8 — Pemisah kalimat tidak memecah baris baru** (`pisah_kalimat`, baris 117). Daftar poin tanpa titik (gaya ✅ … ✅ …) dihitung satu "kalimat" 52 kata. Usulan: juga split pada `\n`.
**B9 — Varian 3 (template) hampir selalu > 500 karakter** (506, 558, 594 di skenario 01–03) → peringatan panjang jadi rutin. Usulan: template V3 targetkan ≤ 500 karakter (4–5 kalimat pendek) atau naikkan ambang saran untuk V3 dan sebutkan di SKILL.md.
**B10 — Label "Singkat (1-2 kalimat)"** tidak cocok dengan template V1 yang berisi 3–4 kalimat (salam + perkenalan/asal + ajakan + opsi keluar). Usulan: "Singkat (± 2–3 kalimat, ≤ 300 karakter)".
**B11 — Detail layanan yang boleh diasumsikan** belum diatur: skill tegas melarang mengarang bukti/testimoni, tapi tidak menyebut detail layanan (mis. "bisa datang ke dapur") — di skenario 04 agent harus menandainya manual di Asumsi. Usulan: tambahkan satu kalimat di Langkah 5: "detail layanan yang tidak diberikan pengguna ditulis sebagai [placeholder] atau masuk Asumsi".
**B12 (ide dari pesaing)** — varian 3 cenderung mendaftar fitur; `cold-email` lebih kuat menyebut akibat masalah bagi penerima. Usulan tulis ulang panduan V3 ("1 kalimat akibat masalah bagi penerima, bila wajar & tidak mengarang").

## Kepatuhan keputusan pemilik (jalur 3) & aturan repo
- ✅ Tidak ada blast/broadcast: satu prospek per permintaan, permintaan massal ditolak/dialihkan (skenario 05).
- ✅ WA = mode copilot: skill hanya menyusun draf + tautan wa.me; pengguna menekan kirim sendiri. Tidak ada instruksi otomasi pengiriman, tidak ada integrasi OpenClaw untuk kirim.
- ✅ Tidak ada scraping login/beli database; domain sensitif (medis/kripto) dibatasi ke perkenalan saja.
- ✅ Frontmatter hanya `name` & `description`; SKILL.md 100 baris; script Python standar, tanpa jaringan; `validate.py` lolos (62 skill).
- ✅ Rujukan `follow-up-prospek`, `broadcast-wa`, `riset-calon-pelanggan`, `balas-chat-cs`, `proposal-kerjasama`, `surat-penawaran-harga` — semua ada di `skills/` dan deskripsinya cocok dengan cara dirujuk (kecuali tumpang tindih B5).
- ✅ Lisensi/atribusi MIT `cold-email` tercatat lengkap; commit sumber cocok dengan hasil clone penguji (`5b2c000…`).

## Skor kualitas: **8 / 10**
**Alasan:**
- (+) Menang telak A/B (20 vs 4) dan menang atas 2 pesaing (19 vs 11/6) → tidak terkena batas maks 6.
- (+) Kelima skenario berperilaku sesuai spesifikasi, termasuk penolakan sumber ilegal & auto-kirim; tidak mengarang bukti; zona waktu ditangani.
- (+) Script andal pada input rusak (tanpa traceback, 43 tes lulus), hitungan & encoding terverifikasi independen.
- (−) B1: pengecek asal kontak bertentangan dengan referensi pola pembuka milik sendiri — bukti ada celah uji di antara referensi & script.
- (−) B2–B4: normalisasi nomor & format jam belum "tahan awam" untuk kasus sangat umum (+62 0…, 19.30), false positive singkatan B2B.
- (−) B6: beberapa rujukan pasal kurang presisi (tidak salah arah).

**Rekomendasi:** layak naik ke status `lulus` setelah perbaikan **B1–B4 & B6** (perbaikan kecil, terukur, tambahkan tes regresi untuk setiap pola di `pola-pembuka.md`). B5 perlu keputusan pemilik/katalog. B7–B12 boleh di versi 1.1. Setelah revisi script, cukup ulang tes regresi + skenario 02 & 03 oleh penguji independen.

---

## Uji ulang v1.0.1 (2026-09-25, penguji independen kedua)
Rincian lengkap: [`06-uji-ulang-v1.0.1.md`](06-uji-ulang-v1.0.1.md). Salinan di scratchpad `uji2-ppw/`; verifikasi angka dengan `wc -m/-w`, wa.me di-decode dengan Perl & Node (bukan Python).

- **Tes bawaan:** 66 tes OK. `validate.py` lolos. SKILL.md 100 baris.
- **B1–B12:** semua ditangani. B1: 6/6 kutipan di `pola-pembuka.md` kini terdeteksi (diekstrak otomatis). B2: `+62 0…`, `00 62…`, 14 digit, telepon rumah 021, digit non-ASCII → benar/ditolak dengan pesan jelas. B3: HRD/PPN/SPT/BPJS lolos. B4: `19.30`/`19:30`/`1930` + `--zona` WIB/WITA/WIT, jam = waktu setempat penerima. B6: pasal diverifikasi web (UU PDP Pasal 20(2)f, 65, 67; UUPK Pasal 9–10; UU ITE jo. 1/2024), wajib vs praktik baik dipisah, disclaimer ada.
- **Skenario 02 & 03 diulang:** pola #3 dipakai apa adanya tanpa ditulis ulang; format jam titik diterima; semua 6 varian [OK]; V3 = 445 & 434 karakter; tidak ada detail layanan dikarang; hitungan & tautan cocok secara independen.
- **Temuan baru:** N1 (sedang) file non-UTF-8 → traceback `UnicodeDecodeError`. N2 (sedang) heuristik asal kontak masih longgar: salah-negatif pada frasa wajar ("bertemu Ibu di … Expo", "peroleh dari", "merekomendasikan") dan salah-positif ("dari teman-teman petani", "kontak dari kami", "di acara roasting"). N3–N9 rendah: ambang emoji 3 vs checklist "maks 1", WIB/WITA dianggap teriak, hitung emoji (skin tone/bendera/⭐), en-dash di nomor & link tanpa skema, jam tepat 20.00, tes pola tidak membaca referensi otomatis, presisi Pasal 9 hak menarik persetujuan.

### Skor kualitas uji ulang: **9 / 10**
**Alasan:** (+) Semua temuan prioritas (B1–B4, B6) tertutup dan terbukti lewat uji ulang, termasuk data rusak baru; skenario 02 & 03 kini mulus tanpa jalan memutar; hitungan & encoding benar secara independen; hukum presisi dengan disclaimer. (−) N1 masih bisa memunculkan traceback pada data rusak; N2 membuat pemeriksaan "asal kontak" (pemeriksaan keselamatan utama) belum sepenuhnya andal — tertolong oleh instruksi penilaian manual di Langkah 6; inkonsistensi kecil emoji (N3).

**Rekomendasi:** **LULUS** (layak naik status `lulus` → lanjut uji platform asli). Perbaiki N1–N3 di v1.0.2 (kecil, tidak perlu uji ulang penuh — cukup tes regresi baru); N4–N9 opsional.
