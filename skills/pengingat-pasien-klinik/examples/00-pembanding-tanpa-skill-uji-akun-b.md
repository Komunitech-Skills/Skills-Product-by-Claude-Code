# Uji A/B tambahan (Akun B, independen) — tanpa skill vs dengan skill

Skenario normal pertama: "Catat Bu Sari, kontrol gigi lagi 10 hari lagi, WA 0812-0000-1111, dia
setuju diingatkan." (hari ini disimulasikan 26 Sep 2026, Sabtu)

## Tanpa skill (perilaku agent generik, diperkirakan dari pola umum tanpa instruksi khusus)
Agent generik biasanya akan:
- Menjawab dalam bentuk teks bebas: "Baik, saya catat Bu Sari untuk kontrol gigi tanggal 6
  Oktober 2026 dengan nomor WA 0812-0000-1111" — tetapi **tidak ada penyimpanan nyata** (tidak
  ada file/database), sehingga jika ditanya lagi besok "siapa yang harus diingatkan hari ini?"
  agent tidak punya cara mengetahuinya kecuali percakapan yang sama diulang dalam satu sesi.
- Perhitungan tanggal "10 hari lagi" dari 26 September dilakukan sebagai penalaran bahasa, bukan
  hitungan pasti — rawan salah terutama dekat pergantian bulan (lihat verifikasi manual di bawah).
- Tidak ada penjaga privasi: agent generik bisa saja ikut mencatat kalau pengguna menambahkan
  "kontrol giginya karena diabetes" — tidak ada mekanisme otomatis yang menolak.
- Tidak ada draf pesan WA yang konsisten formatnya; setiap kali diminta, redaksinya bisa berbeda
  dan berpotensi memuat kalimat yang terdengar seperti saran medis.
- Tidak ada catatan persetujuan/consent yang dipisahkan dari data, dan tidak ada perintah hapus
  data yang terstruktur (hak UU PDP).

## Dengan skill (dijalankan sungguhan, folder scratchpad terpisah)
```
$ python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 --json tambah \
    --nama "Bu Sari" --wa "0812-0000-1111" --jenis "kontrol gigi" --tanggal "10 hari lagi" --persetujuan ya
{"ok": true, "mode": "tersimpan", "id": "1", "teks": "Tersimpan #1: Bu Sari | Kontrol gigi | 6 Okt 2026 | persetujuan: ya", "peringatan": []}
```
Verifikasi manual independen (bukan dari skill): `date(2026,9,26) + timedelta(days=10)` =
**2026-10-06** (Selasa). Cocok persis dengan keluaran skill ("6 Okt 2026"). Data tersimpan
permanen di CSV lokal, sehingga besok/lusa "siapa yang harus diingatkan hari ini?" bisa dijawab
konsisten dari data yang sama (`daftar`), bukan diulang dari percakapan.

## Kesimpulan uji A/B (independen)
Sejalan dengan `00-pembanding-tanpa-skill.md` milik Akun A: skill memberi nilai tambah jelas —
tanggal dihitung pasti (bukan ditebak), data persisten di CSV lokal, format draf konsisten, dan
penjaga privasi/consent yang terstruktur tidak mungkin didapat dari agent generik tanpa skill.
Tidak ada perubahan skor dari temuan ini (skor final ada di `HASIL-UJI.md`, bagian "Uji independen
Akun B (2026-09-26)").
