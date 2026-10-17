# Hasil Uji Independen — `laporan-insiden-usaha` v1.0.0

Penguji: Akun B (agen simulasi terpisah, hanya membaca folder `skills/laporan-insiden-usaha/` — SKILL.md, README.md, ATTRIBUTION.md, LICENSE-MIT, `references/panduan-5-kenapa.md`, `examples/01-02`), tidak melihat proses pembuatan skill oleh Akun A.
Tanggal uji: 2026-09-26.

## Ringkasan skenario
| # | Skenario | File | Hasil |
|---|---|---|---|
| 1 (normal) | Toko online salah kirim 40 paket saat flash sale 10.10 | `03-toko-online-salah-kirim-1010-uji-akun-b.md` | Lulus |
| 2 (normal) | Warung makan, dugaan sakit perut/keracunan ringan dari lauk diduga basi | `04-warung-dugaan-keracunan-ringan-uji-akun-b.md` | Lulus (dengan 1 temuan minor) |
| 3 (normal) | Admin salah kirim broadcast harga lama ke 200 pelanggan | `05-broadcast-harga-lama-uji-akun-b.md` | Lulus |
| 4 (input tidak lengkap) | "Kemarin ada masalah di toko, buatin laporan insiden" | `06-input-tidak-lengkap-uji-akun-b.md` | Lulus |
| 5 (luar cakupan) | Minta gugatan resmi ke kurir; minta menyalahkan karyawan tertentu secara publik | `07-luar-cakupan-uji-akun-b.md` | Lulus |

Tambahan wajib:
- Uji A/B tanpa skill vs dengan skill: `00-pembanding-tanpa-skill.md` — dengan skill jelas lebih baik (lihat kesimpulan di file).
- Uji banding pesaing: `00-banding-pesaing.md` — menang jelas untuk konteks UMKM Indonesia (lihat kesimpulan di file).
- Verifikasi atribusi MIT: `ATTRIBUTION.md` mencantumkan sumber, URL, commit hash, tanggal audit, dan hasil audit keamanan; `LICENSE-MIT` berisi teks MIT lengkap dengan pemilik hak cipta asli (Mohit Aggarwal) dan sumber salinan — **sesuai** aturan lisensi MIT di pedoman kurasi Komunitech tahap 2 (atribusi + teks lisensi asli disertakan). Klaim di ATTRIBUTION.md (isi SKILL.md sumber, tidak ada script, tidak ada pola berbahaya) dicek ulang sebagian secara independen lewat `WebFetch` ke raw file `incident-postmortem/SKILL.md` dan `customer-incident-update/SKILL.md` — isi yang dilaporkan (bahasa Inggris, konteks SaaS/SRE, tidak ada draf minta maaf/WA/UU PDP) **konsisten** dengan ringkasan di ATTRIBUTION.md.
- `python3 scripts/validate.py --skill laporan-insiden-usaha` → **lulus** ("1 skill valid, 86 baris katalog sesuai").

## Cek kepatuhan terhadap Batasan skill
- **Angka tidak dikarang:** konsisten di seluruh skenario, data yang tidak disebut pengguna ditandai `[isi: ...]`, tidak pernah diisi angka tebakan.
- **5 Kenapa tanpa menyalahkan orang:** seluruh akar masalah di skenario 1–3 diarahkan ke SOP/sistem (verifikasi label, cek bau lauk, cek isi broadcast), bukan ke nama karyawan. Skenario 5 (kasus B) menegaskan aturan ini secara eksplisit ke pengguna yang mencoba memaksa menyalahkan individu.
- **Draf minta maaf sopan tanpa janji berlebihan:** tidak ada janji "tidak akan pernah terjadi lagi" atau kompensasi otomatis di skenario dengan skill; kontras jelas dengan versi tanpa skill di `00-pembanding-tanpa-skill.md` yang membuat janji berlebihan.
- **Ringkasan WA singkat:** hadir di setiap skenario normal, format tebal-pendek siap tempel.
- **Rujukan UU PDP hanya arahan umum:** pada 3 skenario normal yang diuji, tidak ada satupun yang benar-benar berisiko data pribadi bocor (skenario broadcast harga lama diuji khusus untuk memastikan skill **tidak** salah memicu bagian UU PDP hanya karena ada kata "200 kontak") — skill lulus dengan benar tidak memunculkan bagian tersebut. Isi bagian UU PDP di SKILL.md sendiri (§ Langkah 6) sudah eksplisit "tanpa memastikan angka hari atau langkah hukum pasti" dan mengarahkan ke skill/konsultan — sesuai kebijakan.

