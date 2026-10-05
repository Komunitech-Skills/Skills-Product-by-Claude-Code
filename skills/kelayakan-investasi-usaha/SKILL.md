---
name: kelayakan-investasi-usaha
description: Menilai layak/tidaknya rencana investasi usaha kecil-menengah (beli mesin, buka cabang, renovasi, beli kendaraan/mobil box, alat produksi) dengan angka pasti dari script - balik modal (payback biasa & terdiskonto), NPV, IRR, profitability index, BEP omzet tahunan, nilai sisa garis lurus, pajak sebagai persen (PPh final 0,5% / PPh badan), dan uji sensitivitas omzet turun 10-20% / biaya naik 10% - lalu kesimpulan layak / kurang layak / tidak layak beserta syaratnya. Gunakan saat pengguna tanya "layak nggak beli mesin ini", "kapan balik modal", "buka cabang untung nggak", "hitung NPV/IRR", kelayakan investasi, studi kelayakan sederhana, capital budgeting, investment feasibility, payback period. Bukan untuk cicilan/KUR (pengajuan-kur), saham/kripto/reksa dana, atau janji pasti untung.
---

# Kelayakan Investasi Usaha

> **Aturan balasan (Telegram/chat):** hasil ditulis UTUH di chat (kesimpulan, tabel, syarat, asumsi). Tabel maks. 3 kolom. Jangan menyebut kata proses (script, file, path, folder, cek, JSON, LULUS/GAGAL, "menjalankan") dan jangan menempel teks berlabel "UNTUK AGENT SAJA" apa adanya. Tidak ada fakta karangan: angka hanya dari pengguna atau hasil hitungan; harga pasar, omzet pesaing, atau "rata-rata industri" tidak dikarang.

> **Aturan kerja:** Jangan menginstal paket/aplikasi; jangan membuka atau mencari file selain yang diberikan pengguna dan isi folder skill ini; jangan menulis file baru tanpa diminta (bila diminta, sebut lokasinya, bukan /tmp).

## Aturan "kerjakan dulu, tanya di akhir" (utama)
Bila pengguna sudah menyebut **nilai investasi** dan **minimal satu angka hasil** (tambahan omzet, laba, penghematan, atau arus kas), jangan membalas hanya dengan pertanyaan. Dalam satu balasan:
1. Hitung dengan default yang masuk akal (tabel Input) dan **sebut asumsinya**.
2. Tulis hasil lengkap (format di bawah) dengan kesimpulan **layak / kurang layak / tidak layak**.
3. Di akhir, **maks. 3 pertanyaan** yang paling mengubah hasil (mis. "berapa persen bahan baku dari omzet?", "berapa perkiraan harga jual kembali?"), dan tawarkan hitung ulang.
Bila hanya nilai investasi yang ada (tanpa angka hasil): hitung **uang bersih minimal** per bulan agar layak (`--cari-minimal`), sampaikan, lalu tanya maks. 3 hal.

## Tujuan
Membantu pemilik usaha memutuskan investasi dengan angka, bukan perasaan: berapa lama balik modal, apakah hasilnya mengalahkan bunga pinjaman/hasil minimal yang diharapkan, dan seberapa aman bila omzet meleset. Semua angka dihitung script (Decimal), bukan dikira.

## Kapan digunakan
- "Mau beli mesin espresso 45 juta, tambahan jualan 6 juta sebulan. Layak nggak?"
- "Buka cabang modal 250 juta, kapan balik modal?" / "Hitung NPV dan IRR rencana ini."
- "Beli mobil box 180 juta atau tetap sewa ekspedisi 6,5 juta sebulan?" (investasi penghematan)
- Membandingkan dua pilihan alat/lokasi: jalankan masing-masing, bandingkan NPV & balik modal.

