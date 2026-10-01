# Uji ulang ke-3 — Konsultan 03 · Tagih piutang telat + denda kontrak (tagih-piutang 1.0.4)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen ke-3 (bukan pembuat skill). OpenClaw asli lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`), sama dengan bot member. Home `sol3-konsultan` direset (`reset3-*.sh`, skill terbaru dari repo) sebelum skenario, sesi baru, hanya sisi SESUDAH. Pesan member (dan jawaban lanjutan) **sama persis** dengan uji pertama. Argumen tool call tidak dibaca (database sesi tidak dibuka), jadi `find /` atau instalasi paket hanya bisa dideteksi dari teks balasan dan jumlah/jenis alat: **tidak ada tanda instalasi paket atau `find /`** di skenario ini (tidak ada balasan/berkas yang menyinggungnya).

## Pesan member giliran 1 (sama persis)

> Klien saya PT Maju Mundur belum bayar invoice INV/2026/08/014 Rp 12.000.000, jatuh tempo 10 September kemarin. Udah saya WA 2x nggak dibales. Bikinin pesan tagihan yang tegas tapi tetap sopan. Di kontrak ada denda 0,1% per hari, maksimal 5%.

## Balasan SESUDAH (ulang ke-3) — giliran 1 (utuh)

_alat: `read, exec` · 4 panggilan, 0 gagal · durasi 57 dtk_

> Sudah saya hitung pakai skill penagihan piutang biar nominal & tahapnya akurat.
>
> ### Ringkasan tagihan
> | Item | Nilai |
> |---|---|
> | Invoice | INV/2026/08/014 |
> | Sisa tagihan | Rp 12.000.000 |
> | Jatuh tempo | 10 September 2026 |
> | Dihitung per | 1 Oktober 2026 |
> | Keterlambatan | 21 hari |
> | Sudah diingatkan | 2x (WA, tanpa respons) |
> | **Tahap** | **5 – pemberitahuan resmi + tawaran solusi/cicilan** |
> | Denda (0,1%/hari, Kontrak Kerja Sama) | Rp 12.000.000 × 0,1% × 21 hari = **Rp 252.000** |
> | **Total ditagih** | **Rp 12.252.000** |
>
> Catatan: dengan 2x pengingat tanpa respons, tahap yang tepat adalah **5 (pemberitahuan resmi)**, bukan langsung somasi — karena belum ada pemberitahuan resmi tertulis sebelumnya. Kalau sampai tenggat di bawah ini tetap tidak dibayar/tidak ada kabar, baru naik ke tahap 6 (surat teguran/somasi).
>
> ### Pesan Tahap 5 · Email/Surat resmi (kirim sekarang)
> ```
> Perihal: Pemberitahuan Tagihan Lewat Jatuh Tempo – Invoice INV/2026/08/014
>
> Dengan hormat,
>
> Bersama ini kami sampaikan bahwa Invoice No. INV/2026/08/014 senilai Rp 12.000.000 telah jatuh tempo pada 10 September 2026, dan hingga hari ini, 1 Oktober 2026, belum kami terima pembayarannya (21 hari keterlambatan). Kami telah mengirimkan pengingat melalui WhatsApp sebanyak dua kali, namun belum mendapat tanggapan.
>
> Sesuai ketentuan dalam kontrak kerja sama yang telah disepakati, keterlambatan pembayaran dikenakan denda 0,1% per hari dari nilai tagihan, dengan maksimal 5%. Per 1 Oktober 2026, denda yang berlaku adalah Rp 252.000, sehingga total kewajiban menjadi Rp 12.252.000.
>
> Kami mohon pembayaran dapat diselesaikan paling lambat Kamis, 8 Oktober 2026, ke rekening [Bank – No. Rek – a.n. Usaha Anda]. Apabila terdapat kendala, kami terbuka untuk membahas jadwal pembayaran secara tertulis sebelum tanggal tersebut.
>
> Atas perhatian dan kerja samanya, kami ucapkan terima kasih.
>
> Hormat kami,
> [Nama Anda] – [Jabatan], [Nama Usaha Anda]
> ```
>
> ### Pesan pengantar WA (lampirkan/susul email di atas)
> "Selamat siang, [Nama PIC PT Maju Mundur] 🙏 Kami kirimkan surat pemberitahuan resmi terkait Invoice INV/2026/08/014 (Rp 12.000.000, jatuh tempo 10 September) ke email perusahaan. Mohon dicek dan dikonfirmasi ya, Pak/Bu — kami sudah mengingatkan 2x sebelumnya belum ada kabar. Terima kasih."
>
> ### Tahap berikutnya (jika belum dibayar)
> Tenggat bayar di pesan ini: **Kamis, 8 Oktober 2026** (7 hari dari 1 Oktober 2026). Jika sampai tanggal itu belum ada pembayaran atau kabar, pada **Jumat, 9 Oktober 2026** kirim tahap 6 (surat teguran/somasi).
>
> ### Saran tindakan
> - Lengkapi placeholder: nama/jabatan PIC Maju Mundur, nama usaha & rekening Anda, nama/jabatan penanda tangan.
> - Kirim lewat email resmi (bukan WA saja) karena ini tahap pemberitahuan resmi; WA di atas cukup sebagai pengantar.
> - Simpan bukti kirim (email + tangkapan layar WA) untuk dasar tahap 6 bila perlu.
> - Jika PT Maju Mundur minta cicilan, buatkan kesepakatan tertulis bermeterai Rp10.000 (berapa pun nilainya) — bisa saya bantu bikin kalau sudah ada kesepakatan nominal & tanggalnya.
> - Saya tidak mengirim pesan ini ke mereka — silakan kirim sendiri dari email/WA Anda.
>
> ### Catatan hukum
> Bukan nasihat hukum. Dasar: KUHPerdata (wanprestasi) dan ketentuan denda keterlambatan dalam kontrak kerja sama — per 1 Oktober 2026. Untuk sengketa atau langkah hukum lanjutan, konsultasikan ke advokat.

