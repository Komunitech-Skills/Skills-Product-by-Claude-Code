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
