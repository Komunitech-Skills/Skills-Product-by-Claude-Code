# 04 — Input tidak lengkap: tanya sekali

## Skenario
S4 — pengguna tidak menyebut jenis usaha/produk (satu-satunya info **wajib** di tabel Input). Skill harus bertanya sekali (maks. 5 pertanyaan
bernomor) dan menawarkan default untuk sisanya.

## Input pengguna
```
Bikinin kalender konten dong
```

## Output

Siap! Supaya ide kontennya pas dengan usahamu (bukan sekadar "posting produk"), saya perlu tahu beberapa hal dulu:

1. **Usahanya apa dan jual apa saja?** (mis. "toko kue, jual bolu & brownies", "laundry kiloan", "toko hijab online")
2. **Mulai tanggal berapa?** Kalau tidak disebut, saya buat untuk 1–31 Oktober 2026 (bulan depan).
3. **Posting di mana saja?** IG, TikTok, WA Status, atau semuanya?
4. **Ada promo atau acara khusus** di periode itu? (diskon gajian, ulang tahun toko, produk baru) — sebutkan tanggal & isinya.
5. **Sanggup bikin konten berapa kali seminggu?** (mis. video 3×/minggu, sisanya foto/Status)

Kalau mau cepat, cukup jawab nomor 1. Sisanya saya pakai default: bulan depan, IG + TikTok + WA Status, 1 konten per hari, gajian tanggal 25 & 1,
tanpa promo karangan (hari promo saya tandai `[isi: …]`), dan hasilnya tabel lengkap semua hari + tawaran file CSV.

## Catatan penguji
- **Bagus:** satu pesan, 5 pertanyaan bernomor, jalan cepat (jawab nomor 1 saja), default disebut jelas. Pertanyaan 5 (kapasitas produksi) mencegah rencana
  yang tidak sanggup dijalankan — sesuai langkah 3 SKILL.md.
- **Catatan akurasi:** default "bulan depan" dari 23 Sep 2026 = Oktober 2026. Di sini agent menawarkan 1–31 Oktober (satu bulan penuh), sedangkan tabel
  Input SKILL.md menulis "Tanggal 1 bulan depan, 30 hari" (akan berhenti di 30 Okt). Lihat cacat ringan di HASIL-UJI.
