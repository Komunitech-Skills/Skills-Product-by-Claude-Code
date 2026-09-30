# Sumber ATM: marketingskills `referrals` (untuk skill `program-referral-loyalitas`) - 2026-09-30

| Hal | Catatan |
|---|---|
| Sumber | skill `referrals` (SKILL.md v2.0.1 + `references/program-examples.md`, `viral-mechanisms.md`, `affiliate-programs.md`) |
| URL | https://github.com/coreyhaines31/marketingskills (folder `skills/referrals/`) |
| Pembuat | Corey Haines (perorangan; repo koleksi 3-4 skill kita sebelumnya sudah dipakai) |
| Snapshot | `git clone --depth 1` 2026-09-30, commit `5b2c0007766c6a1cf1d53fd8fc73e979e0821022` (commit tanggal 2026-09-04) |
| Lisensi | MIT, Copyright (c) 2025 Corey Haines (file `LICENSE` di root dibaca; disalin ke skill sebagai `LICENSE-MIT-marketingskills`) |
| Sinyal bukti | Bintang ±52 rb, fork ±7,8 rb (GitHub API, dicek 2026-09-30 di `research/` kandidat); aktif (push 5 Sep 2026); dipakai untuk 3 skill kita lain yang sudah lulus; ada folder `evals`. Lolos >= 3 sinyal (popularitas, perawatan, komunitas/fork, isi berstruktur). |
| Audit keamanan | Isi folder `referrals/` = 4 file `.md` + `evals/evals.json`; **tidak ada script** dan tidak ada yang dijalankan. Dibaca seluruhnya: tidak ada instruksi menyuruh agent mengabaikan pengguna, mengirim file, atau menonaktifkan konfirmasi; tidak ada kunci/token tertanam. Rujukan ke `tools/REGISTRY.md` (Rewardful, Tolt, dll.) adalah layanan SaaS pihak ketiga dan tidak dipakai. |
| Skill lain dicek | `churn-prevention` (alur pembatalan & dunning langganan berbasis SaaS): tidak relevan untuk UMKM barang/jasa, tidak dipakai. Tidak ada skill "loyalty" terpisah di repo. |
| Keputusan | **DIPAKAI (ATM, MIT, atribusi).** Nilai tambah: seluruh konteks UMKM Indonesia, script Python `hitung_referral.py` (4 perintah, uji regresi 26 kasus), pola per usaha, anti-curang, S&K, teks WA/IG, kepatuhan UU 8/1999, UU 27/2022, UU 7/2014, dan aturan "tanpa blast". |

## Yang diadaptasi (ide/struktur, ditulis ulang)
- Alur pikir "momen pemicu -> ajakan -> konversi -> hadiah" dan pilihan hadiah satu sisi/dua sisi/bertingkat.
- Saran memicu ajakan di momen puas dan mengurangi gesekan (teks siap pakai).
- Kerangka ukuran: tingkat merujuk, konversi, ROI program, biaya per pelanggan via referral dibanding kanal lain.
- Rumus batas hadiah dari nilai seumur pelanggan dikali margin kotor (dirombak: 30% dari laba kotor seumur pelanggan sebagai aturan praktis berlabel).

## Yang TIDAK dipakai
Program afiliasi SaaS (komisi berulang, buyout ~12x, aturan 20/80 afiliasi, peluncuran afiliasi), mekanisme viral produk digital (badge "Powered by", embed), contoh perusahaan asing (Dropbox, Uber, Notion, Morning Brew), harga dolar, dan tabel integrasi alat SaaS.
