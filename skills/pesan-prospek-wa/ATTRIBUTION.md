# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi prinsip cold outreach B2B yang terbukti dari skill publik berlisensi MIT, ditulis ulang total untuk saluran WhatsApp dan konteks Indonesia (lihat "Apa yang diubah/ditambahkan" di bawah).

## Sumber yang diadaptasi
- **Repo:** [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
- **Skill sumber:** `skills/cold-email/`
- **Pembuat:** Corey Haines
- **Lisensi:** MIT (dicek langsung di file `LICENSE` repo sumber via `git show HEAD:LICENSE` — lihat `LICENSE-MIT` di folder ini untuk teks lengkapnya)
- **Commit yang dipakai:** `5b2c0007766c6a1cf1d53fd8fc73e979e0821022` (Fri Sep 4 21:48:02 2026 -0700), diperoleh lewat `git clone --depth 1 --filter=blob:none --sparse` pada 2026-09-25, `git sparse-checkout set skills/cold-email`.
- **Bagian yang dipelajari:** `skills/cold-email/SKILL.md` dan seluruh isi `references/` di dalamnya (`frameworks.md`, `personalization.md`, `subject-lines.md`, `follow-up-sequences.md`, `benchmarks.md`) — prinsip "tulis seperti rekan sejawat, bukan vendor", struktur pesan (observasi → masalah → bukti → ajakan), level personalisasi, dan larangan taktik manipulatif ("just checking in", urgensi palsu, jargon).
- **Bagian yang TIDAK dipakai:** `evals/evals.json` (skema evaluasi internal repo sumber, bukan konten produk) dan seluruh skill lain di repo tersebut (di luar cakupan `pesan-prospek-wa`).

## Audit lisensi & keamanan (Tahap 2–3 CLAUDE.md)
- `LICENSE` root repo sumber dibaca langsung via `git show HEAD:LICENSE`: MIT, Copyright (c) 2025 Corey Haines — mengizinkan modifikasi & penjualan turunan. Sesuai `research/sources/kurasi-terbukti-2026-09-24.md`, seluruh repo (termasuk `cold-email`) sudah **LULUS audit** popularitas (45.000★/7.800 fork lintas beberapa sumber independen), pembuat kredibel, dan keamanan.
- Seluruh isi `skills/cold-email/` (SKILL.md + 5 file `references/` + `evals/evals.json`) dibaca penuh oleh sesi ini. Tidak ada script (`scripts/`) di skill sumber ini — murni instruksi Markdown + data.
- Diperiksa manual untuk: perintah destruktif, pengiriman data ke server luar, permintaan kredensial/SSH key/data browser, `curl`/`wget` yang dieksekusi otomatis, kode ter-obfuscate, dan instruksi tersembunyi yang menyuruh agent mengabaikan pengguna/menonaktifkan konfirmasi/mengirim file — **nihil ditemukan**. Tidak ada API key, token, atau data pribadi tertanam.
- Kesimpulan: **lolos audit**, aman diadaptasi.

## Apa yang diubah/ditambahkan (nilai tambah ATM)
Sumber ditulis untuk **cold email B2B berbahasa Inggris** dengan asumsi tim SDR/sales enterprise. Perubahan berikut menulis ulang total untuk **pesan pembuka WhatsApp** UMKM/profesional Indonesia:

1. **Ganti saluran total: email → WhatsApp.** Cold email tidak lazim dipakai UMKM/profesional Indonesia; prospek B2B/B2C lokal jauh lebih responsif lewat WA. Konsekuensinya bukan sekadar ganti kata "email" jadi "WA" — subjek email dihapus, panjang pesan disesuaikan layar HP (bukan panjang email desktop 25–75 kata ala benchmark sumber), dan struktur multi-paragraf email diringkas jadi pesan chat yang wajar dibalas dalam satu sentuhan jari.
2. **Wajib menyebut asal kontak.** Tidak ada di skill sumber sama sekali (SDR B2B AS umumnya membeli/scrape data lead, bukan konteks yang relevan/legal di Indonesia). Di sini menjadi langkah wajib: sebutkan dari mana nomor didapat (referral, pameran, Google Maps, IG, grup komunitas) — inti dari menghindari kesan spam/penipuan di WhatsApp Indonesia.
3. **Kepatuhan hukum Indonesia** (`references/dasar-hukum-wa.md`): UU PDP No. 27/2022 (dasar pemrosesan data kontak, larangan pakai data bocoran/beli database), UU ITE & UU Perlindungan Konsumen No. 8/1999 (klaim jujur, dilarang menyamar/memanipulasi) — sama sekali tidak ada di sumber (sumber berbasis hukum AS/GDPR Eropa sekilas di `benchmarks.md`, tidak dibahas mendalam maupun untuk konteks Indonesia).
4. **Sapaan & nada lokal**: Pak/Bu/Kak, bahasa Indonesia sehari-hari sopan, kalibrasi B2B vs B2C ala Indonesia — sumber berbasis nada Inggris Amerika ("write like a peer", kontraksi bahasa Inggris) yang tidak bisa diterjemahkan langsung.
5. **Jam kirim wajar WIB/WITA/WIT** — konsep waktu lokal Indonesia sama sekali tidak dibahas sumber (sumber membahas "Tuesday-Thursday 9-11AM" ala kalender kerja AS).
6. **3 varian per pesan (singkat/sedang/dengan nilai)** menggantikan konsep "subject line + body + follow-up sequence" email — struktur output benar-benar berbeda karena WA adalah percakapan langsung, bukan inbox.
7. **Tegas memisahkan dari skill lain di katalog kita**: follow-up-prospek (pesan susulan), broadcast-wa (promo massal — skill ini eksplisit MENOLAK dipakai untuk blast), riset-calon-pelanggan (tahap mencari data, bukan mengirim pesan pertama) — pemisahan cakupan ini spesifik untuk struktur katalog Komunitech, tidak ada di sumber.
8. **Checklist anti-spam/anti-blokir WhatsApp** dan **script Python teruji** (`scripts/cek_pesan.py`, 43 kasus uji termasuk data rusak: nomor kosong/bukan angka/kode negara asing, jam format salah, file tidak ada) yang memeriksa draf pesan secara otomatis (panjang, kalimat kepanjangan, kata pemicu spam, huruf kapital berlebihan, jumlah link, asal kontak, opsi keluar, jam kirim) dan membangun tautan wa.me — sumber tidak menyertakan script sama sekali untuk skill ini.
9. **Disclaimer bukan nasihat hukum** dan tanggal cek dasar hukum — mekanisme kepatuhan yang tidak ada di sumber (sumber fokus performa/reply rate, bukan kepatuhan regulasi lokal).

## Pembagian lisensi bagian ini
- **Prinsip struktur pesan yang diadaptasi** (pola observasi→masalah→bukti→ajakan, larangan taktik manipulatif/"just checking in"/urgensi palsu, konsep level personalisasi) di `SKILL.md` dan `references/pola-pembuka.md`: turunan dari materi MIT `coreyhaines31/marketingskills` (skill `cold-email`) — tunduk pada ketentuan MIT (lihat `LICENSE-MIT`), sudah ditulis ulang total & dilokalkan penuh untuk WhatsApp Indonesia.
- **Semua bagian lain** — `references/dasar-hukum-wa.md`, `references/checklist-anti-blokir.md`, `templates/`, `scripts/`, `tests/`, `examples/`, dan `README.md` — adalah karya orisinal Komunitech, tidak mengandung materi pihak ketiga, dan boleh diperlakukan sebagai proprietary Komunitech.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, ditambah ketentuan MIT pada bagian yang disebut di atas.
