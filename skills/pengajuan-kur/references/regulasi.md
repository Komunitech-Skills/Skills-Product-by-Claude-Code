# Ketentuan KUR — Dasar Aturan & Status Verifikasi

**Berlaku per: 2026-09-23 (tanggal pengecekan).** Tinjau ulang minimal tiap 6 bulan atau saat terbit Permenko KUR baru.

## Sumber yang dibaca langsung (2026-09-23)
1. **Teks lengkap Permenko Perekonomian No. 1 Tahun 2026 tentang Pedoman Pelaksanaan KUR**. Ditetapkan 5 Januari 2026 dan diundangkan 13 Januari 2026 (Berita Negara 2026 No. 17). Permenko ini mencabut Permenko 1/2022 beserta perubahannya (terakhir Permenko 12/2025). Teks dibaca dari basis data hukum DDTC: https://perpajakan.ddtc.co.id/id/sumber-hukum/peraturan-pusat/peraturan-menteri-koordinator-bidang-perekonomian-1-tahun-2026
2. **Siaran Pers resmi Kemenko Perekonomian** HM.02.04/23/SET.M.EKON.3/01/2026 (27 Jan 2026). Isinya: Permenko 1/2026 berlaku sejak 13 Januari 2026; Super Mikro 3% efektif; Mikro/Kecil sektor produksi & perdagangan berorientasi ekspor 6% efektif; kekayaan intelektual dapat menjadi agunan tambahan. Sumber: https://www.ekon.go.id/publikasi/detail/6784/konsolidasi-kredit-program-pemerintah-2026-perkuat-pedoman-pelaksanaan-kredit-program-optimalkan-penyaluran-dan-wujudkan-pertumbuhan-ekonomi-inklusif-berbasis-usaha-mikro-dan-kecil
3. **Portal kur.ekon.go.id** (halaman Kebijakan KUR, Landasan Hukum, FAQ). Isinya **usang**: daftar landasan hukum berhenti di 2021 dan FAQ masih menyebut bunga 7%. Portal ini hanya dipakai untuk konteks sejarah, bukan untuk angka 2026.

Pencarian 2026-09-23 tidak menemukan perubahan atas Permenko 1/2026. Salinan resmi di JDIH Kemenko (jdih.ekon.go.id) tidak dapat diakses saat pengecekan.

Label status:
- **TERVERIFIKASI-RESMI**: tertulis di teks Permenko 1/2026 (pasal disebut) dan/atau siaran pers resmi Kemenko. Boleh disebut dengan kalimat "menurut Permenko Perekonomian 1/2026 Pasal …", tetap dengan anjuran konfirmasi ke bank penyalur.
- **BELUM TERVERIFIKASI**: tidak ditemukan di sumber resmi (praktik bank, blog, atau media). Jangan dinyatakan pasti.

## Jenis, plafon, bunga, tenor (TERVERIFIKASI-RESMI)
| Jenis | Plafon per akad | Bunga efektif/tahun | Tenor awal (modal kerja / investasi) | Pasal |
|---|---|---|---|---|
| Super Mikro | ≤ Rp10 juta | **3%** | 3 th / 5 th | 29, 30, 31 |
| Mikro | > Rp10 juta s.d. Rp100 juta | Produksi & perdagangan berorientasi ekspor: **6%**. Perdagangan non-ekspor: **6% (akad ke-1), 7% (akad ke-2)**, paling banyak 2 kali akad | 3 th / 5 th | 36, 37, 38 |
| Kecil | > Rp100 juta s.d. Rp500 juta | Produksi & perdagangan berorientasi ekspor: **6%**. Perdagangan non-ekspor: **6% / 7% / 8% / 9%** untuk akad ke-1 s.d. ke-4; akumulasi penarikan maks. Rp500 juta (termasuk KUR mikro) | 4 th / 5 th | 43, 44, 45 |

Catatan pasal:
- Setiap pasal bunga berbunyi "…% efektif per tahun, dengan Suku Bunga/Marjin **flat/anuitas yang setara menyesuaikan**" (Pasal 30, 37, 44). Artinya bila bank menyebut bunga flat, angkanya harus setara dengan bunga efektif tersebut, dan angka flat itu lebih kecil. Contoh: 6% efektif untuk 36 bulan setara ±3,17% flat. Angka ini dihitung script lewat `--kur`.
- Sektor produksi = kegiatan yang menghasilkan barang/jasa **di luar sektor perdagangan** (Pasal 1 angka 2). Perdagangan berorientasi ekspor harus dibuktikan dengan dokumen proses ekspor (Pasal 36 ayat 3, Pasal 43 ayat 3).
- Tenor dapat diperpanjang (di luar restrukturisasi): Super Mikro sampai 4 th (modal kerja) / 7 th (investasi); Mikro dan Kecil sampai 5 th / 7 th. Grace period mengikuti ketentuan penyalur (Pasal 31, 38, 45).
- Debitur graduasi dari Super Mikro: akad awal di Mikro/Kecil dihitung sebagai akad pertama (Pasal 37 ayat 2, Pasal 44 ayat 2).
- Ada juga jenis KUR khusus dan KUR penempatan Pekerja Migran Indonesia (Pasal 24). Keduanya di luar cakupan skill ini; arahkan ke bank.

