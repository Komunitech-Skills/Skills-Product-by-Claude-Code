# Evaluasi Kecocokan Lowongan

Menilai seberapa cocok pengguna dengan lowongan tertentu — **skor + alasan + celah** — sebelum (atau sekaligus dengan) menyesuaikan CV. Tujuannya membantu pengguna memutuskan apakah layak melamar dan bagian mana yang perlu diperkuat di surat lamaran, bukan menjamin lolos seleksi.

Jalankan evaluasi ini berdasarkan **profil pengalaman induk** pengguna (lihat `profil-induk.md`) dan teks lowongan yang ditempel. Jangan pernah menaikkan skor dengan menganggap pengguna punya keahlian yang tidak tercatat di profilnya.

## Saringan wajib (jalankan dulu, sebelum menilai skor)

### 1. Syarat keras yang jelas gagal-total
Baca lowongan apa adanya untuk syarat yang bersifat **mutlak**, bukan preferensi — mis. jenjang pendidikan minimal, usia maksimal, domisili wajib, kepemilikan SIM/kendaraan, atau sertifikasi wajib yang disebut eksplisit "wajib"/"syarat mutlak". Jika profil pengguna jelas-jelas tidak memenuhi salah satu syarat mutlak → tandai **GAGAL SYARAT**, jangan lanjut ke skor, sebutkan syarat mana dan kutip kalimatnya. Beri tahu pengguna dia tetap boleh melamar atas risiko sendiri (kadang syarat tidak ditegakkan ketat), tapi ini bukan rekomendasi skill.

### 2. Lokasi & logistik
- Sesuai domisili/kesediaan relokasi pengguna → LULUS.
- WFH/remote atau hybrid yang cocok dengan preferensi pengguna → LULUS.
- Wajib pindah kota dan pengguna menyatakan tidak bersedia relokasi → **GAGAL** (deal-breaker), tandai jelas.
- Tidak disebutkan → catat "belum jelas, tanyakan saat wawancara/telepon HRD".

### 3. Ekspektasi gaji
**Jangan pernah menaksir kisaran gaji pasar.** Skill ini tidak mengakses data gaji real-time. Bandingkan hanya jika:
- Lowongan mencantumkan angka/rentang gaji secara eksplisit → bandingkan dengan ekspektasi gaji pengguna dari profil induk, tandai PAS/DI BAWAH/DI ATAS.
- Lowongan tidak mencantumkan gaji → catat "belum diketahui, tanyakan saat proses (HRD biasanya membahas di wawancara awal)", jangan mengarang angka.

Jika lowongan berasal dari instansi pemerintah/CPNS/BUMN, ingatkan bahwa skema gaji & tunjangan mengikuti golongan/aturan resmi instansi tersebut (Perpres/aturan internal), bukan negosiasi bebas seperti swasta — arahkan ke pengumuman resmi untuk detail, jangan menyebut angka spesifik.

## Dimensi skor (setelah lolos saringan)

Nilai tiap dimensi 0–100, lalu hitung skor akhir dengan bobot berikut:

| Dimensi | Bobot | Pertanyaan penilaian |
|---|---|---|
| Kecocokan keahlian & alat kerja | 35% | Berapa banyak hard skill/tools yang diminta lowongan sudah ada di profil induk? |
| Kecocokan pengalaman | 30% | Apakah jenis pekerjaan & tanggung jawab di pengalaman kerja pengguna sejalan dengan tugas di lowongan (nilai fungsi pekerjaannya, bukan sekadar cocok nama jabatan)? |
| Kecocokan preferensi & arah karier | 20% | Apakah tugas sehari-hari di lowongan sejalan dengan "yang bikin semangat kerja" & "tujuan karier" di profil induk? |
| Kelengkapan syarat administratif | 15% | Pendidikan minimal, sertifikasi, pengalaman minimal tahun — terpenuhi penuh/sebagian/tidak? |

**Aturan normalisasi bobot bila satu dimensi tidak bisa dinilai** (mis. lowongan sama sekali tidak menyebut syarat administratif apa pun, atau teks lowongan terlalu singkat untuk menilai preferensi/arah karier): jangan beri dimensi itu skor 0 (itu akan menghukum pengguna atas ketidakjelasan lowongan, bukan atas kekurangannya). Sebaliknya, **keluarkan dimensi itu dari perhitungan** dan **bagikan ulang bobotnya secara proporsional** ke dimensi yang tersisa (bobot baru tiap dimensi = bobot asli ÷ total bobot dimensi yang tersisa). Contoh: syarat administratif (15%) tidak bisa dinilai → tiga dimensi lain memakai bobot 35/85, 30/85, 20/85 (dibulatkan) dari total 85%. Sebutkan di catatan tabel dimensi mana yang dikeluarkan dan alasannya ("tidak disebutkan di lowongan"), supaya pengguna tahu skor akhir dihitung dari dimensi yang tersedia saja, bukan menganggap dimensi itu bernilai 0.

| Skor akhir | Label |
|---|---|
| 80–100 | Sangat cocok — layak dikejar serius |
| 60–79 | Cocok — lamar, perkuat bagian yang kurang di surat lamaran |
| 40–59 | Cukup — pertimbangkan matang, sebutkan celahnya ke pengguna |
| 0–39 | Kurang cocok — sarankan pertimbangkan ulang, kecuali pengguna punya alasan strategis (mis. ingin pindah bidang) |

## Format keluaran evaluasi

```
## Evaluasi Kecocokan: [Posisi] di [Perusahaan]

**Saringan wajib:** [LULUS semua / GAGAL SYARAT: <sebutkan> / catatan lokasi & gaji]

| Dimensi | Skor | Catatan |
|---|---|---|
| Keahlian & alat kerja | XX/100 | ... |
| Pengalaman | XX/100 | ... |
| Preferensi & arah karier | XX/100 | ... |
| Syarat administratif | XX/100 | ... |

**Skor akhir: XX/100 — [Label]**

### Kenapa cocok
- (poin dari profil induk yang selaras dengan lowongan)

### Celah yang perlu diperhatikan
- (keahlian/syarat yang belum terpenuhi — sebutkan apa adanya, jangan disamarkan)

### Rekomendasi
[Lamar sekarang / Lamar sambil perkuat celah di surat lamaran / Pertimbangkan matang / Sebaiknya cari lowongan lain] — 1–2 kalimat alasan.
```

Setelah evaluasi ditampilkan, tanyakan ke pengguna apakah mau lanjut ke penyesuaian CV & surat lamaran (lanjut ke langkah kerja utama SKILL.md), terutama bila skor di bawah 60 — beri pengguna kesempatan memutuskan sendiri.
