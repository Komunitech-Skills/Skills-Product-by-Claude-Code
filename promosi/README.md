# promosi/ — bukti sebelum/sesudah (SSOT untuk materi promosi)

| Berkas | Isi | Diedit manual? |
|---|---|---|
| `sebelum-sesudah.jsonl` | **SSOT.** Satu baris per skill: skor tanpa/dengan skill, verdik, contoh tugas, tanpa/dengan skill, angka kunci, catatan jujur, tanggal uji. | Ya (hanya berkas ini) |
| `CARA-UJI.md` | Cara uji & arti skor untuk calon pembeli. | Ya |
| `template-halaman.html` | Templat halaman promosi. | Bila desain berubah |
| `SEBELUM-SESUDAH.md`, `halaman-sebelum-sesudah.html` | Dibuat otomatis oleh `python3 scripts/promosi_sebelum_sesudah.py`. | **Tidak** |

Aturan tampil (keputusan pemilik 2026-10-03 + keputusan otomatis 100, 2026-10-16): verdik terakhir LULUS, skor dengan skill ≥ 8, selisih ≥ 1,5, DAN bila ada uji sebelum/sesudah di bot Telegram asli (`telegram_terakhir` — diisi otomatis oleh pemroses gelombang: `ada`, `tanggal`, `gelombang`, `versi_diuji`, `skor_tanpa`, `skor_dengan`, `verdik_aturan` LOLOS/BELUM/TIDAK-DINILAI, `pembeda_awam`, `sumber`), `verdik_aturan` bukan BELUM. Kolom `label` tampil sebagai keterangan di kartu (mis. "Belum direview tenaga medis"). Kolom turunan `selisih` dan `lolos_promosi` diselaraskan otomatis oleh skrip. Teks kartu (`catatan_jujur` dll.) ditulis untuk pembeli awam: tanpa nomor gelombang/keputusan, tanpa nama berkas atau istilah agent, singkatan dijelaskan sekali.

## Artifact yang dibagikan
- Nama: **Bukti Sebelum–Sesudah Komunitech** — https://claude.ai/artifact/6zja3WtPTK7YE3MbDTXUtM (private; pemilik membagikan lewat menu Share).

## Wajib setiap ada uji sebelum/sesudah baru atau uji ulang (skill mana pun)
1. Perbarui/menambah baris skill itu di `sebelum-sesudah.jsonl` dari bagian uji TERAKHIR di `skills/<nama>/examples/00-openclaw-sebelum-sesudah.md` (skor rata-rata terakhir, verdik, ringkasan ≤30 kata, angka yang ada di berkas uji saja, nama/data fiktif saja).
2. `python3 scripts/promosi_sebelum_sesudah.py` (membuat ulang MD + HTML).
3. Commit `promosi: perbarui <nama>`.
4. Terbitkan ulang artifact ke URL yang sama: tool Artifact `publish` dengan `file_path` = `promosi/halaman-sebelum-sesudah.html` dan `url` = URL di atas (sesi lain wajib `read` dulu). Jangan buat artifact baru.

## Pemilihan skill untuk gelombang Telegram (keputusan pemilik 2026-10-03)
Kandidat gelombang Telegram diambil HANYA dari skill yang tampil di `SEBELUM-SESUDAH.md` (lolos uji internal), urut selisih terbesar, dan belum pernah ditampilkan (cek `koordinasi/telegram-*.md`). Utamakan yang mudah dipahami pengusaha awam (angka/aturan yang jelas beda) dan tidak butuh sistem luar. Usulan daftar tetap dikirim ke pemilik dulu; kirim hanya setelah disetujui.
