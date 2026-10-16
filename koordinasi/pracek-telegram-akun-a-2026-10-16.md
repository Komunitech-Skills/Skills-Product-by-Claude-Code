# Pra-cek konteks Telegram: 7 permintaan uji ulang Akun A + seleksi-cv-pelamar (2026-10-16)

Penguji: agen penguji independen. Alat: `openclaw-real/uji-tg.sh` (`--channel telegram`, tanpa kirim), HOME bersih berisi hanya skill yang diuji, berurutan, 1 percobaan per skill (tanpa router timeout). Sisi DENGAN saja; `tender-checklist` juga TANPA (HOME tanpa skill). Pesan = field `text` pada msgs-gNNb.json (mention bot di awal dihapus). Versi katalog cocok untuk semua skill. Data g21/g22 disalin ke `data/` workspace uji. Tidak ada token/kunci dicetak.

Catatan teknis: mode `--channel telegram` tanpa `--deliver` tidak memperlihatkan lampiran; keberadaan berkas dicek dari workspace uji, bukan dari pengiriman.

## Ringkasan

| Skill | Versi | Skor | Verdik | Alasan singkat |
|---|---|---|---|---|
| presentasi-instan | 1.1.6 | 7,5 | SIAP KIRIM (bersyarat) | 13 slide, pasca-uang Rp3 M benar; pra-uang Rp2,55 M tidak disebut; berkas .html dibuat, cek lampiran di bot asli |
| audit-akun-iklan | 1.0.7 | 6,5 | TIDAK SIAP | angka margin benar, tetapi tanpa verdik tunggal BONCOS/TIPIS/SEHAT; 2 dari 3 tindakan tak nyambung ke keluhan boncos |
| laporan-insiden-usaha | 1.0.5 | 8 | SIAP KIRIM | semua angka kunci benar, dugaan ditandai, "sudah dilakukan" hanya yang disebut |
| sop-writer | 1.0.6 | 8 | SIAP KIRIM | SOP utuh di chat (4 bagian), tanpa klaim kirim/jalur berkas |
| studio-video-pendek-ai | 1.0.5 | 8,5 | SIAP KIRIM | semua syarat tambahan terpenuhi |
| resi-picking | 1.0.5 | 9 | SIAP KIRIM | semua kunci & syarat terpenuhi |
| tender-checklist (DENGAN) | 1.0.9 | 8,5 | SIAP KIRIM | semua kunci angka, checklist, dasar aturan, PPh 22 muncul |
| tender-checklist (TANPA) | , | 6 | pembanding | generik, tanpa dasar aturan/PPh 22, minta konfirmasi dulu; selisih +2,5 |
| seleksi-cv-pelamar (5 CV) | 1.0.2 | 6 | TIDAK SIAP | tabel 10 kolom + 6.882 karakter; isi seleksi benar |

## Rincian

### presentasi-instan 1.1.6 (7,5, SIAP KIRIM bersyarat)
- Tools: read, ls, write, exec. Berkas dibuat: `pitch-bersih-kilat.html` (19,6 KB, 13 elemen `<section>`/slide). Chat menyebut "(13 slide)" dan daftar 13 judul: cocok.
- Kunci: "valuasi post-money Rp 3.000.000.000 dihitung dari Rp 450 juta / 15%" benar. Pra-uang Rp2,55 M TIDAK ada di chat maupun HTML (hanya "Implikasi valuasi post-money").
- Berkas: HTML tidak disebut jalur komputer; chat menutup "Balas 'kirim file' kalau file di atas tidak muncul". Pra-cek tidak dapat membuktikan lampiran terkirim sebagai dokumen; wajib dicek di bot asli.
- Istilah proses: "Sudah dicek: file bisa dibuka tanpa internet ... tidak ada slide yang kepadatan teks" (klaim proses ringan). Tabel lebar: tidak ada di chat.
- Bukti: "Presentasi Pitch Investor - Bersih Kilat sudah jadi (13 slide)." / "valuasi post-money Rp 3.000.000.000 dihitung dari Rp 450 juta ÷ 15%"

