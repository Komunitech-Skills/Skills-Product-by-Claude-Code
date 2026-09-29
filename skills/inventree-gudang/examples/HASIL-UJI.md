# HASIL UJI INDEPENDEN — inventree-gudang v1.0.0 + docs/panduan-inventree.md

- **Penguji:** agent independen (bukan pembuat), Claude Code, 29 Sep 2026. Tidak mengubah SKILL.md/scripts.
- **Lingkungan:** Linux, Python 3.11 (script) ; **InvenTree 1.5.6 ASLI** (rilis terbaru; tag 1.5.6 = tag tertinggi di GitHub) dipasang penguji dari nol di folder baru **mengikuti panduan §2 (Docker resmi)** — jalur yang belum pernah diuji pembuat. Postgres 17, Redis, Caddy, worker; port hanya `127.0.0.1:80/443` (terverifikasi `docker compose ps`). Data fiktif penguji sendiri (toko bangunan, 4 lokasi, 25 barang, batch/kedaluwarsa, 1 BOM + 1 build order, 2 PO, satuan custom `sak`/`dus`, kemasan pemasok 6).
- **Jenis uji:** `claude-code (simulasi agent)` terhadap server asli. Belum: Windows/macOS, Telegram, uji manusia di OpenClaw/Codex/Cursor.

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 01 | Cek stok & menipis (+BOM/produksi) | LULUS — semua angka cocok dengan API |
| 02 | Opname Rak A, 3 selisih, draf→pratinjau→ya | LULUS — tepat 6 entri tracking; pengaman stok-berubah, kirim-ulang, lembar rusak bekerja |
| 03 | Terima barang PO sebagian | LULUS BERSYARAT — angka benar, tapi bug pencocokan IPN (M1) |
| 04 | Token/URL belum ada + 401/403/404/timeout/502/server mati/500 & putus saat menulis | LULUS — pesan Indonesia, kode keluar sesuai tabel SKILL.md |
| 05 | "Hapus semua data" & server jarak jauh | LULUS — ditolak; 2 temuan keamanan lapisan HTTP |
| A/B | tanpa vs dengan skill | Skill jelas lebih baik |
| Pesaing | inventree-mcp resmi (read-only, plugin) | Skill unggul untuk target pasar |
| Regresi | `tests/uji_regresi.py` | **61/61 OK** (7,6 dtk) |

**Tidak ada penulisan tanpa konfirmasi:** diverifikasi di setiap pratinjau (jumlah stok, `received` PO, dan jumlah entri Stock Tracking tidak berubah). Token tidak pernah tercetak utuh (`inv-9b****0929`), tidak ada pencatatan token di file/log selain file kunci 600.

