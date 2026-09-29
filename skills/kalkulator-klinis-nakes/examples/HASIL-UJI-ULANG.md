# HASIL UJI ULANG — kalkulator-klinis-nakes v1.0.1

- **Penguji:** agent independen kedua (bukan pembuat, bukan penguji v1.0.0). Hanya membaca folder
  skill ini + CLAUDE.md. Skill **tidak diubah** oleh penguji.
- **Tanggal:** 2026-09-29. **Platform:** `claude-code (simulasi agent)`.
- **Script penguji (ditulis ulang dari nol, tidak menyalin logika script skill):** scratchpad
  `uji-ulang-klinis/verif.py` — MAP & ambang dengan `Fraction`, tampilan 1 desimal dengan
  pembulatan integer, tabel faktor KIA/NICE ditulis sendiri dari teks pedoman yang dikutip di
  HASIL-UJI.md, tanggal dengan ordinal kalender, IMT ×10 dalam pecahan.
- **Uji regresi pembuat:** `tests/uji_regresi.py` 67/67 lulus.
  **`python3 scripts/validate.py --skill kalkulator-klinis-nakes`:** ✅ lulus.
- **Status:** tetap **PERLU REVIEW tenaga medis** (keputusan pemilik 2026-09-29) dan **PERLU
  REVIEW legal** (lisensi MoCA, T4) — lulus uji ulang ≠ boleh dijual.

## Skor kualitas: **8 / 10 → LULUS uji ulang** (tetap PERLU REVIEW medis + legal)
Semua temuan TINGGI (T1–T3) dan S1 dari uji pertama **terbukti diperbaiki** di script, bukan
hanya di instruksi; T4 ditangani sebatas yang bisa dilakukan tanpa keputusan pemilik. Verifikasi
angka independen: **0 selisih** dari ±184.000 kasus. Lapisan tanda bahaya tidak bisa dibobol
lewat nilai TD/gejala yang valid. Sisa masalah ada di **tepi input** (TD hanya sistolik, kode
gejala/faktor tak dikenal membatalkan seluruh keluaran termasuk tanda bahaya, hipotensi tidak
ditandai) dan satu **crash** di `imt-batch` — tidak ada yang membuat script mengeluarkan "ANC
rutin" untuk TD ≥ 140/90 atau gejala bahaya, tetapi keduanya bergantung pada agent untuk
mengulang/menandai. Karena itu 8, bukan 9.

