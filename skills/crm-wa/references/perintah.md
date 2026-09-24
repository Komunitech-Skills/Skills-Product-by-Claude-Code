# Daftar perintah `scripts/crm.py`

Format umum: `python3 scripts/crm.py <perintah> [opsi] [--db PATH] [--json]` (Windows: `python`/`py`).
Perintah bertanda **(besar)** hanya pratinjau sampai ditambah `--ya` setelah pengguna setuju. Perintah
bertanda **(tulis)** langsung tersimpan. Lainnya hanya membaca (database dibuka read-only).

Lokasi database: `--db` → ENV `KOMUNITECH_CRM_DB` → ENV `KOMUNITECH_DATA` + `/crm/crm.db` →
`~/KomunitechData/crm/crm.db`. Cadangan: `backup-crm/` di folder yang sama. Batas tunggu database terkunci:
ENV `KOMUNITECH_CRM_TIMEOUT` (detik, default 15).

| Perintah | Kegunaan | Opsi penting |
|---|---|---|
| `init` (besar) | Buat database | `--nama-usaha`, `--pengirim`, `--sapaan` (Kak/Bapak/Ibu/`-`), `--zona WIB|WITA|WIT` |
| `info` | Lokasi, jumlah per tahap, pemeriksaan database, cadangan, beda jam komputer | — |
| `atur` (tulis) | Ubah pengaturan | `--nama-usaha`, `--pengirim`, `--sapaan`, `--zona` |
| `tambah` (tulis) | Kontak/lead baru | `--nama` (wajib), `--wa`, `--sumber`, `--label "a, b"`, `--tahap`, `--nilai`, `--kebutuhan`, `--followup`, `--catatan`, `--masuk`, `--sapaan`, `--alasan` (bila batal), `--izinkan-duplikat` |
| `ubah` (tulis) | Ubah data kontak | `--kontak`, `--nama`, `--wa` (`-` hapus), `--sumber`, `--label` (ganti semua), `--tambah-label`, `--hapus-label`, `--nilai` (`-` kosongkan), `--kebutuhan`, `--sapaan`, `--masuk`, `--izinkan-duplikat` |
| `catat` (tulis) | Catatan obrolan / pindah tahap / nilai / jadwal | `--kontak`, `--isi`, `--tahap`, `--alasan`, `--nilai`, `--followup`, `--tanpa-followup`, `--tanggal` (tanggal kejadian, default hari ini) |
| `tunda` (tulis) | Pindah jadwal follow-up | `--kontak`, `--ke` |
| `terkirim` (tulis) | Pemilik sudah mengirim pesan | `--kontak`, `--berikutnya` (`stop` = tanpa jadwal) |
| `daftar` | Daftar kontak | `--tahap aktif|terbuka|semua|<tahap>` (default aktif = baru s.d. deal), `--label`, `--sumber`, `--cari`, `--urut followup|nilai|nama|terbaru`, `--maks 50`, `--samarkan` |
| `lihat` | Detail + riwayat + draf berikutnya | `--kontak`, `--maks 20` |
| `draf` | Draf + tautan wa.me satu kontak | `--kontak`, `--pesan "<teks final>"` (tautan untuk teks yang sudah diperhalus) |
| `hari-ini` | Pengingat harian + draf | `--maks-draf 10`, `--tanpa-draf`, `--samarkan` |
| `rekap` | Rekap pipeline | `--periode`, `--bulan YYYY-MM|ini|lalu`, `--tanggal`, `--dari/--sampai`, `--rumus` |
| `cek-duplikat` | Nomor sama / nama sama | `--samarkan` |
| `gabung` (besar) | Gabung dua kontak (riwayat dipindah, kolom kosong diisi) | `--dari`, `--ke` |
| `hapus` (besar) | Hapus kontak + riwayat permanen | `--kontak` |
| `impor <file.csv>` (besar) | Impor kontak | `--sumber-default`, `--tahap-default` |
| `ekspor` | CSV untuk Excel / jembatan pengingat | `--csv` (wajib), `--format lengkap|pengingat`, `--tahap`, `--samarkan`, `--timpa` |
| `backup` | Cadangan manual / daftar | `--daftar`, `--label` |
| `restore` (besar) | Pulihkan dari cadangan | `--dari <file>` |

