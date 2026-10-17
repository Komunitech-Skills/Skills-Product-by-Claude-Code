# Contoh 04 — Input tidak lengkap

## Skenario
S4. Pengguna hanya minta "presentasi" tanpa tujuan, isi, atau data.

## Input pengguna
```
tolong buatin presentasi dong buat besok pagi
```

## Output
```
Siap, saya bantu. Supaya presentasinya pas, boleh jawab singkat pertanyaan ini (sekali saja):

1. Presentasi ini untuk apa? (mis. pitch ke investor, proposal ke perusahaan lain, pengajuan KUR/bank, laporan bulanan ke atasan, profil perusahaan, penawaran ke reseller, atau materi pelatihan karyawan)
2. Boleh kirim poin-poin isinya, atau saya buatkan dulu kerangkanya dari topik saja?
3. Kira-kira berapa slide / berapa lama presentasinya?
4. Ada warna atau logo brand yang mau dipakai?
5. Nanti dipakai untuk ditampilkan di layar, dicetak jadi PDF, atau dua-duanya?

Kalau mau cepat, cukup jawab nomor 1 saja — sisanya saya pakai pengaturan standar dan saya sebutkan asumsinya di akhir.
```

## Catatan penguji
- Sesuai SKILL.md bagian Input: hanya tujuan yang wajib, pertanyaan digabung satu pesan bernomor (5 pertanyaan), tidak menanyakan satu per satu.
- Kalimat penutup "cukup jawab nomor 1" adalah penerapan aturan "jika pengguna ingin cepat … pakai default" — tidak tertulis persis di SKILL.md tapi sejalan. Saran: tambahkan kalimat itu ke contoh pertanyaan di SKILL.md agar semua agent melakukannya (pengguna "buat besok pagi" jelas sedang terburu-buru).
- Tidak ada file dibuat sebelum tujuan jelas — benar, karena tujuan menentukan template.

## Penyegaran v1.1.6 (2026-10-17)
> Isi output dan catatan penguji di atas **tidak diubah**. Dicocokkan dengan SKILL.md v1.1.6 bagian Input: tetap maksimal 5 pertanyaan bernomor dalam satu pesan, dan kalimat "Kalau mau cepat, cukup jawab nomor 1 saja" kini memang tertulis di SKILL.md (saran penguji di atas sudah diterapkan). Perubahan v1.1.6 (lampiran berkas di kanal chat, bahasa awam, tanpa nama skill/alat) tidak memengaruhi skenario ini karena belum ada berkas yang dibuat; output di atas tidak menyebut nama skill sehingga sudah sesuai.
