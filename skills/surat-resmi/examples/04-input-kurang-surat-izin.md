# Contoh 04 – Input tidak lengkap: "buatin surat izin"

## Skenario
S4, input tidak lengkap. "Surat izin" bisa berarti izin kegiatan, izin keramaian, izin tidak masuk kerja, atau izin memakai tempat. Jenis surat, pengirim, dan penerima (semuanya wajib) tidak jelas. Skill harus bertanya sekali, maksimal 5 pertanyaan.

## Input pengguna
```
buatin surat izin
```

## Output

Siap! "Surat izin" ada beberapa macam, jadi aku perlu tahu sedikit dulu. Jawab singkat saja:

1. **Izin untuk apa?** Misalnya izin mengadakan acara/keramaian, izin memakai tempat (balai, lapangan, parkiran), izin tidak masuk kerja/sekolah, atau lainnya.
2. **Dari siapa?** Nama kamu atau nama usaha/organisasi/panitia, plus alamat singkat. Surat pakai kop atau tidak?
3. **Ditujukan ke siapa?** Contoh: Ketua RT/RW, Lurah, Kapolsek, atasan di kantor, atau kepala sekolah.
4. **Kapan dan di mana?** Hari/tanggal, jam, dan tempat kegiatan (kalau izin kegiatan).
5. **Siapa yang tanda tangan** (nama dan jabatan)?

Kalau mau cepat, sebutkan saja jenisnya (mis. "izin keramaian acara nikahan"). Aku buatkan template dengan kolom `[...]` yang tinggal kamu isi.

## Catatan penguji
- **Bagus:** tepat sesuai aturan "tanyakan sekali (maks 5 pertanyaan bernomor)", dengan opsi cepat. Pertanyaan 1 memberi contoh konkret yang sesuai daftar "Kapan digunakan" (permohonan izin kegiatan/keramaian/peminjaman tempat/cuti).
- **Bagus:** tidak menebak jenis surat. Kalau menebak, hasilnya berisiko tidak berguna.
- **Catatan:** untuk "izin keramaian" ke kepolisian, instansi sering meminta formulir/syarat sendiri. Pengingat ini sebaiknya muncul setelah jenisnya diketahui. SKILL.md tidak menyebutnya secara khusus, hanya lewat catatan umum "ikuti instansi tujuan".
