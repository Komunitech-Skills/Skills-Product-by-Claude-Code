# Uji 04 - Input tidak lengkap

**Prompt:** "Analisis pesaing saya."
**Perilaku agen (mengikuti Input & contoh-input-buruk):** satu pesan, maks. 5 pertanyaan bernomor: (1) jenis usaha & kota, (2) 3-5 nama saingan, (3) harga kira-kira, (4) tujuan utama, (5) yang sering dipuji/dikeluhkan pelanggan.

**Lanjutan:** "Cepat aja, usaha katering nasi kotak di Bekasi."
Agen memakai default (positioning + celah), menyebut asumsi, memberi kerangka: 3 lingkaran pesaing (katering lain, warteg/pesan antar, pengganti: masak/beli dekat kantor), daftar data yang harus dicari, contoh kriteria & bobot usulan, **tanpa** nama, harga, atau rating karangan. Semua sel "belum diketahui + cara mencari" (mis. cari "katering nasi kotak Bekasi" di Google Maps sebagai pembeli, tanya harga via WA).

Script tidak dijalankan (tidak ada data), sesuai aturan "jangan mengarang". **Verdict:** lulus.
