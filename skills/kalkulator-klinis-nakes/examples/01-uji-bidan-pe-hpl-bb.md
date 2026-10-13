# Uji 01 — Normal: bidan, skrining preeklampsia + HPL + kenaikan BB

Penguji independen (bukan pembuat), 2026-09-29. Simulasi agent: `claude-code (simulasi agent)`,
membaca hanya folder skill. Data fiktif.

> **Disinkronkan dengan skrip v1.0.6 2026-10-13:** blok "Output agent" di bawah disamakan dengan
> keluaran `scripts/klinis.py` saat ini untuk data yang sama (ambang MAP ≥ 90 mmHg, Buku KIA
> cetakan 2025, kalimat rujukan terencana, posisi kenaikan BB trimester 1). Angka tidak berubah.

## Input pengguna
> "Saya bidan di PMB. Bu S (RM 0412), G2P1A0, usia 36 th, HPHT 2 Juli 2026 siklus 28 teratur.
> TB 155 cm, BB sebelum hamil 74,5 kg (IMT sekitar 31), BB hari ini 76 kg. TD 118/78.
> Kehamilan pertama dulu preeklampsia. Tolong skrining PE, HPL, dan cek kenaikan BB-nya."

## Langkah agent
1. Langkah 0: peran sudah jelas (bidan) → lanjut.
2. Pemetaan: "kehamilan pertama dulu preeklampsia" → `riwayat-preeklampsia`; G2P1 → **bukan**
   nullipara. Usia & IMT & TD diisi lewat angka.
3. Perintah yang dijalankan:
```
python3 scripts/klinis.py preeklampsia --faktor riwayat-preeklampsia --sistolik 118 --diastolik 78 --usia-ibu 36 --imt 31
python3 scripts/klinis.py kehamilan --hpht 2026-07-02 --tanggal-periksa 2026-09-29
python3 scripts/klinis.py bb-hamil --tinggi 155 --bb-prahamil 74.5 --bb-sekarang 76 --usia-minggu 12
```

## Output agent (dengan skill)
```
🩺 Skrining faktor risiko preeklampsia — Bu S (RM 0412) — 29 September 2026
Hasil:
- MAP 91,3 mmHg (≥ 90)
- Kategori (Buku KIA cetakan 2025): RISIKO TINGGI (≥ 1 faktor tinggi)
  - Faktor tinggi: multipara dengan riwayat preeklampsia sebelumnya
  - Faktor sedang: MAP ≥ 90 mmHg; obesitas sebelum hamil (IMT > 30 kg/m²); usia ibu ≥ 35 tahun
- Belum ditanyakan: pasangan baru, jarak kehamilan > 10 th, riwayat PE pada ibu/saudari,
  diabetes, hipertensi kronik, penyakit ginjal, autoimun/SLE, APS, proteinuria.
Arti untuk tindak lanjut:
- Memenuhi kriteria ibu berisiko preeklampsia menurut Buku KIA. Buku KIA: pemeriksaan
  kehamilan, proses melahirkan, dan pemeriksaan nifas dilaksanakan di Rumah Sakit; lakukan
  rujukan terencana (tidak perlu menunggu inpartu). Pelaksanaan sesuai protokol fasilitas &
  keputusan dokter. Keputusan terapi/obat pencegahan (termasuk dosis) bukan bagian alat ini —
  ikuti PNPK/pedoman dan resep dokter.
Catatan: Aturan kategori Buku KIA (cetakan 2025): ≥ 2 faktor risiko sedang dan/atau ≥ 1 faktor
risiko tinggi → ibu berisiko preeklampsia → rujukan terencana. Buku KIA: skrining dilakukan pada
usia kehamilan < 20 minggu (saat ini 12 mg 5 hr ✔).
Sumber: Kemenkes RI, Buku KIA edisi terbaru (cetakan Ditjen Kesehatan Primer dan Komunitas 2025,
ISBN 978-623-301-149-5) — lembar skrining preeklampsia < 20 minggu; rumus MAP =
(sistolik + 2 × diastolik)/3, ambang MAP ≥ 90 mmHg dari Buku KIA (cetakan 2025).

🩺 Kalkulator kehamilan — Bu S — 29 September 2026
- HPL (Naegele): 9 April 2027 | HPL (HPHT + 280 hari): 8 April 2027
- Usia kehamilan: 12 minggu 5 hari — Trimester 1
Catatan: Naegele vs +280 hari beda 1 hari karena panjang bulan; keduanya ditampilkan.
Sumber: Aturan Naegele (HPHT + 7 hari − 3 bulan + 1 tahun); penyesuaian siklus = modifikasi
umum (siklus − 28 hari).

🩺 Kenaikan berat badan hamil — Bu S — 29 September 2026
- IMT pra-hamil 31,0 → Obesitas (≥ 30,0) (batas WHO internasional, dipakai IOM)
- Rekomendasi kenaikan total: 5–9 kg; laju trimester 2–3: 0,17–0,27 kg/minggu
- Kenaikan sejauh ini: 1,5 kg (usia 12 minggu) — posisi: di dalam asumsi IOM trimester 1
  (0,5–2,0 kg)
Catatan: IOM memakai batas IMT WHO internasional (bukan Asia-Pasifik). Usia ≤ 13 minggu: IOM
tidak memberi laju mingguan; mual/muntah bisa membuat BB turun — nilai klinis. IOM 2009 tidak
dimaksudkan untuk populasi yang jauh lebih pendek/kurus dari perempuan Amerika; untuk ibu
Indonesia pakai sebagai acuan umum, bukan target mutlak.
Sumber: IOM & NRC, Weight Gain During Pregnancy: Reexamining the Guidelines (2009).
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap
pada dokter/bidan yang memeriksa.
```

