# HASIL UJI INDEPENDEN - fider-masukan-pelanggan v1.0.0
Penguji: agen terpisah (Tahap 6), 2026-09-29. Hanya membaca folder skill, docs/panduan-fider.md, CLAUDE.md. Fider v0.38.0 ASLI dijalankan ulang (Docker + PostgreSQL 17, port 3100, SMTP tiruan), termasuk akun Administrator dan akun Collaborator sungguhan. `validate.py --skill` lulus; 24 uji regresi maker lulus.

## Skor: 7 / 10 (lulus BERSYARAT; perbaiki butir WAJIB sebelum beta)
A/B menang, banding pesaing menang (tanpa batas skor 6). Nilai dipotong karena satu celah gerbang tulis, satu celah cek HTTPS, dan deteksi duplikat yang salah sasaran.

## Ringkasan skenario (bukti di examples/06-15)
| # | Skenario | Hasil |
|---|---|---|
| 06 | Impor WA | Lulus. HP +62/wa.me/email disamarkan. Telepon rumah, nama, alamat, IG tidak. |
| 07 | Tag + gabung | Lulus (pratinjau, idempoten, induk duplikat ditolak, suara pindah). |
| 08 | Status + ringkasan + draf | Lulus dengan catatan draf (lihat M5). Ringkasan sama untuk Administrator dan Collaborator. |
| 09 | Input tidak lengkap | Lulus, satu bug (S3). |
| 10 | Di luar cakupan | Lulus: tidak ada perintah suara/hapus/pengaturan. Celah halus S6. |
| 11-12 | Data rusak/besar | Lulus: kunci salah (3), server mati (4), HTTP (2), 500/429/HTML/redirect (5/4), status asing (2), 60 butir (2), JSON rusak (6), biner (6), 5,5 MB diterima. |
| 14 | Gerbang tulis | 8 perintah tulis tanpa `--ya` = basis data tidak berubah (dicek lewat SQL). ENV/pipe tidak melewati. **Tetapi `--y` menulis.** |
| 15 | Collaborator asli | tag, gabung, status, komentar, ringkasan berhasil; tag-buat ditolak (7) sesuai panduan. |

## Audit
- Format: frontmatter hanya name+description; SKILL.md 85 baris; lintas-OS; Python standar; tidak ada os.system/subprocess/eval/socket. Kunci tidak muncul di keluaran/berkas contoh (dicek).
- Lisensi: ATTRIBUTION.md benar (Fider AGPL-3.0 dipakai terpisah lewat API, tidak disertakan, "tidak berafiliasi"). Baik.
- Panduan vs docs.fider.io (WebFetch): BASE_URL/DATABASE_URL/JWT_SECRET/EMAIL_NOREPLY/SMTP, postgres:17, port 3000, HTTPS disarankan, API key di Settings > API Key, Bearer, hanya Collaborator/Administrator: cocok. Selisih: docs memakai `getfider/fider:stable` (panduan mengunci v0.38.0, ok, tetapi cek tag saat rilis); docs mencantumkan `EMAIL_SMTP_ENABLE_STARTTLS` (panduan tidak; belum terverifikasi perlu untuk penyedia nyata); menu Settings > Privacy/Moderation tidak terverifikasi dari docs. Docs juga punya `X-Fider-UserID` (impersonasi admin) - tidak dipakai, baik.

## Daftar perbaikan
WAJIB
- **M1 (gerbang):** argparse menerima singkatan: `status 5 ditolak --y` MENULIS. Set `allow_abbrev=False` di semua parser/subparser.
- **M2 (keamanan):** `host_lokal` memakai regex `^(10\.|192\.168\.|172\.16-31\.)` pada NAMA host, jadi `http://10.contoh.com` / `192.168.evil.com` lolos sebagai "lokal" dan kunci terkirim lewat HTTP. Periksa sebagai alamat IP (`ipaddress`), bukan awalan teks. Berlaku juga di `simpan-alamat`.
- **M3 (dedup):** ambang 60% salah menandai permintaan BERBEDA sebagai duplikat lalu LEWATI: "Tambah pembayaran GoPay/ShopeePay" dilewati karena mirip QRIS, "Notifikasi email" karena mirip "Notifikasi WA" (data 13). Sementara sinonim ("Bayar QRIS" vs "Tambah pembayaran QRIS") lolos. Ubah bawaan jadi "tandai, jangan lewati" atau sediakan `--tetap` per nomor butir; jelaskan di SKILL.md bahwa agen wajib menilai maksud.
- **M4:** penyamaran tidak menutup telepon rumah/kantor (021-5551234). Tambah pola, atau tulis tegas di SKILL.md/README.
SEDANG
- **M5:** `draf-balasan` untuk pos berstatus "Sedang dikerjakan" tetap menulis "telah selesai kami perbaiki"; judul mentah ("...minta 4 orang") dikutip ke pelanggan; salam "Selamat siang" tetap. Tolak/ganti teks bila status bukan Selesai; sarankan agen menulis ulang judul.
- **S1:** `impor <berkas kunci>` mencetak isi kunci di pratinjau (kunci tercetak 1x) dan bisa menulisnya ke papan publik. Tolak jalur di `~/.komunitech`/berkas yang isinya sama dengan kunci; terapkan `samarkan()` pada semua keluaran.
- **S2:** `cek` menyebut Collaborator sebagai "Administrator" (v0.38.0 mengizinkan Collaborator membaca /api/v1/users). Deteksi lewat cara lain, atau tulis "peran tidak dapat dipastikan".
- **S3:** berkas berisi butir kosong ("-") menghasilkan pos berjudul "-". Buang butir tanpa huruf/angka.
- **S4:** timeout 20 dtk (baik), tetapi uraian 5,5 MB diterima klien; beri batas (mis. 5.000 huruf). `simpan-kunci` tanpa terminal menampilkan traceback EOFError.
- **S5:** `--catatan` pada status/gabung tidak melewati penyamaran HP/email (hanya `komentar` yang melewati).
- **S6 (anti-manipulasi):** `pelanggan` di JSON menghasilkan "Dilaporkan oleh sekitar 9.999 pelanggan" tanpa verifikasi; `status ditolak` tanpa catatan dan `gabung` ke pos tak terkait bisa menyingkirkan keluhan. Tambah larangan eksplisit di SKILL.md (jumlah pelanggan hanya dari catatan asli; tolak/gabung hanya dengan alasan dan konfirmasi terhadap isi kedua pos), dan wajibkan `--catatan` untuk `ditolak`.
- **S7:** pesan galat Fider dari server tidak diterjemahkan ("This has already been posted before").
RENDAH
- Panduan: tambahkan `EMAIL_SMTP_ENABLE_STARTTLS` bila perlu untuk port 587 dan verifikasi; sebut tag `stable` vs versi terkunci.
- Belum diuji siapa pun: Windows/macOS, HTTPS VPS, OpenClaw jadwal + Telegram, Codex/Cursor. `platform_teruji` jangan diisi lebih dari simulasi agen.

## Catatan uji
Data uji pribadi hanya fiktif. Instans uji: proyek Docker `ujifider` (port 3100) masih menyala; hentikan dengan `docker compose -p ujifider down -v` di scratchpad `uji-fider/`.