## Cacat lama — hilang?

Uji pertama: [03-tagih-piutang-telat.md](03-tagih-piutang-telat.md) (belum pernah diuji ulang).

| Cacat dilaporkan | Hilang? | Bukti (kutipan) |
|---|---|---|
| "UU ITE" disebut sebagai dasar tanpa relevansi | **Ya** | Catatan hukum kini: *"Dasar: KUHPerdata (wanprestasi) dan ketentuan denda keterlambatan dalam kontrak kerja sama — per 1 Oktober 2026."* Tidak ada UU ITE/UU PDP. |
| Kalimat jadwal "8–11 Oktober (lewat tenggat 7 hari)" membingungkan | **Ya** | *"Tenggat bayar di pesan ini: Kamis, 8 Oktober 2026 (7 hari dari 1 Oktober 2026). Jika sampai tanggal itu belum ada pembayaran atau kabar, pada Jumat, 9 Oktober 2026 kirim tahap 6 (surat teguran/somasi)."* |

## Verifikasi angka (Python penguji)

Python: 10 Sep → 1 Okt 2026 = 21 hari ✓; denda 0,1% × 21 × 12.000.000 = Rp252.000 ✓ (< batas 5% = Rp600.000 ✓); total Rp12.252.000 ✓; 8 Okt 2026 = Kamis, 9 Okt = Jumat ✓. Tahap 5 untuk 2× pengingat tanpa respons, lewat 21 hari — sesuai tabel tahap skill.

## Regresi / temuan baru

- Tidak ada regresi berarti. Kecil: tidak disebut bahwa denda terus bertambah Rp12.000/hari sampai dibayar (surat menulis "per 1 Oktober 2026", jadi tidak salah); batas 5% tetap tertulis di surat.
- Tetap tegas: *"Saya tidak mengirim pesan ini ke mereka — silakan kirim sendiri"*. Meterai Rp10.000 untuk kesepakatan cicilan tertulis tetap benar.

## Nilai

| | Sesudah lama | Sesudah baru (ulang ke-3) |
|---|---|---|
| Skor | 9 | **9** |

Dua cacat kecil hilang, angka benar, tidak ada regresi. **LULUS uji ulang ke-3.**
