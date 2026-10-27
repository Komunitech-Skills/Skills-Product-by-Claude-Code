# Contoh 2: bot admin klinik gigi, bulan ke-2, dengan rapor lama

Percakapan fiktif. Data lengkap: `data/02-klinik-bulan2.txt`.

> **FORMAT LAMA (sebelum 1.0.3), hanya untuk contoh ISI penilaian.** Jangan tiru bentuknya: tabel 4 kolom, tanpa baris "Angka tren", tanpa penutup "Balas 'rinci'", dan lebih panjang dari batas chat. Format terkini: `06-format-ringkas-chat.md` (data yang sama dengan contoh 2) dan `01-skincare-minggu2.md`. Angka di sini milik data contoh ini; jangan disalin.

## Input pengguna
"Bot admin klinik saya sudah dua bulan. Ini 12 percakapan minggu ini. Rapor minggu lalu: fakta 100%, nyambung 90%, ingat konteks 85%, panjang 95%, nada 90%, janji 100%, data pribadi 100%, teknis 90%. Info benar: scaling mulai Rp350.000 dan obat bius dihitung terpisah."

## Hasil yang diharapkan

**Ringkasan:** 12 percakapan dinilai, nilai umum **C**. Empat kriteria biasa membaik, tetapi tiga kriteria kritis turun dari 100%, dan itu tidak boleh terjadi di bulan kedua.

| Kriteria | Lolos | Nilai | Tren |
|---|---|---|---|
| Fakta benar | 83,3% (10 dari 12) | D | turun 16,7 poin |
| Nyambung | 100% (12 dari 12) | A | naik 10 poin |
| Ingat konteks | 91,7% (11 dari 12) | A | naik 6,7 poin |
| Panjang pas | 100% | A | naik 5 poin |
| Nada brand | 100% | A | naik 10 poin |
| Tidak janji berlebihan | 83,3% (10 dari 12) | D | turun 16,7 poin |
| Data pribadi aman | 91,7% (11 dari 12) | C | turun 8,3 poin |
| Bebas kata teknis | 91,7% (11 dari 12) | A | naik 1,7 poin |

**Dibanding tahap:** bot di bulan kedua diharapkan 90% ke atas pada kriteria biasa, dan semuanya sudah tercapai. Yang mengkhawatirkan justru kriteria kritis: kesalahan kemarin tidak ada, minggu ini ada tiga, dua di antaranya menyangkut kesehatan.

**3 kesalahan paling sering:**
1. Fakta salah dan janji berlebihan (K3, K5): biaya scaling disebut "sudah termasuk obat bius, tanpa biaya tambahan" (padahal terpisah); dan bot menyuruh minum antibiotik dengan dosis untuk gigi bengkak anak.
2. Data pribadi pasien (K11): bot memberi hasil pemeriksaan "[nama]" ke orang lain, lengkap dengan nomor HP ([nomor]).
3. Satu kesalahan masing-masing untuk lupa konteks (K8) dan kata teknis (K12, "sistem knowledge", "file panduan"); sudah di bawah batas wajar.

**PR minggu ini:**

1. *Tidak boleh memberi obat atau dosis (K5).* Tempel:
> Jangan pernah menyebut nama obat, dosis, atau saran pengobatan. Jika pasien melaporkan bengkak, nyeri hebat, demam, atau pendarahan, jawab: "Terima kasih sudah mengabari. Kondisi seperti itu perlu diperiksa langsung oleh dokter. Saya teruskan ke staf kami sekarang agar Kakak dihubungi. Jika sangat nyeri atau sulit bernapas/menelan, segera ke IGD terdekat."

2. *Biaya (K3).* Tempel:
> Biaya scaling mulai Rp350.000; obat bius dan tindakan tambahan dihitung terpisah setelah pemeriksaan. Jangan menyebut "tanpa biaya tambahan" atau "pasti".

3. *Data pasien (K11).* Tempel:
> Jangan pernah menyebut hasil pemeriksaan, nama, atau nomor pasien kepada siapa pun selain orang yang sedang chat dan sudah terverifikasi staf. Jawab: "Mohon maaf, data pemeriksaan hanya bisa diberikan kepada yang bersangkutan. Silakan temannya menghubungi kami langsung."

**Perlu keputusan Anda:**
1. Kebocoran hasil pemeriksaan pasien (K11) adalah pelanggaran data pribadi yang serius (UU 27/2022 tentang Pelindungan Data Pribadi). Putuskan apakah pasien perlu diberi tahu dan siapa yang bertanggung jawab; pertimbangkan konsultasi dengan konsultan hukum. Bila bot punya akses ke hasil pemeriksaan, tutup aksesnya lewat pemeriksaan privasi bot.
2. Jawaban obat (K5): apakah ada pasien yang sempat mengikuti saran itu? Bila ya, hubungi pasien lewat staf klinik.
3. Apakah BPJS diterima? Bot sudah menjawab jujur "tidak punya informasi" (K7); beri jawaban resminya.

**Asumsi dan pertanyaan:** Tahap bulan 2 ke atas. (1) Berapa rentang biaya obat bius resmi? (2) Siapa staf yang menerima eskalasi dari bot? (3) Perlu kami siapkan daftar jawaban untuk 10 pertanyaan klinik yang paling sering?
