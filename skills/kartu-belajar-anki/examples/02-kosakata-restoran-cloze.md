# Skenario 2: kosakata restoran, Basic + Cloze

**Input:** `data/pesan-2-kosakata-restoran.txt`.

## Output SESUDAH (skill aktif, kartu-belajar-anki 1.0.1)

> **Ringkasan:** 21 kartu total — 16 kartu Basic (kosakata & frasa restoran) + 5 kartu Cloze (isi bagian kosong, dari kalimat-kalimat yang kamu kasih). Tag: `inggris-restoran`, `inggris-restoran-frasa`. Asumsi: "bill" dan "check" digabung jadi satu kartu (keduanya berarti tagihan, check = gaya Amerika).
>
> **Pratinjau (contoh):**
>
> | Depan | Belakang |
> |---|---|
> | Bahasa Inggrisnya: daftar makanan? | Menu |
> | Bahasa Inggrisnya: "Sudah siap memesan?" | Are you ready to order? |
> | Are you ready to {{c1::order}}? | Tanya ke pelanggan: sudah siap memesan? |
> | Please wait a {{c1::moment}} | Minta pelanggan menunggu sebentar |
>
> **Rencana belajar:** 15 kartu baru/hari, 20 menit/hari → selesai kartu baru dalam **2 hari**. Hari 1: 15 kartu baru. Hari 2: 6 kartu baru sisa + mulai review kartu hari 1 (±5-10 menit). Setelah itu Anki otomatis mengatur jadwal review (spaced repetition) — tinggal buka app tiap hari dan jawab kartu yang muncul.
>
> **Blok 1 — Basic (kosakata & frasa):**
> ```
> #separator:tab
> #notetype:Basic
> Bahasa Inggrisnya: daftar makanan (yang dipegang pelanggan)?	Menu	inggris-restoran
> Bahasa Inggrisnya: tagihan yang diminta pelanggan di akhir makan?	Bill / Check (Check = gaya Amerika)	inggris-restoran
> Bahasa Inggrisnya: alergi (reaksi terhadap makanan tertentu)?	Allergy	inggris-restoran
> Bahasa Inggrisnya: pedas (rasa makanan)?	Spicy	inggris-restoran
> Bahasa Inggrisnya: dibakar (cara masak, mis. ikan bakar)?	Grilled	inggris-restoran
> Bahasa Inggrisnya: digoreng (cara masak)?	Fried	inggris-restoran
> Bahasa Inggrisnya: dikukus (cara masak)?	Steamed	inggris-restoran
> Bahasa Inggrisnya: "Sudah siap memesan?"	Are you ready to order?	inggris-restoran-frasa
> Bahasa Inggrisnya: "Mau minum apa?"	Would you like something to drink?	inggris-restoran-frasa
> Bahasa Inggrisnya: "Mohon tunggu sebentar"	Please wait a moment	inggris-restoran-frasa
> Bahasa Inggrisnya: "Selamat menikmati"	Enjoy your meal	inggris-restoran-frasa
> Bahasa Inggrisnya: "Apakah Anda punya alergi makanan?"	Do you have any food allergies?	inggris-restoran-frasa
> Bahasa Inggrisnya: uang tip / uang terima kasih untuk pelayan?	Tip	inggris-restoran
> Bahasa Inggrisnya: reservasi (pesan meja lebih dulu)?	Reservation	inggris-restoran
> Bahasa Inggrisnya: bawa pulang (makanan tidak dimakan di tempat)?	Takeaway	inggris-restoran
> Bahasa Inggrisnya: tambah isi ulang minuman?	Refill	inggris-restoran
> ```
>
> **Blok 2 — Cloze (isi bagian kosong, dari 5 kalimat yang paling sering dipakai):**
> ```
> #separator:tab
> #notetype:Cloze
> Are you ready to {{c1::order}}?	Tanya ke pelanggan: sudah siap memesan?
> Would you like something to {{c1::drink}}?	Tawarkan minuman ke pelanggan
> Please wait a {{c1::moment}}	Minta pelanggan menunggu sebentar
> Enjoy your {{c1::meal}}	Ucapan sebelum pelanggan mulai makan
> Do you have any food {{c1::allergies}}?	Tanya alergi makanan sebelum memesan
> ```
>
> **Cara impor ke Anki:**
> 1. Buka Anki → **File → Import**.
> 2. Pilih file dari blok di atas (simpan masing-masing sebagai `.txt` atau `.tsv`, satu per blok).
> 3. Pastikan pemisah **Tab**.
> 4. Untuk blok Basic: pilih tipe catatan **Basic**, kolom 1 = Front, kolom 2 = Back, kolom 3 = Tags.
> 5. Untuk blok Cloze: ganti tipe catatan jadi **Cloze** sebelum impor (Anki akan deteksi `{{c1::...}}` otomatis).
>
> **Pertanyaan:**
> 1. Mau ditambah kosakata lain, misal nama-nama seafood (udang, kepiting, cumi, dll.) atau frasa soal pembayaran (cash/card/split bill)?
> 2. 15 kartu baru/hari sudah pas, atau mau lebih santai (misal 10/hari jadi 3 hari)?

## Catatan penguji

- Basic (16) dan Cloze (5) di dua blok terpisah, masing-masing dengan `#notetype:`; masing-masing lolos validasi (`data/v101-sesudah-2-basic.tsv`, `data/v101-sesudah-2-cloze.tsv`).
- Kelima kalimat cloze berasal dari frasa pengguna; tidak ada kalimat cloze karangan.
- Nilai: SESUDAH 9,0 (SEBELUM 6,0).

Rincian dua sisi: `00-openclaw-sebelum-sesudah.md`.
