# Perawatan dokumen repo — 2026-10-17 (Akun A)

## Perubahan
- `README.md`: angka katalog, kategori, jalur, bundle, daftar skrip & struktur diperbarui dari `catalog.csv`/`bundles/`/`scripts/`.
- `CONTRIBUTING.md`: tidak ada rujukan usang yang ditemukan; ditambah rujukan skrip bantu.
- `docs/instalasi.md`: catatan untuk pembeli paket VIP.

## Temuan untuk pemilik
- `build.py --vip` tanpa `--beta` melewati skill berstatus selain `rilis`; saat ini 0 skill `rilis`, jadi ZIP VIP untuk pembeli akan gagal ("Tidak ada skill untuk dipaketkan") sampai ada skill `rilis`. Paket beta memakai `--vip --beta`.
- ZIP VIP hanya memuat file `.md` dari `solusi-vip/` (folder `uji-openclaw/` yang berisi non-.md tidak ikut) dan `templates/openclaw-AGENTS-komunitech.md`.

## CHANGELOG tertinggal / tidak ada
Dibanding `catalog.csv` (entri versi teratas di `skills/<skill>/CHANGELOG.md`). 118 skill sudah sinkron; 25 perlu dicek.

| Skill | Status | Versi catalog | Versi teratas CHANGELOG |
|---|---|---|---|
| caption-sosmed-umkm | arsip | 1.1.4 | (tidak ada file) |
| lowongan-kerja | beta | 1.0.5 | 1.0.3 (maks 1.0.5) |
| kalender-konten-30hari | arsip | 1.0.8 | (tidak ada file) |
| hitung-hpp | beta | 1.0.4 | 1.0.3 (maks 1.0.4) |
| perjanjian-sederhana | beta | 1.0.8 | 1.0.4 (maks 1.0.8) |
| hitung-thr | beta | 1.0.11 | 1.0.4 (maks 1.0.11) |
| agen-cs-toko | beta | 1.0.11 | 1.0.6 (maks 1.0.11) |
| cv-lamaran-ats | beta | 1.1.3 | (tak ada entri versi) |
| laporan-status-kantor | beta | 1.0.8 | 1.0.3 (maks 1.0.8) |
| pantau-pasar-kripto | beta | 1.0.11 | (tak ada entri versi) |
| rencana-pelajaran-guru | beta | 1.0.11 | 1.0.4 (maks 1.0.11) |
| pesan-prospek-wa | beta | 1.0.7 | 1.0.6 (maks 1.0.7) |
| brainstorming-ide-usaha | arsip | 1.0.7 | (tidak ada file) |
| kebijakan-privasi-pdp | beta | 1.0.8 | (tak ada entri versi) |
| sop-onboarding | beta | 1.0.7 | (tak ada entri versi) |
| tender-checklist | beta | 1.0.9 | (tak ada entri versi) |
| siyuan-sop | beta | 1.0.11 | (tak ada entri versi) |
| odoo-usaha | beta | 1.0.5 | (tak ada entri versi) |
| spt-tahunan-op | beta | 1.0.7 | (tak ada entri versi) |
| kanboard-papan-kerja | beta | 1.0.6 | (tak ada entri versi) |
| seleksi-cv-pelamar | beta | 1.0.2 | (tak ada entri versi) |
| landing-page-siap-tayang | beta | 1.0.3 | (tak ada entri versi) |
| persiapan-jual-atau-wariskan-usaha | lulus | 1.0.1 | (tak ada entri versi) |
| jadwal-pelajaran-sekolah | arsip | 1.0.1 | (tidak ada file) |
| panduan-wawancara-kerja | beta | 1.0.3 | (tak ada entri versi) |
