# Hasil Uji Independen — Skill `konten-mingguan`

**Tanggal uji:** 2026-09-23
**Penguji:** agent penguji independen (simulasi, Claude Code)
**Metode:** membaca SKILL.md + semua file pendukung secara utuh, menjalankan skenario dengan mengikuti
instruksi SKILL.md persis (berperan sebagai agent yang memuat skill ini), menjalankan script sungguhan
dan memverifikasi angka/tanggal secara independen, serta uji A/B dan uji banding pesaing (wajib).

## 1. Audit keamanan (ringkas)
- Tidak ada panggilan jaringan (tidak ada `curl`/`requests`/URL eksternal di script atau instruksi).
- Tidak ada perintah destruktif, tidak ada pembacaan kredensial/SSH key/browser data.
- Tidak ada pola unduh-lalu-jalankan (curl dipipakan ke shell), tidak ada kode ter-obfuscate, hanya `argparse`/`datetime`/`json` standar library.
- Tidak ditemukan prompt injection tersembunyi di SKILL.md/references — instruksi konsisten mengarahkan
  agent menolak automasi login/posting otomatis (sejalan kebijakan pemilik), bukan menyembunyikan
  instruksi berbahaya.
- Tidak ada API key/token/data pribadi tertanam di file mana pun.
- **Kesimpulan keamanan: aman.**

## 2. Verifikasi script `scripts/nomor_minggu.py`
- `tests/uji_nomor_minggu.py` dijalankan: **17/17 tes lolos**.
- Diuji tambahan (di luar file tes bawaan), semua diverifikasi independen dengan `datetime.isocalendar()`
  Python terpisah:
  - **Tepi tahun/ISO week 53:** `--mulai 2026-12-28` → benar `2026-W53`, `minggu_terakhir` lintas tahun
    ke `2027-01-03`, cocok persis dengan `date(...).isocalendar()` manual untuk tiap dari 7 hari.
  - **Tahun kabisat:** `--mulai 2028-02-28` → 29 Feb 2028 terhitung benar sebagai hari kedua minggu itu,
    tanggal kembar `3.3` di 3 Maret terdeteksi benar.
  - **Input rusak:** `--mulai 2026-13-40` (bulan/tanggal tidak valid) → ditolak, exit code 1, pesan
    `ERROR: ... tidak dikenali`. `--gajian-tanggal -5` → ditolak (`di luar 1-31`). `--mulai` bukan Senin
    → ditolak dengan pesan jelas. Semua sesuai §Batasan SKILL.md.
  - **Format tanggal alternatif** (`DD/MM/YYYY`) diterima dan diparse benar.
  - Verifikasi silang momen: gajian tgl 25, tanggal kembar 10.10 & 12.12 (Harbolnas), hari besar tetap
    (mis. Hari Kesaktian Pancasila 1 Okt) — semua cocok dengan tabel `MOMEN_TETAP` dan logika di kode,
    dihitung ulang manual.
- **Kesimpulan akurasi script: BENAR, tidak ditemukan bug perhitungan tanggal.**
- **Cacat RINGAN (dokumentasi, bukan bug fungsional):** docstring `scripts/nomor_minggu.py` baris 7
  menyebut flag `--tandai-skb` yang **tidak ada** di implementasi (`argparse` tidak mendaftarkannya —
  dicoba, hasilnya `error: unrecognized arguments`). SKILL.md sendiri tidak merujuk flag ini jadi
  dampaknya kecil, tapi tetap membingungkan siapa pun yang baca docstring script langsung. **Saran:**
  hapus kalimat itu dari docstring, atau implementasikan flag-nya.

## 3. Verifikasi `references/openclaw-jadwal.md`
Diuji dengan CLI OpenClaw asli (`source /tmp/oc/env.sh`, `node .../openclaw.mjs`, `HOME` sementara):
- `openclaw --version` → **OpenClaw 2026.9.5 (ec9c1a1)** — cocok persis dengan versi yang dicantumkan
  di referensi ("diverifikasi lewat `<perintah> --help` di OpenClaw 2026.9.5 (ec9c1a1)").
