# Skenario 3 (S3, normal) — HR kantor 30 orang: pengumuman + FAQ + THR

## Skenario
HR kantor 30 orang minta: pengumuman cuti bersama, perubahan jam kerja Ramadan, FAQ
karyawan, dan pengumuman THR (skill tidak boleh menghitung nominal).

## Input pengguna (persis)
> "Tolong buatin 3 hal: (1) pengumuman cuti bersama Idul Fitri, kantor libur tanggal 30
> Maret - 3 April 2026, masuk lagi 6 April, (2) pengumuman jam kerja selama Ramadan jadi
> jam 08.00-16.00 (biasanya 08.00-17.00) mulai 1 Maret 2026, (3) FAQ karyawan dari
> pertanyaan yang sering masuk: 'THR cair kapan?', 'cuti tahunan sisa boleh dirapel gak?',
> 'kalau WFH pas Ramadan boleh gak?'. Kantor kami 30 orang, kontak HR: Ibu Sari
> (0812-0000-1234)."

## Output (mengikuti SKILL.md, template `pengumuman-internal.md` x2 + `faq-karyawan.md`)

### 1. Pengumuman Cuti Bersama
```
📢 *Pengumuman: Libur Cuti Bersama Idul Fitri*

Sehubungan dengan Hari Raya Idul Fitri, kantor akan libur pada:
📅 30 Maret – 3 April 2026

Operasional kembali normal pada 6 April 2026.
Untuk keperluan mendesak selama libur, hubungi Ibu Sari (0812-0000-1234).

Selamat Idul Fitri bagi yang merayakan 🙏
```

### 2. Pengumuman Perubahan Jam Kerja Ramadan
```
📢 *Pengumuman: Perubahan Jam Kerja*

Mulai 1 Maret 2026, jam kerja kantor selama bulan Ramadan berubah menjadi:
🕐 08.00 – 16.00, Senin–Jumat

Penyesuaian ini berlaku untuk menyesuaikan jam operasional selama bulan Ramadhan.

Mohon seluruh karyawan menyesuaikan jadwal mulai tanggal tersebut. Pertanyaan bisa
disampaikan ke Ibu Sari (0812-0000-1234).
```

### 3. FAQ Karyawan
```
❓ *FAQ Karyawan* — Cuti Bersama, Jam Kerja Ramadan & THR

*THR cair kapan?*
[isi: tanggal pencairan THR belum disebutkan pengguna — mohon konfirmasi ke HR/keuangan;
sesuai aturan pemerintah THR wajib dibayarkan paling lambat H-7 sebelum Hari Raya]. Untuk
perhitungan nominal per karyawan, silakan gunakan skill `hitung-thr` atau hubungi Ibu Sari.

*Cuti tahunan sisa boleh dirapel gak?*
[isi: kebijakan rapel cuti tahunan belum disebutkan — mohon konfirmasi kebijakan resmi
kantor ke HR sebelum dijawab ke karyawan].

*Kalau WFH pas Ramadan boleh gak?*
[isi: kebijakan WFH selama Ramadan belum disebutkan pengguna — mohon konfirmasi ke HR/
atasan].

Pertanyaan lain yang belum tercakup? Hubungi Ibu Sari (0812-0000-1234).
```

## Catatan penguji

**Bagus:**
- Pengumuman cuti bersama & jam kerja: tanggal dipakai persis dari input pengguna, tidak
  ada tanggal SKB dikarang — sesuai instruksi "TANYAKAN ke pengguna, jangan mengarang
  tanggal" (di sini pengguna sudah memberi tanggal, jadi langsung dipakai, benar).
- **FAQ THR eksplisit TIDAK mengarang nominal atau tanggal pasti** — mengikuti instruksi
  "jangan mengarang kebijakan yang tidak disebutkan", dan **benar merujuk ke skill
  `hitung-thr`** sesuai SKILL.md §Batasan. Ini poin kritis dari brief uji dan LOLOS.
- Dua pertanyaan FAQ lain (rapel cuti, WFH Ramadan) **tidak dijawab dengan menebak** —
  ditandai `[isi: ...]` sesuai instruksi "Jika jawaban pasti tidak diketahui, tulis 'Akan
  dikonfirmasi...' alih-alih menebak." Ini penting karena kalau agen asal menjawab "boleh"
  atau "tidak boleh" tanpa dasar, itu berisiko jadi kebijakan palsu yang dibaca 30 orang.
- Nomor kontak HR dipakai sesuai bahan mentah, format `0812-0000-1234` (fiktif, aman untuk
  contoh).

**Temuan:**
- **RINGAN**: FAQ pertanyaan "THR cair kapan" agak panjang/bertele karena menggabungkan
  tiga hal sekaligus (isi placeholder + rujukan H-7 + rujukan skill hitung-thr) dalam satu
  jawaban yang seharusnya "1-2 kalimat" sesuai format FAQ. Template `faq-karyawan.md`
  tidak memberi contoh konkret bagaimana menjawab singkat sambil tetap merujuk ke
  `hitung-thr` — sedikit menyulitkan agen menjaga keringkasan. Saran: tambahkan 1 contoh
  jawaban FAQ THR di template agar formatnya lebih konsisten antar-agen.
- Tidak ada cacat berat/sedang. Rujukan ke `hitung-thr` (cek brief) terbukti ADA dan
  benar dipakai, bukan skill mengarang angka sendiri.
