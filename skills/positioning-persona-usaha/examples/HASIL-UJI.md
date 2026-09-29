# HASIL UJI — positioning-persona-usaha

- Tanggal: 2026-09-29
- Penguji: agent independen (bukan pembuat), hanya membaca folder skill + CLAUDE.md. Uji = **simulasi agent** di `claude-code (simulasi agent)`; belum diuji di platform asli.
- Script dijalankan sungguhan di folder scratchpad penguji; angka diverifikasi dengan hitungan pecahan eksak buatan penguji.

## 1. Audit keamanan & format
| Butir | Hasil |
|---|---|
| Frontmatter hanya `name` + `description`; name = nama folder; description 604 karakter (≤ 1024), ada kata kunci ID & EN | ✔ |
| Tidak ada field/placeholder khusus platform | ✔ |
| SKILL.md 117 baris (< 300); materi panjang di `references/` | ✔ |
| Struktur Tahap 5 (SKILL, README, examples, references, templates, scripts, ATTRIBUTION) | ✔ |
| Script: hanya `argparse, csv, json, sys` (uji: `json, os, subprocess, sys, tempfile`); tidak ada jaringan, eval/exec, penulisan file, akses kredensial | ✔ aman |
| Tidak ada API key/token/data pribadi | ✔ |
| Lisensi: sumber MIT (phuryn/pm-skills, coreyhaines31/marketingskills); teks lisensi asli + hak cipta disertakan; keterangan "file telah diubah" ada; snapshot commit 8607e3b / 5b2c000 cocok dengan repo yang dikloning penguji; baris hak cipta cocok (2026 Pawel Huryn, 2025 Corey Haines) | ✔ |
| README menyatakan tidak berafiliasi dengan pembuat sumber | ✔ |
| Lokasi instalasi di tabel README | tidak diverifikasi (di luar folder skill; cocokkan dengan `docs/instalasi.md`) |
| `scripts/uji_skor_segmen.py` bawaan | "Semua uji lulus" ✔ |

## 2. Skenario
| # | File | Jenis | Putusan | Catatan |
|---|---|---|---|---|
| 1 | `01-uji-katering-rantang-semarang.md` | Normal (katering, Semarang) | **Lulus** | Script 79/78/66/57 cocok verifikasi; hitungan paket Rp 25.000/porsi benar; bio 131 karakter dihitung. Skor 1-2 seri (selisih 1), tidak ada aturan seri |
| 2 | `02-pakai-data-analisis-ulasan.md` | Normal (jasa AC, pakai data ulasan) | **Lulus** | Data ulasan jadi FAKTA; nama+nomor pelanggan tidak ikut ke persona. Risiko menjumlah hitungan tema ulasan (19+12) tidak diperingatkan |
| 3 | `03-skor-segmen-script.md` | Normal (keripik, bobot kustom, minta ringkas) | **Lulus dengan catatan** | Skor bobot kustom (Σ bobot 105) cocok: 78,1/68,6/61,0/60,0. Uji data rusak: 1 crash + 3 bug kecil (lihat bawah) |
| 4 | `04-input-kurang.md` | Input tidak lengkap | **Lulus** | Tanya sekali, 5 pertanyaan, jalan pintas "lanjut", asumsi ditandai |
| 5 | `05-luar-cakupan.md` | Klaim medis + testimoni palsu + data pribadi | **Lulus** | Menolak 3 hal berisiko, menawarkan alternatif sah |
| A/B | `00-pembanding-tanpa-skill.md` | — | **Skill menang jelas** | Tanpa skill: klaim "sehat/terbaik" tanpa bukti, tidak ada skor, tidak ada teks tempel. Skill kalah hanya di panjang |
| Pesaing | `00-banding-pesaing.md` | — | **Skill menang** (35 vs 19 vs 19) | Pesaing unggul di dokumen konteks berversi |

## 3. Bug ditemukan
| # | Tingkat | Bug | Bukti |
|---|---|---|---|
| B1 | **Sedang** | Baris CSV dengan kolom lebih banyak dari judul (mis. nama segmen berkoma tanpa tanda kutip: `Ibu muda, pengajian,3,3,...`) → **traceback** `AttributeError: 'list' object has no attribute 'strip'`, kode keluar 1. Melanggar janji "kesalahan CSV dijelaskan pesan GAGAL". Input ini sangat mungkin dari pengguna awam | `skor_segmen.py` baris 76: `(v or "").strip()` saat DictReader menaruh sisa kolom sebagai list di kunci `None` |
| B2 | Rendah | `--bobot ukuran=inf` / `ukuran=nan` diterima → skor `nan`, label "Tunda", kode 0 | `baca_bobot` tidak memeriksa angka hingga (finite) |
| B3 | Rendah | Judul kolom ganda (mis. dua `ukuran`) diterima diam-diam, kolom terakhir yang dipakai (skor 82 → 73) | `baca_csv` tidak memeriksa duplikat |
| B4 | Rendah | Bobot desimal koma (`ukuran=1,5`) gagal karena koma juga pemisah antar-bobot; `v.replace(",", ".")` tidak pernah berguna | pesan: `Bobot '5' salah format` |
| B5 | Rendah (tampilan) | Nama segmen dipotong 33 karakter di tabel keluaran ("Karyawan perantau & anak kos kerj") → mudah tersalin terpotong ke laporan | format `{h['segmen'][:33]:<34}` |
| B6 | Rendah | CSV berpemisah tab → pesan "Kolom 'segmen' tidak ada" (kurang menjelaskan penyebab) | deteksi pemisah hanya `,`/`;` |

