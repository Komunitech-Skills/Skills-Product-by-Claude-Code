# HASIL UJI — atur-keuangan-pribadi v1.0.0

- **Penguji:** agent independen (bukan pembuat), Claude Code (Opus), 2026-09-26.
- **Cara uji:** folder skill disalin ke scratchpad; agent hanya membaca `SKILL.md`, `references/`, `templates/`, `README.md` sebagai pengguna skill dan menjalankan `scripts/keuangan.py` dari salinan. **Kode `keuangan.py` dan `tests/uji_regresi.py` tidak dibaca** (hanya `--help` dan grep impor jaringan/berkas → nihil) agar verifikasi angka independen.
- **Platform:** `claude-code (simulasi agent)`. `scripts/uji_openclaw.sh` tidak dijalankan dalam sesi uji ini.

## 1. Ringkasan skenario
| # | Berkas | Skenario | Hasil |
|---|---|---|---|
| 01 | `01-keluarga-muda-bekasi-anggaran-dana-darurat.md` | Suami Rp8,5 jt + istri Rp4 jt, 1 anak, KPR Rp3,1 jt, motor Rp1,2 jt, kiriman ortu Rp1 jt — anggaran zero-based 60/20/20 + dana darurat 9–12 bln | LULUS |
| 02 | `02-karyawan-4-utang-avalanche-snowball.md` | KK Rp12 jt, KTA Rp30 jt flat 0,9%/bln 24 bln, paylater Rp3 jt, pinjol Rp2 jt, ekstra Rp2,5 jt | LULUS (10 bln, bunga Rp4.226.895) |
| 03 | `03-freelancer-target-dp-rumah.md` | Freelancer penghasilan naik-turun, bonus Rp10 jt, DP rumah Rp150 jt 4 th | LULUS |
| 04 | `04-input-tidak-lengkap.md` | "gimana cara atur keuangan saya?" | LULUS (tanya sekali, 6 butir + jalur cepat) |
| 05 | `05-di-luar-cakupan-berisiko.md` | Minta pinjol "pasti cair" utk tutup utang + saham/kripto "pasti naik" | LULUS (tolak sopan, arahkan OJK 157, restrukturisasi) |
| A/B | `00-pembanding-tanpa-skill.md` | Skenario 02 tanpa vs dengan skill | Dengan skill **jelas lebih baik** (tanpa skill bunga meleset −37%) |
| Pesaing | `00-banding-pesaing.md` | openaccountant `debt-payoff`/`zero-based-budget` + joellewis `debt-management` | Skill kita **unggul** (pesaing −37% bunga, tanpa flat/OJK/BI) |

## 2. Verifikasi angka independen
Simulator penguji ditulis sendiri (Python `fractions.Fraction`, bulan demi bulan: bunga = round-half-up(saldo × bunga bulanan) → tambah ke saldo → bayar minimum `min(minimum, saldo, sisa anggaran)` → sisa anggaran ke utang prioritas berurutan; anggaran tetap sehingga cicilan utang lunas bergulir; %/th ÷ 12, %/hari × 30; Avalanche = bunga tertinggi, seri → saldo kecil; Snowball = saldo terkecil, seri → bunga tinggi). Flat→efektif dengan bisection anuitas (setara RATE). Target dengan FV anuitas (setor akhir bulan).

| Uji | Jumlah kasus | Hasil |
|---|---:|---|
| Skenario 02 (Avalanche & Snowball): total bunga, bulan lunas, bunga per utang, urutan | 2 | **Identik** (Rp4.226.895; 10 bln; 1/2/5/10) |
| Utang acak 1–5 utang, bunga %/th, %/bln, %/hari, 0%, saldo & minimum acak, ekstra 0–4 jt, mode banding | **60** | **60/60 identik** (total bunga, total bulan, bunga & bulan lunas tiap utang, urutan serangan) |
| Kasus tepi: minimum < bunga tanpa ekstra | 1 | Script: peringatan + "TIDAK AKAN LUNAS", sisa Rp20.100.000 ✓ |
| Minimum < bunga tapi ekstra cukup | 1 | 17 bln, Rp3.893.827 — identik ✓ (peringatan tetap muncul untuk "hanya bayar minimum" — tepat) |
| Saldo nol | 1 | Lunas "bulan ke-0", bunga Rp0; utang lain identik ✓ |
| Bunga 0% | 1 | 8 bln, Rp0 ✓ |
| Anggaran < total minimum; bunga 60%/bln; bunga/saldo negatif | 4 | Ditolak dengan pesan ramah, kode keluar 2 ✓ |
| Contoh di SKILL.md (Avalanche 15 bln Rp3.345.301; Snowball Rp3.501.409; kemenangan pertama bln 3 vs 2) | 1 | Identik ✓ |
| Contoh `references/rumus-manual.md` (1 utang Rp45.950 bln 4; flat 17,97% & 21,57%; DP Rp888.542) | 4 | Identik ✓ |
| Flat→efektif acak (pokok, flat 1–40%/th, tenor 6–60) | **40** | **40/40** cicilan ±Rp1 & efektif/th ±0,01 poin ✓ |
| Target acak (biaya, 1–25 th, inflasi 0–10%, imbal 0–7,25%, terkumpul) | **40** | **40/40** biaya nanti & tabungan/bulan identik ✓ |
| Skenario 01/03/04 (THR ÷ 12 floor, rasio cicilan, dana darurat ceil) | — | Cocok hitungan manual ✓ |
| Varian penguji: minimum KK 5% dari saldo (bukan tetap) pada skenario 02 | 1 | Rp4.226.985 vs Rp4.226.895 (selisih Rp90) — asumsi minimum tetap tidak material bila anggaran tetap |

