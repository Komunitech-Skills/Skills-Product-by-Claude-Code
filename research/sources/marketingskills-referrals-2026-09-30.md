# Sumber ATM: marketingskills `referrals` (untuk skill `program-referral-loyalitas`) - 2026-09-30

| Hal | Catatan |
|---|---|
| Sumber | skill `referrals` (SKILL.md v2.0.1 + `references/program-examples.md`, `viral-mechanisms.md`, `affiliate-programs.md`) |
| URL | https://github.com/coreyhaines31/marketingskills (folder `skills/referrals/`) |
| Pembuat | Corey Haines (perorangan; repo koleksi 3-4 skill kita sebelumnya sudah dipakai) |
| Snapshot | `git clone --depth 1` 2026-09-30, commit `5b2c0007766c6a1cf1d53fd8fc73e979e0821022` (commit tanggal 2026-09-04) |
| Lisensi | MIT, Copyright (c) 2025 Corey Haines (file `LICENSE` di root dibaca; disalin ke skill sebagai `LICENSE-MIT-marketingskills`) |
| Sinyal bukti | Bintang ±52 rb, fork ±7,8 rb (GitHub API, dicek 2026-09-30 di `research/` kandidat); aktif (push 5 Sep 2026); dipakai untuk 3 skill kita lain yang sudah lulus; ada folder `evals`. Lolos >= 3 sinyal (popularitas, perawatan, komunitas/fork, isi berstruktur). |
| Audit keamanan | Isi folder `referrals/` = 4 file `.md` + `evals/evals.json`; **tidak ada script** dan tidak ada yang dijalankan. Dibaca seluruhnya: tidak ada instruksi menyuruh agent mengabaikan pengguna, mengirim file, atau menonaktifkan konfirmasi; tidak ada kunci/token tertanam. Rujukan ke `tools/REGISTRY.md` (Rewardful, Tolt, dll.) adalah layanan SaaS pihak ketiga dan tidak dipakai. |
| Skill lain dicek | `churn-prevention` (alur pembatalan & dunning langganan berbasis SaaS): tidak relevan untuk UMKM barang/jasa, tidak dipakai. Tidak ada skill "loyalty" terpisah di repo. |
| Keputusan | **DIPAKAI (ATM, MIT, atribusi).** Nilai tambah: seluruh konteks UMKM Indonesia, script Python `hitung_referral.py` (4 perintah, uji regresi 26 kasus), pola per usaha, anti-curang, S&K, teks WA/IG, kepatuhan UU 8/1999, UU 27/2022, UU 7/2014, dan aturan "tanpa blast". |

## Yang diadaptasi (ide/struktur, ditulis ulang)
- Alur pikir "momen pemicu -> ajakan -> konversi -> hadiah" dan pilihan hadiah satu sisi/dua sisi/bertingkat.
- Saran memicu ajakan di momen puas dan mengurangi gesekan (teks siap pakai).
- Kerangka ukuran: tingkat merujuk, konversi, ROI program, biaya per pelanggan via referral dibanding kanal lain.
- Rumus batas hadiah dari nilai seumur pelanggan dikali margin kotor (dirombak: 30% dari laba kotor seumur pelanggan sebagai aturan praktis berlabel).

## Yang TIDAK dipakai
Program afiliasi SaaS (komisi berulang, buyout ~12x, aturan 20/80 afiliasi, peluncuran afiliasi), mekanisme viral produk digital (badge "Powered by", embed), contoh perusahaan asing (Dropbox, Uber, Notion, Morning Brew), harga dolar, dan tabel integrasi alat SaaS.

## Riset regulasi promosi layanan kesehatan (revisi v1.0.1, dicek 2026-09-30)
Dipicu temuan T2 penguji. Ringkasan untuk skill, **bukan nasihat hukum**; status PERLU REVIEW tenaga medis/hukum.

