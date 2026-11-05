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

## A. Skill yang sudah rilis: DIKOREKSI setelah isi skill diperiksa (2026-11-05)
Versi awal bagian ini (menyebut `pph-final-umkm` "paling mendesak") **keliru**: agen riset hanya membaca berita dan tidak memeriksa isi skill. Pemeriksaan isi (grep) menunjukkan:
- `pph-final-umkm` 1.0.6 sudah mengacu PP 55/2022 jo. PP 20/2026 dan mencatat "dicek ke naskah resmi 14 Oktober 2026" (rincian di `references/regulasi.md`). Tidak perlu diperbarui hanya karena temuan ini.
- `slip-gaji-bpjs` (dicek ulang 15 Okt 2026), `harga-jual-marketplace` (DJP SP-23/2026, dicek 13 Okt), `gaji-umkm` (26 Sep), `hitung-thr` (23 Sep, sudah menyebut cuti bersama), `kalender-pajak` (25 Sep), `pengajuan-kur` (23 Sep) sudah memuat dasar dan tanggal verifikasi; sebagian besar sudah menyebut 2027.
- Yang benar-benar baru dan belum diverifikasi: (1) UMP/UMK 2027 (belum final; dasar hukumnya masih diperdebatkan), (2) UU Pelindungan Ketenagakerjaan (dikabarkan disahkan 6 Okt 2026, transisi 1 tahun; dampak ke PKWT/pesangon), (3) KUR 2027 (belum diputuskan), (4) wajib halal UMK sejak 18 Okt 2026 (belum ada skill). Tiga yang pertama hanya perlu pemeriksaan ulang dan catatan, bukan perombakan, setelah naskah resmi tersedia.
- `promo-kalender` 1.0.4 berstatus BELUM (Telegram 6) karena alasan lain, tidak terkait temuan ini.
Sisa pekerjaan A: verifikasi naskah resmi untuk poin (1)–(3), lalu bandingkan baris per baris dengan `references/regulasi.md` tiap skill sebelum mengubah apa pun (Opus untuk skill pajak/gaji).

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
