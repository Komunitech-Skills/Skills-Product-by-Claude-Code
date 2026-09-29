# HASIL UJI - riset-saham-berita v1.0.0

- **Tanggal uji:** 2026-09-29
- **Penguji:** agent independen (bukan pembuat), hanya membaca folder skill + CLAUDE.md. SKILL.md & script tidak diubah.
- **Platform:** claude-code (simulasi agent). Belum diuji di OpenClaw/Codex/Cursor asli; `scripts/uji_openclaw.sh` tidak dijalankan dalam sesi uji ini.
- **Folder kerja:** scratchpad `uji-saham/` (bukan `.claude/skills/`).

## Skor kualitas: **8 / 10** -> LULUS (>= 7), dengan 3 perbaikan SEDANG yang disarankan sebelum `beta`

Alasan: kepatuhan aturan pemilik sempurna (0 kebocoran rekomendasi), angka script 100% cocok dengan verifikasi
independen, penanganan data basi/interim/rugi/ekuitas negatif sangat baik, dan menang telak di A/B & banding pesaing.
Tidak 9-10 karena: exit code `level` menyesatkan untuk jadwal otomatis, akhiran "M" dibaca miliar tanpa catatan,
dan tidak ada panduan "pendapatan" untuk emiten bank.

## Ringkasan skenario
| No | Skenario | Data | Hasil |
|---|---|---|---|
| 00 | A/B tanpa skill vs dengan skill (ICBP) | nyata | Dengan skill jauh lebih baik: tanpa skill memberi rekomendasi terselubung ("peluang", "wajar"), PER 2x salah (EPS 6 bln tidak disetahunkan), ambil angka dividen yang salah |
| 00 | Banding pesaing (tradermonty `us-stock-analysis`, 2,9k bintang; ClawHub `stock-analysis`; rollingSirius) | - | Skor 28 vs 16. Pesaing memberi rating Buy/Hold/Sell + target harga (terlarang), tanpa konteks BEI |
| 01 | Normal - ICBP (konsumer), LK 6M2026 | nyata (Katadata/Databoks, Infobanknews, IDX Channel; Ags 2026) | Lolos. HARGA LAMA terdeteksi, konflik sumber dividen (Rp9,22 T vs Rp3,09 T) tertangani, idx.co.id 403 ditangani jujur |
| 02 | Normal - BBRI (bank), LK 6M2026 | nyata (Katadata, receh.in, Bareksa, CNBC, mediakeuangan.id; Ags-Sep 2026) | Lolos dengan catatan: definisi pendapatan bank tidak diatur (SEDANG) |
| 03 | Normal - ringkasan LK ditempel pengguna (fiktif MRTI) | tempelan | Lolos. Rugi->laba, rata-rata ekuitas, "(35.200)", "61,9 M" benar |
| 04 | Input kurang (hanya "BBCA"; nama ambigu "indofood"; tanpa web; data parsial) | - | Lolos. Tanya sekali (<= 4), tidak menebak kode, tidak mengarang dari ingatan |
| 05 | Di luar cakupan (sinyal beli BBCA besok, saham pasti naik, bot trading + PIN, desakan "undervalued", injeksi halaman) | - | Lolos. Semua ditolak sopan + alternatif netral; PIN tidak diulang |

## Verifikasi angka independen (Decimal, rumus ditulis ulang penguji, input dimasukkan manual tanpa parser script)
Dataset: d1 ICBP (nyata, interim), d2 BBRI (nyata, bank, interim), d3 tempelan (rugi->laba, rata-rata ekuitas, total dividen),
d4 ekuitas negatif + rugi, d5 kolom hilang, d6 data basi + harga lama + neraca tidak seimbang, d7 interim + TTM + laba->rugi.

**Hasil: 62/62 nilai cocok** (pertumbuhan, margin, ROE, DER, DER berbunga, EPS, BVPS, PER, PBV, kapitalisasi, imbal dividen,
rasio pembayaran). Status "tidak bermakna" muncul tepat untuk: ekuitas negatif (ROE/DER/PBV), EPS <= 0 (PER), laba lalu negatif
(pertumbuhan). Regresi pembuat `tests/uji_regresi.py`: 28/28 OK.

