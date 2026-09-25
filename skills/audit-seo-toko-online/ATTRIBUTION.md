# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi kerangka & prioritas audit yang terbukti dari skill publik berlisensi MIT, dengan nilai tambah besar untuk pemilik toko online/UMKM Indonesia yang awam teknologi (lihat "Apa yang diubah/ditambahkan" di bawah).

## Sumber yang diadaptasi
- **Repo:** [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
- **Pembuat:** Corey Haines
- **Lisensi:** MIT (dicek langsung di file `LICENSE` repo sumber — lihat `LICENSE-MIT` di folder ini untuk teks lengkapnya; satu lisensi berlaku untuk seluruh repo)
- **Commit/snapshot yang dipakai:** hasil `git clone --depth 1` pada 2026-09-25 (branch default saat itu; commit sha tidak dicatat karena depth 1 tidak menyertakan riwayat penuh)
- **Bagian yang dipelajari:** `skills/seo-audit/SKILL.md` (kerangka & prioritas audit teknis-onpage-konten, ambang aman title/meta description, catatan keterbatasan deteksi schema lewat `web_fetch`/`curl`, format laporan Issue/Impact/Evidence/Fix/Priority), sekilas `skills/schema/SKILL.md` (daftar field wajib/disarankan per tipe schema.org) dan `skills/programmatic-seo/SKILL.md` (dibaca untuk menilai relevansi cakupan — di luar cakupan audit satu halaman, tidak diadaptasi).
- **Bagian yang TIDAK dipakai:** `ai-seo` (AI Overviews/GEO — di luar cakupan audit dasar toko online), `programmatic-seo` (pembuatan halaman skala besar — beda fungsi dari audit), bagian "International SEO/hreflang" di `seo-audit` (tidak relevan untuk mayoritas toko online UMKM satu bahasa).

## Audit lisensi & keamanan (Tahap 2–3 CLAUDE.md)
- File `LICENSE` di root repo sumber dicek langsung: MIT, Copyright (c) 2025 Corey Haines — mengizinkan modifikasi & penjualan turunan.
- Tidak ada file `LICENSE` terpisah per-skill di `skills/*/` — seluruh repo tunduk pada satu `LICENSE` MIT di root.
- Skill `seo-audit`, `schema`, dan `programmatic-seo` tidak memiliki folder `scripts/` — hanya berisi `SKILL.md`, `references/*.md`, dan `evals/evals.json` (kasus uji, tidak dijalankan). Tidak ada kode dari sumber ini yang dijalankan.
- Isi `SKILL.md` ketiganya dibaca penuh, plus pencarian pola mencurigakan (`curl`, `wget`, `eval(`, `base64`, `rm -rf`, `sudo`, "ignore the user", `api_key`, `token`, `ssh`, `.env`, `exec(`, `subprocess`) di seluruh folder `skills/seo-audit/`. Satu-satunya kecocokan "curl" adalah dua kalimat penjelasan keterbatasan ("`web_fetch` dan `curl` tidak bisa mendeteksi skema JS yang disisipkan JavaScript") — bukan instruksi eksekusi, dan justru diadaptasi jadi peringatan yang sama di skill ini.
- Tidak ditemukan perintah destruktif, pengiriman data ke server luar, permintaan kredensial/SSH key/data browser, kode ter-obfuscate, atau instruksi tersembunyi yang menyuruh agent mengabaikan pengguna/menonaktifkan konfirmasi/mengirim file.
- Tidak ditemukan API key, token, atau data pribadi tertanam.
- Kesimpulan: **lolos audit**, aman diadaptasi.

## Apa yang diubah/ditambahkan (nilai tambah ATM)
Sumber berbahasa Inggris dan ditulis untuk konsultan/agency SEO profesional yang mengaudit situs SaaS/e-commerce besar dengan akses Search Console, Screaming Frog, dan tools berbayar. Skill ini ditulis ulang total untuk pemilik toko online/UMKM Indonesia yang awam teknologi dan **tanpa akun/API/tools berbayar apa pun**:

1. **100% Bahasa Indonesia awam**, setiap istilah teknis (meta description, canonical, schema, dst.) dijelaskan dalam satu kalimat sederhana — lihat `references/istilah-seo.md` (tidak ada di sumber, yang menulis untuk audiens yang sudah paham jargon SEO).
2. **Script Python teruji `scripts/cek_halaman.py`** yang membaca file HTML lokal (tanpa akses internet) dan **menghitung** panjang title/meta description, jumlah H1, lompatan level heading, gambar tanpa alt, format tautan bermasalah, canonical, meta robots, Open Graph, dan **validasi JSON-LD** (termasuk pengecekan field spesifik `LocalBusiness`/`Product`) — sumber sama sekali tidak menyertakan script apa pun untuk skill `seo-audit` (hanya instruksi + daftar tools eksternal berbayar seperti Screaming Frog/Ahrefs/Semrush).
3. **Konteks lokal Indonesia menyeluruh**: kata kunci berbahasa Indonesia + variasi lokal (mis. "servis AC Bekasi", bukan generic keyword research), Google Business Profile/Maps dengan konsistensi NAP (Nama-Alamat-Telepon), cara meminta ulasan Google yang sah (bukan beli ulasan), schema `LocalBusiness` dengan format alamat Indonesia (`references/skema-localbusiness.md`) — sumber aslinya hanya menyebut "Local Business" secara umum (NAP, GBP, local schema) tanpa contoh format Indonesia sama sekali.
4. **Kecepatan di HP dengan jaringan seluler** (`references/kecepatan-mobile.md`) ditulis sebagai ceklis manual untuk pemilik toko yang tidak punya akses PageSpeed Insights/Search Console berbayar — sumber mengasumsikan pembaca punya akses Core Web Vitals report dari Search Console.
5. **Larangan tegas teknik terlarang** (keyword stuffing, beli backlink, ulasan/rating palsu, cloaking) dan **tanpa janji peringkat #1** dengan bahasa eksplisit — sumber menyebut prinsip serupa secara implisit (E-E-A-T, hindari thin content) tapi tidak melarang taktik ini secara eksplisit dan gamblang untuk audiens awam.
6. **Larangan mengarang angka volume pencarian** — sumber tidak membahas isu ini sama sekali (mengasumsikan pembaca punya akses tool riset kata kunci berbayar).
7. **Daftar perbaikan diurutkan dampak × kemudahan** dengan teks perbaikan **siap tempel** (title, meta description, H1, alt gambar, contoh JSON-LD terisi) — sumber memberi format laporan (Issue/Impact/Evidence/Fix/Priority) yang diadaptasi strukturnya, tapi tidak pernah menuliskan teks pengganti siap pakai, hanya rekomendasi umum.
8. **Batasan tegas dengan skill lain di katalog kita** (`listing-marketplace`, `copy-landing-page`, `caption-sosmed-umkm`) — tidak relevan untuk sumber yang berdiri sendiri sebagai satu skill generik.
9. **Contoh kasus lokal & dokumentasi pembeli** (`README.md`, `examples/`) — tidak ada di repo sumber (repo sumber adalah instruksi untuk agent coding, bukan produk untuk dijual ke pembeli awam).

## Pembagian lisensi bagian ini
- **Kerangka prioritas audit (Crawlability → Technical → On-Page → Content) dan ambang aman title/meta description** yang dipelajari dari `seo-audit`, ditulis ulang penuh dalam `references/checklist-teknis.md`: turunan dari materi MIT `coreyhaines31/marketingskills` — tunduk pada ketentuan MIT (lihat `LICENSE-MIT`).
- **Semua bagian lain** — `SKILL.md`, `references/istilah-seo.md`, `references/skema-localbusiness.md`, `references/lokal-dan-gmb.md`, `references/kecepatan-mobile.md`, `templates/`, `scripts/`, `examples/`, dan `README.md` — adalah karya orisinal Komunitech, tidak mengandung materi pihak ketiga, dan boleh diperlakukan sebagai proprietary Komunitech.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, ditambah ketentuan MIT pada bagian yang disebut di atas.
