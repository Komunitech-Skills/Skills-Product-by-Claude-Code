# Riwayat perubahan — perjanjian-sederhana

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.4 (2026-10-01)
- Tanggal penandatanganan tidak lagi diisi otomatis dengan tanggal hari ini; bila belum disebut, draf memuat `[isi: tanggal]`.
- Nilai bawaan template (mis. denda keterlambatan 0,1%/hari maks. 5%) kini selalu dicantumkan sebagai asumsi yang perlu kamu konfirmasi.

## Catatan revisi 1.0.5 (2026-10-03)
- Naskah perjanjian lengkap kini selalu ditampilkan langsung di chat (dipecah rapi per pasal bila panjang) sehingga bisa disalin, tidak hanya disimpan sebagai file.
- Ada pengecekan konsistensi biaya: listrik, air, iuran/retribusi pasar, PBB, dan perbaikan masing-masing ditanggung satu pihak dan sama di semua pasal maupun daftar asumsi. Pemeriksa draf otomatis menandai bila bertentangan.
- Tetap: draf ini bukan nasihat hukum.

## Catatan revisi 1.0.6 (2026-10-03)
- Pasal pengakhiran sewa tempat & sewa alat kini memakai jalur yang sah: teguran tertulis, tenggat, lalu musyawarah atau pengadilan. Tidak ada lagi pengosongan/pengambilan paksa sebagai bawaan.
- Bila kamu sendiri meminta klausul pengosongan sepihak, skill menampilkannya sebagai opsi dengan peringatan risiko hukumnya. Pemeriksa draf menandai klausul seperti ini.

## Catatan revisi 1.0.7 (2026-10-13)
- Rujukan "UU PDP" di checklist tanda tangan kini ditulis lengkap: UU 27/2022 tentang Pelindungan Data Pribadi. Tidak ada perubahan perilaku.

## Catatan revisi 1.0.8 (2026-10-13)
- `references/regulasi.md`: rujukan ke catatan riset internal diganti kalimat yang berdiri sendiri. Tidak ada perubahan perilaku.

## Catatan revisi 1.0.9 (2026-10-26)
Perbaikan cacat kanal chat dari pra-cek konteks Telegram 21 Okt 2026 (skor 7,5, TIDAK SIAP; isi hukum dan angka saat itu sudah benar). Isi pasal, angka, dan aturan hukum tidak diubah.
- Di aplikasi chat, jalur/folder/nama berkas tidak lagi disebut. Bila draf juga disimpan, balasan hanya berbunyi: "Draf juga sudah saya simpan sebagai berkas. Balas 'kirim file' bila mau dikirim sebagai dokumen."
- Balasan tidak lagi memakai kata script/skrip/tool/exec/python (mis. "angka & terbilang sudah dihitung ulang").
- Naskah di chat dikirim sebagai teks biasa (bukan satu blok kode besar), tanpa judul `#`/`##`, Lampiran berupa baris pendek (bukan tabel), dipecah "Bagian 1/N" masing-masing < 3.800 karakter dan hanya dipotong di antara pasal.
- Perintah baru `perjanjian.py bagi` (naskah siap kirim per bagian) dan `perjanjian.py cek-balasan` (memeriksa balasan sebelum dikirim). `perjanjian.py --versi` menampilkan versi. `cek` kini memberi info bila masih ada isian gaya `[[...]]`.
- Satu gaya isian `[isi: ...]` di SKILL.md, templates, references, dan contoh 01–05 (rekaman uji 00-* dibiarkan apa adanya, diberi catatan).
- Uji regresi ditambah untuk semua aturan di atas.
- Belum diuji ulang di bot Telegram asli maupun pra-cek konteks Telegram.
