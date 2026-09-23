# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama dengan S1):**
> Balesin chat ini dong: "kak paketku udah 5 hari blm sampe, katanya 2-3 hari. gmn sih?? mau buat oleh2 lusa". Tokoku Kopi Lereng Fiktif, jual kopi bubuk, kirim pakai JNE REG, resinya JP0000FIKTIF01, status terakhir kemarin sore di gudang transit Surabaya. Tujuannya Sidoarjo.

## Output TANPA skill (AI agent biasa, lengkap)
```
Halo Kak! Mohon maaf atas ketidaknyamanannya ya 🙏😊

Paket Kakak dengan resi JP0000FIKTIF01 saat ini sudah berada di gudang transit Surabaya, jadi
kemungkinan besar akan sampai besok ke Sidoarjo. Keterlambatan ini biasanya disebabkan oleh
volume paket yang tinggi di ekspedisi, jadi di luar kendali kami ya Kak.

Mohon ditunggu sebentar lagi ya Kak, pasti sampai sebelum lusa kok! Terima kasih atas
kesabarannya 😊🙏
```

## Output DENGAN skill
Lihat `01-paket-telat-wa.md` (balasan + versi singkat + catatan admin).

## Perbandingan

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Empati | Generik ("mohon maaf atas ketidaknyamanannya") + emoji senyum yang tidak cocok untuk pelanggan kesal | Spesifik (lewat perkiraan, untuk oleh-oleh lusa), emoji hemat |
| Janji | **"pasti sampai sebelum lusa kok!"**, "kemungkinan besar besok" — janji yang tidak bisa dijamin toko | Tidak menjanjikan tiba; menjanjikan hal yang bisa dikendalikan (hubungi JNE, kabar jam 16.00) |
| Menyalahkan | "di luar kendali kami" (defensif, melempar ke kurir) | Tidak defensif; toko mengambil tindakan |
| Tindak lanjut | "Mohon ditunggu" — pasif | Tindakan konkret + waktu kabar |
| Panduan admin | Tidak ada | Checklist: hubungi JNE, rencana cadangan H-1 (usulan), status "terkirim" tapi belum diterima |

## Penilaian
Hasil dengan skill **jelas lebih baik**: versi tanpa skill membuat janji palsu ("pasti sampai sebelum lusa") yang berpotensi memicu komplain kedua dan ulasan buruk, serta bernada defensif. Skill menghasilkan balasan E-S-T yang menenangkan tanpa salah janji, ditambah panduan tindakan untuk admin.
