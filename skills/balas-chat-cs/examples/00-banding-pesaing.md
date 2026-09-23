# 00 — Uji banding pesaing (S1)

## Pencarian
- Kata kunci: "WhatsApp reply", "customer service reply SKILL.md", "balas chat", "Bahasa Indonesia customer service", "complaint handling skill".
- Sumber dicek: github.com/manairalabs/bicara-skills, github.com/alvinindra/bahasa-skills, github.com/anthropics/skills, github.com/VoltAgent/awesome-openclaw-skills (pine-assistant dll. berupa layanan API; ClawHub/clawskills.sh **diblokir proxy**), pencarian web GitHub.
- Temuan paling sebanding: **`wa-reply-id`** — github.com/manairalabs/bicara-skills (skills/wa-reply-id/SKILL.md + examples/scenarios.md), lisensi **MIT**, v0.1.0. Pesaing langsung: skill balas WA CS berbahasa Indonesia.
- Script pihak ketiga tidak dijalankan; isi tidak disalin.

## Input S1 (sama)
> Balesin chat ini dong: "kak paketku udah 5 hari blm sampe, katanya 2-3 hari. gmn sih?? mau buat oleh2 lusa". Tokoku Kopi Lereng Fiktif, jual kopi bubuk, kirim pakai JNE REG, resinya JP0000FIKTIF01, status terakhir kemarin sore di gudang transit Surabaya. Tujuannya Sidoarjo.

## Output dengan instruksi pesaing (`wa-reply-id`, disimulasikan)
Instruksi pesaing: pilih register (default Formal-Friendly; pelanggan pakai "gmn sih" → bisa Casual-Warm), pola "Order status: jawaban dulu, lalu konteks", jangan menjanjikan yang tidak pasti (boleh "biasanya 1–2 hari"), output 1 draf tanpa pengantar/penjelasan.
```
Halo Kak, mohon maaf atas keterlambatannya 🙏
Pesanan Kakak dengan resi JNE JP0000FIKTIF01 statusnya sudah di gudang transit Surabaya sejak kemarin sore, jadi sudah dekat dengan Sidoarjo. Biasanya dari transit ke alamat tujuan butuh 1–2 hari.
Kami paham kurang nyaman apalagi untuk oleh-oleh lusa. Saya akan pantau pengirimannya dan kabari Kakak setelah ada update ya.
Salam, Tim Kopi Lereng Fiktif
```
(Catatan: contoh resmi pesaing untuk kasus serupa bahkan menulis "Perkiraan sampai besok siang" dan memberi kompensasi gratis ongkir tanpa izin pemilik — bertentangan dengan aturannya sendiri.)

## Output dengan skill kita
Lihat `01-paket-telat-wa.md` (balasan + versi singkat + catatan admin).

## Penilaian

| Kriteria | Pesaing (`wa-reply-id`) | Skill kita |
|---|---|---|
| Kualitas balasan | Baik, natural, ringkas | Baik; empati lebih spesifik; janji tindak lanjut berjam |
| Konteks Indonesia | Sangat baik (register Kak/Bapak/Ibu, katalog frasa) | Sangat baik + aturan marketplace (Shopee/Tokopedia/TikTok Shop), UU Perlindungan Konsumen, UU PDP |
| Akurasi / tidak salah janji | "Biasanya 1–2 hari" masih semi-janji; contohnya sendiri mengarang estimasi & kompensasi | Tidak ada estimasi karangan; kompensasi hanya "usulan — konfirmasi pemilik" |
| Siap pakai | Draf saja, tanpa panduan tindakan | Draf + versi singkat + catatan admin (hubungi JNE, rencana H-1, status "terkirim") |
| Cakupan | 7 pola chat, tanpa bank jawaban, tanpa kasus kesehatan/kasar/ancaman ulasan | + mode bank jawaban 15–30 template, kasus kesehatan, pelanggan kasar, ancaman ulasan |
| **Total** | Kompetitif, tapi kalah | **Menang (selisih sedang)** |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Deteksi register dari gaya tulisan pelanggan** (kata "dong/sih/btw" → santai) — bisa ditambahkan ke `references/nada-brand.md`.
2. **Katalog frasa kaku vs natural** (mis. terjemahan mesin yang harus dihindari) — memperkuat kualitas bahasa.
3. Aturan **"jangan minta pelanggan mengulang info yang sudah ia berikan"** dan **"satu pertanyaan klarifikasi, bukan tiga"** untuk chat yang tidak jelas — layak jadi butir checklist.
4. Opsi **2–3 draf berlabel register** bila pengguna minta alternatif.
