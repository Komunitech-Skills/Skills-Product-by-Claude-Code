# Daftar perintah `scripts/gaji.py`

Format umum: `python3 scripts/gaji.py <perintah> [opsi] [--db PATH] [--json]` (Windows: `python`/`py`).
Perintah bertanda **(besar)** hanya pratinjau sampai ditambah `--ya` setelah pemilik setuju. **(kecil)** langsung tersimpan (hanya untuk periode yang belum final). Angka boleh ditulis `6jt`, `750rb`, `Rp 5.396.761`, `4,2jt`.

| Perintah | Kegunaan | Opsi penting |
|---|---|---|
| `init` (besar) | Buat database | `--nama-usaha` |
| `info` | Lokasi database, pengaturan, pemeriksaan, versi mesin | — |
| `atur` (kecil) | Pengaturan usaha | `--nama-usaha`, `--umk`, `--jkk` (persen), `--batas-jp`, `--tanggal-gajian 1-31/akhir`, `--potongan-per-hari-alpa` + `--dasar-potongan "<pasal PK/PP/PKB>"` (`-` = hapus) |
| `karyawan tambah` (besar) | Karyawan baru | wajib `--nama --ptkp --gaji-pokok --masuk`; opsional `--kode`, `--jabatan`, `--jenis tetap/kontrak`, `--tunjangan-tetap`, `--tunjangan-tidak-tetap` (rutin tiap bulan), `--zakat`, `--bpjs kes,tk,jp/kes,tk/kes/tidak`, `--jkk`, `--hari-kerja 5/6`, `--dasar-bpjs-kesehatan`, `--dtp ya --bruto-tetap-januari`, `--nik`, `--bank`, `--rekening`, `--atas-nama`, `--kode-absensi` |
| `karyawan ubah` (besar) | Ubah data | `--karyawan <kode/nama>` + opsi di atas; `--keluar YYYY-MM-DD` (`-` batal). Nilai `-` mengosongkan NIK/rekening/bank |
| (pagar BPJS) | `tambah`/`ubah`/`impor` yang membuat karyawan tanpa BPJS Kesehatan/Ketenagakerjaan atau `--dasar-bpjs-kesehatan` di bawah upah (min. UMK, maks. 12 jt) | Pratinjau berlabel "PERLU PERSETUJUAN KHUSUS"; `--ya` saja ditolak (`masalah_kepatuhan` di JSON). Simpan hanya dengan `--ya --ya-saya-paham [--alasan-khusus "..."]` atas keputusan pemilik; dicatat di log |
| `karyawan keluar` (besar) | Catat berhenti | `--karyawan`, `--tanggal` |
| `karyawan daftar` | Daftar (NIK/rekening disamarkan) | `--semua` (termasuk yang keluar) |
| `karyawan impor <file>` (besar) | Banyak dari CSV | kolom seperti `templates/karyawan-contoh.csv`; satu baris salah → tidak ada yang disimpan |
| `isi` (kecil; `--file` besar) | Komponen bulan ini | `--bulan`, `--karyawan`, `--tunjangan-tidak-tetap`, `--lembur-hari-kerja 2+3`, `--lembur-hari-libur 8+6p`, `--lembur-rp`, `--bonus`, `--thr`, `--kasbon`/`--potongan-lain`, `--potongan-tidak-masuk`, `--zakat`, `--gaji-pokok-dibayar`, `--tunjangan-tetap-dibayar`, `--hari-alpa`, `--catatan`, `--keterangan`; nilai `-` = hapus. `--file komponen.csv` (kolom kode/nama + nama komponen) |
| `impor-absensi <file>` (besar) | CSV `--csv-gaji` dari absensi-lokal | `--bulan`. Mengisi jam lembur, hari hadir/alpa, menit terlambat; potongan alpa hanya bila diatur |
| `saldo-awal` (kecil) | Data Jan s.d. sebelum memakai aplikasi | `--karyawan --tahun --sampai-bulan 1-11 --bruto --pph21 --iuran [--zakat]`, `--hapus` |
| `hitung` (kecil) | Hitung massal (draf) | `--bulan` |
| `final` (besar) | Kunci periode | `--bulan` |
| `revisi` (besar) | Buka revisi tercatat | `--bulan --alasan "..."` |
| `periode` | Daftar periode + riwayat revisi | — |
| `rekap` | Rekap perusahaan | `--bulan` atau `--tahun`. JSON `total`: `pph21_dipotong`, `pengembalian_pph21`, `setor_pph21` (= perkiraan setor, dipotong − dikembalikan, min. 0), `lebih_bayar_pph21` |
| `slip` | Slip Markdown per karyawan | `--bulan`, `--karyawan` (tampilkan satu), `--keluar <folder>` |
| `transfer` | CSV transfer (periode final) | `--bulan`, `--pemisah ;/,`, `--penuh` (periode revisi: gaji penuh, bukan selisih), `--rekening-lengkap` (nomor lengkap hanya di file) |
| `thr` (besar) | THR via mesin hitung-thr | `--bulan --hari-raya --nama-hari-raya [--tanggal-bayar] [--karyawan ...]` |
| `pph21-tahunan` | Cek PPh 21 setahun via mesin pph21-ter | `--tahun [--karyawan]` |
| `pengingat` | Tenggat gajian & setoran N hari ke depan | `--rentang 3` (0–60) |
| `backup` | Cadangan manual / daftar | `--label`, `--daftar` |
| `restore` (besar) | Pulihkan dari cadangan | `--dari <file>` |

