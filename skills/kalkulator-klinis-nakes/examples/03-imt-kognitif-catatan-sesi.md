# 03 — IMT dewasa + lingkar perut, skor MoCA-Ina, catatan sesi stimulasi kognitif

> Contoh dari pembuat skill (data fiktif). Belum uji independen.

**Input:** "Saya perawat di klinik lansia. Ibu S (ID L-07): TB 158, BB 61, lingkar perut 84.
MoCA-Ina oleh dokter tadi skor 22, sekolah sampai SD (6 tahun). Buatkan juga catatan sesi
stimulasi kognitif hari ini: orientasi — sebut hari benar, tanggal salah; ingat 5 benda — 3 benar;
bercerita foto keluarga lancar; ikut aktif."

**Perintah:**
```
python3 scripts/klinis.py imt --tinggi 158 --berat 61 --lingkar-perut 84 --jk P
python3 scripts/klinis.py kognitif --instrumen moca --skor 22 --pendidikan-tahun 6
```
**Output script:**
```
Tinggi (cm): 158.0
Berat (kg): 61
IMT (kg/m2): 24.4
Kategori Asia-Pasifik: Berat badan lebih / berisiko (23,0-24,9)
Kategori Kemenkes: Normal (18,5-25,0)
Lingkar perut (cm): 84
Lingkar perut: >= 80 cm -> obesitas sentral (batas Asia-Pasifik)
Catatan: IMT dibulatkan 1 desimal (setengah ke atas) lalu dikategorikan. Hanya untuk dewasa >= 18 tahun, tidak untuk ibu hamil/anak.
Sumber: WHO WPRO/IASO/IOTF, The Asia-Pacific Perspective: Redefining Obesity and its Treatment (2000)
Sumber: Kemenkes RI, Pedoman Gizi Seimbang (Permenkes No. 41 Tahun 2014) - batas ambang IMT Indonesia
PENTING: Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap pada dokter/bidan yang memeriksa.

Instrumen: MoCA / MoCA-Ina
Skor mentah: 22
Koreksi pendidikan: 1
Skor akhir: 23
Interpretasi: di bawah batas skrining 26 - pertimbangkan evaluasi lanjut
Catatan: MoCA mewajibkan pelatihan & sertifikasi pemeriksa (sejak 2019). Skill ini hanya menafsirkan skor total yang Anda masukkan.
Catatan: Batas 26 adalah versi asli; studi validasi MoCA-Ina 2010 belum menetapkan batas khusus Indonesia.
Catatan: Hasil skrining bukan diagnosis demensia/gangguan kognitif.
Sumber: Nasreddine dkk. 2005 (J Am Geriatr Soc 53:695-699): >= 26 normal, +1 poin bila pendidikan <= 12 tahun; MoCA-Ina: Husein dkk. 2010 (Neurona 27(4)) - batas khusus Indonesia belum ditetapkan dalam studi validasi itu
PENTING: Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap pada dokter/bidan yang memeriksa.
```
Verifikasi manual: 61 / 1,58² = 61 / 2,4964 = 24,43 → 24,4 → Asia-Pasifik "BB lebih/berisiko",
Kemenkes "Normal"; LP 84 ≥ 80 (P) → obesitas sentral ✓. MoCA 22 + 1 (≤ 12 th) = 23 < 26 ✓.

**Catatan sesi (dari `templates/catatan-sesi-stimulasi-kognitif.md`, ringkas):**
```
Catatan Sesi Stimulasi Kognitif — ID L-07 — 29-09-2026
| Aktivitas (domain) | Hasil yang terlihat | Bantuan |
| Orientasi realitas (orientasi) | Menyebut hari benar, tanggal belum tepat | Petunjuk kalender |
| Mengingat 5 benda (memori) | 3 dari 5 | Tanpa bantuan |
| Reminiscence foto keluarga (bahasa) | Bercerita lancar | - |
Partisipasi: aktif.
Skor instrumen: MoCA-Ina 22 (skor akhir 23 setelah koreksi pendidikan) — di bawah batas skrining
26, pertimbangkan evaluasi lanjut (Nasreddine 2005; Husein dkk. 2010).
⚠️ Dokumentasi aktivitas, bukan diagnosis.
```
