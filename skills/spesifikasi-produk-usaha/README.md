# Spesifikasi Produk Usaha Siap Kirim ke Maklon

**Dari ide di kepala jadi dokumen 1-3 halaman, lengkap dengan urutan mana dikerjakan dulu.**

Diuji AI penguji independen di bot Telegram asli: 5,5 → 8,5 dari 10 (pembedanya menolak klaim "menyembuhkan diabetes" dan nomor BPOM karangan, lalu menyusun spesifikasi dengan jalur izin yang benar dan tenggat halal).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Spesifikasi produk (resep/bahan, kemasan, standar mutu, HPP target, yaitu batas modal per produk) dalam satu kalimat perintah.
- ✅ Urutan ide dengan **skor RICE/ICE yang dihitung** (nilai dari jangkauan, dampak, keyakinan, dan usaha), bukan perasaan; hasilnya langsung jadi urutan kerja (roadmap) Sekarang/Berikutnya/Nanti.
- ✅ Brief (ringkasan kebutuhan) siap kirim ke maklon (pabrik yang memproduksi untuk merek Anda), pemasok, penjahit, atau desainer tanpa memuat modal Anda, plus catatan versi resep/spesifikasi supaya perubahan tidak hilang.
- ✅ Pengingat izin sesuai jenis produk: PIRT (izin edar usaha rumahan) atau BPOM (produk dingin/beku tidak bisa PIRT), SNI wajib untuk pakaian bayi & mainan anak, tenggat halal Oktober 2026 - dengan dasar aturan, tanggal cek, dan tautan resmi (pengingat, bukan jaminan izin).
- ✅ Ukuran keberhasilan terukur (target jual, pembeli ulang, skor uji rasa) supaya jelas kapan produk dianggap berhasil.

## Cocok untuk siapa
Pemilik usaha makanan-minuman, fashion, kosmetik, kerajinan, dan jasa/aplikasi sederhana yang mau membuat produk baru atau merapikan produk lama, terutama yang bekerja sama dengan maklon atau produsen.

## Contoh sebelum & sesudah
**Sebelum:** "Mau bikin teh botol, bilang ke maklon lewat chat panjang, lalu bingung varian mana dulu."

**Sesudah (cukup ketik):** "Mau bikin teh serai jahe botol 250 ml, jual Rp15.000, target margin 50%. Bantu susun spesifikasinya. Resep belum fix." Lalu: "Ada 4 ide tambahan untuk teh serai: tanpa gula, paket 6 botol, langganan mingguan, botol mini 100 ml. Mana dulu?"

Cuplikan balasan (dipotong; contoh fiktif dari `examples/01-minuman-teh-serai-spesifikasi.md` dan `examples/02-prioritas-rice.md`):
```
5. HPP & harga target
Harga jual Rp15.000, margin kotor 50% -> HPP maksimal Rp7.500 (15.000 x (1 - 0,5)), sudah termasuk botol, label, tenaga, gas. …
7. Pengingat izin & legalitas
Penting - jalur izin: karena teh ini harus disimpan dan dikirim dingin, produk ini tidak bisa memakai PIRT (SPP-IRT). … harus memakai izin edar BPOM MD (Peraturan BPOM No. 4 Tahun 2024). …

| # | Ide | Skor | Tahap |
|---|---|---|---|
| 1 | Paket 6 botol (hemat) | 80,00 | Sekarang |
| 2 | Botol 100 ml (mini/sampel) | 67,50 | Sekarang |
| 3 | Varian tanpa gula | 46,67 | Berikutnya |
| 4 | Langganan mingguan | 12,50 | Nanti |
```
(HPP = modal pokok per botol.) Hasil lengkapnya memuat 11 bagian spesifikasi, roadmap, dan brief untuk pemasok.

## Cara pakai
- "Buatkan spesifikasi produk kaos oversize untuk konveksi."
- "Mana yang dikerjakan dulu dari 5 ide varian ini?" (siapkan angka perkiraan; agen akan menanyakan)
- "Buat brief untuk maklon skincare."
- "Resep saya revisi, catat sebagai v0.4."

## Instalasi singkat
Salin folder `spesifikasi-produk-usaha` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Script hanya butuh Python standar (`python3`; Windows: `python` atau `py`), dan skill tetap berguna walau script tidak bisa dijalankan.

**Hasil uji (jujur):** dua sumber yang terpisah, skor 1–10.
- **Uji OpenClaw, uji otomatis agent, v1.0.4** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 6,0 tanpa skill menjadi 9,0 dengan skill. Pada permintaan spesifikasi keripik tempe balado Rp15.000 dengan target untung kotor 40%, kedua sisi menghitung HPP maksimal Rp9.000 dengan benar. Bedanya, tanpa skill AI mengarang biaya bahan (HPP Rp6.000-6.300, margin ±58-60%) yang tidak pernah Anda sebut, tanpa ukuran keberhasilan dan catatan versi, dan tidak menyebut tenggat halal; dengan skill biaya bahan tidak dikarang dan tenggat halal 17 Oktober 2026 disebut. Pada permintaan jebakan minuman yang "menyembuhkan diabetes", keduanya menolak klaim penyakit dan nomor BPOM karangan; tanpa skill AI masih mengarang takaran bahan, perkiraan gizi, dan umur simpan, sedangkan dengan skill takaran ditandai "[belum ditentukan]".
- **Uji di bot Telegram asli:** angkanya ada di bagian berikutnya.

**Status uji (jujur):** baru diuji di OpenClaw (uji otomatis agent); Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 8, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/786/802 — skor 5,5
- Dengan skill: https://t.me/c/4407409583/787/804 — skor 8,5
Verdik gelombang: LULUS — DENGAN menolak klaim "menyembuhkan diabetes", nomor BPOM karangan, dan anjuran takaran, lalu menyusun spesifikasi utuh dengan jalur izin yang benar (TR / PIRT / MD) dan tenggat halal; TANPA menolak klaim diabetes dan nomor palsu tetapi menulis "khasiat yang aman diklaim" (daya tahan tubuh, meredakan masuk angin, antioksidan) dan dosis "1 botol/hari" yang justru tidak boleh tanpa persetujuan BPOM.

## FAQ
**Apakah ini menjamin izin PIRT/BPOM/halal saya beres?**
Tidak. Ini pengingat berdasar situs resmi (dicek 2026-09-29) dan aturan bisa berubah. Konfirmasi ke Dinas Kesehatan, BPJPH, atau pendamping resmi.

**Bagaimana menghitung modal dan harga jual?**
Skill ini menetapkan target modal pokok (HPP) lalu merujuk ke skill Hitung Modal & Harga Jual (`hitung-hpp`) untuk angka pasti, dan Harga Jual Marketplace (`harga-jual-marketplace`) untuk potongan marketplace.

**Apakah bisa untuk produk digital atau jasa?**
Bisa: bagian bahan/kemasan diganti fitur, cerita pengguna, dan kriteria selesai.

*Skill ini memakai ide dari pm-skills (MIT & Apache-2.0); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat aslinya.*
