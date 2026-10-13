# Uji Pasar Produk Cepat

**Tahu produk baru Anda laku sebelum produksi besar, dengan angka, bukan feeling.**

Diuji AI penguji independen di bot Telegram asli: 7 → 8,5 dari 10 (pembedanya minat lisan 41,7% dipisahkan dari konversi nyata 0 dari 12, lengkap dengan rentang wajar 0–24% dan keputusan tegas; tanpa skill, saran praktisnya sudah benar tetapi tanpa angka).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Tahu asumsi mana yang paling berbahaya dan diuji dulu, tidak semua sekaligus.
- Pilih eksperimen murah yang cocok kanal Anda: pre-order (pesan dulu, bayar DP) lewat WA, sistem PO (pesanan terjadwal), sampel di bazar, landing page (halaman web satu halaman) + WA, listing marketplace uji, konten TikTok, survei Google Form.
- Kriteria lulus ditetapkan SEBELUM uji, supaya angka tidak digeser setelah hasil keluar.
- Hasil dihitung script (konversi, yaitu berapa persen yang benar-benar membayar; rentang wajar, yaitu kisaran angka yang masuk akal; dan perbandingan dua varian), bukan dikira-kira, lengkap dengan peringatan kalau sampel terlalu sedikit.
- Keputusan jelas: LANJUT, UBAH, atau STOP, plus pilihan pivot (ganti arah produk) bila perlu.

## Cocok untuk siapa
- Pemilik UMKM (makanan beku, kue, fesyen, kerajinan, jasa) yang mau meluncurkan varian atau produk baru.
- Yang sudah punya ide dan mau menguji dua pilihan (harga, kemasan, rasa, kalimat iklan).
- Profesional yang mau menguji layanan baru ke kontak sendiri.
- Ide baru satu kalimat? Pakai skill Tes Ide Sebelum Modal Habis (`validasi-ide-produk-baru`) dulu, lalu pakai skill ini.

## Contoh sebelum & sesudah
**Sebelum:** "Lima dari 12 orang di grup WA bilang mau. Berarti 42% laku, langsung produksi 400 box, modal 15 juta."

**Sesudah (cukup ketik):** "Kak, aku tawarin brownies kukus varian matcha ke 12 orang di grup WA, 5 bilang mau pre-order (blm ada yg transfer sih, baru bilang 'mau'). Berarti konversi 42% dong ya, bagus banget kan? Aku mau langsung beli bahan buat 400 box, modal 15 juta. Bener kan?"

Cuplikan balasan (dipotong; dari `examples/00-openclaw-sebelum-sesudah.md`):
```
Belum, Kak. Itu masih terlalu dini buat keluar modal 15 juta. …
Yang kamu punya sekarang:
- 12 orang ditawari, 5 bilang "mau" → itu minat lisan 42%, bukan konversi
- Yang transfer/DP beneran: 0 dari 12 → konversi nyata = 0%
- Rentang wajar sebenarnya: antara 0% - 24% (lebar banget karena sampelnya cuma 12 orang, jauh di bawah minimal 30)

Keputusan: ULANGI UJI, jangan beli bahan dulu. …
1. Balik ke 5 orang yang bilang "mau" → minta DP kecil (misal Rp10-20rb) dengan tenggat jelas, bukan cuma "nanti ya"
2. Perluas tawaran ke minimal 30 orang (campur: bukan cuma keluarga/teman deket, biar nggak terlalu optimis)
```

## Cara pakai
Cukup tulis dalam bahasa biasa:
- "Aku mau tes varian mentai untuk dimsum beku, mulai dari mana?"
- "Harga 35 ribu vs 45 ribu, dari 60 orang: 9 beli vs 15 beli. Mana yang menang?"
- "Buatkan catatan eksperimen dan langkah berikutnya."

Angka konversi dan rentang wajar dihitung oleh skrip bawaan (cara menjalankannya sendiri ada di bagian Instalasi).

## Instalasi singkat
Salin folder `uji-pasar-produk-cepat` ke folder skills agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

Skrip hitung (opsional, Python standar): `python3 scripts/hasil_eksperimen.py hasil --ditawari 80 --aksi 14 --target 15` (Windows: `python` atau `py`). Skill tetap berguna walau skrip tidak bisa dijalankan.

**Hasil uji (angka nyata):** dua sumber yang terpisah, skor 1–10.
- **Uji OpenClaw, uji otomatis agent, v1.0.4** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 6,0 tanpa skill menjadi 9,0 dengan skill. Pada kasus brownies matcha yang ditawarkan ke 12 orang (5 bilang mau, 0 transfer), skill memisahkan minat lisan 41,7% dari konversi nyata 0/12 = 0% (rentang wajar 95%: 0%-24%), memutuskan tegas ULANGI UJI, meminta DP kecil Rp10-20 ribu, dan menambah sampel minimal 30 sebelum modal Rp15 juta keluar. Catatan jujur: tanpa skill, logikanya sudah sehat (minat bukan pembelian, sampel kecil), tetapi tanpa angka rentang, tanpa keputusan tegas, dan ada satu perbandingan yang salah hitung.
- **Uji di bot Telegram asli:** angkanya ada di bagian berikutnya.

**Status uji (jujur):** baru diuji di OpenClaw (uji otomatis agent); Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 7, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/734/748 — skor 7
- Dengan skill: https://t.me/c/4407409583/735/751 — skor 8,5
Verdik gelombang: LULUS — DENGAN memisahkan minat lisan 41,7% dari konversi nyata 0/12 dengan rentang Wilson 0–24%, lalu memberi keputusan tegas plus langkah DP berbatas waktu yang bisa di-refund dan target 30 kontak baru; TANPA memberi saran praktis yang benar (minta DP, batch kecil) tetapi tanpa angka konversi atau rentang ketidakpastian.

## FAQ
**1. Bedanya dengan Tes Ide Sebelum Modal Habis (`validasi-ide-produk-baru`)?**
Itu untuk mengubah ide jadi hipotesis dan menjalankan satu uji 7 hari pertama. Ini untuk eksekusi lanjutan: beberapa asumsi, membandingkan dua varian, catatan eksperimen, dan keputusan berbasis rentang wajar.

**2. Saya hanya punya sedikit kontak. Masih bisa?**
Bisa, tapi hasilnya "sinyal arah". Skill akan menandai sampel kecil dan menyarankan uji berulang atau kanal tambahan (listing, titip kafe).

**3. Apakah hasilnya pasti akurat?**
Tidak. Ini alat bantu keputusan skala UMKM, bukan penelitian ilmiah. Teman dekat cenderung membuat hasil terlalu optimis, dan angka ambang adalah patokan praktis. Skill ini tidak menggantikan izin usaha (PIRT/BPOM/halal) untuk produk yang memerlukannya.

## Atribusi
Diadaptasi dari kerangka open source (product-on-purpose/pm-skills, Apache-2.0; phuryn/pm-skills, MIT) dan ditulis ulang untuk konteks Indonesia. Tidak berafiliasi dengan pembuat sumber. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
