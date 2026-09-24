# Uji A/B — Skenario normal 1 (IPA kelas 7 ekosistem 2 pertemuan): Tanpa skill vs Dengan skill

Input yang sama untuk keduanya: **"buatkan modul ajar IPA kelas 7 tentang ekosistem 2 pertemuan"**

## A — TANPA skill (agent generik, hanya memakai pengetahuan umum, tanpa membaca folder skill ini)

```
MODUL AJAR IPA - EKOSISTEM

A. Informasi Umum
Mapel: IPA | Kelas: VII | Alokasi waktu: 2 x pertemuan (2x45 menit)
Capaian Pembelajaran: Peserta didik memahami konsep ekosistem, interaksi makhluk hidup,
dan pelestarian lingkungan (CP Fase D). [Kode CP: 7.3 IPA]
Profil Pelajar Pancasila: Bernalar kritis, gotong royong

B. Tujuan Pembelajaran
- Siswa memahami pengertian ekosistem
- Siswa memahami komponen ekosistem

C. Kegiatan Pembelajaran
Pertemuan 1: Pendahuluan (10 menit) - Inti (60 menit) - Penutup (10 menit)
Pertemuan 2: Pendahuluan (10 menit) - Inti (60 menit) - Penutup (10 menit)
Kegiatan: guru menjelaskan materi ekosistem, siswa berdiskusi kelompok, presentasi.

D. Penilaian
Penilaian sikap, pengetahuan (tes tertulis), keterampilan (presentasi).

Semoga membantu! Silakan disesuaikan dengan kondisi kelas Anda.
```

### Masalah pada versi tanpa skill
1. **Mengarang kode CP** ("Kode CP: 7.3 IPA") seolah pasti benar — kode seperti itu tidak
   pernah ada di format resmi BSKAP (CP tidak berkode angka mapel per kelas seperti KTSP
   lama). Guru awam bisa menempel ini ke dokumen resmi tanpa curiga → risiko nyata.
2. **Menit tidak dijumlahkan/tidak diverifikasi**: "2x45 menit" ditulis di header lalu
   rincian pendahuluan+inti+penutup = 10+60+10 = 80 menit — **tidak sama** dengan 90
   menit (2x45) yang disebut di atasnya. Guru yang percaya begitu saja jadwalnya bisa
   kacau (kurang 10 menit tiap pertemuan). Tidak ada yang menghitung ulang.
3. **Menit/JP salah untuk SMP**: dipakai asumsi umum "45 menit" (durasi SMA/SMK), padahal
   SMP/MTs adalah **40 menit**/JP — bukan hasil pengecekan aturan Indonesia yang benar,
   sekadar tebakan generik.
4. **Tujuan Pembelajaran pakai kata kerja tidak terukur** ("memahami" tanpa kelanjutan
   yang bisa diamati/dinilai) — tidak sesuai prinsip TP yang baik di Kurikulum Merdeka.
5. **Tidak ada konteks lokal Indonesia** sama sekali (tidak ada sawah/pasar/UMKM/budaya
   daerah) — generik, bisa dipakai negara mana pun.
6. **Tidak ada LKPD, tidak ada soal+kunci+rubrik** meski secara implisit "Modul Ajar"
   idealnya melampirkan itu — hasil terasa seperti kerangka kosong yang masih harus
   dikerjakan ulang oleh guru.
7. Tidak ada pengecekan/pengakuan bahwa CP di atas belum tentu benar — disajikan seolah
   sudah final dan siap dipakai.

## B — DENGAN skill (`rencana-pelajaran-guru`)

Lihat hasil lengkap di `examples/01-uji-independen-modul-ajar-ipa-kelas7-ekosistem.md` (uji independen).
Ringkasan pembeda:
- CP ditulis sebagai **ringkasan umum** + ditandai jelas `(cek CP resmi — cocokkan dengan
  dokumen resmi IPA Fase D BSKAP No. 046/H/KR/2025)` — **tidak** mengarang kode/kutipan CP.
- Menit/JP benar untuk SMP (40 menit), dan total menit tiap pertemuan **dihitung &
  diverifikasi** lewat `scripts/hitung_alokasi_waktu.py` (status COCOK, dibuktikan dengan
  log JSON di file skenario 01).
- Tujuan Pembelajaran memakai kata kerja operasional & terukur ("menjelaskan", "menyusun",
  "menganalisis").
- Konteks lokal konkret: ekosistem sawah/kebun sekolah, alih fungsi lahan, pestisida —
  bukan generik.
- Paket lengkap: Modul Ajar + LKPD ("Ekosistem Sawah/Kebun Sekitar Kita") + 5 soal uraian
  dengan kunci jawaban terverifikasi + rubrik skor eksplisit (nilai akhir dihitung, bukan
  dikira).
- Diferensiasi (pengayaan/remedial) dan asesmen diagnostik-formatif-sumatif disertakan
  dengan instrumen konkret, bukan sekadar nama jenisnya.
- Ditutup dengan asumsi yang dipakai + 3 opsi revisi spesifik.

## Perbandingan berdampingan

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Kode/teks CP | **Mengarang** kode "7.3 IPA" seolah resmi | Ringkasan umum + jujur ditandai "cek CP resmi" |
| Menit/JP SMP | Salah (pakai 45 menit, harusnya 40) | Benar (40 menit), sesuai `dasar-kurikulum.md` §3 |
| Total menit vs rincian kegiatan | **Tidak cocok** (header 90’ vs rincian 80’), tidak ada verifikasi | Dihitung & diverifikasi via script, status COCOK, log tersimpan |
| Tujuan Pembelajaran | Kata kerja tidak terukur ("memahami") | Kata kerja operasional & terukur |
| Konteks lokal | Tidak ada | Sawah/kebun, alih fungsi lahan, pestisida (konkret) |
| LKPD & soal+kunci+rubrik | Tidak ada | Lengkap, kunci dihitung ulang, rubrik skor eksplisit |
| Diferensiasi | Tidak disebutkan | Pengayaan & remedial konkret |
| Siap tempel Word/Google Docs | Perlu banyak diedit ulang oleh guru | Siap tempel + instruksi cara pindah ke Word/Docs |

## Kesimpulan
Skill **jelas lebih baik**: versi tanpa skill memuat kesalahan yang secara nyata
berbahaya untuk pengguna awam guru — kode CP karangan yang bisa ditempel ke dokumen resmi
tanpa curiga, dan total menit kegiatan yang tidak cocok dengan jam pelajaran sekolah
(bisa membuat jadwal pelajaran berikutnya kacau). Skill memperbaiki keduanya secara
struktural (jujur soal CP, verifikasi waktu wajib), bukan hanya kebetulan lebih rapi.