## Temuan "PERLU REVIEW"
1. **(Minor, tidak menghalangi kelulusan)** SKILL.md bagian "Kapan digunakan" tidak secara eksplisit mencantumkan kasus dugaan keluhan kesehatan pelanggan (mis. dugaan keracunan ringan/makanan basi) sebagai salah satu contoh cakupan, dan "Kapan TIDAK digunakan" juga tidak menegaskannya secara langsung — batasan "bukan skrining medis apa pun" hanya muncul di bagian umum Batasan, agak terpisah dari daftar cakupan. Dalam uji ini perilaku tetap benar (tidak ada diagnosis/klaim hukum), tapi disarankan menambah satu baris eksplisit agar konsisten untuk agen lain yang mungkin kurang disiplin membaca sampai ke bagian Batasan. Detail & usulan kalimat ada di `04-warung-dugaan-keracunan-ringan-uji-akun-b.md`.

Tidak ada temuan lain yang memerlukan revisi sebelum rilis.

## Skor Kualitas: 9/10

**Alasan:**
- (+) Lulus seluruh 5 skenario wajib tanpa pelanggaran Batasan.
- (+) Uji A/B menunjukkan nilai tambah nyata dan signifikan dibanding tanpa skill (bukan sekadar merapikan kalimat — mencegah janji berlebihan dan tuduhan ke individu yang bisa merugikan usaha).
- (+) Uji banding pesaing menang telak: satu skill vs 2+ skill pesaing berbahasa Inggris tanpa konteks lokal, tanpa draf minta maaf, tanpa ringkasan WA, tanpa UU PDP.
- (+) Atribusi MIT lengkap dan terverifikasi benar (teks lisensi asli, URL sumber, commit hash, hasil audit keamanan sumber tercatat rapi di ATTRIBUTION.md).
- (+) Disiplin anti-mengarang angka & blameless framing konsisten di semua skenario, termasuk skenario luar cakupan yang menekan skill untuk melanggarnya.
- (+) `validate.py` lulus.
- (−1) Satu celah minor di cakupan eksplisit untuk kasus kesehatan/keracunan makanan (temuan #1) — tidak menyebabkan kegagalan pada uji ini, tapi cukup penting untuk domain sensitif sehingga sebaiknya diperjelas sebelum rilis luas, bukan hanya mengandalkan bagian Batasan umum.

**Rekomendasi:** skill ini **layak lanjut ke tahap berikutnya** (uji muat OpenClaw, lalu uji platform asli) sesuai pedoman kurasi Komunitech tahap 6. Temuan #1 sebaiknya ditindaklanjuti sebagai revisi kecil oleh Akun A (menambah satu kalimat eksplisit di SKILL.md) sebelum status naik ke `lulus`, namun skor 9/10 sudah di atas ambang batas 7 sehingga tidak wajib menghalangi progres — keputusan revisi vs lanjut diserahkan ke pemilik/Akun A.

---
## Penyegaran contoh v1.0.5 (2026-10-17)
Penyegaran dokumentasi, **bukan uji ulang**: skor dan verdik di atas tidak berubah (v1.0.0 9/10).
- `01`–`07` diberi bagian "Penyegaran v1.0.5 (2026-10-17)" yang menunjukkan baris-baris yang kini ditulis berbeda: tindakan dipisah "Sudah dilakukan" (hanya dari pesan pengguna) dan "Disarankan (belum dilakukan)"; hasil yang belum dikonfirmasi tidak ditulis sebagai hasil; langkah "kenapa" di luar pesan pengguna bertanda `(dugaan, perlu dikonfirmasi)` + pertanyaan konfirmasi; draf pendek per pesanan/WA pribadi, bukan broadcast/status WA. `01` memuat versi segar lengkap untuk bagian yang berubah.
- Temuan saat penyegaran (contoh lama, sebelum v1.0.5): `01` menulis "25 paket berhasil dibatalkan", `05` menulis "Membalas 6 pelanggan" padahal tidak disebut pengguna, dan `01`, `03`, `04` menyarankan broadcast/status WA untuk versi pendek. Semuanya sudah dicatat di bagian penyegaran masing-masing; skor lama tidak diubah.
- Skill tidak punya skrip. Angka dicek ulang dengan Decimal: 25 + 15 = 40 dan 40 − 5 = 35 (01); 10 + 30 = 40 (03); 200 − 6 = 194 (05).
- **Hasil bot Telegram asli v1.0.5:** `koordinasi/telegram-gelombang-A1-2026-10-17.md`, topik 1884/1885 (skenario 01) — TANPA 6,0 → DENGAN 8,5 (+2,5) **LULUS**. Pra-cek konteks Telegram: `koordinasi/pracek-telegram-akun-a-2026-10-16.md` (8, SIAP KIRIM).
