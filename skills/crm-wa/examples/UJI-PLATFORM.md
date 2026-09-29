# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ ("Pakai CRM buat usaha saya ya, nama usahanya Dapur Mama Tia ... Catat: Bu Rina dari IG ..." → scripts/crm.py init/tambah; lalu "Follow-up hari ini siapa saja?" → 3 draf + tautan wa.me; "sudah kukirim ... Pak Anton deal 1,1 juta ... Kak Nia batal ... Rekap CRM bulan ini")
3 Permintaan malas: ✅ ("catet dong ada yg nanya kue lapis td, namanya bu dewi" → langsung dicatat K0004, follow-up hari ini, menyebut WA & sumber belum ada)
4 Script: ✅ rekap: lead 3, deal 1 Rp 1.100.000, batal 1, konversi 33,3%, win rate 50,0%, sumber terbaik Referensi; terkirim → FU +2 hari; tautan wa.me berisi nomor 62… & draf ter-encode benar (dicek manual)
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara (skala lebih kecil dari examples/01 15 prospek; angka & draf sesuai pola contoh)
Masalah: (1) Agent menjalankan `init --ya` langsung setelah pratinjau tanpa menunggu persetujuan pengguna — melanggar aturan SKILL.md no. 4 (perubahan besar: pratinjau → setuju → --ya). Dampak kecil (DB baru), tapi perlu dipertegas. (2) Uji 3: agent menampilkan sintaks perintah (`ubah --kontak K0004 --wa <nomor>`) ke pengguna awam.

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