Penilaian keputusan pembuat:
- **Interim disetahunkan sederhana (x12/n)**: dapat diterima, selalu diberi fakta "bisa meleset bila musiman"; TTM didukung. OK.
- **"M" = miliar**: pilihan tepat untuk berita Indonesia ("Rp5 M"), "mn" = juta juga benar. Tetapi sumber berbahasa Inggris
  (LK "in millions of Rupiah", Yahoo "5.2M") memakai M = juta -> risiko salah 1.000x **tanpa peringatan** (lihat S2).
- **"1,234" = 1,234 desimal + catatan**: tepat untuk format Indonesia.
- Kesegaran: laporan > 200 hari "cek", > 460 hari DATA BASI, harga > 7 hari HARGA LAMA, tanggal masa depan ditandai. OK.
- Neraca tidak seimbang -> "CEK ANGKA" (terpicu di d6). OK.

Format angka diuji lewat `angka`: "Rp1,2 T", "1.234,5 miliar", "1,234,567", "1,234.5", "(12.000)", "−1.000", "Rp 1.500,-",
"IDR 2.5bn", "Rp2.352 triliun", "1 234 567" benar. Error jelas (exit 1) untuk "1.2.3", "abc", "1e6", "10%", "US$5 M", ".5".

Kode keluar: `rasio` 0 = sukses, 1 = JSON rusak / bukan objek / saham 0 / periode_bulan 4 / tanggal "30 Juni 2026" / satuan tak dikenal / angka terlalu besar / boolean (semua pesan jelas).
`level`: 0 = tidak ada tersentuh, 2 = tersentuh (termasuk harga = level persis), 1 = kolom wajib hilang / file kosong / file tidak ada / --hari-ini salah. CSV titik-koma & tanggal dd/mm/yyyy didukung.

## Sapuan kepatuhan (aturan pemilik: tanpa rekomendasi/sinyal/auto-trading)
- grep `beli|jual|tahan|akumulasi|target|sinyal|undervalued|murah|mahal|layak|menarik|wajar|peluang|support|resistance|entry`
  pada SKILL.md, README, references, templates, examples pembuat, script, dan keluaran uji 01-05: **semua kemunculan berupa
  larangan, penolakan, atau kutipan permintaan pengguna. Kebocoran: 0 (tidak ada temuan TINGGI).**
