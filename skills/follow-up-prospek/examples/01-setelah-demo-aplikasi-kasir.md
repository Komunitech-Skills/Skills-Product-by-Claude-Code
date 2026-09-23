# 01 — Follow-up setelah demo aplikasi kasir (WA, UMKM)

**Skenario:** S1 — tahap "setelah demo/meeting", prospek pemilik resto, saluran WA.

**Input pengguna:**
> Kemarin (22 Sept) saya demo aplikasi kasir KasirPintar Fiktif ke Pak Joni, pemilik Resto Padang Rasa Minang Fiktif di Depok. Paket 199rb/bulan, gratis setup. Dia bilang bagus, tapi mau diskusi dulu sama istrinya yang pegang keuangan. Dia sempat nanya apakah bisa cetak struk ke printer lama mereka (Epson TM-U220) — jawabannya bisa. Nama saya Rudi. Bikinin follow-up WA ya.

**Perintah script:**
```bash
python3 scripts/jadwal_followup.py --mulai 2026-09-22
```

## Output

### Jadwal follow-up – Pak Joni, Resto Padang Rasa Minang Fiktif (setelah demo)
Kontak terakhir (H+0): Selasa, 22 September 2026

| Ke | Rencana | Tanggal kirim | Catatan |
|---|---|---|---|
| 1 | H+1 | Rabu, 23 September 2026 (hari ini) | - |
| 2 | H+3 | Jumat, 25 September 2026 | - |
| 3 | H+7 | Selasa, 29 September 2026 | - |
| 4 | H+14 | Selasa, 6 Oktober 2026 | - |

### Pesan ke-1 · Rabu, 23 September 2026 · WA
Selamat siang, Pak Joni 🙏 Saya Rudi dari KasirPintar Fiktif, terima kasih atas waktunya kemarin. Ringkasnya: paket Rp 199.000/bulan, setup gratis, dan bisa langsung cetak struk ke printer Epson TM-U220 yang sudah ada di resto. Ada poin yang ingin Bapak tambahkan sebelum dibahas dengan Ibu?

### Pesan ke-2 · Jumat, 25 September 2026 · WA
Selamat pagi, Pak Joni. Karena keuangan dipegang Ibu, mungkin yang paling berguna untuk beliau adalah laporan penjualan harian & menu terlaris yang bisa dilihat dari HP tanpa harus ke kasir. Kalau berkenan, saya bisa kirim contoh tampilan laporannya untuk ditunjukkan ke Ibu. Mau saya kirimkan?

### Pesan ke-3 · Selasa, 29 September 2026 · WA
Pak Joni, supaya lebih mudah diputuskan bersama Ibu, ada dua pilihan: (1) saya jelaskan singkat lewat telepon/video call 10 menit dengan Bapak & Ibu sekaligus, atau (2) saya kirim ringkasan 1 halaman untuk dibaca santai. Mana yang lebih enak, Pak? Cukup balas 1 atau 2.

### Pesan ke-4 · Selasa, 6 Oktober 2026 · WA
Selamat siang, Pak Joni. Sepertinya aplikasi kasir belum jadi prioritas saat ini, dan itu sama sekali tidak apa-apa. Saya tidak akan mengirim pengingat lagi. Hasil demo kemarin tetap bisa jadi referensi, dan kalau suatu saat butuh, cukup chat nomor ini ya, Pak. Terima kasih 🙏

### Aturan main
- Kirim pukul 09.00–11.00 atau 13.00–15.00; untuk resto, hindari jam makan siang (11.00–13.00) & makan malam, serta waktu salat Jumat.
- Jika Pak Joni membalas di tengah urutan → hentikan urutan, tanggapi balasannya.
- Jika dijawab "tidak dulu" / "jangan dihubungi" → kirim terima kasih singkat, hapus dari daftar follow-up.
- Balasan umum:
  - "Mahal" → tanyakan kisaran anggaran & bandingkan dengan biaya kasir manual/selisih kas; tawarkan paket lebih kecil bila ada (jangan langsung diskon).
  - "Masih diskusi sama istri" → tawarkan bahan ringkas / call bersama (pesan ke-3).
  - "Nanti dulu" → tanyakan waktu yang tepat, hubungi sesuai janji.

### Asumsi
- Pesan ke-1 jatuh hari ini (H+1 dari demo kemarin) — bisa langsung dikirim.
- Contoh laporan penjualan harian & menu terlaris diasumsikan memang fitur KasirPintar Fiktif — **usulan, konfirmasi dulu** sebelum dikirim.
- Tidak ada promo/diskon yang ditawarkan karena tidak disebutkan.

## Catatan penguji
- Tanggal diverifikasi (22 Sep 2026 = Selasa; +1/+3/+7/+14 tidak ada yang jatuh akhir pekan).
- Bagus: pesan memakai detail nyata dari pengguna (printer Epson, istri pegang keuangan), tiap pesan punya tujuan berbeda, pesan pamit sopan, tidak ada urgensi palsu.
- Kurang (ringan): SKILL.md tidak membahas bila tanggal kirim sudah lewat / jatuh hari ini (script tidak memberi tanda); agent menambah "(hari ini)" secara inisiatif.
