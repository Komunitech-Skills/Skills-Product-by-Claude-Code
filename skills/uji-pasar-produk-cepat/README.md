# Uji Pasar Produk Cepat

**Tahu produk barumu laku sebelum produksi besar, dengan angka, bukan feeling.**

## Manfaat
- Tahu asumsi mana yang paling berbahaya dan diuji dulu, tidak semua sekaligus.
- Pilih eksperimen murah yang cocok kanalmu: pre-order WA, sistem PO, sampel di bazar, landing page + WA, listing marketplace uji, konten TikTok, survei Google Form.
- Kriteria lulus ditetapkan SEBELUM uji, jadi tidak ada angka yang digeser setelah hasil keluar.
- Hasil dihitung script (konversi, rentang wajar, perbandingan dua varian), bukan dikira-kira, lengkap dengan peringatan kalau sampel terlalu sedikit.
- Keputusan jelas: LANJUT, UBAH, atau STOP, plus pilihan pivot bila perlu.

## Cocok untuk siapa
- Pemilik UMKM (makanan beku, kue, fesyen, kerajinan, jasa) yang mau meluncurkan varian atau produk baru.
- Yang sudah punya ide dan mau menguji dua pilihan (harga, kemasan, rasa, kalimat iklan).
- Profesional yang mau menguji layanan baru ke kontak sendiri.
- Belum punya ide sama sekali? Mulai dari `brainstorming-ide-usaha`. Ide baru satu kalimat? `validasi-ide-produk-baru` dulu, lalu pakai skill ini.

## Contoh sebelum & sesudah
**Sebelum:** "Aku mau produksi 200 pack dimsum mentai. Kayaknya laku sih."
**Sesudah:** "Kirim penawaran ke 80 kontak, target 15% bayar DP dalam 5 hari." Hasil: 14 dari 80 (17,5%, rentang wajar 10,7%-27,3%) -> LANJUT BERTAHAP: produksi 40 pack dulu, bukan 200, lalu uji pengiriman beku. Modal terlindungi.

## Cara pakai
Cukup tulis dalam bahasa biasa:
- "Aku mau tes varian mentai untuk dimsum beku, mulai dari mana?"
- "Harga 35 ribu vs 45 ribu, dari 60 orang: 9 beli vs 15 beli. Mana yang menang?"
- "Buatkan catatan eksperimen dan langkah berikutnya."

Script (opsional, Python standar): `python3 scripts/hasil_eksperimen.py hasil --ditawari 80 --aksi 14 --target 15` (Windows: `python` atau `py`). Skill tetap berguna walau script tidak bisa dijalankan.

## Instalasi singkat
Salin folder `uji-pasar-produk-cepat` ke folder skills agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap: lihat `docs/instalasi.md` di dalam paket pembelian.

## FAQ
**1. Bedanya dengan Tes Ide Sebelum Modal Habis (`validasi-ide-produk-baru`)?**
Itu untuk mengubah ide jadi hipotesis dan menjalankan satu uji 7 hari pertama. Ini untuk eksekusi lanjutan: beberapa asumsi, membandingkan dua varian, catatan eksperimen, dan keputusan berbasis rentang wajar.

**2. Saya hanya punya sedikit kontak. Masih bisa?**
Bisa, tapi hasilnya "sinyal arah". Skill akan menandai sampel kecil dan menyarankan uji berulang atau kanal tambahan (listing, titip kafe).

**3. Apakah hasilnya pasti akurat?**
Tidak. Ini alat bantu keputusan skala UMKM, bukan penelitian ilmiah. Teman dekat cenderung membuat hasil terlalu optimis, dan angka ambang adalah patokan praktis. Skill ini tidak menggantikan izin usaha (PIRT/BPOM/halal) untuk produk yang memerlukannya.

## Atribusi
Diadaptasi dari kerangka open source (product-on-purpose/pm-skills, Apache-2.0; phuryn/pm-skills, MIT) dan ditulis ulang untuk konteks Indonesia. Tidak berafiliasi dengan pembuat sumber. Lihat `ATTRIBUTION.md`.
