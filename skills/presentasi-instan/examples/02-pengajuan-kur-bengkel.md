# Contoh 02 — Presentasi pengajuan KUR ke bank (bengkel motor)

## Skenario
S2, permintaan normal dengan banyak angka Rupiah. Pemilik bengkel mau bertemu analis kredit BRI.

## Input pengguna
```
Mau ajukan KUR ke BRI bulan depan, butuh presentasi buat ketemu mantri/analisnya. Usaha: bengkel motor "Maju Jaya Motor" di Sidoarjo, jalan 5 tahun, 3 mekanik. Omzet rata2 Rp 42.500.000 per bulan, laba bersih sekitar Rp 9.800.000. Aset: peralatan bengkel Rp 65.000.000, motor operasional Rp 18.000.000, stok sparepart Rp 30.000.000, tempat masih sewa. Mau pinjam Rp 150.000.000 tenor 3 tahun: Rp 85.000.000 alat (kompresor, scanner injeksi, lift motor), Rp 50.000.000 stok sparepart, Rp 15.000.000 renovasi. Udah ada NIB, NPWP juga ada.
```

## Output
File nyata: [`kur-maju-jaya-motor.html`](kur-maju-jaya-motor.html) (10 slide, palet "Hijau Amanah").

Susunan slide (mengikuti `templates/pengajuan-kur.md`):
1. Sampul — Pengajuan KUR · BRI, Bengkel Maju Jaya Motor
2. Profil — 5 tahun · 3 mekanik · Sidoarjo (`[isi alamat]`)
3. Layanan
4. Kinerja — omzet Rp 42.500.000/bulan, laba bersih Rp 9.800.000/bulan
5. Aset — Rp 65.000.000 + Rp 18.000.000 + Rp 30.000.000 = **Rp 113.000.000**; tempat sewa
6. Penggunaan dana — Rp 85.000.000 (56,7%) · Rp 50.000.000 (33,3%) · Rp 15.000.000 (10,0%) = Rp 150.000.000
7. Rencana pengembalian — cicilan ±**Rp 4.563.291**/bulan (asumsi 6% efektif/tahun, anuitas, 36 bulan), laba Rp 9.800.000, **cicilan = 46,6% laba**
8. Proyeksi — kenaikan omzet `Rp [isi angka]` + asumsi `[isi]`
9. Legalitas — NIB ada, NPWP ada, nomor tidak dicantumkan
10. Penutup + disclaimer "pelengkap, bukan pengganti formulir resmi bank; cek kur.ekon.go.id"

Balasan ke pengguna:
```
Presentasi Pengajuan KUR - Bengkel Maju Jaya Motor sudah jadi: kur-maju-jaya-motor.html (10 slide)

Cara pakai:
- Buka file-nya dua kali klik, bisa dibuka di laptop maupun HP, tanpa internet.
- Navigasi: panah kiri/kanan, geser jari di HP, atau tombol ‹ ›.
- Cetak jadi PDF: Ctrl+P / Cmd+P → Simpan sebagai PDF → orientasi Lanskap.

Asumsi yang dipakai: palet "Hijau Amanah"; cicilan dihitung dengan bunga 6% efektif per tahun (anuitas) sebagai perkiraan — angka resmi mengikuti tabel angsuran bank.
Bagian yang masih perlu Anda lengkapi: alamat usaha, layanan tambahan, perkiraan kenaikan omzet setelah dana cair + asumsinya, status bukti sewa tempat.
Catatan: presentasi ini pelengkap, bukan pengganti formulir resmi KUR — cek syarat terbaru ke bank/penyalur KUR (kur.ekon.go.id).
Hasil cek otomatis: LULUS, tanpa peringatan.
```

## Catatan penguji
- **Angka diverifikasi independen:** total aset 113.000.000 ✔; porsi dana 56,7/33,3/10,0% ✔ dan total 150.000.000 ✔; cicilan anuitas `P·r/(1−(1+r)^−n)` = Rp 4.563.291 ✔, cocok dengan `skills/pengajuan-kur/scripts/simulasi_kur.py` (cicilan Rp 4.563.291, total bunga Rp 14.278.462); rasio 4.563.291/9.800.000 = 46,6% ✔.
- **Cacat sedang (isi):** skill ini **tidak menyebut skill `pengajuan-kur`** yang ada di library yang sama (cek plafon/agunan Permenko 1/2026, simulasi cicilan, rasio kemampuan bayar). Rumus cicilan dan asumsi bunga di atas datang dari pengetahuan penguji, bukan dari SKILL.md — agent lain bisa memakai bunga flat, tidak menghitung cicilan, atau tidak memberi tahu bahwa rasio 46,6% termasuk **BERAT** (script `pengajuan-kur` memperingatkan dan menyarankan plafon aman ±Rp 96.640.000) serta bahwa plafon > Rp 100 juta bisa diminta agunan tambahan. Presentasi ke analis kredit tanpa cek ini bisa merugikan pengguna.
- **Uji teknis:** 0 permintaan jaringan; tidak ada elemen meluber; `validasi_html.py` LULUS. Cetak PDF: 10 halaman (satu slide/halaman ✔) tetapi sisi kanan terpotong: pada ukuran kertas bawaan (Letter tegak) slide "Rencana penggunaan dana" hanya menampilkan kolom "Keperluan" — **semua nominal Rupiah hilang** — cacat kerangka yang sama dengan contoh 01.
