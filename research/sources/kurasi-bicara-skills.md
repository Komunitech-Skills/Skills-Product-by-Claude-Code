# Kurasi: manairalabs/bicara-skills

Tanggal tinjau: 2026-09-23 · Peninjau: agent kurator (sesi terpisah) · Status: **menunggu keputusan koordinator/pemilik**

## 1. Identitas

| Item | Isi |
|---|---|
| Nama | bicara-skills (2 skill: `invoice-extract-id`, `wa-reply-id`) |
| URL | https://github.com/manairalabs/bicara-skills |
| Pembuat | Manaira Labs, dipelihara oleh Nurul Arif Setiawan (github.com/arifsetiawan) |
| Update terakhir | Commit terakhir 2026-09-20 (hanya README). Isi skill dari commit awal 2026-04-17 (v0.1.0). Total 2 commit. |
| **Lisensi (file LICENSE dibaca langsung)** | **MIT**, "Copyright (c) 2026 Manaira Labs". Frontmatter tiap SKILL.md juga menulis `license: MIT`. |
| Popularitas | 0 bintang, 0 fork |

Isi repo: `skills/invoice-extract-id/` (SKILL.md 139 baris, examples/faktur-pajak.md, examples/kwitansi-umkm.md), `skills/wa-reply-id/` (SKILL.md 198 baris, examples/scenarios.md), README EN+ID, CHANGELOG, CONTRIBUTING, `.github/workflows/ci.yml`.

### Ringkasan isi
- **invoice-extract-id**: mengubah nota, kwitansi, faktur pajak, PO, surat jalan, dan bukti transfer menjadi JSON baku (vendor, NPWP, item, DPP, PPN, PPh, meterai, total, terbilang, rekening). Ada aturan normalisasi NPWP, deteksi tarif PPN, kode PPh, cek konsistensi angka, dan jebakan umum (format angka Indonesia, NPWP "-" dianggap kosong, jangan mengarang item).
- **wa-reply-id**: membuat draf balasan CS WhatsApp dalam 3 register (Formal-Friendly, Casual-Warm, Strictly-Formal), 7 pola skenario (harga, stok, status kirim, komplain, refund, promo, pesan tak jelas), daftar larangan, dan katalog frasa EN→ID.

## 2. Audit keamanan (Tahap 3)

Metode: file diunduh ke scratchpad (di luar repo) untuk **dibaca saja**; tidak ada yang dieksekusi.

| Pemeriksaan | Hasil |
|---|---|
| Script dalam skill | Tidak ada. Skill murni Markdown. |
| Jaringan / kirim data keluar | Tidak ada. Hanya tautan dokumentasi (manairalabs.com, bicara.ai, npmjs `@manairalabs/id-locale`). |
| Kredensial / SSH / data browser | Tidak ada. `.gitignore` hanya mengecualikan `.env`. |
| `curl \| bash`, obfuscation, base64 | Tidak ada. |
| CI workflow | Hanya lint frontmatter (`pip install pyyaml` di runner GitHub). Tidak relevan untuk kita dan tidak ikut disalin. |
| Prompt injection di SKILL.md | Tidak ada. Tidak ada perintah mengabaikan pengguna, mengirim file, atau mematikan konfirmasi. |
| Karakter tersembunyi (zero-width, bidi) | Tidak ada (dipindai dengan skrip). |
| API key / data pribadi tertanam | Tidak ada. Contoh memakai nama PT fiktif dan NPWP contoh. |

**Hasil: LULUS.**

Catatan kecil: bagian "See also" mengarahkan ke paket npm milik pembuat. Hapus saat adaptasi karena kita tidak boleh bergantung pada paket luar.

## 3. Penilaian

