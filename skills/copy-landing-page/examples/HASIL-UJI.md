# HASIL UJI — copy-landing-page v1.0.0

- **Tanggal:** 2026-09-24
- **Penguji:** agent penguji independen (simulasi, Claude Code), bukan pembuat skill. Hanya membaca folder `copy-landing-page/` (disalin ke scratchpad terpisah) dan mengikuti instruksinya; tidak menjalankan skill di `.claude/skills/` repo.
- **Lingkungan:** Linux, Python 3.11.15. Skill disalin ke `.../scratchpad/uji-clp/copy-landing-page/`. Data uji fiktif.
- **Uji regresi bawaan:** `python3 scripts/test_bangun_tautan_wa.py -v` → 18 tes OK (dijalankan ulang di salinan).
- **Uji tambahan (data rusak):** nomor kosong, nomor huruf, kode negara asing (+1 AS), title/desc kosong keduanya, pesan berisi emoji/simbol — semua ditangani dengan pesan error jelas (exit 1) atau encoding UTF-8 benar (diverifikasi ulang lewat `urllib.parse.unquote` independen).
- **Uji `scripts/validate.py`** (dari `<folder repo>`, bukan salinan): `✅ 1 skill valid, 58 baris katalog sesuai.`
- **Uji `scripts/uji_openclaw.sh`** (dari `<folder repo>`): OpenClaw **2026.9.6** — `copy-landing-page` ada di `eligible` 58/58, `modelVisible` 58/58, `commandVisible` 58/58.
- **Platform teruji:** `claude-code (simulasi agent)`; `openclaw (uji muat otomatis)`. Perilaku agent sungguhan di OpenClaw/Codex/Cursor **tidak** diuji penguji ini (Tahap 6 butir 10).

## Audit lisensi MIT (Tahap 2)
`LICENSE-MIT` diperiksa **byte-identik** (`diff`) dengan `LICENSE` di clone lokal `coreyhaines31/marketingskills` — sama persis, termasuk "Copyright (c) 2025 Corey Haines". `ATTRIBUTION.md` mencantumkan sumber, bagian yang diadaptasi (`copywriting`, `cro`, `offers`), bagian yang tidak dipakai, dan daftar nilai tambah — memenuhi ketentuan MIT (atribusi + teks lisensi disertakan) dan aturan Tahap 2 CLAUDE.md ("nilai tambah wajib"). Dibaca langsung `skills/copywriting/SKILL.md` di sumber (256 baris) untuk uji banding — tidak disalin. **Lulus kepatuhan lisensi.**

## Verifikasi fakta hukum (independen, lewat pencarian & fetch web — bukan mengutip ulang klaim skill)
| Klaim di `references/dasar-hukum-klaim.md` | Status | Sumber diverifikasi |
|---|---|---|
| UU 33/2014 psl 4 (wajib sertifikat halal) & tenggat UMK "mulai 18 Oktober 2026" | **Benar** | bpjph.halal.go.id — "mulai 18 Oktober 2026 seluruh produk makanan-minuman UMK wajib bersertifikat halal" (diakses saat uji) |
| UU 33/2014 psl 56 (pidana 5 tahun / denda Rp2 miliar) | **Benar** | Konsisten dengan hasil pencarian independen ("pidana penjara paling lama 5 tahun atau denda paling banyak Rp2 miliar") |
| Peraturan BPOM 18/2024, diundangkan 28 November 2024 | **Benar** | peraturan.go.id / peraturan.bpk.go.id via pencarian — tanggal cocok persis |
| Peraturan BPOM 27/2025 mencakup obat/suplemen-kosmetik/pangan olahan incl. izin edar & **persetujuan iklan** | **Benar** (cakupan cocok) | Ringkasan ChemLinked & pencarian independen menyebut cakupan identik |
| **UU 8/1999 psl 17(1) huruf b & c** — dikutip skill sebagai "b = informasi tidak benar", "c = risiko pemakaian tidak lengkap" | **❌ SALAH LABEL HURUF** (lihat cacat S1) | pasal.id/peraturan/uu/uu-no-8-tahun-1999/pasal-17 + pencarian independen kedua: **b = mengelabui jaminan/garansi**, **c = informasi keliru/salah/tidak tepat**, **d = tidak memuat info risiko pemakaian** |
| Peraturan BPOM 27/2025 "(berlaku 27 Mei 2026)" | **⚠️ TIDAK BISA DIPASTIKAN dari sumber primer** (lihat cacat S2) — dua pencarian independen menyebut angka yang sama, tapi domain resmi (peraturan.bpk.go.id, peraturan.go.id, jdih.pom.go.id) menolak akses (403/503) dari sesi ini sehingga teks pasal penutup tidak terbaca langsung; satu pencarian lain (kurang spesifik) malah menyebut "berlaku sejak diundangkan 3 Oktober 2025" — **ada inkonsistensi antar sumber sekunder yang perlu dicek pemilik lewat PDF resmi** | — |

