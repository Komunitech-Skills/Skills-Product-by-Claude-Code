# Checklist Pemeriksaan Kebijakan Privasi (mode "cek")

Dipakai untuk mode 3 (memeriksa kebijakan privasi yang sudah ada), bersama atau tanpa `scripts/cek_kebijakan.py`. **Urutan (v1.0.3):** agent membaca seluruh dokumen lebih dulu dan menilai risiko per kategori di `kategori-risiko-cek.md` (K1–K16), baru menjalankan script sebagai pemeriksa kedua untuk unsur (bagian A) dan skor. Script memeriksa kata kunci; isinya tetap dinilai agent (mis. "masa simpan" disebut, tapi isinya "selamanya" = tetap bermasalah).

## A. Unsur pokok (bobot sama dengan script)
| # | Unsur | Bobot | Dasar | Tingkat risiko bila tidak ada |
|---|---|---|---|---|
| 1 | Identitas pengendali (nama usaha/pemilik) | 1 | Ps. 5, 21 | TINGGI |
| 2 | Kontak urusan data (email/WA/alamat) | 1 | Ps. 5, 21 | TINGGI |
| 3 | Jenis data yang dikumpulkan | 1 | Ps. 21 ayat (1) c, e | TINGGI |
| 4 | Tujuan pemrosesan | 1 | Ps. 16, 21 ayat (1) b | TINGGI |
| 5 | Dasar pemrosesan | 1 | Ps. 20 ayat (2), 21 ayat (1) a | SEDANG |
| 6 | Pihak penerima data | 1 | Ps. 21 | SEDANG |
| 7 | Transfer/penyimpanan di luar negeri | 1 | Ps. 56 | SEDANG (TINGGI bila jelas memakai layanan asing tanpa disebut) |
| 8 | Masa simpan | 1 | Ps. 21 ayat (1) d, f; Ps. 43 | SEDANG |
| 9 | Hak subjek data (akses, koreksi, hapus, tarik persetujuan) | 2 | Ps. 5–13 | TINGGI |
| 10 | Cara mengajukan & batas waktu 3×24 jam | 1 | Ps. 30, 32, 40 | SEDANG |
| 11 | Keamanan data | 1 | Ps. 35–39 | SEDANG |
| 12 | Pemberitahuan kebocoran 3×24 jam | 1 | Ps. 46 | SEDANG |
| 13 | Tanggal berlaku / diperbarui | 1 | Ps. 21 ayat (2) | RENDAH |
| 14 | Cara memberi tahu perubahan | 1 | Ps. 21 ayat (2) | RENDAH |
| B1 | (bila ada data anak) persetujuan orang tua/wali | 1 | Ps. 25 | TINGGI |
| B2 | (bila ada data spesifik) perlakuan khusus & persetujuan eksplisit | 1 | Ps. 4 ayat (2), 20, 34 | TINGGI |

Skor = jumlah bobot terpenuhi ÷ bobot berlaku × 100. Status diperiksa **berurutan** (yang pertama cocok dipakai; sama dengan `--daftar` dan kunci JSON `alasan_status`): (1) skor < 60 = **KURANG LENGKAP** — ini mengalahkan BELUM SIAP, kecuali dokumen berisian kosong yang skor strukturnya ≥ 60 dan tanpa frasa TINGGI; (2) ada frasa TINGGI = **PERLU PERBAIKAN**; (3) masih ada isian `[isi: ...]`/`[fill: ...]`/`{JIKA ...}` = **BELUM SIAP**; (4) skor 60–84 = **PERLU PERBAIKAN**; (5) ≥ 85 = **CUKUP LENGKAP**. Selama ada isian, skor dibatasi maks. 84, dan unsur yang buktinya hanya ada di kalimat berisian kosong (atau hanya di judul) dihitung setengah (**BELUM DIISI**). Script juga menampilkan *skor struktur* (skor bila semua isian dilengkapi).

