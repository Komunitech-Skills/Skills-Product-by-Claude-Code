# Uji ulang v1.0.2 — pantau-pasar-kripto (2026-09-24)

- **Penguji:** agent penguji independen (bukan pembuat/perbaikan skill), sesi terpisah.
- **Lingkungan kerja:** `<folder uji sementara>/uji-kripto/` (`kripto/`, `migrasi/`, `pulih/`, `elif/`, `live/`, `home/` untuk OpenClaw). Python 3.11. OpenClaw **2026.9.6 (eb377ac)** (sudah terpasang di `/tmp/uji-openclaw`, dipakai ulang; tidak dipasang ulang). Gateway uji baru dijalankan khusus sesi ini (`--dev --allow-unconfigured --bind loopback`, port 19881, HOME scratchpad sendiri, tanpa model AI/kanal login sungguhan).
- Data harga: **fixture lokal** (`--harga-file`) untuk semua skenario reliabilitas; **1 pemanggilan nyata** ke CoinGecko (batch 1 permintaan, 2 koin) + **1 ke Indodax** untuk memastikan format respons publik belum berubah — tidak lebih.

## 1. Regresi otomatis
- `python3 tests/uji_regresi.py` → **92 tes OK** (naik dari 75 di v1.0.1; +17 tes baru S2-1/S2-2/S2-3, jaringan/zona waktu).
- `python3 scripts/validate.py` → ✅ 58 skill valid (termasuk pantau-pasar-kripto).
- `bash scripts/uji_openclaw.sh` → `eligible 58/58`, `modelVisible 58/58`, `commandVisible 58/58`.

## 2. Verifikasi klaim S2-1 (anti-spam per jenis ambang)
Konfigurasi 1 koin (BTC) dengan `ambang_turun_persen` + `ambang_harga_di_bawah`. Direproduksi via **CLI langsung dan via OpenClaw Gateway sungguhan** (`automations add --command-argv ... --command-cwd ...` lalu `automations run --wait` dua kali berurutan pada job yang sama).
- Giliran 1 (harga turun ke bawah kedua ambang sekaligus): kedua `>> AMBANG TERLEWATI` tampil, exit 2, Gateway: `deliveryStatus not-delivered` hanya karena token Telegram uji kosong (bukan bug — didokumentasikan).
- Giliran 2 (kondisi identik): **NO_REPLY** — anti-spam bekerja, tanpa upaya kirim (`deliverySuppressionReason: "silent"`).
- `state.json` hasil run memakai kunci baru persis `bitcoin_idr_coingecko#0#turun`, `#0#di_bawah`, `#0#naik`, `#0#pemantauan` — sesuai klaim.
- Kasus kritis (satu jenis ambang lama diredam, ambang lain baru terlewati di koin sama): direproduksi via `unittest` bawaan (test_76/77) — **lulus**, tidak diulang manual karena sudah tercakup penuh.
**Status: TERBUKTI BENAR.**

## 3. Verifikasi klaim S2-2 (pemantauan buta + "PEMANTAUAN PULIH")
Direproduksi langsung (`scripts/cek_ambang.py`, koin SOL, sumber gagal total 2x lalu pulih):
- Giliran 1 (gagal total baru): exit 3, "TIDAK BISA DICEK", `perlu_lapor_pemantauan=true`.
- Giliran 2 (masih gagal, segera): exit 0, tetap tercatat `pemantauan_bermasalah=true` tapi diredam (fakta vs status lapor terpisah, sesuai desain).
- Giliran 3 (sumber pulih): exit 3, baris `✅ PEMANTAUAN PULIH`, `pemantauan_pulih=true`.
Uji tambahan: cache basi tanpa dasar % (kombinasi ambang harga terlewati + "tidak bisa dicek" pada koin yang sama) — **bug lama `elif` yang menyembunyikan "tidak bisa dicek" sudah tidak ada**, kedua baris tampil bersamaan.
**Status: TERBUKTI BENAR.**

## 4. Verifikasi klaim S2-3 (`--command-argv` + `--command-cwd`)
`openclaw automations add --help` (biner sungguhan) mengonfirmasi kedua flag persis ada dan berfungsi seperti didokumentasikan (`--command-argv <json>` argv array, `--command-cwd <path>`), berbeda dari `--command <shell>` (dijalankan `sh -lc`). Dibuat & dijalankan job sungguhan di Gateway dengan pola dokumen persis (lihat §2) — job "exec" tercatat menjalankan `argv` langsung (bukan lewat shell), keluaran tenang persis `"NO_REPLY"` tanpa kontaminasi apa pun. Dokumen tidak lagi memuat klaim kontradiktif "belum dicoba" untuk kombinasi ini (dicek juga oleh `test_90/91/92`).
**Status: TERBUKTI BENAR** (Linux; Windows tetap ditandai "S" sesuai dokumen, jujur apa adanya).