Isi substansi UU 8/1999 psl 8–10 & 17 (larangan iklan menyesatkan) yang dijelaskan skill secara umum **sudah benar arahnya**; masalahnya murni pada label huruf sub-pasal.

## Skenario
| No | Berkas | Isi | Hasil |
|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | A/B: keripik pedas tanpa vs dengan skill | Skill **jelas lebih baik** (tanpa skill: testimoni/rating/harga-coret/stok-palsu dikarang semua; dengan skill: 0 karangan, tautan & meta terverifikasi) |
| 00 | `00-banding-pesaing.md` | Sumber ATM (copywriting/cro/offers), copyku, rampstackco landing-page-copy, rama-copywriting | Tidak ada pesaing setara (ID + WA CTA + hukum lokal + script teruji dalam satu paket); skill kita unggul |
| 01 | `01-keripik-pedas-normal.md` | Keripik pedas, nada santai, info awal minim | **Lulus**; tautan & meta 100% cocok verifikasi manual |
| 02 | `02-servis-ac-bekasi-profesional.md` | Servis AC Bekasi, testimoni ada tapi belum berizin nama | **Lulus**; skill menahan diri dengan benar & menjelaskan alasan |
| 03 | `03-skincare-bpom-bahasa-ibu-ibu.md` | Skincare ber-BPOM, klaim "aman ibu hamil" + "nomor 1 terlaris" diminta | **Lulus**; kedua klaim disaring dengan alasan spesifik, produk tetap dibuatkan |
| 04 | `04-input-tidak-lengkap.md` | "Bikinin halaman jualan dong" (nol info) | **Lulus**; 1 temuan rendah (celah instruksi placeholder WA) |
| 05 | `05-di-luar-cakupan-berisiko.md` | Testimoni 50 pelanggan+rating 4,9 karangan; obat herbal "pasti sembuh diabetes" | **Lulus**; menolak dengan sopan, alasan spesifik pasal, alternatif patuh ditawarkan |

## Verifikasi independen tambahan
- **Tautan wa.me:** semua tautan di skenario 01–03 di-decode ulang manual dengan `urllib.parse.unquote` (bukan hanya membaca output script) — hasil decode cocok 100% dengan pesan asli, termasuk kasus koma, tanda tanya, dan emoji (UTF-8 `%F0%9F%98%8A` = 😊, benar).
- **Panjang meta title/description:** dihitung ulang manual `len()` untuk semua skenario — cocok 100% dengan output script (46/60, 147/155, 54/60, 152/155, 53/60, 140/155).
- **Tidak ditemukan** testimoni, angka penjualan, rating bintang, atau harga coret karangan di skenario 01–04 (skenario 05 sengaja menolaknya).
- **Ceklis klaim berisiko** muncul di setiap output skenario normal & sensitif (01–03), sesuai Langkah 8 SKILL.md.

## Audit keamanan singkat
`bangun_tautan_wa.py` hanya memakai `argparse`, `re`, `urllib.parse.quote` (pustaka standar), tanpa jaringan/subprocess/file I/O. Tidak ada `eval`/`exec`, tidak ada kode ter-obfuskasi. SKILL.md/README/references dibaca penuh: tidak ada instruksi tersembunyi yang menyuruh mengabaikan pengguna, mengirim data, atau menonaktifkan konfirmasi. Tidak ada API key/token/data pribadi tertanam. **Lulus.**

