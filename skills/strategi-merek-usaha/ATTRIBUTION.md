# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi)** dari skill publik berlisensi MIT, dengan nilai tambah besar untuk konteks Indonesia.

## Sumber yang diadaptasi
| Sumber | Pembuat | Lisensi | Snapshot |
|---|---|---|---|
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Corey Haines | MIT (c) 2025 Corey Haines | `git clone --depth 1`, commit 5b2c0007 (4 Sep 2026), dibaca 2026-09-30 |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Pawel Huryn | MIT (c) 2026 Pawel Huryn | `git clone --depth 1`, commit 8607e3b0 (14 Sep 2026), dibaca 2026-09-30 |

Bagian yang dipelajari (struktur/alur saja):
- marketingskills: `skills/offers/SKILL.md` dan `references/` (persamaan nilai, enam komponen penawaran, jenis garansi, susunan bonus, skarsitas jujur/larangan skarsitas palsu, diagnosis tuas terlemah).
- pm-skills: `pm-marketing-growth/skills/product-name/SKILL.md` (pendekatan menamai: beberapa opsi beralasan, mudah diucap/dieja, catatan domain dan merek).
- Tidak dipakai: skill lain di kedua repo; tautan, kursus, atau contoh kasus milik pembuat sumber tidak disalin.

## Audit keamanan (Tahap 3 CLAUDE.md)
- Seluruh `SKILL.md` dan `references/` yang diadaptasi dibaca penuh. Skill `offers` dan `product-name` tidak memiliki folder `scripts/`; tidak ada kode dari sumber yang dijalankan atau disalin.
- Pencarian pola berbahaya (curl/wget/eval/exec/base64, kredensial, token, instruksi "abaikan") pada file terpilih: tidak ditemukan. Tidak ada prompt injection tersembunyi, permintaan mengirim file, atau menonaktifkan konfirmasi.
- Tidak ada API key/token/data pribadi tertanam.
- Kesimpulan: **lolos audit**. Sinyal sumber: marketingskills ±52 rb bintang, ±7,8 rb fork; pm-skills ±26,7 rb bintang, ±2,8 rb fork (GitHub, dicek 2026-09-30); dirawat aktif; pembuat individu (lihat `research/sources/branding-naming-2026-09-30.md`).

## Apa yang diubah/ditambahkan (file telah diubah dari sumber)
Sumber berbahasa Inggris dan berorientasi kursus/info-produk/SaaS dan pasar global. Perubahan besar:
1. Ditulis ulang penuh dalam Bahasa Indonesia sehari-hari; penamaan dan perumusan penawaran digabung dalam satu alur untuk UMKM.
2. **Script Python baru** `scripts/skor_nama.py` (skor nama berbobot, hitung suku kata Indonesia, kemiripan ejaan dengan daftar merek pengguna) dan `scripts/hitung_penawaran.py` (laba per unit, bonus, refund, ruang bonus), plus uji regresi `tests/uji_regresi.py`; sumber tidak punya script.
3. Lokalisasi Indonesia: cek arti di bahasa daerah dan slang, uji ucap, domain .id/.com, handle IG/TikTok, nama toko marketplace, langkah PDKI/DJKI dan kelas Nice (tanpa opini hukum), Rupiah, WA/Shopee/Tokopedia/TikTok Shop, hitungan potongan marketplace.
4. Kepatuhan: ringkasan pasal UU Perlindungan Konsumen yang relevan (Pasal 9, 10, 11, 12, 13, 17), aturan kelangkaan jujur, ceklis tayang; bukan nasihat hukum.
5. Penanganan input awam: satu daftar pertanyaan, default beralasan, larangan mengklaim ketersediaan nama, contoh nyata, README pembeli.

## Pembagian lisensi
- Kerangka umum (istilah persamaan nilai, komponen penawaran, jenis garansi, gagasan menamai beberapa opsi beralasan) berasal dari materi MIT di atas; ditulis ulang dan dilokalkan; tunduk MIT (teks di bawah). Persamaan nilai berasal dari gagasan yang dipopulerkan pihak lain dan dirujuk oleh sumber; di sini hanya dipakai sebagai kerangka umum.
- Semua bagian lain (`scripts/`, `tests/`, `templates/`, `references/cek-merek-pdki.md`, `references/kata-dan-klaim.md`, contoh, README) = karya orisinal Komunitech.
- Penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian, ditambah ketentuan MIT di bawah untuk bagian turunan. Salinan teks lisensi juga di folder `licenses/`.

## Teks lisensi asli

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
