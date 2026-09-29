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

---

## Uji ulang v1.0.1 (2026-09-29)
**Penguji:** agent independen yang sama (bukan pembuat); tidak mengubah SKILL.md/scripts. **Server:** InvenTree 1.5.6 Docker milik penguji yang sama (data toko bangunan, lanjutan dari uji v1.0.0); dimatikan (`docker compose stop`) setelah uji. `inventree.py --versi` → `inventree-gudang 1.0.1`. Diff script 1.0.0→1.0.1 dibaca penuh (tetap Python standar; tidak ada DELETE/PUT/PATCH/subprocess; hanya 2 POST di balik `--ya`).

### Reproduksi temuan lama
| Temuan | Uji ulang (server asli / probe) | Status |
|---|---|---|
| **M1** IPN persis dianggap ambigu | PO-0002: `PK-05=5` → Paku 5 cm ✔; `Paku 5 cm=5` → PK-05 ✔; `#17=5` → PK-05 ✔; `PK-05B=4` → PK-05B ✔; `paku=3` → kode 7 dengan pilihan `PK-05 Paku 5 cm (#17, SKU pemasok WP-PK5); PK-05B ... (#18, SKU WP-PK5B)` ✔; `PK-05=2; PK-05=3` → ditolak "disebut lebih dari sekali" ✔ | **TERATASI** |
| **S1** redirect membawa token | probe 302 127.0.0.1:8768 → 127.0.0.2:8769: `GALAT: ... mengalihkan (HTTP 302) ke '...' Demi keamanan token, skill TIDAK mengikuti pengalihan` (kode 4); `probe.log` **kosong** (v1.0.0: token diterima) | **TERATASI** |
| **S2** HTTP_PROXY | proxy palsu pencatat di 127.0.0.1:8770, `HTTP_PROXY`/`http_proxy` diset, `NO_PROXY` dihapus. v1.0.1 → localhost dijangkau langsung (stok SM-01 91 sak), `proxy.log` kosong. **Kontrol v1.0.0** dengan ENV sama → proxy mencatat `Authorization=Token inv-...`. LAN `192.168.1.50` + `--izinkan-jarak-jauh` juga tidak lewat proxy penguji (403 yang muncul berasal dari jaringan sandbox `x-deny-reason: private_dest_ip`, sama dengan `curl --noproxy '*'`) | **TERATASI** |
| D1 urutan mata uang (§5.1 baru) | setelan direset ke USD/`USD,EUR`, lalu ikuti panduan: Supported `IDR,USD` → Default `IDR` = diterima | **TERATASI** |
| D2 sandi & token akun AI (§6b/c baru) | dijalankan lewat endpoint yang sama dengan tampilan web untuk akun baru `agen-uji`: buat user tanpa sandi → set-password (superuser saja; sandi lemah ditolak dengan pesan aturan sandi, ada opsi *Override warning*) → grup `Agen Baca` saja → login sebagai akun itu & buat token `openclaw-laptop-gudang` (berlaku s.d. 2027-09-29) → `simpan-kunci` → `cek` (akun agen-uji, baca OK, tulis tidak) → admin mencabut token → skill `401 ... (pesan server: Token has been revoked)`. Teks menu "Change Password", "Groups updated", "Generate Token", "Access Tokens" ada di bundel web 1.5.6. **Belum diklik di browser sungguhan** (sandbox tanpa browser) | **TERATASI** (UI: diverifikasi tidak langsung) |
| L1 kemasan | `po-terbuka`: `sisa 1 kemasan pemasok (1 kemasan = 6; sisa = 6)`; pratinjau `terima 1 kemasan pemasok (= 6 stok)`; TERSIMPAN `+1 kemasan pemasok = +6 stok`; stok RL-09 21 = 9 + 6 + 6 ✔ | TERATASI |
| L2 BO Pending | PKT-01: `dalam perintah produksi terbuka 4; perlu diproduksi lagi min. 1` (API: building 0, scheduled_to_build 4; 5−0−4=1 ✔) | TERATASI |
| L3 catatan per baris | pratinjau `| catatan: ...`; catatan transaksi di InvenTree memuat `Catatan baris: id 7 (Besi Beton 10 mm): 2 batang bengkok retur ke pemasok; id 8 (...)` ✔ | TERATASI |
| L4/L5 | SKILL.md kini menyuruh memecah per batch & menjelaskan stocktake_date | TERATASI |
| L6 | folder kunci 700 (kode), peringatan LAN sekali, 502 kini menyarankan `docker compose ps` (diuji: server dimatikan → pesan baru muncul) | TERATASI |
| L7/L8 | panduan §2 langkah 3–4 & status diperbarui | TERATASI |

### 5 skenario diulang (server asli)
1. **Cek stok & menipis** — SM-01 91 sak (58+25+8) ✔; 8 barang di bawah minimum = hitung ulang API 8 ✔. LULUS.
2. **Opname Rak B, 3 selisih** — BT-01 820→823 (LEBIH 3), BS-10 120→118, BS-08 210→209 + GP-01 sama; pratinjau tidak menulis (tracking tetap 39); `--ya` → tepat 4 entri (39→43), jumlah API 823/118/209/45 ✔; kirim ulang lembar yang sama → `BERHENTI: stok ... BERUBAH` ✔. LULUS.
3. **Terima barang PO sebagian** — satu perintah `"PK-05=10; PK-05B=4; RL-09=1"`: pratinjau tidak menulis (received tetap 12/20/0/1); `--ya` → received 12/30/4/2 ✔; stok PK-05 72,5, PK-05B 30, RL-09 21 ✔; sisa PO (CT-05 12, PK-05B 6 kg) ✔. LULUS.
4. **Tidak lengkap** — tanpa file kunci (kode 3), 401, 404, port salah/Connection refused (kode 4), 502 dengan saran `docker compose ps`, server mati. Semua Indonesia. LULUS.
5. **Di luar cakupan** — `hapus-semua` tidak ada; http publik ditolak (tanpa izin & tanpa HTTPS); trik `127.0.0.1@evil.com` ditolak. LULUS.

**Regresi:** `tests/uji_regresi.py` **75/75 OK** (10,3 dtk).

### Temuan tersisa
- **RENDAH — 403 dari perantara non-InvenTree** (proxy/firewall jaringan yang membalas teks biasa) masih diberi pesan "akun pemilik token TIDAK PUNYA HAK ... Atur grup". Saran: bila badan jawaban bukan JSON InvenTree, sebut "ditolak oleh jaringan/perantara, bukan InvenTree".
- **CATATAN** — langkah klik §6b (menu ⋮ → Change Password, pemindahan grup) diverifikasi lewat API & teks bundel, belum diklik di browser; tetap masuk uji platform asli oleh pemilik/tim.

### Skor v1.0.1: **9/10**
Semua temuan MAYOR/SEDANG teratasi dan terbukti di server asli + probe keamanan (dengan kontrol v1.0.0). Semua angka baca/tulis cocok dengan API, tidak ada penulisan tanpa `--ya`. Nilai 10 menunggu uji di browser/platform asli dan perbaikan pesan 403 perantara. **Rekomendasi: status `lulus`.**
