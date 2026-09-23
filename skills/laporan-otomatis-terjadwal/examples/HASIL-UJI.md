# HASIL UJI — laporan-otomatis-terjadwal v1.1.0 (uji ulang)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi diuji:** v1.1.0 (commit `285d267`). Uji pertama v1.0.0: skor 6 (REVISI), 0 cacat berat, 5 sedang, 5 ringan.
- **Lingkungan:** Python 3.11; OpenClaw **2026.9.5 (ec9c1a1)**, HOME uji `/tmp/uji-oc-home`, Gateway lokal (`gateway run --allow-unconfigured --bind loopback --token …`, tanpa model AI & tanpa kanal login). Data di `/tmp/uji-laporan-otomatis-terjadwal/`. Skill pendamping `buku-stok` v1.1.1.

## Uji ulang cacat v1.0.0
| Cacat v1.0.0 | Uji ulang v1.1.0 | Status |
|---|---|---|
| **S-1** `run/edit/disable/enable/rm` memakai nama | SKILL.md Langkah 5–7 & references kini memakai **id** dari output `add` (dijelaskan cara mengambilnya); hanya `show` yang memakai nama persis. Dijalankan: `show "<nama>"` ✓; `disable`/`enable`/`edit --cron --tz`/`edit --to`/`run` (`enqueued: true`)/`runs`/`rm` dengan id ✓ | **Beres** |
| **S-2** template `add` di references ditolak CLI | Dua bentuk: A (`add "<cron>" "<pesan>" --name …`, dipakai SKILL.md) & B (`add --cron … --message … --name …`) — **keduanya dijalankan sungguhan dan berhasil** (jadwal `0 7 * * 1` @ Asia/Jakarta, `announce -> telegram:123456789`). Aturan jangan mencampur posisi + `--cron` + `--name` dijelaskan; klaim verifikasi di references kini akurat | **Beres** |
| **S-3** resep stok menipis tidak memakai buku-stok, salah untuk kasus 0 | Jalur utama `stok.py info --json` + `laporan menipis --json` (hanya baca). Diuji: `jumlah: 2` → pesan dengan perkiraan habis; `jumlah: 0` → "Jumlah produk menipis: 0 / Tidak ada produk menipis hari ini"; DB tidak ada → `ok: false` exit 1 → berhenti. Job dengan `--tools exec,read` dijalankan → `toolsAllow: ["exec","read"]` | **Beres** |
| **S-4** data basi / banyak file | Tabel `--maks-umur-hari` per irama (harian 1 / mingguan 6 / bulanan 27) di SKILL.md & semua resep; Langkah 3.2 wajib mencocokkan periode hasil dengan periode yang diminta; `--daftar-semua` diuji dengan 3 file harian → `file_cocok` 3 item + peringatan agar digabung | **Beres** |
| **S-5** deteksi PDP lemah & bocor ke pesan | "unik", "Klinik", "Teknik" tidak lagi memicu; `081200001234`, email, dan "NIK" terdeteksi → **exit 3**, peringatan hanya di stderr, isi pesan bersih | **Beres** (sisa: lihat R-6) |
| R-1 pemotongan membuang peringatan | 20 item + 1 catatan + 2 peringatan, `--maks-baris 15` → kedua peringatan dipertahankan, daftar dipotong + keterangan "(disingkat …)" tanpa merujuk folder arsip | Beres |
| R-2 label "Jumlah transaksi" | Kini "Jumlah baris/item terjual" di resep & contoh | Beres |
| R-3 judul "Harian" untuk 2 hari | README/contoh kini "Mingguan" | Beres |
| R-4 cara mencari chat id | references diperbarui | Beres |
| R-5 ikon ⚠️ untuk catatan netral | `catatan` tanpa ikon, `peringatan` dengan ⚠️ | Beres |

## Uji end-to-end
- **Resep penjualan** (`cek_sumber_data --maks-umur-hari 6` → `rekap.py` → cek periode 14–20 Sep = Senin–Minggu penuh → `susun_pesan`): omzet Rp 2.778.000, 62 baris, rata-rata Rp 396.857, 3 teratas & hari terbaik/terendah **cocok dengan hitungan independen**; exit 0; 13 baris.
- **Data kosong:** folder tidak ada / 0 byte / hanya judul / baris `;;;` → `siap: false`; semua baris Batal → `rekap.py` exit 1. Tidak ada angka nol palsu.
- **Kanal & aturan pemilik:** Telegram default; WA hanya nomor terpisah + persetujuan tertulis + hanya ke pemilik; broadcast ditolak. Tidak berubah dari uji pertama (lulus).
- **Keamanan:** kedua script tetap library standar, tanpa jaringan/subprocess; tidak ada prompt injection. Contoh jadwal stok membatasi alat (`--tools exec,read`).

## Skor
| Kriteria | Skor |
|---|---|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 8 |
| Kualitas output | 8 |
| Akurasi (angka/fakta) | 9 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 9 |
| **SKOR AKHIR** | **8 / 10 — LULUS** |

Alasan: semua cacat sedang dari uji pertama beres dan dibuktikan dengan perintah OpenClaw yang dijalankan sungguhan. Angka akurat, dan jalur stok kini benar-benar memakai buku-stok. Skor tidak 9 karena pengiriman nyata ke Telegram/WA dan `run --wait` sampai selesai belum bisa diuji (mesin uji tanpa model AI & tanpa token bot), dan masih ada beberapa kekurangan ringan di bawah. Keduanya perlu dicek pada uji platform asli oleh pemilik/tim.

## Cacat tersisa (ringan)
- **R-6. Nomor HP yang ditulis dengan pemisah tidak terdeteksi.** `0812-0000-1234`, `+62 812 0000 1234`, `(0812) 00001234` → exit 0. Ini cara menulis nomor yang paling umum di Indonesia. *Saran:* regex yang mengizinkan spasi/strip/titik/kurung, mis. `(?<!\d)(\+?62|0)[\s\-.()]*8(?:[\s\-.()]*\d){7,11}(?!\d)` (susun_pesan.py baris 67).
- **R-7. Positif palsu pada kode berisi angka 08…:** "Resi: JNE0812345678" → exit 3. Jarang di laporan agregat; cukup disebut di SKILL.md bahwa exit 3 bisa salah tuduh untuk kode resi/invoice.
- **R-8. Pesan tanpa baris kosong antarbagian** (judul/angka/daftar/catatan) — di v1.0.0 ada. Di layar HP jadi lebih padat; pertimbangkan satu baris kosong sebelum daftar dan sebelum catatan (tidak dihitung sebagai baris isi).
- **R-9. Peringatan "banyak file cocok" hanya muncul dengan `--daftar-semua`.** Tanpa flag itu hanya ada `file_lain_cocok: 2` tanpa peringatan; agent harus ingat membaca field itu (SKILL.md sudah menyuruh). Saran: tampilkan peringatan singkat juga tanpa flag bila `file_lain_cocok > 0`.

## Verifikasi angka independen
**Ya.** Rekap penjualan (omzet, jumlah, rata-rata, terlaris, hari terbaik/terendah) dan angka stok menipis (rata-rata laku, perkiraan habis) dihitung ulang dengan Python terpisah dan cocok.