`--kontak` menerima kode (`K0003`, `3`), nomor WA (format apa pun), atau nama (tanpa huruf besar/kecil;
"Rina" cocok dengan "Bu Rina"). Lebih dari satu yang cocok → gagal dengan daftar `pilihan`.

## Aturan data
- **Nomor WA** → `62…` (hanya angka). `08…`, `+62…`, `0062…`, `62 0812…` (0 dibuang), `812…`. 9–12 digit setelah 62.
  Telepon kantor (bukan 628…) dan nomor luar negeri (`+60…`) diterima dengan peringatan. Ditolak: huruf, dua nomor
  dalam satu sel, angka ilmiah Excel, jumlah digit tidak wajar. Tampilan: `0812-0000-1234`; disamarkan `0812-****-1234`.
- **Nilai**: `450rb`, `4,5 jt`, `4,275 jt`, `4.500.000`, `Rp4.500.000,-`, `4 jt 500 rb`, `1,2 M` (M besar = miliar). Ditolak:
  `5m`, `1.500 jt`, `4,5` tanpa satuan, negatif. Disimpan rupiah bulat.
- **Tanggal** (urutan hari/bulan): `2026-10-03`, `3/10/2026`, `3/10`, `3 Okt`, `tgl 3`, `besok`, `lusa`, `Jumat`,
  `Senin depan`, `3 hari lagi`, `+3`, `2 minggu lagi`, `minggu depan` (+7), `bulan depan`. Follow-up tanpa tahun yang
  baru lewat ≤ 60 hari → ditolak (tanya maksudnya); lewat > 60 hari → tahun depan. Tanggal kejadian (`--tanggal`,
  `--masuk`) tidak boleh di masa depan.
- **Sumber baku**: Instagram, TikTok, TikTok Shop, Facebook, Shopee, Tokopedia, Lazada, Marketplace lain, WhatsApp
  langsung, Referensi, Walk-in, Website/Google, Iklan, Pameran/Event, Pelanggan lama. Lainnya disimpan apa adanya.
- **Alasan batal baku**: harga terlalu mahal, tidak ada respon, pilih penjual lain, belum butuh, belum ada dana,
  stok/layanan tidak tersedia, hanya bertanya. Lainnya disimpan apa adanya (huruf kecil).
- **Tanggal deal** = tanggal kontak pertama kali masuk deal/selesai (dari `--tanggal`, default hari ini). Kontak yang
  ditambahkan/diimpor langsung sebagai deal/selesai: tanggal deal = tanggal masuk. Mundur ke tahap terbuka →
  tanggal deal dihapus.

## Irama follow-up & jenis draf
| Tahap | Pesan ke- (`fu_ke`) | Jenis draf | Setelah `terkirim` |
|---|---|---|---|
| baru | – | `sapaan-awal` | tahap → dihubungi, follow-up +2 hari |
| dihubungi | 0 / 1 / 2 | `follow-up-1` / `pilihan-mudah` / `pamit` | +3 hari / +4 hari / berhenti + saran batal "tidak ada respon" |
| ditawar | 0 / 1 / 2 | `follow-up-penawaran` / `pilihan-mudah` / `pamit` | sama seperti dihubungi |
| deal | 0 / ≥1 | `konfirmasi-order` / `pengingat-order` | +2 hari (tidak pernah pamit) |
| selesai | 0 / ≥1 | `terima-kasih` / `tawaran-ulang` | tanpa jadwal kecuali `--berikutnya` |
| batal | – | tidak ada | `terkirim` ditolak |

Pindah tahap mengembalikan `fu_ke` ke 0. Draf tidak pernah memuat nilai/harga dan catatan pribadi; sapaan: nama
yang sudah diawali Bu/Pak/Kak/Mas/Mbak/dll. dipakai apa adanya, nama lembaga (PT/CV/Toko/...) → "Bapak/Ibu di …",
selain itu sapaan default (`Kak`).

## Rumus rekap (juga di `rekap --rumus`)
- Posisi saat ini = jumlah kontak & jumlah nilai per tahap untuk semua kontak. Pipeline terbuka = baru + dihubungi + ditawar.
- Lead masuk = kontak dengan tanggal masuk di periode.
- Deal baru = kontak deal/selesai yang tanggal deal-nya di periode; nilai = Σ nilai (kontak tanpa nilai dihitung
  jumlahnya saja, disebut "belum diisi nilainya").