## Agunan (TERVERIFIKASI-RESMI)
- Agunan pokok adalah usaha atau objek yang dibiayai. Agunan tambahan bisa berupa aset berwujud maupun tidak berwujud, **termasuk kekayaan intelektual** (Pasal 19).
- Untuk plafon **s.d. Rp100 juta**, penyalur **tidak diperbolehkan** mensyaratkan agunan tambahan (Pasal 20 ayat 1). Jika dilanggar, subsidi bunga untuk debitur tersebut tidak dibayarkan kepada penyalur (Pasal 21).
- Untuk plafon di atas Rp100 juta, agunan tambahan dapat diberlakukan. Pengecualian: petani tebu rakyat dan KUR khusus pertanian dengan offtaker sebagai avalis (Pasal 20 ayat 2).
- Pemerintah menegaskan ulang aturan ini pada Agustus 2026 dan meminta masyarakat melapor bila diminta agunan tambahan atau pungutan. Status: dilaporkan media (Antara, CNN Indonesia, 3–4 Agustus 2026), sejalan dengan Pasal 20.

## Biaya & pencairan
| Fakta | Status |
|---|---|
| Jumlah KUR yang diterima debitur **harus sesuai** dengan jumlah di akad (Pasal 13 ayat 2), jadi tidak boleh ada potongan dari nilai pencairan | TERVERIFIKASI-RESMI |
| "Tanpa biaya provisi & administrasi" | **BELUM TERVERIFIKASI**. Kata "provisi" tidak ditemukan di teks Permenko 1/2026. Sampaikan hanya sebagai: "tanyakan rincian biaya (asuransi, notaris, materai) ke bank; nilai yang cair harus sama dengan nilai akad". |

## Syarat calon penerima (TERVERIFIKASI-RESMI, Pasal 27, 34, 41)
| Syarat | Super Mikro | Mikro | Kecil |
|---|---|---|---|
| Usaha produktif & layak, berjalan **≥ 6 bulan** | Ya. Jika < 6 bulan: ikut pendampingan/pelatihan, tergabung kelompok usaha, atau punya anggota keluarga yang sudah berusaha (Pasal 27 ayat 2) | Ya. Pengecualian: pekerja terkena PHK dengan usaha ≥ 3 bulan + pelatihan kewirausahaan; petani tebu dengan offtaker | Ya. Pengecualian: petani tebu dengan offtaker |
| **NIB atau surat keterangan usaha** mikro/kecil dari pejabat berwenang | Ya | Ya | Ya |
| **NIK** (KTP-el atau surat keterangan pembuatan KTP-el) | Ya | Ya | Ya |
| **NPWP** | Tidak disebut | Hanya jika pinjaman **> Rp50 juta** | **Wajib** |
| Belum pernah menerima kredit/pembiayaan **komersial** | Ya | Ya | Ya |

- Pengecualian "kredit komersial" (Pasal 27 ayat 3, 34 ayat 3, 41 ayat 3): kredit konsumsi rumah tangga; kredit ultra mikro s.d. Rp20 juta; pinjaman **fintech P2P/pembiayaan digital**; kredit konsumtif s.d. Rp500 juta yang tercatat sebagai produktif.
- Boleh **sedang** menerima kredit berikut, asalkan kolektibilitas lancar (Pasal 28, 35, 42): KPR, kredit/leasing motor roda dua untuk tujuan produktif, kredit dengan jaminan SK pensiun, kartu kredit, kredit resi gudang, kredit konsumsi rumah tangga.
- Penyalur mengecek kelayakan lewat **SLIK** OJK. Bila masih tercatat ada baki debet kredit produktif yang sebenarnya sudah lunas, siapkan **surat keterangan lunas/roya** plus bukti cetak rekening dari pemberi kredit sebelumnya (Pasal 14).

## Masih BELUM TERVERIFIKASI (praktik per bank, jangan dinyatakan pasti)
- Kartu Keluarga, surat nikah/KTP pasangan, pas foto, mutasi rekening, foto usaha: umum diminta bank, tetapi **tidak** tercantum di Permenko. Beri tanda "cek ke bank penyalur".
- Metode angsuran & pembulatan tiap bank. Minta tabel angsuran resmi.
- Lama proses pencairan.

## Aturan pemakaian di skill
1. Bunga pada simulasi diisi dari bank/pengguna. Jika belum ada, jalankan script dengan `--kur --sektor … --akad-ke …` agar dipakai **bunga acuan Permenko 1/2026** berlabel "acuan … konfirmasi ke bank penyalur". Bila sektor tidak diketahui, pakai contoh 6% dengan `--bunga-contoh`.
2. Syarat yang TERVERIFIKASI-RESMI boleh disebut beserta pasalnya. Tetap tulis "konfirmasi ke bank penyalur", karena bank juga menilai kelayakan sendiri (Pasal 28/35/42 ayat 3).
3. Checklist dokumen tambahan (KK, surat nikah, dll.) selalu bertanda **"cek ke bank penyalur"**.
4. Jangan menjanjikan persetujuan, plafon yang akan disetujui, atau lama proses.
5. Hak debitur yang boleh disampaikan dengan pasti: plafon ≤ Rp100 juta tanpa agunan tambahan (Pasal 20) dan nilai cair = nilai akad (Pasal 13 ayat 2).
