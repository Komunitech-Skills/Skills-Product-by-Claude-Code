# Uji Banding Pesaing

Skenario dibandingkan: "Buatkan landing page untuk keripik pedas saya, harga 25 ribu." Pesaing **dibaca untuk dinilai saja**, tidak disalin.

## Pesaing 1 — Skill sumber ATM: `coreyhaines31/marketingskills` (skills `copywriting`, `cro`, `offers`, MIT)
Dibaca langsung dari repo (clone lokal, commit terbaru per 2026-09-24).
- **Bahasa:** Inggris, generik global (SaaS-oriented: contoh "Start Free Trial", "Slack lets you share files").
- **Struktur:** kerangka halaman mirip (hero → social proof → problem → solution → how it works → objection handling → final CTA) — ini yang memang diadaptasi (lihat `ATTRIBUTION.md`).
- **Tidak ada:** Bahasa Indonesia, CTA WhatsApp/wa.me, harga Rupiah, konteks UMKM, aturan hukum Indonesia (BPOM/halal/UU 8/1999), mekanisme anti-karang bukti sosial yang eksplisit (hanya prinsip umum "Honest over sensational... fabricated testimonials erode trust"), script pembantu, atau contoh kasus lokal.
- **Skor kasar untuk kebutuhan UMKM Indonesia:** kerangka 8/10 (matang, teruji di banyak produk), tapi 0/10 untuk siap pakai pembeli awam Indonesia (perlu ditulis ulang total).

## Pesaing 2 — `copyku` (clawskills.sh, OpenClaw skill Indonesia)
Dibaca lewat halaman produk (SKILL.md aslinya tidak diunduh — cukup untuk menilai cakupan, bukan menyalin isi).
- **Kelebihan:** Bahasa Indonesia asli, memilih formula (PAS untuk landing page, SSC untuk sales page) otomatis berdasarkan platform.
- **Tidak ditemukan dari deskripsi publik:** penanganan testimoni/bukti sosial yang eksplisit anti-karang, pembuatan tautan WhatsApp (wa.me) dengan encoding, ceklis kepatuhan hukum Indonesia (BPOM/halal/UU 8-1999), meta title/description dengan panjang dihitung, atau versi pendek link-in-bio.
- **Catatan:** tidak bisa dinilai skor pasti karena SKILL.md lengkapnya tidak dibaca (di luar cakupan uji ini untuk mengunduh/menjalankan skill pihak ketiga); dinilai dari deskripsi publik saja.

## Pesaing 3 — `rampstackco/claude-skills`, skill `landing-page-copy`
Dibaca langsung dari GitHub.
- **Kelebihan:** struktur 7 bagian rapi dengan catatan visual & variasi uji per bagian; prinsip bukti sosial spesifik-terukur bagus ("Kami kurangi onboarding dari 2 minggu jadi 4 hari" vs generik); tegas soal tidak boleh mengarang data ("jika metrik hilang, cantumkan kesenjangan, jangan estimasi").
- **Tidak ada:** Bahasa Indonesia, CTA WhatsApp, Rupiah, konteks UMKM Indonesia, aturan hukum lokal, script pembantu. Konteksnya B2B SaaS (istilah "trial", "onboarding") — tidak relevan untuk warung/UMKM.

## Pesaing 4 — `RamaAditya49/rama-copywriting` (sudah pernah ditinjau tim, (riset internal kurator, tidak disertakan dalam paket), Apache-2.0)
Bukan skill landing page khusus, tapi copywriting umum ID/EN dengan "claim ledger" (Verified/Attributed/Qualified/Unverified) — kerangka kejujuran klaim yang **lebih formal** dari `copy-landing-page` (yang memakai pendekatan lebih sederhana: tulis/jangan tulis + placeholder).
- **Kelebihan pesaing ini:** claim ledger eksplisit memaksa setiap klaim dikategorikan sebelum ditulis — lebih sistematis untuk klaim non-hukum (mis. "produk kami lebih cepat") yang `copy-landing-page` tidak punya mekanisme setara (skill kita baru menyaring klaim yang eksplisit disebut di daftar `dasar-hukum-klaim.md`, belum mekanisme umum untuk SEMUA jenis klaim tak berbukti di luar daftar itu).
- **Kekurangan pesaing ini untuk kasus ini:** Bahasa Inggris/generik, tidak spesifik landing page (fokus copywriting umum), tidak ada CTA WhatsApp/wa.me, tidak ada aturan BPOM/halal Indonesia, referensinya panjang untuk pembeli awam.

## Kesimpulan
Tidak ada pesaing yang setara secara langsung (landing page + Bahasa Indonesia + CTA WhatsApp + kepatuhan hukum Indonesia + script wa.me/meta teruji) dalam satu paket. `copy-landing-page` menang telak untuk kebutuhan spesifik UMKM Indonesia dibanding keempatnya. Satu kelebihan pesaing 4 (claim ledger sistematis) layak dicatat sebagai **usulan perbaikan versi berikutnya**: skill saat ini menyaring klaim berisiko yang **terdaftar** di `dasar-hukum-klaim.md` dengan baik, tapi belum punya mekanisme umum untuk klaim tak berbukti *di luar* daftar itu (mis. "lebih murah dari kompetitor", "kualitas terbaik" tanpa data spesifik) — ini dicatat sebagai temuan di `HASIL-UJI.md`, bukan alasan gagal uji banding (skill kita tetap unggul untuk cakupannya sendiri).
