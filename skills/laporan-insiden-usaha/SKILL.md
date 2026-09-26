---
name: laporan-insiden-usaha
description: Menyusun laporan insiden operasional usaha (retur/pesanan salah kirim massal, stok habis saat promo, komplain viral di medsos, mesin kasir/QRIS error, karyawan telat buka toko, data pelanggan bocor ringan) berisi kronologi, dampak berangka, akar masalah tanpa menyalahkan orang (5 kenapa), tindakan cepat, rencana pencegahan dengan penanggung jawab & tenggat, draf permintaan maaf ke pelanggan, dan ringkasan singkat untuk WA tim/pemilik. Gunakan saat pengguna minta laporan insiden, postmortem toko/usaha, kronologi kejadian, incident report UMKM, atau draf minta maaf ke pelanggan setelah masalah operasional.
---

# Laporan Insiden Usaha

## Tujuan
Mengubah kejadian buruk operasional (bukan bencana besar, bukan tuntutan hukum) jadi satu dokumen rapi: apa yang terjadi, siapa/berapa yang terdampak, kenapa bisa terjadi (tanpa berburu kambing hitam), apa yang sudah dilakukan, dan apa yang dilakukan supaya tidak terulang — plus draf siap kirim (permintaan maaf ke pelanggan, ringkasan ke tim/pemilik via WA).

## Kapan digunakan
- Pesanan salah kirim/tertukar massal, retur menumpuk
- Stok habis mendadak saat promo/live/flash sale
- Komplain pelanggan viral di medsos/marketplace
- Mesin kasir, aplikasi kasir, atau QRIS error saat jam sibuk
- Karyawan telat buka toko/gerai
- Data pelanggan bocor ringan (mis. file pesanan salah kirim ke grup lain, nomor WA pelanggan tersebar tanpa sengaja)
- Masalah operasional lain yang menimbulkan kerugian, komplain, atau risiko reputasi tapi **bukan** kejadian yang mengancam nyawa/butuh penanganan darurat

## Kapan TIDAK digunakan
- Notulen rapat rutin (bukan insiden) → `notulen-rapat`
- Balasan chat komplain satuan/harian (bukan insiden besar) → `balas-chat-cs`
- Laporan status kerja mingguan biasa → `laporan-status-kantor`
- Surat peringatan ke karyawan tertentu → `surat-peringatan-karyawan` (skill ini sengaja **tidak menyalahkan individu** — lihat Batasan)
- Kejadian yang menyangkut **kebocoran data pribadi** dalam skala luas/sensitif, ancaman pidana, kecelakaan kerja, atau kebakaran/bencana: skill ini hanya bantu menyusun kronologi & komunikasi dasar. **Bukan nasihat hukum, bukan nasihat K3/keselamatan.** Untuk kewajiban pemberitahuan kebocoran data pribadi, rujuk ke `kebijakan-privasi-pdp` dan/atau konsultan hukum — lihat Batasan.

## Input
Tanyakan **sekali** dalam satu pesan bila belum lengkap:
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Apa yang terjadi (kronologi kasar) | Ya | — (tanyakan) |
| Kapan (tanggal & jam mulai/ketahuan/selesai) | Ya | — (tanyakan) |
| Siapa/berapa yang terdampak (jumlah pesanan, pelanggan, atau omzet) | Tidak, tapi diminta jika ada | Ditandai `[isi: jumlah]` — **tidak pernah dikarang** |
| Bagaimana ketahuan & bagaimana ditangani sejauh ini | Tidak | Ditandai `[isi: ...]` |
| Apakah menyangkut data pelanggan | Ya, khusus dicek | Jika tidak disebut, dianggap tidak — tapi ingatkan sekali untuk dicek |
| Nama usaha/toko (untuk draf minta maaf) | Tidak | `[Nama Usaha]` |