### audit-akun-iklan 1.0.7 (6,5, TIDAK SIAP)
- Angka benar: 33.695 (GMV Max, 37,9 %), 55.500 (website, 62,4 %). Titik impas: 82 dan 179 pesanan benar (pembulatan ke atas). ROAS impas ditulis 1,61 dan 2,65, hitungan persis 89.000/55.500 = 1,603 dan 89.000/33.695 = 2,641: dibulatkan ke atas, selisih kecil.
- Syarat tambahan: titik impas ada di balasan pertama (ya); 3 tindakan (ya); maks 5 pertanyaan (ya, 5); skor sementara "belum bisa dihitung" (bukti ~10 %, dapat diterima). TIDAK terpenuhi: verdik tunggal BONCOS/TIPIS/SEHAT; bot menulis "BELUM BISA DIPASTIKAN" dengan rentang ROAS per jalur. Tindakan 2 (2FA) dan 3 (tab Under Review) tidak berkaitan dengan keluhan boncos.
- Jalur file: tidak ada kecuali kalimat penutup "File kerja: belum ada (audit pendahuluan, file jawaban dibuat setelah data di atas terisi)", ini istilah proses/berkas yang membingungkan pembeli awam.
- Bukti: "VERDIK: BELUM BISA DIPASTIKAN — Anda belum sebut ROAS aktual" / "File kerja: belum ada (audit pendahuluan..."

### laporan-insiden-usaha 1.0.5 (8, SIAP KIRIM)
- Kunci: 40 label salah, 25 dibatalkan, 15 terlanjur jalan, 5 komplain, 35 belum komplain, ongkir Rp1.500.000, 09.00 sampai 14.00: semua benar dan konsisten antarbagian (kronologi, dampak, ringkasan WA).
- Syarat tambahan: "Sudah dilakukan" hanya "Menghubungi kurir untuk membatalkan 25 paket" (benar); penyebab tak disebut ditandai "(dugaan, perlu dikonfirmasi)"; ada `[isi: ...]` untuk yang kosong.
- Minus kecil: kronologi 09.00 menulis "admin menyalin data alamat" (jam penyalinan tidak disebut pengguna); 5.095 karakter (2 pesan Telegram); tanggal "16 Oktober 2026 (kemarin)" dari jam bot. Jalur file/tabel/istilah proses: tidak ada.
- Bukti: "Sudah dilakukan (sesuai keterangan Anda): - Menghubungi kurir untuk membatalkan 25 paket yang belum diambil"

### sop-writer 1.0.6 (8, SIAP KIRIM)
- Tools: read, ls, exec, tool_search, tool_describe. Tidak ada berkas di workspace. SOP lengkap tampil di chat dalam 4 bagian bertanda "(1/4)" sampai "(4/4)" (5.661 karakter), tanpa klaim "sudah dikirim", tanpa jalur berkas, tanpa tabel.
- Kunci: 150 paket/hari (indikator), 2 staf packing, admin Mbak Sinta QC, pickup 15.00, botol pecah dan salah varian ditangani tersendiri.
- Minus: botol diasumsikan "kaca" tanpa ditandai asumsi (pengguna hanya bilang botol toner pecah); "[isi jam]" satu isian ditanyakan di akhir; tawaran poster/SOP lanjutan.
- Bukti: "Ini SOP Packing Pesanan untuk Glowria Skin. (1/4)" / "Bungkus botol kaca dengan bubble wrap minimal 2 lapis"

### studio-video-pendek-ai 1.0.5 (8,5, SIAP KIRIM)
- Hasil pertama: asumsi, hook (maks 3 dtk, plus cadangan), naskah per adegan 0-3/3-8/8-15, shot list rekam HP per adegan, sulih suara, caption, checklist label AI. 15 detik, Rp6.500/kg, WA benar. Placeholder `[nomor WA]` ada. Tidak ada kalimat "lolos cek fakta". Berkas `laundry-bersih-jaya-naskah.txt` dibuat tapi tidak disebut di chat (bagus).
- Minus: kata "Fiktif" pada nama usaha dibuang; 2 baris "jalur A/B" sedikit istilah teknis ("jalur A - rekam HP").
- Bukti: "Adegan 3 | 8-15 dtk | ... Teks layar: "Pesan via WA: [nomor WA]""

