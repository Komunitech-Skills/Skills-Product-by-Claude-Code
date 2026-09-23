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
