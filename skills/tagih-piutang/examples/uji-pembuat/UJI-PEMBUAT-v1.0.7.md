# Catatan pembuat: tagih-piutang v1.0.7 (2026-10-10)

Bukan hasil uji independen; ini catatan perbaikan dari laporan penguji OpenClaw
(`examples/HASIL-UJI-openclaw-2026-10-10.md`, v1.0.6: tanpa 6,4 / dengan 8,0, LULUS tipis).

## 1. Kolom pembayaran diabaikan diam-diam (dampak terbesar)
Reproduksi (CSV 10 nota fiktif toko bangunan, judul 'no nota,pelanggan,total,sdh bayar,jatuh tempo,keterangan',
rupiah/tanggal campur, tanggal hitung 2026-10-10):
- v1.0.6: kolom 'sdh bayar' tidak dikenali tanpa peringatan. Total piutang Rp183.415.000 (10 nota),
  telat Rp168.140.000 (8 nota); UD Maju Jaya (lunas Rp9.600.000) tampil telat 41 hari; Umar tampil sisa Rp27.800.000
  (seharusnya Rp17.800.000); pengingat dari keterangan tidak terbaca ("pengingat sebelumnya 0x").
- v1.0.7: total belum lunas Rp157.540.000 (9 nota), telat Rp142.540.000 (7 nota), belum jatuh tempo Rp15.000.000;
  UD Maju Jaya masuk blok "Sudah lunas, TIDAK ditagih"; Umar sisa Rp17.800.000/101 hari, tahap 6 (3x diingatkan,
  dibaca dari keterangan); Slamet Rp13.750.000/59 hari tahap 6; Anton Rp4.200.000/22 hari; Dedi Rp1.000.000.
  Cocok dengan hitungan independen Decimal di tes `test_csv_berantakan_sdh_bayar_angka_independen`
  dan dengan angka kebenaran milik penguji.
- Judul dikenali tanpa peduli huruf besar/kecil, spasi, garis bawah, tanda hubung, camelCase, aksen: sdh bayar,
  sudah dibayar, dibayar(kan), terbayar, DP, uang muka, cicilan, angsuran, pembayaran (Rp), paid, amount paid, dll.
  Beberapa kolom pembayaran dijumlahkan. Kolom 'lunas'/'status bayar' menandai nota lunas ('belum lunas' dan
  'lunas sebagian' tidak dianggap lunas).
- Peringatan (baris berawal ⚠️ di paling atas output, tidak diam): judul mirip pembayaran tetapi tidak dikenali
  (mis. 'sdh transfer'); isi pembayaran tak terbaca (baris tetap ada, dianggap belum dibayar, ditandai);
  tanggal bayar terisi padahal sisa ada; keterangan menyebut lunas padahal sisa ada; kolom sisa di file beda dari
  hitungan. Bila tidak ada kolom pembayaran sama sekali: catatan eksplisit.
- Bonus (saran penguji no. 2): jumlah pengingat dibaca dari kolom keterangan ("sudah WA 2x", "diingatkan 3x"),
  ditandai di tabel agar pengguna bisa mengoreksi; kolom `sudah_diingatkan` eksplisit tetap menang.
- Tes: 16 lama + 17 baru = 33 OK (`python3 tests/uji_regresi.py`).

## 2-4. Perubahan SKILL.md
- Input kurang: kerjakan dulu (templat tahap awal + versi lebih tegas bila "sudah lama"), tanya maks. 3 di akhir.
- Aturan bahasa: tanpa script/skill/file/folder/path/JSON/nama berkas; tanpa sapaan bergender/gaul untuk pengguna;
  debitur disapa sesuai pemberian pengguna atau "Bapak/Ibu".
- Penolakan jebakan: 1-2 kalimat + alasan hukum utama, 1 kalimat alternatif, lalu langsung kerjakan yang boleh.
- Saran penguji no. 4-5 (murah): batas maksimal denda ditulis dalam rupiah; baris rekening di semua pesan.
- Checklist diperluas. SKILL.md 156 baris.

## Belum diuji ulang
Perubahan perilaku agent (butir 2-4) belum diuji ulang di OpenClaw; perlu uji independen berikutnya.
