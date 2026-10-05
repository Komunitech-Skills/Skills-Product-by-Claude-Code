# 02 (UJI INDEPENDEN Akun B) — Jasa konsultan dengan piutang & potongan PPh 23

> Penguji independen (Akun B), 2026-09-26, hledger 1.52.4 asli dari scratchpad. Data fiktif buatan penguji.

**Pengguna:** "Saya konsultan, Rangga Konsultan, rekening BCA. Saldo 31 Agustus: kas 500rb, BCA 12 jt, laptop 15 jt. September: tagih PT Nusantara Logistik 15 jt (belum bayar), CV Mitra Tani 8,5 jt (belum bayar), sewa coworking 1,5 jt, konsultasi Bu Dewi 3.250.000 ditransfer, internet 450rb, gaji asisten 4 jt, Grab ke klien 320rb tunai, CV Mitra Tani cicil 4 jt. Tanggal 12, PT Nusantara bayar 14,7 jt karena dipotong PPh 23 2% (ada bukti potong). Langganan software 600rb. Siapa yang belum bayar? Saldo BCA saya di m-banking 19.330.000, cocok? Laporan September."

**Keputusan agent:** transaksi potongan PPh 23 tidak ada di tabel jenis → `catat --jenis bebas` dengan akun baru `Aset:PPh 23 Dibayar Dimuka` (ditolak dulu tanpa `--akun-baru`, lalu pratinjau setelah pengguna setuju). Akun `Beban:Langganan Software` juga dibuat dengan persetujuan. Skill tidak menghitung PPh 23 (sesuai batasan); angka 300rb dari bukti potong pengguna.

Catatan uji: angka "saldo nyata" 19.330.000 **sengaja salah** untuk menguji deteksi selisih.

## Log
```
init kode 0
Tersimpan 1 transaksi ke <scratch>/s2/Pembukuan/usaha.journal. Cadangan versi sebelumnya: usaha.journal.sebelum-ubah
Tersimpan 8 transaksi ke <scratch>/s2/Pembukuan/usaha.journal. Cadangan versi sebelumnya: usaha.journal.sebelum-ubah
(kode 0)
$ catat bebas: pelunasan PT Nusantara dipotong PPh 23 (tanpa --akun-baru)
GAGAL: Akun 'Aset:PPh 23 Dibayar Dimuka' belum ada di jurnal. Bila memang akun baru, ulangi dengan --akun-baru.
(kode 2)
$ ... sama + --akun-baru (setelah pengguna setuju)
PRATINJAU CATATAN (BELUM disimpan)
File: <scratch>/s2/Pembukuan/usaha.journal

2026-09-12 Pelunasan PT Nusantara, dipotong PPh 23 2%
    Aset:Bank:BCA                                  Rp 14.700.000
    Aset:PPh 23 Dibayar Dimuka                        Rp 300.000
    Aset:Piutang Usaha:PT Nusantara Logistik        -Rp 15.000.000
Artinya: Transaksi bebas 3 baris.

Akun baru yang akan dibuat: Aset:PPh 23 Dibayar Dimuka
Simpan 1 transaksi ini? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
(kode 0)
Tersimpan 1 transaksi ke <scratch>/s2/Pembukuan/usaha.journal. Cadangan versi sebelumnya: usaha.journal.sebelum-ubah
$ catat beban software akun salah ketik
GAGAL: Akun 'Beban:Langganan Sofware' belum ada di jurnal. Bila memang akun baru, ulangi dengan --akun-baru.
(kode 2)
Tersimpan 1 transaksi ke <scratch>/s2/Pembukuan/usaha.journal. Cadangan versi sebelumnya: usaha.journal.sebelum-ubah
$ saldo Aset:Piutang Usaha
SALDO AKUN
Rangga Konsultan
Per 26 September 2026

Aset:Piutang Usaha: Rp 4.500.000
- Aset:Piutang Usaha:CV Mitra Tani: Rp 4.500.000

Sumber: usaha.journal | Dihitung dengan: hledger 1.52.4
Uji silang pembaca bawaan: COCOK
(kode 0)
$ saldo Aset:Bank:BCA --nyata "Aset:Bank:BCA=19.330.000"
SALDO AKUN
Rangga Konsultan
Per 26 September 2026

Aset:Bank:BCA: Rp 27.400.000
Dibanding saldo nyata Rp 19.330.000: SELISIH Rp 8.070.000 (catatan lebih besar dari kenyataan).

Sumber: usaha.journal | Dihitung dengan: hledger 1.52.4
Uji silang pembaca bawaan: COCOK
(kode 1)
$ bulanan --bulan September 2026
RINGKASAN 1 SEPTEMBER 2026 S.D. 30 SEPTEMBER 2026
Rangga Konsultan
- Pendapatan: Rp 26.750.000
- Laba bersih: Rp 19.880.000
- Kas & bank akhir: Rp 27.580.000 (+Rp 15.080.000 dari awal bulan)
- Piutang (belum dibayar pelanggan): Rp 4.500.000
- Utang: Rp 0
- Neraca: seimbang

--------------------------------

LAPORAN LABA RUGI
Rangga Konsultan
Periode: 1 September 2026 s.d. 30 September 2026

PENDAPATAN
- Jasa: Rp 26.750.000
Total pendapatan: Rp 26.750.000

HARGA POKOK PENJUALAN (HPP)
- (belum ada)
Total HPP: Rp 0

LABA KOTOR: Rp 26.750.000 (100,0% dari pendapatan)

BEBAN USAHA
- Gaji: Rp 4.000.000
- Sewa: Rp 1.500.000
- Langganan Software: Rp 600.000
- Listrik Air Internet: Rp 450.000
- Transportasi: Rp 320.000
Total beban: Rp 6.870.000

LABA BERSIH: Rp 19.880.000 (74,3% dari pendapatan)

--------------------------------

NERACA (POSISI KEUANGAN)
Rangga Konsultan
Per 30 September 2026

ASET (yang dimiliki)
- Bank: Rp 27.400.000
- Peralatan: Rp 15.000.000
- Piutang Usaha: Rp 4.500.000
- PPh 23 Dibayar Dimuka: Rp 300.000
- Kas: Rp 180.000
Total aset: Rp 47.380.000

UTANG (kewajiban)
- (tidak ada)
Total utang: Rp 0

MODAL
- Saldo Awal: Rp 27.500.000
- Laba (rugi) tahun 2026 s.d. tanggal ini: Rp 19.880.000
Total modal: Rp 47.380.000

Cek: Aset = Utang + Modal (Rp 47.380.000). SEIMBANG.

--------------------------------

LAPORAN ARUS KAS
Rangga Konsultan
Periode: 1 September 2026 s.d. 30 September 2026

Kas & bank awal: Rp 12.500.000

ARUS KAS DARI OPERASI (jualan & biaya sehari-hari)
- Aset:Piutang Usaha: masuk Rp 18.700.000
- Beban:Gaji: keluar Rp 4.000.000
- Pendapatan:Jasa: masuk Rp 3.250.000
- Beban:Sewa: keluar Rp 1.500.000
- Beban:Langganan Software: keluar Rp 600.000
- Beban:Listrik Air Internet: keluar Rp 450.000
- Beban:Transportasi: keluar Rp 320.000
Bersih: +Rp 15.080.000

ARUS KAS DARI INVESTASI (beli/jual peralatan)
- (tidak ada)
Bersih: Rp 0

ARUS KAS DARI PENDANAAN (modal, prive, pinjaman)
- (tidak ada)
Bersih: Rp 0

Kenaikan (penurunan) kas: +Rp 15.080.000
Kas & bank akhir: Rp 27.580.000
- Aset:Bank:BCA: Rp 27.400.000
- Aset:Kas: Rp 180.000
Cek: kas akhir = saldo akun kas & bank. COCOK.
Pindah uang antar kas/bank sendiri tidak dihitung sebagai masuk/keluar.

Sumber: usaha.journal | Dihitung dengan: hledger 1.52.4
Uji silang pembaca bawaan: COCOK
Laporan manajemen dari catatan Anda sendiri, bukan laporan audit/pajak. Untuk bank/KUR format SAK EMKM, pakai perintah ekspor-emkm.
(kode 0)
```

