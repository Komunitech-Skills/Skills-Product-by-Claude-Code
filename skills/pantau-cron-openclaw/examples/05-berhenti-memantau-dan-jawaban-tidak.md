# Contoh 05: berhenti memantau, dan pemilik menjawab "tidak"

> Contoh perilaku yang diharapkan menurut SKILL.md 1.0.6, ditulis pembuat skill. **Bukan hasil uji** di bot; belum dijalankan penguji independen.

## A. Pemilik minta berhenti, lalu menjawab "tidak"

**Pemilik:** Pantauan laporan harian hentikan saja ya.

**Asisten:**
Rencana (belum ada yang saya ubah):
- Laporan harian (tiap hari 21.00 WIB): langkah lapor selesai di akhir pesannya saya buang; isi laporan tidak berubah
- Tagih piutang: tetap dipantau, jadi pengawas tiap jam dan ringkasan pagi tetap jalan
- Laporan harian saya keluarkan dari pantauan; riwayatnya dibiarkan
- Sesudah selesai, saya baca ulang daftar jadwal sebelum bilang "sudah dihapus"

Lanjut? (ya/tidak)

**Pemilik:** tidak

**Asisten:** Baik, tidak ada yang saya ubah; pantauan dan pengawas tetap berjalan seperti sebelumnya.

(Tidak ada perintah yang dijalankan, tidak ada pertanyaan ulang.)

## B. Pemilik minta berhenti untuk jadwal yang lapor selesainya ada di perintah buatan sendiri

Keadaan: di pantauan ada laporan harian, tagih piutang, dan backup mingguan. Backup mingguan adalah jadwal berupa perintah buatan pemilik yang sudah memanggil lapor selesai sendiri (bukan dipasang pantauan ini).

**Pemilik:** Backup mingguan tidak usah dipantau lagi.

**Asisten:**
Rencana (belum ada yang saya ubah):
- Backup mingguan (tiap Minggu 02.00 WIB): langkah lapor selesai ada di perintah buatan Anda sendiri; tidak saya ubah
- Backup mingguan tidak diawasi lagi; langkah lapor selesainya tetap jalan tanpa galat, tidak dicatat, dan tidak mengirim kabar apa pun
- Laporan harian dan tagih piutang tetap dipantau, jadi pengawas tiap jam dan ringkasan pagi tetap jalan
- Sesudah selesai, saya baca ulang daftar pantauan sebelum bilang "sudah tidak diawasi"

Lanjut? (ya/tidak)

**Pemilik:** ya

**Asisten:**
- Backup mingguan: tidak diawasi lagi (saya baca ulang dari daftar pantauan). Langkah lapor selesai di perintah buatan Anda tidak saya ubah; langkah itu tetap jalan tanpa galat, tidak dicatat, dan tidak mengirim kabar apa pun.
- Laporan harian dan tagih piutang tetap diawasi seperti sebelumnya.

(Di balik layar: `hapus backup-mingguan --terima-lapor`, bukan `hapus` biasa; jadwal backup pemilik tidak diubah sama sekali.)

## C. Pemilik menolak rencana pemasangan

**Pemilik:** tidak

**Asisten:** Baik, tidak ada yang saya pasang atau ubah. Kalau nanti mau, cukup bilang "pantau laporan saya".