## Verifikasi independen (kode penguji, `uji-klinis/verifikasi.py` + hitung tangan)
| Item | Script | Hitung penguji | Cocok |
|---|---|---|---|
| MAP | 91,3 | (118 + 2×78)/3 = 274/3 = 91,33 | ✔ |
| IMT | 31,0 | 74,5 / 1,55² = 74,5 / 2,4025 = 31,009 | ✔ |
| HPL Naegele | 9 Apr 2027 | 2 Jul + 7 hr = 9 Jul → −3 bln +1 th = 9 Apr 2027 | ✔ |
| HPL +280 | 8 Apr 2027 | 2 Jul→31 Des = 182 hr; sisa 98 = Jan 31 + Feb 28 + Mar 31 + 8 → 8 Apr | ✔ |
| Usia kehamilan | 12 mg 5 hr | 2 Jul→29 Sep = 89 hr = 12×7 + 5 | ✔ |
| IOM obesitas | 5–9 kg; 0,17–0,27 | Tabel S-1 IOM 2009 (dikutip dari NAP) | ✔ |
| Kategori KIA | RISIKO TINGGI | ≥ 1 faktor tinggi → rujukan (lembar Buku KIA) | ✔ |

## Catatan penguji
- ✔ Tidak ada dosis aspirin/kalsium; tidak ada diagnosis; sumber + penafian ada; hanya inisial/RM.
- ⚠️ Ambang MAP: lembar Buku KIA terbitan 2025 (unduhan ayosehat.kemkes.go.id) tertulis
  **"≥ 90 mmHg"**, script memakai "> 90" (lihat HASIL-UJI, temuan T1). Pada kasus ini tidak
  mengubah hasil (MAP 91,3). → Status 2026-10-13: ditutup; skrip v1.0.6 memakai "≥ 90" dan
  Buku KIA cetakan 2025 (output di atas sudah disinkronkan).
- ⚠️ Kalimat tindak lanjut lebih lunak dari sumber: lembar KIA menulis "Lakukan rujukan
  terencana ... pemeriksaan kehamilan, proses melahirkan dan pemeriksaan nifas dilaksanakan di
  Rumah Sakit" (temuan S3). → Status 2026-10-13: ditutup; kalimat skrip v1.0.6 mengikuti bunyi
  Buku KIA (output di atas sudah disinkronkan).
- Output kenaikan BB pada usia ≤ 13 minggu tidak memberi posisi/penjelasan dari script; agent
  harus menambahkan sendiri (temuan R2). → Status 2026-10-13: ditutup; skrip v1.0.6 mencetak
  baris "Posisi" untuk usia ≤ 13 minggu.

Skor skenario: 8/10 (angka benar semua; kalimat tindak lanjut & ambang MAP perlu diselaraskan).