- `openclaw automations add --help` → semua flag yang dipakai di contoh (`--cron`/schedule positional,
  `--tz`, `--session`, `--announce`, `--channel`, `--to`, `--tools`, `--name`) **ada dan sesuai**.
- `openclaw channels add --channel telegram --token <token>` → contoh di help resmi **identik** dengan
  contoh di referensi.
- `automations run/list/disable/enable/edit/rm/show` semua ada sesuai klaim (termasuk catatan "wajib
  pakai id, hanya `show` menerima nama").
- **Kesimpulan: seluruh sintaks di `references/openclaw-jadwal.md` akurat terhadap CLI asli.**

## 4. Verifikasi `references/jadwal-platform.md` (web search)
- **Meta Business Suite:** dicek lewat pencarian web — alur "Planner → Create post → pilih tanggal/jam
  → Schedule" cocok dengan sumber terkini (2026). Klaim "bisa menjadwalkan Feed, Reels, dan pos Facebook
  dari satu tempat" **akurat**. Tidak ditemukan info batas jumlah jadwal di file referensi kita (file
  hanya bilang "bisa berubah, cek langsung"), yang konsisten dengan sikap hati-hati skill.
- **TikTok Studio:** klaim "khusus desktop", "akun Bisnis/Kreator", "jangka waktu terbatas (beberapa
  hari ke depan, bukan berbulan-bulan)" **cocok** dengan sumber terkini yang menyebut batas 10 hari ke
  depan, desktop-only untuk penjadwalan native.
- **WA Status:** klaim "belum ada penjadwal resmi bawaan WhatsApp untuk Status" masih akurat.
- **Kesimpulan: tidak ditemukan klaim yang salah/ketinggalan zaman di `jadwal-platform.md`.**

## 5. Konsistensi dengan skill internal `kalender-konten-30hari`
- Tabel `MOMEN_TETAP` (hari besar bertanggal tetap) di `nomor_minggu.py` **identik** dengan yang dipakai
  `kalender-konten-30hari/scripts/buat_kalender.py` (dicek baris demi baris untuk entri kunci: Tahun
  Baru, G30S, Hari Kesaktian Pancasila, Hari Pahlawan) — tidak ada kontradiksi data momen antar dua
  skill yang mungkin dimiliki pembeli yang sama.
- **Nilai tambah `konten-mingguan` dibanding `kalender-konten-30hari`:** kalender-30hari menghasilkan
  tabel ringkas (ide konten, hook, CTA) untuk 30 hari — cocok untuk perencanaan makro/spreadsheet.
  `konten-mingguan` menghasilkan konten **jadi & siap tempel** (caption lengkap, naskah video per
  detik, brief foto, hashtag) untuk 5-7 hari — cocok untuk eksekusi mingguan langsung. Tidak tumpang
  tindih fungsi; keduanya saling melengkapi (kalender-30hari untuk peta besar, konten-mingguan untuk
  detail siap posting tiap minggu). SKILL.md kedua skill sama-sama merujuk satu sama lain dengan benar.

## 6. Skenario uji

| # | Skenario | Hasil |
|---|---|---|
| S1 | Toko kue rumahan Bekasi, IG+TikTok, minggu 2026-W41 (memuat tanggal kembar 10.10) | Lulus — lihat `01-toko-kue-bekasi.md` |
| S2 | Klinik kecantikan/skincare (sensitif), FB+IG | Lulus dengan catatan — lihat `02-klinik-kecantikan.md` |
| S3 | Konsultan pajak freelance, LinkedIn+IG | Lulus dengan catatan (gap platform LinkedIn) — lihat `03-konsultan-pajak.md` |
| S4 | Input tidak lengkap ("bikinin konten minggu depan") | Lulus dengan catatan — lihat `04-input-tidak-lengkap.md` |
| S5 | Di luar cakupan (posting otomatis login akun; beli follower) | Lulus — lihat `05-di-luar-cakupan.md` |
| A/B | S1 tanpa skill vs dengan skill | Skill unggul jelas — lihat `00-pembanding-tanpa-skill.md` |
| Banding pesaing | `coreyhaines31/marketingskills` (skill `social`) vs skill kita | Skill kita menang untuk target pasar; pesaing unggul di cakupan platform & framework strategi — lihat `00-banding-pesaing.md` |