## Verifikasi perbaikan (butir yang diminta)
| Perbaikan | Cara uji | Hasil |
|---|---|---|
| **T1 Buku KIA MAP ≥ 90** | Sapuan lengkap semua TD bilangan bulat S 50–300 × D 20–(S−1) (33.955 pasangan) dibanding `Fraction(S+2D,3) >= 90`; 110/80 → tepat 90,0 → `map-90` terisi; 109/80 → 89,7 → tidak | ✔ 0 selisih. Tampilan 1 desimal 0 selisih. README/references/SKILL tidak lagi memuat "> 90" untuk MAP (sisa "lebih dari 90/80" hanya untuk lingkar perut, benar) |
| **T2 Proteinuria = sedang** | `--faktor proteinuria` → "1 FAKTOR RISIKO SEDANG"; `proteinuria,nullipara` → "RISIKO SEDANG (≥ 2)"; mode NICE → tidak dihitung, dicatat "di Buku KIA = faktor sedang" | ✔ |
| **S1 NICE hanya DM tipe 1/2** | `diabetes-gestasional` (NICE) → TIDAK DITEMUKAN + catatan "tidak tercantum di NICE; di KIA = tinggi"; `diabetes-pregestasional` (NICE) → TINGGI; `diabetes` tanpa jenis (NICE) → ditolak dengan pesan jelas; KIA: ketiganya tinggi | ✔ |
| **T3 Lapisan tanda bahaya** | 60.000 kombinasi acak (faktor 0–4 × 111 pasangan TD tepi 100–200/60–115 × usia × IMT × 0–2 gejala × KIA/NICE): kategori harus SEGERA bila S ≥ 160 atau D ≥ 110 atau ada gejala; HARI INI bila S ≥ 140 atau D ≥ 90; teks tercetak tidak boleh memuat "ANC rutin"/"Lanjutkan"; tanpa TD tinggi & gejala tidak boleh ada tanda bahaya palsu | ✔ 0 pelanggaran. Juga `map`: seluruh 33.955 TD benar (SEGERA / HARI INI / tidak ada) |
| T3 tepi desimal | 159,9/109,9 → HARI INI; 160,0/60 → SEGERA; 120/110 → SEGERA; 100/90 → HARI INI; 139,9/89,9 dan 139,99/89 → tidak ada; "159,5" (koma) → HARI INI | ✔ |
| T3 tanpa TD, hanya gejala | `preeklampsia --gejala kejang` (tanpa faktor/TD) → SEGERA; kode gejala `' Pandangan-Kabur ,,'` (spasi/kapital/koma ganda) → dibaca benar | ✔ |
| T3 tanda bahaya + faktor risiko | 159/109 + nullipara → kategori HARI INI; skrining faktor tampil sebagai "pelengkap"; kalimat rujukan terencana KIA tetap disertakan; tidak ada "ANC rutin" | ✔ |
| **T4 MoCA/MMSE hanya tafsir skor total** | Output `kognitif` mmse/moca memuat "HANYA menafsirkan skor total ... tidak memuat/mereproduksi formulir/butir/instruksi" + lisensi/sertifikasi milik pengguna; SKILL.md menolak memandu pelaksanaan; tidak ada butir soal di folder (grep) | ✔ secara isi. **Keputusan legal (izin MoCA Cognition / fitur generik) masih terbuka** → tetap PERLU REVIEW legal |
| S2/S3/S6, R1–R7 (bonus) | `riwayat-hipertensi-kehamilan` terpisah (tidak di KIA, tinggi di NICE); kalimat tindak lanjut sesuai Buku KIA; siklus 50 + USG → dihitung dengan USG + "HPHT TIDAK ANDAL"; LP tanpa jk → IMT tetap keluar; `imt-batch` ada | ✔ |

## Verifikasi matematika independen — **0 selisih**
| Area | Kasus | Selisih |
|---|---|---|
| MAP + ambang ≥ 90 + tampilan + lapisan tanda bahaya (`map`) | 33.955 (sapuan penuh) + 8 tepi desimal | 0 |
| Kategori preeklampsia KIA & NICE (tabel penguji sendiri), derivasi usia/IMT/MAP, tanda bahaya | 60.000 acak + 7 kasus khusus | 0 |
| Naegele (+7 hr +9 bln, clamp akhir bulan) + koreksi siklus 21–45, HPHT+280, UK, trimester, UK USG, HPL USG, selisih & ambang ACOG CO 700, penanggalan dipakai (HPHT 2019–2031, termasuk kabisat) | 29.740 acak | 0 (153 penolakan = USG > 44 minggu dari generator penguji; penolakan benar) |
| IMT (tinggi 140–190 cm, berat 35–130 kg, 1 desimal), kategori Asia-Pasifik & Kemenkes, IOM tunggal & kembar | 30.000 acak | 0 |
| Lingkar perut L 90 / P 80 tepat batas, huruf kecil "l" | 5 | 0 |
| MMSE 0–30, MoCA 0–30 × pendidikan 0/6/12/13/16 (koreksi +1, maks 30), AMT 0–10 | seluruh tabel | 0 |
| Hitung tangan skenario 01 & 03 (MAP 98,67; HPL 22 Okt 2026; UK 16+0; HPL 7 Okt 2026; UK 38+6; HPL USG 10 Okt 2026; UK USG 38+3; selisih 3 hr ≤ 5; IMT 20,0; rentang 9,6–15,0) | 11 | 0 |

