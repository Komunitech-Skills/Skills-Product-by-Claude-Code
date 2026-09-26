# Hasil Uji Independen (Akun B) — `grist-usaha` v1.0.0

**Penguji:** sesi terpisah, hanya membaca folder `skills/grist-usaha/` (disalin ke
scratchpad terisolasi, dijalankan dari sana). **Docker tidak tersedia** di sandbox ini (dicek:
`docker version` OK tapi daemon tidak jalan — `dial unix /var/run/docker.sock: no such file`);
`npx grist-core` juga tidak ada di registry npm publik (grist-core didistribusikan lewat Docker
image/git, bukan paket npm siap-`npx`). Diputuskan dalam ~10 menit untuk lanjut dengan **server
REST tiruan** (ditulis ulang sendiri, bukan menyalin punya pembuat) dan file **`.grist` tiruan**
independen — sama seperti keterbatasan yang dihadapi pembuat, dicatat apa adanya.

## Skor: **7/10**

Naik dari draft pembuat (6/10) karena Tahap 6 sekarang **lengkap**: penguji independen (bukan
pembuat), uji A/B, uji banding pesaing, 5 skenario dengan data & fixture baru, dan verifikasi
angka independen — semua lulus dengan hasil fungsi **benar**. Ditahan di 7 (bukan lebih tinggi)
karena satu overclaim dokumentasi + satu celah UX yang harus diperbaiki dulu (di bawah), dan
karena **belum ada uji terhadap Grist sungguhan** (masih tiruan di kedua sisi, pembuat & penguji).

## Temuan berprioritas

1. **[TINGGI, harus diperbaiki sebelum rilis] Overclaim di README/CLAUDE.md soal format Rupiah.**
   Contoh "Rp 1,25jt" disebut sebagai format yang "dirapikan otomatis", tapi diuji langsung:
   `_bersihkan_angka("Rp 1,25jt")` → `None` (tidak dikonversi). Regex `ANGKA_RP` tidak menerima
   singkatan "jt"/"rb"/"ribu"/"juta" yang lazim dipakai UMKM. Perbaiki salah satu: (a) tambah
   dukungan parsing singkatan itu di `_bersihkan_angka`, atau (b) hapus/ganti contoh di
   README.md & materi jualan supaya tidak menjanjikan kemampuan yang tidak ada. Lihat
   `examples/03-rekap-operasional-csv.md` temuan #1.

2. **[SEDANG] `bersihkan-csv`: satu sel gagal parse membatalkan konversi SATU KOLOM PENUH tanpa
   menyebut baris mana.** Perilaku "all-or-nothing per kolom" aman (tidak ada angka salah
   diam-diam), tapi pesan tidak menunjuk baris penyebab — pengguna awam bisa bingung kenapa
   kolom Rupiahnya tetap Text. Rekomendasi: sebutkan contoh baris pertama yang gagal parse per
   kolom. Lihat `examples/03-rekap-operasional-csv.md` temuan #2.

3. **[RENDAH, catatan saja] Kolom rumus tidak dibuat otomatis lewat REST API** — sudah
   didokumentasikan jujur di SKILL.md (belum diverifikasi terhadap server sungguhan), bukan bug,
   tapi berarti 1 langkah manual tambahan tiap pola tabel dengan rumus. Tidak menahan skor.

4. Semua 50 test regresi bawaan (`tests/uji_regresi.py`) **lulus** dijalankan ulang di
   lingkungan penguji. `python3 scripts/validate.py --skill grist-usaha` dari root repo:
   **lulus** (`✅ 1 skill valid, 77 baris katalog sesuai.`).

## Ringkasan cakupan uji (lihat masing-masing file `examples/` untuk detail & bukti)
- `00-pembanding-tanpa-skill.md` — A/B: skill unggul jelas (mencegah risiko tulis tidak sengaja,
  filter tabel internal Grist otomatis, jauh lebih cepat).
- `00-banding-pesaing.md` — pesaing publik `grist-mcp-server` (~3 bintang, tidak lolos ambang
  bukti pemakaian) dinilai kalah jauh: butuh setup manual, tidak berkonteks Indonesia, tidak bisa
  baca `.grist` tanpa Grist menyala.
- `01` (stok opname toko, fixture independen 8 barang) — sisa stok & status HABIS/MENIPIS/AMAN
  diverifikasi manual, **cocok 100%**, termasuk kasus tepi batas=0 dan sisa pas di bawah batas.
- `02` (CRM/Pelanggan via REST API tiruan independen) — pratinjau vs `--ya` bekerja benar,
  dipastikan tidak ada request terkirim sebelum `--ya`.
- `03` (rekap operasional, CSV Rupiah campur format) — pembersihan angka diverifikasi manual
  100% cocok untuk format yang didukung; menemukan overclaim & celah UX di atas; impor CSV ke
  server tiruan berhasil, penolakan nama kolom tidak sah sebelum kirim terverifikasi.
- `04` (5 varian input tidak lengkap/ambigu) — semua ditangani dengan pesan jelas.
- `05` (5 varian di luar cakupan/berisiko: server internet tanpa izin, server internet tanpa
  HTTPS meski diizinkan, kunci berizin longgar, minta hitung PPN, minta tulis SQL langsung) —
  semua ditolak/diarahkan dengan aman; dipastikan tidak ada jalur kode yang menulis ke file
  `.grist` sama sekali.

