# Uji OpenClaw: Solusi VIP Konsultan & Freelancer

**Tanggal:** 2026-10-01 (Asia/Jakarta)
**Penguji:** agent penguji independen (bukan pembuat skill). Hasil ditulis apa adanya, tanpa dipoles.

## Cara uji

- **Mesin:** OpenClaw lokal (`openclaw agent --local`, satu giliran per panggilan, `--session-id` sama untuk percakapan lanjutan). Gateway dan Telegram tidak dipakai.
- **Model:** router Komunitech (`ninerouter/komunitech`), sama dengan bot Telegram member.
- **SEBELUM:** home `kosong-konsultan`, tanpa skill terpasang.
- **SESUDAH:** home `sol-konsultan`, paket skill solusi konsultan terpasang di `~/.openclaw/skills/` (25 skill, termasuk `buat-invoice`, `surat-penawaran-harga`, `tagih-piutang`, `laporan-klien-konsultan`, `kalender-pajak`).
- Workspace awal kedua sisi identik (AGENTS/IDENTITY/SOUL). Untuk skenario 04, file fiktif `catatan-kerja.csv` yang sama ditaruh di kedua workspace.
- Pesan member identik di kedua sisi. Jika agent bertanya balik, member menjawab sekali dengan pesan yang sama di kedua sisi (skenario 02 & 05).
- Pemakaian skill dicek dari transkrip (`read ~/.openclaw/skills/<skill>/SKILL.md` dan `exec` script skill). Angka dan aturan pajak diverifikasi ulang secara independen dengan Python (PPN = 12% × DPP nilai lain 11/12 sesuai PMK 131/2024, lalu dibulatkan ke bawah; PPh 23 2% dari bruto) serta dengan menjalankan script skill di luar agent.
- Semua nama klien, rekening, dan nomor di skenario adalah **fiktif**.

## Tabel skor

| No | Skenario | Skill terpakai (SESUDAH) | SEBELUM | SESUDAH |
|---|---|---|---|---|
| 01 | [Invoice PKP + PPN + PPh 23](uji-openclaw/01-invoice-ppn-pph23.md) | `buat-invoice` (script) | 7 | 8 |
| 02 | [Surat penawaran harga non-PKP](uji-openclaw/02-surat-penawaran-harga.md) | `surat-penawaran-harga` (script) | 7 | 8 |
| 03 | [Tagih piutang telat + denda](uji-openclaw/03-tagih-piutang-telat.md) | `tagih-piutang` (script) | 7 | 9 |
| 04 | [Laporan progres ke klien dari CSV](uji-openclaw/04-laporan-progres-klien.md) | `laporan-klien-konsultan` (script) | **8** | 7 |
| 05 | [Kalender pajak, info kurang](uji-openclaw/05-kalender-pajak-info-kurang.md) | `kalender-pajak` (script) | 5 | 7 |
| | **Rata-rata** | 5/5 skenario memakai skill | **6,8** | **7,8** |

**Skor keseluruhan solusi: 7/10.** Skill selalu terpicu dan dipakai dengan benar oleh agent OpenClaw asli (5/5). Angka dari script benar di skenario 01–03 dan 05, dan dasar aturan mutakhir (PMK 131/2024, PMK 81/2024, PP 55/2022). Agent juga tidak lagi menawarkan kirim langsung ke klien. Tapi kemenangannya tidak telak:

- Model dasar sudah bisa menghitung invoice, SPH, dan denda dengan benar.
- Di skenario 04, versi tanpa skill malah lebih akurat.
- Ada celah penting untuk konsultan: PPh 23 dan uang neto yang diterima tidak dihitung.

## Temuan lintas skenario (SEBELUM, model tanpa skill)

Temuan ini memperkuat nilai paket.

- Menjalankan `find /` ke seluruh disk komputer member untuk mencari file (01 dan 04; SESUDAH juga sekali di 04).
- Menjalankan **`pip install weasyprint` tanpa izin member** (02). Paket itu terpasang di Python sistem mesin uji.
- Menawarkan "kirim langsung ke PT Maju Mundur via WhatsApp" (03). Ini melanggar kebijakan Copilot.
- Memakai aturan pajak lama: "PPN 11%", "PP 23", dan setor PPh 21 tanggal 10.

