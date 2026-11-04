# Riset software pengganti SaaS (kebutuhan BELUM tertutup) — 2026-11-04

Metode: hanya baca halaman GitHub/rilis lewat WebFetch (tidak ada yang dipasang/dijalankan). Lisensi diambil dari label lisensi repo dan teks LICENSE bila dibuka (Kimai, DocuSeal). Bintang dibulatkan seperti tampil di GitHub. Tahun rilis tidak selalu tampil di halaman; ditandai "(tahun tidak tampil)". Item bertanda ? perlu diverifikasi ulang sebelum dikurasi.

Tidak diulang (sudah ada skill/riset): Dolibarr, Odoo, Frappe Books, Actual Budget, hledger, Kanboard, Vikunja, Fider, InvenTree, SiYuan, notebook-riset-lokal, Grist, Listmonk, Umami, Uptime Kuma, Healthchecks, Datasette, OpenRefine, pdf-lokal (Stirling-PDF), arsip-nota, kasir-lokal.

Celah yang dituju: transkripsi rapat lokal, backup/sinkron berkas, OCR/arsip dokumen, e-sign, aset, waktu/penagihan jam kerja, wiki tim, booking, Gantt, kendaraan.

## Tabel kandidat

| # | Software | URL | Lisensi | Bintang | Rilis terakhir | Pasang tercepat | Agent (CLI/API) | Sumber daya | Awam | Risiko | Keputusan |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Vibe** (transkripsi offline, Whisper) | github.com/thewh1teagle/vibe | MIT | 8,0 rb | v3.3.0, 29 Okt 2026 | Installer Win/macOS dari halaman unduh proyek | **CLI + HTTP API (Swagger)** | CPU cukup; GPU opsional; model unduh ratusan MB-GB | Tinggi (aplikasi desktop) | Rendah. Installer mungkin tak bertanda tangan; unduhan model | **KURASI pembeli** (transkripsi rapat/voice note WA; tidak ada biaya per menit) |
| 2 | **Buzz** (transkripsi offline) | github.com/chidiwilliams/buzz | MIT | 22,4 rb | v1.4.5, 23 Agu (tahun tidak tampil; sebelumnya 14 Mar) | Installer Win/macOS (SourceForge); macOS hanya Apple silicon sejak setelah 1.4.5 | CLI (otomasi) | Sedang | Tinggi | Rilis jarang (~5 bln); installer tak bertanda tangan (peringatan SmartScreen/Gatekeeper); Mac Intel tidak didukung | **KURASI sebagai cadangan Vibe** (pilih Vibe dulu) |
| 3 | **Syncthing** (sinkron berkas P2P) | github.com/syncthing/syncthing | MPL-2.0 | 90,1 rb | v2.1.7, 21 Okt 2026 | Biner bertanda tangan Win/macOS; pembungkus GUI pihak ketiga | REST API bawaan (README tidak menyebut; dokumentasi resmi ? verifikasi) | Sangat ringan | Sedang (GUI web lokal, konsep perangkat ID) | Rendah. MPL-2.0 per berkas, aman dijual sebagai panduan | **KURASI pembeli** (pengganti Dropbox/Drive untuk sinkron antar laptop & backup ke HP) |
| 4 | **Kopia** (backup terenkripsi) | github.com/kopia/kopia | Apache-2.0 | 14,6 rb | v0.23.1, 16 Jun 2026 | KopiaUI (desktop) Win/macOS; CLI | **CLI** (+ server REST, ? verifikasi) | Ringan | Sedang | Rilis terakhir ~4,5 bln (masih dalam batas 6 bln, menipis); versi 0.x | **KURASI pembeli** (backup harian otomatis ke disk eksternal/cloud sendiri). Alternatif: restic (BSD-2, belum dicek) |
| 5 | **OCRmyPDF** (OCR PDF hasil scan) | github.com/ocrmypdf/OCRmyPDF | MPL-2.0 (kode non-inti MIT, dokumen CC-BY-SA 4.0) | 35,2 rb | v17.13.0, 28 Sep (tahun tidak tampil) | macOS: `brew install ocrmypdf`; Windows: tidak mulus (WSL, atau Tesseract + Python) | **CLI** matang | Ringan-sedang | **Rendah di Windows** | Pemasangan Windows menyulitkan awam | **KURASI internal/skill panduan terbatas** (dipasang oleh Komunitech/jasa setup); cocok digabung `pdf-lokal` & `arsip-nota` |
| 6 | **Paperless-ngx** (arsip dokumen + OCR) | github.com/paperless-ngx/paperless-ngx | GPL-3.0 | 47,7 rb | v3.4.2, 3 Nov (tahun tidak tampil) | **Docker Compose** (utama); Windows/macOS lewat Docker Desktop | REST API (dokumentasi resmi, ? halaman utama tidak menyebut) | Docker + ±2-4 GB RAM | **Rendah** | Butuh Docker; berat untuk awam | **INTERNAL Komunitech + jasa setup** (arsip kontrak/invoice klien). Bukan produk ecer |
| 7 | **DocuSeal** (tanda tangan elektronik) | github.com/docusealco/docuseal | AGPL-3.0 + **Section 7(b)**: atribusi DocuSeal wajib tetap tampil di UI. Fitur Pro berbayar terpisah | 19,0 rb | 3.3.5, 2 Nov (tahun tidak tampil) | `docker run -p 3000:3000 -v.:/data docuseal/docuseal` (SQLite) | API & webhook | Ringan (SQLite) | Sedang (butuh Docker) | Atribusi wajib (boleh); TTE tidak tersertifikasi (lihat catatan riset 2026-09-23); tautan tanda tangan ke pihak luar butuh URL publik | **KURASI pembeli bersyarat** (penandatanganan lokal/jaringan kantor); sertakan peringatan hukum UU ITE & tanpa klaim "tersertifikasi" |
| 8 | **Kimai** (pencatat jam kerja + invoice jam) | github.com/kimai/kimai | AGPL-3.0 (teks LICENSE tampak tak diubah; ada pasar plugin berbayar) | 5,1 rb | 2.71.0, 25 Okt (tahun tidak tampil) | Docker/Docker Compose; PHP | JSON API (token) | Server kecil | Rendah-sedang | Plugin berbayar tidak boleh dibundel | **KURASI pembeli bersyarat** (freelancer/konsultan: tagih per jam; Docker). Cadangan: kerjakan setelah #1-#4 |
| 9 | **Snipe-IT** (aset & inventaris kantor) | github.com/snipe/snipe-it | AGPL-3.0 | 15,1 rb | v8.8.3, 22 Okt (tahun tidak tampil) | Docker Compose / web server | **REST API JSON** | Server (PHP+MySQL) | Rendah | Berat untuk UMKM kecil | **INTERNAL Komunitech** (aset laptop tim) / jasa setup untuk usaha mapan |
| 10 | **Easy!Appointments** (booking janji) | github.com/alextselegidis/easyappointments | GPL-3.0 (konten CC-BY 3.0) | 4,5 rb | tidak tampil di halaman (? verifikasi) | PHP 8.2+, MySQL, Apache/Nginx | openapi.yml di repo (REST) | Server | Rendah; butuh URL publik untuk pelanggan | Butuh hosting publik, bukan lokal murni | **INTERNAL / jasa setup** (booking mentoring); bukan produk ecer |
| 11 | **Docmost** (wiki/dokumen tim) | github.com/docmost/docmost | AGPL-3.0 (folder `ee` lisensi komersial, jangan dibundel) | 22,2 rb | tidak tampil (? verifikasi) | Docker Compose | API tidak terdokumentasi di halaman (? verifikasi) | Server (Postgres+Redis) | Rendah | Overlap dengan SiYuan/Logseq yang sudah ada | **TOLAK untuk pembeli** (tumpang tindih); opsional internal |
| 12 | **GanttProject** (jadwal proyek Gantt) | github.com/bardsoftware/ganttproject | GPL-3.0 | 1,1 rb | tidak tampil (? verifikasi) | Aplikasi desktop Java (halaman unduh resmi ? verifikasi) | Tidak ada CLI terdokumentasi di README; berkas .gan (XML) bisa disunting agent | Ringan | Sedang | Bintang jauh di bawah ambang (≥500 OK, tapi komunitas kecil) dan butuh Java | **TOLAK untuk sekarang** (Vikunja/Kanboard sudah menutup; skor rendah) |
| 13 | **LubeLogger** (servis & BBM kendaraan) | github.com/hargata/lubelog | MIT | 2,9 rb | tidak dicek | Windows standalone `.exe` atau Docker | API tidak disebut (? verifikasi) | Sangat ringan | Tinggi | Pasar sempit (usaha armada kecil/ojek/rental) | **KURASI niche, prioritas rendah** |