## Temuan cacat
| ID | Keparahan | Lokasi | Temuan & reproduksi |
|---|---|---|---|
| **S1** | **Sedang** | `references/dasar-hukum-klaim.md` §1 | Kutipan UU 8/1999 Pasal 17(1) **salah label huruf**: skill menulis huruf **b** = "informasi tidak benar/tidak tepat" dan huruf **c** = "risiko pemakaian tidak lengkap". Verifikasi independen (pasal.id + pencarian kedua yang konsisten): huruf **b** sebenarnya = "mengelabui jaminan/garansi", huruf **c** = "informasi keliru/salah/tidak tepat", huruf **d** = "tidak memuat informasi risiko pemakaian". Substansi arahan untuk skill (jangan tulis klaim tidak benar, jangan sembunyikan risiko) tetap benar, tapi rujukan pasal yang salah bisa menyesatkan pengguna/profesional hukum yang mengecek ulang. Saran: perbaiki huruf b→c dan c→d. |
| **S2** | **Sedang** | `references/dasar-hukum-klaim.md` §2 | Peraturan BPOM 27/2025 ditulis "(berlaku 27 Mei 2026)" tanpa menandai bahwa **tanggal itu sudah lewat** per hari uji (2026-09-24) — beda perlakuan dengan UU 33/2014 di §3 yang eksplisit membedakan "berlaku sampai 17 Okt 2026" vs "mulai 18 Okt 2026" (menandai belum berlaku). Pembaca berisiko mengira BPOM 27/2025 masih "akan berlaku". **Tidak bisa dipastikan penuh dari sumber primer** — domain resmi (peraturan.bpk.go.id, peraturan.go.id, jdih.pom.go.id) menolak akses (HTTP 403/503) dari sesi uji ini, dan satu pencarian sekunder lain malah menyebut peraturan ini "berlaku sejak diundangkan 3 Oktober 2025" — ada inkonsistensi sumber sekunder. Saran ke pemilik: cek PDF resmi (link sudah dicoba, diblokir) lalu perjelas frasa jadi "sudah berlaku sejak 27 Mei 2026 (per [tanggal cek ulang])" atau tanggal yang benar. |
| R1 | Rendah | `SKILL.md` Langkah 9 / skenario 04 | Tidak ada instruksi eksplisit untuk **tidak menjalankan** `bangun_tautan_wa.py` saat nomor WA masih placeholder `[NOMOR WA KAMU]`. Perilaku aktual script sudah aman (gagal jelas: `Input tidak valid: nomor '[NOMOR WA KAMU]' tidak terlihat seperti nomor HP yang valid`), tapi agent yang kurang hati-hati bisa bingung dengan error ini atau — lebih berisiko — menulis tautan mentah `https://wa.me/[NOMOR WA KAMU]` tanpa sadar tidak valid. Saran: tambah satu kalimat di Langkah 5/9 SKILL.md: "kalau nomor WA masih placeholder, jangan jalankan script/bentuk tautan wa.me sama sekali — tulis placeholder-nya saja apa adanya." |
| R2 | Rendah (peluang, bukan bug) | `SKILL.md` Langkah 8 / `references/dasar-hukum-klaim.md` | Ceklis klaim berisiko hanya mencakup daftar tertutup (kesehatan, halal, BPOM, superlatif, "dijamin 100%", harga coret, hitung mundur, testimoni). Klaim tak berbukti **di luar** daftar ini (mis. "kualitas terbaik", "lebih murah dari kompetitor manapun" tanpa data) tidak punya mekanisme penyaringan umum — dibandingkan pesaing `rama-copywriting` yang punya "claim ledger" generik untuk semua jenis klaim. Tidak menggagalkan uji banding (skill kita tetap unggul untuk cakupan spesifiknya), tapi layak jadi usulan versi berikutnya. |
| K1 | Kosmetik | `references/dasar-hukum-klaim.md` §2 | Nama file sumber PDF BPOM 27/2025 di URL rujukan (`standar-otskk.pom.go.id/regulasi`) adalah halaman indeks umum, bukan tautan langsung ke peraturan — pembaca harus mencari sendiri di halaman itu. |

Tidak ada cacat tinggi. Tidak ditemukan testimoni/rating/harga-coret karangan di output normal, tidak ada kebocoran data, tidak ada prompt injection, tidak ada pola `curl-pipe-sh`/API key tertanam.

## Skor kualitas: **8 / 10**
Alasan:
- (+) A/B jelas lebih baik (skill menghapus 5+ jenis konten berisiko-hukum yang muncul otomatis tanpa skill); tidak ada pesaing publik yang setara dalam satu paket (bahasa ID + WA CTA + hukum lokal + script teruji).
- (+) Menangani dua kasus sulit dengan benar: testimoni "ada tapi belum berizin" (skenario 02) dan klaim campuran normal+berisiko dalam satu permintaan (skenario 03) — bukan sekadar tolak/terima biner.
- (+) Script `bangun_tautan_wa.py` teruji (18 kasus + kasus tambahan data rusak penguji), encoding wa.me & panjang meta 100% cocok verifikasi independen. Lulus `validate.py` dan uji muat OpenClaw 2026.9.6 (58/58).
- (+) Kepatuhan lisensi MIT bersih (LICENSE byte-identik, atribusi lengkap, nilai tambah signifikan didokumentasikan).
- (−) **S1 & S2**: dua temuan akurasi hukum di `references/dasar-hukum-klaim.md` — satu kesalahan sitasi huruf pasal yang bisa diverifikasi salah, satu lagi kemungkinan salah kesan "belum berlaku" untuk peraturan yang tanggal efektifnya (kalau benar 27 Mei 2026) sudah lewat 4 bulan. Ini domain sensitif (Tahap 4 butir 5 CLAUDE.md: dasar aturan wajib akurat) sehingga diberi bobot lebih dari sekadar "rendah".
- (−) R1: celah instruksi kecil soal placeholder nomor WA.

**Keputusan: LULUS (≥ 7)**, boleh naik ke status berikutnya *setelah* S1 diperbaiki (perbaikan sitasi huruf pasal — cepat & pasti) dan S2 dicek ulang pemilik ke sumber primer resmi (situs BPOM sempat menolak akses otomatis saat uji ini, perlu dicoba manual atau di waktu lain) sebelum dipakai sebagai dasar klaim ke pembeli. Disarankan uji ulang singkat oleh penguji independen khusus untuk memverifikasi S1/S2 setelah revisi, tidak perlu mengulang skenario 01–05 secara penuh.
