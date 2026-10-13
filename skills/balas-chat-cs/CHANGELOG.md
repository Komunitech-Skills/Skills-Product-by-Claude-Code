# Riwayat perubahan — balas-chat-cs

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-02)
- Revisi putaran 2: bagian "ATURAN WAJIB" ditambahkan di awal SKILL.md. Bila pelanggan menempel password, token, kunci, OTP, PIN, atau data login di chat, agent tidak boleh mengulang satu karakter pun (tidak utuh, tidak awalan, tidak disamarkan) baik di draf balasan maupun di catatan admin, dan memakai templat balasan baku.
- Draf tidak boleh menjanjikan atau menerima kompensasi (refund penuh/sebagian, ganti baru, voucher, ongkir) sebelum pemilik memutuskan; dipakai frasa netral dan ditandai [KEPUTUSAN PEMILIK]. Daftar periksa diperbarui.

## Catatan revisi 1.0.4 (2026-10-02)
- Masuk skill inti paket klinik (temuan uji gabungan klinik: tidak ada skill yang terpicu untuk "chat pasien ini gimana jawabnya"). Ditambah aturan chat pasien klinik: selalu draf, tanpa dosis/diagnosis, arahkan ke dokter + tanda bahaya IGD/119, tanpa promo/imbalan rujukan. PERLU REVIEW tenaga medis.

## Catatan revisi 1.0.3 (2026-10-01)
- Janji dan kompensasi (mis. siapa menanggung ongkir) hanya dari kebijakan toko yang Anda berikan; sisanya ditulis [isi: kebijakan ...], tidak dikarang.
- Setiap permintaan pembeli (mis. refund) kini ditanggapi dan ditandai untuk konfirmasi pemilik.
- Balasan selalu menyertakan waktu tindak lanjut yang jelas.

## Catatan revisi 1.0.2 (2026-09-30)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.1 (2026-09-24)
- Versi saat skill pertama masuk repo (lolos uji muat OpenClaw). Perbaikan kecil; rincian di riwayat git.

## Catatan revisi 1.0.0 (sebelum 2026-09-24)
- Rilis awal (uji internal).
