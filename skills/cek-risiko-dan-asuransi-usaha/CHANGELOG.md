# Riwayat perubahan — cek-risiko-dan-asuransi-usaha

Catatan teknis per versi.

## Catatan revisi 1.0.2 (2026-10-09)
- Daftar jenis perlindungan diperluas: tanggung gugat profesi (malpraktik/kelalaian profesi), kerusakan mesin/peralatan, dan barang titipan pelanggan, disertai penegasan bahwa tanggung gugat umum biasanya tidak menjamin ketiganya. Ditambah catatan bahwa tidak ada angka premi atau nilai pertanggungan di dokumen.
- Urutan langkah kerja dirapikan: dana darurat dihitung lebih dulu, baru risiko. BPJS menyebut juga JKP (jaminan kehilangan pekerjaan). Untuk klaim ditolak/tertunda disebut urutan keberatan tertulis, lalu OJK lewat Kontak 157, lalu lembaga penyelesaian sengketa. Jawaban permintaan "merek asuransi terbaik" menambah cara mengecek legalitas perusahaan dan agen. Script dan uji regresi diperbarui.

## Catatan revisi 1.0.1 (2026-10-09)
- Perbaikan tiga cacat berat dari uji independen pertama (7/10): risiko yang tidak bisa diasuransikan (akun marketplace dibekukan, orang kunci atau pemasok utama hilang) kini diberi respons "kurangi + alihkan lewat kontrak/cadangan", bukan saran asuransi (kolom `bisa_diasuransikan` di berkas risiko).
- Risiko yang "besar" (dampak ≥ 4 atau kerugian lebih besar dari dana darurat) selalu diarahkan ke alih risiko; opsi `--dana` memakai dana darurat yang sudah dihitung. Karyawan cedera/sakit otomatis ditulis sebagai kewajiban BPJS pemberi kerja.
- Perintah `dana` menambah opsi `--cicil` (cicilan menabung dibulatkan ke atas); angka ditulis 3000000 atau 3.000.000, desimal ditolak. 16 uji regresi.

## Catatan revisi 1.0.0 (2026-10-09)
- Rilis awal (draft, ditulis ulang bersih dari daftar ide): memetakan risiko usaha kecil (kebakaran, banjir/gempa, pencurian, tanggung jawab ke pelanggan, BPJS, ketergantungan pada satu orang/pemasok) menjadi tabel risiko dengan skor prioritas, langkah murah, dan keputusan perlu asuransi atau tidak, serta target dana darurat yang dihitung script `cek_risiko.py`. Bukan nasihat asuransi.