## Cacat per skill

| Skill | Bukti | Saran |
|---|---|---|
| `buat-invoice` | Di 01, member menyebut "mereka biasanya potong PPh 23". Agent mengecek script dengan `grep pph` dan tidak menemukan apa pun. Hasilnya, potongan Rp270.000 dan neto Rp14.715.000 tidak dihitung, hanya ditulis catatan "mohon dipotong". Model tanpa skill justru menghitungnya dengan benar. File HTML hanya disebut path-nya, tidak dikirim sebagai lampiran chat, jadi member di Telegram tidak bisa membukanya. | Tambahkan opsi `--pph23 2` (dan 4% bila tanpa NPWP) di script. Opsi ini menampilkan "perkiraan dipotong klien" dan "neto diterima" di luar total invoice, plus pengingat minta bukti potong. Tambahkan instruksi di SKILL.md agar file HTML/PDF dilampirkan ke chat (`MEDIA:`) bila kanalnya Telegram. |
| `surat-penawaran-harga` | Di 02, teks WA berbunyi "Surat penawaran resmi (PDF) terlampir" padahal tidak ada file yang dibuat. Tidak ada output file cetak. Tidak ada catatan untuk freelancer orang pribadi bahwa klien badan biasanya memotong PPh 21 bukan pegawai. | Template WA jangan menyebut lampiran kecuali file benar-benar dibuat. Tambahkan output HTML siap cetak seperti di `buat-invoice` dan lampirkan ke chat. Tambahkan satu baris catatan potongan PPh 21/PPh 23 sesuai status penyedia. |
| `laporan-klien-konsultan` | Di 04, jam dibulatkan ke 1 desimal: 3,25 jam tercetak "3,2 jam" dan total 9,75 tercetak "9,8 jam", padahal jumlah item yang tampil 9,7. Penguji mereproduksinya di luar agent dengan script skill. Teks "Periode periode kustom" berulang. Script tidak bisa membaca CSV milik member, jadi agent harus menyalin baris satu per satu dengan `catat`. Bagian "Rencana berikutnya" mekanis ("Lanjutkan ..." ×3). | Tampilkan jam dengan 2 desimal atau format "9 jam 45 menit". Pastikan total = jumlah item yang tampil. Tambahkan subperintah `impor` dengan pemetaan kolom fleksibel ("90 menit", "2,5 jam"). Perbaiki label periode. Rencana berikutnya sebaiknya disusun dari catatan/kendala, bukan diulang dari judul. |
| `kalender-pajak` | Script benar (Kamis, 15 Okt 2026). Tetapi di 05 model menambahkan "KAP 411128/411125", padahal 411125 adalah kode PPh 25/29 OP, dan kode ini tidak ada di skill. Model juga menyimpulkan omzet 600 jt/tahun "kemungkinan besar sudah melewati Rp500 juta sebelum September" (seharusnya baru sekitar Oktober). Output script merujuk "skill pph-final-umkm" yang **tidak termasuk paket konsultan**. | Tambahkan tabel KAP-KJS resmi (PP 55: 411128-420) atau larangan eksplisit menyebut KAP. Tambahkan rumus perkiraan bulan tembus ambang (omzet/12 × bulan) beserta catatan batas 7 tahun untuk OP. Masukkan `pph-final-umkm` ke paket konsultan, atau ubah rujukannya. |
| `tagih-piutang` | Kuat (skor 9). Hanya ada cacat kecil: "UU ITE" disebut sebagai dasar tanpa relevansi jelas, dan kalimat "8–11 Oktober (lewat tenggat 7 hari)" membingungkan. | Rapikan daftar dasar hukum dan kalimat jadwal tahap berikutnya. |

## Masalah teknis alat uji

