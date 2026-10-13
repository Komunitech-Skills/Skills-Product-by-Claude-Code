# Uji 04 — Input tidak lengkap ("buatin privacy policy dong")

> Penguji independen, 2026-09-25. `claude-code (simulasi agent)`. Mengikuti SKILL.md bagian "Input (mode SUSUN)": info wajib kurang → tanya **sekali** dalam satu pesan berisi daftar bernomor.

## Input pengguna
> buatin privacy policy dong

## Output agent (lengkap)

Siap, saya bantu buatkan Kebijakan Privasi yang mengacu pada UU 27/2022 tentang Pelindungan Data Pribadi. Supaya isinya sesuai praktik usaha Anda (dan tidak ada yang dikarang), mohon jawab singkat pertanyaan berikut dalam satu balasan:

1. Nama usaha dan nama pemilik/PT/CV-nya?
2. Jualan/layanan lewat mana saja? (website, marketplace, WA Business, aplikasi, klinik/jasa tatap muka)
3. Data pelanggan apa saja yang dicatat? (nama, no. WA, alamat, email, foto, data kesehatan, data anak, dll.)
4. Dipakai untuk apa saja? (kirim pesanan, CS, promo, pengingat, dll.)
5. Data dibagikan ke siapa? (nama kurir, payment gateway, marketplace, Meta/Google/TikTok pixel, Google Drive/cloud, chatbot AI)
6. Disimpan berapa lama? (kalau belum tahu, saya pakai saran umum)
7. Email/WA untuk urusan data pribadi, dan alamat usaha?
8. Perlu versi bahasa Inggris?

Kalau ingin cepat, cukup jawab nomor 1–3; sisanya saya isi dengan saran umum dan tandai `[isi: ...]` supaya bisa Anda lengkapi nanti.

## Lanjutan (pengguna ingin cepat)
> Pengguna: "Warung Kopi Nanda, jualan lewat GoFood sama WA aja, nyatet nama & no WA buat pesanan."

Agent (ringkas): menyusun draf dari `templates/kebijakan-privasi.md` dengan nama "Warung Kopi Nanda"; data = nama, no. WA, isi chat, alamat antar; penerima = `[isi: kurir/ojek online]`, GoFood disebut sebagai platform (catatan: GoFood punya kebijakan privasi sendiri untuk data di platformnya — pilihan-per-jenis-usaha §2); transfer LN opsi (a) karena WhatsApp/Meta; masa simpan saran default ditandai "saran"; bagian cookie dihapus (tidak ada website). Status `PERLU DILENGKAPI` + daftar asumsi + disclaimer.

## Penilaian penguji
- ✅ Tanya sekali, daftar bernomor, bahasa awam, ada opsi cepat (sesuai pedoman kurasi Komunitech "instan").
- ✅ Tidak langsung mengarang dokumen generik.
- ⚠ 8 pertanyaan sedikit panjang untuk pengguna awam; opsi "jawab 1–3 saja" (tambahan agent) sebaiknya ditulis eksplisit di SKILL.md.
- ⚠ Pertanyaan "Data anak / kesehatan / keuangan?" (tabel Input: **wajib**) hanya tersirat di no. 3 — cukup, tetapi bisa terlewat bila pengguna menjawab singkat. Usul: tambah "(ada data kesehatan/anak? ya/tidak)".
