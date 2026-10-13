# Hasil Uji Independen — `presentasi-data-ke-atasan` v1.0.0

Penguji: agen terpisah dari pembuat skill, hanya membaca folder skill ini (Tahap 6
pedoman kurasi Komunitech). Tanggal: 2026-09-26.

## Ringkasan pengujian
- 5 skenario dijalankan: 3 normal (`03`, `04`, `05`), 1 input tidak lengkap (`06`),
  1 luar cakupan/etis (`07`).
- `scripts/hitung_perubahan.py` dijalankan langsung dengan data normal, nilai lama = 0,
  nilai lama negatif, format Indonesia (titik ribuan `1.250.000`, koma desimal `12,5`),
  dan data rusak (huruf, argumen kurang, tanpa argumen sama sekali). Semua hasil
  diverifikasi ulang manual dengan `Decimal` secara independen — **seluruh angka
  cocok**, tidak ada selisih pembulatan.
- Uji A/B tanpa-skill vs dengan-skill: `examples/00-pembanding-tanpa-skill.md`.
- Uji banding pesaing (`executive-summary-generator` + `visualization-builder`,
  github.com/nimrodfisher/data-analytics-skills): `examples/00-banding-pesaing.md`.
- `python3 scripts/validate.py --skill presentasi-data-ke-atasan` → **lolos**
  (`1 skill valid, 86 baris katalog sesuai.`).
- Atribusi MIT diperiksa: `ATTRIBUTION.md` menyebut sumber, URL, lisensi MIT, tanggal
  tinjau, dan daftar rinci yang diambil vs diubah/ditambahkan; `LICENSE-MIT` berisi
  teks lisensi MIT asli dengan nama pemegang hak cipta asli (Nimrod Fisher) — **sesuai
  aturan lisensi MIT pedoman kurasi Komunitech tahap 2** (atribusi + teks lisensi asli disertakan).
- Tidak ditemukan pola unduh-pipe-ke-shell, instruksi tersembunyi/prompt injection, atau
  permintaan kredensial di SKILL.md maupun script — konsisten dengan catatan audit di
  `ATTRIBUTION.md`.
- Tidak menjalankan `scripts/uji_openclaw.sh` (di luar cakupan tugas ini).

## Temuan perhitungan (script) — semua terverifikasi benar
| Kasus | Hasil script | Verifikasi manual |
|---|---|---|
| Normal (Omzet 32jt→24,5jt) | -23,4% | -23,4375 → -23,4 (HALF_UP) ✓ |
| Normal (Biaya iklan 4jt→5,6jt) | +40,0% | 40,0 ✓ |
| Nilai lama = 0 | `persen_perubahan: null` + catatan | Benar, tidak dipaksakan jadi angka ✓ |
| Nilai lama negatif (-5jt→2jt) | selisih +7jt, **arah "naik"**, persen **-140,0%** | Matematis benar (7.000.000/-5.000.000×100), tapi **arah dan tanda persen tampak kontradiktif** secara visual (naik tapi -140%) — lihat Temuan #1 |
| Format Indonesia (`1.250.000`, `12,5`) | Ditolak dengan pesan error jelas | Sesuai desain (script minta angka polos, agent yang membersihkan dulu — didokumentasikan di SKILL.md langkah 2 & docstring script) ✓ bukan bug |
| Huruf (`abc`) | Ditolak, pesan jelas | ✓ |
| Argumen kurang (`Label:angka` saja) | Ditolak, pesan jelas | ✓ |
| Tanpa argumen | Error jelas, exit 1 | ✓ |
| `--daftar` normal & rata-rata | Total/rata-rata/min/max benar | 145.000.000÷3=48.333.333 (HALF_UP) ✓ |

