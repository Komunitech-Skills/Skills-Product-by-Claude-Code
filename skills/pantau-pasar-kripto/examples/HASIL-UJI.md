# HASIL UJI — pantau-pasar-kripto v1.0.0

- **Tanggal:** 2026-09-24 (07:30–08:10 WIB, data pasar nyata)
- **Penguji:** agent penguji independen (simulasi, Claude Code) — bukan pembuat skill; hanya membaca folder skill + CLAUDE.md + brief uji.
- **Lingkungan:** Python 3.11; jaringan lewat proxy (CoinGecko publik & Indodax publik); OpenClaw **2026.9.5 (ec9c1a1)** dengan Gateway lokal (`gateway run --allow-unconfigured --bind loopback --token …`, HOME sementara `/tmp/uji-kripto-oc/home`, tanpa model AI & tanpa kanal login). Berkas kerja: `/tmp/uji-pantau-pasar-kripto/`.
- **Tes bawaan:** `python3 tests/uji_regresi.py` → **40 tes OK**.
- **Audit keamanan:** tidak ada API key/token, tidak ada pembacaan kredensial, tidak ada perintah destruktif, tidak ada prompt injection. Jaringan hanya ke `api.coingecko.com` & `indodax.com` (endpoint publik, hanya kode koin yang dikirim) — sesuai yang diungkap di SKILL.md. ✅

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B tanpa skill vs dengan skill | Dengan skill jelas lebih baik (tanpa harga karangan, tanpa sinyal/alokasi/auto-trade) |
| 00 | Banding pesaing (portfolio-watcher 10k unduhan, Crypto Market CCXT 4,8k) | Kita menang 22 vs 12 vs 9 |
| 01 | BTC/ETH/SOL, ambang %/Rp, data nyata + `--harga-file`, ringkasan pagi | Harga script = cek manual endpoint (identik). Berita 3 tautan nyata & sesuai. Terkena 429 CoinGecko di percobaan awal. |
| 02 | Jurnal 12 transaksi, FIFO | Semua angka cocok dengan verifikasi `Fraction` independen (total +Rp 2.828.214) |
| 03 | Riset token ramai (PONS) | Fakta bersumber, kolom kosong jujur, tanpa kesimpulan beli/jual |
| 04 | "pantau kripto saya" | Tanya sekali, 5 butir bernomor |
| 05 | 5 permintaan terlarang | Semua ditolak tegas + alternatif |

## Uji script — data rusak / tepi
**cek_ambang.py**
| Kasus | Hasil | Sesuai dokumen? |
|---|---|---|
| Konfigurasi JSON rusak | exit 1, JSON `status:error` | ✅ |
| Koin tak dikenal (id CoinGecko salah, online) | `gagal_total`, exit 3, tanpa angka | ✅ |
| Timeout (server lokal yang tidak pernah menjawab) | 3 koin `gagal_total` "timed out", exit 3; ±38 dtk (8 dtk × 2 percobaan × koin) | ✅ |
| Rate limit CoinGecko 429 (nyata) | koin ke-3 gagal / jatuh ke cache | ⚠️ lihat S-2 |
| Cache dipakai | harga lama ditampilkan, ambang persen **tidak dicek**, pesan tetap "Tidak ada ambang yang terlewati" | ⚠️ S-1 |
| Data "hidup" berumur 96,7 jam (`--harga-file`) | status `hidup`, **tanpa peringatan**, memicu notifikasi | ⚠️ R-1 |
| Ambang `"5%"` (string) atau `"1.450.000.000"` | **traceback** Python (`TypeError`) | ❌ R-2 |
| Ambang naik −5, ambang 0 | diterima tanpa peringatan | ⚠️ R-2 |
| `mata_uang: eur` | exit 1 pesan jelas | ✅ |
| `state.json` berisi daftar | exit 1 → seluruh pemantauan berhenti sampai file diperbaiki | ⚠️ R-3 |
| Koin sama dengan 2 sumber (CoinGecko & Indodax) | kunci cache bentrok (`bitcoin_idr`), cache CoinGecko tertimpa harga Indodax | ⚠️ R-3 |
| Ambang terlewati + koin gagal total bersamaan | exit 2 (gagal total tertutupi) | ⚠️ S-1 |
**hitung_pl_jurnal.py:** lihat tabel di contoh 02 (format ID harga ✅, `jumlah_koin` "0,005" ❌ ditolak, CSV `;` ditolak, file kosong → pesan "tidak ditemukan", `--hari-ini` salah → traceback, jual melebihi saldo ✅ dilaporkan).

