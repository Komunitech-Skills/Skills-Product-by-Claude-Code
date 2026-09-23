# Contoh 02 – Permintaan singkat: undangan rapat warga RT

## Skenario
S2, permintaan singkat/malas. Ketua RT minta undangan rapat warga dalam satu kalimat, dengan jam "jam 7 malem". Kop dan alamat lengkap tidak disebut. Skill harus memakai script untuk nama hari acara, menulis jam sesuai EYD, dan memakai placeholder untuk data yang kurang. Semua nama fiktif.

## Input pengguna
```
bikinin dong surat undangan rapat warga RT 03 RW 07 buat bahas iuran sampah, minggu 4 okt 2026 jam 7 malem di rumah pak RT, yg ttd ketua RT pak slamet riyadi. kelurahan tugu, depok
```

## Proses (dijalankan agent)
```
$ python3 scripts/nomor_tanggal.py --tanggal 23-09-2026 --kota Depok --urut 1 --kode UND --instansi "RT03-RW07" --acara "4 Oktober 2026" --format teks
Tanggal surat     : 23 September 2026
Hari              : Rabu
Bulan Romawi      : IX
Baris tanggal     : Depok, 23 September 2026
Nomor surat       : 001/UND/RT03-RW07/IX/2026
Hari/tanggal acara: Minggu, 4 Oktober 2026
```

## Output

```
RUKUN TETANGGA 03 RUKUN WARGA 07
KELURAHAN TUGU, DEPOK
Sekretariat: [alamat rumah Ketua RT] | WA [nomor]
________________________________________________________________

Nomor    : 001/UND/RT03-RW07/IX/2026                      Depok, 23 September 2026
Perihal  : Undangan Rapat Warga

Yth. Bapak/Ibu Warga RT 03 RW 07
Kelurahan Tugu
di tempat

Dengan hormat,
Kami mengundang Bapak/Ibu untuk menghadiri rapat warga yang akan dilaksanakan pada
hari, tanggal : Minggu, 4 Oktober 2026
pukul         : 19.00 WIB–selesai
tempat        : Rumah Ketua RT 03, [alamat]
acara         : Pembahasan iuran sampah

Mengingat pentingnya acara tersebut, kami mengharapkan kehadiran Bapak/Ibu tepat waktu.
Atas perhatian Bapak/Ibu, kami mengucapkan terima kasih.

Hormat kami,
Ketua RT 03 RW 07,


Slamet Riyadi
```

**Catatan untuk kamu** (tidak dicetak):
- "Minggu, 4 Oktober 2026" sudah dicek dengan script: **benar hari Minggu**.
- "Jam 7 malem" ditulis **pukul 19.00 WIB** sesuai EYD.
- **Isi dulu:** alamat rumah Pak RT dan nomor WA di kop.
- Nomor urut diasumsikan **001** karena tidak disebut. Ganti bila RT sudah punya surat keluar lain bulan ini.
- Baris "Lampiran" dihapus karena tidak ada lampiran.
- Mau ditambah baris konfirmasi kehadiran, atau versi pesan WA singkat untuk grup warga?

## Catatan penguji
- **Script dijalankan sungguhan.** "Minggu, 4 Oktober 2026" dan nomor `001/UND/RT03-RW07/IX/2026` benar. **Verifikasi independen** dengan `datetime`: 4 Oktober 2026 = Minggu.
- **Bagus:** permintaan malas langsung jadi surat siap cetak. "Jam 7 malem" dikonversi ke "pukul 19.00 WIB", "di tempat" dipisah, "Yth." tanpa "Kepada", baris Lampiran dihapus (sesuai tabel aturan), dan nomor urut yang tidak disebut ditulis sebagai asumsi.
- **Kurang (ringan):** contoh di SKILL.md menulis `Lampiran : —`, padahal aturan di `references/aturan-eyd-dan-format.md` menyebut "hapus baris bila tidak ada". Kedua instruksi ini tidak konsisten. Agent mengikuti aturan referensi.
- **Kurang (ringan):** kode instansi `RT03-RW07` berasal dari pilihan agent. SKILL.md tidak memberi pedoman singkatan untuk organisasi warga. Sebaiknya agent menyebutnya di catatan agar pengguna tahu kode itu bisa diganti.