### Data rusak (`dana-darurat --pengeluaran-pokok`, `anggaran`, `utang`, `target`, `konversi-flat`)
| Input | Hasil |
|---|---|
| `1,5jt`, `1.5jt`, `1,5 juta`, `2 juta`, `750 ribu`, `Rp 750.000,-`, `Rp1.500.000,00`, `Rp. 2.000.000`, `IDR 2000000`, `1,500,000`, `10k` | Terbaca benar ✓ |
| `1.250.000,50` | Rp1.250.001 (dibulatkan) ✓ |
| `5M` / `5m` | Ditolak: ambigu juta/miliar ✓ |
| `lima juta`, `2jt500rb`, kosong, `0` | Ditolak ramah, kode 2 ✓ |
| `=-500rb`, pos `-1jt`, saldo `-5jt`, bunga `-2%/bln`, inflasi `-3` | Ditolak "tidak boleh negatif" ✓ |
| `-500rb` tanpa `=` | Pesan argparse bahasa Inggris "expected one argument" (T-7) |
| `1.500` | Diterima sebagai **Rp1.500** tanpa peringatan (T-2) |
| Bunga `dua persen`, `2%/minggu`; utang kurang kolom; tenor 0; cicilan < pokok | Ditolak ramah ✓ |
| Tanpa traceback di semua kasus | ✓ |

`python3 tests/uji_regresi.py` → **33 tes OK**. `python3 scripts/validate.py` (repo) → lolos.

## 3. Pemeriksaan fakta (web search 2026-09-26)
| Klaim di skill | Hasil cek | Sumber |
|---|---|---|
| Batas bunga pinjol konsumtif 0,1%/hari 2026 (0,3% 2024, 0,2% 2025); produktif 0,067%/hari | Sesuai | https://www.antaranews.com/berita/3848418/ojk-tetapkan-suku-bunga-pinjol-produktif-0067-persen-hari-pada-2026 ; https://finansial.bisnis.com/read/20260421/563/1968235/94-daftar-pinjol-resmi-ojk-2026-ini-besaran-bunga-serta-cara-mudah-cek-legalitasnya |
| Batas bunga kartu kredit BI 1,75%/bln sejak Juli 2021, masih berlaku | Sesuai | https://www.cnbcindonesia.com/market/20260818084032-17-760171/segini-batas-maksimum-bunga-kartu-kredit-indonesia-ritel |
| Relaksasi BI minimum 5% & denda maks. Rp100.000 s.d. 31 Des 2026 | Sesuai (perpanjangan hingga akhir 2026) | https://infobanknews.com/bi-perpanjang-keringanan-tagihan-kartu-kredit-hingga-31-desember-2026 ; https://www.stabilitas.id/bi-perpanjang-stimulus-tarif-sknbi-dan-batas-minimum-kartu-kredit-hingga-akhir-2026/ |
| Kontak OJK 157, WA 081-157-157-157 | Sesuai | https://x.com/ojkindonesia/status/1448902618848260105 ; https://periskop.id/pembiayaan/20260817/ciri-pinjol-ilegal-cara-cek-legalitas |
| 94 pinjol berizin (Agustus 2026) | Sesuai (juga per September 2026) | https://www.metrotvnews.com/read/kqYCdrmP-daftar-94-pinjol-resmi-ojk-september-2026-dan-cara-cek-legalitasnya |
| Disclaimer "bukan nasihat keuangan/investasi" | Ada di SKILL.md, setiap keluaran script, README | — |
| Tidak ada rekomendasi produk investasi | Benar; imbal hasil hanya asumsi pengguna; script menulis "tidak ada rekomendasi produk investasi" | — |