## Uji OpenClaw (`references/openclaw-jadwal.md`) — CLI & Gateway asli
1. **Opsi A persis seperti di dokumen → GAGAL dua kali:**
   - `--every 1h … --tz "Asia/Jakarta"` → `--tz is only valid with --cron or offset-less --at`.
   - Tanpa `--tz`: `--trigger-script …/trigger_ambang.sh` → `invalid cron.add params: cron trigger script has a syntax error: Unexpected character '!' (line 1, column 1)`. Menurut dokumentasi bawaan OpenClaw (`docs/automation/cron-jobs/schedules.md` §Event triggers), trigger script adalah **skrip JavaScript code-mode** yang memanggil `exec(...)` dan mengembalikan `json({ fire, message?, state? })` — **bukan** shell script dengan kode keluar.
   - `automations run <id> --wait` **mengabaikan** trigger (paksa jalan) — jadi saran dokumen "uji dengan run --wait untuk melihat apakah trigger bekerja" tidak valid.
2. **Pola yang TERBUKTI jalan di Gateway uji (untuk perbaikan):**
   - **Command payload + `NO_REPLY`** (paling sederhana, tanpa model): `automations add --cron "0 * * * *" --tz Asia/Jakarta --command "<wrapper.sh>"` di mana wrapper menjalankan `cek_ambang.py`, mencetak `pesan_singkat` bila exit 2/3, selain itu mencetak `NO_REPLY`, dan selalu `exit 0`. Hasil `run --wait`: status `ok`, keluaran berisi pesan saat ambang terlewati; `NO_REPLY` saat tenang (dokumentasi OpenClaw: `NO_REPLY` = tidak memposting apa pun).
   - **Catatan penting:** menjalankan `cek_ambang.py` langsung sebagai `--command` → exit 2 dicatat Gateway sebagai **`error` ("command exited with code 2")** dan bisa memicu failure alert.
   - **Trigger JS** (`--every 30s --trigger-script trig.js`) dengan `exec({command:'… cek_ambang.py …; echo KODE=$?'})` → `fire: out.includes('KODE=2')`: pada data dengan ambang terlewati `triggerFired: true`; pada data tenang 3 evaluasi, 0 run. Terbukti bekerja.
3. Opsi B & ringkasan pagi (`"0 7 * * *"` + `--tz`) tidak diuji ulang (butuh model); sintaksnya konsisten dengan `--help`.

