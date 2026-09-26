# Catatan pembuat — laporan-iklan-mingguan v1.0.1 (revisi cacat uji, 2026-09-26)

- **Peran:** pembuat/perevisi skill, **bukan** penguji independen. Menindaklanjuti `examples/HASIL-UJI.md`
  (uji independen v1.0.0, skor 5/10, TIDAK LULUS). `HASIL-UJI.md` **tidak diubah**.
- **Lingkungan:** Linux, Python 3.11. Data reproduksi dibuat di scratchpad (bukan repo) dengan bentuk ekspor
  yang sama dengan skenario penguji: Meta 6 iklan dengan sel `Results` kosong, Google Ads mentah (2 baris judul,
  `Campaign status`, `Avg. cost`, 3 baris `Total: …`, `Currency code`), TikTok dengan kolom `Currency`, Shopee
  28→12 kolom dengan format `Rp1.234.567` dan baris Total di berbagai posisi. Semua data fiktif.
- **Status tetap `uji`.** Revisi ini wajib diuji ulang oleh penguji independen sebelum naik status.

## Tes
- `python3 tests/uji_regresi.py`: **49 tes OK** (19 lama + 30 baru). Satu tes lama diubah karena perilakunya
  sengaja diubah (S1: gabung dua jenis hasil berbeda kini **tidak** menjumlah hasil).
- Tes baru dijalankan terhadap salinan `laporan_iklan.py` v1.0.0 di scratchpad: **28 dari 30 gagal** (plus tes
  gabung lama yang diubah). Dua yang lulus di v1.0.0 adalah tes penjaga yang memang harus tetap lulus:
  nama kampanye "Total Look Hijab" tidak boleh dianggap baris total, dan file Rupiah dengan kolom `Currency`=IDR
  tetap jalan.
- Verifikasi acak terhadap acuan `fractions.Fraction` (tanpa kode skill): 60.000 kasus persen perubahan
  (sepertiganya kasus tepi x,x5%) + 60.000 kasus pembagian rupiah → **0 beda**.
- `python3 scripts/validate.py`: tidak ada masalah untuk skill ini. Satu masalah di luar skill ini
  (`buku-piutang` belum ada di `catalog.csv`, milik agent lain yang sedang berjalan).
- `bash scripts/uji_openclaw.sh` **tidak** dijalankan ulang di revisi ini (frontmatter tidak berubah).

## Reproduksi sebelum → sesudah
| ID | Kasus | v1.0.0 | v1.0.1 |
|---|---|---|---|
| T1 | Skenario 01 Meta apa adanya (`Results` kosong) | Rp 3.945.280, "turun 0,6%", biaya/hasil "turun 6,9%", iklan 0 chat hilang | **Rp 4.302.180, naik 8,4%, Rp 30.297 naik 1,5%**; Retargeting di PERLU PERHATIAN no. 1 & saran no. 1; catatan menyebut nama iklan & Rp 356.900 |
| T1 | `k.csv` (sel Conversions kosong) | Rp 500.000 | **Rp 620.000** |
| T2 | Shopee "Total" di kolom `Urutan`, nama kosong | Rp 4.937.271 (2×), "Kampanye #6" di TERBAIK | **Rp 2.468.636**, 1 baris total dilewati |
| T2 | Label `Total:`, `Total (5 iklan)`, `Total: Account`, `Jumlah Total` | 2× tanpa peringatan | semua **Rp 2.468.636** |
| T2 | Baris total tanpa label apa pun | (tidak diuji penguji) | dikenali karena angkanya = jumlah baris lain, dengan ⚠️ |
| T3 | Google mentah (baris judul) | error "Kolom yang ada: ['Campaign report']" | **Rp 3.326.715, ROAS 4,2x**, periode 2026-09-14 s.d. 2026-09-20 dari baris judul |
| T3 | Google tanpa baris judul (3b) | nama=`Campaign status`, biaya=`Avg. cost` → Rp 5.098, ROAS 8296,5x | nama=`Campaign`, biaya=`Cost` → **Rp 3.326.715** |
| T4 | TikTok `Currency`=USD | "Rp 300" | **ditolak** (kode 2), pesan menyebut kolom `Currency` = USD |
| T4 | Sel `"$1,234.56"` | "Rp 1.235" | **ditolak**, pesan menyebut simbol di sel |
| T4 | `Currency` campur USD & IDR | (tidak diuji) | ditolak: "mencampur lebih dari satu mata uang" |
| S4 | `--omzet "20 juta"` / `"20jt"` | Rp 20 → 24521000,0% | **Rp 20.000.000 → 24,5%**; `"20M"` & `"dua puluh juta"` ditolak dengan contoh format |
| R2 | 103.000 vs 80.000 | naik 28,7% | **naik 28,8%** |

