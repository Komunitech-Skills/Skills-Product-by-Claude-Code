# Skenario 01 (normal) — Klinik gigi, kontrol behel

Hari ini (acuan uji): 26 September 2026 (`--hari-ini 2026-09-26`).

**Input pengguna:** "Catat Bu Rina, kontrol behel lagi 3 hari lagi, WA 0812-3456-7890. Dia
bilang boleh diingatkan."

**Perintah:**
```bash
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 tambah --nama "Bu Rina" \
  --wa "0812-3456-7890" --jenis "kontrol behel" --tanggal "3 hari lagi" --persetujuan ya
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 daftar
```

**Output nyata:**
```
Tersimpan #1: Bu Rina | Kontrol behel | 29 Sep 2026 | persetujuan: ya
H-3 (1)
  #1 Bu Rina | Kontrol behel | 29 Sep 2026 | 0812-3456-7890

DRAF PESAN (salin & kirim sendiri, JANGAN dikirim otomatis):

#1 Bu Rina (0812-3456-7890):
Halo Bu Rina, ini pengingat dari kami untuk jadwal kontrol behel Anda pada 29 Sep 2026. Mohon
konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. Terima kasih.
```

**Verifikasi independen tanggal:** 26 Sep 2026 + 3 hari = 29 Sep 2026. 29 Sep − 26 Sep = 3 hari
→ benar masuk kelompok H-3. Kalender: 29 September 2026 jatuh hari Selasa; script mencetak
"29 Sep 2026" (format pendek, sudah benar tanpa perlu nama hari di sini).

**Penilaian:** sesuai SKILL.md sepenuhnya — persetujuan ditanyakan implisit lewat kalimat
pengguna ("boleh diingatkan") sebelum `--persetujuan ya` diisi, jenis kunjungan umum (bukan
diagnosis), draf disertai peringatan wajib "salin & kirim sendiri". Lulus.
