# Riwayat perubahan — cek-privasi-openclaw

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.1.6 (2026-10-16)
- Tindak lanjut pra-cek konteks Telegram (16 Oktober 2026): balasan di chat terasa terlalu teknis (jalur berkas, perintah terminal, istilah mentah, banyak emoji, ±5.000 karakter yang dipecah otomatis). Kini bila pengguna chat lewat Telegram/WhatsApp, balasan pertama dibatasi 3.000 karakter, berbentuk daftar berbutir (tanpa tabel), berurutan: ringkasan, berbahaya, perlu perhatian, sudah aman, tawaran tindakan.
- Jalur berkas, angka izin, dan perintah terminal tidak lagi ditampilkan di chat. Gantinya kalimat awam ("berkas pengaturan bot Anda bisa dibaca pengguna lain di komputer ini") dan tawaran satu kata: balas "rapikan" untuk mengunci izin berkas pengaturan (hanya setelah Anda setuju; isi berkas tidak diubah; bisa dikembalikan dengan "kembalikan"). Perintah teknis hanya muncul bila Anda membalas "tampilkan perintahnya".
- Istilah teknis diganti kata sehari-hari dan dijelaskan sekali ("izin bot menjalankan perintah di komputer", "ruang terbatas", "kunci rahasia", "layanan inti bot"). Emoji dibatasi tiga penanda status (berbahaya, perlu perhatian, aman); pertanyaan pilihan "dipakai untuk apa" ditulis bernomor biasa tanpa emoji angka.
- Lokasi ditulis relatif saja ("folder pengaturan OpenClaw Anda"), tidak menyebut jalur komputer. Tambahan di bahan agent: `references/format-kanal-chat.md` (kerangka, contoh, kamus istilah), `references/openclaw.md` bagian 10 (langkah kunci izin berkas), satu baris baru di `references/dampak-perubahan.md`.
- Tidak berubah: semua pemeriksaan audit, aturan "tidak mengubah apa pun sebelum daftar lengkap tampil dan Anda setuju", penolakan permintaan menyadap chat orang lain, ringkasan UU PDP, dan larangan menampilkan isi kunci rahasia. Format laporan lengkap untuk terminal/IDE tetap ada.

## Catatan revisi 1.1.5 (2026-10-15)
- Tindak lanjut verifikasi rujukan aturan (dicek 15 Oktober 2026): `references/uu-pdp.md` kini mencantumkan **PP 33/2026** tentang Peraturan Pelaksanaan UU 27/2022 (diundangkan 16 Juli 2026, mulai berlaku 16 Januari 2027) menggantikan catatan "PP belum diverifikasi", serta dasar berlaku penuh UU PDP sejak Oktober 2024 (Pasal 74).
- Pemberitahuan kebocoran data: frasa "dalam hitungan hari" diganti "**paling lambat 72 jam (3×24 jam)** secara tertulis kepada pemilik data dan lembaga" dengan rujukan UU 27/2022 Pasal 46 ayat (1); SKILL.md langkah 5 & checklist ikut diperbarui.
- Tambah satu pengingat sanksi administratif UU PDP (Pasal 57) di `references/uu-pdp.md` dan FAQ README.
- Penolakan permintaan menyadap chat kini merujuk UU ITE lengkap: UU 11/2008 jo. UU 1/2024 (perubahan kedua), Pasal 31 — di SKILL.md dan bagian baru `references/uu-pdp.md`.
- README: manfaat UU PDP menyebut nomor & tahun aturan; versi terkini 1.1.5. Cara kerja audit OpenClaw tidak berubah.

## Catatan revisi 1.1.4 (2026-10-01)
- Uji OpenClaw 2026-10-01: agent sempat menjalankan `chmod` sebelum menampilkan daftar perbaikan. Kini semua perubahan (config, `chmod`/izin file, `--fix`) hanya dijalankan setelah daftar lengkap ditampilkan dan pemilik menjawab "ya"; "gak usah nanya" sebelum melihat daftar bukan persetujuan.
- Permintaan menyadap/memata-matai chat orang lain: penolakan kini wajib ditulis lengkap & sopan di balasan itu sendiri (alasan UU ITE Pasal 31 & UU PDP + alternatif sah), bukan hanya "tetap saya tolak".