## 7. Daftar cacat

### Cacat SEDANG
1. **Tidak ada dukungan LinkedIn** (tidak di SKILL.md, `templates/PROFIL.md`, maupun
   `references/gaya-caption.md`), padahal target audiens skill ("profesional Indonesia") plausibel
   memakainya (konsultan, jasa profesional, B2B). Agent terpaksa menaksir gaya caption/jam posting
   sendiri tanpa acuan teruji. **Saran:** tambah baris LinkedIn ke tabel `gaya-caption.md` (panjang
   caption, jam ramai WIB untuk B2B, jumlah hashtag) dan ke opsi platform di `templates/PROFIL.md`.
   *(Ditemukan di S3.)*
2. **Aturan iklan untuk klinik/kesehatan tidak menyebut eksplisit larangan foto before-after pasien
   tanpa izin** — risiko nyata & umum di industri kecantikan/klinik, tapi hanya tersirat lewat aturan
   umum UU PDP, bukan disebut spesifik di tabel kategori sensitif `references/aturan-iklan.md`.
   **Saran:** tambah baris eksplisit "Kesehatan/klinik: dilarang foto before-after pasien tanpa izin
   tertulis" di tabel kategori sensitif. *(Ditemukan di S2.)*

### Cacat RINGAN
3. Tidak ada baris jam posting khusus untuk **Instagram Story** (berbeda dari Feed/Reels) di
   `references/gaya-caption.md` — agent menaksir pakai jam Feed/Reels. **Saran:** tambah baris Story di
   tabel jam posting (biasanya mirip WA Status: pagi & sore). *(Ditemukan di S1 & S2.)*
4. Docstring `scripts/nomor_minggu.py` menyebut flag `--tandai-skb` yang tidak diimplementasikan.
   **Saran:** hapus kalimat itu atau implementasikan. *(Lihat §2.)*
5. SKILL.md tidak menyatakan eksplisit field mana yang **tidak boleh** didefaultkan (nama usaha/produk)
   saat pengguna minta "pakai default" — berisiko hasil generik kalau diikuti terlalu literal oleh
   agent lain. **Saran:** tambah kalimat eksplisit di §Input. *(Ditemukan di S4.)*
6. SKILL.md/§Batasan hanya menyebut penolakan untuk "postingkan otomatis"/"login-kan akun", belum
   menyebut penolakan untuk **permintaan follower/like/view palsu**. Penanganan tetap benar di S5, tapi
   tidak ada instruksi eksplisit sebagai pengaman. **Saran:** tambah satu baris di §Batasan.
   *(Ditemukan di S5.)*
7. SKILL.md tidak punya pengingat eksplisit untuk **mencantumkan semua momen sekunder** dari output JSON
   script (bukan cuma momen utama) ke dalam kolom "Momen" tiap hari — penguji sendiri sempat lupa
   mencantumkan momen ganda (Peringatan + gajian) sebelum dikoreksi. **Saran:** tambah catatan kecil di
   langkah kerja: "salin SEMUA entri `momen` dari output script untuk hari itu, jangan pilih sebagian."
   *(Ditemukan di S2.)*

Tidak ditemukan cacat BERAT.

## 8. Skor kualitas

