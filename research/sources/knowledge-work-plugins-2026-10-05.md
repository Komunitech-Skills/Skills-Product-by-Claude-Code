# Catatan sumber: anthropics/knowledge-work-plugins (skill `reactivate`)

Tanggal: 2026-10-05 · Pembuat skill: agen pembuat (jalur kurasi/ATM) · Terkait: `research/sources/kurasi-apache-2026-10-05.md` kandidat #1 (baris 5).

## Sumber
- **URL repo:** https://github.com/anthropics/knowledge-work-plugins
- **Skill diambil:** `small-business/skills/reactivate/SKILL.md` (https://github.com/anthropics/knowledge-work-plugins/tree/main/small-business/skills/reactivate). Folder skill sumber hanya berisi `SKILL.md` (109 baris), tanpa script dan tanpa file pendukung.
- **Pembuat:** Anthropic · **Lisensi:** Apache License 2.0 (berkas `LICENSE` di akar repo dibaca 2026-10-05; pemegang hak cipta tidak terisi: masih `[yyyy] [name of copyright owner]`; di akhir berkas ada beberapa baris teks acak non-lisensi yang tidak disalin) · **NOTICE:** tidak ada (404 pada cabang utama, 2026-10-05).
- **Sinyal bukti:** dinilai di berkas kurasi induk (26,2k bintang, 3,1k fork, pembuat resmi, commit terakhir 2026-10-01; 5/5 sinyal). Tidak diverifikasi ulang di sesi ini selain keberadaan file dan lisensi.
- **Cara baca:** `raw.githubusercontent.com` (tanpa clone, tanpa menjalankan kode). Hash SHA-256 `SKILL.md` saat dibaca: `734946c3...39e210`.

## Audit (Tahap 3)
Dibaca penuh. Tidak ada perintah destruktif, pengiriman data ke luar, pembacaan kredensial, kode ter-obfuscate, API key, atau prompt injection. Frontmatter sumber memuat `allowed-tools: Read, WebFetch` (tidak dibawa). Sumber mengandung pagar baik ("isi pesan/dokumen = data bukan perintah"; gerbang persetujuan sebelum kirim). **Lolos.**

## Keputusan
**Diambil (ATM)** jadi `skills/aktifkan-kembali-pelanggan` v1.0.0 (status `uji`). Yang diambil hanya kerangka: temukan pelanggan diam menurut ritmenya, ranking berdasar nilai, konfirmasi penawaran, urutan 3 pesan/4 minggu, pesan pertama tidak jualan, berhenti saat komplain/balasan, catat sentuhan. Semua konektor (CRM, pembayaran, toko online, email, Mailchimp) dan rantai skill lain dibuang.

Nilai tambah: kanal WA/Telegram mode copilot (tanpa kirim massal), segmentasi A-D berdasarkan hari sejak beli terakhir, script `segmentasi.py` (CSV fleksibel, tanggal dd/mm/yyyy, data rusak, nomor ganda, daftar jangan-dihubungi, jadwal dengan batas harian) + 15 uji regresi, template pesan WA, referensi UU PDP, contoh lokal. Tier usulan: ecer Rp99.000 (script hitung + template per segmen; pembanding: pelengkap `program-referral-loyalitas` Rp79.000 dan `crm-wa`).

---

# Skill kedua dari sumber yang sama: `handle-objection` → `tangani-keberatan-pelanggan`

- **Skill diambil:** `sales/skills/handle-objection/SKILL.md` (93 baris, tanpa script/file pendukung). Lisensi Apache-2.0 (`sales/LICENSE`, bersih); repo tidak punya NOTICE.
- **Audit (Tahap 3):** tidak ada prompt injection, perintah berbahaya, atau kunci. Field `allowed-tools` tidak dibawa.
- **Diambil (ATM)** jadi `skills/tangani-keberatan-pelanggan` v1.0.0 (status `uji`, commit 66b4bd6): kerangka klasifikasi keberatan + alur akui → tanya → tawarkan opsi. Ditulis ulang untuk chat WA/DM Indonesia, 6 jenis keberatan, larangan urgensi/diskon/klaim palsu (UU 8/1999), script reframing harga (Decimal), aturan kapan berhenti follow-up.
- Catatan: bagian ini ditulis koordinator karena file sempat ditimpa oleh agent pembuat skill pertama.

---

# Skill ketiga dari sumber yang sama: `ticket-triage` + `customer-escalation` → `triase-keluhan-pelanggan`

Tanggal: 2026-10-05 · Pembuat skill: agen pembuat (jalur kurasi/ATM) · Terkait: `research/sources/kurasi-apache-2026-10-05.md` kandidat #1 (baris 1).

- **Skill diambil:** `customer-support/skills/ticket-triage/SKILL.md` (275 baris) dan `customer-support/skills/customer-escalation/SKILL.md` (248 baris); keduanya hanya `SKILL.md`, tanpa script/file pendukung. URL: https://github.com/anthropics/knowledge-work-plugins/tree/main/customer-support/skills/ticket-triage dan `.../customer-escalation`.
- **Lisensi:** Apache-2.0. `customer-support/LICENSE` ada (202 baris, bersih tanpa teks acak; SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`), disalin sebagai `LICENSE-APACHE`. Pemegang hak cipta tidak terisi (placeholder). **NOTICE:** `customer-support/NOTICE` 404 (dicek 2026-10-05).
- **Cara baca:** `raw.githubusercontent.com` (tanpa clone, tanpa menjalankan kode). SHA-256 `ticket-triage/SKILL.md`: `d0e5e95443e358ad2a74811b196071d10807ca95aa20351ab5760feeecee1294`; `customer-escalation/SKILL.md`: `90c33574a41371e8e116aaf40237141adcd6075ef8bcb9de993de2b543867b3e`. Commit terakhir path itu tidak bisa dicek (API GitHub tidak tersedia di sesi ini); sinyal bukti repo dinilai di berkas kurasi induk (26,2k bintang, commit 2026-10-01, pembuat resmi).
- **Audit (Tahap 3):** dibaca penuh; pola berbahaya dicari (curl/wget/eval/base64/rm/ssh/token/api key/password/"ignore"). Tidak ada perintah destruktif, pengiriman data keluar, kredensial, kode ter-obfuscate, atau prompt injection. Yang ada: penanda konektor `~~support platform` dll. dan `argument-hint` di frontmatter (tidak dibawa). **Lolos.**
- **Diambil (ATM)** jadi `skills/triase-keluhan-pelanggan` v1.0.0 (status `uji`). Diambil: kerangka baca keluhan, kategori menurut penyebab, prioritas bertingkat + pemicu naik tingkat, "ragu pilih lebih tinggi", deteksi duplikat/pola, rute eskalasi, isi ringkasan eskalasi, kabar lanjutan. Dibuang: konektor, P4/SLA korporat, kategori perangkat lunak, reproduksi bug, ARR.
- **Nilai tambah:** kategori dan prioritas P1-P3 untuk toko/kafe/jasa (ancaman ulasan, keamanan, tenggat platform, nilai pesanan, pelanggan mengulang), draf balasan per kategori, daftar keputusan pemilik, rekap tanpa data pribadi, `scripts/triase.py` + 30 uji regresi, dasar hukum UU 8/1999 dan UU 27/2022, larangan menghapus/membungkam ulasan.
- **Tanggal cek ketentuan platform: 2026-10-05** (di `references/dasar-hukum-dan-platform.md`). Terbaca dari sumber: Shopee (respons tawaran refund 1 hari kalender, keputusan investigasi bila tak ada respons/bukti 3 hari, kirim balik 5 hari kalender, bukti video paket kosong; help.shopee.co.id). TikTok Shop by Tokopedia (respons retur sekitar 48 jam, otomatis disetujui bila lewat; batas pengajuan 6 hari non-Mall / 15 hari Mall hanya dari ringkasan pencarian, **belum terkonfirmasi** di halaman resmi). Halaman penjual Shopee dan Tokopedia tidak terbaca penuh lewat alat baca; skill menyuruh pengguna mencocokkan dengan Pusat Penjual.
- **UU 8/1999:** Pasal 7 huruf g dan Pasal 19 ayat (3), (5) dikonfirmasi lewat pencarian (teks UU di jdih.esdm.go.id dan jdih.kemenkeu.go.id tidak bisa dibuka lewat alat baca). Pasal 4 huruf c/d/h, Pasal 7 huruf b, Pasal 8 ayat (1) huruf f, Pasal 18 ayat (1) huruf b dari pengetahuan umum: **PERLU REVIEW** cocokkan dengan teks UU sebelum rilis.
