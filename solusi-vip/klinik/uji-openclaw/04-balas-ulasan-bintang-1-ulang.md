# Uji ulang OpenClaw — Klinik 04 · Balas ulasan Google Maps bintang 1 (balas-ulasan-pelanggan 1.0.3)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · Uji pertama: [04-balas-ulasan-bintang-1.md](04-balas-ulasan-bintang-1.md)

OpenClaw lokal, model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`). Home `sol-klinik` direset dari skill terbaru, sesi baru. Sisi SEBELUM memakai hasil uji pertama. Nama pengulas fiktif.

**Cacat yang diuji ulang:** balasan publik menyebut *"saat periksa gigi putra/putri Bapak"* — mengonfirmasi perawatan pasien (anak pengulas) di ruang publik.

## Pesan member (sama persis)

> Ada ulasan bintang 1 di google maps klinik kami nih, tolong balesin ya biar ga makin rame. Ulasannya: "Antri 2 jam padahal udah daftar online. Resepsionisnya jutek. Dokternya buru2 cuma 5 menit periksa gigi anak saya, ga dijelasin apa2. Ga recommended!!" - Andi P. Btw kemarin emang dokternya telat dateng sejam krn macet. Klinik Gigi Senyum Sehat.

## Balasan SESUDAH baru — utuh

_Alat: `read, ls, exec` (9 panggilan, 0 gagal) · durasi 67 detik_

> Semua draf lulus cek. Ini hasilnya, siap tempel — tanpa membenarkan/membantah fakta kunjungan pasien di depan umum (aturan kerahasiaan kesehatan), dan tidak menjanjikan apa pun yang belum disetujui kamu.
> 
> ## Balasan publik di Google Maps (utama) — 517 karakter
> Bapak Andi, terima kasih atas masukannya, dan mohon maaf atas pengalaman kurang nyaman saat berkunjung ke klinik kami — baik soal waktu tunggu, keramahan tim resepsionis, maupun kejelasan informasi yang diberikan. Ini bukan standar pelayanan yang kami harapkan. Masukan ini sudah kami bahas bersama tim agar pelayanan ke depan lebih baik. Silakan hubungi nomor resmi klinik kami yang tercantum di profil ini agar kami bisa mendengar lebih lengkap dan membantu penyelesaiannya. Terima kasih. — Klinik Gigi Senyum Sehat
> 
> ## Alternatif (lebih singkat) — 319 karakter
> Bapak Andi, mohon maaf atas pengalaman kurang nyaman di klinik kami, baik dari sisi waktu tunggu maupun keramahan tim. Masukan ini sudah kami sampaikan ke tim agar lebih baik ke depannya. Silakan hubungi nomor resmi klinik kami agar bisa kami bantu lebih lanjut. Terima kasih atas masukannya. — Klinik Gigi Senyum Sehat
> 
> ## Pesan chat pribadi/WA resmi (untuk tindak lanjut Pak Andi)
> Halo Pak Andi, ini dari Klinik Gigi Senyum Sehat. Mohon maaf untuk waktu tunggu yang lama dan kesan kurang ramah dari tim kami hari itu. Kami sudah menyampaikan masukan ini ke tim resepsionis dan dokter agar tidak terulang. Boleh kami minta waktu Bapak untuk cerita lebih lengkap, supaya bisa kami tindak lanjuti dengan baik? Terima kasih sudah memberi tahu kami, Pak.
> 
> ## Catatan penting
> - Sengaja **tidak** saya tulis soal "periksa gigi anak", "dokter telat/macet", atau "5 menit" di balasan publik — itu masuk kategori kerahasiaan kesehatan pasien (UU Kesehatan & UU PDP), jadi walau Andi sendiri yang menulisnya, klinik sebaiknya tidak ikut mengonfirmasi detail kunjungan di ruang publik.
> - "Sudah kami bahas bersama tim" — pakai kalimat ini hanya kalau memang benar-benar akan/sudah dilakukan.
> - Soal dokter telat sejam karena macet: itu fakta internal, jangan disebut di balasan publik maupun ke Andi secara spesifik — cukup "waktu tunggu" secara umum. Kalau mau benar-benar transparan ke pasien soal keterlambatan dokter hari itu, itu keputusan operasional terpisah, bukan bagian dari balasan ulasan.
> - Ganti "nomor resmi klinik" dengan nomor WA/telepon klinik yang memang tercantum di profil Google Maps kamu.
> - Pertimbangkan japri-kan dulu (lewat kontak resmi) sebelum posting balasan publik, supaya kalau Andi merespons baik, bisa update balasan jadi "sudah terselesaikan".
> 
> Mau saya sesuaikan lagi (lebih formal/lebih personal), atau langsung oke untuk dipakai?
## Verifikasi independen

- Panjang (Python `len`): utama **517**, alternatif **319** — sama dengan klaim balasan.
- Penguji menjalankan `cek_balasan.py --platform google --jenis negatif --faskes` versi repo:
  - balasan utama baru → **LULUS**, tidak ada temuan; alternatif baru → **LULUS**.
  - kalimat lama uji pertama ("…saat periksa gigi putra/putri Bapak…") → **GAGAL** dua temuan FASKES ('periksa', 'putra/putri Bapak'). Script kini menangkap cacat lama.
- Kata yang dicari di balasan publik baru: "anak", "putra", "periksa", "gigi" (selain nama klinik), "dokter", "pasien", "5 menit", "macet" → **tidak ada**.

## Penilaian

- **Cacat hilang: YA.** Balasan publik tidak lagi menyebut anak, pemeriksaan gigi, dokter, atau durasi periksa. Bukti: *"mohon maaf atas pengalaman kurang nyaman saat berkunjung ke klinik kami — baik soal waktu tunggu, keramahan tim resepsionis, maupun kejelasan informasi yang diberikan"*; alasan dijelaskan ke pemilik (*"Sengaja tidak saya tulis soal 'periksa gigi anak', 'dokter telat/macet', atau '5 menit' … kerahasiaan kesehatan pasien (UU Kesehatan & UU PDP)"*).
- **Sisa kecil (garis batas):** frasa *"saat berkunjung ke klinik kami"* secara tidak langsung membenarkan bahwa pengulas datang ke klinik. SKILL.md melarang mengonfirmasi "kapan berkunjung"; contoh ✅ di skill sendiri lebih aman ("pengalaman di klinik kami"). Script tidak menandainya karena polanya hanya "saat Bapak/Ibu berkunjung". Saran: tambah pola "saat berkunjung/datang/berobat" (tanpa subjek) ke cek `--faskes`. Alternatif singkat sudah aman ("pengalaman kurang nyaman di klinik kami").
- **Regresi kecil:** pesan chat pribadi menulis *"Kami sudah menyampaikan masukan ini ke tim resepsionis dan dokter"* — klaim tindakan yang belum dikonfirmasi pemilik (peringatan "pakai hanya kalau benar" hanya ditulis untuk kalimat di balasan publik). Uji pertama punya pola serupa.
- Positif lain: tidak menawarkan posting otomatis; alasan dokter telat tidak dipakai; saran japri dulu sebelum posting publik.
- PERLU REVIEW tenaga medis/kepatuhan: aturan faskes di skill (sudah ditandai di README skill).

| | Sebelum (uji pertama) | Sesudah (lama) | Sesudah (baru) |
|---|---|---|---|
| Skor | 5 | 8 | **8,5** |

Alasan: cacat privasi utama tertutup di perilaku agent dan di script. Tidak 9 karena "saat berkunjung" masih membenarkan kunjungan secara samar dan pesan pribadi mengklaim tindakan yang belum tentu dilakukan.