## 5. Skenario keandalan tambahan
| Skenario | Hasil |
|---|---|
| Migrasi state.json v1.0.1 → v1.0.2 (kunci lama tanpa label ambang) | Kunci lama diabaikan (format beda), kondisi yang sedang terlewati dilaporkan **ulang sekali** di jalan pertama pasca-upgrade, lalu anti-spam normal di jalan kedua — persis sesuai catatan migrasi di SKILL.md. |
| Tengah malam WIB (jeda anti-spam & `usia_jam` lintas pergantian tanggal) | +1j05m lintas tengah malam → diredam (benar); +7j05m → lapor ulang (benar); `usia_jam` 23:30→00:15 = 0,75 jam (benar). |
| Jaringan mati/timeout, respons rusak | Sudah tercakup regresi lewat mock `urlopen` (timeout 3x retry, URLError pulih di percobaan ke-2, respons CoinGecko/Indodax tanpa field yang diminta → dianggap gagal, bukan dipakai apa adanya) — tidak diulang manual (hemat kuota, sesuai instruksi). |
| Harga melompat lewati beberapa ambang sekaligus (turun % + harga absolut) | Kedua ambang dilaporkan independen, tidak saling menutupi (lihat §2). |
| Notifikasi ganda jadwal berurutan | Dikonfirmasi sungguhan di Gateway (§2) dan unit test — aman. |
| Pulih setelah gagal | Dikonfirmasi sungguhan (§3). |
| Panggilan nyata CoinGecko (batch 2 koin) + Indodax | Berhasil, format field (`last_updated_at`, `_24h_change`, `ticker.last`) masih sama seperti diasumsikan skrip — tidak ada error parsing. |

## 6. Batas cakupan (tidak berubah dari v1.0.1, dicek ulang lewat diff)
`git diff` SKILL.md v1.0.1→v1.0.2 hanya menyentuh bagian anti-spam/exit-code (Langkah A.5–A.6) — bagian "Batas Tegas" #1/#2 dan "Kapan TIDAK digunakan" **tidak berubah sama sekali**, jadi perilaku "belikan BTC kalau turun 5%" dan "koin mana yang harus saya beli?" tetap mengikuti aturan yang sudah lulus regresi v1.0.1 (scenario 05, tanpa regresi): ditolak sopan, alasan dijelaskan (risiko prompt injection/kerugian tak bisa dibatalkan/kredensial), alternatif ditawarkan (data/checklist riset, limit order bawaan exchange resmi), disclaimer "Informasi, bukan nasihat investasi" tetap wajib di semua keluaran.

## 7. Verifikasi hukum & jurnal
Tidak diuji ulang (file `regulasi.md`, `hitung_pl_jurnal.py`, `checklist-riset.md` **tidak berubah** di commit ini menurut `git diff --stat` — hanya `SKILL.md`, `references/openclaw-jadwal.md`, `scripts/cek_ambang.py`, `tests/uji_regresi.py` yang tersentuh). Hasil verifikasi v1.0.1 (data OJK/pajak.go.id, FIFO P/L) tetap berlaku.

## Skor v1.0.2
| Kriteria | v1.0.1 | v1.0.2 |
|---|---|---|
| Keandalan notifikasi otomatis | 6 | **9** (S2-1/S2-2/S2-3 semuanya terbukti benar via reproduksi independen + Gateway sungguhan) |
| Lainnya (pemicu, kemudahan, akurasi, batas cakupan, keamanan) | tidak berubah | tidak berubah (tidak ada file yang menyentuhnya) |

## SKOR AKHIR v1.0.2: 9/10 — LULUS, SIAP NAIK KE BETA
Ketiga cacat sedang v1.0.1 (S2-1, S2-2, S2-3) diperbaiki dan **terbukti** lewat reproduksi independen (unit test + Gateway OpenClaw sungguhan, bukan hanya klaim dokumen). Tidak ditemukan regresi pada bagian yang tidak diklaim berubah (batas etika, jurnal, regulasi tidak disentuh). Cacat ringan yang tersisa hanya kosmetik/dokumentasi (lihat bagian bawah), tidak menghalangi beta.

### Cacat tersisa (RINGAN, tidak menghalangi beta)
- Field `perubahan_24jam_persen` bernilai `null` untuk sumber Indodax tetap tidak dijelaskan di `pesan_singkat` itu sendiri (hanya di `ambang_tidak_bisa_dicek` kalau ada ambang % yang dikonfigurasi) — anggota tim boleh menambah catatan singkat "Indodax tidak menyediakan data 24 jam" langsung di baris harga suatu saat, tapi tidak menyesatkan sebagaimana adanya sekarang.
- Windows untuk `--command-argv` masih berstatus "S" (belum diuji mesin Windows sungguhan) — sudah diakui jujur di dokumen, disarankan tetap diuji sebelum diklaim penuh ke pembeli Windows di Tahap 6.10 (uji platform asli oleh pemilik/tim).