## Langkah Kerja
1. **Kumpulkan fakta dulu, jangan simpulkan sebab dulu.** Susun kronologi berurutan waktu: kapan mulai, kapan ketahuan, kapan mulai ditangani, kapan selesai/masih berjalan. Pakai jam yang disebutkan pengguna, jangan mengarang jam.
2. **Hitung dampak dari angka yang diberikan pengguna, jangan mengira-ngira.** Jumlah pesanan/pelanggan terdampak, estimasi kerugian (jika ada angka), waktu operasional yang hilang. Kalau pengguna tidak kasih angka, tulis `[isi: jumlah]` — jangan isi angka perkiraan sendiri.
3. **Cari akar masalah pakai 5 Kenapa, arahnya ke sistem/proses, bukan ke orang.** Tanya "kenapa" berulang sampai ketemu penyebab yang bisa diperbaiki (proses, alat, SOP yang tidak ada/tidak diikuti) — bukan berhenti di "karena karyawan X lalai". Contoh arah yang benar: "kenapa salah kirim → kenapa tidak dicek ulang → kenapa tidak ada langkah cek ulang di SOP packing". Lihat `references/panduan-5-kenapa.md` untuk contoh lengkap & kalimat yang harus dihindari.
4. **Tindakan cepat**: apa yang sudah/perlu dilakukan SEKARANG untuk menghentikan kerugian lanjutan (mis. hubungi kurir, hentikan promo sementara, restart mesin kasir, ganti channel bayar cadangan).
5. **Rencana pencegahan**: minimal 2–4 tindakan konkret, masing-masing dengan **penanggung jawab** (jabatan, bukan wajib nama pribadi) dan **tenggat** (tanggal). Kalau pengguna tidak sebut siapa, tulis `[isi: penanggung jawab]` dan `[isi: tenggat]` — jangan mengarang nama.
6. **Jika insiden menyangkut data pelanggan (bocor/tersebar tanpa izin, sekecil apa pun):** tambahkan bagian khusus yang menjelaskan secara umum bahwa UU 27/2022 (UU PDP) mewajibkan pengendali data memberitahukan kebocoran data pribadi kepada subjek data dan otoritas terkait, termasuk soal batas waktu pemberitahuan — **tanpa memastikan angka hari atau langkah hukum pasti**, arahkan pengguna ke skill `kebijakan-privasi-pdp` dan/atau konsultan hukum/DPO untuk kepastian. Skill ini **tidak memberi nasihat hukum**.
7. **Susun draf permintaan maaf ke pelanggan**: sopan, mengakui masalah secara spesifik, tanpa menyalahkan pelanggan, tanpa janji berlebihan (jangan janji "tidak akan pernah terjadi lagi" — janji "kami sedang benahi [X]"), sertakan langkah konkret yang sudah/akan dilakukan untuk pelanggan yang terdampak. Sertakan juga versi pendek untuk broadcast/DM WA.
8. **Susun ringkasan singkat untuk tim/pemilik via WA** (format tebal-pendek, siap tempel): apa yang terjadi, dampak, status sekarang, tindakan pencegahan + siapa pegang apa.
9. Jika kejadian di luar cakupan (mengancam nyawa, kebakaran, kecelakaan kerja, ancaman pidana serius) → hentikan, sampaikan bahwa ini di luar cakupan skill dan arahkan ke pihak berwenang/profesional yang tepat, jangan paksakan format ini.

## Format Output
Berikan dalam urutan ini (boleh dipersingkat untuk kejadian kecil, tapi urutan tetap):

```
# Laporan Insiden: [Judul singkat kejadian]

**Tanggal kejadian:** [tanggal] · **Ketahuan:** [jam] · **Status:** [Selesai / Masih ditangani]

## Kronologi
[HH:MM] — [kejadian]
[HH:MM] — [kejadian]
...

## Dampak
- Pelanggan/pesanan terdampak: [angka atau [isi: jumlah]]
- Kerugian/omzet: [angka atau [isi: jumlah]]
- Lainnya: [operasional, reputasi, dll]

## Akar Masalah (5 Kenapa)
1. Kenapa [gejala]? → ...
2. ...
**Akar masalah:** [satu kalimat, fokus sistem/proses]

## Tindakan Cepat (sudah/sedang dilakukan)
- [tindakan]

## Rencana Pencegahan
| Tindakan | Penanggung jawab | Tenggat |
|---|---|---|
| ... | [jabatan] | [tanggal] |

## [Jika menyangkut data pelanggan] Kewajiban Pemberitahuan Data Pribadi
[Penjelasan umum UU PDP + arahan ke kebijakan-privasi-pdp/konsultan — bukan nasihat hukum]

## Draf Permintaan Maaf ke Pelanggan
[versi lengkap: email/DM]

[versi pendek: broadcast/status WA]

## Ringkasan untuk Tim/Pemilik (WA)
*[Judul singkat]*
Apa: ...
Dampak: ...
Status: ...
Pencegahan: [tindakan] — PJ: [jabatan], tenggat [tanggal]
```

## Contoh
Lihat `examples/01-pesanan-salah-kirim-massal.md` dan `examples/02-qris-error-jam-sibuk.md` untuk kasus lengkap dari kronologi mentah sampai draf jadi.

## Batasan & Penanganan Error
- **Tidak menyalahkan individu.** Akar masalah selalu diarahkan ke proses/sistem, bukan ke nama karyawan tertentu, kecuali pengguna secara eksplisit minta bagian terpisah untuk tindak lanjut kedisiplinan — itu pun diarahkan ke `surat-peringatan-karyawan`, bukan ditulis di laporan insiden ini.
- **Tidak mengarang angka.** Semua dampak (jumlah pesanan, kerugian, waktu) harus dari input pengguna. Yang tidak diberikan ditandai `[isi: ...]`, tidak diisi kira-kira.
- **Bukan nasihat hukum, bukan nasihat K3/keselamatan, bukan kalkulator/skrining medis apa pun.** Untuk kebocoran data pribadi, skill ini hanya menjelaskan **secara umum** bahwa ada kewajiban pemberitahuan menurut UU 27/2022 dan mengarahkan ke `kebijakan-privasi-pdp` serta profesional — tidak memastikan tenggat hari, tidak menyusun surat resmi ke otoritas.
- **Di luar cakupan:** kejadian yang mengancam keselamatan jiwa, kebakaran, kecelakaan kerja berat, dugaan tindak pidana (pencurian besar, kekerasan) — untuk kejadian ini skill berhenti dan mengarahkan ke pihak berwenang/profesional, tidak memaksakan format laporan insiden usaha biasa.
- **Draf permintaan maaf tidak pernah membuat janji yang tidak bisa dipastikan** (mis. kompensasi, tenggat perbaikan pasti) kecuali pengguna sendiri yang menyebutkannya.
