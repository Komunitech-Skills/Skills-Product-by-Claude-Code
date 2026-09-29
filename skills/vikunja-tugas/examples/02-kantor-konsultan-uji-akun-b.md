# Skenario 2 (uji Akun B) — Agensi/kantor konsultan, proyek klien, mode `dari-teks`

Lingkungan sama seperti skenario 1 (Vikunja 2.6.0 asli, `127.0.0.1:3456`). Proyek: "Agensi - Proyek
Klien PT Maju" (id 5).

## Perintah pengguna: tempel notulen grup WA
Input (`--teks`, notulen fiktif meniru gaya grup WA kantor konsultan):
```
- Andi: follow up supplier bata sebelum Jumat
- Siti: kirim invoice ke PT ABC besok, urgent
- Rapat kickoff dengan klien PT Maju 25/10 jam 10:00
Catatan: semua sudah dikoordinasikan lewat WA grup
```

```
$ python3 vikunja.py dari-teks --teks "..." --anggota "Andi,Siti"
DRAF 3 TUGAS (BELUM masuk Vikunja) -> disimpan di: draf-tugas-20260926-182217.json
1. follow up supplier bata sebelum Jumat (PIC: Andi; tenggat: 2026-10-02)
2. kirim invoice ke PT ABC besok, urgent (PIC: Siti; tenggat: 2026-09-27; mendesak)
3. Rapat kickoff dengan klien PT Maju 25/10 jam 10:00 (tenggat: 2026-10-25)
(1 baris lain diabaikan — bukan baris berawalan '-'/'*'/angka.)
```
**Verifikasi independen (semua benar):**
- Baris "Catatan: ..." memang diabaikan (tidak berawalan `-`/`*`/`1.`) dan dihitung ("1 baris lain") — sesuai dokumentasi.
- "Jumat" dari acuan Sabtu 26 Sep 2026 → 2 Okt 2026. Benar.
- "besok" dari acuan 26 Sep 2026 → 27 Sep 2026 (Minggu). Benar.
- "urgent" terdeteksi sebagai kata pemicu prioritas mendesak(4). Benar sesuai dokumentasi.
- "25/10" → 25 Oktober 2026, dan skrip pratinjau batch menunjukkan "Minggu, 25 Oktober 2026" — dicek manual: 26 Sep 2026 Sabtu + 29 hari = 25 Okt 2026 Minggu. Benar.
- File JSON draf **belum** memanggil Vikunja sama sekali (dikonfirmasi: tidak ada permintaan jaringan tercatat sebelum `tambah --batch` dijalankan).

## Lanjut ke `tambah --batch`
```
$ python3 vikunja.py tambah --batch draf-tugas-20260926-182217.json \
    --proyek "Agensi - Proyek Klien PT Maju"
PRATINJAU TAMBAH 3 TUGAS
1. follow up supplier bata sebelum Jumat ... Ditugaskan ke: Andi
2. kirim invoice ke PT ABC besok, urgent ... Prioritas: 4 (mendesak) ... Ditugaskan ke: Siti
3. Rapat kickoff dengan klien PT Maju 25/10 jam 10:00 ...
Belum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan ke Vikunja.

$ python3 vikunja.py tambah --batch draf-tugas-20260926-182217.json \
    --proyek "Agensi - Proyek Klien PT Maju" --ya
CATATAN: tugas #4 tersimpan, tapi GAGAL menugaskan ke 'Andi': Anggota 'Andi' tidak ditemukan di
proyek ini (atau token tidak berizin 'projects: projectusers'). Pastikan orang itu sudah ditambahkan
ke tim/proyek di Vikunja.
CATATAN: tugas #5 tersimpan, tapi GAGAL menugaskan ke 'Siti': Anggota 'Siti' tidak ditemukan ...
TERSIMPAN 3 TUGAS DI VIKUNJA:
- #4 follow up supplier bata sebelum Jumat (proyek id 5)
- #5 kirim invoice ke PT ABC besok, urgent (proyek id 5)
- #6 Rapat kickoff dengan klien PT Maju 25/10 jam 10:00 (proyek id 5)
```
Ini jalur error YANG BENAR untuk kasus ini: "Andi"/"Siti" adalah nama tebakan dari notulen, bukan
username Vikunja asli yang terdaftar di proyek itu (berbeda dari kasus "budi" di skenario 1, yang
usernya memang ada tapi gagal karena masalah token — lihat HASIL-UJI.md #1). Pesan yang ditampilkan
skrip ("tidak ditemukan ... atau token tidak berizin") sudah mencakup kedua kemungkinan itu, jadi
tidak menyesatkan pengguna meski sebabnya sebenarnya berbeda tiap kasus.

## Verifikasi silang: `minggu-ini` untuk proyek ini
```
$ python3 vikunja.py minggu-ini --proyek "Agensi - Proyek Klien PT Maju"
TUGAS 7 HARI KE DEPAN
Proyek: Agensi - Proyek Klien PT Maju
Jumlah: 2
- kirim invoice ke PT ABC besok, urgent (mendesak; jatuh tempo 27 Sep 2026)
- follow up supplier bata sebelum Jumat (jatuh tempo 2 Okt 2026)
```
Benar: tugas rapat kickoff (25 Okt) di luar jendela 7 hari sehingga tidak muncul — sesuai desain.
