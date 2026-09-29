# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi)** dari skill publik berlisensi MIT, dengan nilai tambah besar untuk konteks Indonesia.

## Sumber yang diadaptasi
| Sumber | Pembuat | Lisensi | Snapshot |
|---|---|---|---|
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Pawel Huryn | MIT (c) 2026 Pawel Huryn | `git clone --depth 1`, commit 8607e3b0 (14 Sep 2026), dibaca 2026-09-29 |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Corey Haines | MIT (c) 2025 Corey Haines | `git clone --depth 1`, commit 5b2c0007 (4 Sep 2026), dibaca 2026-09-29 |

Bagian yang dipelajari (struktur/alur saja):
- pm-skills: `pm-market-research/skills/user-personas`, `market-segments`, `user-segmentation`; `pm-product-strategy/skills/value-proposition` (kerangka 6 bagian: siapa, mengapa, sebelum, cara, sesudah, alternatif); `pm-marketing-growth/skills/positioning-ideas`, `value-prop-statements`; `pm-go-to-market/skills/ideal-customer-profile`, `beachhead-segment` (dibaca, gagasan pemilihan segmen awal).
- marketingskills: `skills/product-marketing` (konteks pemasaran, pembeda, keberatan/anti-persona, Empat Gaya peralihan JTBD, bahasa pelanggan).
- Tidak dipakai: skill lain di kedua repo; tautan kursus/templat luar milik pembuat sumber tidak disalin.

## Audit keamanan (Tahap 3 CLAUDE.md)
- Seluruh `SKILL.md` yang diadaptasi dibaca penuh. Tidak ada folder `scripts/` pada skill sumber ini; tidak ada kode dari sumber yang dijalankan atau disalin.
- Pencarian pola berbahaya (curl/wget/eval/exec/base64, kredensial, `.env`, token, instruksi "abaikan") pada skill terpilih: tidak ditemukan. Tidak ada prompt injection tersembunyi, permintaan mengirim file, atau menonaktifkan konfirmasi. Skill sumber hanya berisi instruksi prompt dan tautan bacaan.
- Tidak ada API key/token/data pribadi tertanam.
- Kesimpulan: **lolos audit**. Sinyal kualitas sumber: bintang tinggi, dirawat aktif (commit terakhir September 2026), ada kontributor luar; pembuat individu (dicatat di `research/sources/`).

## Apa yang diubah/ditambahkan (file telah diubah dari sumber)
Sumber berbahasa Inggris, generik-global (SaaS/produk digital). Perubahan besar:
1. Ditulis ulang penuh dalam Bahasa Indonesia sehari-hari; kerangka persona, segmentasi, value proposition, dan positioning digabung menjadi satu alur STP + message house untuk UMKM.
2. Segmentasi memakai realitas konsumen Indonesia: kota besar vs kabupaten, daya beli sebagai rentang Rupiah, kanal WA/Shopee/Tokopedia/TikTok Shop/IG, kebiasaan bayar (COD/transfer/QRIS), musim (Ramadan, gajian, Harbolnas).
3. **Script Python baru** `scripts/skor_segmen.py` (matriks berbobot 7 kriteria, skala 0-100) dan `scripts/uji_skor_segmen.py` (uji regresi, termasuk data rusak); sumber tidak punya script.
4. Persona berupa kartu dengan penanda FAKTA/HIPOTESIS, anti-persona, wawancara WA 5 pertanyaan, dan aturan tidak memasukkan data pribadi.
5. Tabel pembeda vs pesaing dengan alternatif "cara lama", tagline 5 opsi + versi bio (karakter dihitung), teks siap tempel (bio, listing, caption, sapaan WA).
6. Ceklis klaim & kepatuhan (UU Perlindungan Konsumen, BPOM, halal, merek DJKI); larangan mengarang testimoni.
7. Terhubung dengan `riset-calon-pelanggan` dan `analisis-ulasan`; uji cepat 7 hari; contoh fiktif merek hijab lokal; README pembeli.

## Pembagian lisensi
- Kerangka umum (istilah dan struktur persona, JTBD/Empat Gaya, 6 bagian value proposition, konteks pemasaran) berasal dari materi MIT di atas; ditulis ulang dan dilokalkan; tunduk MIT (teks di bawah).
- Semua bagian lain (`scripts/`, `templates/`, `references/stp-umkm.md`, contoh, README) = karya orisinal Komunitech.
- Penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian, ditambah ketentuan MIT di bawah untuk bagian turunan.

## Teks lisensi asli

### phuryn/pm-skills
```
MIT License

Copyright (c) 2026 Pawel Huryn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### coreyhaines31/marketingskills
```
MIT License

Copyright (c) 2025 Corey Haines

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
