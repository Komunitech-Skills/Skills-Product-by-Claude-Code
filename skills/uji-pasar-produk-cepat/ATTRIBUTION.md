# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi dengan nilai tambah besar).** Kerangka proses dari dua koleksi skill publik bagi product manager software diadaptasi dan ditulis ulang untuk uji pasar UMKM/profesional Indonesia. Skill ini melengkapi `validasi-ide-produk-baru` (yang menangani hipotesis dan uji 7 hari pertama).

## Sumber
| Sumber | Skill yang dibaca | Lisensi | Commit / tanggal ambil |
|---|---|---|---|
| [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills) | `measure-experiment-design`, `iterate-pivot-decision` | Apache License 2.0 | `1cef1a9eae10017389863d51e289e0ae41e17fcb` (10 Sep 2026), diambil 2026-09-29 dengan `git clone --depth 1` |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) (Copyright (c) 2026 Pawel Huryn) | `pm-product-discovery/skills/identify-assumptions-new`, `brainstorm-experiments-new`, `prioritize-assumptions` | MIT | `8607e3b077817f89bf4a9b623246219734ac3be0` (14 Sep 2026), diambil 2026-09-29 |

Teks lisensi asli: [`LICENSE-APACHE`](LICENSE-APACHE) (root repo product-on-purpose) dan [`LICENSE-MIT`](LICENSE-MIT) (root repo phuryn), disalin utuh.

**NOTICE:** repo product-on-purpose/pm-skills tidak memiliki file `NOTICE` (dicek di root repo pada commit di atas), sehingga sesuai Apache-2.0 §4(d) tidak ada NOTICE yang perlu disertakan. Header atribusi sumber ("PM-Skills | https://github.com/product-on-purpose/pm-skills | Apache 2.0") dicatat di sini.

## Pernyataan perubahan (Apache-2.0 §4(b))
Seluruh materi telah **diubah**: tidak ada berkas sumber yang disalin apa adanya. Struktur langkah yang dipertahankan: (a) daftar asumsi berisiko dengan prioritas dampak x risiko (dari phuryn `identify-assumptions-new` / `prioritize-assumptions`, konsep Teresa Torres dan Impact x Risk); (b) hipotesis "sedikitnya X% dari Y akan melakukan Z" dan prinsip "aksi nyata lebih kuat dari opini" / pretotype (phuryn `brainstorm-experiments-new`, gagasan Alberto Savoia); (c) kriteria sukses ditetapkan sebelum uji dan pola desain eksperimen (product-on-purpose `measure-experiment-design`); (d) opsi persevere/pivot beserta bukti dan dokumen keputusan (product-on-purpose `iterate-pivot-decision`).

## Audit lisensi & keamanan (pedoman kurasi Komunitech)
- `LICENSE` kedua repo dicek langsung: Apache-2.0 dan MIT, mengizinkan modifikasi dan penjualan turunan dengan atribusi.
- Skill sumber yang dipakai dibaca penuh. Pencarian pola (perintah destruktif, `curl`, `eval`, base64, SSH/token, "ignore previous instructions") pada folder skill tersebut: **tidak ditemukan**. Skill sumber hanya berisi instruksi teks; tidak ada script yang dijalankan. Skrip CI/tooling repo sumber tidak disalin.
- Tidak ada API key/data pribadi tertanam.
- **Kesimpulan: lolos audit.**

## Nilai tambah (ATM)
Sumber ditujukan bagi tim produk software (A/B test dengan analitik, sample size statistik, dokumen pivot korporat). Versi ini menambahkan sendiri:
1. Menu 7 eksperimen UMKM Indonesia (pre-order WA, sistem PO, sampel bazar, landing page + WA, listing marketplace, konten TikTok, Google Form) dengan aturan kejujuran pre-order.
2. Daftar asumsi khusus usaha fisik (produksi/kirim, margin, izin PIRT/BPOM/halal) dan skor prioritas sederhana.
3. Kriteria sukses per eksperimen, ambang lanjut/stop, aturan jumlah sampel skala UMKM.
4. Script `scripts/hasil_eksperimen.py` (Python standar): konversi, interval Wilson 95%, uji z dua proporsi, ukuran sampel, peringatan sampel kecil, penolakan input rusak; `tests/uji_hasil_eksperimen.py` dengan angka hitung tangan.
5. Template log eksperimen, opsi pivot dengan contoh lokal, contoh kasus frozen food fiktif, dan panduan pembeli berbahasa awam.

## Pembagian lisensi
Bahan yang terinspirasi kerangka sumber tunduk pada Apache-2.0 / MIT sebagaimana dicatat di atas. Teks, script, contoh, dan template selebihnya adalah karya Komunitech. Skill ini tidak berafiliasi dengan, atau didukung oleh, product-on-purpose maupun Pawel Huryn. Penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.