## 4. Temuan instruksi (bukan bug script)
- Tidak ada aturan untuk skor segmen yang hampir seri; di 2 dari 3 skenario normal dua segmen teratas selisih 1 poin dan keduanya berlabel "Utama".
- "Hitung karakter, jangan dikira" tanpa cara menghitung; emoji dihitung berbeda per aplikasi.
- Keluaran lengkap ±150 baris; berat untuk dibaca di chat (OpenClaw via Telegram/WA), padahal audiens mayoritas awam.
- "UU Perlindungan Konsumen" disebut tanpa nomor/tahun/pasal (Tahap 4 butir 5 CLAUDE.md minta dasar aturan + tanggal).
- Contoh `01-toko-hijab-stp-persona-lengkap.md` (fiktif, "bukan hasil uji resmi") masih dirujuk SKILL.md & README sebagai contoh lengkap; kini ada dua file berawalan `01-`.
- Tidak ada peringatan bahwa hitungan tema ulasan bisa tumpang-tindih (satu ulasan memuat beberapa pujian) sehingga tidak boleh dijumlahkan menjadi "N pelanggan".

## 5. Skor kualitas: **8 / 10 — LULUS**
Alasan:
- (+) Alur 9 langkah jelas dan lengkap: FAKTA/HIPOTESIS, STP dengan skor berbobot lewat script, persona + anti-persona + wawasan, JTBD + Empat Gaya, tabel pembeda dengan bukti, positioning 2 versi, 5 tagline, message house, teks siap tempel, uji 7 hari.
- (+) Sangat kuat di kejujuran klaim dan kepatuhan (placeholder `[isi:]`, ceklis BPOM/halal/DJKI, data pribadi disamarkan, stereotip dihindari) — ini pembeda utama melawan jawaban tanpa skill dan pesaing.
- (+) Script benar pada semua angka yang diverifikasi (7 segmen bobot awal + 4 segmen bobot kustom + 4 contoh bawaan); uji regresi bawaan lulus; sebagian besar data rusak ditangani.
- (+) Menang A/B dan menang banding pesaing dengan jelas.
- (−) B1: crash pada input awam yang realistis (koma di nama segmen).
- (−) Tidak ada aturan seri; keluaran panjang untuk chat; beberapa bug kecil script.
Tidak ada batas skor 6 (A/B dan pesaing dimenangkan).

## 6. Permintaan perbaikan untuk pembuat (penguji tidak mengubah skill)
1. **B1:** di `baca_csv`, tolak baris dengan kolom berlebih (kunci `None`) dengan pesan `GAGAL: Baris N: jumlah kolom lebih banyak dari judul — nama segmen yang berisi koma harus diberi tanda kutip "..." atau ganti koma dengan '/'`. Tambahkan kasus ini ke `uji_skor_segmen.py`.
2. **B2:** tolak bobot yang tidak hingga (`math.isfinite`), tambah uji.
3. **B3:** tolak judul kolom ganda dengan pesan jelas, tambah uji.
4. **B4:** dokumentasikan bahwa desimal bobot memakai titik (`ukuran=1.5`), atau pakai pemisah `;` untuk `--bobot`; hapus `replace` yang tidak berguna.
5. **B5:** jangan potong nama di tabel (atau lebarkan kolom), atau instruksikan di SKILL.md Langkah 3 agar agent menyalin nama lengkap dari CSV / memakai `--format json`.
6. **Aturan seri** di Langkah 3: mis. "Bila dua segmen teratas selisih < 5 poin, anggap setara; pilih yang sudah terbukti membeli (FAKTA) atau yang paling murah diuji, dan jelaskan alasannya."
7. Batasan: sebut dasar aturan lengkap, mis. "UU No. 8 Tahun 1999 tentang Perlindungan Konsumen (Pasal 9 dan 17: larangan penawaran/iklan menyesatkan)" + tanggal cek.
8. **Mode chat:** tambahkan aturan "bila dipakai lewat chat (Telegram/WA) atau pengguna awam, kirim dulu Ringkasan 5 baris + teks siap tempel, lalu tawarkan versi lengkap".
9. Langkah 1/8: peringatan bahwa jumlah per tema ulasan tidak boleh dijumlahkan menjadi jumlah pelanggan; tulis angka per tema.
10. Cara hitung karakter bio: sediakan perintah (mis. opsi `--hitung "teks"` di script atau `python3 -c "print(len('...'))"`) dan catatan bahwa emoji bisa dihitung 2 oleh sebagian aplikasi → sisakan ruang ±5 karakter.
11. Pindahkan/ubah nama `examples/01-toko-hijab-stp-persona-lengkap.md` (mis. `contoh-hijab-fiktif.md` atau ke `references/`) dan perbarui rujukan di SKILL.md & README, supaya `examples/01..05` hanya berisi hasil uji.
12. (Opsional, dari banding pesaing) tawarkan menyimpan ringkasan positioning sebagai file konteks yang bisa dibaca skill Komunitech lain (`caption-sosmed-umkm`, `copy-landing-page`).

Setelah perbaikan B1 dan butir 6/8, uji ulang oleh penguji independen (cukup skenario 1, 3, dan data rusak).
