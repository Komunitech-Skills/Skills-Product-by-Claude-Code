# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama dengan S1):**
> Saya punya usaha Katering Dapur Sehati Fiktif di Surabaya. Tagihan makan siang bulan Agustus ke PT Fiktif Makmur Sejahtera Rp 6.300.000, invoice INV-KT-0825, jatuh tempo 5 September. Sudah saya WA tanggal 8 dan 15 September tapi cuma dibaca. Yang ngurus Bu Dewi bagian GA. Pelanggan lama, nggak ada denda di kontrak. Tolong bikinin pesan tagihannya, rekening BCA 000-000-0000 a.n. Dapur Sehati Fiktif.

## Output TANPA skill (AI agent biasa, lengkap)
```
Berikut draf pesan penagihan yang bisa Anda kirim ke Bu Dewi:

"Selamat siang Bu Dewi,

Mohon maaf mengganggu waktunya. Kami dari Katering Dapur Sehati ingin mengingatkan kembali
mengenai pembayaran invoice INV-KT-0825 sebesar Rp6.300.000 yang sudah jatuh tempo sejak
5 September. Kami sudah mengirimkan pesan sebelumnya namun belum mendapat tanggapan.

Mohon segera dilakukan pembayaran ke rekening BCA 000-000-0000 a.n. Dapur Sehati. Apabila
tidak ada pembayaran dalam waktu 3 hari, dengan berat hati kami terpaksa menghentikan layanan
katering dan mengenakan denda keterlambatan sesuai ketentuan yang berlaku.

Terima kasih atas perhatiannya."

Tips: Jika tetap tidak ada respons, Anda bisa mengirim somasi melalui pengacara.
```

## Output DENGAN skill
Lihat `01-katering-kantor-lewat-18-hari.md` (ringkasan hitungan, surat tahap 5, WA pengantar, jadwal tahap berikutnya, saran tindakan, catatan hukum).

## Perbandingan

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Hitungan | Tidak menyebut berapa hari terlambat | 18 hari (script), tahap 5 ditentukan jelas |
| Denda | **"mengenakan denda keterlambatan sesuai ketentuan yang berlaku"** — padahal pengguna bilang tidak ada denda di kontrak (ancaman tanpa dasar) | Tanpa denda; aturan "denda hanya bila tertulis" |
| Ancaman | Menghentikan layanan dalam 3 hari (sepihak, bisa merusak hubungan pelanggan lama) | Tenggat wajar (30 Sept), tawaran jadwal bertahap, tanpa ancaman |
| Format | Satu pesan WA | Surat resmi berkop via email + WA pengantar (sesuai tahap 5) |
| Fakta kronologis | "sudah mengirim pesan sebelumnya" | Tanggal pengingat 8 & 15 Sept disebut |
| Langkah lanjut | "somasi lewat pengacara" (lompat) | Jadwal tahap 6 (5 Okt), saran cek bagian keuangan & dokumen, simpan bukti |
| Jalan keluar | Tidak ada | "Abaikan bila sudah bayar", jadwal bertahap tertulis |

## Penilaian
Hasil dengan skill **jelas lebih baik**: versi tanpa skill mengancam denda yang tidak pernah disepakati (tidak sah & merusak kepercayaan) dan penghentian layanan sepihak, tanpa tahapan. Skill memberi hitungan pasti, dokumen yang sesuai tahap, dan langkah lanjutan yang sah.
