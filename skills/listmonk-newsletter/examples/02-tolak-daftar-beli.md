# 02 - Menolak daftar hasil beli (hasil nyata)

**Pengguna:** "Saya beli database 5.000 email UMKM Jawa Barat, kirim promo ke semuanya."

**Agent:** menolak dengan sopan, menjelaskan alasan (tidak ada persetujuan mereka, melanggar UU PDP 27/2022, email berisiko diblokir SMTP), lalu menawarkan alternatif: formulir daftar di website/QR di kasir, insentif kecil (voucher) untuk pendaftar, dan double opt-in.

Script juga menolak bila tetap dicoba:
```
$ listmonk.py impor kontak.csv --list 4 --sumber-persetujuan "beli database dari vendor" --saya-punya-izin
DITOLAK: daftar hasil beli/sewa/scraping tidak boleh dikirimi newsletter (tidak ada persetujuan mereka; melanggar UU PDP 27/2022). Impor hanya orang yang mendaftar sendiri.
(kode keluar 6; tidak ada data terkirim ke listmonk)
```
Tanpa `--sumber-persetujuan`/`--saya-punya-izin` juga ditolak (kode 6).
