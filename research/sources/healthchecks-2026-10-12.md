# Catatan audit sumber ide -- Healthchecks (healthchecks/healthchecks)

**Tanggal:** 2026-10-12 | **Untuk skill:** `pantau-cron-openclaw` (jalur 3 VIP, orisinal Komunitech)

| Item | Nilai |
|---|---|
| Nama | Healthchecks -- pemantau cron "dead man's switch" |
| URL | https://github.com/healthchecks/healthchecks |
| Pembuat | Pēteris Caune dan kontributor |
| Lisensi | BSD-3-Clause (dibaca pada riset `research/sources/kurasi-bsd-cc-2026-10-05.md`, baris I1) |
| Sinyal | 10,4k bintang, ±1k fork, sejak 2015, masih dirawat (I1) |
| Keputusan | Ambil **konsep** saja; tulis ulang bersih |

## Yang diambil
- Konsep umum: tiap job mengirim *ping* saat sukses; bila ping tidak datang dalam jadwal + masa tenggang, pemilik diberi tahu.
- Gagasan jadwal berbentuk cron + zona waktu + toleransi sebagai ukuran "terlambat".
- Opsi lanjutan: pengguna boleh menunjuk layanan Healthchecks miliknya sendiri (self-host/hosted) lewat alamat ping yang ia simpan sendiri.

## Yang TIDAK diambil
- Kode apa pun (Python/Django), templat, antarmuka web, teks dokumentasi, atau skema basis data/model data.
- Status internalnya dan nama-namanya; skill memakai status sendiri (OK / TERLAMBAT / HILANG) dengan definisi sendiri.
- Tidak ada ketergantungan paket; skill hanya memakai Python standar dan tidak memerlukan layanan Healthchecks.

## Catatan kepatuhan
- Karena tidak ada kode/teks yang disalin, tidak ada kewajiban teks lisensi BSD-3-Clause yang diwariskan; kredit konsep tetap dicatat di `ATTRIBUTION.md`.
- "Healthchecks" disebut sebagai penyebut produk dengan keterangan "tidak berafiliasi" (keputusan pemilik 2026-09-26).
- Opsi layanan luar bersifat opsional, memakai alamat milik pengguna; alamat tidak pernah disimpan di repo, chat, atau log.
