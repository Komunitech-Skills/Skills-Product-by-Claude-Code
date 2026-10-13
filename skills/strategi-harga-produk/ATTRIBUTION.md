# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi kerangka strategi harga dari dua skill publik berlisensi MIT, lalu ditulis ulang total untuk UMKM Indonesia (produk fisik, F&B, fesyen, jasa) dengan script hitung Rupiah yang teruji.

## Sumber yang diadaptasi
1. **coreyhaines31/marketingskills** — https://github.com/coreyhaines31/marketingskills
   - Pembuat: Corey Haines. Lisensi: MIT, Copyright (c) 2025 Corey Haines (teks lengkap: `LICENSE-MIT-marketingskills`).
   - Snapshot: `git clone --depth 1` pada 2026-09-29, commit `5b2c0007766c6a1cf1d53fd8fc73e979e0821022`.
   - Dipelajari: `skills/pricing/SKILL.md` (v2.1.1) dan `references/pricing-models.md`, `references/tier-structure.md`, `references/research-methods.md`.
2. **phuryn/pm-skills** — https://github.com/phuryn/pm-skills
   - Pembuat: Pawel Huryn. Lisensi: MIT, Copyright (c) 2026 Pawel Huryn (teks lengkap: `LICENSE-MIT-pm-skills`).
   - Snapshot: `git clone --depth 1` pada 2026-09-29, commit `8607e3b077817f89bf4a9b623246219734ac3be0`.
   - Dipelajari: `pm-product-strategy/skills/pricing-strategy/SKILL.md` dan `pm-product-strategy/commands/pricing.md`.

## Bagian yang diambil (lalu ditulis ulang dalam Bahasa Indonesia & konteks UMKM)
- Prinsip "harga di antara alternatif terdekat dan nilai yang dirasakan pembeli; biaya hanya lantai" (keduanya).
- Kerangka good-better-best, jangkar (anchoring), pilihan umpan (decoy), harga "charm" vs bulat (marketingskills).
- Urutan kenaikan harga bertahap: uji ke pelanggan baru dulu, umumkan jauh hari dengan alasan, beri opsi lunak (marketingskills "Rollout Methodology").
- Peringatan harga terlalu murah menarik pembeli paling mudah pindah (marketingskills "Low-Price Retention").
- Empat pertanyaan kepekaan harga (Van Westendorp), disederhanakan untuk survei kecil (keduanya).
- Pola keluaran "rekomendasi + asumsi yang perlu diuji + risiko" (phuryn).

## Bagian yang TIDAK dipakai
Metrik nilai SaaS (per seat/usage/credit/outcome), freemium vs free trial, harga enterprise, audit halaman harga & kesiapan dibaca AI (pricing-page-teardown), MaxDiff, proyeksi ARR, contoh harga dolar dan aturan "$10/$100/$1.000" — tidak relevan untuk UMKM Indonesia yang menjual produk fisik/jasa.

## Audit lisensi & keamanan (Tahap 2–3 CLAUDE.md)
- File `LICENSE` di root kedua repo dibaca langsung: MIT, mengizinkan modifikasi & penjualan turunan dengan menyertakan pemberitahuan hak cipta + teks lisensi (disertakan di folder ini).
- Sinyal bukti (dari catatan riset internal kurator (tidak disertakan dalam paket)): marketingskills ±51,9 rb bintang / 7,8 rb fork, 473 commit, masih aktif, sudah dipakai untuk 3 skill kita; pm-skills ±26,7 rb bintang / 2,8 rb fork, rilis v2.0–v2.1, ada PR kontributor luar. Keduanya lolos ≥ 3 sinyal.
- Folder sumber yang dipakai tidak berisi script (hanya `.md` dan `evals/evals.json` yang tidak dijalankan). Tidak ada kode sumber yang dijalankan.
- Semua file sumber yang dipakai dibaca penuh, plus pencarian pola `curl`, `wget`, `eval(`, `base64`, `rm -rf`, `sudo`, "ignore the user/previous", `api_key`, `token`, `ssh`, `.env`, `exec(`, `subprocess`: **tidak ada kecocokan**. Tidak ada instruksi tersembunyi, pengiriman data ke luar, permintaan kredensial, atau data pribadi tertanam. Satu-satunya instruksi luar di sumber adalah membaca file konteks lokal `.agents/product-marketing.md` (tidak diadaptasi).
- Kesimpulan: **lolos audit**.

## Nilai tambah Komunitech (tidak ada di sumber)
1. Seluruhnya Bahasa Indonesia awam, contoh toko roti/kue rumahan dan hampers Lebaran (fiktif).
2. Script `scripts/strategi_harga.py` (Python standar, Decimal) + `tests/uji_regresi.py` dengan angka yang diverifikasi manual: margin vs markup, BEP & batas aman, tangga harga eceran/reseller/grosir/agen dengan margin minimum, dampak diskon/potongan/beli-X-gratis-Y (volume tambahan agar laba tetap), cek paket/hampers, simulasi elastisitas berlabel ESTIMASI + volume impas yang pasti, kandidat harga cantik (x.900, x9.900, x9.000, bulat, kelipatan 500), dan PPN untuk PKP sesuai standar pembulatan library. Sumber tidak menyertakan hitungan apa pun.
3. Strategi yang relevan untuk UMKM: cost-plus, berbasis pesaing (terhubung ke riset-harga-kompetitor), penetrasi terbatas waktu, skimming, tangga reseller dengan harga eceran anjuran, harga per kanal (offline, marketplace, ojol, QRIS).
4. Aturan promo yang menjaga margin + tabel cepat diskon vs margin, kalender promo lokal, larangan harga coret palsu (UU 8/1999) dan kartel harga (UU 5/1999).
5. Integrasi dengan skill katalog: hitung-hpp (HPP), harga-jual-marketplace (potongan), riset-harga-kompetitor (harga pasar), hitung-ppn, promo-kalender.
6. Penanganan input awam: format angka Indonesia (28.000, 28rb, 1,2jt), tanya sekali, default yang disebutkan asumsinya, pesan GAGAL yang ramah.
7. README pembeli dan contoh kasus lokal.

## Pembagian lisensi
- `references/pilihan-strategi.md` (bagian kerangka nilai/pesaing/biaya, kenaikan harga, 4 pertanyaan harga) dan `references/psikologi-dan-paket.md` (bagian good-better-best, jangkar, umpan): turunan dari materi MIT kedua sumber — tunduk pada ketentuan MIT (lihat `LICENSE-MIT-*`).
- Semua bagian lain — `SKILL.md`, `README.md`, `references/aturan-promo.md`, `references/rumus.md`, `scripts/`, `tests/`, `examples/` — karya orisinal Komunitech tanpa materi pihak ketiga.

Nama marketplace/aplikasi (Shopee, Tokopedia, TikTok Shop, GoFood, GrabFood) hanya penyebut kanal; Komunitech tidak berafiliasi. Nama toko di `examples/` fiktif.

Penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian, ditambah ketentuan MIT pada bagian yang disebut di atas.