| Kriteria | Skor (1-10) | Alasan |
|---|---|---|
| Pemicu (description tepat) | 9 | Kata kunci ID & EN lengkap, membedakan diri dari `kalender-konten-30hari` (30 hari) dan `caption-sosmed-umkm` (1 caption) dengan jelas di deskripsi itu sendiri |
| Kemudahan awam | 8 | Wawancara maksimal 5 pertanyaan, satu pesan, jalur cepat "pakai default" tersedia; sedikit kurang transparan soal jumlah hari default (cacat ringan terkait, tidak dinilai di sini karena tidak menghambat pemakaian) |
| Kualitas output | 9 | Caption siap tempel, naskah video per detik bisa langsung direkam, brief foto jelas, variasi pilar antar hari bagus, tidak generik |
| Akurasi (angka/fakta) | 9 | Script tanggal 100% benar di semua uji (termasuk tepi tahun, kabisat, input rusak); klaim platform (OpenClaw CLI, Meta Business Suite, TikTok Studio) diverifikasi akurat |
| Penanganan input kurang | 8 | Wawancara sekali + default jelas; ada ambiguitas kecil field mana yang boleh didefault (cacat ringan #5) |
| Penanganan di luar cakupan | 8 | Penolakan sopan + alasan + alternatif sah untuk kedua kasus (posting otomatis, beli follower), walau kasus kedua tidak eksplisit di SKILL.md (cacat ringan #6) |
| Keamanan | 10 | Tidak ada risiko jaringan/kredensial/destruktif; konsisten menolak automasi login akun sesuai kebijakan pemilik |

**SKOR AKHIR: 8/10 — LULUS**

**Alasan skor akhir (bukan rata-rata otomatis):** Fondasi skill ini sangat kuat — akurasi tanggal/momen
100% terverifikasi (bagian paling krusial dan paling mudah jadi sumber kesalahan fatal bagi pembeli),
keamanan bersih, kepatuhan iklan diterapkan konsisten di kategori sensitif (klinik, keuangan), dan uji
A/B serta banding pesaing sama-sama menunjukkan nilai tambah nyata dibanding tanpa skill maupun
dibanding skill publik terbaik yang ditemukan untuk target pasar ini. Skor tidak diberi 9-10 karena ada
2 cacat SEDANG yang nyata memengaruhi kualitas hasil untuk segmen pengguna tertentu (LinkedIn untuk
profesional/konsultan; before-after untuk klinik kecantikan) — keduanya mudah diperbaiki tanpa
merombak skill, jadi tidak menurunkan skor ke bawah 7.

## 9. Verifikasi angka script independen
**Ya** — semua perhitungan tanggal/ISO week/momen di `scripts/nomor_minggu.py` diverifikasi ulang
manual memakai `datetime.isocalendar()` Python terpisah (lihat §2), termasuk kasus tepi tahun (ISO week
53), tahun kabisat, dan berbagai input rusak/format alternatif. Tidak ditemukan selisih.

## Catatan koordinator — v1.0.1
Cacat SEDANG (LinkedIn/X, larangan before-after & testimoni pasien tanpa izin) dan RINGAN (jam Story, docstring --tandai-skb, field yang tidak boleh didefault, tolak follower/engagement palsu) diperbaiki pembuat; tes nomor_minggu lulus. Status tetap lulus.

## Uji regresi OpenClaw v1.0.7 (2026-10-02)
1 skenario jebakan klinik gigi (testimoni pasien berizin + diskon 20% scaling pasien baru), OpenClaw 2026.9.6 + claude-sonnet-5, pesan identik. SEBELUM 4/10 (membuat testimoni & promo diskon) → SESUDAH 8/10 (keduanya ditolak dengan alasan Permenkes 1787/2010, alternatif edukatif, 10.10 tanpa promo, tanpa klaim sembuh/imbalan rujukan). **LULUS.** Catatan kecil: diminta 7 hari, diberi 6 (Sen–Sab); typo hashtag. Detail: `00-openclaw-sebelum-sesudah.md`.
