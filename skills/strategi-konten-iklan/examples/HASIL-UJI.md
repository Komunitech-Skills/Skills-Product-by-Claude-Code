# Hasil Uji Independen - strategi-konten-iklan v1.0.0

Penguji: agent independen (bukan pembuat), 2026-09-30. Hanya membaca folder skill + CLAUDE.md (+ SKILL.md tiga skill tetangga sekilas untuk cek tumpang tindih). Skill disalin ke scratchpad; tidak dipasang di `.claude/skills`. Platform: `claude-code (simulasi agent)`.

## Ringkasan
| Uji | Hasil |
|---|---|
| 06 Normal 1 - skincare Rp3jt penjualan | Lulus; angka benar; kepatuhan kosmetik ada (catatan TERBATAS perlu diingat agent, tidak otomatis) |
| 07 Normal 2 - bengkel Rp1,5jt leads WA | Lulus; angka benar; Google terbuang oleh bobot tetap walau paling cocok untuk jasa lokal |
| 08 Normal 3 - katering Rp8jt campuran | Lulus bersyarat; tujuan campuran tidak didukung (improvisasi 2x run + jumlah tangan); bug kelayakan kanal mingguan |
| 09 Input tidak lengkap | Lulus; tanya sekali, 6 butir, margin ambigu ditolak |
| 10 Di luar cakupan (klaim sembuh diabetes + jaminan ROAS 10x) | Lulus; klaim & jaminan ditolak, tetap membantu dengan titik impas |
| A/B (`00-pembanding-tanpa-skill.md`) | Dengan skill jelas lebih baik (8,5 vs 4) |
| Banding pesaing (`00-banding-pesaing.md`, marketingskills ads + content-strategy) | Menang 8,1 vs 5,2; pesaing unggul di taktik retargeting & skala berbasis kas |
| `tests/uji_regresi.py` | 30 tes OK |
| Verifikasi angka independen (Fraction, tanpa impor script) | 406 kasus (6 skenario + 400 acak, semua tujuan, 1-5 kanal, 1-5 minggu, bobot 1-5, margin 1-100%): 0 selisih - alokasi kanal, per minggu, aman/uji, rata-rata harian, iklan aktif maks, total = anggaran, ROAS impas = 1/margin (ceil 2 des.), ROAS target, CPA target, CPL, pesanan minimal |
| Contoh 01-03 bawaan | Semua nominal Rp di keluaran script ada di dokumen contoh |
| `validate.py --skill` | Lolos |
| `uji_openclaw.sh` (OpenClaw 2026.9.7) | strategi-konten-iklan eligible/modelVisible/commandVisible (satu-satunya gagal: kanboard-papan-kerja, di luar skill ini) |

## Uji script ekstrem & rusak
- Rp100rb: 1 kanal (Meta), "0 - DI BAWAH BATAS (cukup untuk 4 hari tayang 1 iklan)" + catatan. Rp99rb: GAGAL jelas. Rp500rb (batas bawah klaim README): semua kanal kecuali Meta dibuang, Meta pun di bawah batas (lihat temuan S2).
- Margin 1%: ROAS impas 100,00x, 3.000 pesanan minimal - benar tetapi TANPA peringatan. Margin 0,4% -> 250x tanpa peringatan. Margin 100% -> 1,00x. Margin 0% -> GAGAL. `--margin -10%` -> pesan usage argparse (bukan GAGAL); `--margin=-10%` -> "tidak terbaca".
- Satu kanal (`shopee`, `google`) benar; leads + shopee saja -> GAGAL jelas.
- Ambigu ditolak dengan pesan jelas: `1,500`, `1.5jt`, `5M`, `3,000,000`, `3000000.00`, margin `0,4`/`0.4`/`1.000%`. Diterima benar: `3.000.000,00`, `Rp. 3.000.000`, `1,5 jt`, `3 jt`, `40.5`, `40 %`.
- Ditolak padahal lazim: `Rp 3.000.000,-`, `IDR 3jt`, kanal `ig`/`instagram`/`fb`, `tiktok shop` (pesan "'shop' tidak dikenal" membingungkan).

## Temuan
### Tinggi
- Tidak ada.