## Kapan TIDAK digunakan
- Cicilan, bunga flat vs efektif, syarat & dokumen KUR → `pengajuan-kur` (boleh dipakai bersama: biaya bunga tidak dimasukkan sebagai arus kas di sini karena sudah diwakili tingkat diskonto).
- Kesehatan keuangan dari neraca/laba rugi → `analisis-rasio-keuangan-usaha`. HPP per produk → `hitung-hpp`. Proyeksi kas mingguan → `arus-kas-13minggu`.
- Saham, kripto, reksa dana, emas, properti untuk spekulasi, valuasi perusahaan, atau "taruh uang di mana" → tolak sopan: skill ini menilai investasi **di usaha sendiri**; sarankan penasihat keuangan berizin OJK.
- "Pasti untung berapa?" / minta jaminan → jelaskan tidak ada kepastian; tawarkan skenario (dasar, omzet −10%, −20%) dan batas aman.
- Memoles angka agar terlihat layak untuk bank/investor → tolak; tawarkan hitungan jujur + syarat agar layak.

## Input
| Info | Wajib? | Default bila tidak disebut |
|---|---|---|
| Nilai investasi awal (harga alat + pasang + renovasi + modal awal) | Ya | — (tanya) |
| Tambahan omzet per bulan/tahun, atau uang bersih/penghematan | Ya | — (tanpa ini: `--cari-minimal`) |
| Biaya variabel (bahan baku, kemasan, komisi) | Tidak | Semua biaya dianggap tetap (hati-hati) — sebut asumsi |
| Biaya tetap tambahan (gaji, sewa, listrik, servis, BBM) | Tidak | Rp0 — sebut asumsi dan tanyakan di akhir |
| Masa proyek | Tidak | 5 tahun |
| Umur ekonomis & nilai jual kembali | Tidak | Umur = masa proyek, nilai sisa garis lurus (residu Rp0); kendaraan: umur 8 tahun (asumsi, bisa diubah) |
| Tingkat diskonto | Tidak | **12%/tahun** = bunga KUR 6% efektif (acuan Permenko 1/2026, sektor produksi) + tambahan risiko usaha 6%. Ini **asumsi**, bukan rekomendasi; pakai bunga pinjaman pengguna bila modal dari pinjaman |
| Pajak | Tidak | Tidak dihitung, tetapi disebut. Pengguna menyebut PPh final UMKM → `--pajak-persen 0,5` (dari omzet). Badan usaha (PPh badan) → `--pajak-persen 22 --dasar-pajak laba` |
| Pertumbuhan omzet/biaya | Tidak | 0% (sebut) |

## Langkah kerja

> **Lokasi script:** `scripts/kelayakan.py` di folder yang sama dengan SKILL.md ini. Jalankan dari sana (Windows: `python` atau `py`); jangan mencari file ke seluruh disk.

1. **Petakan kata pengguna ke angka.** Tulis untuk diri sendiri: investasi, omzet, biaya variabel (%), biaya tetap, masa, nilai sisa, pajak. Angka "/bulan" boleh langsung ditulis `6jt/bulan` (script mengalikan 12). Pisahkan:
   - **Biaya variabel** = ikut naik-turun dengan omzet (bahan baku, kemasan, komisi ojol) → `--hpp-persen 40` atau `--biaya-variabel 28,8jt`.
   - **Biaya tetap** = tetap walau sepi (gaji, sewa, listrik dasar, servis, asuransi) → `--biaya`.
   - **Investasi penghematan** (beli mobil vs sewa, beli mesin vs maklon): penghematan → `--omzet`, biaya operasional alat → `--biaya`. Jangan pakai pajak dari omzet untuk penghematan (penghematan bukan omzet; PPh final tidak bertambah). Di balasan, sebut "penghematan", bukan "omzet".
   - Sudah tahu uang bersih per tahun (laba + penyusutan) → `--arus-kas "40jt;55jt;60jt"` (atau satu angka + `--tahun`).
   - Bunga/cicilan pinjaman **tidak** dimasukkan ke biaya (sudah diwakili tingkat diskonto). Bila pengguna ingin melihat cicilan, rujuk `pengajuan-kur`.
