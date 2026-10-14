# Uji banding pesaing: bandingkan-pemasok-vendor vs anthropics `vendor-review`

- **Tanggal:** 2026-10-14 · **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Kata kunci yang dicari (catatan riset gelombang 29):** supplier comparison, vendor evaluation, vendor scorecard, procurement quote comparison, landed cost, bandingkan supplier. Sumber: skills.sh, ClawHub, Tessl, GitHub (WebSearch/WebFetch).
- **Pesaing terkuat:** `operations/skills/vendor-review` di [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins/tree/main/operations/skills/vendor-review) (Anthropic, Apache-2.0; repo ±29,6k bintang). SKILL.md diunduh dari raw.githubusercontent.com (HTTP 200, 3.170 byte) hanya untuk dinilai dan dipasang di home uji terpisah; **tidak disalin** ke skill Komunitech. Isinya kerangka umum: TCO (lisensi, implementasi, pelatihan, dukungan, biaya keluar), penilaian risiko High/Med/Low, matriks banding, putusan Proceed/Negotiate/Pass, poin negosiasi. Tanpa script, tanpa aturan PPN/ongkir/MOQ/termin.
- **Pesaing lain (dari catatan riset, tidak dijalankan):** mohitagw15856/pm-claude-skills `vendor-evaluation` (MIT, rubrik berbobot 1-5, tanpa hitungan harga); anthropics/cwc-workshops `supplier-selection` (Tessl; skor + MOQ/lead time per SKU, tanpa landed cost/PPN/termin, repo tidak dirawat).
- **Cara uji:** OpenClaw 2026.10.2 lokal, model router `claude-sonnet-5`, home berisi hanya `vendor-review`; pesan skenario 1 identik (3 balasan WA pemasok tepung, 600 kg, tenggat 5 hari). Pembanding: hasil SESUDAH skenario 1 di `00-openclaw-sebelum-sesudah.md`.

## Hasil pesaing (vendor-review)
Jejak alat: membaca SKILL.md `vendor-review`, mencoba mencari alat web untuk tarif PPN (tidak tersedia), lalu menjawab tanpa script.

> Sudah saya hitung total biaya all-in untuk 600 kg (termasuk diskon, ongkir, dan PPN kalau berlaku) — ini perbandingannya:
>
> | | Toko Tepung Sentosa | PT Mitra Pangan Jaya | CV Berkah Gandum |
> |---|---|---|---|
> | Harga dasar | Rp118rb/dus (10kg) → Rp11.800/kg | Rp11.200/kg (belum PPN) | Rp11.900/kg (franco, no PPN) |
> | Diskon | 5% (karena 60 dus > 50 dus) | - | - |
> | PPN | - (harga sudah final) | +11% → +Rp739.200 | - (non-PKP) |
> | Ongkir | +Rp100.000 | +Rp150.000 | sudah termasuk |
> | **Total 600 kg** | **Rp6.826.000** | **Rp7.609.200** | **Rp7.140.000** |
> | **Per kg** | **≈Rp11.377** | ≈Rp12.682 | ≈Rp11.900 |
> | Estimasi kirim | 2–3 hari ✅ aman | 3–4 hari ✅ aman | 5–7 hari ⚠️ bisa lewat deadline 5 hari |
> | Pembayaran | Cash pas barang datang (paling aman) | Tempo 30 hari (enak buat cashflow, tapi harus PKP/tagih faktur) | Transfer penuh di muka (risiko kalau barang telat/bermasalah) |
>
> **Rekomendasi: Toko Tepung Sentosa paling untung.**
>
> Alasannya kombo lengkap:
> 1. **Paling murah** — selisihnya lumayan, Rp314rb lebih murah dari Berkah Gandum dan Rp783rb lebih murah dari Mitra Pangan Jaya.
> 2. **Paling cepat** (2-3 hari) — paling aman buat deadline 5 hari ibu, karena stok lagi tipis.
> 3. **Pembayaran paling aman** — bayar pas barang sampai (COD), jadi nggak ada risiko transfer duluan terus barang telat/nggak dikirim.
>
> Soal CV Berkah Gandum: walau harganya nomor 2 termurah, dua hal bikin saya ragu — estimasi kirimnya "5-7 hari" sudah mepet bahkan bisa **lewat** deadline ibu, dan mereka minta transfer lunas duluan sebelum kirim. Kalau ternyata molor atau bermasalah, uang ibu nyangkut duluan.
>
> PT Mitra Pangan Jaya paling mahal walau harga/kg kelihatan paling murah di awal (11.200), karena PPN 11% bikin naik signifikan — kecuali toko ibu PKP dan bisa kreditkan pajak masukannya, PPN itu jadi biaya beneran, bukan sekadar administrasi. Tempo 30 hari-nya memang enak buat cashflow kalau ibu butuh modal kerja, tapi dari sisi untung murni, ini yang paling mahal.
>
> Satu hal yang perlu dicek manual: pastikan "protein sedang" dari Sentosa itu merek/kualitasnya cocok buat resep kue ibu — kadang toko kecil kualitasnya lebih variatif dibanding supplier PT/CV yang biasanya ambil dari pabrikan tertentu. Kalau kualitasnya oke, Sentosa jelas pemenangnya.

## Penilaian berdampingan (skenario 1)

| Kriteria | vendor-review (pesaing) | bandingkan-pemasok-vendor (kita) |
|---|---|---|
| Kebenaran angka | Benar: 6.826.000 / 7.609.200 / 7.140.000; selisih 314rb & 783rb (PPN Mitra tanpa ongkir, Rp739.200) | Benar: 6.826.000 / 7.625.700 / 7.140.000; +799.700 (11,7%) / +314.000 (4,6%) (PPN termasuk ongkir yang ditagih di invoice) - dihitung script |
| Jebakan PPN & status PKP | Menjelaskan PPN Mitra dan kredit pajak masukan; menganggap harga Sentosa "sudah final" tanpa dasar | Menandai status PKP Sentosa belum jelas + dampak Rp750.860 (total 7.576.860, tetap termurah tipis) |
| Tenggat, termin, MOQ | Tenggat & termin dibahas naratif | Skor tertimbang + Berkah otomatis tidak direkomendasikan (melewati tenggat); MOQ Mitra dicek |
| Hal siap pakai | Tidak ada pesan WA; format putusan & poin negosiasi milik skill pesaing tidak dipakai | 2 pesan WA siap kirim, daftar `[isian]`, asumsi, disclaimer |
| Skenario "kalau berubah" | Tidak ada | Jumlah 2x, termurah telat, bagi 70/30 (angka benar) |
| Kesalahan | Tidak ada salah angka | Satu kalimat sensitivitas salah subjek ("hemat Rp314.000" disematkan ke Mitra) |
| Bahasa awam | Sangat luwes, ringkas | Rapi tetapi padat (4.764 karakter) |
| **Skor** | **6,5** | **7,5** |

**Kesimpulan:** skill kita **unggul** (tidak kalah, jadi tidak ada batas skor 6), terutama pada tanda status PKP yang belum jelas, pesan WA, aturan tenggat, dan skenario "kalau berubah" yang dihitung, bukan dikira. Keunggulannya **belum telak**: hasil pesaing hampir sama dengan model dasar (pesaing tidak memberi banyak nilai tambah untuk barang/UMKM), sedangkan skill kita masih membuat kesalahan penyematan selisih di kalimat sensitivitas. Kelebihan pesaing yang patut dipelajari (ditulis ulang dengan cara sendiri, bukan disalin): jawaban yang lebih ringkas dan satu kalimat putusan tegas di awal.
