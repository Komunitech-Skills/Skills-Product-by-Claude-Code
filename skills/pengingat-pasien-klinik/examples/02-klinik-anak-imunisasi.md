# Skenario 02 (normal) — Klinik anak, jadwal imunisasi

Hari ini (acuan uji): 26 September 2026.

**Input pengguna:** "Ada jadwal imunisasi Bayi Aisyah (anaknya Ibu Dewi) besok, nomor ibunya
081234567890, boleh diingatkan. Tolong buatkan drafnya atas nama Klinik Anak Ceria."

**Perintah:**
```bash
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 tambah \
  --nama "Bayi Aisyah (Ibu Dewi)" --wa "081234567890" --jenis "imunisasi" \
  --tanggal "besok" --persetujuan ya
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 draf --id 2 --klinik "Klinik Anak Ceria"
```

**Output nyata:**
```
Tersimpan #2: Bayi Aisyah (Ibu Dewi) | Imunisasi | 27 Sep 2026 | persetujuan: ya
Halo Bayi Aisyah (Ibu Dewi), ini pengingat dari Klinik Anak Ceria untuk jadwal imunisasi Anda
pada 27 Sep 2026. Mohon konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas
pesan ini. Terima kasih.
```

**Verifikasi independen tanggal:** 26 Sep 2026 + 1 hari = 27 Sep 2026 ("besok"). Benar.
Nomor WA `081234567890` (11 digit, awalan 0) dinormalisasi ke `6281234567890` — sesuai aturan
normalisasi nomor Indonesia.

**Catatan konten draf:** kalimat draf tidak menyebut nama penyakit apa pun, hanya "jadwal
imunisasi" (jenis kunjungan umum) — sesuai batasan "tanpa diagnosis". Nama klinik yang diberikan
staf muncul persis di draf ("Klinik Anak Ceria"), bukan default "kami". Lulus.

**Catatan gaya penulisan nama:** karena ini pasien anak/bayi, draf tetap ditujukan "Anda" (format
tetap, sesuai SKILL.md: "tanggal, nama, dan jenis kunjungan tidak boleh diubah" tapi bahasa boleh
diperhalus). Staf disarankan menyunting salam menjadi "Halo Ibu Dewi, ini pengingat untuk jadwal
imunisasi Aisyah..." sebelum dikirim — ini konsisten dengan izin SKILL.md untuk memperhalus
bahasa draf selama tanggal/nama/jenis tidak berubah.
