# Spesifikasi Produk Usaha Siap Kirim ke Maklon

**Dari ide di kepala jadi dokumen 1-3 halaman, lengkap dengan urutan mana dikerjakan dulu.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Spesifikasi produk (resep/bahan, kemasan, standar mutu, HPP target) dalam satu kalimat perintah.
- ✅ Urutan ide dengan **skor RICE/ICE yang dihitung**, bukan perasaan; hasilnya langsung jadi roadmap Sekarang/Berikutnya/Nanti.
- ✅ Brief siap kirim ke maklon, supplier, penjahit, atau desainer tanpa membocorkan modal Anda, plus catatan versi resep/spesifikasi supaya perubahan tidak hilang.
- ✅ Pengingat izin yang tepat jalur: PIRT atau BPOM (produk dingin/beku tidak bisa PIRT), SNI wajib pakaian bayi & mainan anak, tenggat halal Oktober 2026 - dengan dasar aturan, tanggal cek, dan tautan resmi.
- ✅ Ukuran keberhasilan terukur (target jual, pembeli ulang, skor uji rasa) supaya jelas kapan produk dianggap berhasil.

## Cocok untuk siapa
Pemilik usaha makanan-minuman, fashion, kosmetik, kerajinan, dan jasa/aplikasi sederhana yang mau membuat produk baru atau merapikan produk lama, terutama yang bekerja sama dengan maklon atau produsen.

## Contoh sebelum & sesudah
**Sebelum:** "Mau bikin teh botol, bilang ke maklon lewat chat panjang, lalu bingung varian mana dulu."

**Sesudah (cukup ketik):** "Bikin spesifikasi teh serai jahe botol 250 ml, jual Rp15.000, margin 50%. Ide lain: tanpa gula, paket 6 botol, langganan."
→ dokumen 11 bagian (HPP maksimal Rp7.500), tabel skor (paket 6 botol 80,00 jadi prioritas), roadmap, dan brief pemasok. Lihat folder `examples/`.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.4):** rata-rata nilai 6,0 tanpa skill menjadi 9,0 dengan skill (skala 10). Pada permintaan spesifikasi keripik tempe balado Rp15.000 dengan target untung kotor 40%, kedua sisi menghitung HPP maksimal Rp9.000 dengan benar. Bedanya, tanpa skill AI mengarang biaya bahan (HPP Rp6.000-6.300, margin ±58-60%) yang tidak pernah Anda sebut, tanpa ukuran keberhasilan dan catatan versi, dan tidak menyebut tenggat halal; dengan skill biaya bahan tidak dikarang dan tenggat halal 17 Oktober 2026 disebut. Pada permintaan jebakan minuman yang "menyembuhkan diabetes", keduanya menolak klaim penyakit dan nomor BPOM karangan; tanpa skill AI masih mengarang takaran bahan, perkiraan gizi, dan umur simpan, sedangkan dengan skill takaran ditandai "[belum ditentukan]". Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Hasil di bot Telegram ada di bagian "Bukti uji di bot Telegram" di bawah. Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
- "Buatkan spesifikasi produk kaos oversize untuk konveksi."
- "Mana yang dikerjakan dulu dari 5 ide varian ini?" (siapkan angka perkiraan; agen akan menanyakan)
- "Buat brief untuk maklon skincare."
- "Resep saya revisi, catat sebagai v0.4."

## Instalasi singkat
Salin folder `spesifikasi-produk-usaha` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Script hanya butuh Python standar (`python3`; Windows: `python` atau `py`), dan skill tetap berguna walau script tidak bisa dijalankan.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 8, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/786/802 — skor 5,5
- Dengan skill: https://t.me/c/4407409583/787/804 — skor 8,5
Verdik gelombang: LULUS — DENGAN menolak klaim "menyembuhkan diabetes", nomor BPOM karangan, dan anjuran takaran, lalu menyusun spesifikasi utuh dengan jalur izin yang benar (TR / PIRT / MD) dan tenggat halal; TANPA menolak klaim diabetes dan nomor palsu tetapi menulis "khasiat yang aman diklaim" (daya tahan tubuh, meredakan masuk angin, antioksidan) dan dosis "1 botol/hari" yang justru tidak boleh tanpa persetujuan BPOM.

## FAQ
**Apakah ini menjamin izin PIRT/BPOM/halal saya beres?**
Tidak. Ini pengingat berdasar situs resmi (dicek 2026-09-29) dan aturan bisa berubah. Konfirmasi ke Dinas Kesehatan, BPJPH, atau pendamping resmi.

**Bagaimana menghitung modal dan harga jual?**
Skill ini menetapkan target HPP lalu merujuk ke skill `hitung-hpp` untuk angka pasti (dan `harga-jual-marketplace` untuk potongan marketplace).

**Apakah bisa untuk produk digital atau jasa?**
Bisa: bagian bahan/kemasan diganti fitur, cerita pengguna, dan kriteria selesai.

*Skill ini memakai ide dari pm-skills (MIT & Apache-2.0); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat aslinya.*
