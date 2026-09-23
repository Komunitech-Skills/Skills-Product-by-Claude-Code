# 01 — Katering langganan kantor, lewat 18 hari (tahap 5, tanpa denda)

**Skenario:** S1 — pelanggan lama B2B, tidak ada kesepakatan denda, sudah pernah diingatkan lewat WA.

**Input pengguna:**
> Saya punya usaha Katering Dapur Sehati Fiktif di Surabaya. Tagihan makan siang bulan Agustus ke PT Fiktif Makmur Sejahtera Rp 6.300.000, invoice INV-KT-0825, jatuh tempo 5 September. Sudah saya WA tanggal 8 dan 15 September tapi cuma dibaca. Yang ngurus Bu Dewi bagian GA. Pelanggan lama, nggak ada denda di kontrak. Tolong bikinin pesan tagihannya, rekening BCA 000-000-0000 a.n. Dapur Sehati Fiktif.

**Perintah script:**
```bash
python3 scripts/hitung_telat.py --nominal "Rp 6.300.000" --jatuh-tempo 2026-09-05 --tanggal 2026-09-23 --format teks
```
Hasil: sisa Rp 6.300.000, terlambat 18 hari, **Tahap 5** (pemberitahuan resmi + tawaran solusi/cicilan), tanpa denda.

## Output

### Ringkasan tagihan
| | |
|---|---|
| Invoice | INV-KT-0825 (makan siang Agustus 2026) |
| Sisa tagihan | Rp 6.300.000 |
| Jatuh tempo | 5 September 2026 |
| Keterlambatan per 23 September 2026 | 18 hari |
| Tahap | 5 – pemberitahuan resmi |
| Denda | Tidak ada (tidak ada kesepakatan tertulis) |

### Pesan tahap 5 · Email (surat PDF berkop) · kirim 23 September 2026

**Subjek:** Pemberitahuan Tagihan Lewat Jatuh Tempo – Invoice INV-KT-0825

```
KATERING DAPUR SEHATI FIKTIF
[Alamat], Surabaya · WA [nomor] · [email]

Perihal: Pemberitahuan Tagihan Lewat Jatuh Tempo – Invoice INV-KT-0825

Surabaya, 23 September 2026

Kepada Yth.
Ibu Dewi – Bagian General Affairs
PT Fiktif Makmur Sejahtera

Dengan hormat,
Terima kasih atas kepercayaan PT Fiktif Makmur Sejahtera menggunakan layanan makan siang kami.

Bersama ini kami sampaikan bahwa Invoice No. INV-KT-0825 untuk layanan makan siang bulan Agustus 2026 senilai Rp 6.300.000 telah jatuh tempo pada 5 September 2026, dan hingga 23 September 2026 pembayarannya belum kami terima (18 hari keterlambatan). Pengingat telah kami sampaikan melalui WhatsApp pada 8 dan 15 September 2026.

Kami mohon pembayaran dapat diselesaikan paling lambat 30 September 2026 ke rekening BCA 000-000-0000 a.n. Dapur Sehati Fiktif. Apabila terdapat kendala dalam proses pembayaran, kami bersedia membahas jadwal pembayaran bertahap yang dituangkan secara tertulis.

Jika pembayaran sudah dilakukan, mohon abaikan surat ini dan kirimkan bukti transfernya agar dapat segera kami catat.

Atas perhatian dan kerja samanya, kami ucapkan terima kasih.

Hormat kami,

[Nama]
Pemilik – Katering Dapur Sehati Fiktif
```

### Pesan pengantar · WA · kirim 23 September 2026 (setelah email terkirim)
Selamat siang, Bu Dewi. Kami kirimkan surat pemberitahuan terkait invoice INV-KT-0825 (makan siang Agustus, Rp 6.300.000) ke email Ibu. Mohon konfirmasi perkiraan tanggal pembayarannya ya, Bu. Jika ada kendala di proses internal, kami siap membantu, misalnya dengan mengirim ulang invoice/faktur yang dibutuhkan. Terima kasih 🙏

### Tahap berikutnya (jika belum dibayar)
- 5 Oktober 2026 (lewat 30 hari) → tahap 6: surat teguran resmi dengan tenggat 7 hari, dikirim ke pimpinan/bagian keuangan dengan tembusan Bu Dewi.

### Saran tindakan
- Karena pesan WA hanya dibaca, kirim surat ini lewat **email** agar ada jejak tertulis; bila memungkinkan tanyakan juga ke bagian keuangan (Finance/AP) — di banyak perusahaan GA hanya meneruskan invoice.
- Pastikan invoice sudah diterima bagian keuangan beserta dokumen yang biasanya diminta (PO, berita acara, faktur pajak jika PKP).
- Jika layanan bulan September berjalan terus, pertimbangkan membahas termin pembayaran ke depan agar piutang tidak menumpuk (jangan menghentikan layanan secara sepihak tanpa pemberitahuan tertulis).
- Simpan semua bukti pengiriman pesan dan email.

### Catatan hukum
Bukan nasihat hukum. Dasar: KUHPerdata (wanprestasi/somasi), UU ITE, UU PDP, UU Bea Meterai — per 2026-09-23. Untuk sengketa/gugatan, konsultasikan ke advokat.

## Catatan penguji
- Angka & tanggal diverifikasi manual: 5 → 23 September = 18 hari; tahap 5 benar; tanpa denda (sesuai aturan "denda hanya bila tertulis").
- Bagus: fakta kronologis (pengingat 8 & 15 Sept), jalan keluar (jadwal bertahap, abaikan bila sudah bayar), tidak ada ancaman.
- Penghentian layanan tidak disarankan secara sepihak — agent menambahkannya; SKILL.md tidak punya panduan untuk pelanggan langganan yang masih dilayani (ringan).
