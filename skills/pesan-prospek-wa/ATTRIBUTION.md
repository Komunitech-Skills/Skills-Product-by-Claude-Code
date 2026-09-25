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

## Riwayat versi

### v1.0.2 (2026-09-25) — perbaikan kecil dari uji ulang v1.0.1 (skor 9/10)
- N1: `cek --file` membaca file UTF-8 ber-BOM dan cp1252 (Notepad lama) tanpa traceback; file biner → pesan ramah.
- N3: WIB/WITA/WIT tidak lagi dianggap huruf kapital berlebihan; checklist emoji diselaraskan dengan batas script (maks 3).
- Sisa untuk versi berikut: deteksi asal kontak masih meleset untuk frasa "bertemu Ibu di … Expo"/"merekomendasikan" dan salah-positif "dari teman-teman …" (N2), serta temuan rendah N4–N9 di `examples/06-uji-ulang-v1.0.1.md`.

### v1.0.1 (2026-09-25) — revisi temuan penguji independen (`examples/HASIL-UJI.md`, skor 8/10)
Perbaikan berikut TIDAK mengubah `examples/00-*`, `examples/01-05-*`, atau `HASIL-UJI.md` (bukti uji dipertahankan apa adanya untuk audit berikutnya):
- **B1 (tinggi):** `KATA_KUNCI_ASAL_KONTAK` di `scripts/cek_pesan.py` ditulis ulang, diturunkan langsung dari setiap pola di `references/pola-pembuka.md` (referral, pameran/expo/bazar, Google Maps, Instagram/IG/TikTok, grup komunitas, website) sehingga tidak lagi bertentangan dengan referensinya sendiri; "dari bapak/ibu" sendirian dibuang karena memicu salah-positif.
- **B2:** `normalisasi_nomor_wa` mengoreksi salah ketik "+62 0812…" dan membuang awalan internasional "00…"; hanya menerima digit ASCII (menolak digit Unicode full-width/Arab-Indik dengan pesan yang benar); memvalidasi pola & panjang nomor seluler Indonesia (62 + 9-12 digit diawali "8"), menolak nomor 14+ digit atau bukan pola 08xx dengan pesan jelas.
- **B3:** `SINGKATAN_AMAN` diperluas dengan istilah B2B/UMKM Indonesia yang lazim kapital (HRD, PPN, PPh, SPT, BPJS, NPWP, PT, CV, UMKM, WA, IG, PDF, SOP, CEO, KTP, HIPMI, KADIN, APINDO, dll.).
- **B4:** `--jam-kirim` menerima `HH:MM`, `HH.MM`, dan 4 digit (`1930`); ditambah `--zona` (WIB/WITA/WIT); SKILL.md & output script sekarang menegaskan jam = waktu SETEMPAT PENERIMA, bukan waktu pengirim, dengan panduan konversi WITA/WIT.
- **B5:** SKILL.md mempertegas batas cakupan dengan `riset-calon-pelanggan` (riset = cari & saring daftar, pesan pembuka hanya bonus; skill ini = susun & periksa pesan pertama secara mendalam untuk satu prospek). `riset-calon-pelanggan` tidak diubah.
- **B6:** `references/dasar-hukum-wa.md` diperbaiki: UU ITE ditulis "UU 11/2008 jo. UU 19/2016 jo. UU 1/2024"; UU Perlindungan Konsumen diganti ke Pasal 9-10 (bukan 8-9, diverifikasi via web search 2026-09-25); UU PDP dipisah jadi WAJIB menurut pasal (dasar pemrosesan Pasal 20, larangan Pasal 65 & sanksi Pasal 67) vs PRAKTIK BAIK (sebut asal kontak & opsi keluar, terkait hak subjek data Pasal 5-8 dst.).
- **B7-B12 (rendah):** jumlah emoji dihitung & diperingatkan bila >3; pemisah kalimat memecah baris baru (daftar poin tanpa titik); template Varian 3 dirapikan target ≤500 karakter; label "Singkat" diselaraskan jadi "± 2-3 kalimat, ≤300 karakter"; aturan baru — detail layanan yang tidak diberikan pengguna ditandai `[isi: ...]` atau masuk Asumsi, tidak boleh dikarang; Varian 3 kini diarahkan menyebut akibat/masalah bagi penerima (dengan kata sendiri), bukan mendaftar fitur.
- Tes regresi baru ditambahkan di `tests/uji_regresi.py` untuk setiap bug di atas (66 tes total, semua lulus).

### v1.0.0 (2026-09-25) — rilis awal (status `draft`, hasil kurasi ATM dari `cold-email`, lihat bagian atas dokumen ini).
