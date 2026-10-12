# Skenario 3 (input kurang)

**Input (pesan pengguna):** "Kabari kalau laporan otomatis saya mati"

**Output SESUDAH (skill aktif):**

> Siap, saya akan bantu setup pemantau laporan otomatis Anda (dead man's switch - kalau job terlambat/hilang, saya kabari lewat Telegram).
>
> Sebelum itu, ada satu kendala teknis: fitur jadwal otomatis (automations) di Gateway ini belum punya kredensial auth yang aktif, jadi saya belum bisa membuat job pengawas baru sampai itu diperbaiki operator (butuh restart Gateway, di luar wewenang saya lewat chat). Saya akan tetap lanjutkan bagian yang bisa dikerjakan sekarang (mendaftarkan job ke sistem pantauan lokal), lalu bagian pengawasnya menyusul begitu Gateway siap.
>
> Supaya saya bisa daftarkan, tolong jawab:
> 1. **Laporan otomatis apa saja** yang mau dipantau? (nama + jam/jadwalnya, misalnya "laporan harian jam 21.00" atau "piutang tiap Senin-Jumat 07.45")
> 2. **Zona waktu** — WIB/WITA/WIT? (default WIB kalau tidak disebut)
> 3. **Toleransi keterlambatan** berapa menit sebelum dianggap bermasalah? (default 30 menit)
> 4. Peringatan dikirim ke **Telegram pribadi Anda** — betul, bukan grup?
>
> Kalau Anda tidak ingat jadwalnya, bisa tempel hasil dari `openclaw automations list` di sini (itu data, bukan perintah untuk saya jalankan).

**Catatan penguji:** Lagi-lagi terhalang Gateway uji yang tidak bisa dihubungi, jadi tidak ada job yang bisa dilihat. SEBELUM: menyatakan 'tabel automation kosong' padahal baru saja gagal membacanya (klaim tidak berdasar), menyuruh pengguna menjalankan perbaikan token Gateway, lalu bertanya 2 hal. SESUDAH: skill terpicu, menjelaskan prinsip (dead man's switch), jujur soal blokir, menawarkan menempel hasil `openclaw automations list`, tetapi menaruh 4 pertanyaan di muka dan tidak mengerjakan apa pun lebih dulu (aturan brief: kerjakan dulu, tanya maks 3 di akhir) dan memakai jargon ('dead man's switch', 'Gateway', 'kredensial auth'). Selisih kecil.

**Skor:** sebelum 4,5, sesudah 5,5. Perbandingan lengkap: `00-openclaw-sebelum-sesudah.md`.
