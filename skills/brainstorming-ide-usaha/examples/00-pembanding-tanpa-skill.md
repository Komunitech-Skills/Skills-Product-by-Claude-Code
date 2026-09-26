# Uji A/B — Skenario 01 tanpa skill vs dengan skill

Penguji independen (Tahap 6), 2026-09-25. Permintaan sama persis:

> "Pak/Bu, warung makan saya ramai pagi sama malam, tapi jam 1 sampai jam 4 sore sepi banget. Ada ide produk baru buat naikin omzet? Modal paling 5 juta lah."

## A. Tanpa skill (agent yang sama, tanpa folder skill dimuat — jawaban satu kali)

> Berikut beberapa ide untuk meningkatkan omzet di jam sepi (13.00–16.00) dengan modal di bawah Rp5 juta:
>
> 1. **Menu minuman kekinian** — es kopi susu, thai tea, es buah. Modal alat ±Rp2–3 juta.
> 2. **Camilan sore** — gorengan, pisang goreng, roti bakar, cireng.
> 3. **Happy hour** — diskon 20% jam 13.00–16.00.
> 4. **Daftar di GoFood/GrabFood/ShopeeFood** — jangkau pembeli online di jam sepi.
> 5. **Paket hemat** — nasi + lauk + es teh harga spesial.
> 6. **Katering/nasi kotak** — terima pesanan untuk acara.
> 7. **Promosi media sosial** — buat akun Instagram/TikTok warung.
> 8. **Menu takeaway untuk makan malam** — pembeli pesan siang, ambil sore.
> 9. **Kerja sama dengan kantor sekitar** — makan siang langganan.
> 10. **Wifi gratis** — tarik mahasiswa/pekerja nongkrong.
>
> Tips: mulai dari yang modal kecil, uji 1–2 minggu, evaluasi hasilnya. Semoga sukses!

## B. Dengan skill

Lihat `01-warung-makan-sepi-siang.md` (klasifikasi Jalur B → 4 pertanyaan terfokus → pemahaman ditulis ulang & dikoreksi → Pembalikan Masalah + SCAMPER → 3 pendekatan dengan modal/margin/balik modal **dihitung script** (125/500/143 unit, diverifikasi) → persetujuan → MVP bertarget angka → Rencana Aksi 7 Hari → asumsi).

## Penilaian berdampingan (1–5)

| Kriteria | Tanpa skill | Dengan skill | Catatan |
|---|---|---|---|
| Relevan dengan kondisi nyata pengguna (lokasi, tenaga, apa yang sudah dicoba) | 2 | 5 | A mengusulkan lagi **diskon happy hour** padahal (setelah ditanya) pengguna sudah mencobanya & gagal; B membuangnya dengan alasan. A tidak tahu lokasi dekat ruko/bengkel. |
| Menyaring (bukan sekadar daftar) | 1 | 4 | A: 10 ide setara tanpa urutan. B: 3 pendekatan, untung-rugi, rekomendasi + alasan. |
| Angka dihitung, bukan dikira | 1 | 4 | A: "modal ±Rp2–3 juta" tanpa dasar. B: modal, margin, titik impas via `skor_ide.py impas`, asumsi ditandai. |
| Siap dieksekusi minggu ini | 1 | 5 | A: "uji 1–2 minggu" umum. B: MVP dengan target angka, aturan lanjut/perbaiki/hentikan, biaya uji maks, tabel Hari 1–7. |
| Kejujuran / tidak mengarang data pasar | 3 | 5 | B memisahkan "disebut" vs "asumsi". |
| Kecepatan / beban pengguna | 5 | 3 | A langsung jawab; B butuh 4 giliran tanya sebelum ide muncul. |
| Bahasa awam | 4 | 4 | Keduanya mudah; B sedikit lebih panjang. |
| **Total (maks 35)** | **17** | **30** | |

## Kesimpulan

**Dengan skill jelas lebih baik** untuk tujuan pengguna (menaikkan omzet jam sepi dengan modal terbatas): ide disesuaikan dengan kondisi nyata, ide gagal tidak diulang, angka dihitung, dan hasilnya rencana 7 hari yang langsung bisa dikerjakan. Satu-satunya kekalahan: lebih lambat / lebih banyak tanya — lihat temuan "satu pertanyaan per pesan" di `HASIL-UJI.md`.

Bahan "sebelum/sesudah" untuk README: jawaban A (daftar 10 ide generik, termasuk diskon yang sudah gagal) vs rencana 7 hari B.
