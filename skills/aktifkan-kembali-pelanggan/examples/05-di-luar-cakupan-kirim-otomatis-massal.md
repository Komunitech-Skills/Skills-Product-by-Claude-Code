# Contoh 05, di luar cakupan: kirim otomatis ke ratusan nomor, termasuk database beli

> Dibuat oleh pembuat skill. Tidak ada script yang dijalankan.

## Permintaan pengguna
> "Saya punya 400 nomor WA, sebagian dari pelanggan saya dan sebagian dari database yang saya beli. Tolong atur OpenClaw kirim pesan ajakan balik ke semuanya otomatis tiap hari jam 9 pagi, 50 per hari, pakai jeda acak biar nggak diblokir WA."

## Pemeriksaan agen
| Pemicu | Aturan skill | Keputusan |
|---|---|---|
| Kirim otomatis lewat OpenClaw | Aturan keras 1: satu per satu oleh manusia (copilot) | Tolak bagian pengiriman otomatis |
| 50 pesan per hari | Batas harian 10 (maks. 15 disarankan) | Tidak diikuti |
| Jeda acak agar tidak diblokir | Aturan keras 1: tidak membantu mengakali sistem anti-spam | Tolak |
| Nomor dari database yang dibeli | Aturan keras 2: hanya pelanggan yang pernah membeli; UU PDP Pasal 65, 67 | Tolak bagian itu; sarankan tidak dipakai |
| Pelanggan sendiri | Dalam cakupan | Tawarkan jalur Copilot |

## Balasan ke pengguna

Untuk yang ini saya tidak bisa bantu mengaturnya, dan alasannya justru untuk melindungi usaha dan nomor Anda:

1. **Pengiriman otomatis ke ratusan nomor** dari satu WhatsApp adalah pola yang paling cepat membuat nomor diblokir permanen, dan WhatsApp lewat OpenClaw bukan jalur resmi. Jeda acak agar tidak terdeteksi tetap mengakali sistem anti-spam, jadi bagian itu tidak saya bantu. Pesan ajakan balik juga jauh lebih berhasil kalau terasa personal dan dikirim manusia.
2. **Nomor dari database yang dibeli** berisiko melanggar UU Pelindungan Data Pribadi (UU No. 27/2022): pemilik nomor tidak pernah memberikan datanya ke usaha Anda. Saya sarankan bagian itu tidak dipakai.

**Yang bisa saya kerjakan sekarang, untuk pelanggan Anda sendiri:**
- Memilah pelanggan yang benar-benar pernah beli, mana yang sudah lama diam, dan berapa nilai belanja mereka dulu.
- Menyiapkan **teks pesan siap salin** untuk tiap kelompok, jadwal 3 pesan dalam 4 minggu, dan daftar siapa dikirim hari apa (maksimal 10 per hari).
- **Anda yang menekan kirim** satu per satu, dan daftar harian bisa saya siapkan setiap kali Anda minta. Kalau pelanggan membalas, komplain, atau minta berhenti, urutan dihentikan.

Cukup kirim data pelanggan yang pernah membeli (nama, nomor WA, tanggal beli terakhir, total belanja), dan saya langsung kerjakan.

**Tiga pertanyaan:**
1. Berapa dari 400 nomor itu yang memang pernah membeli dari Anda? Kirim yang itu saja.
2. Ada penawaran yang bisa Anda berikan di pesan ketiga, atau tanpa penawaran?
3. Mau jadwal harian dalam bentuk tabel centang?

---
## Catatan pembuat
- Menolak dengan sopan, menjelaskan risiko hukum dan teknis, tidak membuat draf "sekali ini saja" untuk nomor beli, menawarkan jalur Copilot sesuai keputusan pemilik 2026-09-23 (tidak ada broadcast lewat OpenClaw).
