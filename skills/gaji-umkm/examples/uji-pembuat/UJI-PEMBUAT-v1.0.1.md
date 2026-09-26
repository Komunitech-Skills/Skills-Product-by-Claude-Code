# Uji pembuat gaji-umkm v1.0.1 (26 September 2026)

> Catatan **pembuat** atas revisi pemeliharaan berdasarkan temuan penguji independen Akun B
> (`examples/HASIL-UJI.md`, skor 8/10). Bukan uji independen — skenario 05 perlu diuji ulang oleh penguji terpisah.
> `scripts/mesin/*` **tidak diubah** (sha256 tetap cocok dengan `SUMBER.json` dan skill sumber); semua logika baru ada di `scripts/gaji.py`.

## Perubahan
| Temuan | Perbaikan v1.0.1 |
|---|---|
| P1-a pagar BPJS/pajak | `karyawan tambah/ubah/impor` yang membuat karyawan tanpa BPJS Kesehatan/Ketenagakerjaan (tetap **maupun** kontrak) atau `--dasar-bpjs-kesehatan` di bawah dasar menurut aturan (gaji pokok + tunjangan tetap, min. UMK bila diisi, maks. Rp 12 jt): pratinjau berlabel "PERLU PERSETUJUAN KHUSUS" + dasar (UU 24/2011 Ps. 15, Perpres 82/2018 jo. 64/2020 Ps. 32, PP 86/2013); `--ya` saja **ditolak** (JSON `masalah_kepatuhan`, database tidak berubah). Simpan hanya dengan `--ya --ya-saya-paham [--alasan-khusus ".."]`; persetujuan dicatat di tabel `log` (`konfirmasi_kepatuhan`: masalah, pesan, alasan, waktu) dan di JSON keluaran. `hitung` mengingatkan setiap bulan. Hanya masalah **baru** yang meminta persetujuan (ubah jabatan karyawan yang sudah disetujui tidak ditanya ulang). JP saja tidak dipagari (kewajiban JP bertahap menurut skala usaha). SKILL.md: Aturan wajib 7 + jawaban penolakan baku untuk "jangan daftarkan BPJS / lapor UMK saja / ganti PTKP / pecah gaji jadi uang makan / dua versi slip". |
| P1-b setoran PPh 21 | Aturan diverifikasi dari naskah resmi PMK 168/2023 Pasal 21 ayat (1)–(3) (JDIH Kemenkeu) + artikel DJP pajak.go.id 12-03-2025 (kompensasi lebih bayar bila secara akumulatif semua karyawan ada kelebihan potong). Rekap kini: "PPh 21 dipotong bulan ini", "Kelebihan PPh 21 dikembalikan ke karyawan", "Perkiraan setor PPh 21" (= dipotong − dikembalikan, min. 0) dan bila minus "Lebih bayar ... dapat diperhitungkan ke bulan berikutnya lewat SPT Masa" (tidak dikurangkan otomatis), + saran konfirmasi konsultan pajak/Coretax & catatan pembulatan. JSON `total`: `pph21_dipotong`, `pengembalian_pph21`, `setor_pph21` (= perkiraan setor), `lebih_bayar_pph21`. Total periode yang disimpan v1.0.0 dilengkapi otomatis saat dibaca (`rekap`, `pengingat`, rekap tahun). Contoh temuan penguji: September Rp 4.018.864 − Rp 931.100 = **Rp 3.087.764** (dites). |
| P2 tenggat JP/JHT | `pengingat`: bila tgl 15 jatuh Sabtu/Minggu → baris **JP tgl 15 tanpa geser** (PP 45/2015 Ps. 30 ayat (3)) + baris JHT/JKK/JKM di hari kerja berikutnya (PP 46/2015 Ps. 19; PP 44/2015 Ps. 21). Tgl 15 hari kerja → satu baris gabungan. PERLU REVIEW JHT/JP di `references/dasar-aturan.md` ditutup dengan sitasi PDF resmi BPJS TK; catatan BPJS Kesehatan diperbarui (Perpres 82/2018 Ps. 39, pengingat tetap tgl 10). |
| P2 UMK prorata | Peringatan "di bawah UMK" untuk bulan yang diisi `--gaji-pokok-dibayar` diberi catatan bahwa UMK dibandingkan dengan gaji penuh, bukan gaji prorata. |

## Otomatis: `python3 tests/uji_regresi.py` → 36 tes lulus (29 lama + 7 baru, Python 3.11 Linux)
Tes baru (`UjiV101`): pagar tanpa BPJS (pratinjau/tolak/simpan+log/pengingat bulanan/tidak ditanya ulang); pagar dasar Kes di bawah upah (UMK, batas 12 jt, tambah kontrak, impor semua-atau-tidak, JP saja tidak dipagari); setoran PPh 21 neto + lebih bayar di Desember (angka dicocokkan dengan jumlah per karyawan dari mesin, rekap bulan & tahun); tanpa kelebihan tetap satu baris "Setor PPh 21"; total lama v1.0.0 dilengkapi (angka temuan penguji); pengingat JP 15/11/2026 (Minggu) tidak digeser vs JHT Senin 16/11, dan 15/10/2026 (Kamis) satu baris; peringatan UMK prorata. Tes pencocokan massal lama disesuaikan: karyawan acak tanpa BPJS ditambah `--ya-saya-paham`.

## Manual
Skenario Lina (gaji 30 jt Jan–Nov, keluar 31/12 dengan gaji dibayar 1 jt) + Mira: rekap Desember menampilkan dipotong Rp 543.072, dikembalikan Rp 7.251.060, perkiraan setor Rp 0, lebih bayar Rp 6.707.988 dengan catatan kompensasi & konsultan.

## Masih terbuka
- Uji ulang skenario 05 oleh penguji independen.
- Isian SPT Masa PPh 21 di Coretax tidak diuji; pembulatan belum dicocokkan dengan Coretax.
- Temuan P3 penguji (nama kembar saat impor, pesan .xlsx palsu, pola kode, teks THR) belum dikerjakan.
