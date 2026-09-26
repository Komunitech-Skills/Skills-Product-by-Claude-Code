# Memasang Frappe Books & menemukan file datanya

Frappe Books adalah software akuntansi desktop gratis (AGPL-3.0) buatan Frappe. **Komunitech tidak menyertakan atau
mendistribusikan Frappe Books** dan tidak berafiliasi dengan Frappe; pengguna memasangnya sendiri dari sumber resmi.

## Pasang (±10 menit)
1. Buka **https://frappe.io/books** → tombol unduh mengarah ke **https://github.com/frappe/books/releases**.
   Unduh hanya dari dua alamat itu. Pilih file installer yang sesuai komputer (Windows, macOS, atau Linux; nama file tertera di halaman rilis — daftar file rilis belum dicek Komunitech di sesi ini).
2. Jalankan installer seperti program biasa. Jangan pernah memasang lewat skrip yang diunduh lalu langsung dijalankan tanpa dibaca.
   Windows/macOS bisa memberi peringatan keamanan bila sertifikat penanda tangan rilis kedaluwarsa (lihat catatan proyek di
   `references/sumber-resmi.md`); bila ragu, minta bantuan jasa setup Komunitech.
3. Buka Frappe Books → **New Company** → isi nama usaha, negara **Indonesia**, mata uang **IDR**, pilih bagan akun Indonesia
   (atau Standard). Bahasa aplikasi bisa diganti ke Bahasa Indonesia di pengaturan.
4. Bila ingin stok: Setup → Settings → bagian **Features** → centang **Enable Inventory**, lalu centang **Track Inventory** di tiap barang.
5. Buat template pajak PPN (lihat `references/ppn-frappe-books.md`).

## Di mana file datanya?
- Bawaan: folder **Documents/Frappe Books/** dengan nama `<nama usaha>.books.db`
  (Windows: `C:\Users\<nama>\Documents\Frappe Books\`, macOS: `/Users/<nama>/Documents/Frappe Books/`, Linux: `~/Documents/Frappe Books/`).
- Bila saat membuat usaha memilih lokasi lain, lihat di layar awal Frappe Books (daftar file) atau cari file berakhiran `.books.db`.
- Script mencari otomatis di Documents/Frappe Books bila hanya ada satu file; bila lebih, sebutkan dengan `--db`.

## Backup (wajib sebelum impor CSV)
Tutup Frappe Books → salin file `.books.db` ke flashdisk/Google Drive/folder lain dengan nama bertanggal, mis.
`Toko Saya 2026-09-26.books.db`. Memulihkan = tutup aplikasi, salin balik file tersebut.