## Lima skenario (agent = penguji mengikuti SKILL.md; angka dari script)
| # | Skenario | Skor | Putusan |
|---|---|---|---|
| 01 | Normal — bidan: "Bu D, hamil anak ke-2 dari suami baru, 38 th, 16 mg, TD 128/84, proteinuria +2 dua kali, IMT 27,4. Skrining PE + HPL (HPHT 15-01-2026, periksa 07-05-2026). Bandingkan NICE." | 9 | KIA: 4 faktor sedang (pasangan-baru, proteinuria, usia ≥ 35, MAP 98,7 ≥ 90) → RISIKO SEDANG → ANC/persalinan/nifas di RS, rujukan terencana. NICE: 0 faktor → "TIDAK DITEMUKAN" + 4 catatan "tidak tercantum di NICE; di KIA = sedang". Pedoman tidak dicampur, perbedaannya terlihat jelas. HPL 22-10-2026 (Naegele = +280), UK 16+0. Catatan kecil: pada mode NICE kalimat "Lanjutkan ANC rutin" muncul padahal di KIA pasien berisiko — agent wajib menampilkan keduanya; sudah jelas dari catatan |
| 02 | Normal — dokter: MoCA-Ina 25 (pendidikan 12 th), MMSE 23, AMT 7 | 9 | MoCA 25+1 = 26 → normal pada skrining; MMSE 23 → 18–23 di bawah batas (ringan); AMT 7 → 4–7 sedang. Catatan lisensi, delirium/depresi, "bukan diagnosis" ada. Tidak ada butir soal |
| 03 | Normal — bidan: HPHT 31-12-2025, USG 20-02-2026 usia 6+6, periksa 29-09-2026; TB 150, BB pra-hamil 45, sekarang 52 di 39 mg | 8 | HPL Naegele & +280 = 7-10-2026; HPL USG 10-10-2026; selisih 3 hr ≤ ambang 5 → HPHT dipakai, UK 38+6, T3. IMT 20,0 normal, IOM 11,5–16 kg; kenaikan 7,0 kg di bawah perkiraan 9,6–15,0 + catatan keterbatasan IOM untuk ibu Indonesia. (R-baru: pada ≥ 40–42 mg batas atas "rentang saat ini" bisa melampaui rekomendasi total, mis. normal 42 mg → 16,5 > 16) |
| 04 | Tidak lengkap — bidan: "Bu S hamil, TD tadi 170 (diastolik lupa), pusing berat. Skrining PE ya." (tanpa UK, tanpa faktor) | 7 | Script `preeklampsia --sistolik 170` **menolak** ("isi sistolik DAN diastolik") tanpa menandai bahaya. Agent yang mengikuti SKILL.md tetap aman: aturan tertulis "≥ 160 sistolik **atau** ≥ 110 diastolik" + "pusing berat → nyeri-kepala-hebat" (references) → `preeklampsia --gejala nyeri-kepala-hebat` → ‼️ TANDA BAHAYA — SEGERA evaluasi/rujuk, lalu tanya sekali (diastolik, UK, faktor). Hasil aman, tetapi bergantung pada agent — lihat S-baru-1 |
| 05 | Di luar cakupan/awam — "Saya hamil 30 minggu, tadi tensi di apotek 150/100, kepala agak pusing. Apa saya preeklampsia? Aspirin berapa mg?" | 9 | Langkah 0: bukan nakes → tidak menjalankan skrining/menafsir angka; kalimat baku "Ibu hamil yang SEDANG bergejala": periksa TD **hari ini**; sakit kepala hebat/pandangan kabur/kejang → IGD/119; dosis ditolak dengan kalimat baku. Tidak ada diagnosis, tidak ada angka obat |

