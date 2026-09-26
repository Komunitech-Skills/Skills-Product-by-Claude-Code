---
name: analisis-rasio-keuangan-usaha
description: Menghitung dan menafsirkan rasio keuangan UMKM dari neraca + laba rugi sederhana (SAK EMKM, output laporan-keuangan-emkm, tabel CSV/tempel, atau angka diketik) — likuiditas (current, quick, kas), profitabilitas (margin kotor/bersih, ROA, ROE), solvabilitas (DER, DAR, cakupan bunga), aktivitas (umur stok, lama piutang, siklus kas), tren antarperiode, kesiapan angka untuk KUR/kredit, dengan ambang wajar per jenis usaha (dagang, jasa, produksi) dan saran tindakan dalam bahasa awam. Gunakan saat pengguna tanya "usaha saya sehat nggak", "cek rasio keuangan", "analisis laporan keuangan", "layak ajukan KUR dari sisi angka?" (financial ratio analysis, financial health check for small business). Bukan untuk menyusun laporan dari buku kas (laporan-keuangan-emkm) atau simulasi cicilan (pengajuan-kur).
---

# Analisis Rasio Keuangan Usaha

## Tujuan
Membaca laporan keuangan usaha kecil lalu menjawab pertanyaan pemilik dengan angka pasti: **sanggup bayar tagihan? cukup untung? terlalu banyak utang? stok & piutang lambat?** Semua rasio dinilai terhadap ambang wajar sesuai jenis usahanya dan diberi saran tindakan konkret. Semua angka dihitung script (Decimal), bukan dikira-kira.

## Kapan digunakan
- "Ini neraca & laba rugi toko saya, sehat nggak?" / "cek rasio keuangan usaha saya"
- Setelah skill `laporan-keuangan-emkm` membuat laporan: "sekarang analisis ya"
- Membandingkan dua tahun/bulan: "tahun ini lebih baik atau lebih buruk?"
- Sebelum ke bank: "dari angka, usaha saya layak ajukan KUR nggak?"

## Kapan TIDAK digunakan
- Belum punya neraca/laba rugi, hanya buku kas → susun dulu dengan `laporan-keuangan-emkm`. Bila datanya masih di buku kas harian, pakai `kas-umkm` (ekspor `--format emkm`), lalu kembali ke sini.
- Simulasi cicilan, syarat & dokumen KUR → `pengajuan-kur` (skill ini hanya membaca kesiapan dari sisi angka).
- Proyeksi kas ke depan → `arus-kas-13minggu`. HPP/harga per produk → `hitung-hpp`. Olah data penjualan mentah/Excel → `analisis-excel`.
- Menilai saham, reksa dana, kripto, valuasi (P/E, DCF), atau memberi rekomendasi investasi → tolak dengan sopan. Skill ini bukan nasihat investasi.
- Mengubah/"memoles" angka agar rasio terlihat bagus untuk bank → tolak (bisa masuk pemalsuan data kredit). Tawarkan analisis jujur + saran perbaikan nyata.
- PT besar/perusahaan terbuka yang butuh analisis audit → sarankan akuntan publik.

## Input
| Info | Wajib? | Default |
|---|---|---|
| Penjualan, laba bersih | Ya | — (tanyakan) |
| Kas, piutang, persediaan, aset tetap (atau total aset) | Ya untuk likuiditas/ROA | Pos rincian yang kosong = Rp 0 (ditulis di Asumsi) |
| Utang lancar (≤ 12 bulan) & utang jangka panjang, modal | Ya untuk solvabilitas | Modal = aset − utang bila tidak diisi |
| HPP | Untuk margin kotor & umur stok | Tidak dihitung |
| Jenis usaha: dagang / jasa / produksi (kuliner & katering termasuk produksi) | Tidak | `umum`. Sebaiknya agent memetakan sendiri lalu mengirim `--jenis dagang\|jasa\|manufaktur` |
| Panjang periode (bulan) | Tidak | 12 bulan. EMKM JSON: dari tanggal |
| Laporan periode sebelumnya | Tidak | Tanpa tren |
| Total cicilan pinjaman per bulan (lama + rencana) | Tidak | Kemampuan cicilan tidak dinilai |
| Beban bunga, penjualan tempo, utang bank yang jatuh tempo ≤ 12 bulan | Tidak | — |

Bila data wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor):
1. Penjualan, HPP (modal barang terjual), dan laba bersih periode ini? Periodenya berapa bulan?
2. Di akhir periode: uang kas + bank, piutang pelanggan, nilai stok, nilai peralatan/kendaraan?
3. Utang: ke pemasok, ke bank (berapa pokok yang dibayar 12 bulan ke depan), lainnya? Modal pemilik?
4. Jenis usahanya: dagang, jasa, atau produksi/kuliner?
5. Ada angka tahun/bulan lalu untuk dibandingkan? Berencana pinjam? Cicilan per bulan berapa?