| Aturan | Isi relevan | Status (per 2026-09-30) | Sumber |
|---|---|---|---|
| Permenkes 1787/MENKES/PER/XII/2010 tentang Iklan dan Publikasi Pelayanan Kesehatan (ditetapkan 13-12-2010, berlaku 27-12-2010) | Pasal 5: iklan/publikasi fasilitas pelayanan kesehatan dilarang, antara lain, mengiklankan **promosi penjualan dalam bentuk apa pun termasuk potongan harga (diskon), imbalan atas pelayanan kesehatan, dan/atau metode MLM**; juga dilarang testimoni di media massa, pujian berlebihan/superlatif, dan mendorong pemakaian layanan yang tidak perlu | Tidak ditemukan pencabutan atau pengganti. Masih dirujuk materi tata kelola pemasaran RS 2026. Status resmi di Hukumonline berbayar (tidak terbaca). | Hukumonline Klinik (2018): https://www.hukumonline.com/klinik/a/ketentuan-iklan-pelayanan-kesehatan-alternatif-di-televisi-lt5ad4049e8a0df/ ; teks: https://kms.kemkes.go.id/contents/1715917225382-bukuperaturaniklanpublikasikes.pdf ; data: https://hukumonline.com/pusatdata/detail/lt4dba32b15ec13/ ; https://galihendradita.wordpress.com/2026/09/19/tata-kelola-digital-marketing-rumah-sakit/ |
| UU 17/2023 tentang Kesehatan, Pasal 453 | Peraturan pelaksanaan UU kesehatan lama "dinyatakan masih tetap berlaku sepanjang tidak bertentangan dengan ketentuan dalam Undang-Undang ini" | Berlaku | https://pasal.id/peraturan/uu/uu-no-17-tahun-2023/pasal-453 ; https://peraturan.bpk.go.id/Details/258028/uu-no-17-tahun-2023 |
| PP 28/2024 (pelaksanaan UU 17/2023) | Mengatur antara lain larangan diskon/hadiah untuk susu formula (Pasal 33) dan iklan kosmetik/produk tertentu; **tidak ditemukan** pasal yang mencabut Permenkes 1787/2010 atau mengizinkan diskon/imbalan layanan kesehatan | Berlaku | https://peraturan.bpk.go.id/details/294077/pp-no-28-tahun-2024 ; https://nasional.kompas.com/read/2024/07/31/11451181/ |
| Permenkes 44/2018 Promosi Kesehatan Rumah Sakit | Promosi kesehatan (edukasi) RS; dibaca harmonis dengan UU 17/2023 | Berlaku (dirujuk 2026) | sumber galihendradita di atas |
| Kode Etik Kedokteran Gigi Indonesia (KODEKGI, PB PDGI; SKEP/034/PB PDGI/V/2008, edisi buku 2020) | Pasal 3 (kemandirian profesi): dokter gigi dilarang promosi dalam bentuk apa pun seperti memuji diri, mengiklankan alat/bahan, memberi janji langsung/tidak langsung agar pasien datang. MKEKG PDGI (2022): "promosi yang dilarang ... adalah memberi diskon" | Berlaku | https://fkg.unair.ac.id/en/wp-content/uploads/2021/06/Buku-Kode-Etik-Kedokteran-Gigi-2020.pdf ; https://www.nusabali.com/berita/132576/rawan-langgar-kode-etik-dokter-gigi-harus-hati-hati-di-media-sosial (18-12-2022) |
| Kode Etik Kedokteran Indonesia (KODEKI 2012, IDI) | Dokter tidak boleh memuji diri/beriklan berlebihan; kemandirian profesi (tidak dipengaruhi imbalan) | Berlaku | https://www.researchgate.net/publication/320334796 |

**Kesimpulan untuk skill (v1.0.1):**
1. Fasilitas/praktik kesehatan (klinik, RS, praktik dokter/dokter gigi/bidan, apotek untuk layanan kefarmasian, lab, fisioterapi, klinik kecantikan dengan tindakan medis): skill **tidak merancang** referral berimbalan, diskon layanan medis, poin/cashback atas layanan, atau komisi rujukan pasien.
2. Alternatif patuh yang dirancang: program edukasi (kelas/materi), pengingat kontrol (draf dikirim staf; skill `pengingat-pasien-klinik`), kartu info/"kartu keluarga sehat" tanpa imbalan untuk merujuk, informasi tarif yang jelas dan jujur.
3. Hadiah produk non-medis untuk pengajak: **tidak dirancang secara default** karena Pasal 5 memakai frasa "dalam bentuk apa pun" dan kode etik melarang janji/imbalan agar pasien datang. Hanya boleh dibahas bila pemilik sudah mendapat konfirmasi tertulis dari dinas kesehatan/organisasi profesi; itu pun tidak dipublikasikan sebagai iklan.
4. Toko ritel non-fasyankes yang menjual produk umum (mis. toko perlengkapan bayi, skincare kosmetik terdaftar) tetap memakai pola ritel biasa, tanpa klaim kesehatan.
5. Belum diverifikasi: teks resmi Pasal 5 langsung dari berkas pemerintah (PDF tidak terbaca otomatis; dikutip via Hukumonline), kode etik bidan/apoteker. Tandai **PERLU REVIEW tenaga medis/hukum**.
