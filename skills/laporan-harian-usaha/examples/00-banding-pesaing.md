# 00 — Uji banding pesaing (skenario 01)

Pencarian (24 Sep 2026): WebSearch "openclaw skill daily report business owner SKILL.md sales inventory", "clawhub daily business briefing skill SQLite sales report telegram". Sumber yang dibuka: clawskills.sh (cermin ClawHub), VoltAgent/awesome-openclaw-skills (kategori marketing-and-sales), dokumentasi Datasette & Metabase. Script pihak ketiga tidak dijalankan dan tidak ada teks yang disalin.

## Kandidat yang ditemukan
| Pesaing | Sumber / lisensi | Sinyal | Relevansi |
|---|---|---|---|
| `daily-report` (@visualdeptcreative) | https://clawskills.sh/skills/visualdeptcreative-daily-report, lisensi tidak disebut | ±3,6 rb unduhan, bintang 4. Ditandai "suspicious" oleh pemindai OpenClaw | Laporan pipeline **lead** (jumlah lead, email, biaya), butuh Ollama + token Telegram. **Bukan** penjualan/stok/karyawan |
| `oc-daily-business-report` (@mariusfit) | https://clawskills.sh/skills/mariusfit-oc-daily-business-report, lisensi tidak disebut | 345 unduhan, v1.0.0 | Cuaca, kripto, berita, kesehatan server. **Tidak** ada penjualan/stok/karyawan/piutang |
| `daily-briefing` (berbagai) | lobehub/termo | Populer | Email, kalender, cuaca. Bukan data usaha |
| **Datasette** (open-source) | github.com/simonw/datasette, Apache-2.0 | ±10 rb bintang (perkiraan), dipelihara sejak 2017 | Penjelajah SQLite di browser. Mode immutable `-i` mematikan penguncian |
| **Metabase** (open-source) | github.com/metabase/metabase, AGPL | ±40 rb bintang (perkiraan) | Dashboard BI. Mendukung file SQLite (tidak di Cloud), dashboard subscription |

Tidak ditemukan skill publik yang menggabungkan kasir, stok, absensi, dan piutang lokal menjadi satu laporan pemilik. Pembanding yang paling setara fungsinya adalah **dashboard open-source (Datasette/Metabase)** yang diarahkan ke file SQLite yang sama.

## Skenario 01 dengan pesaing (disimulasikan dari dokumentasinya, tidak diinstal: CLAUDE.md meminta izin pemilik sebelum memasang paket baru)
- **Datasette:** `pip install datasette` → `datasette -i kasir.db stok.db absensi.db`. Pemilik mendapat tabel mentah `nota`, `bayar`, `nota_item`. Untuk mendapat "omzet bersih 276.600" pemilik atau agent harus menulis SQL sendiri (`SUM(netto)` termasuk baris void/retur bernilai negatif). Kesalahan umum `SUM(total) WHERE jenis='jual'` menghasilkan 371.580 (lihat 00-pembanding-tanpa-skill). Tidak ada perbandingan %, tidak ada "perlu perhatian", tidak ada pengiriman ke Telegram. Nama pelanggan tampil utuh dari CSV bila dimuat. Catatan: `-i` (immutable) di file yang sedang ditulis kasir bisa membaca data setengah jadi, karena penguncian dimatikan.
- **Metabase:** butuh Java/Docker (±1–2 GB RAM), setup koneksi SQLite per file, menyusun pertanyaan/dashboard sendiri. Dashboard subscription dikirim lewat email/Slack, bukan Telegram. Angka hanya benar bila query-nya benar. PBJT, void, retur, dan selisih kas harus dimodelkan sendiri.

## Penilaian untuk UMKM awam (skala 1–5)
| Kriteria | Datasette | Metabase | Skill pesaing ClawHub | **laporan-harian-usaha** |
|---|---|---|---|---|
| Kualitas isi laporan pemilik | 2 (tabel mentah) | 3 (bila disusun ahli) | 1 (topik lain) | **5** |
| Konteks Indonesia (Rp, PBJT, WIB, lembur, piutang) | 1 | 2 | 1 | **5** |
| Akurasi tanpa keahlian SQL | 2 | 2 | – | **5** (angka dari perintah resmi, diverifikasi) |
| Siap pakai / kirim ke HP | 1 | 3 (email) | 3 (Telegram) | **5** (Telegram via OpenClaw, teruji hingga percobaan kirim) |
| Setup untuk awam | 2 | 1 | 2 | **4** (butuh Python + alat di folder yang sama) |
| Eksplorasi bebas / grafik | **5** | **5** | 1 | 2 (teks saja) |

**Hasil:** skill kita **menang** untuk kebutuhan pemilik UMKM. Pesaing dashboard unggul untuk eksplorasi dan grafik, tetapi butuh keahlian SQL. Skill ClawHub yang ada tidak menyentuh data usaha.

## Yang bisa dipelajari (ide, bukan salinan)
- Dari Datasette/Metabase: sediakan **tautan/ekspor detail** (mis. CSV per jam/per produk) untuk pemilik yang ingin menggali lebih dalam, dan opsi grafik tren 7 hari sederhana (teks sparkline atau PNG) di laporan mingguan.
- Dari dashboard subscription Metabase: **ambang peringatan** yang bisa diatur (mis. "kirim hanya jika omzet turun > 20%" atau "selisih kas > Rp 10.000").
- Dari daily-briefing ClawHub: urutan "yang harus dilakukan hari ini" di bagian atas pesan, bukan di bawah. Pemilik yang sibuk hanya membaca 5 baris pertama.
