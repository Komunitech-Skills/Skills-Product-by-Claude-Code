# Uji pembuat — umami-analitik 1.0.0 (29 Sep 2026)

> Ini catatan **pembuat** skill, bukan hasil penguji independen (Tahap 6 butir 2). Penguji independen menulis `HASIL-UJI.md` tersendiri.

## Lingkungan (Umami ASLI)
- **Umami 3.4.0** = rilis terbaru saat uji (tag `v3.4.0`, commit `ec0ff50`, 16 Sep 2026; dicek lewat `git ls-remote` + halaman Releases GitHub). Repo `umami-software/umami`: ±39,1 rb bintang, ±8,1 rb fork, lisensi **MIT** (file `LICENSE`: "Copyright (c) 2022 Umami Software, Inc.").
- Image Docker resmi `ghcr.io/umami-software/umami:3.4.0` (digest `sha256:85909afc45bdcda1917394594a087421fdbb05610fded0fa9f6fb861abb2f367`) + `postgres:15-alpine`, `docker-compose.yml` resmi 3.4.0 dengan perubahan panduan §2 (port `127.0.0.1:3000`, `APP_SECRET` & sandi DB acak, `DISABLE_TELEMETRY=1`). Sebelum dijalankan, `Dockerfile`, `scripts/start-docker.sh`, `scripts/update-tracker.js` dibaca: hanya migrasi DB + menjalankan server, tanpa unduhan skrip.
- Login admin bawaan `admin/umami` → sandi diganti lewat API `/api/me/password` (sama dengan menu Profile).
- Dua website: **Keripik Bu Sri (landing)** `keripikbusri.contoh.id` (dipindah ke tim "Usaha Bu Sri") dan **Toko Batik Laras** `batiklaras.contoh.id` (milik admin, di luar tim).
- Akun AI `agen-baca`: peran **view-only**, anggota tim sebagai **team-view-only**; kunci API `umami_...` dibuat oleh akun itu sendiri (`/api/me/api-keys`). Admin juga membuat kunci API (uji pilihan 2 website).
- Data: `tests/isi_data_fiktif.py kirim` → 51 hit (23 kunjungan, 16 pengunjung fiktif, 14–29 Sep 2026) ke endpoint publik **`/api/send`** dengan `timestamp`, User-Agent HP/laptop/tablet, IP blok dokumentasi `203.0.113.0/24`, kota lewat header `cf-ipcountry`/`cf-ipcity`. Event `klik-wa` & `beli` (dengan data `produk`, `nilai`). Plus 1 tautan pelacak (Links) `/q/wa-busri-bio` → `wa.me/...` diklik 3x (Referer Instagram).

## Verifikasi angka (skill vs hitungan independen `isi_data_fiktif.py harapan`)
| Periode | Ukuran | Skill | Hitung ulang | Cocok |
|---|---|---|---|---|
| minggu lalu 21–27 Sep | pengunjung / kunjungan / tayangan | 11 / 12 / 23 | 11 / 12 / 23 | ✔ |
| | bounce / total detik → rata-rata | 3 (25%) / 580 → 48 dtk | 3 / 580 → 48 | ✔ |
| | halaman (pengunjung) | / 10, balado 5, cara-pesan 3, original 2, terima-kasih 2 | sama | ✔ |
| | referrer | IG 3, google 2, tiktok 2, facebook 1 | sama | ✔ |
| | UTM source / campaign | ig 3, tiktok 2, wa 2 / promo-gajian-sep 7 | sama | ✔ |
| | perangkat | HP 8 (android 6 + iPhone 2), desktop 2, tablet 1 | sama | ✔ |
| | negara / kota | ID 10, MY 1 / 9 kota | sama | ✔ |
| | event | klik-wa 3, beli 2; nilai 25.000+22.000 = Rp47.000 | sama | ✔ |
| pembanding 14–20 Sep | pengunjung / tayangan / bounce / rata | 4 / 6 / 50% / 17 dtk | 4 / 6 / 2 dari 4 / 70÷4=17 | ✔ |
| minggu ini s.d. 29 Sep 16.00 | pengunjung / tayangan / bounce / rata | 7 / 13 / 28,6% / 44 dtk | 7 / 13 / 2 dari 7 / 310÷7=44 | ✔ |
| pembanding 21 Sep 00.00–22 Sep 16.00 | pengunjung / tayangan / klik-wa | 2 / 5 / 1 | A & E saja (F, G setelah 16.00) | ✔ |
| kemarin 28 Sep | pengunjung / tayangan / total detik | 4 / 8 / 240 | 4 / 8 / 240 | ✔ |
| 30 hari | UTM campaign | promo-gajian-sep 10, reseller-okt 2 | sama | ✔ |
| tautan 7 hari | klik / pengunjung / asal | 3 / 3 / l.instagram.com 3 | 3 klik curl | ✔ |
Angka skill juga sama dengan field `comparison` bawaan Umami untuk minggu lalu (pembanding 4/4/6).