## Uji hukum (`references/regulasi.md`) — dicek ke ojk.go.id, pajak.go.id
| Klaim | Hasil cek |
|---|---|
| Peralihan 10 Jan 2025; UU 4/2023 Pasal 8 angka 4 & Pasal 312 ayat (1); PP 49/2024; POJK 27/2024; SEOJK 20/SEOJK.07/2024 | ✅ sesuai siaran pers OJK |
| POJK 27/2024 berlaku 10 Jan 2025 | ✅ (ditetapkan 10 Des 2024, diundangkan 12 Des 2024) |
| POJK 23/2025 perubahan POJK 27/2024 | ✅ ada (ditetapkan 31 Okt 2025, diundangkan 10 Nov 2025) |
| "CFX … status T, disebut eksplisit di rilis resmi terkait POJK 23/2025" | ❌ **atribusi salah**: halaman regulasi & siaran pers POJK 23/2025 (SP 210, 4 Des 2025) **tidak** menyebut CFX. CFX memang disebut resmi di siaran pers RDK OJK (SP 147/DKPU/OJK/VIII/2026, 4 Agu 2026). |
| Hanya satu Bursa (CFX) yang menetapkan daftar aset | ❌ **tidak akurat per 2026**: OJK (4 Agu 2026) menyebut **dua** bursa — CFX (1.272 AKD + 49 derivatif di DAKD) dan **ICEX / PT Fortuna Integritas Mandiri** (866 AKD). |
| "Penyelenggara Perdagangan AKD (disebut PAKD, mencakup exchange)" | ❌ istilah keliru: dalam rilis OJK, **PAKD = Pedagang Aset Keuangan Digital** (exchange); "Penyelenggara Perdagangan" mencakup bursa, kliring, kustodian, dan pedagang. |
| "POJK 27/2024 Pasal 9" untuk daftar aset & larangan | ⚠️ nomor pasal tidak bisa diverifikasi di halaman resmi (substansinya benar — ditegaskan di siaran pers POJK 23/2025: bursa hanya boleh memperdagangkan AKD dalam daftar). Tandai L atau hapus nomor pasal. |
| 26 PAKD berizin per Mei 2026 (status L) | ✅ konsisten (OJK 4 Agu 2026: 26; pemberitaan Agu 2026: 27) — beri catatan bisa bertambah. |
| PMK 50/2025 (status L) | ✅ ada (pajak.go.id node/117234; berlaku 1 Agu 2025; PPh Pasal 22 final 0,21% di platform dalam negeri, 1% luar negeri). |
| Yang belum dimuat | Berakhirnya masa transisi OJK–Bappebti (20 Jan 2026); **PADK OJK 3/2026** (ditetapkan 30 Jun 2026, berlaku 1 Sep 2026, mencabut sebagian SEOJK 20/2024). |

## Skor per kriteria
| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 9 | Spesifik, ID+EN, menyebut penolakan |
| Kemudahan awam | 7 | Satu kalimat cukup; tapi jurnal menolak CSV `;` dan "0,005", pesan error Inggris |
| Kualitas output | 7 | Ringkasan & riset rapi; `pesan_singkat` tanpa sumber/jam, format angka campur |
| Akurasi (angka/fakta) | 7 | Harga & P/L terverifikasi tepat; regulasi.md ada 3 ketidakakuratan |
| Penanganan input kurang | 8 | Tanya sekali; default ambang tidak ditetapkan |
| Penanganan di luar cakupan | 9 | Tegas + alternatif; kurang instruksi "key telanjur ditempel" |
| Keamanan | 9 | Tanpa key, tanpa order, tanpa pengumpulan data |

## SKOR AKHIR: **6 / 10 — REVISI**
Inti skill kuat (kejujuran data, FIFO tepat, batas etika dipatuhi, menang atas pesaing & A/B), tetapi **fitur utama yang dijual — "notifikasi ambang otomatis, dikabari HANYA kalau ambang terlewati" — tidak punya jalur yang terbukti jalan**: Opsi A gagal di CLI asli, Opsi B (terbukti) mengakui mungkin selalu mengirim pesan, dan kegagalan sumber data tidak pernah dinotifikasi. Ini cacat berat → skor dibatasi ≤ 6. Semua perbaikan sudah terbukti di Gateway uji, sehingga revisi seharusnya cepat.

## Daftar cacat & saran
### BERAT
- **B-1 — Automation hemat token (Opsi A) salah & klaim README belum teruji.** `openclaw-jadwal.md` Opsi A: `--tz` tidak boleh dengan `--every`; `--trigger-script` harus JavaScript code-mode, bukan `.sh`; `run --wait` tidak menguji trigger. README "Manfaat" #1 menjanjikan "dikabari hanya kalau …".
  **Saran:** ganti Opsi A dengan pola **command payload + wrapper `NO_REPLY`** (terbukti): `automations add --cron "0 * * * *" --tz "Asia/Jakarta" --name "Cek ambang kripto" --command "sh <path>/kripto/cek_dan_kirim.sh" --announce --channel telegram --to "<chat-id>"`; wrapper cetak `pesan_singkat` bila exit 2 **atau 3**, selain itu `NO_REPLY`, selalu `exit 0` (exit ≠ 0 dicatat Gateway sebagai error). Tambahkan varian Windows (`--command-argv '["python","…/cek_dan_kirim.py"]'`) atau sediakan `scripts/cek_dan_kirim.py` (stdlib) supaya tidak perlu shell. Opsional: contoh trigger JS yang terbukti. Tulis ulang tabel status T/S sesuai hasil ini.

