# HASIL UJI ULANG INDEPENDEN - fider-masukan-pelanggan v1.0.1
Penguji: agen terpisah (Tahap 6, uji ulang), 2026-09-29. Hanya membaca folder skill, docs/panduan-fider.md, CLAUDE.md. Fider v0.38.0 ASLI di port 3100 (proyek `ujifider`) sedang menyala dan dipakai (akun Collaborator/Administrator). `validate.py --skill fider-masukan-pelanggan` lulus; 37 uji regresi maker lulus (33 dtk). Tidak ada kunci yang dicetak (semua keluaran uji disaring). Data uji fiktif. Basis data uji sengaja ditulis: pos #11 dan #12 dibuat oleh uji M3.

## Skor: 8 / 10 (LULUS; siap uji platform asli setelah butir kecil di bawah)
Semua butir WAJIB (M1-M4) terbukti bekerja. Nilai tidak 9 karena masih ada celah penyamaran kecil (termasuk satu celah baru pada `--sumber`), satu traceback, dan pendeteksi sinonim yang terbatas.

## Hasil per perbaikan
| Butir | Hasil | Bukti |
|---|---|---|
| M1 singkatan opsi | LULUS | `--y`, `-y`, `--ye`, `--ya=1`, `--tet`, `--hapus`, `--su`, `--js` ditolak (kode 2) di status, gabung, tag, tag-buat, komentar, impor. Snapshot basis data (nomor, status, suara) sebelum dan sesudah identik. |
| M2 host HTTP | LULUS | Ditolak (wajib HTTPS) lewat `--url`, ENV `FIDER_URL`, dan `simpan-alamat`: `10.contoh.com`, `192.168.evil.com`, `127.0.0.1.nip.io`, `localhost.evil.com`, `2130706433`, `0x7f.0.0.1`, `127.1`, `0177.0.0.1`, `010.0.0.1`, `[::ffff:10.0.0.1]`, `172.32.x`, `172.15.x`, `169.254.x`, `100.64.x`, `0.0.0.0`, `fe80::`, `.local`, `localhost@evil.com`, `evil.com#@localhost`, `user:p@localhost`. Diterima: `localhost`, `LOCALHOST:3100`, `127.0.0.1`, `[::1]`, `10.0.0.5`, `172.16.0.1`, `192.168.1.1`, `[fd00::1]`. Cacat kecil di bawah (K1). |
| M3 duplikat | LULUS (dengan catatan) | 10 butir uji: GoPay, ShopeePay, "email" vs "WA", Excel vs PDF tidak lagi ditahan. "Bayar QRIS" = 100% (ditahan), "Print struk..." vs "Cetak resi..." 80% (ditahan), "Dark mode" vs "Mode gelap" 100%. Butir ditahan TIDAK ditulis; `--ya` menulis hanya butir non-tahan (dicek: #11, #12 dibuat, "Bayar QRIS" tidak). `--tetap 1,9`, `--tetap semua` benar; `--tetap 99` ditolak. Diulang: 3 butir kini ditahan sebagai duplikat pos yang baru dibuat (idempoten). `gabung` tanpa `--ya` tidak menulis; pratinjau memuat uraian kedua pos, "PERIKSA...", dan PERINGATAN bila judul tak mirip (#12 ke #5). Gabung ke diri sendiri/nomor salah/huruf ditolak. |
| M4 penyamaran | LULUS untuk format utama | Tertutup: HP `0812-3456-7890`, `081234567890`, spasi, titik, `+62 812-...`, `+6281...`, `6281...`, wa.me/62..., telepon rumah `021-5551234`, `021 555 1234`, `(021) 555-1234`, `(0274) 555123`, `+62 21 5551234`, `+62 (21) 555 1234`, dan yang tertanam dalam kalimat ("hubungi Budi 0812-... ya", "telp:021-5551234.", "No.HP:0812..."). Tidak salah menutup: Rp 1.500.000, tanggal, jam, NPWP, rekening 10 digit, "stok 0812". Lubang di bawah (K2-K5). |
| S1 | LULUS | `impor <berkas kunci>`, salinan kunci, kunci di dalam butir, kunci diberi tanda kutip, berkas di `~/.komunitech`, symlink ke kunci: semua ditolak tanpa mencetak kunci; `--json` juga bersih. Sisa: awalan kunci (20 huruf) tidak dianggap kunci (rendah). |
| S2 | LULUS | `cek`: "Collaborator atau Administrator (peran pastinya tidak dapat dipastikan)". |
| S3 | LULUS | "-", "* --", "- ..." dibuang; "123" dan "Ok" dipertahankan; berkas semua kosong = galat jelas. |
| S4 | LULUS | Uraian 20.000 huruf dipotong 5.000 dengan pemberitahuan; `simpan-kunci` tanpa terminal = pesan jelas, tanpa traceback. |
| S5 | LULUS | `--catatan` pada status/gabung disamarkan, dengan penghitung. |
| S6 | LULUS sebagian | `status ditolak` tanpa catatan / catatan spasi ditolak (juga `tolak`, `DECLINED`). Klaim `pelanggan` ditandai "tidak diverifikasi" di pratinjau; nilai non-angka ditolak. Namun catatan sepele ("-", "ok") lolos, dan `pelanggan` -5 atau 99999999999999999999 diterima (K6). |
| S7 | LULUS | Judul sama: "Usulan dengan judul yang sama sudah ada di Fider." (bukan pesan Inggris mentah). |
| M5 (draf) | LULUS | Pos "Sedang dikerjakan" dan "Terbuka" tidak lagi ditulis "selesai"; ada peringatan; salam "Halo"; `--topik` mengganti judul mentah; gaya santai jalan. |
| Aturan SKILL.md 1-8 | Sesuai | Perilaku script cocok dengan aturan tertulis (pratinjau dulu, anti-manipulasi, tetap perlu konfirmasi gabung). |

## Cacat yang masih ada (tidak ada yang menghalangi kelulusan)
**Sebaiknya diperbaiki sebelum beta**
- **K3 (baru, kebocoran data):** `--sumber "WA dari 0812-3456-7890"` TIDAK disamarkan; nomor tertulis apa adanya di uraian pos publik (pratinjau juga menampilkannya). Samarkan `sumber` seperti judul/uraian.
- **K2 (penyamaran):** tidak tertutup: `(+62) 812 3456 7890`, `62 21 5551234` (tanpa plus), `kontak0812-3456-7890` (menempel huruf), `0812 - 3456 - 7890` (tanda hubung berspasi), `0812–3456–7890` (en dash), `0812/3456/7890`, `tel:+622155512`. `0896 1234 5678 9` menyisakan satu digit "9". SKILL.md sudah menyuruh pemilik memeriksa pratinjau, tetapi bagian yang tertulis "otomatis" agak berlebihan.
- **K4:** judul pos LAMA yang sudah memuat HP/email (data #7, #8, #9 dari uji lama) tampil apa adanya di `ringkasan-mingguan`, `daftar`, pratinjau `gabung`, dan dikutip di `draf-balasan`. Terapkan `samarkan_pribadi` saat menampilkan/mengutip judul dan uraian pos.
**Rendah**
- **K1:** `--url "http://[::1]evil"` melempar `ValueError` (traceback) dari `periksa_url`; tangkap dan ubah menjadi galat kode 2. `http:// localhost` (spasi) lolos periksa (tidak berbahaya, koneksi gagal).
- **K5:** `http://[::1]` diterima tetapi di kontainer uji gagal terhubung (bukan kesalahan skill).
- **K6:** validasi `pelanggan`: tolak angka negatif/nol/tidak wajar (mis. > 1.000) atau minta konfirmasi; tolak catatan tolak yang tidak bermakna.
- **K7 (M3 residu):** sinonim terbatas. Tidak dianggap mirip: "Ongkir ke Papua" vs "Ongkos kirim ke Papua" (29%), "Pembayaran lewat QR code" vs QRIS, "Kirim notif WhatsApp saat paket berangkat" vs "Notifikasi WA ... dikirim" (33%). Sebaliknya "Ongkir ke Papua" vs "Ongkir ke Bali" 67% dan "QRIS BCA" vs "QRIS" 67%, tetapi hasilnya hanya TAHAN (aman, bukan dilewati). Aturan SKILL.md 8 (agen menilai maksud) menutup celah ini; pastikan agen memang membandingkan judul, bukan hanya mengandalkan skor.
- Pesan `--tetap` harus ditulis setelah nama berkas: `impor --tetap berkas.txt` menelan nama berkas dengan pesan argparse Inggris (rendah).

## Belum diuji (dan jangan diklaim)
Windows/macOS, HTTPS di VPS sungguhan, OpenClaw jadwal + Telegram, Codex/Cursor, Fider selain v0.38.0. `platform_teruji` tetap hanya simulasi agen.
