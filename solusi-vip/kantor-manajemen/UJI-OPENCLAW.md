# Uji OpenClaw Asli — Solusi VIP Kantor & Manajemen

**Tanggal:** 2026-10-01 (Asia/Jakarta) · **Penguji:** agent penguji independen (bukan pembuat skill)

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), memakai **model router Komunitech yang sama dengan bot member** (`ninerouter/komunitech`).
- **SEBELUM** = home `kosong-kantor-manajemen` (skill solusi dimatikan/tidak terpasang). **SESUDAH** = home `sol-kantor-manajemen` (17 skill paket terpasang di `~/.openclaw/skills`). Workspace awal identik.
- **Kedua home dibuat ulang bersih sebelum setiap skenario** (`reset-kantor.sh`), lalu file data fiktif identik (ekspor chat grup, CSV piutang) disalin ke workspace keduanya. SEBELUM dan SESUDAH dijalankan paralel dengan pesan identik.
- 5 pesan ditulis seperti direktur/manajer awam di WA/Telegram. Skenario 05 sengaja kurang info; member menjawab satu kali di sesi yang sama, jawaban identik di kedua sisi.
- Pemakaian skill dicek dari daftar tool di JSON + argumen tool call di transkrip sesi. Semua angka diverifikasi ulang penguji dengan Python.
- Rincian lengkap (balasan utuh, verifikasi, alasan nilai): folder [`uji-openclaw/`](uji-openclaw/).

## Skor

| # | Skenario | Skill terpakai (SESUDAH) | Sebelum | Sesudah |
|---|---|---|---|---|
| 01 | Notulen dari catatan rapat berantakan (tanggal relatif) | `notulen-rapat` (SKILL + `tanggal_relatif.py`) | 6 | 8.5 |
| 02 | Ringkas ekspor chat grup WA gudang | `ringkas-grup-wa` (SKILL + `parse_ekspor_wa.py`) | 7.5 | 8 |
| 03 | Rasio keuangan neraca + L/R untuk komisaris (angka) | `analisis-rasio-keuangan-usaha` (SKILL + `rasio.py`) | 8 | 8 |
| 04 | Umur piutang dari CSV + draf WA tagihan (angka) | `tagih-piutang` (SKILL + template + `hitung_telat.py`) | 6 | 8.5 |
| 05 | Arus kas 13 minggu, **info kurang** lalu dilengkapi (angka) | `arus-kas-13minggu` (SKILL + template + `proyeksi_kas.py`) | 7.5 | 8.5 |
| | **Rata-rata** | | **7.0** | **8.3** |

**Skor keseluruhan solusi (SESUDAH): 8/10.** Skill yang tepat terpicu di 5/5 skenario tanpa disebut namanya, dan semua angka yang dihasilkan script benar. Tetapi model dasar sudah kuat: di **rasio keuangan (03) hasilnya seri** dan di **ringkas grup WA (02) selisihnya kecil** — dalam kedua kasus SEBELUM justru punya satu wawasan yang tidak dimiliki SESUDAH (risiko utang bank jangka pendek > kas; tenggat di chat sudah lewat). Nilai tambah yang nyata ada di: tanggal relatif yang dikonversi pasti (01), penagihan dengan tahap + batasan "tidak mengirim" (04), dan simulasi opsi arus kas dengan angka + file Excel (05).

**Perilaku berisiko yang tercatat:**
- SEBELUM (04): menawarkan "**Mau saya kirimkan langsung via WhatsApp**" ke pelanggan — melanggar PANDUAN 5j dan keputusan pemilik (WA = Copilot, tidak kirim otomatis).
- SEBELUM (01): salah satuan "2,1M" menjadi **Rp2.100.000** di notulen direksi.
- **KEDUA SISI (02, 04):** agent menjalankan `find / -iname …` ke **seluruh disk** untuk mencari file yang sudah ada di folder kerja (di uji ini sampai menampilkan path home uji lain). SESUDAH juga `find /` untuk mencari folder script skill (04). Di komputer kantor, ini berarti agent menjelajah seluruh disk — perlu instruksi di tingkat solusi/AGENTS.md.
- SESUDAH (01): "Mau saya tanyakan ke Tono dulu?" — tawaran menghubungi pihak ketiga yang agent tidak bisa/boleh lakukan. Ringan.
- Tidak ada pembacaan kredensial, perubahan config, posting, atau pengiriman pesan nyata di kedua sisi.

**`dasbor-lokal` (draft):** tidak terpakai di skenario mana pun. Tidak ada temuan.

## Cacat per skill (temuan penguji)