## Kolom file impor karyawan (`templates/karyawan-contoh.csv`)
Wajib: `nama`, `ptkp`, `gaji_pokok`, `masuk` (tanggal masuk; alias `tanggal_masuk`/`tanggal_mulai`). Opsional: `kode`, `jabatan`, `jenis`, `tunjangan_tetap`, `tunjangan_tidak_tetap`, `zakat`, `bpjs`, `jkk`, `hari_kerja`, `dtp`, `bruto_tetap_januari`, `dasar_bpjs_kesehatan`, `nik`, `bank`, `rekening`, `atas_nama`, `kode_absensi`, `keluar`. Pemisah `;` `,` tab atau `|`; UTF-8/UTF-16/Windows-1252.

## Status & aturan periode
- `draf` → boleh `isi`/`hitung` berulang. `final` → terkunci; `slip` tanpa tanda DRAF dan `transfer` hanya untuk final.
- `revisi` membuat nomor revisi baru (status kembali draf). Hasil final lama tetap tersimpan; saat final lagi, selisih per karyawan dicatat di riwayat (`periode`).
- Karyawan ikut periode bila `tanggal masuk ≤ akhir bulan` dan (belum keluar atau `tanggal keluar ≥ awal bulan`).
- Masa Pajak Terakhir (Desember atau bulan keluar): total bruto, PPh 21, iuran JHT+JP karyawan, dan zakat Januari (atau bulan masuk) s.d. bulan lalu diambil dari periode FINAL + `saldo-awal`, lalu dikirim ke mesin `slip-gaji-bpjs` (`bruto_sd_bulan_lalu`, `pph21_sd_bulan_lalu`, `iuran_sd_bulan_lalu`, `zakat_sd_bulan_lalu`, `bulan_mulai`).

## Keluaran file (default: folder `keluaran/<YYYY-MM>/` di sebelah database)
- `slip-YYYY-MM-<kode>[-revN][-DRAF].md`
- `transfer-gaji-YYYY-MM[-revN].csv` atau `transfer-selisih-YYYY-MM-revN.csv`: kolom `no;kode;nama_penerima;bank;no_rekening;nominal;keterangan` (UTF-8 BOM, pemisah `;`). Sesuaikan dengan template unggah massal bank masing-masing.