## Verifikasi independen (Decimal) — `verif2.py`
```
pend 26750000 beban 6870000 laba 19880000 margin 74.3
kas 180000 bank 27400000 piutang 4500000 aset 47380000 modal 47380000 selisih 0
kas+bank awal 12500000 akhir 27580000 naik 15080000
```
hledger asli: `is` Net Rp 19.880.000; `bs` Piutang CV Mitra Tani Rp 4.500.000, PPh 23 Dibayar Dimuka Rp 300.000, Net Rp 47.380.000; `cf` +Rp 15.080.000; `check accounts` lulus. **Semua sama.**

## Penilaian
- ✅ Piutang per pelanggan tepat (`saldo Aset:Piutang Usaha` → hanya CV Mitra Tani Rp 4.500.000 — jawaban langsung untuk "siapa yang belum bayar").
- ✅ Saldo nyata beda → `SELISIH Rp 8.070.000 (catatan lebih besar)`, kode 1; agent diarahkan mencari transaksi terlupa dulu, bukan memaksa.
- ✅ Akun baru hanya dengan `--akun-baru`; potongan PPh 23 tercatat benar sebagai aset (kredit pajak), piutang lunas penuh 15 jt, pendapatan tetap bruto 15 jt.
- ⚠️ SKILL.md/references tidak punya pola siap pakai untuk "dibayar klien dipotong PPh 23" — sangat umum bagi konsultan/jasa di Indonesia. Agent harus merancang sendiri (di uji ini benar, tetapi rawan salah: mis. mencatat pendapatan neto 14,7 jt). Saran: tambah baris di `references/akun-dan-jenis.md` + akun bawaan `Aset:Pajak Dibayar Dimuka`.
- ⚠️ Salah ketik akun yang belum ada sama sekali (`Beban:Langganan Sofware`) hanya ditolak tanpa saran — wajar karena akun belum ada.
- ⚠️ Minor: "LABA KOTOR ... (100,0%)" dan HPP "(belum ada)" untuk usaha jasa terasa janggal; bisa disembunyikan bila HPP nol.