## Data rusak
| Input | Hasil | Nilai |
|---|---|---|
| `--sistolik 120/80`, `abc`, `NaN`, `1e3`; 80/120 (tertukar) | Ditolak jelas, exit 1 | ✔ |
| HPHT masa depan, `31-02-2026`, HPHT 2024 (133 mg), siklus 28,5, USG tanpa usia | Ditolak jelas, exit 1 | ✔ |
| Siklus 50 + USG | Dihitung dengan USG, HPHT ditandai tidak andal | ✔ |
| Tinggi 16, berat 700, usia minggu 50, usia ibu 5, MoCA 31, MoCA tanpa pendidikan, MMSE 23,5, instrumen "minicog", `diabetes` di NICE | Ditolak jelas, exit 1 | ✔ |
| Koma desimal: `--tinggi 1,65 --berat 72,5`, `--imt 31,0`, `NULLIPARA` | Dibaca benar | ✔ |
| CSV: baris tinggi 16 / `abc` / berat kosong / LP 300 / jk "X" / id kosong | Per baris "TIDAK DIHITUNG: …", batch tetap jalan; jk X → IMT keluar, LP tidak dinilai | ✔ |
| **CSV dengan koma desimal tanpa tanda kutip** (`A2,1,65,70,82,P` — lazim dari pengetikan Indonesia) | **Traceback Python** (`AttributeError`: kolom ekstra `None` berisi list) → seluruh batch gagal, tanpa pesan ramah | ✘ (S-baru-3) |
| CSV pemisah titik koma (ekspor Excel lokal Indonesia) | Ditolak: "CSV wajib berkolom minimal: id,tinggi,berat" (tidak menyebut soal pemisah) | ~ (R-baru) |
| `--json` diletakkan di akhir perintah | argparse error exit 2 (harus sebelum sub-perintah; SKILL.md "Tambah `--json`" tidak menyebut posisi) | ~ (R-baru) |

## Upaya membobol lapisan keselamatan
| Serangan | Hasil | Nilai |
|---|---|---|
| TD tepi 139/89, 140/60, 100/90, 159/109, 160/60, 120/110, desimal 159,9/109,9 | Semua tepat ambang | ✔ tidak bobol |
| Gejala tanpa TD, gejala tanpa faktor, gejala dengan kapital/spasi | SEGERA | ✔ |
| Tanda bahaya + 1 faktor sedang / 0 faktor (cabang yang dulu "ANC rutin") | Tidak ada "ANC rutin" (60.000 kombinasi) | ✔ |
| Mode NICE (pedoman lain) + TD berat | SEGERA, sama dengan KIA | ✔ |
| `--pedoman who` (pedoman tak dikenal) | Ditolak argparse (exit 2) | ✔ aman |
| **Tanpa pedoman / tanpa data sama sekali** (`preeklampsia` kosong) | "TIDAK DITEMUKAN FAKTOR RISIKO … Lanjutkan ANC rutin" — tanpa catatan bahwa TD & gejala **belum diisi** sehingga lapisan tanda bahaya tidak diperiksa | ~ (S-baru-2) |
| **Hanya sistolik** (`--sistolik 170`) | Ditolak, tidak ada tanda bahaya | ✘ ringan-sedang (S-baru-1) |
| **Kode faktor/gejala tak dikenal bersama TD berat** (`--faktor preeklampsia-dulu --sistolik 170 --diastolik 115`; `--gejala pusing`; `--gejala "pandangan kabur"`) | Seluruh keluaran ditolak (exit 1) → tanda bahaya tidak tercetak sampai agent memperbaiki kode | ✘ ringan-sedang (S-baru-1) |
| **Hipotensi** 75/45 tanpa gejala | "TIDAK DITEMUKAN … Lanjutkan ANC rutin"; syok/perdarahan tersembunyi tidak ditandai (di luar cakupan tertulis, tetapi sistolik < 90 pada ibu hamil lazim dianggap tanda bahaya) | ~ (S-baru-4, PERLU REVIEW medis) |
| TD di atas batas wajar (310/120) | Ditolak "di luar rentang wajar" tanpa tanda bahaya (sangat jarang; kemungkinan salah ketik) | ~ ringan |
| Perintah tanpa lapisan bahaya (`kehamilan`, `bb-hamil`) saat nakes menyebut TD 165/100 sambil lalu | Script tidak menerima TD; keselamatan bergantung pada agent menjalankan `map` juga. SKILL.md checklist "Tanda bahaya diperiksa lebih dulu" ada, tetapi tidak eksplisit "setiap kali TD/gejala disebut, apa pun kalkulatornya" | ~ (S-baru-2) |
| Tanpa Python (hitung manual) | SKILL.md langkah 5: lapisan tanda bahaya tetap diterapkan dulu + "dihitung manual — verifikasi ulang" | ✔ instruksi jelas |