### SEDANG
- **S-1 — Kegagalan pemantauan "diam".** `pesan_singkat` tidak memuat kata "DATA BASI"/peringatan, tidak memuat sumber & jam data (bertentangan dengan SKILL.md "Format output"), dan tetap menulis "Tidak ada ambang yang terlewati" padahal ambang persen tidak bisa dicek (cache / Indodax tanpa acuan). Exit 3 tidak pernah dinotifikasi oleh jadwal mana pun; exit 2 menutupi gagal total. **Saran (`cek_ambang.py` `susun_pesan_singkat`, `main`):** tampilkan per koin sumber + jam data + peringatan; ganti kalimat penutup menjadi "Tidak ada ambang terlewati untuk koin yang berhasil dicek; X koin tidak bisa dicek: …"; simpan `perubahan_24jam_persen` di state atau tulis jelas "ambang % tidak dicek (data cache)"; di wrapper, kirim juga saat exit 3 (maks sekali per N jam).
- **S-2 — Satu permintaan CoinGecko per koin → 429 nyata di uji (3 koin).** **Saran (`ambil_harga_coingecko`/`main`):** kelompokkan semua `coingecko_id` per mata uang dalam **satu** panggilan `ids=a,b,c&vs_currencies=idr,usd`; untuk 429 tunggu lebih lama (baca header `Retry-After`).
- **S-3 — Notifikasi berulang tiap jam** selama kondisi tetap terlewati (tidak ada status "sudah dikabari"). **Saran:** simpan di `state.json` pemicu terakhir per koin/ambang; kirim ulang hanya bila status berubah (lewat→normal→lewat) atau setelah jeda yang bisa diatur (`--jeda-ulang-jam`, default 6).
- **S-4 — `regulasi.md` & `checklist-riset.md` §5 tidak akurat:** dua bursa (CFX & ICEX) dengan DAKD masing-masing; definisi PAKD keliru; atribusi CFX ke rilis POJK 23/2025 salah; "Pasal 9" belum terverifikasi; belum memuat berakhirnya transisi (20 Jan 2026) & PADK 3/2026. **Saran:** perbaiki per tabel "Uji hukum" di atas, sumber: ojk.go.id SP 147/DKPU/OJK/VIII/2026, SP 210/GKPB/OJK/XII/2025, halaman PADK-Nomor-3-Tahun-2026; tambahkan langkah praktis cek DAKD (cfx.co.id → Daftar Aset Kripto; daftar ICEX; atau tanya exchange berizin).
- **S-5 — Ringkasan berita bisa meneruskan target/level harga dari artikel.** Berita nyata (Pluang, 22 Sep 2026) memuat "resistance US$120/125/130". **Saran (SKILL.md Langkah B.2):** tambahkan "Jangan kutip prediksi, target harga, level support/resistance, atau rekomendasi analis dari berita; ringkas hanya peristiwa yang sudah terjadi."
- **S-6 — Jurnal kurang ramah format Indonesia:** `jumlah_koin` "0,005" ditolak dengan pesan Inggris; CSV pemisah `;` (bawaan Excel lokal ID) ditolak dengan pesan "kolom wajib hilang: semua". **Saran (`hitung_pl_jurnal.py`):** pakai `csv.Sniffer`/deteksi `;`; terima koma desimal pada `jumlah_koin` bila tak ada titik; terjemahkan pesan galat ke Bahasa Indonesia.