2. **Jalankan script:**
   ```bash
   python3 scripts/kelayakan.py --investasi 45jt --omzet 6jt/bulan --hpp-persen 40 --biaya 1,2jt/bulan \
     --tahun 5 --nilai-residu 5jt --pajak-persen 0,5 --format teks
   python3 scripts/kelayakan.py --investasi 250jt --omzet "380jt;470jt;500jt;520jt;540jt" --hpp-persen 45 \
     --biaya 14,5jt/bulan --kenaikan-biaya 5 --nilai-sisa 40jt --pajak-persen 0,5 --format teks
   python3 scripts/kelayakan.py --investasi 85jt --cari-minimal --format teks      # belum ada angka hasil
   ```
   Opsi lain: `--diskonto 10`, `--umur-ekonomis 8`, `--nilai-residu 20jt`, `--nilai-sisa 90jt` (perkiraan harga jual kembali, mengalahkan garis lurus), `--kenaikan-omzet 5`, `--dasar-pajak laba`, `--sensitivitas "omzet-15;biaya+20"`. Tanpa `--format teks` keluarannya JSON lengkap (tabel per tahun di `tabel_arus_kas`).
3. **Baca hasil**: `kesimpulan.status` (LAYAK / KURANG LAYAK / TIDAK LAYAK), `alasan`, `syarat`, `asumsi`, `peringatan`. Status ditentukan script; jangan diubah. Aturannya: NPV < 0 → tidak layak; NPV ≥ 0 tetapi negatif saat omzet −10% atau biaya +10%, atau bergantung pada nilai jual kembali → kurang layak; selain itu layak.
4. **Script keluar kode 2** (pesan `error` + `saran`): angka tidak terbaca, investasi ≤ 0, masa di luar 1–30 tahun, daftar per tahun tidak sama panjang, dll. Perbaiki sendiri bila jelas (mis. `45,000` → `45rb`), atau tanyakan ke pengguna dengan bahasa awam.
5. **Tulis balasan** dengan format di bawah, istilah awam (lihat `references/istilah-dan-asumsi.md`), lalu periksa checklist.

**Fallback tanpa Python** (sebut "dihitung manual, mohon dicek"): arus kas tahunan = omzet − biaya variabel − biaya tetap − pajak. NPV = −investasi + Σ arus kas_t ÷ (1 + r)^t (+ nilai sisa di tahun terakhir). Balik modal = tahun sebelum kumulatif ≥ 0 + sisa ÷ arus kas tahun itu. Penyusutan = (investasi − residu) ÷ umur. Uang bersih minimal per tahun = investasi × r ÷ (1 − (1 + r)^−n). IRR tanpa script: sebut "tidak dihitung".

## Format output (chat)
```
**[Nama rencana]: [LAYAK / KURANG LAYAK / TIDAK LAYAK] (dengan asumsi di bawah)**
[1–2 kalimat alasan utama dengan angka: balik modal ..., hasil per tahun ...% vs patokan 12%.]

| Ukuran | Hasil | Arti |
|---|---|---|
| Balik modal | 1 tahun 7 bulan | modal kembali dari uang bersih |
| Balik modal (nilai waktu uang) | 1 tahun 10 bulan | memperhitungkan patokan 12%/th |
| NPV | Rp60.356.969 | untung bersih setara uang hari ini, di atas patokan |
| IRR | 57,3%/tahun | imbal hasil per tahun; layak bila > 12% |
| PI | 2,34 | tiap Rp1 modal kembali Rp2,34 (nilai kini) |
| Omzet impas | Rp3.137.255/bulan | di bawah ini rugi secara pembukuan |

**Kalau meleset** (NPV): omzet −10% → Rp...; omzet −20% → Rp...; biaya +10% → Rp...
**Syarat agar tetap layak:** omzet tidak turun > ...%; biaya tidak naik > ...%; omzet minimal ±Rp.../bulan.
**Arus kas per tahun** (opsional bila diminta "rinci"): tabel Tahun | Uang bersih | Kumulatif.
**Asumsi:** diskonto 12% (bunga KUR 6% + risiko 6%, bisa diganti), masa ... tahun, nilai sisa ..., pajak ....
Catatan: bukan nasihat keuangan; hasil tergantung asumsi, tidak ada jaminan untung.
[Maks. 3 pertanyaan untuk mempertajam hitungan + tawaran hitung ulang.]
```
- KURANG LAYAK/TIDAK LAYAK: tulis jelas apa yang perlu berubah (dari `syarat`: omzet minimal, kenaikan yang diperlukan, tekan investasi/biaya, beli bekas/sewa dulu). Jangan melunakkan kesimpulan.
- Nominal ditulis `Rp60.356.969` (titik ribuan); persen dengan koma (`57,3%`). Angka dari hasil hitungan, tidak dibulatkan ulang kecuali menulis "±".
- Pajak tidak dihitung → tetap tulis satu baris: "Pajak belum dihitung; bila memakai PPh final UMKM 0,5% dari omzet atau PPh badan, hasil sedikit turun — bisa saya hitungkan."

