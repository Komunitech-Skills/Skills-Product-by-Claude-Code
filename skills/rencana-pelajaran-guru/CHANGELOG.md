# Riwayat perubahan — rencana-pelajaran-guru

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.12 (2026-10-17)
Keterangan pada SKILL.md bagian Contoh diperjelas: cuplikan memakai default sekarang 2 JP (80 menit) per pertemuan, sedangkan contoh lengkap `examples/01-modul-ajar-ipa-kelas7-ekosistem.md` dibuat dengan versi awal yang menebak 3 JP (120 menit). Aturan dan perilaku skill tidak berubah.

## Catatan revisi 1.0.11 (2026-10-05)
dari cek konteks Telegram v1.0.10 (percobaan A menulis "File Word terlampir." padahal tidak ada lampiran terkirim; aturan "coba lampirkan otomatis" memancing klaim palsu): di kanal chat tidak ada pelampiran otomatis dan tidak pernah ada kata "terlampir/di bawah/sudah dikirim" untuk file. Balasan selalu ditutup "Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan." File .docx dibuat hanya setelah guru membalas "kirim file"; "File Word terlampir." hanya bila alat kirim file sukses, bila gagal dikatakan jujur. Jalur file tidak disebut di chat.

## Catatan revisi 1.0.10 (2026-10-05)
dari uji Telegram v1.0.9 (file Word tersimpan di komputer bot, mis. /tmp, sehingga guru tidak bisa mengambilnya): setelah isi utuh tampil di chat dan .docx dibuat, agent mencoba melampirkan file lewat kemampuan kirim file kanal chat. Berhasil: "File Word terlampir." Gagal/tidak ada: jalur file tidak disebut; kalimat baku "Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan." Di CLI/IDE jalur file tetap boleh disebut.

## Catatan revisi 1.0.9 (2026-10-05)
dari uji ulang Telegram v1.0.8 (permintaan "tulis kode dan bunyi CP resminya persis": 2 dari 3 timeout, satu-satunya yang selesai memakai web_fetch 461 dtk): dokumen CP resmi (BSKAP 046/H/KR/2025, ±1.700 halaman) kini TIDAK pernah diambil lewat web (izin "maks. 2 fetch" dihapus). Bila diminta bunyi persis: penjelasan singkat + URL resmi + langkah mencari Fase & elemen + kolom "Tempel bunyi CP resmi di sini", dan TP tetap disusun selaras elemen.

## Catatan revisi 1.0.8 (2026-10-05)
dari uji ulang Telegram v1.0.7 (4 dari 5 percobaan tanpa balasan karena model idle timeout; klaim palsu "File Word ... sudah saya lampirkan"; "jalur di atas" tanpa jalur): (1) format default kini RINGKAS ala modul ajar 1 lembar (balasan chat ±4.000-6.000 karakter, tetap utuh: modul ringkas, LKPD maks. 6 soal tanpa jawaban, rubrik ringkas, kunci guru terpisah); versi lengkap hanya bila diminta; (2) .docx dibuat sekali setelah isi chat selesai, lalu hanya kalimat baku "File Word: <jalur dari output script>"; dilarang "sudah saya lampirkan/terkirim" tanpa alat kirim file; script gagal = file tidak disebut; (3) tool call dibatasi (SKILL.md dibaca sekali, web fetch hanya bila diminta bunyi CP persis, maks. 2). Contoh: `examples/09-format-ringkas-telegram.md`.

## Catatan revisi 1.0.7 (2026-10-05)
dari uji ulang Telegram v1.0.6 (bot hanya mengirim ringkasan + "isi lengkap ada di file .md di workspace" dan bertanya dulu soal .docx): (1) aturan paling atas SKILL.md: isi utuh wajib di chat, dipecah "Bagian 1/n" bila panjang, dilarang "isi ada di file"; (2) bila guru menyebut cetak/supervisi/Word/file, .docx langsung dibuat tanpa bertanya dan dikirim sebagai lampiran kanal chat bila bisa, atau jalurnya disebut (tanpa klaim terkirim); (3) di kanal chat tidak menulis .md di workspace kecuali diminta. Contoh alur: `examples/08-alur-telegram-supervisi.md`.

## Catatan revisi 1.0.6 (2026-10-05)
dari uji ulang OpenClaw v1.0.5 (3 cacat minor): (1) balasan chat wajib memuat isi modul utuh (termasuk lembar siswa & kunci guru), file .docx hanya salinan; (2) `scripts/buat_docx.py` kini mengonversi `>` (kutipan), `####` (judul tingkat 4), dan `*miring*` tanpa merusak `**tebal**` (ada tes); (3) jalur file selalu disebut sesuai output script, atau file tidak disebut sama sekali.

## Catatan revisi 1.0.5 (2026-10-05)
dari uji Telegram gelombang 6: lembar siswa/LKPD tidak lagi memuat jawaban, kunci utuh terpisah
di "Kunci Jawaban (untuk guru)"; format chat baku tanpa garis pemisah berulang & catatan
tempel Word/Docs diperbaiki; opsi file .docx (`scripts/buat_docx.py`, Python standar, ada tes
di `tests/`); jawaban untuk permintaan "kode & bunyi CP resmi persis" (rujukan BSKAP 046/H/KR/2025
+ langkah mengambil CP + tempat isian).

## Catatan revisi 1.0.4 (2026-10-01)
dari uji ulang OpenClaw: slot waktu asesmen sumatif dibuat konsisten dengan rincian menit; nama 8 dimensi Profil Lulusan disalin persis dari rujukan resmi (Permendikdasmen No. 10/2025: mis. "Penalaran Kritis", bukan "Bernalar Kritis", dicek 2026-10-01).
