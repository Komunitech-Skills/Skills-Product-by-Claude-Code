# Uji A/B v1.0.1 vs v1.1.0 (Akun B) — Skenario Normal Pertama (Fresh Graduate Akuntansi)

Input yang sama dipakai untuk kedua versi (lihat `01-fresh-graduate-akuntansi-uji-akun-b.md`
untuk teks lengkap). v1.0.1 = `git show HEAD~3:skills/cv-lamaran-ats/SKILL.md`
(156 baris, sebelum profil induk/evaluasi kecocokan/STAR ditambahkan). v1.1.0 = versi
saat ini yang diuji (175 baris).

## v1.0.1 (tanpa profil induk, tanpa evaluasi kecocokan, tanpa STAR)
Langkah kerja v1.0.1 langsung ke: kumpulkan bahan → analisis kata kunci → skor
kecocokan kata kunci (script) → susun CV → surat lamaran. **Tidak ada** langkah
evaluasi kecocokan (skor + alasan + celah berbasis lowongan) sebelum CV disusun,
dan **tidak ada** konsep "profil pengalaman induk" yang bisa dipakai ulang di
lamaran berikutnya — riwayat pengguna ditanyakan langsung tiap sesi tanpa format
baku tersimpan.

Output v1.0.1 untuk skenario ini: langsung skor kata kunci (48,0%, 12/25 — sama,
karena scriptnya identik) lalu CV & surat lamaran. Pengguna **tidak** mendapat
jawaban eksplisit atas pertanyaan tersirat "apakah saya layak melamar posisi ini
mengingat saya cuma fresh graduate dengan magang, bukan kerja formal?" — CV
langsung dibuat tanpa penilaian kecocokan skor+alasan+celah.

## v1.1.0 (dengan profil induk + evaluasi kecocokan)
Menambahkan di depan: profil pengalaman induk terstruktur (bisa dipakai ulang di
lamaran berikutnya tanpa mengetik ulang) dan **Evaluasi Kecocokan Lowongan**
eksplisit — skor akhir 66/100 "Cocok, lamar sambil perkuat celah", dengan alasan
per dimensi dan celah konkret (Accurate/MYOB belum dikuasai, pengalaman masih
magang). Ini langsung menjawab pertanyaan "layak nggak saya lamar" yang v1.0.1
tidak jawab secara eksplisit. Skor kata kunci & CV yang dihasilkan sama persis
kualitasnya dengan v1.0.1 (fitur lama tidak berubah/regresi).

## Kesimpulan uji A/B
**v1.1.0 jelas lebih baik** untuk skenario ini — nilai tambah nyata: (1) evaluasi
kecocokan memberi keputusan berbasis data (skor+alasan+celah) sebelum pengguna
buang waktu menyiapkan lamaran untuk posisi yang mungkin kurang cocok, (2) profil
induk menghemat waktu di lamaran-lamaran berikutnya karena riwayat tidak perlu
diketik ulang. **Tidak ada regresi**: kualitas CV, skor kata kunci, surat
lamaran v1.0.1 semuanya tetap ada dan identik perilakunya di v1.1.0 (langkah
3-11 v1.1.0 = langkah 2-10 v1.0.1, hanya nomor bergeser).
Penilaian: v1.1.0 menang telak dibanding v1.0.1 pada skenario ini → **tidak**
memicu aturan "skor maks. 6" karena bukan kasus versi baru gagal menambah nilai.

## Banding Pesaing — MadsLorentzen/ai-job-search (dibaca untuk dinilai, bukan disalin)

Repo sumber inspirasi fitur v1.1.0 dinilai dari deskripsi & struktur publiknya (README
di GitHub), **tidak diimpor/disalin ke uji ini** sesuai kebijakan ATM. Ringkasan
penilaian berdampingan:

| Aspek | ai-job-search (pesaing) | cv-lamaran-ats v1.1.0 |
|---|---|---|
| Bahasa & lokalisasi | Inggris, konteks global/AS | Bahasa Indonesia penuh, konteks lokal (CPNS/BUMN, marketplace, sinonim ID/EN) |
| Evaluasi kecocokan | Ide umum "job fit scoring" tanpa rincian bobot dimensi publik yang setara | Bobot 4 dimensi eksplisit (35/30/20/15%), label skor, saringan wajib (syarat mutlak, lokasi, gaji) — lebih terstruktur & bisa diverifikasi manual |
| Auto-apply/scraping | Beberapa tool sejenis di ekosistem ini menyertakan alur scraping/otomasi platform kerja | Sengaja dibuang (lihat `ATTRIBUTION.md`) — hanya proses teks yang ditempel manual, lebih aman & sesuai kebijakan Komunitech |
| Perhitungan gaji | Tidak diverifikasi apakah ada larangan taksir gaji pasar | Eksplisit melarang menaksir gaji pasar, hanya pakai angka dari pengguna/lowongan |
| Verifikasi kata kunci | Tidak diverifikasi apakah pakai script lokal atau API eksternal | Script Python standar, lokal, tanpa koneksi jaringan (teruji di HASIL-UJI.md) |

**Penilaian:** cv-lamaran-ats v1.1.0 unggul untuk pasar Indonesia dari sisi lokalisasi,
struktur evaluasi kecocokan yang bisa diverifikasi manual, dan keamanan (tanpa
scraping/auto-apply). Tidak ditemukan kelebihan pesaing yang belum diadopsi dengan
cara sendiri oleh skill ini pada fitur-fitur yang bisa dinilai dari luar repo
(README publik) — sehingga **tidak memicu aturan skor maks. 6**.