## Temuan
1. **(Minor, tidak menghalangi rilis) Nilai lama negatif menghasilkan `arah` dan tanda
   `persen_perubahan` yang tampak bertentangan.** Contoh: laba dari -Rp5.000.000 ke
   Rp2.000.000 → `arah: "naik"` (benar, berdasarkan selisih) tapi
   `persen_perubahan: -140.0` (matematis benar untuk basis negatif, tapi membingungkan
   dibaca sekilas). Kasus ini jarang terjadi untuk omzet/biaya (biasanya selalu positif)
   tapi bisa muncul untuk laba/rugi. **Saran perbaikan (untuk revisi berikutnya, bukan
   blocker):** tambahkan catatan otomatis di script saat `nilai_lama < 0`, mis.
   `"catatan": "nilai lama negatif, persen perubahan tidak intuitif — sampaikan arah
   dan Rupiah saja tanpa persen"`, dan SKILL.md menyebutkan agent sebaiknya tidak
   menampilkan persen mentah untuk kasus basis negatif ke pengguna awam.
2. **(Sangat minor, kosmetik)** Nama fungsi internal `rupiah()` dipakai untuk membulatkan
   semua nilai bilangan bulat (termasuk ROAS yang bukan Rupiah di Uji 04) — tidak
   memengaruhi kebenaran hasil, hanya penamaan kurang generik. Tidak perlu revisi
   sebelum rilis.
3. **(Saran penguatan, bukan cacat)** SKILL.md Batasan belum punya baris eksplisit untuk
   kasus "pengguna minta angka/arah data diubah dari yang sebenarnya" (Uji 07). Perilaku
   yang benar berhasil disimulasikan dari penalaran umum + larangan mengarang yang sudah
   ada, tapi baris eksplisit akan membuat perilaku ini lebih terjamin konsisten di
   berbagai model/agent. Lihat detail saran di `examples/07-...md`.
4. Semua 4 format output (WA 5 baris, email, 1 halaman eksekutif, skrip bicara) di
   ketiga skenario normal konsisten memakai **angka yang identik**, format Rupiah
   (`Rp45.000.000`) dan persen (`15,6%`) sesuai `references/gaya-komunikasi.md` di semua
   kanal — tidak ada penyimpangan format antar skenario.
5. Skill dengan benar **menolak mengarang risiko** ketika data tren positif tanpa sinyal
   negatif (Uji 03) dan **menolak menghitung margin yang tidak diminta/tidak ada
   datanya** (Uji 05) — bukti kepatuhan konsisten pada larangan mengarang, diuji di dua
   skenario berbeda.
6. Disclaimer keuangan (Batasan SKILL.md) muncul dengan benar pada skenario bank/KUR
   (Uji 05), sesuai domain sensitif Tahap 4 poin 5 pedoman kurasi Komunitech.

## Skor kualitas: 9/10

**Alasan:**
- Tidak ada perhitungan yang dikarang; seluruh angka di 5 skenario dan pengujian script
  terverifikasi independen dan cocok 100%.
- Format & pembulatan konsisten sesuai standar pedoman kurasi Komunitech tahap 4 dan
  `references/gaya-komunikasi.md` di semua kanal dan skenario.
- Uji A/B menunjukkan skill unggul telak dibanding respons tanpa skill (kesimpulan di
  depan, angka presisi, rekomendasi PIC/tenggat, 4 format sekaligus) — tidak memenuhi
  syarat skor maks. 6.
- Uji banding pesaing menunjukkan skill unggul dibanding sumber adaptasi (lokalisasi
  penuh, 4 format kanal, script perhitungan) — tidak memenuhi syarat skor maks. 6.
- Atribusi MIT lengkap dan benar.
- **-1 poin** untuk dua temuan minor di atas (kejelasan kasus basis negatif pada script;
  baris eksplisit anti-poles-angka di SKILL.md) — keduanya perbaikan kecil yang tidak
  mengubah kebenaran hasil atau keamanan, sehingga tidak menahan rilis (ambang revisi
  wajib adalah skor < 7), tapi layak masuk revisi minor berikutnya.

## Rekomendasi tindak lanjut
1. Revisi minor `scripts/hitung_perubahan.py`: tambahkan catatan otomatis untuk
   `nilai_lama < 0` (Temuan #1).
2. Tambahkan satu baris eksplisit di Batasan SKILL.md untuk menolak permintaan
   memalsukan arah data/mengarang target (Temuan #3).
3. Lanjutkan ke uji muat OpenClaw (`scripts/uji_openclaw.sh`) dan uji platform asli
   sesuai Tahap 6 poin 8–10 pedoman kurasi Komunitech sebelum status naik dari `draft`/`uji` ke `lulus`.
