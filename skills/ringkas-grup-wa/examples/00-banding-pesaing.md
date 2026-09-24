# Uji Banding Pesaing — Ringkas Grup WhatsApp

## Kata kunci & sumber yang dicari
- GitHub code search: `"SKILL.md" whatsapp group chat summary`
- Web search: `SKILL.md whatsapp group chat summary skill ClawHub OR skills.sh OR github 2026`
- Diperiksa juga (lewat listing sebelumnya/pengetahuan umum): `VoltAgent/awesome-openclaw-skills`,
  `openclaw/clawhub`, Hermes Skills Hub (lobehub.com/market), `anthropics/skills` — tidak ditemukan
  skill ringkas grup WA resmi dari Anthropic.
- Tidak sempat mengecek `manairalabs/bicara-skills` / `alvinindra/bahasa-skills` secara spesifik
  (akses waktu terbatas); tidak muncul di hasil pencarian di atas.

## Kandidat yang ditemukan
1. **`mocasus/whatsapp-group-summary`** (GitHub, MIT License, 14 ⭐, 8 commit, pembuat individu
   `mocasus`) — skill Hermes yang **merekam semua pesan grup WA secara diam-diam** dengan
   mem-patch 3 file source Hermes/whatsapp gateway (melewati filter default WhatsApp), lalu
   mengirim ringkasan otomatis 2x sehari (07.00 & 23.00 WIB) via cron, gaya bahasa gaul santai
   ("gw", "lo"), mode normal atau "roast" (sarkastik).
2. **`agentlyhq-skills/summarize-whatsapp-group-chats`** (terindeks di Hermes Skills Hub via
   lobehub.com) — memakai tool CLI `wacli` untuk fetch & sinkronisasi riwayat WhatsApp; halaman
   detail tidak bisa diakses penuh (403 saat di-fetch), jadi dinilai hanya dari cuplikan hasil
   pencarian awal ("Debug and monitor WhatsApp message delivery..." — kategori lebih ke observability
   API, bukan ringkasan grup untuk pengguna awam).

## Penilaian kelayakan sebagai pesaing (sebelum dibandingkan langsung)
`mocasus/whatsapp-group-summary` **TIDAK LOLOS** ambang bukti kurasi CLAUDE.md (repo skill
tunggal perlu ≥100 ⭐; ini baru 14 ⭐, 8 commit, tidak ada bukti dipakai komunitas lain/issue/fork).
Secara arsitektur pun **tidak sebanding langsung**: skill kita memproses **file ekspor** yang
pengguna buat sendiri sekali jalan (tanpa setup), sedangkan skill ini mengharuskan **mem-patch
kode sumber Hermes** dan menjalankan **bot yang merekam semua pesan grup terus-menerus tanpa
sepengetahuan anggota lain** — bertentangan langsung dengan keputusan pemilik Komunitech
(CLAUDE.md §1 jalur 3: harus Copilot/persetujuan, anggota grup wajib diberi tahu, tanpa
perekaman diam-diam) dan dengan SKILL.md kita sendiri ("Kapan TIDAK digunakan": menyadap grup
tanpa sepengetahuan anggotanya).

Karena arsitekturnya beda total (live recording vs file ekspor sekali proses) dan skenario S1
kita (pengguna melampirkan file ekspor untuk diringkas sekali) **tidak bisa dijalankan** dengan
pendekatan pesaing ini (perlu instalasi bot, akses WhatsApp Web live, patch kode, cron — bukan
"tempel file, langsung dapat ringkasan"), tidak dibuat tabel output berdampingan literal. Sebagai
gantinya, perbandingan kualitatif di bawah ini menilai pendekatan keduanya untuk kebutuhan yang
sama (tahu apa yang perlu ditanggapi di grup WA).

## Tabel penilaian
| Aspek | `mocasus/whatsapp-group-summary` (pesaing) | `ringkas-grup-wa` (kita) |
|---|---|---|
| Kesiapan pakai ("instan, tanpa setup") | Tidak — wajib patch 3 file source, atur cron, verifikasi checklist | Ya — tempel file ekspor, langsung jalan |
| Etika/persetujuan anggota grup | **Merekam diam-diam**, melewati filter default WhatsApp, tanpa mekanisme persetujuan anggota | Hanya proses ekspor yang pengguna buat sadar dari grup miliknya; menolak permintaan menyadap |
| Kesesuaian konteks Indonesia | Bahasa gaul Indonesia ("gw","lo"), tapi tanpa perhitungan uang/tenggat terstruktur | Bahasa Indonesia sehari-hari + Rupiah, deteksi tenggat/uang/keputusan terstruktur |
| Kutipan asli & jam per item penting | Tidak disebutkan di dokumentasi (ringkasan tema, bukan kutipan per pesan) | Wajib, +jam, ±15 kata, bisa dicek langsung |
| Daftar tindakan siapa-apa-tenggat | Tidak ada | Ada, format tabel |
| Akurasi/anti-mengarang | Merangkum "3-5 tema" dari LLM tanpa mekanisme verifikasi eksplisit anti-halusinasi | Prinsip eksplisit "setia pada isi asli", item ambigu ditandai ⚠️, tidak menebak isi pesan terhapus |
| Popularitas/bukti pemakaian | 14 ⭐, 8 commit — di bawah ambang kurasi kita | N/A (orisinal) |
| Legalitas & keamanan | Berisiko UU PDP (rekam tanpa consent) + mem-patch source pihak ketiga (potensi melanggar ToS Hermes/WA) | Selaras UU PDP (consent lewat ekspor sadar pengguna) |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
- **Ide bagus yang layak dipertimbangkan (opsional, bukan wajib):** opsi "gaya bahasa" (formal vs
  santai/gaul) untuk ringkasan — skill kita saat ini hanya satu gaya bahasa baku. Bisa jadi
  fitur tambahan di versi mendatang, SELAMA tetap memakai jalur ekspor (bukan live recording).
- **Peringatan yang dikonfirmasi:** pendekatan "bot merekam live" jelas menimbulkan risiko privasi
  nyata di pasar (ada skill publik yang benar-benar melakukannya) — ini memperkuat pentingnya
  SKILL.md kita tetap tegas menolak permintaan serupa (sudah diuji di `examples/05-di-luar-cakupan.md`).

## Kesimpulan
Skill kita **unggul** untuk kebutuhan "ringkas grup WA dari ekspor, instan & aman" — pesaing yang
ditemukan tidak sebanding kualitasnya (di bawah ambang bukti kurasi) dan justru mengambil
pendekatan yang secara eksplisit dilarang oleh kebijakan Komunitech sendiri. Tidak ditemukan
pesaing sebanding yang memakai pendekatan **file ekspor** yang sama seperti skill kita.