- Konversi = lead masuk periode yang kini deal/selesai ÷ lead masuk periode × 100%.
- Win rate = deal/selesai ÷ (deal/selesai + batal) dari lead masuk periode.
- Persen dihitung pecahan persis lalu dibulatkan sekali ke 1 desimal (0,05 ke atas).
- Rata-rata nilai deal = Σ nilai deal baru ÷ jumlah deal baru bernilai, dibulatkan ke rupiah terdekat (0,5 ke atas).
- Lama closing = rata-rata (tanggal deal − tanggal masuk) hari, 1 desimal.
- Sumber terbaik = nilai deal terbesar dari lead masuk periode; seri → konversi lebih tinggi → lead lebih banyak.
  < 5 lead → `sampel_kecil: true`.

## Kontrak JSON `rekap --json` (untuk `laporan-harian-usaha` dan alat lain)
Stabil selama `skema_json` = 1. Tidak memuat nomor HP atau nama kontak (`data_sensitif: false`).
```json
{
  "ok": true, "mode": "baca", "aplikasi": "crm-wa", "versi": "1.0.0", "skema_json": 1,
  "zona": "WIB", "hari_ini": "2026-09-24",
  "periode": {"nama": "bulan September 2026", "dari": "2026-09-01", "sampai": "2026-09-30"},
  "posisi": {"baru": {"jumlah": 0, "nilai": 0}, "dihubungi": {}, "ditawar": {}, "deal": {}, "selesai": {}, "batal": {},
             "pipeline_terbuka": {"jumlah": 0, "nilai": 0}, "total_kontak": 0},
  "periode_ini": {"lead_masuk": 0,
                  "deal_baru": {"jumlah": 0, "nilai": 0, "tanpa_nilai": 0, "rata_nilai": null, "rata_hari_closing": null},
                  "batal": 0,
                  "kohort": {"lead": 0, "deal_atau_selesai": 0, "batal": 0, "masih_berjalan": 0},
                  "konversi_persen": null, "konversi_teks": "-", "win_rate_persen": null, "win_rate_teks": "-"},
  "sumber": [{"sumber": "Instagram", "lead": 0, "deal": 0, "batal": 0, "nilai_deal": 0,
              "konversi_persen": 0.0, "konversi_teks": "0,0%"}],
  "sumber_terbaik": null,
  "alasan_batal": [{"alasan": "harga terlalu mahal", "jumlah": 1}],
  "followup": {"terlambat": 0, "hari_ini": 0, "besok": 0, "belum_dijadwalkan": 0, "nilai_terlambat_dan_hari_ini": 0},
  "rumus": {}, "teks": "REKAP CRM ...", "data_sensitif": false
}
```
Contoh pemakaian harian: `crm.py rekap --db <snapshot> --tanggal 2026-09-24 --json` (lead masuk & deal hari itu +
posisi & follow-up saat ini). Mingguan: `--dari 2026-09-14 --sampai 2026-09-20`. Database tidak ada → kode keluar 1
dengan `belum_ada: true`; rusak → `rusak: true`; terkunci → pesan "sedang dipakai program lain".

## Kolom CSV
Impor (judul kolom bebas, dikenali otomatis; urutan bebas; pemisah `;` `,` atau tab; UTF-8/BOM/ANSI):
`nama` (atau First Name + Last Name), `no wa`/`hp`/`telepon`/`phone`/`Phone 1 - Value`, `sumber`, `tahap`/`status`,
`nilai`, `kebutuhan`/`produk`, `label`/`tag`, `catatan`, `follow up`, `tgl masuk`, `alasan batal`, `sapaan`.
Baris bermasalah dan duplikat (terhadap database atau di dalam file) dilewati dan disebut nomor barisnya.
Tanda `'` pelindung dari ekspor dibuang saat impor ulang.

Ekspor `lengkap`: `kode;nama;no_wa;link_wa;sumber;label;tahap;nilai;kebutuhan;followup;alasan_batal;tgl_masuk;tgl_deal;kontak_terakhir`
(UTF-8 BOM, `;`). Sel teks diawali `=`, `+`, `-`, `@`, tab → diberi `'` agar tidak dijalankan sebagai rumus Excel.
Ekspor `pengingat`: `jenis;nama;tanggal;nominal;perihal;kode_crm` (tanpa nomor HP) + JSON `perintah_pengingat`.
