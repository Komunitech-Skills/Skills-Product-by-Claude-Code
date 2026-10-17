# Riwayat perubahan — satu-lawan-satu-dan-umpan-balik

Catatan teknis per versi.

## Catatan revisi 1.0.3 (2026-10-17)
- Contoh ringkas di SKILL.md disamakan dengan `examples/01-teguran-kasir-terlambat.md` (jam masuk 09.40/09.35/09.50, standar 08.45, dampak ke Dedi dan pelanggan). Sebelumnya memakai "09.30" dan "toko telat buka" yang tidak ada di contoh uji dan menambah fakta yang tidak disebut di input. Aturan dan perilaku skill tidak berubah.

## Catatan revisi 1.0.2 (2026-10-12)
- Revisi dari uji OpenClaw asli (skor 5,5 naik ke 8,4 sesudah revisi): untuk permintaan PHK sepihak atau mencari-cari kesalahan karyawan, jawaban memakai pola wajib tiga bagian dalam satu jawaban: tolak singkat, padanan yang sah (pembinaan bertahap, catatan kejadian faktual, konsultasi ketenagakerjaan), lalu tetap kerjakan bagian yang boleh secara tertulis. Jawaban tidak ditutup dengan menu "mau yang mana dulu?".
- Larangan di jawaban: tidak menyebut kata "skill", "script", atau nama berkas/folder kepada pengguna dan tidak memakai emoji. Fakta yang disebut pengguna tidak diubah. Aturan tanggal ditambah: hari ke-N sama dengan tanggal mulai ditambah (N-1) hari.
- Contoh di `references/kerangka-umpan-balik.md` dan deskripsi skill (kata pemicu seperti "nggak enak negur karyawan") diperbarui.

## Catatan revisi 1.0.1 (2026-10-09)
- Ditambah catatan khusus: mengubah jam kerja, upah, atau tugas pokok harus mengecek perjanjian kerja/peraturan perusahaan lebih dulu dan disampaikan ke yang bersangkutan sebelum diumumkan. Masalah pribadi yang diceritakan karyawan tidak diteruskan ke tim dan tidak dicatat di grup. Bila tanggal cek jatuh di hari libur, digeser ke hari kerja berikutnya; teguran tidak ditutup dengan "bukan hal buruk kok". Hasil uji simulasi agent 6,2 naik ke 8,5.

## Catatan revisi 1.0.0 (2026-10-09)
- Rilis awal (draft, belum diuji): panduan percakapan atasan/pemilik usaha dengan tim kecil: agenda 1-on-1, kerangka umpan balik KONTEKS-FAKTA-DAMPAK-TANYA-SEPAKAT untuk budaya sungkan, rencana onboarding karyawan baru 30 hari, dan cara mengumumkan perubahan, lengkap dengan naskah ucapan dan pesan WhatsApp. Diadaptasi dari karya berlisensi CC BY 4.0 (lihat `ATTRIBUTION.md`).