### Sedang
- **S1 Bug kelayakan kanal saat bobot minggu tidak rata** (bukti: `08`, run B): `pilih_kanal` membandingkan bagian SEBULAN dengan 28 x minimum harian, sedangkan "iklan aktif maks" memakai minggu TERKECIL. Google Rp769.231 lolos (>= Rp700.000) tetapi minggu 1-2 hanya Rp128.205 < Rp175.000 -> tabel "0 - DI BAWAH BATAS (cukup untuk 30 hari...)" (30 > 28 hari tayang), dan catatan "DI BAWAH batas uji" tidak muncul. Perbaiki: saring kanal dengan minggu terkecil (atau konsisten dengan total), dan batasi `hari_tayang_terbiayai` ke jumlah hari rencana.
- **S2 Pemilihan kanal yang dipertahankan mengabaikan kelayakan** (bukti: Rp500rb semua kanal -> Meta dipertahankan walau tetap di bawah batas, padahal Shopee sendiri dengan min Rp10rb/hari cukup 28 hari; `07` bengkel: Google terbuang, padahal referensi kanal sendiri menyebut Google terkuat untuk jasa lokal). Saran: bila sisa 1 kanal, pilih kanal yang layak; atau SKILL.md menyuruh agent menawarkan varian satu kanal yang paling cocok (mis. `--kanal google` untuk jasa lokal).
- **S3 Tujuan campuran tidak didukung** (bukti: `08`): permintaan umum "kenal dulu tapi tetap jualan" memaksa agent membagi sendiri & menjumlah tangan (bertentangan dengan "angka dari script"). Saran: tambahkan aturan di SKILL.md (mis. pembagian default + dua run) atau opsi `--tujuan campuran`/`--porsi-awareness`.
- **S4 Tumpang tindih pemicu dengan `rencana-marketing-usaha`**: deskripsi keduanya memuat "alokasi anggaran iklan"/"bagi anggaran", dan contoh pemicu rencana-marketing-usaha ("Anggaran iklan Rp5 juta enaknya dibagi ke mana?") sama persis dengan contoh skill ini. Rumus impas konsisten (ROAS impas = harga/laba), jadi tidak bertentangan, tetapi agent bisa memilih skill yang salah. `rencana-marketing-usaha` juga belum merujuk skill ini. Nilai tambah skill ini tetap jelas (per minggu, batas uji & jumlah iklan, Shopee/TikTok Shop Ads, pilar + kreatif per tahap, aturan keputusan mingguan); `kalender-konten-30hari` (jadwal harian) dan `laporan-iklan-mingguan` (membaca hasil) terpisah dengan baik. Saran: pertegas di kedua deskripsi ("rencana 1-12 bulan" vs "anggaran iklan BULAN INI per kanal per minggu") dan tambahkan rujukan silang.

### Rendah
- R1 Margin sangat tipis (<= ~10%, ROAS impas >= 10x) tidak diberi peringatan "iklan berbayar hampir mustahil untung, perbaiki harga/margin dulu"; margin negatif hanya menghasilkan pesan usage/format, bukan penjelasan "setiap penjualan rugi".
- R2 Kata `skincare`/`kosmetik`/`suplemen`/`klinik`/`obat` tidak memicu catatan kesehatan TERBATAS (hanya kata "kesehatan"), padahal referensi pilar menandai skincare sebagai TERBATAS. Serupa: `pinjaman`/`investasi`/`asuransi` tidak memicu catatan keuangan.
- R3 Alias kanal lazim (ig, instagram, fb, "tiktok shop") dan format `Rp 3.000.000,-` ditolak; agent bisa menerjemahkan, tetapi pesan "'shop' tidak dikenal" membingungkan.
- R4 Pesan GAGAL margin selalu memakai contoh "0,4" meski input berbeda.
- R5 Tidak ada panduan retargeting (pengunjung/pengobrol WA yang belum beli) - kelebihan utama pesaing.
- R6 Contoh eksplisit klaim penyakit kronis / ajakan meninggalkan pengobatan belum ada di examples bawaan (kini diwakili `10`).

## Skor: 8/10
Alasan: semua angka terbukti benar lewat verifikasi independen 406 kasus dan tidak pernah memprediksi hasil; parsing angka ambigu sangat hati-hati; pilar konten dan kepatuhan (kategori terbatas, tanpa jaminan) kuat; menang jelas di A/B dan banding pesaing. Dikurangi karena bug konsistensi kelayakan kanal mingguan (S1), heuristik kanal yang bisa memilih kanal kurang cocok/tidak layak (S2), tujuan campuran belum didukung (S3), dan tumpang tindih pemicu dengan rencana-marketing-usaha (S4). Skor >= 7: boleh `lulus`; perbaikan S1-S4 disarankan sebelum `beta`, lalu uji ulang independen untuk bagian yang diubah.

## Revisi 1.0.5 (2026-10-05) - menunggu uji ulang independen
Pemicu: pra-cek Telegram G9 skor 6,5 (tanpa dasar BPOM/iklan, hanya bertanya AOV, kata "script" bocor). Perbaikan: aturan "kerjakan dulu, tanya di akhir" (tolak klaim + dasar aturan, ROAS impas 2,5x langsung, tidak ada ROAS pasti), larangan kata proses, checklist, dan `references/kepatuhan-klaim-iklan.md` (PERLU REVIEW pasal). Script tidak berubah; tes regresi dijalankan ulang. **Status: menunggu uji ulang independen** (belum diuji di OpenClaw oleh pembuat).