**Satu temuan per kalimat (v1.0.2):** bila beberapa pola cocok di satu kalimat, script menampilkan satu temuan dengan tingkat tertinggi; alasan lain digabung ("Juga: ...") dan kecocokan lain ada di `cocok_lain`. Klausa setelah "tetapi/namun/akan tetapi/kecuali" dinilai tersendiri.

**Polaritas (v1.0.1):** unsur hanya terpenuhi oleh kalimat positif ("kami **tidak akan** memberi tahu bila bocor" ≠ unsur kebocoran; "tidak akan mengubah … **tanpa** pemberitahuan" = positif). Pengecualian: pernyataan "data tidak dikirim ke luar negeri" tetap memenuhi unsur transfer LN (informasi yang sah). Frasa berisiko yang disangkal ("Data Anda tidak akan dijual") tidak ditandai.

## B. Frasa berisiko (contoh kata kunci yang dikenali script)
Tabel ini hanya contoh bentuk yang umum. Kalimat dengan makna sama tetapi kata berbeda **tidak** dikenali script; penilaian risiko memakai kategori di `kategori-risiko-cek.md`, bukan tabel ini.

| Frasa | Tingkat | Masalah | Ganti dengan |
|---|---|---|---|
| "Kami tidak akan memberi tahu bila terjadi kebocoran" / "merahasiakan kebocoran" | TINGGI | Ps. 46 (wajib beri tahu ≤ 3×24 jam) | Komitmen pemberitahuan tertulis ≤ 3×24 jam |
| "Kami dibebaskan dari tanggung jawab …" / "tidak bertanggung jawab jika data bocor" | TINGGI | Ps. 35, 46, 47 | Komitmen keamanan + pemberitahuan |
| "Data dapat dialihkan/ditukar dengan imbalan", "memperdagangkan/memonetisasi data", "may sell or rent" | TINGGI | Ps. 65, 67 | "Kami tidak menjual data pribadi Anda" |
| "Dibagikan ke pihak ketiga untuk pemasaran mereka" tanpa persetujuan | SEDANG | Ps. 16, 20, 22 | Persetujuan aktif per tujuan |
| "Kami tidak menjual data, **tetapi** dapat membagikannya ke mitra iklan" · "data dapat kami berikan/serahkan/teruskan kepada pengiklan/agensi iklan/sponsor untuk promosi" · "tidak membagikan data **kecuali** kepada mitra pemasaran" · EN "share … with advertisers/ad networks", "disclose … for advertising" | SEDANG | Ps. 16, 20, 22 — klausa "tidak menjual" di depan tidak menghapus risiko klausa kedua | Hapus, atau hanya dengan persetujuan aktif terpisah + sebut penerimanya |
| "Diam/tidak membalas kami anggap setuju" · "silence is deemed consent" | TINGGI | Ps. 20, 22 | Persetujuan aktif |
| "Untuk tujuan apa pun" · "for any purpose" | SEDANG | Ps. 16 ayat (2) huruf b (tujuan spesifik) | Sebut tujuan spesifik |
| "under the age of 13" / "di bawah 13 tahun" (batas usia ala COPPA AS) | SEDANG | Ps. 25 + UU 35/2014 Ps. 1 angka 1 (anak = belum 18 tahun) | "di bawah 18 tahun … dengan persetujuan orang tua/wali" |
| "Kami tidak bertanggung jawab atas kebocoran data" | TINGGI | Kewajiban pengendali tidak bisa dilepas (Ps. 35, 46, 47) | Komitmen keamanan + pemberitahuan ≤ 3×24 jam |
| "Data dapat dijual/dibagikan kepada mitra" | TINGGI | Ps. 65, 67; tak ada dasar sah | "Kami tidak menjual data pribadi Anda" + daftar penerima spesifik |
| "Persetujuan dianggap diberikan" / "Anda dianggap setuju" | TINGGI | Persetujuan harus eksplisit & terekam (Ps. 20, 22) | Centang aktif / balas SETUJU |
| "Persetujuan tidak dapat ditarik" | TINGGI | Ps. 40 | Cara menarik persetujuan |
| "Data disimpan selamanya" | TINGGI | Ps. 43, 21 | Masa simpan per jenis data |
| "Anda melepaskan hak menuntut" | TINGGI | Hak gugat ganti rugi (Ps. 5–13) | Hapus |
| "Dengan menggunakan situs ini Anda setuju..." | SEDANG | Bukan persetujuan eksplisit per tujuan | Jadikan pemberitahuan; minta persetujuan terpisah untuk promo/data spesifik |
| "Dapat diubah sewaktu-waktu tanpa pemberitahuan" / "kebijakan dapat berubah sewaktu-waktu" (tanpa janji pemberitahuan) | SEDANG | Ps. 21 ayat (2) | Pemberitahuan sebelum berlaku |
| "Dibagikan kepada pihak mana pun" | SEDANG | Prinsip terbatas & spesifik (Ps. 16) | Penerima spesifik + tujuan |
| "Mengakses semua data di perangkat Anda" | SEDANG | Minimisasi | Batasi izin |