### resi-picking 1.0.5 (9, SIAP KIRIM)
- Tools: read, exec; berkas `daftar-ambil.md` dan `urutan-resi.md` dibuat di data/ tetapi tidak disebut jalurnya. Kunci benar: 7 pesanan di file, 4 aktif, 4 jenis, 12 pcs (3+3+1+5), JNE 2 / SiCepat 1 / J&T 1, A5 batal, A6 dan A7 bermasalah (alasan disebut), KAOS-HT-M stok 3 → 0 HABIS. Tambahan benar: baris dobel dan baris Total dilewati, GANTUNGAN-X tak ada di stok, resi A3 kosong ditandai.
- Minus kecil: bagian "Dilewati" menambah 2 butir (baris dobel, baris Total) di luar kunci; alasan A6 "jumlah 0/negatif" kurang spesifik. Tabel: tidak ada. Penutup "Balas 'kirim file'" sesuai keputusan 2026-10-05.
- Bukti: "KAOS-HT-M: stok 3 → 0, HABIS (minimum 10) — perlu restock segera"

### tender-checklist 1.0.9 (DENGAN 8,5 SIAP KIRIM; TANPA 6)
- DENGAN (4.163 karakter): DPP Rp39.768.000, PPN Rp4.374.480, total Rp44.142.480, 23,86 % dari HPS, ambang 80 % (Rp148 jt): semua benar. Tenggat 14 Okt 15.00 disebut di baris pertama DAN checklist dokumen tetap lengkap (administrasi, teknis, harga). Jaminan penawaran tidak disyaratkan; jaminan pelaksanaan bila kontrak > Rp200 jt. Ada "Dasar aturan: ... dicek 26 Sep 2026", penafian, dan pengingat bendahara memungut PPN dan memotong PPh 22 1,5 %. Tidak ada jalur file; tidak ada tabel.
- Minus: 4.163 karakter hanya melewati 4.096 sedikit (terpotong 2 pesan); "PPN 11% efektif" tidak menyebut 12 % x 11/12; jaminan pelaksanaan "5 %" tidak relevan karena kontrak ± Rp44 jt.
- TANPA (4.131 karakter): hitungan benar (Rp39.768.000 / Rp4.374.480 / Rp44.142.480), tetapi tidak menyebut % HPS maupun ambang 80 %, daftar dokumen umum, tanpa dasar aturan/penafian, tanpa PPh 22, minta konfirmasi tenggat dulu, klaim PPN "11 % bukan 12 %" kurang tepat, dan menduga salah ketik harga tinta. Selisih DENGAN − TANPA = +2,5.
- Bukti DENGAN: "Terhadap HPS Rp185.000.000 → hanya 23,86%, jauh di bawah batas 80%" / "Dasar aturan: Perpres 16/2018 ... dicek 26 Sep 2026"

### seleksi-cv-pelamar 1.0.2 (6, TIDAK SIAP)
- Pesan uji: skenario 01 dikurangi dari 12 menjadi 5 CV (`examples/data/admin-toko/cv-01..05.txt`, 3.276 karakter). Berhasil dalam 1 percobaan (tanpa timeout); 6.882 karakter di jawaban.
- Isi benar dan rapi: 5 CV terbaca, 3 lanjut, 1 cadangan, 1 belum sesuai; ranking C1 92, C2 92, C3 75, C5 54, C4 27; 4 pertanyaan wawancara per kandidat; 3 draf pesan; pengingat privasi; tidak ada kriteria usia/status pernikahan.
- Cacat: "Tabel skor per kriteria" berkolom 10 (Kode, 6 kriteria, Wajib, Tambah, Skor) dan satu tabel lain; di Telegram tampil sebagai teks mentah lebar. Panjang 6.882 karakter (2 pesan) dengan bagian ganda (ranking, tabel, detail, rekap). Timeout sebelumnya diduga karena 12 CV (6,8 KB); 5 CV berjalan lancar. Istilah "NIK/alamat/tanggal lahir tidak saya tampilkan" aman.
- Perbaikan yang disarankan: hapus tabel skor lebar (ganti satu baris per kandidat), pangkas bagian rekap supaya < 4.096 karakter bila memungkinkan.
- Bukti: "Tabel skor per kriteria ... | Kode | Shopee/Tokopedia (3) | Excel/Sheet (2) | Chat/komplain (2) | Canva (1) | Iklan (1) | Foto/konten (1) | Wajib | Tambah | Skor |"
