# Catatan pembuat — laporan-harian-usaha v1.1.1 (perawatan, 2026-09-26)

- **Peran:** pembuat/perevisi skill, **bukan** penguji independen. Menindaklanjuti temuan rendah/kosmetik yang
  tersisa di `examples/HASIL-UJI.md` (uji ulang v1.0.1 dan uji v1.1.0). `HASIL-UJI.md` **tidak diubah**.
- **Lingkungan:** Linux, Python 3.11, `TZ=Asia/Jakarta`. Data reproduksi dibuat di scratchpad (bukan repo) dengan
  generator yang sama dengan `tests/uji_regresi.py` (script resmi kasir-lokal, buku-stok, absensi-lokal,
  pengingat-follow-up, crm-wa). Semua nama/nomor fiktif.
- **Tidak ada fitur baru** dan **tidak ada definisi angka yang diubah** (omzet, uang diterima, rata-rata per nota,
  persen, stok, kehadiran, tagihan, seluruh angka PROSPEK). Bukti: JSON `penjualan`/`stok`/`kehadiran`/`tagihan`/
  `prospek`/`periode`/`alat` dari v1.1.0 vs v1.1.1 dibandingkan pada 3 set data × 4 mode (harian, mingguan,
  `--samarkan`, minggu berjalan) → **12/12 identik**. Yang berubah hanya butir `PERLU PERHATIAN` dan teksnya.
- `python3 tests/uji_regresi.py`: **53 tes OK** (47 lama + 6 baru). Keenam tes baru **gagal** bila dijalankan terhadap
  `laporan.py` v1.1.0 (diverifikasi di salinan scratchpad), jadi benar-benar menjaga regresi.

## Daftar temuan sisa sebelum perawatan ini
| ID | Asal | Keparahan | Status di v1.1.0 | Keputusan v1.1.1 |
|---|---|---|---|---|
| S2 | uji v1.1.0 | Sedang | Sudah diperbaiki di commit v1.1.0 (label "termasuk dari prospek lama" / "Konversi prospek baru") | — |
| N1 | uji ulang v1.0.1 | Rendah | Terbuka | **Diperbaiki** |
| N2 | uji ulang v1.0.1 | Rendah | Terbuka | **Diperbaiki** |
| N3 | uji ulang v1.0.1 | Rendah | Terbuka | **Diperbaiki** |
| N4 | uji ulang v1.0.1 | Rendah | §0 aturan penerima sudah selaras; tersisa catatan status basi di bagian verifikasi | **Diperbaiki** (catatan status) |
| N5 | uji ulang v1.0.1 | Kosmetik | Terbuka | **Diperbaiki** |
| N6 | uji ulang v1.0.1 | Kosmetik | Terbuka | Tidak diubah (keputusan desain) |
| K1 | uji v1.0.0 | Kosmetik | Terbuka | Tidak diubah (keputusan desain) |
| N-baru | uji v1.1.0 | Rendah | Terbuka | **Diperbaiki** |
| Order perlu konfirmasi | uji v1.1.0 | Kosmetik | Terbuka | **Diperbaiki** |

## Temuan yang diperbaiki

### N1 — alarm "belum absen tanpa keterangan" sebelum jam masuk bila sebagian karyawan sudah tap
- **Reproduksi (v1.1.0):** data master + `absensi.py catat --karyawan Sari --tanggal 2026-09-25 --masuk 07.45` →
  `laporan.py --sekarang 2026-09-25T07:50+07:00` → `PERLU PERHATIAN`: "Belum absen tanpa keterangan (4): Andi, Budi,
  Rina, Joko. Tanyakan & catat izin/alpa." padahal shift baru mulai 08.00.
- **Perbaikan** (`susun_perhatian`): kondisi "sebelum jam masuk paling awal" (sudah ada untuk R2) kini juga menahan
  alarm tanpa keterangan, bukan hanya kasus "belum ada satu pun yang tap". Daftar "Belum absen (4)" di bagian
  KEHADIRAN tetap tampil apa adanya.
- **Setelah:** 07.50 → tidak ada butir kehadiran di `PERLU PERHATIAN`; 09.00 → "Belum absen tanpa keterangan (4)"
  tetap muncul (perilaku R1 terjaga). Tes: `test_n1_sebagian_tap_sebelum_jam_masuk_tanpa_alarm`.
- **Batas yang tidak diklaim:** acuannya jam masuk shift **paling awal**. Karyawan shift siang (mis. 13.00) masih
  bisa tercantum sebagai alarm antara jam masuk shift pagi dan shift siangnya. Menghitung per karyawan per shift
  berarti membaca jadwal per orang dari tabel absensi — perubahan desain, lihat bagian bawah.

### N2 — cek yang dilewati (struktur tabel berubah) tidak terlihat di teks Telegram
- **Reproduksi (v1.1.0):** salinan `stok.db` dengan `ALTER TABLE pesanan RENAME COLUMN no_pesanan TO no_psn` → JSON
  `catatan` berisi "Cek impor kasir ke buku-stok dilewati: struktur tabel pesanan berubah.", teks Telegram diam.
- **Perbaikan:** isi `catatan` ikut ditambahkan (tanpa duplikat) ke `PERLU PERHATIAN`, sehingga tampil di teks dan
  JSON `perhatian`. JSON `catatan` tetap ada.
- **Setelah:** pesan tampil tepat 1 kali di teks. Tes: `test_n2_cek_dilewati_tampil_di_teks`.