## C. Hal yang tidak bisa dinilai script (agent periksa manual)
Daftar lengkap per kategori, dengan contoh parafrasa ID/EN dan dasar pasal: `kategori-risiko-cek.md`. Yang paling sering lolos dari script pada uji buta v1.0.2:
- Pembatasan hak: "dipertimbangkan sesuai diskresi kami", "tidak dapat dilayani", persetujuan "final/tidak dapat ditarik kembali", biaya atau syarat berlebihan (K9).
- Anak mendaftar sendiri atau tanpa izin orang tua/wali (K10).
- Opt-out ("kecuali Anda keberatan") untuk data spesifik, mis. foto pasien untuk testimoni (K3, K11).
- Transfer LN tanpa jaminan pelindungan setara (K6); catat semua layanan asing yang disebut, termasuk Google Sheets/Drive.
- Perubahan tujuan tanpa persetujuan ulang (K4).
- Pelacakan lokasi yang tidak bisa dimatikan; data berlebih seperti swafoto + KTP (K12).
- Eufemisme berbagi/monetisasi: "kolaborasikan", "salurkan ke rekan bisnis", "made available to partners", "monetisasi wawasan" (K1, K2).
- Unsur yang salah dibaca script pada teks Inggris (identitas "X ("the Clinic")", "Purpose:", "Sharing") → koreksi status unsur.

- Isi sesuai praktik nyata? (mis. mengaku "tidak ada transfer LN" padahal pakai Google Drive/WA).
- Kebijakan hasil salinan dari usaha lain/luar negeri (menyebut GDPR, CCPA, "California", nama perusahaan lain, mata uang asing) → **SEDANG** (sama dengan script): tulis ulang sesuai UU PDP. Naikkan ke TINGGI hanya bila salinan itu memuat praktik terlarang (mis. menjual data) atau tidak sesuai praktik nyata.
- Bahasa: ada versi Bahasa Indonesia? (UU 24/2009 Ps. 31 untuk dokumen perjanjian; praktik baik untuk kebijakan).
- Batas usia anak dari template luar negeri (13 tahun, COPPA) → SEDANG (juga ditandai script): di Indonesia pakai **di bawah 18 tahun** + persetujuan orang tua/wali (lihat `dasar-hukum.md`, baris Data anak).
- Klaim keamanan berlebihan ("100% aman", "tidak mungkin bocor") → SEDANG: ganti dengan langkah nyata. Kalimat jujur "tidak ada sistem yang 100% aman" **bukan** masalah.
- Data spesifik dikumpulkan lewat Google Form/WA tanpa perlindungan tambahan → TINGGI.
