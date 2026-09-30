# Sumber: penamaan & penawaran (skill `strategi-merek-usaha`) — 2026-09-30

| Item | Sumber A | Sumber B |
|---|---|---|
| Repo | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), skill `offers` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills), skill `pm-marketing-growth/skills/product-name` |
| Pembuat | Corey Haines (individu) | Pawel Huryn (individu) |
| Lisensi | **MIT** (c) 2025 Corey Haines; halaman GitHub menampilkan MIT; file LICENSE disalin identik | **MIT** (c) 2026 Pawel Huryn; halaman GitHub menampilkan MIT; file LICENSE disalin identik |
| Sinyal (GitHub, 2026-09-30) | ±52 rb bintang, ±7,8 rb fork, 473 commit, ±429 pengamat | ±26,7 rb bintang, ±2,8 rb fork; 69 skill + 42 alur kerja, 9 plugin |
| Snapshot dibaca | commit `5b2c000` (4 Sep 2026) | commit `8607e3b` (14 Sep 2026) |
| Isi skill | `offers`: 8 file referensi (persamaan nilai, anatomi 6 komponen, garansi 8 jenis, bonus, skarsitas jujur, format, SaaS, contoh) + evals | `product-name`: prompt singkat 5 nama dengan alasan, catatan domain/merek; tidak ada script |
| Keputusan | **Diterima**, ATM (salin-edit dengan atribusi) | **Diterima**, ATM |

## Audit keamanan
Seluruh `offers/SKILL.md`, `references/*`, `evals.json`, dan `product-name/SKILL.md` diperiksa. Tidak ada folder `scripts/`; pencarian curl/wget/eval/exec/base64/kredensial/token/instruksi "abaikan": nihil. Tidak ada prompt injection. Lolos.

## Catatan kualitas dan nilai tambah
- `product-name` tipis (satu prompt), `offers` kuat tetapi berorientasi kursus/info-produk/B2B AS dan bahasa Inggris. Nilai tambah Komunitech: script skor nama (suku kata Indonesia, kemiripan dengan daftar merek pengguna), script laba per unit penawaran, cek arti bahasa daerah/slang, langkah PDKI/DJKI + kelas Nice tanpa opini hukum, kelangkaan jujur dengan dasar UU Perlindungan Konsumen (Pasal 9-13, 17), teks WA/IG/marketplace, contoh lokal.
- Merek/handle/domain tidak dicek agent; skill hanya menyarankan (keputusan pemilik).
- Skill hukum baru dilarang: bagian merek hanya arahan praktis dan disclaimer.
- Verifikasi pasal UU 8/1999 (9-13, 17) dari ingatan pembuat: PERLU REVIEW terhadap teks resmi di peraturan.go.id/JDIH BPK. Verifikasi alamat pdki-indonesia.dgip.go.id dan klasifikasi kelas Nice (edisi berlaku) juga PERLU dicek pemilik sebelum rilis.
