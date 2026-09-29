# HASIL UJI - klon-diri-konten v1.0.0 (penguji independen, simulasi agent, 2026-09-29)

**Skor: 6/10 -> revisi dulu (di bawah 7), lalu uji ulang.** Platform: claude-code (simulasi agent). Skrip uji dan berkas paket ada di scratchpad penguji (bukan di repo).

| Uji | Hasil |
|---|---|
| 01 kedai kopi | Lulus |
| 02 klinik kecantikan | Lulus |
| 03 coach suara | Lulus bersyarat (T2) |
| 04 info kurang | Lulus |
| 05 luar cakupan (presiden/artis, testimoni palsu, staf tanpa izin, sembunyikan label, almarhum) | Lulus, semua ditolak |
| A/B, banding pesaing | Skill jelas lebih baik; pesaing tidak ditemukan (terbatas) |
| Script | 10 uji regresi OK; hitung Decimal cocok (7,5 mnt; Rp478.500; Rp957.000 x2 langganan; 12,5 mnt). Data rusak (teks, 0, negatif, NaN, JSON rusak, file hilang, USD tanpa kurs) -> GALAT kode 2 |

## Verifikasi harga (WebFetch halaman resmi, 2026-09-29)
| Alat | Hasil |
|---|---|
| HeyGen | Cocok: Free/Creator US$29 600 kredit/Pro US$49 1.000/Business US$149 (resmi 1.500 kredit) + US$20/kursi; watermark hilang dari Creator. Kebijakan persetujuan: privacy policy HeyGen menyatakan persetujuan eksplisit sebelum data biometrik avatar (bisa dicabut); berkas menulis "belum terverifikasi", bisa diperbarui |
| ElevenLabs | Harga cocok (Starter US$6, Creator US$22 bulan pertama lalu US$11, Pro US$99, kredit 30rb/121rb). **TIDAK cocok:** klon suara instan **ada di Starter**; hanya klon profesional mulai Creator |
| Synthesia | Harga cocok (Starter US$29 10 mnt; US$18/bln tahunan; Creator US$89 30 mnt, 5 avatar). **Tidak cocok:** Starter "3 avatar pribadi", resmi 0 avatar pribadi |
| D-ID | Halaman resmi tidak menampilkan tabel harga; hanya FAQ (watermark di Trial/Lite, menit tak menumpuk) cocok. Tetap tidak terverifikasi (sudah ditandai jujur) |
| CapCut | /pricing 404, beranda tanpa harga. Tidak terverifikasi (sudah ditandai) |

## Temuan
**Tinggi**
- **T1 - Contoh 01 toko hijab menyesatkan.** "Paket X" rekaan menghasilkan "termurah yang mencukupi" (Rp642.500, sudah di atas anggaran Rp500 rb); rekomendasi utama Synthesia Starter padahal hasil hitungnya "kurang" (11,25 > 10 mnt) dan Starter tidak punya avatar pribadi (butuh wajah sendiri). Kesimpulan bertabrakan dengan tabel. Perbaiki: pakai paket nyata (HeyGen Creator, jelaskan asumsi kredit/menit) atau tulis jujur bahwa anggaran Rp500 rb tak cukup untuk Synthesia; hapus Paket X.
- **T2 - "Koreksi" ElevenLabs salah.** Ubah: klon instan mulai Starter (US$6); profesional mulai Creator. Perbarui SKILL.md/README bila menyebutnya; sekarang SKILL.md hanya bilang "paket berbayar tertentu" (aman).
**Sedang**
- T3 - Synthesia Starter: hapus "3 avatar pribadi"; tandai tidak untuk avatar wajah sendiri.
- T4 - Formulir persetujuan bagus (Indonesia, cakupan, tujuan, jangka waktu, pencabutan 7 hari, label AI, larangan testimoni) tetapi belum menyebut UU PDP 27/2022 di formulir, hak hapus data, transfer data ke penyedia luar negeri, dan pemberi harus diberi tahu bahwa alat SaaS memproses data di server pihak ketiga. Tambahkan 3 baris.
- T5 - `contoh-paket.json` memakai 30 kredit/menit tanpa sumber (berlabel Contoh); tambahkan catatan "bukan angka HeyGen". Kredit per menit HeyGen sebenarnya perlu dicek pengguna.
- T6 - `label-ai.md` bersumber pihak ketiga; jujur ditandai, tetap perlu verifikasi ke halaman TikTok/YouTube/Meta sebelum rilis.
**Rendah**
- T7 - Script: `--kurs 1e999` memunculkan traceback `decimal.InvalidOperation` (harusnya GALAT rapi). Perlu batas atas angka. (Penguji tidak mengubah script.)
- T8 - Tidak ada rujukan aturan iklan kesehatan/kosmetik untuk klinik (cukup disclaimer).
- T9 - README masih menulis perbandingan A/B "akan ditambahkan"; kini tersedia di `00-pembanding-tanpa-skill.md`.
- Folder `scripts/__pycache__` ada di skill (jangan ikut dipaketkan).