## Temuan & keputusan
| ID | Keparahan | Status v1.0.1 | Perubahan |
|---|---|---|---|
| T1 | Tinggi | **Diperbaiki** | `baca_sel()` membedakan *kosong* (`""`, `-`, `--`, `—`, `n/a`) dan *rusak*. Metrik kosong = 0 dan dicatat (nama iklan + biayanya). Baris hanya dibuang bila **biaya** tidak terbaca, dan ⚠️ menyebut nama iklan + isi selnya. Metrik lain yang rusak = 0 dengan ⚠️. |
| T2 | Tinggi | **Diperbaiki** | Pola total (`total`, `jumlah`, `grand total`, `subtotal`, `summary`, `ringkasan`, `keseluruhan`, `semua kampanye`, `all campaigns`, boleh diikuti `:`/`(`/`-`/angka/kata total lain) dicek di **setiap kolom teks**. Cadangan: baris yang biaya, tayangan, dan kliknya persis = jumlah semua baris lain (min. 2 baris lain berbiaya) dianggap total dengan ⚠️. |
| T3 | Tinggi | **Diperbaiki** | Pencocokan kolom per kata utuh, berprioritas kata kunci (persis dulu, lalu mengandung), bukan urutan kolom di file. Larangan baru: `avg`, `average`, `budget`, `status`, `type`, `id`, `share`, `/`, dst. Cek kewajaran: CPC < Rp 10 atau ROAS > 50x → ⚠️. Laporan mencetak "Kolom dibaca: …". |
| T4 | Tinggi | **Diperbaiki** | Mata uang dari 3 sumber (label `(USD)`, kolom `Currency`/`Currency code`/`Mata uang`, simbol/kode di sel). Asing → ditolak tanpa `--kurs`/`--mata-uang IDR`; campur → selalu ditolak. |
| S1 | Sedang | **Diperbaiki** | Gabung: (a) nama hasil sama tapi beda platform → ⚠️ atribusi berbeda; nama beda → hasil & biaya/hasil gabungan **tidak dihitung**; (b) ROAS gabungan hanya dari platform yang punya nilai + disebut platformnya; (c) catatan kurs ikut; (d) tidak ada label "Pesan wa: 360" campuran; (e) JSON yang sama dua kali ditolak (sidik SHA-256 file); (f) saran bergiliran per platform (maks. 6). |
| S2 | Sedang | **Diperbaiki** | Kampanye Rp 0 tidak dinilai (dicatat). TERBAIK & PERLU PERHATIAN tanpa irisan (≤ 2×top kampanye ber-hasil: TERBAIK maks. separuhnya). Iklan di TERBAIK tidak pernah disarankan "matikan". |
| S3 | Sedang | **Diperbaiki** | Header dicari dalam 15 baris pertama; baris judul dilewati & dicatat; periode dibaca dari baris judul (mis. "September 14, 2026 - September 20, 2026"). UTF-16 (BOM atau banyak byte nol) didekode; pemisah dipilih dari baris header. `.xlsx/.xls` ditolak dengan petunjuk Save As CSV. |
| S4 | Sedang | **Diperbaiki** | `parse_omzet()`: angka penuh, `Rp…`, `rb/ribu/k`, `jt/juta`, `miliar/milyar`; `M` ditolak karena ambigu. |
| R1 | Rendah | **Diperbaiki** | Periode dari `Reporting starts/ends`; ⚠️ rentang > 7 hari; ⚠️ tanggal tak terbaca (contoh isinya); ⚠️ file minggu lalu sama persis / periode sama. |
| R2 | Rendah | **Diperbaiki** | Seluruh hitungan uang, persen, dan ROAS memakai `Decimal` (tanpa float). |
| R3 | Rendah | **Diperbaiki** | `--kurs` ≤ 0/bukan angka ditolak (pesan JSON, bukan usage argparse); biaya negatif → ⚠️; `"250.000,00;x"` = rusak. |
| R4 | Rendah | **Diperbaiki** | `--csv-keluaran` = file input ditolak; judul kolom dari `--nama-hasil` disanitasi; angka CSV mentah (tanpa pemisah ribuan, desimal titik) konsisten di semua kolom. |
| R5 | Rendah | **Diperbaiki** | Pembanding saran = biaya per hasil semua iklan (sama dengan angka di atasnya). Hasil < 5 → catatan "sampel kecil". Catatan PPN saat `--omzet` diisi (**PERLU REVIEW** pemilik: kalimatnya sengaja umum, "bisa ditambah PPN, cek invoice"). |
| R6 | Rendah | **Diperbaiki** | SKILL.md: password/OTP/token yang ditempel tidak diulang/disimpan, sarankan ganti password + 2FA; jalur "API resmi + token" disebut ditolak. |
| R7 | Rendah | **Diperbaiki** | `references/openclaw-jadwal.md` §3a: bentuk `--command-argv` (deterministik) dengan resep nama file tetap `…-minggu-ini.csv`/`…-minggu-lalu.csv`. |
| R8 | Rendah | **Diperbaiki sebagian** | `Results`/`Results value` Google dikenali. `sumber-kolom.md` kini punya tabel status verifikasi jujur per platform (TikTok: sebagian dari sumber pihak ketiga). |
| K1 | Kosmetik | **Diperbaiki** | "Pesan WA" (bukan "Pesan wa"); peringatan berupa kalimat, bukan `dict`; "naik dari 0" untuk jumlah hasil; "sama dengan minggu lalu"; pesan file tidak ada/izin dalam Bahasa Indonesia; JSON bukan hasil `analisis` → pesan ramah; peringatan kini di blok "⚠️ PERLU DICEK" di atas laporan (tidak ada lagi "di bawah ini"). |

