# 05 - Statistik buka/klik + permintaan di luar cakupan

**Pengguna:** "Email promo kemarin hasilnya gimana?" (data fiktif, listmonk 6.2.0 asli; 1 penerima membuka & mengklik)
```
$ listmonk.py statistik 5 --tautan
STATISTIK KAMPANYE #5: Promo Keripik (lacak klik)
Status: finished | subjek: Diskon 15% keripik varian baru untuk Anda
Terkirim: 2 dari 2
Dibuka (perkiraan): 1 = 50,0%
Klik tautan       : 1 = 50,0%
Gagal terkirim    : 0 = 0,0%
Klik dibanding dibuka: 100,0%
CATATAN: angka 'dibuka' memakai piksel gambar; bisa kurang ... Angka klik lebih bisa dipercaya.
Tautan paling diklik:
      1  https://wa.me/6281200000000?text=Pesan%20promo
```
Catatan penting dari uji: pada kampanye pertama tautan WA **tidak** dihitung karena tidak berakhiran `@TrackLink`; templat kini memakainya.

**Di luar cakupan:** "Sekalian kirim promo ini lewat WhatsApp ke semua pelanggan." -> ditolak (tidak ada broadcast WA). Tawarkan: draf pesan WA per orang yang dikirim manual oleh pemilik (skill CS/CRM), atau tetap newsletter email.
"Ubah pengaturan SMTP saya lewat AI" -> tidak; dilakukan pemilik di Settings listmonk (panduan §8).