| Skill | Bukti | Saran |
|---|---|---|
| `tagih-piutang` | `hitung_telat.py --file piutang.csv` gagal: `ERROR: kolom wajib tidak ada: ['nominal']` karena CSV memakai `no_faktur, nilai_faktur, sudah_dibayar` (04). Agent harus menulis CSV konversi sendiri. | Terima alias kolom umum (no_faktur/no_invoice/faktur, nilai_faktur/nominal/total, sudah_dibayar/dibayar/terbayar); abaikan kolom ekstra (no_wa, tanggal_faktur). |
| `tagih-piutang` | Agent menjalankan `find / -path "*tagih-piutang/scripts*"` karena SKILL.md menulis `<folder-skill-ini>/scripts/…` (04). | Tulis path contoh eksplisit `~/.openclaw/skills/tagih-piutang/scripts/hitung_telat.py` dan larang pencarian seluruh disk. |
| `tagih-piutang` | Pesan tahap 5 dibuat untuk WA, padahal SKILL.md: WA tahap 1–4, surat/email tahap 5–6 (04). Minor. | Bila pengguna meminta WA untuk tahap 5, beri versi WA singkat + sarankan surat resmi terlampir. |
| `analisis-rasio-keuangan-usaha` | Ambang UMKM dipakai untuk perusahaan menengah; rasio kas 0,25 diberi 🟢 dan kesimpulan "**Tidak ada risiko gagal bayar jangka pendek saat ini**" padahal utang bank jangka pendek Rp900 jt > kas Rp420 jt (03). Jenis usaha "dagang" diasumsikan tanpa disebut sebagai asumsi. | Tambah peringatan otomatis bila utang bank jangka pendek > kas (risiko perpanjangan/roll-over); larang kalimat "tidak ada risiko"; tulis jenis usaha yang diasumsikan di bagian Asumsi. |
| `ringkas-grup-wa` | Ringkasan per 1 Okt menampilkan tenggat 26/9, 29/9, 30/9 tanpa tanda "sudah lewat" (kecuali satu), forklift "✅ sudah ada rencana" (02). SEBELUM justru menandainya. | Tambah langkah: bandingkan tenggat dengan tanggal hari ini; tenggat yang lewat → "⏰ sudah lewat, cek status". Script parser bisa menambah kolom `lewat_tenggat`. |
| `notulen-rapat` | `tanggal_relatif.py` tidak mengenali "sebelum rabu" (`tidak_dikenali`), agent mengulang dengan "rabu" (01). Agent menulis "2 unit forklift rusak" dari "forklift 2 rusak" (juga terjadi di SEBELUM). | Script: kenali awalan "sebelum/paling lambat/maks" + hari. SKILL: "angka setelah nama alat (forklift 2, mesin 3) = nomor unit, jangan diubah jadi jumlah; bila ragu tulis apa adanya". Larang tawaran menghubungi peserta. |
| `arus-kas-13minggu` | Narasi salah: "minggu 12 … gaji, bahan, **dan cicilan Rp62 juta** jatuh bersamaan" padahal cicilan ada di minggu 11 (tabelnya sendiri benar, 05). Pos BPJS/PPh 21 yang ditanyakan dan tidak dijawab tidak disebut sebagai asumsi "belum dimasukkan". | Minta agent mengutip rincian keluar minggu kritis langsung dari output script (script bisa mencetak rincian per minggu kritis). Tambah ke checklist: pos yang ditanyakan tapi tidak dijawab ditulis di Asumsi sebagai "belum termasuk". |
| (tingkat solusi) | `find /` seluruh disk di 02 dan 04, kedua sisi. | Tambahkan ke panduan/AGENTS.md bawaan solusi: "file yang dikirim member ada di folder kerja; jangan mencari ke seluruh disk". |

## Masalah teknis alat uji
- Tidak ada kegagalan alat; semua 12 panggilan `rc=0`. Gateway sengaja tidak berjalan, jadi jadwal terjadwal (laporan harian/mingguan, digest tugas, ringkasan piutang pagi) **tidak diuji** di sini.
- Karena kedua home berada di bawah folder yang sama, `find /` agent menampilkan path home uji lainnya. Tidak memengaruhi hasil (masing-masing membaca file di home-nya sendiri), tetapi sebaiknya home uji diisolasi (mis. chroot/container) untuk uji berikutnya.
- `vikunja-tugas`, `laporan-harian-usaha`, `buku-stok`, `buku-piutang` (alur basis data lokal) dan `laporan-insiden-usaha` belum diuji di putaran ini.

## Cuplikan jualan (jujur, terpendek)

**1. Tagih piutang: angka pasti, dan AI tidak mengirim sendiri** (04, pesan: *"mana aja yg udah telat bayar & total berapa? terus bikinin pesan WA buat nagih yg paling parah"*)
- Tanpa skill: *"…Mau saya kirimkan langsung via WhatsApp, atau cukup draft ini aja…?"*
- Dengan skill: *"TOTAL YANG TELAT: Rp 221.800.000 … Mohon kesediaannya untuk menyelesaikan pembayaran paling lambat 8 Oktober 2026 … saya tidak mengirim apa pun — pesan di atas tinggal Bapak/Ibu kirim sendiri lewat WA."*