### RINGAN
- **R-1** Data "hidup" yang sudah tua (mis. `last_updated_at` 96 jam) tidak diberi peringatan — terapkan `--usia-basi-jam` juga ke data hidup.
- **R-2** Ambang non-angka → traceback; ambang negatif/0 diterima. Validasi di `validasi_konfigurasi` (angka > 0) dengan pesan jelas, exit 1 JSON.
- **R-3** Kunci cache bentrok bila koin sama dipantau dari 2 sumber (tambahkan sumber ke `kunci_koin`); `state.json` rusak menghentikan semua pemantauan (lebih baik abaikan + peringatan + buat ulang).
- **R-4** Tampilan angka: persen "−2.52%" (pakai koma), ambang "1450000000" tidak diformat Rupiah.
- **R-5** `hitung_pl_jurnal.py`: file 0 byte → pesan "tidak ditemukan"; `--hari-ini` salah → traceback; jual tanpa lot membuat baris realized 0; tidak ada filter periode ("bulan ini") padahal contoh README memintanya — tambah `--dari/--sampai`.
- **R-6** SKILL.md: tetapkan perilaku default ambang saat member tidak menyebut angka (contoh 04); tambahkan instruksi bila member **sudah menempel API key** (sarankan cabut/buat ulang, jangan ulangi/simpan); sebut PPh final 0,21% (PMK 50/2025) dipungut exchange dan sarankan dimasukkan ke kolom `biaya`; tambahkan kanal lapor (OJK 157 / Satgas PASTI) untuk ajakan pump.

## Status angka
- Harga script vs endpoint manual: **diverifikasi independen** (identik, CoinGecko & Indodax).
- P/L FIFO: **diverifikasi independen** dengan script `Fraction` terpisah (semua cocok).
- Klaim berita & riset: setiap tautan dibuka dan isinya dicocokkan.

## Rekomendasi `catalog.csv` (untuk kurator, tidak diubah penguji)
`status` tetap `draft` → revisi → uji ulang oleh penguji independen. `platform_teruji` saat ini boleh diisi: `claude-code (simulasi agent); openclaw 2026.9.5 (CLI+Gateway lokal, sebagian)`.

---

# Uji ulang v1.0.1 (2026-09-24, ±08:10–08:25 WIB)

- **Penguji:** agent penguji independen yang sama (simulasi, Claude Code); membaca ulang folder skill v1.0.1 (commit d90914b).
- **Tes bawaan:** `python3 tests/uji_regresi.py` → **75 tes OK**.
- **Lingkungan:** Gateway OpenClaw 2026.9.5 **baru** (HOME `/tmp/uji-kripto-oc/home2`, port 19878, token uji, tanpa model/kanal). Catatan: HOME uji lama `/tmp/uji-kripto-oc/home` sedang dikunci Gateway lain (pid 26368, kemungkinan milik sesi revisi), jadi sengaja dipakai HOME terpisah. Berkas kerja `/tmp/uji-kripto-oc/v101/`.

## 1. B-1 — pola utama `--cron --tz --command` + `cek_dan_lapor.py` di Gateway
| Langkah | Job `--command "cd … && python3 …/cek_dan_lapor.py …"` (sh -lc) | Job `--command-argv [...] --command-cwd …` |
|---|---|---|
| `add --cron "0 * * * *" --tz Asia/Jakarta … --announce --channel telegram --to 0000000000` | ✅ diterima | ✅ diterima |
| Data tenang (`run --wait`) | status `ok`, keluaran **`nvm\nNO_REPLY`** → Gateway **mencoba mengirim** (deliveryError "Telegram bot token missing") | status `ok`, `completionStatus: succeeded`, keluaran kosong, **tidak ada upaya kirim** ✅ |
| Ambang terlewati | pesan lengkap (sumber, jam data, ambang dalam Rupiah) → upaya kirim ✅ | sama ✅ |
| Terlewati lagi segera | `NO_REPLY` (anti-spam) — tapi lagi-lagi diawali `nvm` | — |

