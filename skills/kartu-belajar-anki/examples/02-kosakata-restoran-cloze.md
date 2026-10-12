# Contoh 2: kosakata Inggris pelayan, basic + cloze

> Hasil uji OpenClaw 2026-10-12 oleh penguji independen (sisi SESUDAH, skill aktif). Perbandingan lengkap dengan sisi SEBELUM: `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna

> Aku pelayan baru di restoran seafood, mau hafalin kosakata Inggris buat melayani turis. Tolong bikin kartu Anki, kalau bisa ada yang model cloze (isi bagian kosong) juga. Daftarnya:
> - menu = daftar makanan
> - bill / check = tagihan
> - allergy = alergi
> - spicy = pedas
> - grilled = dibakar
> - fried = digoreng
> - steamed = dikukus
> - "Are you ready to order?" = Sudah siap memesan?
> - "Would you like something to drink?" = Mau minum apa?
> - "Please wait a moment" = Mohon tunggu sebentar
> - "Enjoy your meal" = Selamat menikmati
> - "Do you have any food allergies?" = Apakah Anda punya alergi makanan?
> - tip = uang tip/uang terima kasih
> - reservation = reservasi
> - takeaway = bawa pulang
> - refill = tambah isi ulang (minuman)

## Keluaran di chat (SESUDAH)

> Semua valid. Berikut kartunya:
>
> **Ringkasan:** 32 kartu — 16 Basic (kata & frasa layanan) + 16 Cloze (isi kosong, kalimat & arti). Tag: `inggris-kata`, `inggris-frasa`, `inggris-cloze`.
>
> **Pratinjau contoh:**
>
> | Depan | Belakang | Jenis |
> |---|---|---|
> | spicy | pedas | basic |
> | "Enjoy your meal" | Selamat menikmati | basic |
> | Please {{c1::wait}} a moment. | Artinya: "Mohon tunggu sebentar" | cloze |
> | The crab is {{c1::steamed}} with ginger. | Kepitingnya dikukus dengan jahe | cloze |
> | Would you like a {{c1::refill}} on your iced tea? | Mau tambah isi ulang es teh Anda? | cloze |
>
> **Rencana belajar** (dari script):
> - 32 kartu, 15 kartu baru/hari → **selesai kartu baru dalam 3 hari**
> - 20 menit/hari; hari 1–3 fokus kartu baru, setelahnya sisihkan ±5–10 menit review kartu kemarin (Anki otomatis mengatur jadwal review ini)
>
> **Berkas TSV lengkap** (sudah tersimpan di `kartu-pelayan-seafood.tsv`):
>
> ```
> #separator:tab
> menu	daftar makanan	inggris-kata
> bill / check	tagihan	inggris-kata
> allergy	alergi	inggris-kata
> spicy	pedas	inggris-kata
> grilled	dibakar	inggris-kata
> fried	digoreng	inggris-kata
> steamed	dikukus	inggris-kata
> tip	uang tip / uang terima kasih	inggris-kata
> reservation	reservasi	inggris-kata
> takeaway	bawa pulang	inggris-kata
> refill	tambah isi ulang (minuman)	inggris-kata
> "Are you ready to order?"	Sudah siap memesan?	inggris-frasa
> "Would you like something to drink?"	Mau minum apa?	inggris-frasa
> "Please wait a moment"	Mohon tunggu sebentar	inggris-frasa
> "Enjoy your meal"	Selamat menikmati	inggris-frasa
> "Do you have any food allergies?"	Apakah Anda punya alergi makanan?	inggris-frasa
> {{c1::Are}} you ready to order?	Artinya: "Sudah siap memesan?"	inggris-cloze
> Would you like something to {{c1::drink}}?	Artinya: "Mau minum apa?"	inggris-cloze
> Please {{c1::wait}} a moment.	Artinya: "Mohon tunggu sebentar"	inggris-cloze
> {{c1::Enjoy}} your meal.	Artinya: "Selamat menikmati"	inggris-cloze
> Do you have any food {{c1::allergies}}?	Artinya: "Apakah Anda punya alergi makanan?"	inggris-cloze
> Can I see the {{c1::menu}}, please?	Bisakah saya lihat daftar makanannya? (menu = daftar makanan)	inggris-cloze
> Could we have the {{c1::bill}}, please?	Bolehkah kami minta tagihannya? (bill = tagihan)	inggris-cloze
> I have a seafood {{c1::allergy}}.	Saya punya alergi makanan laut. (allergy = alergi)	inggris-cloze
> This curry is too {{c1::spicy}} for me.	Kari ini terlalu pedas untuk saya. (spicy = pedas)	inggris-cloze
> The salmon is {{c1::grilled}} to perfection.	Salmon ini dibakar dengan sempurna. (grilled = dibakar)	inggris-cloze
> We serve {{c1::fried}} shrimp as an appetizer.	Kami menyajikan udang goreng sebagai pembuka. (fried = digoreng)	inggris-cloze
> The crab is {{c1::steamed}} with ginger.	Kepitingnya dikukus dengan jahe. (steamed = dikukus)	inggris-cloze
> Should I include the {{c1::tip}} in the bill?	Haruskah saya masukkan uang tip ke dalam tagihan? (tip = uang tip)	inggris-cloze
> Do you have a table {{c1::reservation}} tonight?	Apakah Anda punya reservasi meja malam ini? (reservation = reservasi)	inggris-cloze
> Would you like that for {{c1::takeaway}}?	Apakah Anda mau itu untuk dibawa pulang? (takeaway = bawa pulang)	inggris-cloze
> Would you like a {{c1::refill}} on your iced tea?	Apakah Anda mau tambah isi ulang es teh Anda? (refill = tambah isi ulang minuman)	inggris-cloze
> ```
>
> **Cara impor ke Anki:**
> 1. Buka Anki → File → Import.
> 2. Pilih file `kartu-pelayan-seafood.tsv`.
> 3. Pastikan pemisah/separator = Tab.
> 4. Untuk 16 baris pertama (kata & frasa): pilih tipe catatan **Basic**, kolom 1 = Front, kolom 2 = Back, kolom 3 = Tags.
> 5. Untuk 16 baris cloze (yang ada `{{c1::...}}`): impor terpisah atau ganti tipe catatan ke **Cloze** sebelum impor — kolom 1 jadi Text (kalimat cloze), kolom 2 jadi Back Extra (penjelasan arti).
>
> **Asumsi:**
> - "bill / check" aku gabung jadi satu kartu karena keduanya sinonim.
> - Kartu cloze kata kerja/benda inti (menu, bill, allergy, dst.) dibuat dari kalimat contoh biar lebih kena konteks restoran, bukan cuma terjemahan literal frasa yang sudah ada basic-nya.
>
> Pertanyaan:
> 1. Mau kartu cloze dan basic dipisah jadi 2 file TSV (biar gampang pilih tipe catatan Cloze/Basic saat impor), atau cukup satu file seperti ini?
> 2. Mau ditambah kosakata lain, misalnya nama-nama menu seafood (udang, cumi, kerang, dll.) atau frasa komplain tamu?

## Catatan penguji

- TSV diekstrak ke `data/hasil-sesudah-2-kosakata.tsv`; validasi ok, 32 kartu; rencana 3 hari benar.
- Cacat: Basic dan Cloze dalam satu berkas sehingga harus diimpor dua kali dengan tipe catatan berbeda; 16 kalimat cloze dikarang sendiri (tidak ada di daftar pengguna); menyebut nama berkas.
- Pembanding: sisi SEBELUM menghasilkan .apkg yang langsung bisa dibuka, tetapi isinya tidak tampil di chat dan jawabannya memuat path internal.
