# Checklist kelayakan & dokumen penawaran

Pakai sebagai **daftar periksa umum**. Syarat pasti tiap paket ada di **dokumen pemilihan** (LDP/LDK, spesifikasi, rancangan kontrak) + adendum. Tandai `[x]` bila sudah ada, `[!]` bila bermasalah, `[-]` bila tidak diminta.

## A. Cek kelayakan (sebelum memutuskan ikut)
| # | Pemeriksaan | Cara cek | Gugur jika |
|---|---|---|---|
| A1 | Kualifikasi usaha sesuai paket (kecil / non-kecil) | Kualifikasi di NIB/OSS; kriteria usaha kecil PP 7/2021 (modal > Rp1–5 M atau omzet > Rp2–15 M/tahun) | Paket untuk usaha kecil tapi NIB bukan usaha kecil (atau sebaliknya) |
| A2 | **KBLI** di NIB cocok dengan KBLI yang diminta paket | Bandingkan kode 5 digit KBLI di OSS dengan LDK | KBLI tidak ada di NIB |
| A3 | NIB aktif & perizinan berusaha sesuai risiko (PP 28/2025) | Cetak NIB terbaru dari OSS RBA | Izin belum terbit / tidak berlaku |
| A4 | NPWP badan/usaha valid & **status PKP** (bila paket mensyaratkan / bila akan memungut PPN) | Coretax: status NPWP & PKP; bukti lapor SPT tahunan terakhir (bila diminta) | NPWP tidak valid; mencantumkan PPN padahal bukan PKP |
| A5 | **Konstruksi:** SBU sesuai subklasifikasi & kualifikasi; **SKK** personel manajerial | Portal LPJK / SIJK | SBU tidak sesuai / kedaluwarsa; personel tanpa SKK |
| A6 | Pengalaman sejenis | Kontrak + BAST 3–4 tahun terakhir (sesuai LDK) | Tidak punya pengalaman padahal wajib (pengecualian usaha kecil < 3 tahun untuk paket s.d. Rp2,5 M — cek LDK) |
| A7 | **Sisa Kemampuan Paket (konstruksi)** | SKP = KP − P; usaha kecil KP = 5; P = paket konstruksi yang sedang berjalan | SKP ≤ 0 |
| A8 | Tidak masuk daftar hitam; pengurus tidak dalam sanksi | Portal daftar hitam nasional (INAPROC) | Masuk daftar hitam |
| A9 | Kemampuan menyediakan: stok/produksi, TKDN (bila ada syarat PDN), tenaga & alat, modal kerja (termasuk potongan PPN/PPh oleh bendahara) | Hitung arus kas; minta surat dukungan pemasok bila diminta | — (risiko wanprestasi) |
| A10 | Akun SPSE aktif & terverifikasi di LPSE | Login SPSE di spse.inaproc.id; verifikasi berkas asli ke LPSE bila belum | Tidak bisa mengunggah |

## B. Dokumen penawaran — per metode
### B1. Tender/seleksi (pascakualifikasi, umumnya satu file)
**Administrasi & kualifikasi**
- [ ] Isian data kualifikasi di SPSE (identitas, izin, akta, pengurus, pajak, pengalaman, tenaga, peralatan) — isi lengkap & konsisten dengan dokumen asli
- [ ] Surat penawaran (format dari dokumen pemilihan): nama paket, **masa berlaku penawaran** ≥ yang diminta, jangka waktu pelaksanaan, **tanggal**, **ditandatangani** direktur/pihak yang berwenang (atau penerima kuasa dengan surat kuasa sah)
- [ ] Pakta integritas (biasanya tersedia di SPSE)
- [ ] **Jaminan penawaran** asli (bila HPS > Rp10 M atau diminta): nama paket & pokja benar, nilai sesuai, masa berlaku ≥ masa berlaku penawaran, **bisa dicairkan** (unconditional), dari penerbit yang diterima
- [ ] Surat kuasa/akta bila penandatangan bukan direktur utama
- [ ] Perjanjian kemitraan/KSO (bila KSO)

**Teknis**
- [ ] Spesifikasi teknis yang ditawarkan **memenuhi/melebihi** yang diminta (merek, tipe, brosur bila diminta)
- [ ] Jadwal & jangka waktu pelaksanaan ≤ yang ditetapkan
- [ ] Metode pelaksanaan (konstruksi/jasa)
- [ ] Daftar personel & peralatan (konstruksi/jasa) + SKK/sertifikat
- [ ] Surat dukungan pemasok / garansi / layanan purnajual (bila diminta)
- [ ] Rencana keselamatan konstruksi (RKK) (konstruksi, bila diminta)
- [ ] Bukti TKDN / PDN (bila dipersyaratkan)

**Harga**
- [ ] Rincian harga (daftar kuantitas & harga): volume sama dengan dokumen, **volume × harga satuan** benar, subtotal, PPN (bila PKP), total → jalankan `scripts/cek_penawaran.py`
- [ ] Total penawaran **≤ HPS**; cek persen terhadap HPS; bila < 80% siapkan bukti kewajaran harga
- [ ] **Angka = terbilang** di surat penawaran
- [ ] Harga satuan timpang? (satu item jauh di atas HPS satuan) — siap klarifikasi

### B2. Pengadaan langsung (nilai kecil)
- [ ] Undangan/permintaan penawaran dari Pejabat Pengadaan dibaca lengkap
- [ ] Isian kualifikasi/berkas: NIB (KBLI sesuai), NPWP, pakta integritas
- [ ] Surat penawaran + rincian harga (bertanda tangan)
- [ ] Spesifikasi/brosur sesuai permintaan
- [ ] Siap **klarifikasi & negosiasi teknis dan harga**
- [ ] Batas nilai: konstruksi s.d. Rp400 jt; barang/jasa lainnya s.d. Rp200 jt; konsultansi s.d. Rp100 jt (Perpres 46/2025 — PERLU REVIEW)

### B3. E-purchasing (Katalog Elektronik / Toko Daring)
- [ ] Akun penyedia & produk tayang di katalog; data produk (spesifikasi, TKDN, SNI, harga, wilayah kirim, stok) benar
- [ ] Ikuti Peraturan LKPP 2/2026: metode **pembelian langsung, negosiasi harga, mini-kompetisi**; untuk mini-kompetisi siapkan harga ≤ harga tayang/HPS dan jadwal kirim
- [ ] Respons pesanan tepat waktu; siapkan faktur/BAST & dokumen kirim
- [ ] Toko Daring/Bela Pengadaan: pastikan kanal & aturan terbaru di situs INAPROC (sedang transisi ke Peraturan LKPP 2/2026 — PERLU REVIEW)

## C. Pemeriksaan akhir sebelum unggah (H-2 s.d. H-1)
- [ ] Nama paket & kode tender/RUP pada semua surat benar (bukan sisa paket lain)
- [ ] Tanggal surat ≤ batas unggah & masih dalam masa berlaku izin
- [ ] Semua surat ditandatangani & dicap (bila diminta), dipindai jelas
- [ ] Format & ukuran file sesuai ketentuan; file bisa dibuka; tidak dipassword (kecuali diminta)
- [ ] File diunggah ke **kolom yang benar** (administrasi/teknis/harga)
- [ ] Setelah unggah: cek status "terkirim" & simpan bukti
