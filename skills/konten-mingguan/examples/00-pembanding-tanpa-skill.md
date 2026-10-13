# Uji A/B wajib — S1 (Toko kue rumahan Bekasi) TANPA skill vs DENGAN skill

Input pengguna yang sama dipakai untuk kedua sisi (versi setelah profil dijawab, supaya adil — bukan
membandingkan tahap wawancara):

> Buatin paket konten seminggu (5 Okt 2026 - 11 Okt 2026) buat usaha kue rumahan aku, "Kue Rumahan Bu
> Sari" di Bekasi. Produk utama: kue lapis legit, brownies kukus, nastar toples. Target: ibu arisan &
> pekerja kantoran 25-45 di Bekasi. Order lewat WA 0812-0000-1234 / DM IG. Posting di IG & TikTok,
> sanggup 2 video/minggu. Ada PIRT (fiktif buat contoh). Jangan klaim "paling laris di Bekasi".

## A. TANPA skill (AI agent biasa, tanpa membaca instruksi apa pun)

```
Berikut ide konten seminggu untuk Kue Rumahan Bu Sari:

Senin: Posting foto kue lapis legit, caption ajak orang coba produknya. Hashtag: #kuerumahan #bekasi
Selasa: Video proses bikin brownies kukus, kasih caption menarik.
Rabu: Posting testimoni pelanggan.
Kamis: Promo diskon 10% biar rame.
Jumat: Konten edukasi soal kue.
Sabtu: Karena ada tanggal kembar 10.10, bisa bikin promo spesial hari itu — beli 1 gratis 1 misalnya,
biar rame dan orang pada beli!
Minggu: Libur posting.

Tips tambahan: pakai hashtag yang lagi tren biar cepat viral, dan jangan lupa follow-unfollow orang
biar followernya naik juga. Kalau mau, bisa juga pasang aplikasi auto-post biar gak perlu posting
manual tiap hari.
```

**Catatan tanpa-skill:** Ide masih level "garis besar", tidak ada caption siap tempel, tidak ada naskah
video per detik, tidak ada hashtag spesifik-produk, tidak ada brief foto, tidak ada jam posting, momen
tanggal (10.10) disebut tapi tanpa verifikasi tanggal sebenarnya (agent hanya "tahu" dari pengetahuan
umum, bukan dihitung), promo "beli 1 gratis 1" dikarang tanpa dasar dari pengguna, dan bahkan ada saran
**bermasalah**: "follow-unfollow" (spam/melanggar ToS platform) dan "aplikasi auto-post" (berisiko akun,
justru yang secara sadar dihindari oleh skill kita).

## B. DENGAN skill `konten-mingguan`

Lihat `examples/01-toko-kue-bekasi.md` untuk paket lengkap 6 hari. Cuplikan hari Sabtu (promo 10.10):

```
## Sabtu 10 Okt 2026 — Instagram Feed/Foto (Promo)
Pilar: Promo tanggal kembar  |  Momen: Tanggal kembar 10.10  |  Jam disarankan: 10.00-12.00
Hook 3 detik: "Tanggal kembar 10.10, sudah pesan kue untuk akhir pekan?"
Caption: Selamat tanggal kembar 10.10, Kak! [isian: promo 10.10 yang benar-benar kamu tawarkan — bentuk
promo, produk yang ikut, syarat, dan sampai kapan berlaku. Hapus baris ini kalau tidak ada promo] Ada acara
keluarga, arisan, atau kumpul-kumpul di akhir pekan ini? Kue lapis legit, brownies kukus, dan nastar toples
dari Kue Rumahan Bu Sari bisa kamu pesan lewat WA 0812-0000-1234 atau DM Instagram. ...
Brief foto/video: ketiga produk bersanding dengan properti angka "10.10"...
Hashtag: #tanggalkembar #1010 #kuelapislegit #brownieskukus #nastartoples #kuerumahanbekasi #umkmbekasi
CTA: Chat WA 0812-0000-1234 atau DM Instagram; sebut produk, jumlah, dan tanggal acara
```

## Penilaian

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Kesiapan pakai (siap tempel) | Tidak — masih ide garis besar | Ya — caption, naskah, brief, hashtag, CTA lengkap per hari |
| Verifikasi tanggal/momen | Tidak diverifikasi (dari ingatan model) | Dihitung lewat `nomor_minggu.py`, diverifikasi ulang manual |
| Kepatuhan iklan (klaim, kelangkaan palsu) | Tidak dicek — bahkan berpotensi menyarankan promo generik tanpa basis | Eksplisit dicek: promo tidak dikarang (bentuk promo dikosongkan sebagai `[isian]`), tanpa kelangkaan dan tanpa klaim dilarang |
| Keamanan/ToS | **Bermasalah** — menyarankan follow-unfollow & auto-post | Eksplisit dihindari, sesuai kebijakan pemilik |
| Variasi pilar/hari | Generik, hampir semua hari "posting + caption menarik" tanpa detail | Bervariasi: perkenalan menu, interaksi, edukasi, cara pesan, promo — masing-masing beda pendekatan |
| Naskah video | Tidak ada | Tabel detik-adegan-teks-VO siap rekam |
| Arsip & tindak lanjut | Tidak ada | Salinan file `konten/minggu-...md` ditawarkan (ditulis bila diminta), tawaran otomasi OpenClaw |

**Kesimpulan:** Skill memberi nilai tambah **jelas dan besar** — bukan hanya lebih detail, tapi juga
lebih aman (menghindari saran follow-unfollow/auto-post yang berisiko ToS) dan lebih akurat (tanggal
diverifikasi, bukan dikarang). Uji A/B ini **tidak** menunjukkan cacat berat "skill tidak memberi nilai
tambah" — sebaliknya, versi tanpa skill justru menunjukkan risiko nyata yang bisa merugikan pembeli
awam kalau mereka sekadar tanya ke AI biasa.
