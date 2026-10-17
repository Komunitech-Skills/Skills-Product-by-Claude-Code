# Uji 02 (penguji independen, Akun B) - Kedai kopi, Meta Ads lokal radius 3 km

> Uji simulasi agent oleh penguji terpisah, 2026-09-26. Data fiktif. Skenario: **normal 2**.

## Permintaan pengguna
"Kedai kopi saya di Bandung. Iklan IG/FB Rp1,2 jt sebulan, arahnya ke WhatsApp buat pesan antar
(radius 3 km). Chat banyak tapi yang order dikit. Tolong cek pengaturannya." (disertai screenshot
Ads Manager, Kualitas Akun, pengaturan ad set)

## Perilaku agent
- `daftar --platform meta`. Iklan hanya ke WA/DM → M01 & M17 `tidak_berlaku` (sesuai kolom
  `tidak_berlaku_jika`); M20 `tidak_berlaku` (belum punya audiens pengirim pesan).
- Tanya sekali: siapa admin, jam balas WA, catatan chat → order, frekuensi 7 hari.
- `roas-impas` tidak dijalankan (pemilik tidak tahu laba per pesanan) → M10 `tidak_tahu`.

## Output script (ringkas)
```
$ python3 scripts/skor_audit.py hitung jawaban.csv --belanja meta=1,2jt --mulai 2026-09-28 --usaha "Kedai Kopi Senja"
Skor gabungan: 42,7 / 100 (Kritis) - FINAL; bobot: porsi belanja
- Meta Ads: 42,7/100 (Kritis); bukti 90,0% (final)
    Pelacakan 31,3 | Struktur 50,0 | Audiens 0,0 | Anggaran 100,0 | Materi 45,5 | Halaman 50,0 | Frekuensi 0,0 | Pengecualian belum tahu
PRIORITAS: 1 M04 (15, +3,6, sebagian) · 2 M02 (10, +6,6, sebagian) · 3 M03 (9, +7,9) · 4 M18 (9, +7,9)
           5 M08 (9, +5,3) · 6 M05 (9, +4,3) · 7 M09 (6) · 8 M16 (6) · 9 M13 (6) · 10 M14 (6) · 11 M19 (2)
Rencana: H1 M04,M02 · H2 M03,M18,M08 · H3 M05,M09 · H4 M16 · H5 M13 · H6 diam · H7 laporan; antrean M14, M19
```

## Jawaban akhir agent (ringkas)
Skor **42,7/100 – Kritis – final (bukti 90%)**.
1. **Kampanyenya "Boost" & Traffic, bukan Pesan** – Meta mencari orang yang suka klik, bukan yang
   mau chat. Buat kampanye baru tujuan Interaksi → Pesan WhatsApp (tujuan kampanye lama tidak bisa diganti).
2. **Jangkauan seluruh Bandung +25 km, padahal antar hanya 3 km** – pasang pin kedai, radius 3 km.
3. **Chat iklan tidak dicatat sampai jadi order** – beri label "Iklan" di WhatsApp Business, hitung tiap Sabtu.
Plus: barista lama masih admin (hapus), iklan jalan sampai 22.00 tapi WA hanya dibalas 08–17
(atur jadwal iklan/admin).

## Catatan penguji
- Angka cocok 100% dengan verifikasi independen.
- ❌ **Klaim usang di M08:** perbaikan berbunyi "untuk layanan lokal pilih orang yang **tinggal** di
  lokasi tersebut". Meta sudah menghapus pilihan *Tinggal di / Baru-baru ini di / Bepergian di*;
  kini hanya "Tinggal di atau baru-baru ini berada di lokasi ini"
  ([Search Engine Land](https://searchengineland.com/new-update-to-meta-ads-location-targeting-404124),
  [Jon Loomer](https://www.jonloomer.com/big-change-to-meta-ads-location-targeting/)). Pemilik
  kedai akan mencari menu yang tidak ada. Agent penguji mengganti saran itu dengan "radius 3 km dari pin".
- ⚠️ **Saran bertabrakan:** M18 (frekuensi 5,8 → "perluas audiens") dijadwalkan di hari yang sama
  dengan M08 (sempitkan ke 3 km). Untuk usaha hiperlokal, frekuensi tinggi wajar; solusi yang benar
  adalah menurunkan anggaran/menambah materi, bukan memperluas. Patokan frekuensi ≤ 3 sudah ditandai
  "patokan Komunitech", tetapi SKILL.md tidak meminta agent merekonsiliasi perbaikan yang berlawanan.
- M05 "tujuan tidak bisa diganti setelah terbit" — benar (sesuai panduan umum Meta).

## Penyegaran v1.0.7 (2026-10-17)
> Hasil, angka, dan skor di atas **tidak diubah**. Dicocokkan dengan SKILL.md v1.0.7: skenario ini memakai screenshot Ads Manager sehingga bukti akhirnya 90% (≥ 60%) → tetap **Format output audit lengkap**. Bedanya di v1.0.7: pertanyaan (admin, jam balas WA, catatan chat → order, frekuensi 7 hari) diajukan **di akhir balasan, maks. 5**, setelah hasil sementara dari screenshot, bukan sebelum ada hasil. Karena harga/modal belum ada, ROAS impas tidak ditebak: jelaskan cara hitung impas dalam satu kalimat dan jadikan harga & modal pertanyaan nomor 1. Di kanal chat, ID cek (M04, M02, ...) boleh dibuang dan tanpa tabel Markdown. Saran M08 di skrip sudah diperbarui sejak v1.0.1 (lihat `08-uji-ulang-v101-akun-b.md`). Skrip v1.0.7 tidak mengubah rumus, jadi skor 42,7/100 tetap berlaku untuk jawaban yang sama.
