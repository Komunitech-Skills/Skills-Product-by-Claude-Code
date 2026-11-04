# Ringkasan riset 2026-11-04 (4 jalur) dan urutan kerja usulan

Sumber rinci (semua di `research/sources/`):
- `riset-2026-11-04-celah-katalog.md`: 25 ide dari celah katalog (tanpa web).
- `riset-2026-11-04-musiman-regulasi.md`: perubahan aturan/musiman Nov 2026–Mar 2027 (berita; **8 butir BELUM TERVERIFIKASI**).
- `riset-2026-11-04-kurasi-baru.md`: 17 kandidat skill publik.
- `riset-2026-11-04-software-pengganti-saas-baru.md`: 13 kandidat software lokal.

## Peringatan keandalan (baca dulu)
- Temuan aturan di jalur musiman berasal dari **hasil pencarian berita**; naskah resmi (peraturan.go.id, pajak.go.id, Kemnaker, BPJPH) belum dibuka. Jangan masukkan angka/tanggal ke skill atau materi jualan sebelum dicek.
- Jalur kurasi tidak bisa memakai `gh`/API (diblokir): tanggal rilis pertama banyak yang "?", isi tiap skill belum dibaca. Catatan bahwa `anthropics/skills` (theme-factory, canvas-design, brand-guidelines) kini Apache-2.0 **bertentangan** dengan catatan 2026-09-23 ("proprietary"): wajib dibuka berkas LICENSE-nya sebelum salin-edit.
- Jalur celah katalog hanya memeriksa duplikat lewat nama skill (file riset VIP/KPI tidak dibaca). Ide no. 8, 12, 13, 22 dekat dengan skill yang sudah ada: cek ulang.

## A. Perbaikan skill yang sudah rilis (prioritas tertinggi; skill pajak/gaji = Opus + verifikasi angka)
Syarat: naskah resmi dibaca dulu. Daftar dari jalur musiman:
1. `pph-final-umkm`: cocokkan dengan PP 20/2026 (PPh final 0,5% tanpa batas waktu untuk OP/PT Perorangan; CV/PT biasa tarif normal).
2. `gaji-umkm`, `slip-gaji-bpjs`, `hitung-thr`: UMP/UMK 2027 belum final (target akhir Nov); UU Pelindungan Ketenagakerjaan (disebut disahkan 6 Okt 2026, transisi 1 tahun).
3. `kalender-pajak`, `promo-kalender`: libur 2027 (SKB 15 Sep 2026: 18 libur nasional + 8 cuti bersama), Harbolnas, Coretax.
4. `harga-jual-marketplace`: biaya logistik/komisi marketplace berubah Mei 2026.
5. `pengajuan-kur`: plafon/bunga KUR 2026 (flat 6%); KUR 2027 belum diputuskan.

## B. Skill baru, urut usulan (dikerjakan hanya setelah rilis yang ada selesai; prinsip no. 28)
| Urut | Nama usulan | Skor | Mengapa sekarang | Syarat |
|---|---|---|---|---|
| 1 | `rekonsiliasi-payout-marketplace` | 24 | Tidak bergantung perubahan aturan; seller online rutin | script, uji dengan CSV contoh |
| 2 | `peta-biaya-marketplace-2027` | 23 | Biaya berubah Mei 2026; tarif **diisi pengguna** (tidak mengunci tarif) | script; digabung/diselaraskan dengan `harga-jual-marketplace` |
| 3 | `persiapan-harbolnas` | 21 | 12.12 masih ±5 minggu; 11.11 terlalu dekat | tanpa klaim aturan |
| 4 | `cek-halal-usaha-kuliner` | 22 | Wajib halal UMK dilaporkan berlaku 18 Okt 2026 | **PERLU REVIEW** aturan (PP 42/2024, BPJPH) |
| 5 | `siap-umk-2027-penggajian` | 21 | UMP ditetapkan Nov–Des | **tunggu angka resmi** |
| 6 | `hitung-lembur-dan-cuti` | 22 | Kebutuhan HR tinggi | verifikasi PP 35/2021 + UU baru; Opus |
| 7 | `tutup-buku-bulanan` + `tutup-buku-akhir-tahun` | 20 / 19 | Des–Jan | gabung satu skill bila mungkin |
| 8 | `siap-lebaran-2027`, `persiapan-spt-badan-umkm` | 21 | Q1 2027 | tunggu verifikasi aturan |
| 9 | `tangani-retur-refund-marketplace`, `jadwal-shift-karyawan` | 22 / 21 | Celah kategori E-commerce/HR | tanpa klaim aturan |

Kategori tertipis (celah): Coding & DevOps 0 skill (ide: `keamanan-akun-digital-usaha`, `backup-data-usaha-lokal`, `rapikan-folder-file-massal`), Kehidupan Pribadi 1, Pendidikan 2. Legal tidak diperluas (keputusan pemilik).

## C. Kurasi skill publik (setelah verifikasi LICENSE di berkas repo)
- `career-ops` (MIT): skor lowongan + tailor CV. Uji banding dulu dengan skill HR/CV yang ada (`cv-lamaran-ats`, dll.).
- `anthropics/skills` theme-factory/canvas-design/brand-guidelines: **cek LICENSE** (klaim Apache-2.0 vs catatan lama proprietary); `docx` tetap proprietary.
- `mattpocock/skills` (MIT, selektif): hanya yang cocok audiens awam.
- `humanizer` (MIT): uji banding melawan `tulisan-tanpa-kesan-ai`.
- Ditolak: KalarisLabs (slop: 281 skill dalam 32 commit), `openai/skills` curated, `awesome-copilot`, `duckdb-skills`, `kostja94`.

## D. Software lokal (panduan + pemasangan terarah)
- Kurasi pembeli: **Vibe** (MIT, transkripsi rapat offline, ada CLI/HTTP API), **Syncthing** (MPL-2.0), **Kopia** (Apache-2.0), **DocuSeal** (AGPL-3.0, bersyarat; tanda tangan bukan TTE tersertifikasi, atribusi wajib), **Kimai** (AGPL-3.0, bersyarat). Cadangan: Buzz, LubeLogger.
- Internal / jasa setup: Paperless-ngx, Snipe-IT, Easy!Appointments, OCRmyPDF.
- Tolak: Docmost, GanttProject.
- Syncthing + Kopia cocok digabung dengan ide `backup-data-usaha-lokal`.

## E. Yang tidak dikerjakan otomatis
Memasang software dari sumber luar, skill hukum baru, perubahan bot produksi, pesan ke luar grup uji.