### N3 — nota di-void setelah diimpor ke buku-stok tidak diingatkan
- **Reproduksi (v1.1.0):** data master (nota 23/9 sudah diimpor) → `kasir.py void --nota N-260923-0001 --waktu
  "2026-09-24 14:00"` → laporan 24/9 tidak menyebut bahwa stok nota itu masih terpotong di buku-stok.
- **Perbaikan** (`cek_void_setelah_impor`, baru, hanya-baca di salinan): nota jual yang di-void **di periode laporan**
  dicocokkan ke `pesanan.no_pesanan` buku-stok; bila barisnya ada dan `dibatalkan` = 0 → butir perhatian dengan nomor
  nota (maks. 5) + langkah perbaikan. Cek kolom lebih dulu; bila struktur berubah → dilewati dengan catatan yang sama
  dengan cek impor (tampil sekali, lihat N2). Nota yang di-void **sebelum** diimpor tidak pernah punya baris
  `pesanan` (stok.py melewatinya), jadi tidak diingatkan.
- **Langkah perbaikan yang disarankan diverifikasi:** `kasir.py ekspor --format buku-stok --tanggal 2026-09-23` →
  `stok.py impor-pesanan ... --ya` → buku-stok mengembalikan stok (`dibatalkan`=1) → butir hilang.
- **Setelah:** "1 nota kasir di-void setelah diimpor ke buku-stok, stoknya belum dikembalikan (N-260923-0001). Ekspor
  ulang tanggal nota itu dari kasir lalu impor lagi ke buku-stok." Omzet tetap angka kasir (turun Rp 36.000 karena
  void, dihitung kasir-lokal, bukan laporan). Tes: `test_n3_void_setelah_impor_diingatkan`.

### N4 (sisa) — catatan status basi di `references/openclaw-jadwal.md`
- Aturan penerima di §0 sudah selaras dengan SKILL.md sejak v1.0.1. Yang tersisa: baris status masih menulis
  "Bagian PROSPEK belum diuji ulang lewat `automations run` sungguhan", padahal uji v1.1.0 (penguji independen,
  2026-09-25, OpenClaw 2026.9.6) sudah membuktikannya. Baris itu diganti dengan status terverifikasi + rujukan ke
  `HASIL-UJI.md`. Tidak ada klaim platform baru.

### N5 — `--samarkan` menghasilkan "J.. Tanyakan"
- **Reproduksi (v1.1.0):** data master + `--samarkan` → "Belum absen tanpa keterangan (1): J.. Tanyakan & catat
  izin/alpa."
- **Perbaikan:** titik akhir daftar nama dibuang sebelum ". Tanyakan". **Setelah:** "(1): J. Tanyakan"; tanpa
  samarkan tetap "(1): Joko. Tanyakan". Tes: `test_n5_samarkan_tanpa_titik_ganda`.

### N-baru — `--samarkan` tidak diteruskan ke `crm.py rekap`
- **Reproduksi (v1.1.0):** argv `ambil_crm()` sama dengan/tanpa `--samarkan`.
- **Perbaikan:** `--samarkan` ditambahkan ke argv bila aktif. Opsi ini ada di `rekap` sejak crm-wa versi pertama
  (dicek dari riwayat git) dan di `hitung_rekap` hanya memengaruhi `alasan_batal`, yang tidak dipakai laporan ini.
- **Setelah:** JSON `prospek` dengan/tanpa `--samarkan` identik; argv memuat `--samarkan` hanya saat diminta. Tes:
  `test_crm_samarkan_diteruskan_angka_sama`.

### Kosmetik v1.1.0 — order (deal) perlu konfirmasi tidak jadi butir perhatian
- **Reproduksi (v1.1.0):** `crm.py catat --kontak "Mas Andi" --followup 2026-09-24` (kontak deal) → PROSPEK "order
  perlu konfirmasi 1", `PERLU PERHATIAN` tanpa butir.
- **Perbaikan:** butir "N order (deal) sudah waktunya dikonfirmasi ke pelanggan. Ketik 'follow-up hari ini' ..."
  memakai angka `followup.order_perlu_konfirmasi` apa adanya dari `crm.py rekap --json` (definisi crm-wa: jadwal
  konfirmasi hari ini atau sudah lewat). Tes: `test_order_perlu_konfirmasi_di_perhatian`.

## Tidak diperbaiki (butuh keputusan desain)
- **N6** — void lintas hari: "Nota: 5 (+2 dibatalkan)" vs butir impor "6 dari 6 nota". "Nota sah" dan rata-rata per
  nota = nota jual − nota void **pada hari void** (angka kasir-lokal yang sudah diverifikasi). Menyamakan keduanya
  berarti mengubah definisi rata-rata per nota atau cek impor. Perlu keputusan pemilik.
- **K1** — `--samarkan` bentrok untuk nama berawalan sama (mis. "Sari" & "Sinta" → "S."). Pilihan penanganan
  (dua huruf, nomor urut, kode karyawan) mengubah format keluaran privasi. Perlu keputusan.
- **N1 per-shift** — acuan jam masuk per karyawan (bukan shift paling awal), lihat batas N1 di atas.

## Perintah yang dijalankan
- `python3 skills/laporan-harian-usaha/tests/uji_regresi.py` → 53 tes OK.
- Tes yang sama terhadap `laporan.py` v1.1.0 (salinan scratchpad) → 6 gagal, tepat tes baru.
- `python3 scripts/validate.py` → lolos.