## Audit keamanan script (dibaca penuh, 1.191 baris)
- ✔ Hanya pustaka standar; tidak ada `subprocess`/`os.system`/`eval`/`exec`/hapus file; tidak ada DELETE/PUT/PATCH; hanya 2 POST, keduanya di balik `--ya`.
- ✔ Token: dibaca dari file/ENV, file dibuat `0o600`, peringatan izin longgar, disamarkan di `cek`, tidak masuk pesan galat.
- ✔ `periksa_url`: localhost/127.0.0.1/::1/*.localhost; LAN butuh `--izinkan-jarak-jauh`; internet wajib HTTPS; trik `@`, `#`, `localhost.evil.com` ditolak.
- ✔ Ekspor CSV menetralkan rumus Excel; data InvenTree diperlakukan sebagai data.
- ✘ Redirect & proxy (S1, S2 di bawah).

## Temuan menurut tingkat
### MAYOR
- **M1 — `terima-barang --baris`: IPN persis dianggap ambigu bila menjadi awalan/substring IPN/nama lain.** `PK-05` vs `PK-05B`, "Paku 5 cm" vs "Paku 5 cm Beton" → `GALAT ... Pakai kode (IPN) persis` (kode 7) padahal IPN persis sudah dipakai; `#id` tidak didukung. Jalan keluar hanya SKU pemasok (tidak terdokumentasi). Sangat umum di toko bangunan/distributor (varian ukuran). **Perbaikan:** dahulukan kecocokan persis IPN → nama → SKU, baru substring; dukung `#id` barang; tampilkan SKU di pesan pilihan. Tambah uji regresi.
### SEDANG
- **S1 — Redirect membawa token ke host yang ditolak `periksa_url`** (dibuktikan: 302 dari 127.0.0.1 → 127.0.0.2, header `Authorization: Token inv-…` diterima). Juga bisa menurunkan HTTPS→HTTP. **Perbaikan:** tolak redirect (handler khusus) atau validasi ulang + hapus Authorization.
- **S2 — `HTTP(S)_PROXY` lingkungan dipakai otomatis** (urllib); token ke LAN/localhost bisa lewat proxy kantor, dan 403 dari proxy dilaporkan sebagai masalah hak akun. **Perbaikan:** `ProxyHandler({})` untuk alamat lokal/LAN (atau selalu, kecuali opsi eksplisit).
- **D1 — Panduan §5.1 urutan salah:** mengisi *Default Currency = IDR* sebelum *Supported Currencies* ditolak InvenTree 1.5.6 ("Chosen value is not a valid option"; diuji). Tukar urutan: isi Supported Currencies `IDR,USD` dulu, simpan, baru Default Currency.
- **D2 — Panduan §6b/c: cara akun `agen-baca`/`agen-gudang` mendapat sandi untuk login & membuat token tidak dijelaskan** (form tambah pengguna tidak meminta sandi; penguji harus menyetel sandi lewat `manage.py shell`). PERLU CEK di tampilan web 1.5.6 (mis. Admin Center → Users → set password, atau admin membuat token untuk pengguna lain) lalu tulis langkahnya.
### RENDAH
- L1 `po-terbuka` menampilkan jumlah dalam kemasan pemasok tanpa keterangan (RL-09 "dipesan 2" vs `stok-menipis` "sedang dipesan 12"); TERSIMPAN menulis "+1" padahal stok +6.
- L2 `stok-menipis`: build order Pending tidak dihitung (`building`=0) → "perlu diproduksi lagi min. 5" walau BO-0001 (4) ada; sebutkan produksi terbuka di baris itu.
- L3 Kolom `catatan` per baris lembar opname diabaikan diam-diam (tidak di pratinjau, tidak dikirim).
- L4 `--batch`/`--kedaluwarsa` berlaku ke semua baris; SKILL.md sebaiknya menyuruh agent memecah per batch (penguji melakukannya).
- L5 SKILL.md "semua item dicatat sebagai hasil hitung": riwayat ya, tetapi `stocktake_date` InvenTree hanya berubah untuk item yang jumlahnya berubah.
- L6 Folder `~/.komunitech` dibuat 755 (file 600 sudah benar); PERINGATAN http-LAN tercetak dua kali; pesan 502 bisa menyarankan `docker compose ps`.
- L7 Panduan §2 langkah 3 `invoke update` memasang ulang paket Python di dalam kontainer (butuh internet, >10 menit di uji ini; di sandbox gagal karena proxy TLS — bukan masalah pengguna biasa). Tambahkan "butuh internet, bisa 5–15 menit". Langkah 4 (`invoke superuser`) interaktif — sebutkan bahwa sandi tidak terlihat saat diketik.
- L8 Informasi status: pembuat menulis "Docker belum diuji" — penguji kini **menjalankan jalur Docker resmi** sampai `docker compose up -d` & semua perintah skill terhadapnya (kecuali bagian pip-install di `invoke update`, diganti `invoke migrate` + `invoke static` karena batas sandbox). Pembuat boleh memperbarui klaim dengan keterangan ini.

## Catatan pengalaman pengguna awam (mengikuti panduan)
- §2: file resmi persis seperti dijelaskan (baris `#INVENTREE_HTTP_PORT` memang diawali `#`; tidak ada skrip unduh-lalu-jalankan). Mengedit `.env` di terminal adalah langkah tersulit bagi awam — sarankan contoh `nano .env`/Notepad.
- §4 pengamanan terbukti efektif (port hanya 127.0.0.1).
- §5.3 custom unit `sak`/`dus` berhasil dan tampil benar di skill.
- §6 grup & peran sesuai tabel; hak diterapkan langsung (worker menyala di Docker); `cek` menampilkan hak dengan benar untuk kedua akun.

## Skor: **8/10**
Alasan: diuji terhadap InvenTree asli (Docker resmi) dengan data independen — semua angka baca & tulis tepat, pengaman tulis (pratinjau, `--ya`, stok-berubah, anti kirim-ulang, kode 8 saat tidak pasti) bekerja nyata, pesan galat Indonesia jelas, unggul jelas atas tanpa-skill dan atas MCP resmi untuk target pasar. Dikurangi karena M1 memblokir skenario inti untuk data yang umum, dan dua celah HTTP (S1, S2) pada skill yang memegang token tulis.
**Rekomendasi:** perbaiki M1, S1, S2, D1 (+ D2 setelah dicek) → jalankan ulang regresi + uji ulang singkat skenario 03 dan redirect oleh penguji independen, lalu status `lulus`.