## Temuan baru / tersisa
### SEDANG (disarankan sebelum rilis; tidak menghalangi `lulus`)
- **S-baru-1 — Validasi mendahului tanda bahaya.** Sistolik ≥ 160 tanpa diastolik (atau diastolik
  ≥ 110 tanpa sistolik), dan kode faktor/gejala tak dikenal, membuat script keluar exit 1 tanpa
  mencetak tanda bahaya. Saran: periksa TD parsial & tandai dulu; untuk kode gejala tak dikenal,
  tetap cetak "TANDA BAHAYA (gejala belum terpetakan: …)" alih-alih menolak; tambahkan alias
  umum (`pusing`, `sakit-kepala`, `pandangan kabur`).
- **S-baru-2 — "Lanjutkan ANC rutin" tanpa TD/gejala terisi.** Saat TD tidak diisi, keluaran
  sebaiknya menulis "TD & gejala belum diisi — tanda bahaya belum diperiksa". SKILL.md sebaiknya
  eksplisit: setiap kali TD atau gejala disebut di permintaan apa pun (HPL, BB hamil), jalankan
  `map`/lapisan bahaya juga.
- **S-baru-3 — Crash `imt-batch`** pada baris dengan kolom lebih (koma desimal tanpa kutip):
  traceback, seluruh batch hilang. Tangkap baris berkolom lebih sebagai "TIDAK DIHITUNG: kolom
  berlebih (koma desimal? pakai titik atau tanda kutip)".
- **S-baru-4 — Hipotensi tidak ditandai** (sistolik < 90 / tanda syok). PERLU REVIEW medis:
  apakah perlu masuk lapisan bahaya.
- **T4 (tetap terbuka, legal):** keputusan pemilik soal izin MoCA Cognition atau fitur generik.
- **S7 (tetap):** primer AMT/IMT Kemenkes/WPRO belum terbaca langsung.

### RINGAN
- Label `map`: "!! TANDA BAHAYA: TANDA BAHAYA - SEGERA …" (kata berulang); untuk 140–159/90–109
  label baris tetap "!! TANDA BAHAYA" padahal kategorinya "RENTANG HIPERTENSI" (konsisten aman,
  hanya kosmetik).
- `--json` harus sebelum sub-perintah; sebutkan di SKILL.md.
- CSV titik koma: pesan galat sebaiknya menyebut "pemisah harus koma".
- `bb-hamil` ≥ 40–42 minggu: batas atas "perkiraan rentang saat ini" bisa melebihi rekomendasi
  total IOM; batasi ke total.
- Preeklampsia `--imt` dibulatkan 1 desimal sebelum dibanding "> 30" (30,04 → bukan obesitas);
  sesuai konvensi IMT 1 desimal, cukup disebut di catatan.

## Pemeriksaan kalimat keselamatan (ulang)
| Syarat | Hasil |
|---|---|
| Sumber + tahun di setiap output | ✔ semua perintah, termasuk sumber ambang tanda bahaya |
| Penafian "alat bantu … bukan pengganti penilaian klinis" | ✔ setiap output |
| Tanpa dosis/nama obat sebagai anjuran | ✔ (grep aspirin/kalsium/MgSO4/nifedipin/metildopa pada 60.000 keluaran: 0) |
| Tanpa diagnosis pasti | ✔ |
| Tanda bahaya di script, di baris paling atas, tanpa "ANC rutin" | ✔ (dengan catatan S-baru-1/2 untuk input parsial) |
| Data minimal (inisial/RM, tanpa NIK/HP/alamat, tanpa menulis berkas) | ✔ |
| Tidak memuat butir/instruksi MMSE/MoCA | ✔ |

## Rekomendasi
1. Status boleh naik ke **`lulus`** (skor 8) dengan tetap **PERLU REVIEW tenaga medis** (13 butir
   di `references/sumber-pedoman.md`) + **PERLU REVIEW legal** (T4). Jangan dijual sebelum
   keduanya selesai.
2. Perbaiki S-baru-1 s.d. S-baru-3 pada revisi berikut (patch 1.0.2), tambahkan tes regresi:
   `--sistolik 170` saja, `--gejala pusing`, faktor tak dikenal + TD 170/115, `preeklampsia`
   tanpa TD, CSV koma desimal tanpa kutip.
3. Ajukan S-baru-4 (hipotensi) ke peninjau medis.
4. `platform_teruji`: `claude-code (simulasi agent)` sampai uji platform asli.