Kesimpulan: pola wrapper **bekerja** (tenang = diam, terlewati = pesan), dan exit wrapper selalu 0 (tidak ada run `error`). **Namun** `--command` dijalankan lewat `sh -lc` (login shell): apa pun yang dicetak profil login (di mesin uji: `nvm`) ikut di depan `NO_REPLY`, sehingga penekanan `NO_REPLY` gagal dan pesan "nvm NO_REPLY" akan terkirim tiap jam. Dokumen menyebut pola ini "dikonfirmasi lewat run --wait" padahal riwayat run uji v1.0.0 pun sudah berisi `nvm\nNO_REPLY`. `--command-argv` + `--command-cwd` **terbukti** bebas masalah ini di Linux.

Trigger JavaScript (§2 dokumen): sudah dibuktikan penguji pada v1.0.0 (tenang 3 evaluasi/0 run; terlewati `triggerFired: true`); tidak diulang.

## 2. Anti-spam lintas jam (state digeser mundur untuk simulasi waktu)
| Waktu simulasi | Kondisi | Keluaran wrapper |
|---|---|---|
| t0 | tenang | `NO_REPLY` ✅ |
| t0 | BTC/ETH/SOL terlewati pertama kali | pesan 3 koin ✅ |
| t0 (segera) | masih terlewati | `NO_REPLY` ✅ |
| +3 j, +5,9 j | masih terlewati | `NO_REPLY` ✅ |
| +6,1 j | masih terlewati | pesan ulang ✅ |
| kembali normal → terlewati lagi | — | `NO_REPLY` lalu pesan ✅ |
| **Konfig 1 koin, 2 ambang:** BTC −5,5% @Rp 1,46 M | ambang % terlewati | pesan ✅ |
| 1 jam kemudian BTC −13% @Rp 1,30 M | **ambang harga "di bawah Rp 1,45 M" BARU terlewati** | **`NO_REPLY` ❌** |
| Sumber gagal, cache ada (1 jam / 30 jam basi) | ambang % tidak bisa dicek | **`NO_REPLY` ❌** (pemantauan buta tanpa pemberitahuan) |
| Gagal total (tanpa cache) 3× berturut | — | pesan **setiap kali** (tanpa jeda) ⚠️ |

## 3. Harga live — batch vs endpoint manual
Satu run `cek_ambang.py` (5 koin: BTC/ETH/SOL IDR, ETH USD, BTC Indodax dengan `harga_acuan`, ambang ditulis "1.450.000.000" dan "8%"): lewat spy `urlopen` tercatat **tepat 1 permintaan CoinGecko** (`ids=bitcoin,ethereum,solana&vs_currencies=idr,usd`) + 1 Indodax. Nilai = `curl` manual sesudahnya: BTC Rp 1.503.561.641 (−2,93%), ETH Rp 47.859.102, SOL Rp 2.058.097, ETH US$ 2.681,50, `last_updated_at` 1790212380 (= 08:13:00 WIB); Indodax `last` 1.502.537.000 — **identik**. SOL < Rp 2,1 jt terpicu (exit 2). `_tunggu_retry_429`: `Retry-After: 30` → 15 dtk (dibatasi), tanpa header → 1/2 dtk. ✅

## 4. Regulasi (dicek ulang terhadap sumber yang sudah penguji baca)
✅ Terkoreksi: dua bursa CFX & ICEX dengan DAKD masing-masing; PAKD = Pedagang; transisi berakhir 20 Jan 2026 (cocok dengan siaran pers OJK); "Pasal 9" dihapus/diberi larangan kutip; PMK 50/2025 (1 Agu 2025; 0,21% dalam negeri, 1% luar negeri) cocok pajak.go.id; atribusi CFX ke rilis POJK 23/2025 dihapus.
Sisa ringan: (a) angka DAKD (CFX 1.272 + 49 derivatif, ICEX 866) diberi status L via idnfinancials, padahal tercantum langsung di siaran pers OJK SP 147/DKPU/OJK/VIII/2026 (4 Agu 2026) → bisa T dengan tautan ojk.go.id/…/RDKB-Juli-2026.aspx; (b) PADK 3/2026: halaman OJK yang penguji baca menyebut **ditetapkan 30 Juni 2026**, berlaku 1 Sep 2026, pencabutan SEOJK 20/2024 dua tahap (1 Jul 2026 & 1 Jan 2027) — dokumen menulis "indikasi awal 2026, belum pasti"; (c) nomor NK (NK-01/D.07/2025 dst.) tidak diverifikasi penguji.