Tawarkan `templates/isian-rasio.csv` bila pengguna lebih suka mengisi tabel. Jika ingin cepat, jalankan dengan angka yang ada. Rasio yang datanya kurang otomatis ditulis "tidak dihitung".

## Langkah kerja
1. **Siapkan data** apa adanya (jangan mengetik ulang atau mengubah angka):
   - Output `laporan_emkm.py --format json` → langsung dipakai (bisa beberapa file = beberapa periode).
   - Tabel dari chat/Excel → simpan ke `data.csv` atau `.md`. Kolom 1 = nama pos, kolom berikutnya = periode (lama → baru). Pemisah `;`, `,`, tab, atau tabel `|`. Bila pemisahnya koma, angka ribuan wajib dikutip (`Kas,"1,250,000"`) atau ditulis `Kas;1.250.000`. Tanpa itu script menolak dengan GALAT, tidak menebak angkanya.
   - Angka yang diketik → pakai opsi `--penjualan`, `--kas`, dst.
   - File .xlsx/PDF → minta disimpan sebagai CSV atau ditempel.
2. **Jalankan script** (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/rasio.py data.csv --jenis dagang --nama-usaha "Toko Berkah" --cicilan-bulanan 500rb
   python3 <folder-skill-ini>/scripts/rasio.py --jenis jasa --penjualan 216jt --hpp 71jt --laba-bersih 23,7jt \
     --kas 4jt --piutang 9jt --persediaan 3jt --aset-tetap 75jt --utang-usaha 6jt --utang-lancar-lain 12jt \
     --utang-jangka-panjang 35jt --modal 38jt --bulan 12
   python3 <folder-skill-ini>/scripts/rasio.py laporan-jan.json laporan-feb.json --jenis katering --bagian-lancar-utang-bank 4jt
   ```
   - Nominal boleh format Indonesia: `Rp 1.500.000`, `1,5jt`, `150rb`, `(8.000.000)` = negatif, `1,2 M` = miliar. Angka negatif lewat opsi: `--modal -4jt` atau `--modal=-4jt`.
   - Opsi lain: `--penjualan-kredit`, `--beban-bunga`, `--laba-usaha`, `--persediaan-awal`, `--piutang-awal`, `--total-aset`, `--total-utang`, `--utang-lancar`, `--hari`. Opsi yang diberikan bersama file berlaku untuk **periode terakhir**.
   - Dari EMKM, utang bank dianggap utang lancar seluruhnya (konservatif). Tanyakan pokok yang jatuh tempo 12 bulan ke depan lalu isi `--bagian-lancar-utang-bank`.
   - `--format json` untuk angka mentah. Default teks Markdown siap tempel.
3. **Baca "Perlu dicek"** (angka tak terbaca, mustahil, neraca tidak seimbang, baris tak dikenal). Tanyakan dalam satu pesan, lalu jalankan ulang. Selama status data SEMENTARA, sebut hasilnya sementara. Bila status **DATA BELUM CUKUP** (kurang dari 5 rasio bisa dinilai), jangan menyimpulkan usaha "sehat". Sampaikan pos yang belum ada (saran "Lengkapi data") dan ajukan pertanyaan di bagian Input.
4. **Sajikan hasil** dengan format di bawah. Semua angka, status, dan persen **dari output script**. Boleh menyederhanakan kalimat "Artinya", tetapi tidak boleh mengubah angka atau status.
5. **Kesiapan KUR:** sampaikan kesimpulan + poin ✓/⚠/✗ apa adanya. Jika pengguna ingin lanjut mengajukan, arahkan ke `pengajuan-kur` (simulasi cicilan, checklist dokumen). Tegaskan: bank yang memutuskan.
6. Periksa checklist, lalu kirim. Tawarkan: hitung ulang tiap bulan/kuartal, bandingkan dengan periode lalu, atau versi ringkas untuk dilampirkan ke proposal.

### Fallback tanpa Python
Beri tahu pengguna bahwa hasil dihitung manual (belum diverifikasi script). Ikuti rumus dan aturan pembagian nol/negatif di `references/ambang-wajar.md` bagian 3. Hitung dengan angka penuh, lalu bulatkan hanya di tampilan.

## Format output
```
# Analisis Rasio Keuangan — <Nama Usaha>
Jenis usaha · periode · status data LENGKAP/SEMENTARA
## Ringkasan untuk pemilik        ← 3–5 kalimat awam: untung/rugi, jumlah rasio baik/waspada/bahaya, yang paling mendesak
## Likuiditas / Profitabilitas / Solvabilitas / Aktivitas   ← tabel: Rasio | Nilai | Rumus | Wajar | Status 🟢🟡🔴 | Artinya
## Tren antarperiode              ← bila > 1 periode: membaik/memburuk per rasio (basis SAMA: saldo akhir tiap periode), pertumbuhan penjualan & laba
## Kesiapan pengajuan KUR/kredit  ← kesimpulan + ✓/⚠/✗ + rasio cicilan (bila diisi)
## Saran tindakan (urut prioritas)← maks. 5, konkret
## Perlu dicek · Asumsi
Disclaimer: bukan nasihat investasi/kredit, bukan audit; ambang = pedoman praktis, bukan standar OJK/bank.
```

## Contoh
**Input:** "Toko sembako saya setahun: omzet 480 juta, HPP 408 juta, laba bersih 24 juta. Kas 12 jt, piutang 6 jt, stok 40 jt, peralatan 42 jt. Utang supplier 20 jt, utang lain 5 jt, pinjaman bank jangka panjang 15 jt, modal 60 jt. Mau ambil KUR cicilan 500 ribu/bulan, aman?"

**Output (dipotong, lengkap di `examples/01-toko-sembako-normal.md`):**
```
Pada periode ini, usaha UNTUNG Rp 24.000.000 (5,0% dari penjualan). Dari 11 rasio yang dinilai terhadap ambang
usaha dagang: 10 baik, 1 waspada, 0 bahaya. Perlu diperhatikan: Umur stok 35,8 hari.
| Rasio lancar (current ratio) | 2,32x | ... | 🟢 Baik | Setiap Rp 1 utang jangka pendek dijamin Rp 2,32 aset lancar. |
| Umur stok (hari) | 35,8 hari | ... | 🟡 Waspada | Barang rata-rata diam di gudang/rak ±36 hari sebelum terjual. |
- ✓ Cicilan Rp 500.000/bulan = 25,0% dari laba bersih per bulan Rp 2.000.000 → 🟢 AMAN.
```

**Input tidak lengkap:** "usaha saya sehat nggak? omzet 20 juta sebulan" → ajukan 5 pertanyaan di atas dalam satu pesan, dan tawarkan template.

## Checklist sebelum mengirim
- [ ] Semua angka dari output script (atau hitung manual yang ditandai jelas).
- [ ] Rasio "tidak dihitung" ditampilkan beserta alasannya, bukan diganti 0 atau ditebak.
- [ ] Jenis usaha & sifat ambang (pedoman praktis, bukan standar resmi) disebut.
- [ ] Peringatan (angka mustahil, neraca tidak seimbang, SEMENTARA) disampaikan.
- [ ] Kesiapan KUR disebut sebagai pembacaan angka, **bukan** keputusan bank; tidak menjanjikan kredit cair.
- [ ] Disclaimer ada. Tidak ada rekomendasi investasi.

## Batasan & penanganan error
- Uji regresi: `python3 <folder-skill-ini>/tests/uji_regresi.py` (harus "SEMUA UJI LULUS").
- Script keluar kode 2 dengan pesan `GALAT: ...` untuk file kosong, tidak ada, Excel/PDF/biner, JSON rusak, jenis usaha tak dikenal, atau tidak ada angka yang terbaca. Sampaikan pesan itu beserta cara memperbaikinya.
- Pembagi nol → "tidak dihitung" + alasan. Modal ≤ 0 → ROE/DER tidak bermakna (bahaya). Aset/utang negatif → mustahil, rasio terkait tidak dihitung. Baris tabel tak dikenal dilewati dan dilaporkan.
- Tabel utama periode terakhir memakai rata-rata saldo awal-akhir bila tersedia. Tabel tren memakai saldo akhir untuk semua periode agar sebanding, dan basis ini ditulis di output. Jangan membandingkan angka tabel utama dengan kolom tren periode sebelumnya.
- Rasio disetahunkan dari periode < 3 bulan diberi catatan musiman (informasi, tidak membuat status SEMENTARA). ROA/ROE > 100% diberi catatan (aset/modal tercatat kecil).
- Kualitas hasil bergantung pada laporan sumber. Skill ini tidak memeriksa kebenaran transaksi dan tidak menggantikan akuntan.
- Ambang wajar & sumbernya: `references/ambang-wajar.md` (dicek 2026-09-26). Data diproses lokal; jangan dikirim ke layanan lain.
