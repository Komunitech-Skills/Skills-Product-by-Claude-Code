# Uji ulang OpenClaw — Klinik 03 · Pengingat kontrol, info kurang (pengingat-pasien-klinik 1.0.6)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · Uji pertama: [03-pengingat-kontrol-info-kurang.md](03-pengingat-kontrol-info-kurang.md)

OpenClaw lokal, model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`). Home `sol-klinik` direset dari skill terbaru (`reset-klinik.sh`, juga membuat ulang `kosong-klinik` yang confignya diubah agent di uji pertama). Sesi baru, 2 giliran. Workspace awal kosong (sama seperti uji pertama). Sisi SEBELUM memakai hasil uji pertama. Data pasien fiktif.

**Cacat yang diuji ulang:** (1) contoh perintah di SKILL.md (`--json` di akhir) gagal rc=2 sehingga agent harus mencoba ulang; (2) agent menjalankan `find / -name pengingat_pasien.py` ke seluruh disk.

## Pesan member giliran 1 (sama persis)

> tolong catat pasien buat diingetin kontrol ya: Bu Rina, kontrol behel bulan depan

## Pesan member giliran 2 (sama persis)

> WA nya 0812-0000-2222, tanggalnya 3 November aja. iya dia udah setuju diingetin lewat WA. sekalian bikinin draf pesan pengingatnya ya

## Balasan SESUDAH baru — giliran 1 (utuh)

_Alat: `read` (1 panggilan) · durasi 10 detik_

> Sebelum saya catat, saya butuh dua info wajib yang belum ada:
> 
> 1. Nomor WA Bu Rina (untuk draf pengingat nanti)?
> 2. Bu Rina setuju dihubungi lewat WA untuk pengingat jadwal kontrolnya? (ya/tidak)
> 
> Begitu dijawab, langsung saya catat jadwal kontrol behel "bulan depan"-nya.
## Balasan SESUDAH baru — giliran 2 (utuh)

_Alat: `exec` (**2 panggilan, 0 gagal**) · durasi 15 detik_

> Sudah dicatat ✅
> 
> **Bu Rina** | Kontrol behel | **3 Nov 2026** | WA 0812-0000-2222 | persetujuan: ya
> (Catatan: tahun tidak disebutkan, jadi dipakai 2026 — tahun terdekat ke depan. Kalau maksudnya bukan itu, bilang aja nanti saya koreksi.)
> 
> Nanti sistem akan menandainya di daftar H-3 (31 Okt), H-1 (2 Nov), dan hari-H (3 Nov) secara otomatis.
> 
> Draf pesan pengingatnya (salin & kirim sendiri, bukan dikirim otomatis):
> 
> > Halo Bu Rina, ini pengingat dari kami untuk jadwal kontrol behel Anda pada 3 Nov 2026. Mohon konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. Terima kasih.
## Bukti pemakaian script & verifikasi

- **Jumlah panggilan tool** (dari `meta.toolSummary` di JSON keluaran, tanpa membaca database sesi): uji pertama giliran 2 = **4 panggilan `exec`** (termasuk `find /` dan percobaan `--json` yang gagal); uji ulang = **2 panggilan `exec`** (sesuai alur `tambah` lalu `draf`). Argumen tool call tidak dibaca (database sesi sengaja tidak dibuka), jadi tidak adanya `find /` disimpulkan dari jumlah panggilan — tidak ada ruang untuk panggilan pencarian atau percobaan ulang.
- **File hasil** `pasien/DAFTAR.csv` di workspace: `1,Bu Rina,6281200002222,Kontrol behel,2026-11-03,dijadwalkan,ya,2026-10-01,,` — data minimal, persetujuan tercatat, tanpa diagnosis.
- **Uji script langsung oleh penguji** (folder sementara): `pengingat_pasien.py tambah … --file ./D.csv --json` (opsi global di **akhir**) → `rc=0`, `"ok": true` (di versi lama: `unrecognized arguments: --json`, rc=2). `daftar --hari-ini 2026-10-31 --json` → Bu Rina masuk kelompok H-3 dengan draf identik dengan balasan agent.
- SKILL.md baris 90–91 kini menulis lokasi script eksplisit dan "jangan mencarinya ke seluruh disk (`find /`)".
- Tanggal: 3 Nov 2026 = Selasa; H-3 = 31 Okt, H-1 = 2 Nov ✅.

## Penilaian

- **Cacat 1 (sintaks `--json` gagal): HILANG — ya.** 0 kegagalan, 2 panggilan; script menerima `--json` di dua posisi (diuji penguji).
- **Cacat 2 (`find /`): HILANG — ya (bukti tidak langsung).** Jumlah panggilan turun dari 4 ke 2 dan SKILL.md melarang eksplisit.
- Perilaku inti tetap baik: giliran 1 menanyakan 2 hal wajib (WA + persetujuan, "ya/tidak"), giliran 2 mencatat satu baris + label *"salin & kirim sendiri, bukan dikirim otomatis"*.
- **Regresi kecil:** kalimat *"Nanti sistem akan menandainya di daftar H-3 (31 Okt), H-1 (2 Nov), dan hari-H (3 Nov) secara otomatis"* bisa dibaca admin awam seolah ada pengingat yang jalan sendiri, padahal pengelompokan hanya muncul saat daftar dibuka/diminta (jadwal ringkasan harian belum dipasang). Tidak menjanjikan kirim ke pasien, tetapi sebaiknya diganti "akan muncul di daftar H-3… saat Anda minta daftar pengingat, atau lewat ringkasan harian bila dijadwalkan". Uji pertama justru menawarkan jadwal harian secara eksplisit.

| | Sesudah (lama) | Sesudah (baru) |
|---|---|---|
| Skor | 8,5 | **9** |
