# Hasil Uji Ulang: uji-pasar-produk-cepat v1.0.1

- Penguji: agent independen kedua (bukan pembuat, bukan penguji pertama). Hanya membaca folder skill + CLAUDE.md. Tanggal: 2026-09-29.
- Platform: `claude-code (simulasi agent)`. Belum diuji di OpenClaw/Codex/Cursor asli.
- `python3 scripts/validate.py --skill uji-pasar-produk-cepat` → ✅ "1 skill valid". `python3 tests/uji_hasil_eksperimen.py` → "Semua uji lolos."
- Hitungan pembanding ditulis sendiri oleh penguji di scratchpad (`verif.py`), tanpa memakai kode skill: Fisher dua sisi dengan `Fraction` + faktorial eksak; ukuran sampel = n terkecil yang power normalnya ≥ 0,80 (`statistics.NormalDist`, varians gabungan di H0, varians terpisah di H1).

## 1. Verifikasi perbaikan B1-B8

| ID | Cek penguji | Hasil |
|---|---|---|
| B1 | `banding 0/10 vs 4/10`: script p Fisher **0,0867**, "ada kecenderungan, tapi BELUM meyakinkan". Hitungan independen: **0,0867**. `0/20 vs 5/20`: script 0,0471 vs independen 0,0471, pesan "ada tanda ... tapi sampel terlalu kecil untuk yakin" (bukan pemenang). `9/60 vs 15/60`: independen 0,2536 (script tetap pakai uji z karena n ≥ 50 dan sel harapan ≥ 5, p 0,1709, "BELUM meyakinkan"). | ✅ |
| B2 | `sampel --banding`: 5/10 = 435, 10/20 = **199**, 15/25 = **250**, 10/15 = **686**, 20/25 = **1.094** per varian. Independen: sama persis; power di n-1 = 0,7996 / 0,7981 / 0,7984 / 0,7997 / 0,7997 (< 0,80), jadi n minimum tepat. Angka "150-300" dan "100-150" sudah tidak ada di SKILL/references; kalimat "SEBANYAK itu untuk TIAP varian" sudah dihapus dari script (hanya tersisa di rekaman uji lama `05-...`, memang sengaja). | ✅ |
| B3 | `sampel --margin 10 --perkiraan 5` → 19 orang + PERINGATAN margin ≥ perkiraan (saran `--margin 2,5`) + PERINGATAN < 30 orang. `--margin 60` → 3 orang + dua peringatan. SKILL kini memakai contoh `--margin 5` dan aturan "margin ≈ separuh ambang". | ✅ |
| B4 | `--target 1.250`, `2.500`, `1,250,000` ditolak dengan pesan jelas (exit 2); `1,25` diterima sebagai 1,25%. | ✅ |
| B5 | `--batas-stop 8` tanpa `--target` → PERINGATAN eksplisit, tanpa keputusan. | ✅ |
| B6 | Label "LANJUT BERTAHAP" seragam di script, SKILL, references, README, contoh 00/01/02. `hasil 10/12 target 15` → "LANJUT BERTAHAP (sampel kecil)", bukan "kuat". | ✅ |
| B7 | Tafsir "dengan data ini, angka sebenarnya kemungkinan besar ada di antara ..." dan "selisih sebesar ini jarang muncul hanya karena kebetulan"; SKILL melarang menyebut p-value sebagai peluang benar. | ✅ |
| B8 | Langkah 6 mewajibkan "target pembeli ÷ konversi", dihitung dengan konversi tengah dan batas bawah (contoh 343/561 orang, benar: 60/0,175 = 342,9 → 343; 60/0,107 = 560,7 → 561). | ✅ |

Semua 8 perbaikan terverifikasi.

## 2. Skenario uji ulang

### R1 — Normal (baru): uji dua foto listing marketplace, konversi rendah
**Pengguna:** "Listing sambal roa di Shopee, 2 foto sampul bergantian seminggu. Foto A: 180 pengunjung, 3 pesanan. Foto B: 190 pengunjung, 11 pesanan. Target saya 3%. Pakai foto mana, lanjut stok?"

```
$ python3 scripts/hasil_eksperimen.py banding --a-ditawari 180 --a-aksi 3 --b-ditawari 190 --b-aksi 11
Varian A: 3/180 = 1,7% (rentang wajar 0,6% - 4,8%)
Varian B: 11/190 = 5,8% (rentang wajar 3,3% - 10,1%)
Selisih B - A: +4,1 poin persen
Nilai z = 2,08; p (uji z) = 0,0378
Artinya: selisih sebesar ini jarang muncul hanya karena kebetulan (p < 0,05). Varian B layak dipilih sebagai pemenang untuk kelompok pembeli seperti ini.
$ python3 scripts/hasil_eksperimen.py hasil --ditawari 190 --aksi 11 --target 3 --batas-stop 1,5
Konversi: 11 dari 190 orang = 5,8%
Rentang wajar 95% (Wilson): 3,3% sampai 10,1%
KEPUTUSAN: LANJUT (kuat): bahkan batas bawah rentang wajar sudah mencapai target.
$ python3 scripts/hasil_eksperimen.py sampel --banding --a 2 --b 6
... butuh sekitar 376 orang PER VARIAN (total 752).
```
Verifikasi independen: Wilson 11/190 = 3,26%-10,07% ✅; n per varian 2% vs 6% = 376 ✅; **Fisher tepat 3/180 vs 11/190 = 0,054** (script tidak menghitungnya karena sel harapan terkecil 6,8 ≥ 5 dan n ≥ 50).