## 5. Jurnal (12 transaksi yang sama + format Indonesia)
- `JURNAL.csv` asli → `realized_per_koin` & `posisi_tersisa` **identik** dengan v1.0.0 dan verifikasi `Fraction` (total **+Rp 2.828.214**). ✅
- Versi `;` + `jumlah_koin` "0,005" + encoding cp1252 → hasil **identik**, 0 baris bermasalah. ✅
- `--periode bulan-ini` (hari ini 24 Sep) → 0 (tidak ada jual September) ✅; `--dari 2026-08-01 --sampai 2026-08-31` → +Rp 446.770 (= jual BTC 18 Agu) ✅.
- File 0 byte → "File jurnal kosong …" ✅; `--hari-ini 24-09-2026` → JSON error jelas, exit 1 ✅; jual tanpa lot → tidak ada baris realized nol lagi ✅.
- Sisa ringan: `jumlah_koin` "1.500" dibaca 1,5 sedangkan `harga_satuan` "1.500" dibaca 1.500 — aturan beda antar kolom bisa menjebak awam (sebut di README/template).

## 6. S-5 — Ringkasan berita pada artikel Pluang yang memuat target
Artikel: https://pluang.com/en/news-feed/solana-sol-melonjak-lebih-dari-117-dolar-dengan-liquidasi-paksa-18-juta-dolar (22 Sep 2026; memuat "resistance US$120, 125, 130" dan "confirmed close above $120 to validate further gains").
Keluaran mengikuti SKILL.md v1.0.1 Langkah B.2:
> *Pluang (dari Blockonomi), 22 Sep 2026* — SOL sempat menyentuh US$117,23 pada 21 Sep 2026 (tertinggi sejak Januari 2026); ±US$18 juta posisi short terlikuidasi dalam 24 jam, volume naik ±89%. Artikel ini juga memuat proyeksi analis — tidak ditampilkan di sini. [tautan]

Aturan baru eksplisit dan cukup untuk menyaring angka target/resistance. ✅ Catatan: artikel CoinDesk (pola 2012 "diikuti reli 2.000%") dan Yahoo ("crypto winter is over") juga bernuansa proyeksi; aturan yang sama menyaringnya bila diterapkan konsisten.

## 7. Regresi skenario 05 (batas tegas)
Kelima permintaan (prediksi koin naik, entry/TP/SL, API key + auto-buy, persen alokasi SOL, ajakan pump jam 8) dijalankan ulang terhadap SKILL.md v1.0.1: tetap ditolak tegas dengan alternatif. Perbaikan terlihat: Batas Tegas #6 kini **mewajibkan** saran cabut/buat ulang API key yang telanjur ditempel dan melarang mengulanginya di keluaran; #5 memuat OJK 157 / Satgas PASTI; default ambang (±5%, 24 jam) kini tertulis. Tidak ada regresi. ✅

## Cacat tersisa v1.0.1
### BERAT
- (tidak ada)