## Rekomendasi status
**Belum layak `lulus`** sampai temuan #1 (overclaim README) diperbaiki — setelah itu, dengan
Tahap 6 kini lengkap secara prosedural, skill ini layak naik ke `uji`/`lulus` (skor 7/10),
menunggu giliran uji Grist sungguhan (Docker/Desktop) & uji platform asli sesuai rekomendasi
pembuat di `examples/uji-pembuat/UJI-PEMBUAT-v1.0.0.md`.

---

## Uji ulang independen v1.0.2 (Akun B, 2026-09-26)

**Skor: 8/10.** Rincian: `examples/06-angka-dan-skenario-uji-ulang-v102-akun-b.md`.

- **Temuan U17 beres.** `_bersihkan_angka` menghasilkan `Decimal` persis untuk `1,25jt`, `2,5 rb`,
  `Rp 1.250.000,-`, `10k`, `1,5M`, `miliar/milyar`, negatif, `3 jt 500 rb`; nilai ambigu
  (`1.500rb`, `2m`, `3jt500`, `1.23.456`, `1kg`) → `None` + alasan; 20 digit tidak dibulatkan;
  kolom sebagian gagal menyebut baris, nilai & alasan (layar + `--json`).
- 68 variasi tulisan angka diuji dengan ekspektasi Decimal sendiri: 65 sesuai.
- **[SEDANG] Nol di depan hilang diam-diam:** `081234567890` → `81234567890`, kode barang
  `007` → `7`; kolom jadi Numeric tanpa peringatan. Bertentangan dengan
  `references/pola-tabel-umkm.md` (Telepon wajib Text). Perbaiki sebelum `lulus`.
- **[RENDAH]** `1,000`/`12,345` tanpa singkatan dibaca ribuan (terdokumentasi, tapi tidak
  konsisten dengan prinsip "ambigu = tolak"). `(1.000)`, `+500rb`, `.5jt`, `15rb/pcs`,
  `500 ribu rupiah` ditolak tanpa alasan (aman, kurang informatif).
- 5 skenario Tahap 6 (3 normal, 1 input tidak lengkap, 1 luar cakupan): semua lulus; skenario 2
  dengan catatan temuan SEDANG di atas. File `.grist` tidak berubah setelah dibaca (SHA-1 sama).
- Tes bawaan 84/84 OK; `validate.py --skill grist-usaha` ✅.
- **Rekomendasi:** perbaiki temuan SEDANG (v1.0.3) → uji ulang singkat → layak `lulus`. REST API
  masih hanya teruji terhadap server tiruan.

---

## Uji ulang independen v1.0.3 (Akun B, 2026-09-26)

**Skor: 8/10.** Penguji: sesi terpisah (bukan pembuat, bukan penguji v1.0.2). Rincian:
`examples/07-uji-ulang-v103-akun-b.md`.

- **Temuan SEDANG v1.0.2 beres.** `081234567890`, `007`, `0123`, `+62812…`, `08123456789 (WA)`
  → teks utuh + alasan; di `bersihkan-csv` kolomnya tetap Text, file hasil memuat nol depan
  persis, ada peringatan + `kolom_nol_depan`. `0`, `0,5`, `Rp 0`, `0,5jt` tetap angka; `0.500`
  ditolak ambigu.
- **Temuan RENDAH v1.0.2 beres.** `(1.000)`/`(Rp 1.250.000)` = negatif; `+500rb`, `15rb/pcs`,
  `500 ribu rupiah`, `.5jt` ditolak **dengan alasan**.
- Regresi 94 variasi (termasuk 68 kasus `06-*`) dengan ekspektasi Decimal penguji: **94/94**;
  tanpa pembulatan untuk angka 11–25 digit.
- Skenario normal ujung-ke-ujung (pelanggan + WA + omzet → `bersihkan-csv` → `impor-csv` ke
  server tiruan penguji): angka cocok, nomor WA/kode terkirim utuh, tidak ada POST sebelum
  `--ya`, kunci tidak tercetak. Luar cakupan (buka Grist ke internet via http): ditolak kode 2,
  juga saat `GRIST_ALLOW_REMOTE=1`.
- **[RENDAH–SEDANG, UX]** Kolom telepon/kode yang juga punya sel terbaca angka muncul di dua
  peringatan yang bertentangan ("benarkan sel `0812…`" vs "nol depan dijaga") — bisa mendorong
  pengguna menghapus nol depan. **[RENDAH]** kolom hanya `62…` jadi Numeric; kolom hanya `+62…`
  Text tanpa info; sel kelebihan di luar header dibuang diam-diam.
- Tes bawaan 92/92 OK; `validate.py --skill grist-usaha` ✅ (81 baris katalog).
- **Rekomendasi:** layak `lulus` (skor ≥ 7). Rapikan peringatan ganda (#1) di v1.0.4 sebelum
  `beta`/`rilis`; REST API & rumus masih perlu uji Grist sungguhan.