Jawaban agent (mengikuti SKILL): foto B dipakai sebagai acuan; konversi B 5,8% (kemungkinan besar 3%-10%) sudah di atas target 3% → LANJUT; untuk 60 pesanan/bulan perlu ±1.037 pengunjung (60 ÷ 11/190) atau ±1.819 pada batas bawah 3,3% yang dibacakan script (±1.839 bila memakai batas bawah tak dibulatkan 3,26%); minggu dibedakan = kelompok belum tentu setara (hari/kampanye), jadi uji ulang dua foto bersamaan bila fitur tersedia. Asumsi berikutnya: ulasan/beli ulang, ongkir kirim botol kaca.
**Vonis: LULUS dengan catatan (N1).** Keputusan wajar, angka benar, tetapi kata "layak dipilih sebagai pemenang" terlalu tegas untuk total 14 pesanan: uji z tanpa koreksi kontinuitas memberi p 0,038, sedangkan Fisher 0,054.

### R2 — Data rusak
Semua ditolak dengan pesan jelas tanpa traceback (exit 2): `--target 150`, `--batas-stop 20 > --target 15`, `--ditawari -5`, `--ditawari abc`, `--target nan`, `--target 1,250,000`, `banding` aksi 60 > 50, `sampel --banding --a 15` (tanpa `--b`), `--a 15 --b 15`, `--a 0`, `sampel` tanpa argumen, `--margin 0`. Kasus batas yang tetap dijawab dengan benar: 0/50 vs 0/50 dan 30/30 vs 30/30 → p = 1, "belum ada bukti", ada peringatan sel kecil.
Kasus ekstrem: `banding 10/40 vs 40000/200000` butuh ±8 detik (Fisher dengan `math.comb` pada n besar), tetapi hasilnya benar dan tidak crash (N3).
**Vonis: LULUS.**

### R3 — Regresi skenario 1 penguji pertama (pre-order nastar 21/120, target 15%, "produksi 300?")
```
$ python3 scripts/hasil_eksperimen.py hasil --ditawari 120 --aksi 21 --target 15
Konversi: 21 dari 120 orang = 17,5%
Rentang wajar 95% (Wilson): 11,7% sampai 25,3%
Artinya: dengan data ini, angka sebenarnya kemungkinan besar ada di antara 12% dan 25%.
KEPUTUSAN: LANJUT BERTAHAP: angka mencapai target, tapi batas bawah rentang (11,7%) masih di bawah target. ...
```
Angka sama dengan v1.0.0 (Wilson 11,7%-25,3% ✅); label kini "LANJUT BERTAHAP" (dulu "LANJUT DENGAN CATATAN") dan tafsir B7 baru. Dengan Langkah 6 (B8), agent kini **wajib** menulis: 300 toples (anggap 1 toples/pembeli) ÷ 0,175 = 1.715 kontak (tengah), ÷ 0,117 = 2.565 kontak (hati-hati; 2.556 bila memakai batas bawah tak dibulatkan 11,74%), padahal kontak yang ada 120 → jangan 300, mulai batch kecil. Ini sebelumnya hanya dilakukan inisiatif penguji; sekarang bagian dari skill.
**Vonis: LULUS (tidak ada regresi, lebih baik dari v1.0.0).**

## 3. Temuan baru (tidak memblokir)
| ID | Tingkat | Temuan | Saran |
|---|---|---|---|
| N1 | Kecil-sedang | Pada konversi rendah dengan n ≥ 50 dan sel harapan sedikit di atas 5 (mis. 3/180 vs 11/190), script memakai uji z dan menyatakan "layak dipilih sebagai pemenang" (p 0,038), padahal Fisher tepat 0,054. Kasus ini umum di listing marketplace/landing page. | Pakai Fisher juga bila sel harapan < 10 atau total aksi < 20, atau selalu tampilkan Fisher dan ambil p yang lebih besar. |
| N2 | Kecil (tampilan) | Persen ditampilkan 1 desimal/0 desimal sehingga input tidak tampil apa adanya: `--target 1,25` tampil "1,2%" dan stop "0,6%"; `--margin 1,5` tampil "+-2%". Hitungan tetap memakai nilai asli. | Tampilkan hingga 2 desimal bila nilai input berdesimal. |
| N3 | Sangat kecil | Fisher lambat (±8 dtk) untuk varian sangat timpang dengan n ratusan ribu. Jarang di UMKM. | Opsional: hitung peluang dengan log-gamma. |

## 4. Skor
**8/10 — LULUS.** Naik dari 7/10.
- (+) Semua permintaan B1-B8 terpenuhi dan terverifikasi angka independen (Fisher 0,0867; n 199/250/686/1.094 cocok 100%, termasuk batas power di n-1).
- (+) Tidak ada lagi klaim pemenang pada sampel < 50 per varian; alat power/MDE menutup kekalahan terhadap pesaing; validasi input lengkap tanpa traceback; regresi S1 lebih baik.
- (−) N1: masih ada celah overclaim tipis di zona konversi rendah yang justru relevan untuk marketplace; N2 tampilan persen.
- Rekomendasi: boleh lanjut ke uji platform asli / `beta`; N1 dan N2 sebaiknya diperbaiki di v1.0.2 (tidak perlu uji ulang penuh, cukup tes tambahan).
