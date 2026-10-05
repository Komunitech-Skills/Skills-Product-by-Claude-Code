# Uji A/B — Tanpa Skill vs Dengan Skill (Skenario Normal #1)

Skenario: input yang sama dengan Uji 03 (`03-toko-online-salah-kirim-1010-uji-akun-b.md`) — 40 paket salah kirim saat flash sale 10.10.

## Input pengguna (sama persis untuk A dan B)
> "Tolong buatin laporan insiden. Pas flash sale 10.10 kemarin, sistem gudang kami salah cetak 40 label pengiriman (ketuker sama pesanan batch sebelumnya) karena dua batch pesanan digabung manual pas jam sibuk. Mulai packing jam 09.00, ketahuan jam 10.10 pas QC acak nemu label ganda. 10 paket sempat ditahan sebelum diambil kurir, 30 sudah kepiket kurir. Kita langsung hubungin kurir buat tahan yang masih bisa. Kerugian ongkir kirim ulang sekitar Rp2.000.000. Nama toko: Zalira Fashion."

## A — TANPA skill (agen umum, tanpa instruksi khusus)

Simulasi jawaban wajar agen umum tanpa skill ini:

> Baik, berikut laporan insidennya:
>
> **Laporan Insiden — Zalira Fashion**
> Terjadi kesalahan pengiriman 40 paket saat flash sale 10.10 karena label tertukar. Kejadian diketahui pukul 10.10, sebagian paket (10) berhasil ditahan, sisanya (30) sudah terkirim. Kerugian diperkirakan Rp2.000.000.
>
> Penyebabnya kemungkinan karena kurangnya ketelitian staf packing saat menggabungkan batch pesanan di jam sibuk. Ke depannya, staf packing perlu lebih berhati-hati dan teliti saat memproses pesanan, terutama saat flash sale.
>
> Kami mohon maaf sebesar-besarnya kepada seluruh pelanggan yang terdampak dan memastikan hal ini tidak akan pernah terjadi lagi di masa mendatang. Sebagai bentuk tanggung jawab, kami akan memberikan kompensasi kepada pelanggan yang dirugikan.

**Masalah pada hasil ini:**
- Akar masalah berhenti di "kurangnya ketelitian staf" — menyalahkan orang, bukan proses (melanggar prinsip blameless yang seharusnya dipakai).
- Draf minta maaf berjanji berlebihan: "tidak akan pernah terjadi lagi" dan "akan memberikan kompensasi" — padahal pengguna tidak pernah menyebut ada kebijakan kompensasi. Ini janji yang bisa menjebak pemilik usaha.
- Tidak ada bagian rencana pencegahan dengan penanggung jawab & tenggat yang konkret.
- Tidak ada draf versi pendek untuk broadcast WA maupun ringkasan terpisah untuk tim/pemilik.
- Tidak ada penanganan eksplisit untuk data yang tidak diberikan (mis. tenggat, PJ) — tidak jelas apakah ini asumsi atau fakta.
- Format tidak konsisten/dapat diprediksi untuk dipakai berulang sebagai template insiden berikutnya.

## B — DENGAN skill `laporan-insiden-usaha`

Lihat output lengkap di `03-toko-online-salah-kirim-1010-uji-akun-b.md`. Ringkasan perbedaan kunci:
- Akar masalah 5 Kenapa berhenti di **SOP packing belum mengatur verifikasi label per batch** — sistemik, bukan "staf kurang teliti".
- Draf minta maaf tidak menjanjikan kompensasi atau "tidak akan pernah terjadi lagi" — memakai `[isi: langkah konkret]` untuk hal yang belum dipastikan pengguna.
- Ada tabel Rencana Pencegahan dengan kolom Penanggung Jawab & Tenggat eksplisit (`[isi: ...]` bila belum disebut, bukan dikarang).
- Ada draf versi lengkap (DM/email) **dan** versi pendek (broadcast WA), plus Ringkasan terpisah siap tempel untuk tim/pemilik.
- Format tetap dalam urutan baku (Kronologi → Dampak → 5 Kenapa → Tindakan Cepat → Pencegahan → Draf Maaf → Ringkasan WA) — bisa dipakai berulang sebagai standar internal.

## Kesimpulan
Hasil **dengan skill jelas lebih baik**: lebih aman (tidak menyalahkan individu, tidak janji berlebihan yang bisa memberatkan usaha secara hukum/finansial di kemudian hari), lebih lengkap (rencana pencegahan terstruktur, dua level draf komunikasi), dan lebih konsisten formatnya untuk dipakai berulang. Skill memberi nilai tambah nyata, bukan sekadar merapikan kalimat — nilai tambahnya justru terletak pada apa yang **tidak** ditulis (janji berlebihan, tuduhan ke individu, angka karangan).
