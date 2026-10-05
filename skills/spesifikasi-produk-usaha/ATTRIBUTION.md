# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Kerangka dokumen (bagian PRD), kerangka roadmap berbasis hasil, dan rumus RICE/ICE diadaptasi dari dua sumber, lalu seluruhnya ditulis ulang untuk pemilik usaha Indonesia.

## Sumber
1. **phuryn/pm-skills** - https://github.com/phuryn/pm-skills - MIT, Copyright (c) 2026 Pawel Huryn. Bagian: `pm-execution/skills/create-prd`, `outcome-roadmap`, `prioritization-frameworks`. Teks lisensi: `LICENSE-MIT`.
2. **product-on-purpose/pm-skills** - https://github.com/product-on-purpose/pm-skills - Apache-2.0, Copyright 2026 Jonathan Prisant. Bagian: `skills/deliver-prd`. Teks lisensi: `LICENSE-APACHE`; `NOTICE` (repo asal tidak punya NOTICE, dicek 2026-09-29).

## Audit (Tahap 3)
Diambil 2026-09-29. Hanya berkas Markdown (`SKILL.md`) yang dibaca; tidak ada script dari sumber dan **tidak ada yang dijalankan atau disalin**. Diperiksa: tidak ada prompt injection, instruksi tersembunyi, pengiriman data, kunci API, atau tautan berbahaya. Kesimpulan: lolos. Sinyal bukti dicek ulang oleh penguji independen 2026-09-29 lewat GitHub API (lihat `examples/HASIL-UJI.md`): phuryn/pm-skills 26,6 ribu bintang, MIT, aktif (kuat); product-on-purpose/pm-skills 700 bintang, Apache-2.0, aktif (cukup kuat). Teks lisensi identik dengan hulu. Label PERLU REVIEW dicabut (v1.0.1).

## Pernyataan perubahan (wajib Apache-2.0 bagian 4b)
Materi asal **telah diubah** oleh Komunitech: diterjemahkan ke Bahasa Indonesia dan dipadatkan; struktur PRD 8 bagian dan bagian PRD "deliver-prd" diganti menjadi 11 bagian untuk produk fisik/jasa UMKM (resep/BOM, kemasan, HPP target, standar mutu, pengingat izin); bagian khusus rekayasa perangkat lunak/AI (AI Behavior, Agent Execution Contract, integrasi memori proyek) dibuang; seluruh berkas lain ditulis baru.

## Nilai tambah Komunitech
1. Templat per jenis usaha (F&B, fashion, kosmetik, kerajinan, digital/jasa) dan brief maklon/supplier/desainer.
2. **Script baru `scripts/prioritas.py`** (RICE/ICE, `Decimal`, input Indonesia: `80%`, `0,5`, `1.500`, penolakan baris rusak tanpa menebak) + 40 uji regresi (`tests/uji_regresi.py`), pembagian Sekarang/Berikutnya/Nanti dengan opsi kapasitas.
3. HPP target dan rujukan ke `hitung-hpp`, `harga-jual-marketplace`, `validasi-ide-produk-baru`.
4. Pengingat izin PIRT/BPOM MD/TR/halal/notifikasi kosmetik/SNI wajib dengan dasar aturan, tanggal cek, dan tautan resmi (`references/perizinan-produk.md`), catatan versi resep/spesifikasi.
5. Contoh kasus lokal (fiktif), README pembeli, batasan klaim kesehatan.

Bagian berkas asli Komunitech (SKILL.md, script, README, contoh) tunduk pada `LISENSI.txt` paket pembelian; bagian turunan tetap tunduk pada lisensi sumbernya.
