# Contoh 04 – Input tidak lengkap: "buatin SOP dong"

## Skenario
S4, input tidak lengkap. Dua info wajib (pekerjaan yang dibuat SOP-nya dan jenis usaha) sama-sama tidak ada. Skill harus bertanya sekali, maksimal 5 pertanyaan, dan memberi contoh supaya pengguna awam mudah menjawab.

## Input pengguna
```
buatin SOP dong
```

## Output

Boleh! Supaya SOP-nya pas dengan usahamu, jawab singkat pertanyaan ini:

1. **SOP untuk pekerjaan apa?** Contoh: buka/tutup toko, closing kasir, packing pesanan online, menangani komplain pelanggan, kebersihan dapur, atau terima barang di gudang.
2. **Usahanya apa?** Contoh: minimarket, kafe, warung makan, laundry, online shop baju, bengkel.
3. **Siapa yang mengerjakan, dan siapa yang mengecek?** Contoh: "kasir shift pagi, dicek pemilik".
4. **Bagaimana cara kerjanya sekarang?** Ceritakan bebas saja, termasuk aplikasi/alat yang dipakai dan masalah yang sering terjadi.
5. **Ada target atau jam tertentu?** Contoh: "buka jam 08.00", "semua paket siap sebelum kurir datang jam 15.00".

Kalau mau cepat, cukup jawab **nomor 1 dan 2**. Aku buatkan dari praktik umum, dan bagian yang perlu kamu sesuaikan akan aku tandai.

## Catatan penguji
- **Bagus:** sesuai tabel Input (pekerjaan dan jenis usaha wajib) dan batas 5 pertanyaan. Contoh jawaban mengikuti daftar di description dan `references/contoh-sop.md`, sehingga pengguna awam tidak bingung. Pertanyaan 4 memancing masalah nyata yang nanti menjadi langkah ⚠️.
- **Bagus:** jalur cepat jelas (cukup jawab nomor 1 dan 2).
- **Catatan:** tidak ada kekurangan berarti pada skenario ini.

## Penyegaran v1.0.6 (2026-10-17)
Output dan catatan di atas **tidak diubah** dan tetap sesuai SKILL.md v1.0.6: tanya sekali, maks. 5 pertanyaan, jalur cepat "jawab nomor 1 dan 2". Tidak ada nama skill, istilah internal, atau jalur berkas di jawaban ini.