## Temuan API Umami 3.4.0 yang ditangani skill
1. `GET /api/websites?includeTeams=true` **tidak** memuat website tim bila akun hanya anggota *view-only* (hanya tim yang dimiliki/dikelola) → skill menambah `/api/me/teams` + `/api/teams/{id}/websites`.
2. Umami membalas **401 untuk semua penolakan** (kunci salah, website di luar akses, id tidak ada) → skill memeriksa `/api/me` untuk membedakan "kunci salah" vs "tidak punya akses".
3. Jawaban `/api/me` **berisi kunci/token itu sendiri** dan `/api/me/teams` berisi kode undangan tim → tidak pernah dicetak/disimpan (rekaman uji disensor).
4. `metrics/expanded` untuk halaman/referrer/UTM mengembalikan bounce & lama = 0 → skill tidak menampilkan bounce per halaman (CSV dikosongkan); kanal & perangkat benar.
5. Angka di `metrics` = **pengunjung unik** (bukan tayangan) untuk halaman/referrer/UTM; tayangan per halaman diambil dari `metrics/expanded`.
6. Kanal: klik ber-UTM WhatsApp tanpa referrer tercatat **"direct"** → dijelaskan di keluaran & panduan §8.
7. UTM tidak menempel pada event (filter `utmSource` pada event = kosong) → skill tidak mengarang konversi per kampanye.
8. Kunci API tidak bisa dipakai untuk `/api/users`, `/api/auth`, `/api/admin` (diblokir Umami); akun view-only ditolak saat `POST /api/websites` (401).

## Uji keamanan & galat (transkrip lengkap: `transkrip-umami-3.4.0.txt`)
Kunci salah → kode 5; website di luar tim → tidak terlihat / 401 "TIDAK PUNYA AKSES"; admin 2 website tanpa `--situs` → kode 7; server mati → 4; `http://` ke domain publik → 2; `https://` publik tanpa izin → 2; path `/login` di alamat → 2; server yang mengalihkan (302) → 4 dan **tidak ada permintaan ke alamat tujuan** (kunci tidak terkirim ulang); `HTTP_PROXY` mati + alamat lokal → tetap jalan (proxy diabaikan); login sandi `UMAMI_USERNAME`+`UMAMI_PASSWORD` → angka sama; sandi salah → 5; `simpan-kunci` → file 600, menolak menimpa tanpa `--ya`. Kunci tidak muncul di keluaran mana pun (tampil `umami_JJ****LHYJ`).

## Uji regresi
`python3 tests/uji_regresi.py` → **28/28 OK** (server tiruan memutar ulang `tests/fixtures/umami-3.4.0.json` yang direkam dari Umami asli lewat `tests/rekam_semua.sh`; angka dibandingkan dengan `isi_data_fiktif.harapan`).

## Belum diuji
Windows/macOS sungguhan, Umami 2.x, Umami Cloud, HTTPS di VPS sungguhan (Caddy), pengiriman Telegram lewat OpenClaw (hanya bentuk perintah yang disalin dari pola teruji), instalasi tanpa Docker.