**2. Notulen: "Jumat depan" jadi tanggal pasti** (01)
- Tanpa skill: *"Penjualan September: Rp2.100.000 … Tono kirim daftar prospek paling lambat Jumat depan."*
- Dengan skill: *"Bu Sari … Sebelum Rabu, 7 Oktober 2026 … ⚠️ "Jumat depan" — Jumat, 2 Okt 2026 atau Jumat, 9 Okt 2026 … Rapat berikutnya: Kamis, 8 Oktober 2026."*

**3. Arus kas: bukan cuma "kas minus", tapi jalan keluarnya dihitung** (05)
- Tanpa skill: *"Nego termin bayar supplier — geser dari mingguan ke 2-mingguan…"* (tanpa hitungan)
- Dengan skill: *"Naikkan pemasukan ±Rp 60 juta/minggu → saldo terendah naik dari -Rp 451.000.000 menjadi +Rp 123.000.000 … Negosiasi termin … INI HANYA MENUNDA … saldo tetap minus Rp 371.000.000."*

Jangan memakai skenario 02 (ringkas grup WA) dan 03 (rasio keuangan) sebagai bukti sebelum/sesudah: tanpa skill hasilnya hampir sama atau sama bagusnya.

## Uji ulang ke-3 2026-10-01

Penguji independen ke-3 (bukan pembuat). OpenClaw asli lokal, model router Komunitech; home `sol3-*` direset dari skill terbaru sebelum tiap skenario; pesan member, jawaban lanjutan, dan file data **sama persis** dengan uji pertama; hanya sisi SESUDAH. Angka dihitung ulang dengan Python dan script repo dijalankan penguji untuk cek balik. Argumen tool call tidak dibaca (database sesi tidak dibuka): tidak terlihat instalasi paket atau `find /` dari teks/berkas, tetapi tidak bisa dipastikan 100%.

| # | Skill (versi) | Cacat lama hilang? | Regresi / temuan baru | Skor lama → baru | Status |
|---|---|---|---|:-:|---|
| [01](uji-openclaw/01-notulen-rapat-ulang3.md) | `notulen-rapat` 1.0.3 | **Ya** — "Sebelum Rabu, 7 Oktober 2026" (0 gagal script); "Forklift **nomor 2** rusak"; tidak ada tawaran menghubungi Tono | Tugas tambahan "Proses sewa forklift — Hendra" tidak ada di catatan (ditandai ⚠️); sel tenggat Tono menulis 9 Okt sambil ditandai ambigu | 8,5 → **9** | **LULUS** |
| [02](uji-openclaw/02-ringkas-grup-wa-ulang3.md) | `ringkas-grup-wa` 1.0.4 | **Ya** — "⏰ LEWAT TENGGAT (29/09/2026, 2 hari lalu) — belum ada kabar forklift"; "hari ini 01/10/2026" | "PERLU PERHATIAN (6)" berisi 5 butir; "Tiga lainnya" menyebut 4; Sinar Jaya disebut "vendor" di penutup | 8 → **8,5** | **LULUS** |
| [03](uji-openclaw/03-rasio-keuangan-ulang3.md) | `analisis-rasio-keuangan-usaha` 1.0.4 | **Ya** — "risiko likuiditas jangka pendek: SEDANG … Rp 900 jt lebih besar dari kas … 47%"; rasio kas 🟡; tanpa "tidak ada risiko". **Sebagian**: "Usaha dagang" tertulis tapi tak dilabeli asumsi | Tidak ada berarti (skala "kecil" per PP 7/2021 benar) | 8 → **9** | **LULUS** |
| [04](uji-openclaw/04-tagih-piutang-ulang3.md) | `tagih-piutang` 1.0.4 | **Ya** — CSV `no_faktur/nilai_faktur/sudah_dibayar` langsung terbaca (0 gagal; script repo: "Kolom dipakai: … nominal=nilai_faktur"); total telat Rp221.800.000; tahap 5 = surat + WA pengantar | WA "Kami lampirkan surat … di pesan ini" tanpa catatan bahwa file/PDF dibuat member; UD Berkah Tani "jangan ditagih dulu" vs script "pengingat H-1"; catatan pemilik di dalam kutipan WA | 8,5 → **9** | **LULUS** |
| [05](uji-openclaw/05-arus-kas-13-minggu-ulang3.md) | `arus-kas-13minggu` 1.0.3 | **Ya** — "minggu 3 … Gaji Rp 420.000.000 dan bahan baku Rp 130.000.000 … total keluar Rp 550.000.000" (tanpa salah minggu cicilan); "Belum termasuk pajak/BPJS" | Tidak ada berarti | 8,5 → **9** | **LULUS** |

Angka: semua cocok dengan hitung ulang penguji (umur piutang & total Rp221,8 jt / Rp279,8 jt; 15 rasio; 13 saldo mingguan, 451/551 jt, simulasi opsi 1–4 termasuk 206 jt mg8 dari `proyeksi_kas.py`; kalender notulen). Rata-rata SESUDAH 8,3 → **8,9**. Cuplikan jualan 03 (rasio) kini layak: "Utang bank jatuh tempo ≤12 bulan (Rp 900 jt) lebih besar dari kas (Rp 420 jt). Kas hanya menutup 47%".
