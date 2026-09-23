# 00 — Uji banding pesaing

Tanggal uji: 2026-09-23 · Penguji: agent penguji independen (simulasi, Claude Code).

## Pencarian
- Web search: "openclaw skill invoice payment reminder follow-up clawhub SKILL.md",
  "github SKILL.md follow-up reminder accounts receivable agent skill",
  "skills.sh follow-up reminder skill sales leads CRM SKILL.md timesheet".
- Sumber yang dicek: ClawHub (clawhub.ai, API `api/v1/skills/<slug>`), clawskills.sh, aiagentsdirectory.com,
  VoltAgent/awesome-openclaw-skills (tautan hasil pencarian), anthropics/skills (tidak ada skill penagihan/pengingat),
  claude-office-skills `crm-automation` (sekuens CRM berbasis HubSpot/SaaS, bukan pengingat lokal),
  openaccountant/skills (keuangan pribadi, tanpa pengingat piutang).
- manairalabs/bicara-skills & alvinindra/bahasa-skills: **tidak bisa dibaca** (akses GitHub API repo tersebut
  diblokir di sesi ini). Dicatat jujur; tidak dinilai.
- Pesaing paling relevan: **invoice-chaser** oleh @audsmith28.
  - URL: https://clawhub.ai/audsmith28/invoice-chaser (SKILL.md dibaca lewat
    `https://clawhub.ai/api/v1/skills/invoice-chaser/file?path=SKILL.md`)
  - Lisensi: halaman ClawHub menyebut MIT-0 (field license di API versi terbaru kosong).
  - Sinyal: v1.1.0, 2.619 unduhan, 79 instal, 0 bintang, 0 komentar; moderasi ClawHub "clean", clawskills.sh
    menampilkan VirusTotal "Suspicious". Script (`setup.sh`, `chase.sh`, dll.) **tidak dijalankan** (aturan audit).
  - Hanya dibaca untuk dinilai; tidak ada teks yang disalin ke skill kita.

## Pendekatan pesaing (ringkas, parafrase)
Daftar invoice di `~/.config/invoice-chaser/invoices.json`, ditambah lewat `add-invoice.sh --number --client
--email --amount --due`. `chase.sh` dijalankan cron harian dan **mengirim email otomatis langsung ke klien**
lewat Gmail (skill `gog`, env `GOG_DEFAULT_ACCOUNT`) dengan tahap friendly → overdue → firm → final → eskalasi ke
manusia pada hari ke-60/75. Ada log kirim, jeda (pause until), arsip, laporan aging AR, `--dry-run`, batas email/hari.
Template berbahasa Inggris, mata uang $.

## Skenario 01 dijalankan dengan pendekatan pesaing (simulasi agent yang memuat invoice-chaser)
```
To add these invoices I need each client's email address (required by add-invoice.sh --email),
invoice numbers, and amounts as numbers. I'll assume net-30 terms and USD formatting unless configured.

Please provide:
- Bu Rina email, CV Maju email, Toko Sinar email, Pak Harto email
- Your Gmail account in GOG_DEFAULT_ACCOUNT and run scripts/setup.sh first

Parsed so far (please confirm):
INV 0412 | Bu Rina    | 4500000   | due 2026-10-03
INV 0398 | CV Maju    | 750000    | due 2026-09-20   (overdue 11 days)
INV 0405 | Toko Sinar | 1250000   | due 2026-10-02
(none)   | Pak Harto  | 2300000   | due 2026-10-01

Once added, chase.sh will email CV Maju today with the "Payment was due on..." template and
continue escalating automatically. Status report:
Current (0-30 days): $8,800,000 (4 invoices)   <- formatted with "$" per the template
Total Outstanding:   $8,800,000 (4 invoices)
```
(Parsing "4,5 jt", "750rb", "tgl 20/9" dikerjakan oleh LLM tanpa aturan tertulis; skill pesaing tidak punya
parser untuk format Indonesia. Tahun kabur tidak diatur.)

## Output skill kita
Lihat `01-piutang-toko-grosir.md` (rekap terlambat/hari ini/H-1, total tertunggak Rp 3.050.000, draf per
pelanggan dalam Bahasa Indonesia, dikirim sendiri oleh pemilik).

## Penilaian (1–5)
| Kriteria | invoice-chaser | pengingat-follow-up |
|---|---|---|
| Kualitas output untuk pemilik | 3 (laporan aging bagus, tapi butuh setup Gmail & config JSON) | 4 (rekap harian + draf siap salin) |
| Kesesuaian konteks Indonesia | 1 (Inggris, $, email-only, tanpa WA/Telegram, tanpa format "4,5 jt") | 5 (Rupiah, format tanggal/nominal lokal, WA/Telegram, sapaan) |
| Akurasi angka | 3 (tanpa aturan parsing; aging dihitung script) | 4 (aritmetika terverifikasi; ada cacat parsing "4,5,6 jt", nama hari timesheet) |
| Siap pakai untuk awam | 2 (setup.sh, env var, edit JSON) | 4 (satu kalimat, tanpa setup; jadwal opsional) |
| Keamanan/kepatuhan (keputusan pemilik) | 1 (bot menagih klien otomatis; menyimpan email klien) | 5 (pemilik yang mengirim; tolak kontak; tanpa broadcast) |
| Cakupan fitur lain | pause-until, log kirim, arsip, aging bucket, rate limit | prospek, janji, timesheet jam × tarif |

**Kesimpulan:** skill kita **menang** untuk pasar sasaran dan sesuai keputusan pemilik. Pesaing unggul di
beberapa fitur operasional.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Log pengingat per item** (mis. perintah "sudah saya ingatkan #2") → script tahu berapa kali pemilik sudah
   menagih, sehingga nada draf bisa naik dengan dasar data (sekarang dibatasi sampai "pemberitahuan tertulis"
   karena script tidak tahu riwayat).
2. **Ringkasan umur piutang** (0–30 / 31–60 / 61–90 / >90 hari) di rekap mingguan.
3. **Jeda sampai tanggal** untuk pelanggan yang minta perpanjangan (mirip `tunda`, tetapi dengan alasan tercatat).
4. **Pratinjau sebelum pertama kali** (dry-run) untuk jadwal otomatis. Skill kita sudah punya `automations run --wait`.
