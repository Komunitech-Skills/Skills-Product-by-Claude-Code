# Uji A/B — Skenario 01 tanpa skill vs dengan skill

> Penguji independen, 2026-09-25. Permintaan identik dengan `01-katering-kantor-dari-pameran.md`.
> "Tanpa skill" = jawaban agent umum (model yang sama, tanpa folder skill dimuat), ditulis apa adanya seperti yang lazim dihasilkan asisten umum untuk permintaan ini.

## A. Tanpa skill (jawaban agent umum)
```
Selamat siang Ibu Maya 🙏

Perkenalkan, saya Rudi dari Dapur Bu Ratna Catering. Senang sekali bisa bertemu Ibu di Jakarta Food & Franchise Expo kemarin! 😊

Menindaklanjuti obrolan kita, kami ingin menawarkan layanan katering makan siang karyawan untuk PT Sinar Logistik Nusantara dengan keunggulan:
✅ Menu bervariasi, berganti setiap minggu
✅ Bahan segar & higienis
✅ Harga bersaing, bisa disesuaikan budget perusahaan
✅ Pengantaran tepat waktu

Saat ini kami sudah dipercaya melayani 3 pabrik di kawasan Cikarang.

Apakah Ibu ada waktu minggu ini untuk meeting singkat atau food tasting di kantor Ibu? Saya bisa menyesuaikan jadwal Ibu.

Terima kasih banyak atas waktunya, Bu. Ditunggu kabar baiknya! 🙏😊

Salam,
Rudi
Dapur Bu Ratna Catering
0812-xxxx-xxxx
```
Ditambah kalimat penutup agent: "Semoga membantu! Mau saya buatkan versi yang lebih santai?"

Pemeriksaan objektif dengan `scripts/cek_pesan.py` (dijalankan penguji pada teks A): 755 karakter (> 700), satu "kalimat" 52 kata (daftar poin tanpa titik), 5 emoji, opsi keluar tidak ada. Script juga menyatakan asal kontak "tidak terdeteksi", padahal teks menyebut pameran ("bertemu Ibu di Jakarta Food & Franchise Expo") → ini false negative heuristik (lihat HASIL-UJI B1), jadi **tidak** dihitung sebagai kelemahan A.

## B. Dengan skill
Lihat output lengkap di `01-katering-kantor-dari-pameran.md` (3 varian 239/469/506 karakter, semua lolos cek asal kontak & opsi keluar, tautan wa.me, saran jam, checklist, asumsi).

## Penilaian berdampingan (0–2 per kriteria)
| # | Kriteria | A. Tanpa skill | B. Dengan skill | Catatan |
|---|---|---|---|---|
| 1 | Asal kontak jelas & spesifik | 2 | 2 | Keduanya menyebut pameran (pengguna menyebutnya). |
| 2 | Opsi keluar sopan | 0 | 2 | A justru menekan: "Ditunggu kabar baiknya!" |
| 3 | Panjang cocok layar HP pesan pertama | 0 | 2 | A 755 karakter + tanda tangan; B 239–506. |
| 4 | Satu ajakan ringan (mudah dijawab ya/tidak) | 0 | 2 | A minta meeting/food tasting minggu ini — beban besar di pesan pertama. |
| 5 | Tidak mengarang klaim | 1 | 2 | A menambah "bahan segar & higienis, harga bersaing, tepat waktu" yang tidak diberikan pengguna. |
| 6 | Nada & sapaan lokal, tidak terkesan template/spam | 1 | 2 | A: 5 emoji + daftar centang ala broadcast promo. |
| 7 | Kepatuhan/keamanan (UU PDP, anti-blokir) | 0 | 2 | A tanpa pengingat apa pun. |
| 8 | Siap pakai (wa.me, jam kirim) | 0 | 2 | B memberi tautan terverifikasi + jam kirim WIB. |
| 9 | Pilihan varian | 0 | 2 | A satu versi. |
| 10 | Dicek otomatis/terukur | 0 | 2 | B menjalankan script dan memperbaiki draf sebelum ditampilkan. |
| | **Total (maks 20)** | **4** | **20** | |

## Kesimpulan
**Dengan skill jelas lebih baik** (20 vs 4). Kelebihan terbesar bukan hanya gaya bahasa, tapi hal yang tidak dilakukan agent umum tanpa diminta: opsi keluar, larangan klaim karangan, CTA ringan, pengecekan panjang, jam sesuai zona penerima, dan tautan wa.me. Bahan "sebelum/sesudah" untuk README tersedia di atas.

Catatan kejujuran: agent umum yang diberi prompt lebih lengkap ("pendek, sopan, tanpa emoji, ada opsi keluar") bisa mendekati kualitas B untuk teksnya; nilai tambah skill yang tidak tergantikan adalah konsistensi langkah (asal kontak wajib, penolakan sumber ilegal, script, zona waktu) tanpa pengguna awam harus tahu cara meminta.
