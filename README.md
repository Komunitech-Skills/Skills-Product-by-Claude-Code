# Komunitech Skills

Library **agent skills** siap pakai untuk pengusaha & profesional Indonesia, oleh
[komunitech.com](https://komunitech.com). Format terbuka **Agent Skills (SKILL.md)**, diuji untuk
**OpenClaw, OpenAI Codex, Claude Code, dan Cursor**.

> ⚠️ **Repo ini PRIVATE dan berisi produk berbayar.** Jangan ubah visibilitas repo menjadi publik
> dan jangan bagikan isi repo di luar tim internal.

## Isi library (per 2026-10-05)

Katalog: **136 skill** = 110 `beta` + 22 `lulus` + 1 `uji` + 3 `arsip` (133 aktif; 93 orisinal, 43 kurasi). Belum ada yang `rilis`.
Kategori: Produktivitas (25), Keuangan & Akuntansi (24), Marketing & Konten (23), Data & Analisis (12), HR (10),
Sales (9), E-commerce/Marketplace Indonesia (8), Customer Service (7), Legal & Dokumen (3), Pendidikan (1), Kehidupan Pribadi (1).

| Jalur | Isi |
|---|---|
| **1. Skill** | 133 skill aktif: keuangan & pajak, HR & gaji & KPI, marketing & strategi produk (positioning, riset pesaing, harga, peluncuran, uji pasar), toko online/marketplace, sales, customer service, produktivitas, data, kesehatan (khusus nakes), kripto. Tiga skill diarsipkan (`caption-sosmed-umkm`, `kalender-konten-30hari`, `brainstorming-ide-usaha`; folder tidak dihapus) |
| **2. Produk siap pakai pengganti SaaS** | Software yang jalan di komputer pembeli (data lokal, tanpa biaya bulanan), dioperasikan AI agent: kasir, stok, absensi, piutang, CRM WA, dasbor, PDF, serta asisten untuk Frappe Books, Dolibarr, hledger, Actual Budget, Grist, Vikunja, SiYuan, Open Notebook, Uptime Kuma, InvenTree, Umami (analitik web), listmonk (newsletter), Fider (masukan pelanggan), Odoo, Kanboard. Nama produk pihak ketiga hanya penyebut; **tidak berafiliasi** |
| **3. Solusi member VIP** | Paket skill + konfigurasi OpenClaw (jadwal, Telegram) + panduan: toko online, klinik, konsultan, usaha offline, kantor & manajemen, riset kripto & keuangan pribadi — lihat [`solusi-vip/`](solusi-vip/) |

Kurasi kini mencakup proyek top **semua lisensi** (keputusan 2026-10-05); proyek bersetup berat boleh dikurasi
hanya untuk alat **internal** Komunitech (tidak dijual ke audiens awam, tidak dipasang di bot produksi).

Sumber kebenaran daftar skill, status, versi, tier, dan harga: [`catalog.csv`](catalog.csv).
Status mengikuti alur `ide → draft → uji → lulus → beta → rilis`; hanya `rilis` yang dijual ke pembeli.

## Model distribusi

| Kanal | Akses |
|---|---|
| **Member VIP** | Seluruh library + `solusi-vip/` + update berkala |
| **Ecer / bundle** | Per skill atau per paket tematik (10 bundle) di [`bundles/`](bundles/) |
| **Gratis** | Beberapa skill sederhana sebagai pengenalan (tier `gratis`) |

Setiap paket diberi **watermark lisensi** (nama/ID pembeli + kode lisensi unik) agar kebocoran bisa dilacak.

## Lisensi sumber & atribusi

Skill orisinal berlisensi **Proprietary Komunitech** (lihat [`LICENSE`](LICENSE), masih DRAFT). Skill kurasi memakai lisensi sumbernya:

| Lisensi sumber | Kewajiban |
|---|---|
| MIT / BSD-3-Clause | Teks lisensi + atribusi di folder skill (`LICENSE-MIT*`, `LICENSE-BSD`, `ATTRIBUTION.md`) |
| Apache-2.0 | `LICENSE-APACHE*`, atribusi, `NOTICE` bila ada, keterangan bahwa file diubah |
| CC BY 4.0 | Atribusi di `ATTRIBUTION.md` |
| GPL/AGPL/CC-BY-SA | Turunan wajib berlisensi sama dan boleh dibagikan ulang (saat ini tidak ada skill salinan; skill asisten AGPL seperti Fider/listmonk/SiYuan/Vikunja/Frappe Books adalah panduan orisinal, softwarenya tidak didistribusikan) |
| CC-BY-NC / tanpa lisensi / proprietary | Dilarang disalin; hanya "tulis ulang bersih" (CLAUDE.md Tahap 2) |

Setiap skill punya `ATTRIBUTION.md` atau `LICENSE*` di foldernya; jangan dihapus saat memaketkan.

## Struktur repo

```
skills/<nama-skill>/     # SKILL.md, README.md (panduan pembeli), examples/, scripts/, tests/, LICENSE/ATTRIBUTION
catalog.csv              # katalog master (status, versi, tier, harga, platform teruji)
bundles/                 # definisi paket tematik (satu nama skill per baris)
solusi-vip/              # paket solusi per profesi untuk member VIP (OpenClaw)
docs/                    # instalasi per platform, panduan software lokal, uji platform, program beta
docs/jasa-setup/         # jasa setup berbayar: menu layanan (usulan harga), SOP teknisi, formulir persiapan member
research/                # backlog, riset harga, audit sumber & lisensi
promosi/                 # bahan jualan sebelum/sesudah (SSOT sebelum-sesudah.jsonl, halaman HTML, CARA-UJI); hanya skill lolos uji
rejected/                # skill yang gagal audit + alasannya
templates/               # template SKILL.md, README.md, ATTRIBUTION.md
scripts/                 # validate.py, build.py, uji_openclaw.sh, promosi_sebelum_sesudah.py
reports/                 # laporan per sesi kerja
koordinasi/              # papan tugas, rutinitas, pra-cek & catatan gelombang pilot Telegram
CLAUDE.md                # aturan kerja kurator (alur Tahap 1–8, lisensi, keamanan)
```

## Alur uji

1. Maker ≠ tester: pembuat skill tidak menguji skill-nya sendiri.
2. **Uji internal OpenClaw sebelum/sesudah** (skill dimatikan vs aktif, agent yang sama dengan bot Telegram). Lulus bila skor sesudah ≥ 8 **dan** selisih rata-rata ≥ 1,5; hasil di `examples/00-openclaw-sebelum-sesudah.md`.
3. **Konteks kanal Telegram:** `scratchpad/openclaw-real/uji-tg.sh` (`openclaw agent --local --channel telegram`, tanpa `--deliver`); pra-cek wajib untuk setiap calon gelombang Telegram.
4. **Pilot Telegram bot-to-bot** (grup uji, maks. 10 pesan per gelombang, berurutan dengan jeda, tanpa balas-otomatis) hanya untuk skill lolos uji internal dan atas persetujuan pemilik. Laporan ke topik "Ringkasan uji".
5. Hasil lolos masuk `promosi/` ([`promosi/README.md`](promosi/README.md)); skill di bawah acuan tidak diiterasi lagi.

## Instalasi (untuk pembeli)

Ekstrak ZIP, lalu salin folder skill ke lokasi skill platform yang dipakai (OpenClaw, Codex,
Claude Code, Cursor). Rincian lokasi yang sudah diverifikasi ada di
[`docs/instalasi.md`](docs/instalasi.md) (ikut di setiap paket).

## Validasi & build paket

Butuh Python 3.9+ (tanpa dependensi tambahan).

```bash
python3 scripts/validate.py          # cek format semua skill & katalog (wajib lolos sebelum commit)
bash scripts/uji_openclaw.sh         # uji muat di OpenClaw (eligible/terlihat model/bisa dipanggil)

python3 scripts/build.py --pembeli "Nama Pembeli" --skill kasir-lokal       # paket ecer
python3 scripts/build.py --pembeli "Nama Pembeli" --bundle paket-toko-online # paket bundle
python3 scripts/build.py --pembeli "Member VIP #0123" --vip                  # paket VIP
python3 scripts/build.py --pembeli "Beta #01" --vip --beta                   # paket beta tester
```

Hasil ada di `dist/` (**tidak** ikut di-commit karena berisi data pembeli). Catat kode lisensi di sistem penjualan.

## Kontribusi

Baca [CONTRIBUTING.md](CONTRIBUTING.md) dan [CLAUDE.md](CLAUDE.md) sebelum menambah atau mengubah skill.