- Isi hasil tool di transkrip OpenClaw tersimpan terkompresi (zstd), jadi yang bisa diaudit hanya argumen pemanggilan tool (cukup untuk membuktikan skill/script dipakai).
- Di `.err` muncul pesan `SQLite reclamation Worker failed ... owner is no longer current`. Pesan ini tidak berpengaruh pada hasil.
- Agent SEBELUM memasang `weasyprint` ke `/usr/local/lib/python3.11/dist-packages` mesin uji. Lingkungan uji berikutnya sudah tidak identik dengan awal; perlu dibersihkan atau dicatat.

## Cuplikan jualan (hanya yang memang lebih baik)

1. **Tagih piutang (03).** Tanpa skill, agent menawarkan *"Mau saya kirimkan langsung ke kontak PT Maju Mundur via WhatsApp?"*. Dengan skill: *"Karena sudah 2x diingatkan tanpa respons dan telat 21 hari, ini masuk Tahap 5 — pemberitahuan resmi … Denda Rp 252.000 … Total ditagih Rp 12.252.000 … mohon pelunasan paling lambat 8 Oktober 2026"*, lengkap dengan surat resmi dan WA pengantar. Draf hanya untuk Anda.
2. **Kalender pajak (05).** Tanpa skill: *"PPh 21 … bayar paling lambat tanggal 10"* (aturan lama). Dengan skill: *"Kamis, 15 Oktober 2026 — SETOR PPh Final UMKM 0,5% masa September 2026 … setoran yang tervalidasi otomatis dianggap sudah lapor"*, berdasarkan PMK 81/2024 dan dicek otomatis terhadap hari libur.
3. **Invoice PKP (01).** Tanpa skill: *"PPN 11%"*. Dengan skill: *"DPP nilai lain (11/12): Rp 12.375.000 · PPN 12%: Rp 1.485.000 … Invoice ini bukan faktur pajak — faktur pajak keluaran tetap dibuat di Coretax."*

Jangan pakai skenario 04 (laporan klien) sebagai materi jualan sampai pembulatan jam diperbaiki.

## Uji ulang 2026-10-01

Penguji independen (bukan pembuat). Home `sol-konsultan` direset dari skill terbaru sebelum tiap skenario; pesan member (termasuk jawaban lanjutan di 02) dan `catatan-kerja.csv` sama persis dengan uji pertama; hanya sisi SESUDAH diulang. Rincian: [02-…-ulang](uji-openclaw/02-surat-penawaran-harga-ulang.md), [04-…-ulang](uji-openclaw/04-laporan-progres-klien-ulang.md).

| # | Skill (versi) | Sebelum | Sesudah lama | Sesudah baru | Cacat dilaporkan | Status |
|---|---|---|---|---|---|---|
| 02 | `surat-penawaran-harga` 1.0.3 | 7 | 8 | **7,5** | WA: "Surat penawaran resmi (PDF) terlampir" padahal tak ada file | **Hilang** — "skill ini tidak membuat PDF … File → Download/Save as PDF"; WA (giliran tambahan): "Surat penawaran resminya menyusul/bisa saya kirimkan bila diperlukan" |
| 04 | `laporan-klien-konsultan` 1.0.5 | 8 | 7 | **8,5** | Jam dibulatkan (3,2 / 9,8), "Periode periode kustom", CSV member tak terbaca, rencana mekanis, `find /` | **Hilang semua** — "9,75 jam (9 jam 45 menit)", item "3,25 jam", file dibaca langsung (`--file`), rencana `[isi: …]`; panggilan tool 8 → 5 |

**Regresi baru:**
- 02 (nyata): agent di giliran 2 **tidak menampilkan surat di chat** dan **tidak membuat teks WA** — hanya ringkasan + nama file `SPH-001-Berkah-Jaya-Bakery.md` di workspace (tak bisa dibuka member Telegram); WA baru muncul setelah diminta (penguji menambah giliran 3). Surat menulis `[Nama PIC]` padahal member menjawab "PIC nggak tahu" (uji pertama benar: "Pimpinan CV …"). Teks WA "(belum kena PPN)" menyiratkan PPN bisa ditambah — kesalahan yang dulu dikurangi di sisi tanpa skill.
- 04 (kecil): rentang tanggal tertulis dua kali berturut-turut; draf butuh member mengisi 3 rencana sebelum kirim (disengaja, jujur).

