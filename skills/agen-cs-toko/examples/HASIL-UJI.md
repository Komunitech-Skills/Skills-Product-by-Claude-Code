# HASIL UJI — agen-cs-toko

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** OpenClaw 2026.9.5 (ec9c1a1), **HOME uji baru** `/tmp/uji-agen-cs-toko/home`
  (+ salinan `home-agent` untuk uji `agents add`), tanpa login kanal (token Telegram fiktif).
  Skill dipasang dengan `openclaw skills install ./agen-cs-toko --global` → Ready, visible,
  available as command. Data uji fiktif di `/tmp/uji-agen-cs-toko/`.

## Verifikasi perintah & kunci config
| Perintah / kunci di skill | Hasil |
|---|---|
| `openclaw channels add --channel telegram --token <token>` | ✅ jalan (token fiktif → akun "default", `dmPolicy: pairing`, `groupPolicy: allowlist`). `--token` tidak tampil di `--help` umum, tapi ada di contoh resmi |
| `openclaw channels login --channel whatsapp` | ✅ flag ada (tidak dijalankan, tanpa login kanal) |
| `openclaw automations create --cron … --tz Asia/Jakarta --name … --message … --session isolated --announce --channel telegram --to …` | ✅ diterima parser (berhenti di Gateway tanpa kredensial, wajar) |
| `openclaw automations run <id>` wajib id | ✅ tanpa id: "Missing required argument id" |
| `openclaw agents add cs --role coordinator --bind whatsapp:cs` | ⚠️ jalan (exit 0), tapi hasilnya keliru untuk CS (lihat cacat #4) |
| `dmPolicy` / `allowFrom` / `groupPolicy` (default `allowlist`) / `groupAllowFrom` = pengirim di grup | ✅ enum & makna benar (schema + docs `channels/whatsapp.md`) |
| `channels.whatsapp.groups` (ID grup) & fallback `groupAllowFrom` → `allowFrom` | ❌ **tidak disebut sama sekali** (lihat cacat #1) |
| `session.dmScope` enum, `tools.profile` enum | ✅ |
| `selfChatMode` (untuk mode "WA ke diri sendiri") | ⚠️ kunci ada (`channels.whatsapp.selfChatMode`), tidak disebut skill |
| Tidak ada pengiriman otomatis ke pelanggan lewat WA Web | ❌ tidak terjamin (lihat cacat #1: pesan pairing) |

## Uji `scripts/periksa_draf.py` (nyata + verifikasi independen)
Basis pengetahuan fiktif: Pashmina Rp 89.000, Bergo Rp 65.000, Voal Rp 125.000, Paket 3 Rp 240.000, gratis ongkir min. Rp 300.000.

| Draf | Hasil script | Seharusnya | Status |
|---|---|---|---|
| Normal (harga persis dari basis pengetahuan) | bersih, exit 0 | bersih | ✅ |
| Mengarang "promo **Rp 79.000**" | [79000], exit 1 | tandai | ✅ |
| Mengarang "harganya **79.000**" (tanpa "Rp") | **bersih**, exit 0 | tandai | ❌ lolos |
| Mengarang "paket **1,5 juta**" | **bersih**, exit 0 | tandai | ❌ lolos |
| "Pashmina **Rp 89rb**" (harga benar) | [89, …], exit 1 (dibaca Rp 89) | bersih | ⚠️ salah baca (terlalu waspada) |
| "cuma **79rb**" (karangan) | [79], exit 1 | tandai 79.000 | ⚠️ tertangkap, angka salah |
| "Rp 1.500.000,50" | [1500000] | 1.500.000 (desimal dibuang) | ✅ |
| Total turunan "Rp 178.000 (2 × Rp 89.000)" | [178000] | tandai untuk dicek | ✅ |
| "stok tinggal 2" (karangan stok) | tidak diperiksa | — | ⚠️ script tidak memeriksa stok, padahal docstring menyebut "harga/stok" |
| Bocor **NIK 3201010101010001 + OTP 482913** | NIK + "nomor kartu" (dobel) + OTP, exit 1 | tandai | ✅ (duplikat) |
| Kartu "4111 1111 1111 1111 … cvv 123" | kartu + CVV | tandai | ✅ |
| Peringatan "jangan kirim kode OTP" | ditandai OTP, exit 1 | bersih | ⚠️ positif palsu |
| No. HP "0812-0000-1234" | bersih | bersih | ✅ |
| Nomor pesanan 16 digit | ditandai NIK + kartu | bersih | ⚠️ positif palsu |
| "kirim pin lokasi" | ditandai PIN | bersih | ⚠️ positif palsu |
| File basis pengetahuan tidak ada | exit 2 + pesan | error | ✅ |
| Basis pengetahuan kosong + draf "Rp 79.000" | [79000], exit 1 | tandai | ✅ |

Angka dicek independen: 3 × 89.000 = 267.000; selisih paket = 27.000; normalisasi 1.500.000,50 → 1.500.000.

## Skor
| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 8 | Kata kunci ID/EN jelas, batas dengan balas-chat-cs tegas |
| Kemudahan awam | 8 | Wawancara 5 pertanyaan, template, `[isi ...]`, Telegram default |
| Kualitas output | 8 | Draf + keyakinan + "perlu dicek" + eskalasi 3 baris; menang A/B & pesaing |
| Akurasi | 6 | Script meloloskan harga karangan tanpa "Rp"/format "juta", salah baca "rb"; prompt rekap membaca log yang tidak pernah ditulis; `--role coordinator` keliru |
| Penanganan input kurang | 8 | Tanya sekali / `[isi ...]`, tidak mengarang |
| Penanganan di luar cakupan | 9 | Auto-reply penuh, broadcast, diagnosis/dosis ditolak dengan alternatif sah |
| Keamanan | 5 | Janji "tidak pernah kirim otomatis" bisa dilanggar oleh konfigurasi WA yang disarankan (pairing di nomor pemilik); grup WA tidak diatur |

## SKOR AKHIR: 6 / 10 — **REVISI**
Inti produk kuat: basis pengetahuan lokal, draf Copilot, eskalasi wajib, dan batasan kesehatan
yang baik. Skill menang jelas di A/B dan di banding pesaing. Skor dibatasi karena ada satu
cacat berat pada setup kanal WhatsApp. Cacat ini bertentangan langsung dengan dua janji
utama skill: tidak ada pengiriman otomatis ke pelanggan, dan WA hanya lewat nomor terpisah.

## Daftar cacat & saran perbaikan

### Berat
1. **Setup WA "ke diri sendiri" memakai nomor pemilik + `dmPolicy: pairing` dianggap "cukup aman"**
   (`references/eskalasi-dan-kanal.md` §2 "WhatsApp ke diri sendiri (nomor pemilik, bukan nomor
   CS)" dan §4 "pakai `dmPolicy: "pairing"` (default, cukup aman)").
   - Menurut docs `channels/pairing.md`, pada mode pairing, **setiap pengirim baru otomatis
     dikirimi kode pairing oleh bot** (±1×/jam per pengirim). Bila nomor WA yang ditautkan juga
     menerima chat pelanggan (umum pada UMKM: nomor pemilik = nomor toko), bot **mengirim pesan
     otomatis ke pelanggan lewat WA Web**. Ini melanggar janji "tidak pernah mengirim sendiri"
     di README dan berisiko nomor diblokir. Default `channels add` juga `pairing` (terverifikasi).
   - Menautkan **nomor pemilik** bertentangan dengan keputusan pemilik ("WA hanya dengan
     **nomor terpisah** untuk notifikasi ke pemilik sendiri + persetujuan risiko tertulis").
   - Grup tidak diatur: `groupPolicy` bawaan `allowlist` dengan `groupAllowFrom` kosong **jatuh
     ke `allowFrom`**. `channels.whatsapp.groups` (ID grup `…@g.us`) tidak dibahas.

   **Perbaikan:** WA hanya pada **nomor terpisah** + persetujuan risiko tertulis. Konfigurasi wajib:
   `dmPolicy: "allowlist"`, `allowFrom: ["<nomor pemilik E.164>"]` (**jangan pernah `pairing` di
   WA**), `groupPolicy: "disabled"` (atau `groups: {}` bila memang tak ada grup), dan sebutkan
   `selfChatMode` bila memakai self-chat. Sertakan penjelasan fallback `groupAllowFrom → allowFrom`.
   `pairing` hanya dianjurkan untuk **Telegram**.

### Sedang
2. **Pemeriksa harga karangan bolong** (`scripts/periksa_draf.py` `ekstrak_nominal`, baris 47–63):
   angka tanpa "Rp" ("harganya 79.000"), "1,5 juta", "2 jt" lolos sebagai bersih. "rb/ribu" tidak
   dikalikan 1.000 ("Rp 89rb" → Rp 89). **Perbaikan:** dukung pengali `rb|ribu|k|jt|juta`, tangkap
   angka berpemisah ribuan di dekat kata harga (harga, cuma, jadi, total, ongkir, diskon), dan
   tulis jelas di SKILL.md bahwa **stok tidak diperiksa script** (baris 82 & docstring).
3. **Rekap harian membaca "log draf" yang tidak pernah dibuat** (`references/eskalasi-dan-kanal.md`
   §3; SKILL.md langkah 6). Automation `--session isolated` tidak melihat percakapan admin, jadi
   rekap kosong atau dikarang. **Perbaikan:** tambahkan langkah "setiap draf/eskalasi: tambahkan 1
   baris ke `cs/log/<YYYY-MM-DD>.md` (kategori, eskalasi ya/tidak, pertanyaan tanpa jawaban;
   **tanpa nama/nomor pelanggan/pasien**)", lalu arahkan prompt automation ke file itu.
4. **`openclaw agents add cs --role coordinator --bind whatsapp:cs`** (§5): terverifikasi membuat
   agent beridentitas **"Chief of Staff"** dengan subagent `researcher/writer/reviewer` (yang
   tidak ada), **tanpa** `tools.profile: messaging`, dan langsung mengikat akun WA "cs" ke agent
   yang akan membalas sendiri. **Perbaikan:** hapus `--role coordinator` (pakai `--workspace` +
   SOUL/aturan CS sendiri, `--non-interactive`), set `agents.entries.cs.tools.profile messaging`,
   dan tandai seluruh §5 sebagai "hanya dengan jasa setup", bukan contoh siap tempel.
5. **Pesan penahan medis tanpa arahan keselamatan umum** (`references/klinik-dan-data-kesehatan.md`
   kalimat standar; `templates/ATURAN.template.md`): tambahkan kalimat baku non-triase "bila kondisi
   memburuk/darurat, segera ke IGD terdekat atau hubungi 119", terutama untuk chat di luar jam praktik.

### Ringan
6. Script data sensitif: kata "OTP/PIN" di **kalimat peringatan** ikut ditandai. NIK dilaporkan
   dobel (NIK + kartu). Nomor pesanan 16 digit dianggap NIK. Kode OTP tanpa kata "OTP" lolos.
   Sarankan: laporkan NIK sekali, abaikan "OTP" yang didahului "jangan", tangkap "kode \d{4,8}".
7. Setup Telegram tidak memberi perintah persetujuan pairing: tambahkan `openclaw pairing list
   telegram` dan `openclaw pairing approve telegram <KODE>` (flag ada di 2026.9.5).
8. SKILL.md baris 129 merujuk `CLAUDE.md`, yang tidak ada di paket pembeli.
9. Tidak ada aturan pemilihan register (santai/formal/B2B). Ide dari pesaing `wa-reply-id`
   (lihat `00-banding-pesaing.md`) berguna untuk persona percetakan B2B.

## Laporan singkat
agen-cs-toko | 6 | REVISI | berat: konfigurasi WA nomor pemilik + pairing → bot mengirim kode
otomatis ke pelanggan & melanggar aturan nomor terpisah; sedang: script lolos harga tanpa
"Rp"/"juta" dan salah baca "rb", rekap membaca log yang tidak ada, `agents add --role
coordinator` keliru, pesan penahan medis tanpa arahan IGD | angka script diverifikasi independen: **ya**.

---

# Uji ulang v1.0.1

- **Tanggal:** 2026-09-23 · **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** OpenClaw 2026.9.5, HOME uji baru `/tmp/uji-agen-cs-toko/home-v101`, tanpa login
  kanal. Skill v1.0.1 dipasang (`skills install <folder> --as agen-cs-toko --global` → Ready,
  visible, command). File yang dibaca ulang: SKILL.md, `references/*`, `templates/*`, `scripts/periksa_draf.py`.

## Verifikasi klaim perbaikan
| Klaim pembuat | Hasil verifikasi |
|---|---|
| WA wajib nomor terpisah + persetujuan risiko + `dmPolicy: allowlist` + `allowFrom` pemilik + `groupPolicy: disabled`, pairing hanya Telegram | ✅ tertulis konsisten di SKILL.md §7 & Batasan, references §2/§4/§6. Diterapkan sungguhan: `config set` 4 kunci + `selfChatMode true` → `config validate` valid, audit tanpa temuan kanal |
| Fallback `groupAllowFrom → allowFrom`, `channels.whatsapp.groups`, `selfChatMode` dijelaskan | ✅ sesuai docs `channels/whatsapp.md` |
| `openclaw pairing list telegram` / `pairing approve telegram <KODE>` | ✅ ada ("No pending telegram pairing requests"; `approve <codeOrChannel> [code]`) |
| `agents add cs --workspace <dir> --non-interactive` tanpa `--role` + `config set agents.entries.cs.tools.profile messaging` | ✅ jalan: identity `{"name":"cs"}`, tanpa subagent, `tools.profile: "messaging"` |
| Log `cs/log/<tanggal>.md` untuk rekap + prompt "jangan mengarang angka" | ✅ SKILL.md §6 + references §3a–3b. `automations create` baru diterima parser |
| `periksa_draf.py`: harga tanpa "Rp" + pengali rb/jt | ⚠️ sebagian (lihat tabel regresi & kasus baru) |
| Jujur stok tidak diperiksa | ✅ docstring, `--help`, SKILL.md, dan baris `[INGAT]` di setiap keluaran |
| Kurangi positif palsu (NIK dobel, nomor pesanan, "pin lokasi", peringatan OTP) | ⚠️ sebagian; ada **regresi keamanan** baru (lihat bawah) |
| Kalimat IGD/119 | ✅ references klinik baris 18–19 + template ATURAN baris 38, dengan "bukan triase" |
| Aturan nada | ✅ SKILL.md §8 (formal-ringkas untuk B2B/jasa cetak; ramah-sopan untuk konsumen) |
| Rujukan CLAUDE.md di file pembeli | ✅ sudah dihapus |

## 17 kasus regresi (dijalankan ulang)
| # | Kasus | v1.0 | v1.0.1 |
|---|---|---|---|
| 1 | Draf normal | exit 0 ✅ | exit 0 ✅ |
| 2 | Karang "Rp 79.000" | [79000] ✅ | [79000] ✅ |
| 3 | Karang "harganya 79.000" | **lolos** ❌ | [79000] ✅ |
| 4 | Karang "1,5 juta" | **lolos** ❌ | [1500000] ✅ |
| 5 | "Rp 89rb … 240 ribu" (benar) | salah baca [89, 240] | exit 0 ✅ |
| 6 | Karang "79rb" | [79] | [79000] ✅ |
| 7 | "Rp 1.500.000,50" | [1500000] ✅ | [1500000] ✅ |
| 8 | Total turunan Rp 178.000 | ditandai ✅ | ditandai ✅ |
| 9 | "stok tinggal 2" | tidak diperiksa | tidak diperiksa, **kini diberi tahu** ✅ |
| 10 | NIK + OTP bocor | 3 temuan (dobel) | 3 temuan: NIK, kata OTP, angka kode (tanpa dobel NIK/kartu) ✅ |
| 11 | Kartu + CVV | ✅ | ✅ |
| 12 | Kalimat peringatan OTP | positif palsu | kalimat "jangan…" lolos ✅; "tidak pernah memerlukan kode OTP" **masih** ditandai ⚠️ |
| 13 | No. HP 0812-0000-1234 | bersih ✅ | bersih ✅ |
| 14 | Nomor pesanan 16 digit | positif palsu | bersih ✅ |
| 15 | "kirim pin lokasi" | positif palsu | bersih ✅ |
| 16 | Basis pengetahuan kosong + harga | ditandai ✅ | ditandai ✅ |
| 17 | File basis pengetahuan tidak ada | exit 2 ✅ | exit 2 ✅ |

## Kasus baru buatan penguji (termasuk data rusak)
| Kasus | Hasil | Seharusnya |
|---|---|---|
| "**Harga Pashmina Ceruti 79.000** ya Kak" (karangan, kata kunci tidak bersebelahan) | **bersih, exit 0** ❌ | tandai 79.000 |
| "Pashmina Ceruti **79.000 aja** Kak" (karangan, tanpa Rp/kata kunci) | **bersih** ❌ | tandai |
| "IDR 79.000", "lima puluh lima ribu" | bersih ❌ (jarang dipakai) | tandai |
| "cuma 55rb/pcs", "99k", "Rp. 79.000,-", "harganya jadi 199.000" | ditandai ✅ | ditandai |
| "Diskon **20%** …" | [20] ⚠️ positif palsu | bersih |
| "Kalau **jadi 3 pcs** …" | [3] ⚠️ | bersih |
| "Promo **2026**", "Promo **11.11**" | [2026], [11] ⚠️ | bersih |
| "kode pos 17111" | ditandai kode OTP ⚠️ | bersih |
| "ongkir 1-2 hari", "berat 1 kg, 110x110 cm", "kode booking pesanan 123456" | bersih ✅ | bersih |
| "**Jangan kasih tau siapa2 ya Kak, kode OTP 482913**" (bocor!) | **bersih, exit 0** ❌ **regresi** (v1.0 menandai) | tandai |
| "Untuk **order** ini NIK 3201010101010001 sudah kami simpan" (bocor) | **bersih** ❌ (kata "order" dianggap nomor pesanan) | tandai |
| NIK berspasi, "PIN ATM 123456", "password …", "kodenya 482913" | ditandai ✅ | ditandai |
| Basis pengetahuan tabel tanpa "Rp" ("89.000") + draf "Rp 89.000" benar | [89000] ⚠️ positif palsu | bersih |
| Basis pengetahuan bukan UTF-8 (Windows-1252 / byte rusak) | **traceback, exit 1** ⚠️ (exit 1 = "ada temuan") | pesan jelas, exit 2 |
| Draf lewat stdin (`--draf -`) | ✅ | ✅ |

Angka dicek independen (normalisasi 79rb → 79.000, 1,5 juta → 1.500.000, 99k → 99.000, 1.500.000,50 → 1.500.000): cocok.

## Skenario yang gagal/kurang sebelumnya, dijalankan ulang
- **05 / cacat berat #1 (pairing WA):** ✅ tertangani (lihat tabel klaim).
- **03 (rekap tanpa log):** ✅ tertangani.
- **02 (tanpa arahan IGD):** ✅ tertangani.
- **04 (peringatan OTP ditandai):** ⚠️ membaik sebagian (kalimat "jangan" lolos, "tidak pernah" masih ditandai).
- **01 ("89rb" salah baca):** ✅ tertangani.
Catatan penguji tiap contoh sudah ditambah bagian "Uji ulang v1.0.1".

## Skor v1.0.1
| Kriteria | v1.0 | v1.0.1 | Alasan |
|---|---|---|---|
| Pemicu | 8 | 8 | Tetap |
| Kemudahan awam | 8 | 8 | Setup Telegram lebih lengkap (pairing approve) |
| Kualitas output | 8 | 9 | Nada per jenis pelanggan, IGD/119, log rekap |
| Akurasi | 6 | 7 | Rekap berbasis log, `agents add` benar; script masih meloloskan "Harga <produk> 79.000" |
| Penanganan input kurang | 8 | 8 | Tetap |
| Penanganan di luar cakupan | 9 | 9 | Tetap |
| Keamanan | 5 | 8 | Konfigurasi WA kini aman & terverifikasi. Minus: regresi deteksi bocor OTP bila ada kata "jangan" di kalimat yang sama |

## SKOR AKHIR v1.0.1: 8 / 10 — **LULUS**
Cacat berat v1.0 (pairing WA di nomor pemilik → pesan otomatis ke pelanggan) sudah diperbaiki
dan terbukti di OpenClaw sungguhan. Semua cacat sedang v1.0 tertangani: log rekap, `agents add`
tanpa `--role` + profil messaging, IGD/119, dan kejujuran soal stok. Masalah tersisa ada di
**script opsional** `periksa_draf.py`, yang hanya jaring pengaman. Checklist wajib SKILL.md tetap
menuntut pencocokan harga dan larangan data sensitif secara manual. Sisa ini layak diperbaiki
di v1.0.2, tetapi tidak menghalangi kelulusan.

## Temuan tersisa & saran (v1.0.2)
### Sedang
1. **Regresi deteksi bocor** (`cek_data_sensitif`, baris 184–203): pengecualian `KATA_NEGASI`
   berlaku untuk **seluruh kalimat**, sehingga "Jangan kasih tau siapa2, kode OTP 482913" lolos.
   **Saran:** abaikan hanya bila kalimat **tidak** memuat angka 4–8 digit (peringatan tanpa kode =
   aman; ada kode = tetap tandai). Pengecualian konteks "order" untuk NIK (baris 160–165) sebaiknya
   hanya berlaku bila tidak ada kata "NIK/KTP" di dekatnya.
2. **Harga karangan dengan nama produk di antara kata kunci dan angka** ("Harga Pashmina Ceruti
   79.000", "Pashmina Ceruti 79.000 aja") masih lolos. `POLA_NOMINAL` (baris 60–66) mewajibkan
   kata kunci tepat sebelum angka. **Saran:** anggap angka berformat ribuan (`\d{1,3}(\.\d{3})+`)
   sebagai nominal bila ada kata harga/aja/saja/cuma **di kalimat yang sama**, atau semua angka
   ≥ 1.000 berpemisah titik.

### Ringan
3. Positif palsu angka kecil: "diskon 20%", "jadi 3 pcs", "promo 2026/11.11" → abaikan angka
   diikuti `%`/`pcs|pc|buah|x`, tahun 19xx/20xx, dan pola tanggal promo `\d{1,2}\.\d{1,2}`.
   "kode pos" → kecualikan "kode pos/booking/promo/voucher".
4. Kata negasi belum mencakup "tidak pernah", sehingga kalimat peringatan standar skill sendiri masih ditandai.
5. Basis pengetahuan non-UTF-8 menghasilkan traceback dengan exit 1 (bentrok dengan arti "ada
   temuan"). Tangkap `UnicodeDecodeError` → coba `cp1252`/`utf-8-sig`, atau exit 2 dengan pesan jelas.
6. Harga di basis pengetahuan tanpa "Rp" (tabel "89.000") tidak dikenali, sehingga draf yang benar
   ditandai. Sebutkan di template: tulis harga dengan "Rp".
7. references §2 langkah WA: urutan "login dulu, baru set allowlist". Lebih aman set
   `dmPolicy: allowlist` + `allowFrom` **sebelum** `channels login`. Klaim "dry-run berhasil" di
   §4 memakai value mode, yang menurut OpenClaw "does not run schema checks". Validasi sungguhan
   dilakukan penguji (`config validate` → valid).

## Laporan singkat v1.0.1
agen-cs-toko v1.0.1 | 8 | LULUS | berat: tidak ada; sedang: regresi deteksi bocor OTP bila
kalimat memuat "jangan", NIK lolos bila ada kata "order", harga karangan "Harga <produk> 79.000"
lolos | angka script diverifikasi independen: **ya**.

## Catatan koordinator — v1.0.2
Temuan "Uji ulang v1.0.1" di periksa_draf.py diperbaiki pembuat; `tests/uji_regresi.py` 45/45 lulus. Koordinator mengecek ulang secara independen 5 kasus kunci: kebocoran OTP dalam kalimat "jangan…" → ditandai; "tidak pernah memerlukan kode OTP" → bersih; "Harga Pashmina Ceruti 79.000" (karangan, KB Rp89.000) → ditandai; "Diskon 20% untuk 3 pcs" → bersih; "order ini NIK 3201…" → ditandai. Urutan setup WA di references §2 kini: kunci allowlist dulu, baru login QR; §4 memakai `config validate`. Status tetap lulus (perubahan hanya pada pemeriksa opsional + panduan, disertai uji regresi).

## Catatan revisi v1.0.8 (2026-10-05) — menunggu uji ulang independen
Pra-cek Telegram gelombang 8: balasan hanya menolak auto-reply lalu bertanya data toko tanpa hasil. Perbaikan: aturan "kerjakan dulu, tanya di akhir" di SKILL.md & description (paket siap pakai dengan [isian] sebelum maks. 3 pertanyaan). Contoh baru: `06-toko-hijab-kerjakan-dulu-tanya-di-akhir.md`. Belum diuji ulang independen di OpenClaw; skor & status tidak diubah di sini.

## Uji ulang konteks Telegram v1.0.8 — 2026-10-05
Rata-rata 3,7 (5 / 1 timeout / 5); 0/3 lulus. **VERDIK: TIDAK LULUS.** Penolakan auto-balas WA + Copilot benar, tetapi template siap pakai tidak ditampilkan di chat (hanya ditulis ke file workspace). Rincian: `00-openclaw-sebelum-sesudah.md`.

## Catatan revisi v1.0.9 (2026-10-05) — menunggu uji ulang independen
Dari uji ulang Telegram v1.0.8 (TIDAK LULUS): template hanya dirangkum sebagai file. Perbaikan: ATURAN PERTAMA di SKILL.md & description (template + aturan nada + alur admin wajib lengkap di chat, ringkas; file hanya bila diminta, setelah isi tampil), langkah kerja file jadi opsional, checklist baru. Belum diuji ulang independen; skor & status tidak diubah.

## Uji ulang konteks Telegram v1.0.9 (2026-10-05)
VERDIK: LULUS. Skor 9 / 9 / 8 (rata-rata 8,7), 3/3 lulus, tanpa timeout. Penolakan auto-balas WA + Copilot, template stok/ongkir/retur dkk. tertulis lengkap di chat dengan [isian]. Rincian di `00-openclaw-sebelum-sesudah.md`.

## Riwayat revisi - v1.0.10 (2026-10-05)
Temuan Telegram gelombang 9 (cacat no. 5): template cara bayar berisiko melanggar kebijakan Shopee bila dipakai di chat marketplace. Perbaikan: catatan wajib di SKILL.md, template PENGETAHUAN, referensi + sumber. Status: **menunggu uji ulang independen**.