## Perubahan perilaku yang perlu diketahui penguji
- Format teks: blok `⚠️ PERLU DICEK SEBELUM DIPAKAI` di bawah judul (bila ada), judul daftar menjadi `TERBAIK` /
  `PERLU PERHATIAN` (isi maks. 3, bisa kurang agar tidak beririsan), `Catatan:` berupa daftar dan selalu memuat
  "Kolom dibaca: …". Baris VS MINGGU LALU kini menyebut angka minggu lalu.
- JSON: angka tetap angka (bulat → int, pecahan → float); field baru `sidik_file`, `label_baris_total`,
  `catatan`, `ada_nilai_hasil`, `periode.jumlah_hari`, `kolom_dipakai.mata_uang`. Mode gabung membaca JSON dengan
  `parse_float=Decimal`.
- `bulat_satu_desimal()` masih mengembalikan float (kompatibel); hitungan internal memakai `bulat1()` (Decimal).

## Yang belum / batas yang tidak diklaim
- **Belum ada ekspor asli** dari platform mana pun. Nama kolom Meta (Inggris & sinonim UI Indonesia), perilaku
  sel `Results` kosong, bentuk file Google Ads (baris judul, `Total: …`, `Currency code`, UTF-16), dan kolom
  `Currency` TikTok **belum terverifikasi dari file asli** → **PERLU REVIEW**. Saran: pemilik menyediakan satu
  ekspor asli per platform (angka boleh disamarkan) untuk dijadikan tes regresi sebelum `rilis`.
- Deteksi baris total dari angka hanya menangkap baris = jumlah **semua** baris lain; subtotal sebagian tanpa label
  (mis. subtotal per grup tanpa kata "Total") tidak dikenali.
- Nama kampanye yang diawali kata total lalu `:`/`(`/`-`/angka (mis. "Total - Diskon") akan dianggap baris total
  (dicatat labelnya di Catatan, jadi terlihat).
- `¥` dilaporkan sebagai "JPY/CNY" (ambigu); tetap ditolak sebagai mata uang asing.
- Ambang "sampel kecil" (< 5 hasil) dan ambang kewajaran (CPC < Rp 10, ROAS > 50x) adalah pilihan pembuat, bukan
  standar industri.
- Uji A/B (`00-pembanding-tanpa-skill.md`) dan banding pesaing belum diulang untuk v1.0.1; perlu penguji
  independen, terutama skenario 01 apa adanya, 02B/C, 03a/b, dan 04 #8/#9/#11/#18.
- Pengiriman Telegram sungguhan dan `--command-argv` di Gateway Windows belum diuji.