## 4. Temuan (berprioritas)
| ID | Prioritas | Temuan | Lokasi | Usulan perbaikan |
|---|---|---|---|---|
| T-1 | **Sedang** | `konversi-flat --bunga-flat` hanya menerima persen **per tahun** tanpa satuan. Pengguna Indonesia sering menyebut flat **per bulan** ("0,9% per bulan"). `--bunga-flat 0,9` diterima diam-diam sebagai 0,9%/th → efektif **1,72%/th** padahal benar **19,53%/th** (meleset ±11×). `--bunga-flat "0,9%/bln"` ditolak dengan contoh "4 atau 4,5%" yang tidak menyebut "per tahun". | `scripts/keuangan.py` (parser `--bunga-flat`), `SKILL.md` langkah 6 & blok Script, `templates/daftar-utang.md` | Terima satuan `%/th`, `%/bln` seperti `--utang`; pesan galat sebut "persen PER TAHUN (mis. 10,8) atau 0,9%/bln"; peringatan bila flat < 3%/th ("apakah ini per bulan?"); tampilkan periode input di keluaran. Tambah tes regresi. |
| T-2 | Rendah | `1.500` dibaca Rp1.500 tanpa peringatan (bisa maksud 1,5 jt). | parser uang | Peringatkan bila nominal pemasukan/pengeluaran/saldo utang < Rp10.000. |
| T-3 | Rendah | `utang` tidak menerima bunga flat langsung; agent harus menyalin efektif 3 desimal (1,628% vs 1,62753% → selisih bunga Rp1.052). | `utang`, `konversi-flat` | Keluaran `konversi-flat` tampilkan 4–5 desimal, atau `--utang` terima `0,9%/bln flat` + tenor. |
| T-4 | Rendah | Peringatan "bila bunganya FLAT, ubah dulu..." selalu muncul untuk jenis `kta`, meski sudah dikonversi. | `utang` (peringatan jenis) | Hilangkan bila bunga ditandai `efektif`, atau ubah jadi catatan ringan. |
| T-5 | Rendah | `target --kemampuan` hanya menyebut kekurangan/bulan, tidak menghitung **berapa bulan tercapai** dengan kemampuan itu; agent harus coba-coba `--tahun`. | `target` | Tambah baris "Dengan Rp X/bulan, target tercapai ±N bulan (biaya ikut inflasi)" atau "tidak akan tercapai" bila inflasi > setoran. |
| T-6 | Rendah (fitur) | Belum ada pembanding **take over/konsolidasi/refinance** (breakeven biaya, jebakan tenor lebih panjang) — ada di pesaing joellewis, sering ditawarkan bank di Indonesia. | SKILL.md langkah 6 / references | Tulis ulang dengan cara sendiri: bandingkan total biaya (efektif + provisi/admin/penalti) lama vs baru. |
| T-7 | Rendah | Label pos salah (`1jt:hiburan`) → galat menyalahkan angka, bukan label; angka negatif tanpa `=` → pesan argparse Inggris. | parser `--pos`, argparse | Pesan "label harus wajib/sosial/keinginan/tabungan"; tangkap argumen berawalan `-` yang berupa angka. |
| T-8 | Info | Minimum kartu kredit 5% dari tagihan dimodelkan sebagai nominal tetap. Dampak kecil bila anggaran tetap (uji: Rp90). | SKILL.md Batasan | Sebutkan asumsi ini di Batasan. |
| T-9 | Info | Catatan 50/30/20 "Wajar untuk keluarga dengan tanggungan..." muncul juga untuk pengguna lajang. | `anggaran` catatan | Kalimat netral. |

Tidak ditemukan bug perhitungan. Tidak ditemukan pola berbahaya (script tanpa jaringan/berkas), tidak ada rekomendasi produk investasi, disclaimer & tanggal cek aturan lengkap.

## 5. Skor kualitas: **8/10**
Alasan:
- (+) Semua angka tepat sampai rupiah: 60 kasus utang acak + 40 flat + 40 target + kasus tepi identik dengan simulasi independen; parser Rupiah gaya Indonesia kuat; tanpa traceback.
- (+) Uji A/B: dengan skill **jelas lebih baik** — tanpa skill bunga KTA flat membuat total bunga meleset −37% dan tidak ada pagar OJK/BI.
- (+) Banding pesaing: **unggul** atas openaccountant & joellewis (keduanya −37%, konteks AS, joellewis menyiratkan investasi saham).
- (+) Lokalisasi kuat (THR ÷ 12, kiriman ortu, arisan, zakat opsional, e-wallet, pinjol/paylater), penanganan input kurang & di luar cakupan baik, fakta regulasi terkini benar.
- (−) T-1: jebakan satuan bunga flat per bulan di `konversi-flat` bisa menghasilkan angka salah besar secara diam-diam — justru pada kasus yang menjadi nilai jual utama skill.
- (−) Beberapa kekurangan kenyamanan (T-2–T-7) dan belum ada pembanding take over/konsolidasi.

**Rekomendasi:** layak naik status ke `lulus` setelah **T-1 diperbaiki** (+ tes regresi); T-2–T-9 boleh menyusul. Isi `platform_teruji` = `claude-code (simulasi agent)`.