## Terbukti dari pencarian tapi tidak dicek mendalam
Restic (backup, BSD-2), Cal.com (MIT, sudah dicatat 2026-09-23 sebagai berat), Documenso/OpenSign (AGPL, mirip DocuSeal), Formbricks/HeyForm (formulir, butuh server publik), Moodle/Frappe LMS (LMS berat), RustDesk (akses jarak jauh, AGPL, ? verifikasi). Belum ada kandidat lokal-ringan yang kuat untuk: penjadwalan staf, LMS, kasir desktop baru di luar Frappe Books/Dolibarr.

## Keputusan ringkas
- **Kurasi untuk pembeli:** Vibe (MIT), Buzz (MIT, cadangan), Syncthing (MPL-2.0), Kopia (Apache-2.0), DocuSeal (AGPL-3.0 + 7b, bersyarat), Kimai (AGPL-3.0, bersyarat), LubeLogger (MIT, prioritas rendah).
- **Internal Komunitech / jasa setup:** Paperless-ngx (GPL-3.0), Snipe-IT (AGPL-3.0), Easy!Appointments (GPL-3.0), OCRmyPDF (MPL-2.0, terbatas).
- **Tolak:** Docmost (tumpang tindih, ada folder komersial), GanttProject (tumpang tindih, kecil).
- Tidak ada yang ditolak karena lisensi non-komersial; tidak ada BSL/ELv2 yang ditemukan di daftar ini.

## 5 teratas (urutan kerja)
1. Vibe — MIT — transkripsi rapat & voice note, ada CLI + HTTP API, paling cocok untuk awam.
2. Syncthing — MPL-2.0 — sinkron/backup antar perangkat tanpa cloud berbayar.
3. Kopia — Apache-2.0 — backup terenkripsi terjadwal (pantau rilis; terakhir Jun 2026).
4. DocuSeal — AGPL-3.0 + atribusi — tanda tangan dokumen lokal (disclaimer TTE tidak tersertifikasi).
5. Kimai — AGPL-3.0 — pencatat jam & tagihan freelancer.

## Catatan verifikasi sebelum membuat skill
- Tahun rilis banyak yang tidak tampil di halaman rilis; cek tanggal penuh di GitHub saat pembuatan skill.
- Syncthing REST API, Kopia server API, Paperless API, Docmost API, Easy!Appointments rilis: belum dikonfirmasi di sumber ini.
- Uji pasang Docker (DocuSeal, Kimai) belum dilakukan; riset ini hanya membaca dokumentasi.
- Keputusan tier/harga tidak diubah; usulan kurasi saja.
