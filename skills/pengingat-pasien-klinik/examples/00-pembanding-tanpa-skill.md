# Uji A/B — Skenario 01 (klinik gigi, kontrol behel)

**Input pengguna:** "Catat Bu Rina, kontrol behel lagi 3 hari lagi, WA 0812-3456-7890. Dia bilang boleh diingatkan."
(hari ini 26 September 2026, acuan `--hari-ini 2026-09-26`)

## TANPA skill (agent generik, tanpa alat/instruksi khusus)
Agent generik biasanya hanya membalas dalam bentuk saran umum, karena tidak punya tempat
penyimpanan maupun aturan privasi kesehatan built-in:

> "Baik, saya catat: Bu Rina, kontrol behel, tanggal kira-kira 29 September 2026, WA
> 0812-3456-7890. Untuk pengingat, Anda bisa mengirim pesan WhatsApp seperti: 'Halo Bu Rina,
> jangan lupa kontrol behel tanggal 29 September ya.' Saya sarankan simpan datanya di
> spreadsheet Excel untuk klinik Anda."

Masalah:
- Data tidak benar-benar tersimpan di mana pun — hilang begitu sesi chat berakhir. Tidak ada
  `id`, tidak bisa dicari/diubah/dihapus nanti.
- Tidak ada mekanisme H-3/H-1/hari-ini/terlambat otomatis — agent harus dihitung ulang manual
  setiap hari, dan sering salah kalau ditanya lagi minggu depan.
- Tidak ada penanganan persetujuan (consent) — agent tidak menanyakan apakah Bu Rina setuju
  dihubungi, dan tidak ada mekanisme agar pasien yang menolak tidak pernah muncul lagi.
- Tidak ada penjagaan agar diagnosis/nama penyakit tidak ikut tersimpan bila staf lain kelak
  mengetik "kontrol diabetes" di kolom jenis.
- Draf pesan konsisten hanya kebetulan; tidak ada jaminan tanggal/nama/jenis tidak berubah
  saat diminta ulang, dan tidak ada larangan eksplisit "jangan dikirim otomatis".

## DENGAN skill `pengingat-pasien-klinik`
```
$ python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 tambah --nama "Bu Rina" \
    --wa "0812-3456-7890" --jenis "kontrol behel" --tanggal "3 hari lagi" --persetujuan ya
Tersimpan #1: Bu Rina | Kontrol behel | 29 Sep 2026 | persetujuan: ya

$ python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 daftar
H-3 (1)
  #1 Bu Rina | Kontrol behel | 29 Sep 2026 | 0812-3456-7890

DRAF PESAN (salin & kirim sendiri, JANGAN dikirim otomatis):

#1 Bu Rina (0812-3456-7890):
Halo Bu Rina, ini pengingat dari kami untuk jadwal kontrol behel Anda pada 29 Sep 2026. Mohon
konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. Terima kasih.
```

Perbedaan nyata:
- Data tersimpan permanen di `pasien/DAFTAR.csv` dengan `id` unik — bisa dicari, diubah,
  dijadwalkan ulang, atau dihapus kapan pun, oleh staf lain sekalipun.
- Tanggal H-3 (29 Sep) dihitung oleh script, bukan ditaksir agent — konsisten setiap hari
  ditanya ulang, termasuk lintas bulan/zona waktu.
- Persetujuan wajib diisi saat pencatatan pertama dan otomatis menyaring pasien yang menolak
  dari seluruh daftar/draf/ringkasan.
- Jenis kunjungan disaring dari kata yang menyerupai diagnosis (lihat skenario 05).
- Draf pesan berformat konsisten dan selalu disertai peringatan "salin & kirim sendiri, JANGAN
  dikirim otomatis" — sesuai keputusan pemilik (WA lewat OpenClaw tidak resmi, manusia yang kirim).

## Kesimpulan
Dengan skill jelas lebih unggul: penyimpanan nyata & bisa diaudit, perhitungan tanggal yang
diverifikasi, penegakan consent/privasi otomatis, dan batas kirim-manual yang eksplisit — bukan
sekadar teks generik dari agent. Skill memberi nilai tambah signifikan dibanding tanpa skill.