### invoice-extract-id
- **Kualitas: 6/10.** Kontrak output dan aturan cek angka bagus. Namun **aturan pajaknya sudah usang untuk era Coretax (2025–2026)**:
  1. Contoh faktur tertanggal 15 Jan 2026 menghitung PPN = 12% × DPP penuh. Menurut PMK 131/2024, barang non-mewah memakai **DPP nilai lain 11/12**, jadi efektif 11%. Cek konsistensi `dpp × rate ≈ ppn` akan salah menandai faktur yang benar.
  2. Nomor seri faktur ditulis format lama 16 digit (`010.000-25.xxxxxxxx`). Di Coretax (PER-11/PJ/2025) NSFP menjadi **17 digit** dan diberikan otomatis.
  3. NITKU dicontohkan `0000000000` (10 digit). Yang benar **22 digit** (16 digit NPWP + 6 digit kode tempat usaha).
  4. NPWP contoh masih 15 digit. Badan kini memakai NPWP 16 digit (15 digit hanya sebagai format lama).
  5. Contoh barang (tepung terigu, gula, minyak goreng curah) sebagian bisa dibebaskan atau ditanggung pemerintah PPN-nya. Contoh ini menyesatkan jika dipakai sebagai acuan.
  6. Output hanya JSON. Untuk pembeli awam kurang siap pakai (mereka butuh tabel yang bisa ditempel ke Excel/Google Sheets).
- **Tumpang tindih** dengan katalog kita: tidak ada skill ekstraksi dokumen. Berkaitan dengan `hitung-ppn`, `buat-invoice`, `rekonsiliasi-bank`, `laporan-keuangan-emkm`, `tagih-piutang` (hasil ekstraksi bisa menjadi input skill-skill itu).
- **Keputusan: KURASI** (MIT, izinkan komersial) **dengan perombakan besar**. Tidak boleh dijual apa adanya.

### wa-reply-id
- **Kualitas: 7/10.** Register dan pola skenario rapi, bahasanya natural, contoh realistis.
- **Tumpang tindih kuat** dengan `balas-chat-cs` kita (draft), yang cakupannya sudah lebih luas (WA dan chat marketplace, bank quick reply).
- **Keputusan: KURASI parsial, digabung ke `balas-chat-cs`**, bukan dijual sebagai skill terpisah. Bagian yang layak diambil: tabel tiga register dengan sinyal pemilihnya, larangan "passive-aggressive" dan "janji yang tak bisa dipastikan", dan katalog frasa ramah vs formal. Jika diambil, cantumkan atribusi MIT di `ATTRIBUTION.md` `balas-chat-cs`. Jika pemilik ingin `balas-chat-cs` tetap 100% orisinal, perlakukan sebagai inspirasi saja.

## 4. Usulan nilai tambah (untuk invoice-extract-id → nama usulan `ekstrak-nota-faktur`)

1. **Perbarui ke aturan Coretax:** NSFP 17 digit, NPWP 16 digit, NITKU 22 digit, DPP nilai lain 11/12 (PMK 131/2024), 12% penuh hanya untuk barang mewah, dan kasus PPN dibebaskan/DTP. Cantumkan dasar aturan beserta tanggal berlakunya (rujuk `research/sources/regulasi-2026-09-23.md`).
2. **Script Python standar** `scripts/cek_faktur.py`: validasi panjang NPWP/NITKU/NSFP, cek DPP/PPN/total dengan dua skenario (11/12 dan penuh), dan pembuatan terbilang untuk dicocokkan dengan dokumen. Angka dihitung, bukan dikira.
3. **Output ganda:** tabel siap tempel ke Excel/Sheets (CSV) plus JSON opsional untuk pengguna teknis. Tambahkan mode "banyak nota sekaligus" untuk rekap bulanan.
4. **Contoh lokal baru** dari hasil uji sendiri: nota warung tulisan tangan, struk minimarket, faktur Coretax, bukti transfer BCA/BRI/QRIS, invoice jasa dengan PPh 23.
5. Frontmatter hanya `name` dan `description` (buang `license` dan `version`). Hapus rujukan paket npm.
6. Disclaimer pajak dan arahan ke konsultan. Penanganan foto buram: tandai nilai yang kurang yakin, jangan ditebak.
7. Usulan tier: **ECER** (nilai tinggi untuk admin keuangan/UMKM), atau masuk bundle "Paket Admin Keuangan".

## 5. Kewajiban lisensi jika dipakai
- Sertakan teks lisensi MIT asli (Copyright (c) 2026 Manaira Labs) dan atribusi di `ATTRIBUTION.md` skill turunan.
- Catat di `catalog.csv`: `jalur=kurasi`, `sumber_url=https://github.com/manairalabs/bicara-skills`, `lisensi=MIT`.
