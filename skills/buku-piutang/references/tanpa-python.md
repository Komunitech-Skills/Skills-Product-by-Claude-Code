# Jika Python tidak bisa dijalankan (mode manual)

Skill tetap bisa dipakai sebagai **buku piutang di spreadsheet**. Beri tahu pengguna: "Mode manual: angka dihitung
manual, mohon dicek." Jangan membuat/mengubah file `piutang.db` secara manual.

## 1. Tabel nota (Excel/Google Sheets atau CSV)
Pakai kolom yang sama dengan `templates/piutang-contoh.csv` agar kelak bisa diimpor (`piutang.py impor`):
`no nota;pelanggan;tanggal;jatuh tempo;nominal;dibayar;no wa;keterangan;status`
- Tanggal: hari/bulan/tahun lengkap (`26/09/2026`). Format kolom sebagai **Tanggal dd/mm/yyyy** atau **Teks**; jangan
  biarkan Excel mengubahnya menjadi angka seri (46291) atau format bulan/hari.
- Nominal & dibayar: angka bulat rupiah tanpa titik (1250000). Nomor WA: format kolom sebagai **Teks**.
- Satu nota satu baris. Pembayaran berikutnya: tambahkan ke kolom dibayar (catat tanggal & jumlahnya di keterangan).
- Jangan membagikan file ini ke grup (data pribadi pelanggan).

## 2. Rumus (tulis di bawah hasil supaya pemilik bisa memeriksa)
- Sisa = nominal − dibayar. Tidak boleh minus: bila pelanggan membayar lebih, catat kelebihannya terpisah sebagai
  **deposit pelanggan** (dipakai untuk nota berikutnya atau dikembalikan), jangan dijadikan sisa minus.
- Hari lewat = tanggal hari ini − jatuh tempo (hari kalender).
- Umur: ≤ 0 belum jatuh tempo; 1–30; 31–60; 61–90; > 90 hari. Persen = jumlah sisa kelompok ÷ total sisa × 100%,
  1 desimal.
- Saldo per pelanggan = jumlah sisa semua nota pelanggan itu − depositnya.
- PPN dari DPP: 12% × DPP nilai lain 11/12 = DPP × 11%, **dibulatkan ke bawah** ke rupiah (barang mewah: DPP × 12%,
  dibulatkan ke bawah). Pembulatan belum dicocokkan dengan Coretax.

## 3. Daftar jatuh tempo
Urutkan menurut jatuh tempo. Sisa > 0 dan jatuh tempo < hari ini = **terlewat**; = hari ini = **hari ini**;
1–7 hari lagi = **minggu ini**.

## 4. Draf pesan tagihan
Ikuti pola di `references/perintah.md` bagian "Draf pesan tagihan" (pengingat awal → hari jatuh tempo → terlewat
ringan → terlewat → terlewat lama + tawaran bertahap). Cantumkan nomor nota, sisa, jatuh tempo, rekening; tanpa
denda atau ancaman. Tautan: `https://wa.me/62812xxxxxxx?text=` + teks yang di-*URL-encode* (spasi `%20`, koma
`%2C`, baris baru `%0A`). Jika ragu, berikan draf saja dan minta pemilik menyalin-tempel ke WhatsApp.
