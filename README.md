# Komunitech Skills

Library **agent skills** siap pakai untuk pengusaha & profesional Indonesia, oleh
[komunitech.com](https://komunitech.com). Format terbuka **Agent Skills (SKILL.md)**, diuji untuk
**OpenClaw, OpenAI Codex, Claude Code, dan Cursor**.

> ⚠️ **Repo ini PRIVATE dan berisi produk berbayar.** Jangan ubah visibilitas repo menjadi publik
> dan jangan bagikan isi repo di luar tim internal.

## Isi library (per 2026-09-30)

| Jalur | Isi |
|---|---|
| **1. Skill** | 117 skill lulus uji internal (12 di antaranya sedang beta): keuangan & pajak, HR & gaji & KPI, marketing & strategi produk (positioning, riset pesaing, harga, peluncuran, uji pasar), toko online/marketplace, sales, customer service, produktivitas, data, kesehatan (khusus nakes), kripto |
| **2. Produk siap pakai pengganti SaaS** | Software yang jalan di komputer pembeli (data lokal, tanpa biaya bulanan), dioperasikan AI agent: kasir, stok, absensi, piutang, CRM WA, dasbor, PDF, serta asisten untuk Frappe Books, Dolibarr, hledger, Actual Budget, Grist, Vikunja, SiYuan, Open Notebook, Uptime Kuma, InvenTree, Umami (analitik web), listmonk (newsletter), Fider (masukan pelanggan), Odoo, Kanboard |
| **3. Solusi member VIP** | Paket skill + konfigurasi OpenClaw (jadwal, Telegram) + panduan: toko online, klinik, konsultan, usaha offline, kantor & manajemen, riset kripto & keuangan pribadi — lihat [`solusi-vip/`](solusi-vip/) |

Sumber kebenaran daftar skill, status, versi, tier, dan harga: [`catalog.csv`](catalog.csv).
Status mengikuti alur `ide → draft → uji → lulus → beta → rilis`; hanya `rilis` yang dijual ke pembeli.

## Model distribusi

| Kanal | Akses |
|---|---|
| **Member VIP** | Seluruh library + `solusi-vip/` + update berkala |
| **Ecer / bundle** | Per skill atau per paket tematik (10 bundle) di [`bundles/`](bundles/) |
| **Gratis** | Beberapa skill sederhana sebagai pengenalan (tier `gratis`) |

Setiap paket diberi **watermark lisensi** (nama/ID pembeli + kode lisensi unik) agar kebocoran bisa dilacak.

## Struktur repo

```
skills/<nama-skill>/     # SKILL.md, README.md (panduan pembeli), examples/, scripts/, tests/, LICENSE/ATTRIBUTION
catalog.csv              # katalog master (status, versi, tier, harga, platform teruji)
bundles/                 # definisi paket tematik (satu nama skill per baris)
solusi-vip/              # paket solusi per profesi untuk member VIP (OpenClaw)
docs/                    # instalasi per platform, panduan software lokal, uji platform, program beta
docs/jasa-setup/         # jasa setup berbayar: menu layanan (usulan harga), SOP teknisi, formulir persiapan member
research/                # backlog, riset harga, audit sumber & lisensi
rejected/                # skill yang gagal audit + alasannya
templates/               # template SKILL.md, README.md, ATTRIBUTION.md
scripts/                 # validate.py, build.py, uji_openclaw.sh
reports/                 # laporan per sesi kerja
koordinasi/              # papan tugas & rutinitas tim kurator
CLAUDE.md                # aturan kerja kurator (alur Tahap 1–8, lisensi, keamanan)
```

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