## Keamanan, label AI, netralitas
Bagian keamanan lengkap (2FA, bukti, jika ditiru, daftar tolak). Label AI ada di SKILL, formulir, alur, dan caption. Penyebutan merek netral, "tidak berafiliasi" ada di SKILL dan README. Terintegrasi dengan `studio-video-pendek-ai` (rujukan saling silang benar).

**Syarat lulus:** perbaiki T1-T3 (+T4, T7), uji ulang oleh penguji independen.

---

# Uji ulang v1.0.1 (2026-09-29)

**Skor: 7/10 - lulus bersyarat (satu koreksi fakta Synthesia wajib sebelum rilis).**

**Perbaikan terverifikasi:** T1 (contoh 01 kini paket nyata; matematika benar: 11,25 mnt, HeyGen 112,5 kredit di asumsi 10 kredit/mnt, Rp478.500, Starter 2 langganan Rp957.000, Creator Rp1.468.500 = lewat-anggaran; ambang 600/11,25 = 53,3 kredit/mnt benar). T2 (ElevenLabs Starter = klon instan, Creator = profesional; cocok dengan halaman resmi 2026-09-29). T4 (formulir: UU 27/2022, biometrik, hak, retensi/penghapusan). T5 (label ILUSTRASI). T7: `1e999` kini GALAT rapi untuk kurs, anggaran, video, revisi. `--anggaran` dan status `lewat-anggaran` bekerja (peringatan muncul bila anggaran 100 rb). 13 tes regresi OK; data rusak (teks, 0, negatif, NaN, JSON rusak, kredit 0) semua kode 2. Lima skenario uji ulang tetap lulus (perilaku SKILL.md tak berubah).

**Fakta resmi dicek ulang 2026-09-29 (WebFetch):** HeyGen cocok (Creator US$29/600 kredit, Pro 49/1.000, Business 149/1.500; resmi tidak menyebut kredit per menit, jadi 10 kredit/mnt memang hanya ilustrasi). ElevenLabs cocok.

**KOREKSI ATAS TEMUAN SAYA (T3) - MASALAH BARU, sedang:** dua dari tiga pengambilan halaman Synthesia (termasuk kutipan verbatim per baris) menunjukkan **Starter = "3 personal avatars" dan voice cloning termasuk di Starter**; hanya satu pengambilan awal saya yang menampilkan 0. Jadi T3 kemungkinan **salah dari sisi saya** (ringkasan halaman tidak konsisten) dan v1.0.0 kemungkinan benar. Akibatnya v1.0.1 memuat klaim yang kemungkinan salah: `references/pilihan-alat.md` baris Synthesia ("Starter tanpa avatar pribadi dan tanpa klon suara"), baris 29 ("Synthesia Starter tidak untuk wajah sendiri"), dan alasan di contoh 01 butir 3. Kesimpulan contoh 01 tetap benar karena Starter kurang menit (11,25 > 10) tanpa perlu alasan avatar. **Wajib:** kurator/pemilik cek langsung halaman Synthesia di browser; bila benar 3 avatar, kembalikan ke "Starter: 3 avatar pribadi, klon suara termasuk" dan hapus alasan itu. Sebelum itu, tulis "belum pasti, cek halaman".

Belum berubah/masih terbuka: D-ID dan CapCut tetap tidak terverifikasi resmi (ditandai jujur); label AI masih bersumber pihak ketiga.
