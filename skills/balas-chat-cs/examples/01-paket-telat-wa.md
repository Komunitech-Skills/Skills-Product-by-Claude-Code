# 01 — Komplain paket telat (WhatsApp, pelanggan kesal)

**Skenario:** S1 — komplain umum, emosi "kesal", data resi diberikan pengguna.

**Input pengguna:**
> Balesin chat ini dong: "kak paketku udah 5 hari blm sampe, katanya 2-3 hari. gmn sih?? mau buat oleh2 lusa". Tokoku Kopi Lereng Fiktif, jual kopi bubuk, kirim pakai JNE REG, resinya JP0000FIKTIF01, status terakhir kemarin sore di gudang transit Surabaya. Tujuannya Sidoarjo.

## Output

**Balasan (siap kirim):**
Halo Kak, mohon maaf banget paketnya belum sampai padahal sudah lewat dari perkiraan, apalagi mau dipakai buat oleh-oleh lusa 🙏

Kami sudah cek resi JNE **JP0000FIKTIF01**: status terakhir kemarin sore paket sudah di gudang transit Surabaya, jadi posisinya sudah dekat dengan Sidoarjo. Hari ini kami bantu hubungi JNE supaya paket Kakak diprioritaskan untuk diantar.

Kami kabari perkembangannya paling lambat pukul 16.00 hari ini ya, Kak.

— Admin Kopi Lereng Fiktif

**Alternatif lebih singkat:**
Mohon maaf Kak paketnya telat 🙏 Status resi JP0000FIKTIF01 terakhir di gudang transit Surabaya (sudah dekat Sidoarjo). Hari ini kami follow-up ke JNE dan kabari Kakak paling lambat pukul 16.00 ya.

**Catatan untuk admin:**
- Hubungi JNE hari ini (call center/akun bisnis/cabang pengirim) dengan nomor resi; minta estimasi antar ke Sidoarjo.
- Jangan menjanjikan "pasti sampai besok" sebelum ada konfirmasi dari JNE.
- Tepati janji kabar pukul 16.00 — walaupun belum ada info baru, tetap kabari statusnya.
- Jika sampai H-1 acara paket belum bergerak: siapkan opsi (usulan, konfirmasi pemilik toko dulu) kirim ulang dengan layanan lebih cepat, lalu klaim paket lama ke JNE.
- Jika status berubah "terkirim" tapi pelanggan belum terima: minta cek ke tetangga/satpam/keluarga, lalu ajukan investigasi ke JNE.

## Catatan penguji
- Mengikuti alur E-S-T dari `references/alur-komplain.md` (kasus 2: paket telat): empati spesifik (oleh-oleh lusa), fakta resi dari pengguna, tindak lanjut dengan jam yang jelas.
- Tidak mengarang estimasi tiba; opsi kirim ulang ditandai "usulan".
- Jam "16.00" adalah pilihan agent — idealnya disesuaikan jam operasional toko (ringan; bisa ditanyakan).
