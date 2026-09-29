# Jadwal cek level harga di OpenClaw (opsional)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

Ditulis 2026-09-29 (v1.0.1; isi pesan per kode diperbarui v1.0.2). **Status: belum diuji di Gateway OpenClaw untuk skill ini.** Bentuk
perintah `automations add` di bawah mengikuti pola yang sudah terbukti jalan di Gateway uji
OpenClaw 2026.9.5 untuk skill Komunitech lain (laporan terjadwal). Bila versi OpenClaw pengguna
berbeda, jalankan `openclaw automations add --help` dulu dan sesuaikan; beri tahu pengguna.

## 1. Kenapa jadwalnya berupa pesan ke agent (bukan script saja)
`scripts/rasio_saham.py` **tidak mengambil harga dari internet**. Jadi setiap giliran jadwal,
agent yang harus: (1) membuka halaman harga publik tanpa login, (2) memperbarui kolom
`harga_sekarang`, `tanggal_harga`, `sumber_harga` di `saham/WATCHLIST.csv`, (3) menjalankan
perintah `level`, (4) melapor sesuai kode keluar. Level di file tetap milik pengguna; agent
tidak boleh mengubah kolom `level_atas`/`level_bawah`.

## 2. Contoh perintah (Telegram ke pemilik sendiri)
```bash
openclaw automations add "10 16 * * 1-5" "Pakai skill riset-saham-berita langkah E: perbarui harga penutupan tiap kode di saham/WATCHLIST.csv dari halaman publik tanpa login (tulis tanggal & sumber), jangan ubah kolom level, lalu jalankan rasio_saham.py level saham/WATCHLIST.csv dan kirim SATU pesan sesuai kode keluar. Kode 0: kirim pendek 'Cek level watchlist <tanggal>: tidak ada level tersentuh.' lalu baris Ringkasan dari script dan kalimat 'Bukan rekomendasi beli/jual.' Kode 2: kirim hasil script apa adanya (baris Ringkasan, tabel, disclaimer). Kode 3: kirim 'Cek level watchlist <tanggal>: ADA BARIS GAGAL DICEK, jangan dianggap aman.' lalu hasil script apa adanya (Ringkasan, tabel, daftar baris gagal, disclaimer). Kode 1: kirim 'Cek level watchlist <tanggal> GAGAL dijalankan (kode 1), tidak ada saham yang dicek:' lalu pesan galat script apa adanya dan saran memeriksa file saham/WATCHLIST.csv. Bila script tidak bisa dijalankan sama sekali: kirim 'Cek level watchlist <tanggal> tidak berjalan:' + alasannya. Tanpa rekomendasi beli/jual." \
  --tz "Asia/Jakarta" --name "Cek level watchlist saham" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- `"10 16 * * 1-5"` = Senin-Jumat 16.10 WIB (setelah penutupan bursa); ubah sesuai keinginan pengguna.
  Hindari jadwal terlalu rapat: halaman publik bisa memblokir akses berulang.
- `--tz "Asia/Jakarta"` wajib, supaya jam mengikuti WIB, bukan zona waktu komputer.
- WhatsApp hanya dengan **nomor terpisah** + persetujuan risiko tertulis pengguna. Tidak ada
  pengiriman ke grup/broadcast.
- **Selalu ada pesan, termasuk saat kode 0** (satu baris pendek "tidak ada level tersentuh").
  Ini disengaja: pemilik tahu jadwalnya benar-benar berjalan, dan diam tidak bisa disalahartikan
  sebagai "aman" saat job gagal. **Jangan** memakai balasan `NO_REPLY` untuk meredam pesan:
  penekanan `NO_REPLY` pada job berbasis pesan agent + `--announce` **belum terbukti** di Gateway
  OpenClaw (bukti di repo hanya untuk pola `--command-argv`), sehingga pemilik bisa menerima teks
  "NO_REPLY" setiap hari bursa. Bila pengguna ingin hanya diberi tahu saat ada kejadian, uji dulu
  dengan `openclaw automations run <id> --wait` pada hari tanpa level tersentuh dan catat hasilnya;
  sampai terbukti, tetap pakai pesan pendek.

## 3. Isi pesan per kode keluar
| Kode | Arti | Pesan yang dikirim |
|---|---|---|
| 0 | Semua baris dicek, tidak ada level tersentuh | Pendek: "Cek level watchlist 30/09/2026: tidak ada level tersentuh." + baris `Ringkasan:` dari script + "Bukan rekomendasi beli/jual." |
| 2 | Ada level tersentuh | Hasil script apa adanya: `Ringkasan:`, tabel (harga, tanggal & sumber, level, status), disclaimer |
| 3 | Ada baris gagal dicek (harga tak terambil/rusak, level kosong/terbalik); bisa sekaligus ada yang tersentuh | **Selalu dikirim**: pembuka "ADA BARIS GAGAL DICEK, jangan dianggap aman" + hasil script apa adanya termasuk daftar baris gagal + disclaimer |
| 1 | File/input salah (file tidak ada/kosong, kolom wajib hilang) | "Cek level watchlist … GAGAL dijalankan (kode 1), tidak ada saham yang dicek:" + pesan galat script apa adanya + saran memeriksa `saham/WATCHLIST.csv` |
| - | Script tidak bisa dijalankan sama sekali (mis. Python tidak ada) | "Cek level watchlist … tidak berjalan:" + alasannya |

Contoh pesan kode 0:
```
Cek level watchlist 30/09/2026: tidak ada level tersentuh.
Ringkasan: 5 saham dicek, 0 menyentuh level Anda, 0 baris GAGAL dicek.
Bukan rekomendasi beli/jual.
```

Bila agent gagal membuka semua sumber harga, ia harus mengosongkan `harga_sekarang` baris itu
(bukan memakai harga lama diam-diam) sehingga script mengembalikan kode 3.

## 4. Cara uji sebelum diaktifkan
1. Jalankan manual sekali: `python3 <folder-skill-ini>/scripts/rasio_saham.py level saham/WATCHLIST.csv; echo $?`
   (Windows PowerShell: `py ...` lalu `echo $LASTEXITCODE`). Pastikan kode 0/2/3 sesuai isi file.
2. Setelah jadwal dibuat, jalankan sekali dengan `openclaw automations run <id> --wait` dan
   periksa pesan di Telegram. Catatan: perintah ini memaksa job berjalan, jadi hanya menguji isi
   pesan, bukan ketepatan jam.
3. Jelaskan cara menjeda/menghapus: `openclaw automations disable <id>` / `openclaw automations rm <id>`.

Bila pengguna tidak memakai OpenClaw (Claude Code, Codex, Cursor), tidak ada jadwal otomatis:
tawarkan perintah "cek level watchlist saya" yang dijalankan manual kapan saja.
