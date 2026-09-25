# Checklist Pemeriksaan Kebijakan Privasi (mode "cek")

Dipakai untuk mode 3 (memeriksa kebijakan privasi yang sudah ada), bersama atau tanpa `scripts/cek_kebijakan.py`. Script memeriksa kata kunci; agent **wajib membaca isinya** untuk menilai apakah memadai (mis. "masa simpan" disebut, tapi isinya "selamanya" = tetap bermasalah).

## A. Unsur pokok (bobot sama dengan script)
| # | Unsur | Bobot | Dasar | Tingkat risiko bila tidak ada |
|---|---|---|---|---|
| 1 | Identitas pengendali (nama usaha/pemilik) | 1 | Ps. 21 | TINGGI |
| 2 | Kontak urusan data (email/WA/alamat) | 1 | Ps. 21, 46 | TINGGI |
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

Skor = jumlah bobot terpenuhi ÷ bobot berlaku × 100. Status: ≥ 85 dan tanpa frasa TINGGI = **CUKUP LENGKAP**; 60–84 = **PERLU PERBAIKAN**; < 60 = **KURANG LENGKAP**. Frasa berisiko TINGGI selalu membuat status paling baik "PERLU PERBAIKAN". Bila skor tinggi tetapi masih ada isian `[isi: ...]`/`[fill: ...]`, status = **PERLU DILENGKAPI**.

## B. Frasa berisiko (contoh)
| Frasa | Tingkat | Masalah | Ganti dengan |
|---|---|---|---|
| "Kami tidak bertanggung jawab atas kebocoran data" | TINGGI | Kewajiban pengendali tidak bisa dilepas (Ps. 35, 46, 47) | Komitmen keamanan + pemberitahuan ≤ 3×24 jam |
| "Data dapat dijual/dibagikan kepada mitra" | TINGGI | Ps. 65, 67; tak ada dasar sah | "Kami tidak menjual data pribadi Anda" + daftar penerima spesifik |
| "Persetujuan dianggap diberikan" / "Anda dianggap setuju" | TINGGI | Persetujuan harus eksplisit & terekam (Ps. 20, 22) | Centang aktif / balas SETUJU |
| "Persetujuan tidak dapat ditarik" | TINGGI | Ps. 40 | Cara menarik persetujuan |
| "Data disimpan selamanya" | TINGGI | Ps. 43, 21 | Masa simpan per jenis data |
| "Anda melepaskan hak menuntut" | TINGGI | Hak gugat ganti rugi (Ps. 5–13) | Hapus |
| "Dengan menggunakan situs ini Anda setuju..." | SEDANG | Bukan persetujuan eksplisit per tujuan | Jadikan pemberitahuan; minta persetujuan terpisah untuk promo/data spesifik |
| "Dapat diubah sewaktu-waktu tanpa pemberitahuan" | SEDANG | Ps. 21 ayat (2) | Pemberitahuan sebelum berlaku |
| "Dibagikan kepada pihak mana pun" | SEDANG | Prinsip terbatas & spesifik (Ps. 16) | Penerima spesifik + tujuan |
| "Mengakses semua data di perangkat Anda" | SEDANG | Minimisasi | Batasi izin |

## C. Hal yang tidak bisa dinilai script (agent periksa manual)
- Isi sesuai praktik nyata? (mis. mengaku "tidak ada transfer LN" padahal pakai Google Drive/WA).
- Kebijakan hasil salinan dari usaha lain/luar negeri (menyebut GDPR, CCPA, "California", nama perusahaan lain, mata uang asing) → TINGGI: tulis ulang sesuai UU PDP.
- Bahasa: ada versi Bahasa Indonesia? (UU 24/2009 Ps. 31 untuk dokumen perjanjian; praktik baik untuk kebijakan).
- Klaim keamanan berlebihan ("100% aman", "tidak mungkin bocor") → SEDANG: ganti dengan langkah nyata.
- Data spesifik dikumpulkan lewat Google Form/WA tanpa perlindungan tambahan → TINGGI.