- Disclaimer OJK (kontak 157) ada di SKILL.md (Batas Tegas #6), README, template, dan dicetak otomatis oleh kedua perintah script.
- Kalimat penutup script "bukan penilaian murah/mahal atau layak/tidak" dan "bukan sinyal" pada `level`. Bagus.
- Keamanan script: hanya pustaka standar (argparse, csv, json, re, sys, datetime, decimal); tanpa jaringan, tanpa menulis file, tanpa subprocess/eval. Tidak ada kredensial tertanam.

## Temuan per tingkat keparahan

### TINGGI
- Tidak ada.

### SEDANG
- **S1. `level` keluar dengan kode 0 walau baris gagal dicek.** Bila semua baris salah (mis. harga "abc", level kosong, level terbalik),
  keluaran "Baris yang tidak dicek" tetapi exit 0 = "tidak ada level tersentuh". Untuk jadwal OpenClaw/cron yang hanya membaca exit
  code, kegagalan ambil harga akan tampak seperti "aman". Saran: exit 1 (atau kode 3) bila `masalah` tidak kosong dan tidak ada yang tersentuh; dokumentasikan di SKILL.md E.3.
- **S2. Akhiran "M" dibaca miliar tanpa catatan.** Tambahkan catatan otomatis ("'61,9 M' dibaca 61,9 MILIAR; bila sumber berbahasa Inggris M = million, tulis 'juta'") seperti kasus "1,234", dan instruksi di SKILL.md B.1: sumber berbahasa Inggris -> pakai `satuan_laporan` tanpa akhiran.
- **S3. Emiten bank/keuangan: "pendapatan" tidak didefinisikan.** Di BBRI penguji memakai pendapatan bunga bersih -> "margin laba bersih" 38,76% tidak sebanding dengan emiten lain dan tidak diberi catatan oleh script/skill. Saran: untuk sektor keuangan, script menambah fakta "margin memakai [pos yang diisi]; tidak sebanding lintas sektor", dan SKILL.md menyebut pos yang dipakai (mis. total pendapatan operasional) + menjelaskan bila ROE hitungan berbeda dari ROE yang dilaporkan bank (18,08% vs 18,8%).

### RENDAH
- **R1.** "0.125" dibaca 125 tanpa catatan (grup "0" diperlakukan ribuan); "1.250" gaya Inggris (=1,25) juga tanpa catatan. Saran: grup depan "0" -> desimal, dan beri catatan untuk pola "d.ddd" di kolom harga/DPS.
- **R2.** `satuan_laporan` "dalam jutaan" / "jutaan rupiah" ditolak (pesan jelas, tapi awam sering menyalin frasa LK apa adanya). Saran: buang kata "dalam"/"rupiah".
- **R3.** Laba -> rugi ditulis "-251,00%" dan fakta "Laba bersih turun 251,00%"; kasus sebaliknya sudah "tidak bermakna". Saran: simetris, "berbalik dari laba menjadi rugi".
- **R4.** ROE mencampur basis: laba induk / total ekuitas (bila ekuitas induk kosong) tanpa catatan; rata-rata ekuitas tidak mungkin bila ekuitas induk diisi (tidak ada `ekuitas_entitas_induk_lalu`).
- **R5.** Tampilan `level` membulatkan harga/level ke rupiah bulat ("1,5" tampil Rp2, level 2 & 1 tampil Rp2/Rp1). Minor karena harga BEI bulat.
- **R6.** SKILL.md E.5 merujuk `pantau-pasar-kripto/references/openclaw-jadwal.md` yang tidak ada di folder ini; pembeli ecer tanpa skill itu tidak punya panduan jadwal. Saran: salin ringkas ke `references/` skill ini.
- **R7.** Saham treasuri tidak disebut (EPS/BVPS/kapitalisasi memakai "saham beredar"); tambahkan satu baris di SKILL.md B.4.
- **R8.** Langkah A: bila hanya ada cuplikan mesin pencari (sumber asli tak bisa dibuka), SKILL.md belum mengatur statusnya; penguji menandai "perlu dicek". Saran: sebut eksplisit.

## Catatan data nyata yang ditemukan saat uji (menunjukkan nilai skill)
- idx.co.id mengembalikan 403 untuk akses otomatis (sesuai peringatan `references/sumber-data.md`).
- IDX Channel (26-06-2026) menulis total dividen ICBP Rp9,22 T; DPS Rp265 x 11.661.908.000 saham = Rp3,09 T (sesuai sumber lain).
- mediakeuangan.id (25-09-2026): "penutupan sebelumnya 3.300" namun perubahan 0% -> tidak konsisten.
- BBRI: laba konsolidasian 6M Rp31,2 T vs laba bank-only 8M Rp34,77 T - basis berbeda, perlu dijelaskan (skill menangani lewat aturan "sumber bertentangan").

## Rekomendasi
Status boleh naik ke `lulus` (skor 8). Perbaiki S1-S3 (perubahan kecil di script + 3-4 baris SKILL.md) sebelum uji platform asli/beta;
setelah revisi, jalankan ulang skenario 02 & uji `level` oleh penguji independen.

---

# Uji ulang v1.0.1 (2026-09-29)

- **Penguji:** agent independen yang sama (bukan pembuat); SKILL.md & script tidak diubah; tanpa commit.
- **Tes pembuat:** `tests/uji_regresi.py` **43/43 OK**.

## Skor: **9 / 10** -> LULUS (naik dari 8)
Semua temuan SEDANG (S1-S3) dan RENDAH (R1-R8) diperbaiki dan terverifikasi. Kepatuhan tetap bersih. Sisa: 2 catatan RENDAH
di `references/jadwal-openclaw.md` (di bawah) dan jadwal skill ini sendiri belum diuji di Gateway OpenClaw.

## Regresi 7 dataset / 62 nilai
- d1, d2, d4, d5, d7: exit 0, **61/61 + 1 (d5 ROE 19,05%) = 62/62 cocok** dengan verifikasi Decimal independen (angka identik dengan v1.0.0).
- d3 & d6 (berisi "61,9 M", "98,7 M"): kini **ditolak** (exit 1, pesan "akhiran M ambigu ... --arti-m miliar / juta"). Dengan
  `--arti-m miliar` atau `"arti_m": "miliar"` hasil identik dengan v1.0.0 + catatan "dibaca MILIAR karena arti_m = miliar";
  dengan `--arti-m juta` total dividen Rp61,9 jt (DPS Rp0,01) - benar secara hitung.
- Catatan: `examples/03-normal-tempelan.md` langkah 2 menggambarkan perilaku v1.0.0 ("61,9 M" langsung dibaca miliar); di v1.0.1
  agent wajib mengisi `arti_m` setelah konfirmasi pengguna - alur konfirmasi yang dijalankan agent di uji 03 kini dipaksa script.

## Verifikasi perbaikan
| Temuan | Hasil v1.0.1 | Status |
|---|---|---|
| S1 `level` exit 0 walau baris gagal | Semua salah -> **3**; campuran salah (L6) -> 3; tersentuh + gagal (L8) -> 3 + baris "Ringkasan: ... 1 menyentuh level Anda, 1 baris GAGAL dicek ... TIDAK berarti aman" dan baris tersentuh tetap tampil; header saja -> 3; normal 0/2 tetap; kolom hilang/file kosong/tidak ada -> 1. Didokumentasikan di docstring & SKILL.md E.3 | Tuntas |
| S2 "M" diam-diam = miliar | "5 M", "IDR 5.2M" ditolak (exit 1) tanpa `--arti-m`; "mn" = juta tetap | Tuntas |
| S3 pendapatan bank | Label "Margin laba bersih (bank; tidak sebanding lintas sektor)", fakta "pendapatan = pendapatan bunga bersih + pendapatan operasional lain", peringatan ROE beda dari yang dilaporkan bank; SKILL.md B.4 diperbarui | Tuntas |
| R1 "0.125" -> 125 | Kini 0,125 | Tuntas |
| R2 "dalam jutaan rupiah" | Diterima (pangkat 6) | Tuntas |
| R3 laba -> rugi | Fakta "Berbalik dari LABA menjadi RUGI; persen kurang bermakna" (nilai -251% tetap tampil di tabel - dapat diterima) | Tuntas |
| R4 basis ROE campur | `ekuitas_entitas_induk_lalu` -> rata-rata (9/90 = 10,00% cocok); laba induk / total ekuitas -> fakta "ROE mencampur basis" (9/110 = 8,18% cocok) | Tuntas |
| R5 tampilan level desimal | "1,5" tampil Rp1,50 | Tuntas |
| R6 rujukan skill lain | `references/jadwal-openclaw.md` sendiri | Tuntas (lihat catatan) |
| R7 saham treasuri | SKILL.md B.4: saham beredar dikurangi saham treasuri | Tuntas |
| R8 cuplikan mesin pencari | SKILL.md A.6: status "dari cuplikan pencarian, perlu dicek" | Tuntas |

## Cek `references/jadwal-openclaw.md` vs `skills/laporan-otomatis-terjadwal/references/openclaw.md`
- Bentuk perintah = **Bentuk A** referensi (jadwal & pesan posisional, tanpa `--cron`) dengan opsi yang sama persis:
  `--tz "Asia/Jakarta" --name ... --session isolated --announce --channel telegram --to ...`. Pengelolaan `automations run <id> --wait`,
  `disable <id>`, `rm <id>` juga ada di referensi. **Tidak ada flag karangan.** Status "belum diuji di Gateway untuk skill ini" ditulis jujur.
  Kanal default Telegram ke pemilik, WhatsApp hanya nomor terpisah + persetujuan tertulis, tanpa broadcast - sesuai keputusan pemilik.
- **RENDAH J1:** pesan jadwal menyuruh agent "balas persis NO_REPLY" bila kode 0. Referensi `laporan-otomatis-terjadwal` tidak
  memakai/membuktikan penekanan `NO_REPLY` untuk job berbasis pesan agent + `--announce`; bukti `NO_REPLY` di repo hanya untuk pola
  `--command-argv` di `pantau-pasar-kripto`. Risiko: pemilik menerima teks "NO_REPLY" tiap hari bursa. Saran: tandai "belum terbukti"
  dan uji dengan `automations run <id> --wait` saat semua level tidak tersentuh.
- **RENDAH J2:** pesan jadwal tidak menyebut perilaku untuk **kode 1** (tabel §3 menyebut "kirim pesan galat"); tambahkan "Kode 1: kirim pesan galat apa adanya" ke teks pesan.

## Sapuan kepatuhan v1.0.1
grep kata rekomendasi (beli/jual/tahan/akumulasi/target harga/sinyal/undervalued/murah/mahal/layak/menarik/harga wajar/peluang/support/resistance/entry/cut loss)
di SKILL.md, README, references (termasuk jadwal-openclaw.md), templates, script: semua kemunculan berupa larangan, penolakan, atau kutipan
permintaan pengguna. **Kebocoran: 0.** Disclaimer OJK (kontak 157) tetap ada di SKILL.md, README, dan kedua keluaran script; pesan jadwal
mewajibkan disclaimer & "tanpa rekomendasi beli/jual".

## Uji ulang (2026-09-29, akhir) — v1.0.2
- **Penguji:** agent independen (bukan pembuat); scratchpad `uji-0929-akhir`; Python 3.11; simulasi agent `claude-code`. OpenClaw tidak terpasang di lingkungan uji (jadwal dinilai dari dokumen + script). Script/SKILL.md tidak diubah.
- **Tes regresi:** `tests/uji_regresi.py` **46/46 OK** (termasuk tes J1/J2); `validate.py --skill riset-saham-berita` ✅.

| Perbaikan | Hasil |
|---|---|
| J1 tanpa `NO_REPLY` | ✅ pesan jadwal di `references/jadwal-openclaw.md` tidak lagi menyuruh `NO_REPLY`; kemunculan tersisa hanya larangan + alasan ("belum terbukti", uji dulu dengan `automations run <id> --wait`). Kode 0 selalu mengirim pesan pendek (jadwal terbukti hidup). |
| J2 pesan per kode 0/1/2/3 | ✅ didefinisikan di teks perintah **dan** tabel §3 + kasus "script tidak bisa dijalankan". |
| Kode keluar script sesuai dokumen | ✅ diuji dengan 10 file: tidak tersentuh → **0**; satu menembus level atas → **2**; harga kosong + level terbalik (+1 tersentuh) → **3** dengan daftar baris gagal & "TIDAK berarti aman"; semua baris gagal / hanya header → **3**; kolom wajib hilang, file kosong, file tidak ada → **1** dengan pesan galat. Harga Jumat dicek Senin (≤7 hari) → 0 tanpa catatan. |

Kepatuhan: kode 0 menyertakan "Bukan rekomendasi beli/jual."; keluaran script memuat disclaimer OJK (157) dan "level ditetapkan sendiri oleh Anda". Tanpa kata rekomendasi baru.

Temuan:
1. **[RENDAH]** Harga basi (mis. 28 hari) tetap kode **0**; catatan "harga lama (28 hari)" hanya ada di tabel, sedangkan pesan kode 0 berisi baris Ringkasan saja → pemilik bisa menerima "tidak ada level tersentuh" dari harga lama bila agent lupa mengosongkan harga. Saran: hitung harga lama di baris Ringkasan atau jadikan kode 3.

### Skor: **9/10** (lulus)
Alasan: J1 & J2 tertutup, pesan untuk tiap kode keluar jelas dan kode keluar script terbukti sesuai tabel; 46 tes lulus; kepatuhan tanpa rekomendasi terjaga. Penekanan pesan di Gateway OpenClaw asli belum diuji (ditulis jujur di dokumen).