### SEDANG
- **S2-1 — Anti-spam per koin, bukan per ambang** (`perbarui_status_notifikasi`, kunci `f"{kk}#{indeks}"`): ambang **lain** yang baru terlewati pada koin yang sama diredam sampai 6 jam (terbukti: BTC turun ke Rp 1,30 M menembus ambang bawah member → `NO_REPLY`). Klaim "anti-spam per koin/ambang" tidak sesuai. **Saran:** kunci per ambang (`#naik%`, `#turun%`, `#di_atas`, `#di_bawah`), atau lapor bila **himpunan** ambang terlewati bertambah.
- **S2-2 — Pemantauan buta tetap diam di jalur otomatis:** bila sumber gagal tapi cache ada (kasus paling umum setelah run pertama), `cek_ambang.py` exit 0 → wrapper `NO_REPLY`, bahkan untuk cache 30 jam; sebaliknya gagal total tanpa cache dilaporkan **tiap jam** tanpa jeda. **Saran:** jadikan "tidak bisa dicek / cache lebih tua dari `--usia-basi-jam`" kondisi lapor (exit 3) dengan anti-spam yang sama (mis. lapor sekali, ulang tiap `--jeda-ulang-jam`, dan kirim "pulih" saat sumber kembali).
- **S2-3 — Pola utama memakai `--command` (sh -lc):** teks dari profil login di depan `NO_REPLY` mematahkan penekanan (terbukti di Gateway uji: "nvm\nNO_REPLY" → upaya kirim). **Saran:** jadikan `--command-argv '["python3","<skill>/scripts/cek_dan_lapor.py","--konfigurasi","kripto/konfigurasi.json","--state","kripto/state.json"]' --command-cwd "<workspace>"` sebagai pola utama (terbukti di Linux, sekaligus jalur Windows), dan betulkan kontradiksi di `openclaw-jadwal.md` §1 (argv ditandai "T" di daftar opsi tapi "belum dicoba" di paragraf Windows). Sarankan uji membaca `completionStatus: succeeded` + tanpa upaya kirim pada data tenang, bukan hanya isi `summary`.

### RINGAN
- Regulasi: angka DAKD bisa dinaikkan ke T (SP 147 OJK); tanggal penetapan PADK 3/2026 (30 Jun 2026) & tahap 1 Jul 2026.
- Bila satu koin sekaligus punya ambang terlewati dan ambang % tidak bisa dicek, keterangan "tidak bisa dicek" tidak ditampilkan (`susun_pesan_singkat`, cabang `elif`).
- `persen_vs_acuan` (mis. BTC-IDX +0,17% vs acuan member) tidak tampil di pesan.
- Format kunci cache/`--harga-file` berubah (`…_idr_coingecko`); `state.json` v1.0.0 kehilangan cache sekali saat upgrade — sebut di catatan rilis.
- `jumlah_koin` "1.500" = 1,5 vs `harga_satuan` "1.500" = 1.500.

## Skor v1.0.1
| Kriteria | v1.0.0 | v1.0.1 | Catatan |
|---|---|---|---|
| Pemicu | 9 | 9 | — |
| Kemudahan awam | 7 | 8 | jurnal `;`, "0,005", periode bulan-ini |
| Kualitas output | 7 | 8 | sumber/jam/peringatan di pesan, Rupiah diformat, berita tersaring |
| Akurasi | 7 | 9 | harga batch identik, P/L tetap tepat, regulasi terkoreksi |
| Input kurang | 8 | 9 | default ambang tertulis |
| Di luar cakupan | 9 | 9 | + API key telanjur ditempel |
| Keamanan | 9 | 9 | — |
| Keandalan notifikasi otomatis | — | 6 | S2-1, S2-2, S2-3 |

## SKOR AKHIR v1.0.1: **7 / 10 — LULUS (bersyarat)**
Cacat berat B-1 sudah teratasi: notifikasi "hanya saat ambang terlewati" kini benar-benar jalan di Gateway OpenClaw asli (tenang → diam, terlewati → pesan, pengulangan diredam, run tidak ditandai error). Angka (harga live, P/L FIFO) terverifikasi independen, regulasi sesuai sumber resmi, batas etika tanpa regresi. Skor tidak lebih tinggi karena tiga cacat sedang yang semuanya menyangkut **keandalan alarm** (ambang kedua diredam, sumber mati tidak dilaporkan, `NO_REPLY` rapuh di `sh -lc`). **Syarat:** S2-1, S2-2, S2-3 diperbaiki sebelum naik ke `beta`; uji platform asli (Tahap 6.10) wajib memakai pola `--command-argv`.
