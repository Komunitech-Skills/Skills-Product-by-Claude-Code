# Atribusi

Skill `laporan-insiden-usaha` **terinspirasi dari struktur** skill `incident-postmortem`
dan `customer-incident-update` karya **Mohit Aggarwal**, dari repo publik
`pm-claude-skills`, dan **diubah/diperluas secara substansial** untuk konteks UMKM
Indonesia:

- Sumber: https://github.com/mohitagw15856/pm-claude-skills
  (`skills/incident-postmortem/`, `skills/customer-incident-update/`,
  `plugins/pm-crisis/skills/apology-letter/`)
- Cara ambil: `git clone --depth 1` ke scratchpad terpisah, **tidak dijalankan**, dibaca
  penuh sebelum dipakai.
- Commit terbaru repo saat diambil: `f6ca7934` ("release: v80.0.0 — the promote loop"),
  diambil dan ditinjau 2026-09-26. Riwayat commit dicek lewat `git log --follow` pada file
  `skills/incident-postmortem/SKILL.md`: 214 commit tersebar berbulan-bulan dengan rilis
  bertahap (mis. `v76.1`), bukan dump satu hari — memenuhi syarat "umur & perawatan" di
  pedoman kurasi Komunitech tahap 2.
- Lisensi sumber: **MIT**. Diverifikasi langsung dari file `LICENSE` di root repo (bukan
  diasumsikan dari README) — isinya teks MIT standar, hak cipta "Copyright (c) 2026 Mohit
  Aggarwal".

**Bukan salinan verbatim.** Struktur bagian (kronologi → dampak → akar masalah → tindakan
→ pencegahan) dan gagasan "update sesuai tahap" dipelajari dari sumber, tapi seluruh isi
SKILL.md, README, panduan 5 Kenapa, dan kedua contoh ditulis ulang dari nol dalam Bahasa
Indonesia dengan konteks usaha kecil, bukan insiden software/engineering.

Adaptasi oleh Komunitech (komunitech.com). Penggunaan versi adaptasi ini tunduk pada
`LISENSI.txt` yang disertakan dalam paket pembelian, tanpa mengurangi ketentuan lisensi
MIT untuk bagian yang berasal dari karya asli (lihat `LICENSE-MIT`).

## Yang diambil dari sumber (gagasan, bukan teks)
- Gagasan blameless framing: akar masalah diarahkan ke sistem/proses, bukan ke individu
  (dari `incident-postmortem` — "root cause the system, never the person").
- Format "5 Kenapa" (five-whys) untuk mencari akar masalah, berhenti di penyebab yang bisa
  diperbaiki, bukan di kesalahan orang.
- Struktur umum: kronologi (timeline) → dampak (impact, berangka) → akar masalah → action
  item dengan pemilik & tenggat.
- Gagasan draf komunikasi pelanggan yang jujur tanpa over-promise (dari
  `customer-incident-update` & `apology-letter`: akui masalah spesifik, jangan janji
  berlebihan, sebutkan langkah konkret).

## Yang diubah / ditambahkan oleh Komunitech
1. **Konteks total diganti dari insiden software/engineering (P1/P2/SEV, outage,
   deployment) ke insiden operasional UMKM** (pesanan salah kirim, stok promo habis,
   mesin kasir/QRIS error, karyawan telat buka toko) — sumber sama sekali tidak membahas
   konteks ritel/UMKM fisik.
2. **Bahasa Indonesia penuh**, format siap tempel ke WA (bukan status-page/Slack seperti
   sumber).
3. **Penanganan khusus kebocoran data pelanggan ringan**: arahan umum ke kewajiban
   pemberitahuan UU 27/2022 (UU PDP) dan rujukan ke skill `kebijakan-privasi-pdp` di
   perpustakaan ini — tidak ada di sumber (sumber berkonteks AS/GDPR-agnostic, tidak
   membahas regulasi tertentu).
4. **Penanda `[isi: ...]` untuk info yang tidak diberikan pengguna** (anti-mengarang
   angka/nama/tanggal) — sumber mengasumsikan semua input sudah tersedia dari sistem
   monitoring/log, versi ini dirancang untuk pengguna awam yang mengetik manual.
5. **Digabung jadi satu skill tunggal** (kronologi + dampak + akar masalah + pencegahan +
   draf minta maaf + ringkasan WA) — sumber memisahkan ini jadi beberapa skill terpisah
   (`incident-postmortem`, `customer-incident-update`, `apology-letter`) yang saling
   merujuk lewat "spine" multi-skill; digabung karena target pembeli (UMKM) butuh satu
   perintah sederhana, bukan mengelola beberapa skill berantai.
6. **Dihapus total**: rujukan ke tool/skill lain di ekosistem sumber (`action-runner`,
   `professional-brain`, `/slo-error-budget`, `/debugging-log-analyser`, `/oncall-runbook`,
   integrasi MCP), diagram Mermaid Gantt teknis, istilah P1/P2/SEV — tidak relevan dan
   akan membingungkan pengguna awam UMKM.
7. **Rujukan silang ke skill lain di library Komunitech** (`notulen-rapat`,
   `balas-chat-cs`, `laporan-status-kantor`, `surat-peringatan-karyawan`,
   `kebijakan-privasi-pdp`) — konsep "perpustakaan skill terhubung" tidak ada di sumber.
8. **Dihapus**: seluruh contoh dan template sumber (worked example insiden software,
   agenda rapat review 45 menit) — diganti 2 contoh baru dari nol dengan kasus UMKM lokal
   (pesanan salah kirim promo 9.9, QRIS error jam makan siang).

## Audit keamanan sumber (pedoman kurasi Komunitech)
- Seluruh isi `SKILL.md` dari `skills/incident-postmortem/`, `skills/customer-incident-
  update/`, dan `plugins/pm-crisis/skills/apology-letter/` dibaca penuh sebelum dipakai
  sebagai inspirasi. Repo **tidak dijalankan** — hanya `git clone --depth 1`, tidak ada
  script dieksekusi.
- Tidak ditemukan file `scripts/` (`.py`/`.sh`) di ketiga folder skill yang dijadikan
  sumber — murni instruksi teks/markdown.
- Dicek pola perintah destruktif, pola unduh-pipe-ke-shell, kode ter-obfuskasi, pengiriman
  data ke server luar, pembacaan kredensial/SSH key: **nihil kecocokan** (`grep -rniE`
  untuk perintah unduh, `eval`/`exec`, `base64 -d`, `ssh`, `/etc/passwd`, kata kunci
  API key/token).
- Dicek pola prompt injection tersembunyi (`ignore previous/above instructions`,
  `do not tell`, `without telling/asking`, `silently`, `bypass`): **nihil kecocokan**.
  Satu-satunya baris yang cocok pola pencarian kasar ("token") adalah frasa "token praise"
  dan "not token" dalam konteks kualitas tulisan (bukan instruksi tersembunyi) —
  diperiksa manual dan aman.
- Tidak ditemukan API key, token, atau data pribadi tertanam.
- Riwayat commit gradual (214 commit, versi berjenjang v76–v80) dikonfirmasi lewat
  `git fetch --depth 200` + `git log --follow` — bukan pola AI slop (dump ratusan skill
  dalam satu hari).
- **Hasil: LULUS audit keamanan.**

## Teks lisensi asli (MIT)
Lihat file `LICENSE-MIT` pada folder ini — disalin persis dari
`https://github.com/mohitagw15856/pm-claude-skills/blob/main/LICENSE`.