**Status per skill:** `laporan-klien-konsultan` **LULUS uji ulang**. `surat-penawaran-harga` **BELUM** — cacat lama hilang, tetapi output tidak lagi memenuhi format wajib (A) surat + (B) WA di chat. Saran: di SKILL.md tegaskan "selalu tampilkan surat lengkap + teks WA di chat; file `.md` hanya tambahan"; "PIC tidak diketahui → 'Pimpinan <nama perusahaan>', bukan placeholder"; teks WA non-PKP wajib "tanpa PPN (bukan PKP)", bukan "belum kena/termasuk PPN".

**Cuplikan jualan sekarang layak?**
- 04 laporan klien — **sekarang layak** (larangan di uji pertama dicabut): "Total jam dihitung oleh script: 9,75 jam (9 jam 45 menit)" + "Rencana berikutnya … script sengaja tidak mengarang ini" + "saya tidak akan kirim apa pun ke Pak Hendra". Tetap jujur: model tanpa skill juga menjumlah benar; pembedanya rencana tidak dikarang dan format konsisten.
- 02 SPH — **belum layak** sampai regresi format diperbaiki dan diuji ulang.

## Uji ulang 2026-10-01 (keuangan)

Penguji independen, OpenClaw lokal asli, model router Komunitech (`claude-sonnet-5`), home baru `sol2-konsultan` (direset sebelum tiap skenario). Hanya sisi SESUDAH; pesan identik dengan uji pertama. Angka dihitung ulang dengan Python; script `kalender_pajak.py` dijalankan ulang oleh penguji. Tidak ada paket pip yang terpasang selama uji.

| # | Skill (versi) | Cacat lama hilang? | Regresi / temuan baru | Skor lama → baru | Status |
|---|---|---|---|:-:|---|
| [01](uji-openclaw/01-invoice-ppn-pph23-ulang.md) | `buat-invoice` 1.0.3 | **Ya**: PPh 23 Rp270.000 & estimasi diterima bersih Rp14.715.000 dihitung script; invoice utuh ditulis di chat | **Giliran tambahan**: agent bertanya "apakah perlu mencantumkan **PPN 11%**" padahal member menyebut PKP dan data lengkap (uji pertama langsung jadi); label "PPN 11%" usang | 8 → **8** | LULUS dengan catatan (perbaiki default PPN untuk PKP & larang label 11%) |
| [05](uji-openclaw/05-kalender-pajak-info-kurang-ulang.md) | `kalender-pajak` 1.0.7 | **Ya**: ambang Rp500 jt dihitung script (Okt pas 500 jt, lewat Nov, setor pertama Selasa 15 Des 2026); tanpa KAP karangan; tanpa rujukan skill yang tidak terpasang | Tidak ada (batas 7 tahun OP masih tidak disinggung) | 7 → **8,5** | LULUS |

## Uji ulang 2026-10-01 (keuangan, putaran 2)

Penguji independen, OpenClaw lokal asli, model router Komunitech, home baru (direset sebelum skenario). Hanya sisi SESUDAH; pesan identik dengan uji pertama dan uji ulang 1. Angka dihitung ulang dengan Python dan script skill dijalankan ulang oleh penguji. Tidak ada paket pip yang terpasang selama uji.

| # | Skill (versi) | Cacat sisa hilang? | Regresi / temuan baru | Skor lama → baru | Status |
|---|---|---|---|:-:|---|
| [01](uji-openclaw/01-invoice-ppn-pph23-ulang2.md) | `buat-invoice` 1.0.4 | **Ya**: invoice langsung jadi di giliran 1, PPN 12% × DPP nilai lain 11/12 dengan asumsi disebut; tanpa label "PPN 11%"; nomor/kota/penanda tangan jadi placeholder | Tidak ada | 8 → **9** | LULUS |

Angka benar semua (subtotal 13.500.000; DPP 12.375.000; PPN 1.485.000; total 14.985.000; PPh 23 270.000; diterima bersih 14.715.000; jatuh tempo 15 Okt 2026).