## Contoh
**Input:** "Kafe saya mau beli mesin espresso 45 juta. Tambahan jualan kira-kira 6 juta sebulan, bahan baku 40%, listrik+servis+part-time 1,2 juta sebulan. Mesin bekasnya mungkin laku 5 juta setelah 5 tahun. Saya bayar PPh final 0,5%. Layak nggak?"

**Output (ringkas):** **LAYAK** — balik modal 1 tahun 7 bulan (dengan nilai waktu uang 1 tahun 10 bulan); NPV Rp60.356.969; IRR 57,3%/tahun > patokan 12%; PI 2,34. Omzet impas Rp3.137.255/bulan; omzet minimal agar layak ±Rp3.654.956/bulan. Bila meleset: omzet −10% → NPV Rp44.914.108; −20% → Rp29.471.247; biaya +10% → Rp44.784.336 (tetap layak). Syarat: omzet tidak turun > 39,1%. Pertanyaan akhir: apakah 6 juta itu benar-benar penjualan **tambahan** (bukan pindahan dari menu lama)? Contoh lengkap: `examples/01`–`05`.

## Checklist sebelum mengirim
- [ ] Kesimpulan layak/kurang layak/tidak layak sesuai `kesimpulan.status`, dengan alasan berangka dan syarat.
- [ ] Semua angka dari hasil hitungan (atau fallback manual yang disebut); tidak ada angka pasar/industri karangan.
- [ ] Asumsi disebut: diskonto 12% + asal-usulnya (bisa diubah, bukan rekomendasi), masa, nilai sisa (garis lurus/perkiraan), pajak dihitung atau belum, biaya dianggap tetap bila tidak dipisah.
- [ ] Sensitivitas omzet −10%, −20%, biaya +10% ditampilkan.
- [ ] Tabel ≤ 3 kolom; tidak ada kata proses/file/path; label "UNTUK AGENT SAJA" tidak dikutip.
- [ ] Disclaimer satu baris: bukan nasihat keuangan, tergantung asumsi, tanpa jaminan untung.
- [ ] Pertanyaan maks. 3, di akhir.

## Batasan & penanganan error
- Model tahunan sederhana: arus kas dianggap masuk di akhir tiap tahun; inflasi hanya lewat `--kenaikan-*`; modal kerja yang kembali di akhir masukkan ke `--nilai-sisa`; laba/rugi penjualan aset bekas tidak dikenai pajak; rugi tidak dikompensasikan ke tahun berikutnya.
- PPh final 0,5% (PP 55/2022) hanya untuk omzet ≤ Rp4,8 miliar/tahun dan berbatas waktu; orang pribadi punya omzet tidak kena pajak s.d. Rp500 juta/tahun dari **seluruh** usaha — script tidak tahu omzet usaha lain, jadi pajak bisa lebih kecil dari hitungan. Aturan bisa berubah: sarankan cek ke DJP/konsultan pajak.
- IRR bisa lebih dari satu bila arus kas berganti tanda beberapa kali (mis. ada overhaul besar) → script memberi peringatan; pakai NPV sebagai patokan.
- Omzet dari pengguna adalah perkiraan. Bila terdengar terlalu optimis (mis. omzet cabang baru langsung sama dengan cabang lama), sebut risikonya dan tunjukkan skenario turun; jangan mengganti angkanya diam-diam.
- Bukan nasihat keuangan/investasi; untuk investasi besar (≥ ratusan juta) atau keputusan pinjaman, sarankan diskusi dengan konsultan keuangan atau bank.
