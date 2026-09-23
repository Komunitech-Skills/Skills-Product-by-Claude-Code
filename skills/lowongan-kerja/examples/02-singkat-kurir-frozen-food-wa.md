# Contoh 02 – Permintaan singkat: kurir frozen food, versi WA grup saja

## Skenario
S2, permintaan singkat/malas. Pengguna mengetik cepat, hanya minta versi grup WhatsApp. Info wajib (posisi, nama usaha, kota) ada. Status kerja dan jam kerja tidak disebut. Syarat "punya motor sendiri" sah untuk pekerjaan kurir.

## Input pengguna
```
bikinin dong loker kurir buat usaha frozen food aku "Beku Nikmat" di medan, harus punya motor sendiri, gaji 2,8jt + uang bensin. versi WA grup aja, lamar lewat WA 0812-0000-1234
```

## Output

## Versi grup WhatsApp
```
*LOKER KURIR — Medan*
*Beku Nikmat* (frozen food) butuh *kurir antar pesanan*.

✅ Antar pesanan sesuai rute harian
✅ Terima pembayaran COD & foto bukti terima
✅ Jaga frozen box tetap tertutup agar produk tetap beku

Syarat: punya motor sendiri & SIM C aktif, paham jalan di Medan, bisa pakai Google Maps.
Benefit: *Rp2.800.000/bulan + uang bensin*.
Jam kerja: [isi jam kerja].
Lamar: WA 0812-0000-1234 (kirim CV/data diri singkat), paling lambat *7 Oktober 2026*.
Gratis, tidak dipungut biaya apa pun.
```

Versi lengkap (JobStreet/Glints) dan versi Instagram tidak aku buat karena kamu minta versi WA saja. Kalau nanti butuh, bilang saja.

**Pertanyaan screening (untuk disaring lewat chat WA)**
1. Motor apa yang kamu pakai, dan apakah SIM C-mu masih berlaku?
2. Area Medan mana saja yang kamu hafal jalannya?
3. Pernah jadi kurir/ojol sebelumnya? Berapa lama?
4. Kalau pembeli COD tidak ada di rumah saat paket tiba, apa yang kamu lakukan?
5. Bisa mulai kerja kapan, dan jam berapa saja kamu bisa bekerja?

**Asumsi:**
- "SIM C aktif" ditambahkan karena mengendarai motor untuk bekerja wajib punya SIM. Hapus bila tidak perlu.
- Tugas "frozen box" dan "COD" disusun dari tugas umum kurir (sesuaikan).
- Status kerja dan jam kerja belum disebut. Jam kerja ditulis `[isi jam kerja]`; isi sebelum diposting.
- Batas lamaran 14 hari dari hari ini (7 Oktober 2026).
- Karena lamaran lewat WA, data pelamar (nomor HP, CV) sebaiknya hanya dipakai untuk rekrutmen dan dihapus bila pelamar tidak lolos (UU PDP).

## Catatan penguji
- **Bagus:** menghormati permintaan "WA grup aja" (langkah 5 dan tabel Input: kanal default semua, tapi pengguna memilih). Versi WA 76 kata (≤ 80, mepet batas). Syarat motor sendiri dipertahankan karena sah menurut tabel `references/anti-diskriminasi.md` ("Punya motor & SIM C: Boleh"). Nomor WA fiktif.
- **Bagus:** `[isi jam kerja]` tidak diasumsikan, dan uang bensin tidak diberi angka karangan.
- **Catatan:** placeholder `[isi jam kerja]` di dalam teks siap-kirim berisiko ikut terkirim ke grup kalau pengguna awam tidak membacanya dengan teliti. Skill sudah menyebutnya di Asumsi. Saran ringan untuk SKILL.md: pada versi WA, beri peringatan tebal di atas blok bila masih ada placeholder.
- **Kurang (ringan):** SKILL.md tidak menyebut apakah pertanyaan screening tetap diberikan bila pengguna hanya minta satu versi. Di sini tetap diberikan secara singkat, dan itu terasa membantu.
