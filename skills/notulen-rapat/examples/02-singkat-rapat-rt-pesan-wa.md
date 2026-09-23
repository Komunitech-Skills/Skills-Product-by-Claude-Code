# Contoh 02 – Permintaan singkat: rapat RT untuk dikirim ke grup warga

## Skenario
S2, permintaan singkat/malas. Sekretaris RT mengetik ringkasan rapat hari Minggu malam dan terutama butuh pesan untuk grup WA warga. Catatan memuat keputusan "mayoritas setuju", tenggat relatif ("sabtu depan", "minggu depan"), usulan yang ditunda ("nanti dulu"), dan info sensitif (warga yang menunggak iuran). Info sensitif itu tidak boleh masuk ke pesan grup. Semua nama fiktif.

## Input pengguna
```
rangkumin dong rapat RT kemarin buat dikirim ke grup warga

rapat RT 05 RW 02 perum griya asri, minggu malam 20 sept di pos ronda jam 19.30. hadir pak RT (pak darto), bu wulan sekretaris, pak joko bendahara, warga kira2 25 KK.
- iuran keamanan naik dr 50rb jd 60rb, mayoritas setuju. mulai kapan blm dibahas
- kerja bakti bersihin got sabtu depan jam 7 pagi, tiap rumah kirim 1 org
- lampu jalan gang 3 mati, pak joko lapor ke kelurahan minggu depan
- usul bikin grup WA khusus info keamanan, nanti dulu
- pak budi nunggak iuran 4 bulan, nanti dibahas pribadi sm pak RT
```

## Proses (dijalankan agent)
```
$ python3 scripts/tanggal_relatif.py --rapat "20-09-2026" --ekspresi "sabtu depan" "minggu depan" --format teks
Tanggal rapat: Minggu, 20 September 2026
- "sabtu depan" -> Sabtu, 26 September 2026 [pasti]
- "minggu depan" -> Senin, 21 September 2026 [perkiraan] | Tidak menyebut hari; diartikan Senin minggu depan. Mohon dikonfirmasi.
```

## Output

## Pesan untuk grup WhatsApp
```
Selamat pagi, Bapak/Ibu warga RT 05.
Berikut ringkasan rapat RT pada Minggu, 20 September 2026:
1. Iuran keamanan naik dari Rp 50.000 menjadi *Rp 60.000* (disetujui mayoritas warga yang hadir). Mulai bulan apa akan diinformasikan kemudian.
2. *Kerja bakti membersihkan got: Sabtu, 26 September 2026, pukul 07.00.* Setiap rumah mengirim 1 orang.
3. Lampu jalan Gang 3 yang mati akan dilaporkan ke kelurahan oleh Pak Joko.
4. Usulan grup WA khusus info keamanan akan dibahas lagi di rapat berikutnya.
Notulen lengkap tersedia di sekretaris RT. Terima kasih atas kehadirannya.
```

# NOTULEN RAPAT
**Rapat Warga RT 05 RW 02 Perumahan Griya Asri**

| | |
|---|---|
| Hari, tanggal | Minggu, 20 September 2026 |
| Waktu | pukul 19.30 WIB–[isi jam selesai] |
| Tempat/platform | Pos ronda RT 05 |
| Pemimpin rapat | Pak Darto (Ketua RT) (disimpulkan) |
| Notulis | Bu Wulan (Sekretaris) (disimpulkan) |
| Peserta | Pak Darto (Ketua RT), Bu Wulan (Sekretaris), Pak Joko (Bendahara), dan ±25 KK warga (dari catatan, mohon dicek) |

## Agenda (dikelompokkan dari isi)
1. Iuran keamanan
2. Kerja bakti
3. Lampu jalan Gang 3
4. Grup WA info keamanan
5. Tunggakan iuran

## Keputusan
1. Iuran keamanan naik dari Rp 50.000 menjadi Rp 60.000 (mayoritas setuju).
2. Kerja bakti membersihkan got pada Sabtu, 26 September 2026, pukul 07.00; setiap rumah mengirim 1 orang.

## Action Items
| No | Tugas | PIC | Tenggat | Status |
|---|---|---|---|---|
| 1 | Melaporkan lampu jalan Gang 3 yang mati ke kelurahan | Pak Joko | Senin, 21 September 2026 ("minggu depan") ⚠️ | Belum mulai |
| 2 | Pelaksanaan kerja bakti membersihkan got | Semua rumah (1 orang/rumah) | Sabtu, 26 September 2026, pukul 07.00 ("sabtu depan") | Belum mulai |
| 3 | Membicarakan tunggakan iuran secara pribadi | Pak Darto (Ketua RT) | ⚠️ belum ada tenggat | Belum mulai |

## Belum diputuskan / dibahas di rapat berikutnya
- Usulan grup WA khusus info keamanan ("nanti dulu").
- Tanggal mulai berlaku iuran Rp 60.000.

## Perlu dikonfirmasi
- **Iuran Rp 60.000 mulai berlaku bulan apa?** Belum dibahas.
- **"Minggu depan"** untuk laporan lampu jalan diartikan paling lambat **Senin, 21 September 2026** (karena rapat hari Minggu, "minggu depan" dimulai keesokan harinya). Mungkin yang dimaksud **pekan 21–27 September**. Mohon dicek.
- Iuran Rp 60.000 itu per bulan? Catatan tidak menyebut periodenya, jadi pesan WA juga tidak menyebutnya.
- Jumlah peserta "kira-kira 25 KK": bila ada daftar hadir, lampirkan.

Rapat berikutnya: belum ditentukan.

> 🔒 **Catatan untukmu:** poin **tunggakan iuran Pak Budi** hanya ada di notulen lengkap dan **sengaja tidak dimasukkan ke pesan grup WA**, karena menyangkut data pribadi warga. Simpan notulen lengkap di arsip sekretaris.

## Catatan penguji
- **Script dijalankan sungguhan.** "minggu depan" berstatus `perkiraan` dan masuk "Perlu dikonfirmasi". **Verifikasi independen:** 20/9/2026 = Minggu, 26/9 = Sabtu, 21/9 = Senin.
- **Bagus:** info sensitif (tunggakan individu) dikeluarkan dari pesan WA dan pengguna diberi tahu, sesuai *Batasan*. Pesan WA memakai variasi formal untuk pengurus RT dari `references/aturan-klasifikasi.md`, tanpa salam keagamaan karena catatan tidak memakainya. Pesan diletakkan di atas karena itulah yang diminta pengguna. Panjangnya 89 kata (≤ 120).
- **Bagus:** "mayoritas setuju" menjadi keputusan (penanda kuat, sesuai contoh kasus 1 di referensi), dan "mulai kapan" masuk "Perlu dikonfirmasi".
- **Kurang (sedang, dari uji script):** rapat ini jatuh pada **hari Minggu**. Script memakai minggu Senin–Minggu, sehingga "minggu depan" = besoknya (Senin 21/9). Kali ini status sudah `perkiraan`, jadi aman. Tapi pada uji tepi, rapat hari Minggu dengan ekspresi **"senin minggu depan"** menghasilkan **Senin besoknya dengan status `pasti`**, dan "jumat depan"/"rabu depan" juga `pasti`. Padahal banyak orang Indonesia (kalender dimulai hari Minggu) memaknainya satu minggu lebih lambat. Rapat RT, keluarga, dan komunitas sering diadakan hari Minggu. Lihat HASIL-UJI.md.
