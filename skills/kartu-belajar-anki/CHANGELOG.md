# Riwayat perubahan — kartu-belajar-anki

Catatan teknis per versi.

## Catatan revisi 1.0.1 (2026-10-12)
- Revisi dari uji pertama (skor 6,1 naik ke 7,75) dan uji ulang (5,75 naik ke 8,5): kartu Basic dan Cloze tidak boleh dicampur dalam satu blok TSV; bila keduanya diminta, ditulis dua blok berurutan masing-masing dengan baris `#separator:tab` dan `#notetype:`, lalu diimpor dua kali di Anki (dijelaskan di `references/format-impor-anki.md`).
- Kartu Cloze hanya dari frasa atau kalimat yang ditempel pengguna, tidak mengarang kalimat tambahan. Bila materi belum ditempel, agent memberi contoh isian siap balas dan deck contoh fiktif 8-12 kartu, lalu bertanya maksimal 3 hal.
- Di kanal chat (Telegram/WhatsApp), isi kartu wajib utuh di chat dan berkas TSV terpisah hanya ditawarkan lewat "balas kirim file". Agent tidak menyebut jalur file di komputer, nama berkas, atau kata proses ("divalidasi", "script").
- Script: `rencana_belajar.py` memberi peringatan bila menit belajar 0 (rencana hanya perkiraan); `validasi_dek.py` menolak baris yang hanya berisi tab/spasi. Uji regresi diperbarui.

## Catatan revisi 1.0.0 (2026-10-12)
- Rilis awal (uji internal): mengubah materi belajar atau SOP menjadi dek kartu belajar siap impor Anki (format TSV, tipe Basic dan Cloze) dengan validasi dek dan rencana belajar harian lewat script `validasi_dek.py` dan `rencana_belajar.py`, tanpa instalasi tambahan. Termasuk contoh dek SOP gudang.
