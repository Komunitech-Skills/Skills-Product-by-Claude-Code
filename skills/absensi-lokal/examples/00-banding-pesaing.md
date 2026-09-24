# 00 — Uji banding pesaing (skenario 01)

Tanggal cari: 23–24 September 2026. Kata kunci: `SKILL.md attendance overtime agent skill github clawhub`, `clawhub "attendance-sheet" skill`, `open source aplikasi absensi fingerprint rekap lembur PP 35 2021 github`; juga dicek daftar VoltAgent/awesome-openclaw-skills dan hasil web search. Tidak ada skill Indonesia untuk absensi + lembur PP 35/2021 yang ditemukan. Semua pesaing hanya **dibaca**, tidak ada script pihak ketiga yang dijalankan, tidak ada teks yang disalin.

## Pesaing yang ditemukan

| Pesaing | Sumber | Lisensi / sinyal | Isi |
|---|---|---|---|
| **attendance-sheet** (skill OpenClaw, @gykdly) | https://clawskills.sh/skills/gykdly-attendance-sheet · API ClawHub `clawhub.ai/api/v1/skills/attendance-sheet` | Lisensi tidak disebut; v1.0.0; ±807 unduhan; **VirusTotal: Suspicious** | Membuat lembar absensi .xlsx berwarna dari daftar nama + status (contoh berbahasa Mandarin). Butuh `openpyxl`. Tidak membaca log mesin, tidak menghitung jam/lembur/upah. |
| **Frappe HR** (aplikasi open-source) | https://github.com/frappe/hrms | GPL-3.0, ±8,8k bintang, aktif | HRIS lengkap: check-in, shift, cuti, laporan, lembur. Butuh Docker/Bench + ERPNext; tidak ada tangga lembur PP 35/2021 bawaan; tidak dioperasikan lewat chat. |
| **siwajah** | https://github.com/antokcompo/siwajah | "Internal use only — PT PP (Persero)" (proprietary), 0 bintang | Impor Excel mesin, rekap, approval lembur, slip. Butuh Node + Supabase; rumus lembur tidak didokumentasikan. Tidak boleh dipakai/dijual ulang. |

## Menjalankan skenario 01 dengan pesaing terkuat berformat skill (attendance-sheet)

Berperan sebagai agent yang memuat `attendance-sheet`: skill meminta input "daftar karyawan + rentang tanggal + jenis status". Log mesin 304 tap tidak punya status per hari, jadi agent harus lebih dulu menyimpulkan sendiri status tiap hari (tanpa aturan dari skill), lalu skill menghasilkan `Agustus-2026-absensi.xlsx`: baris karyawan × kolom tanggal, sel berwarna (normal/telat/absen/cuti/lembur), total hari. Tidak ada: jam kerja, menit terlambat, lembur dalam jam, rupiah lembur, pasal, pembeda lembur disetujui vs pulang telat, data ganjil, penyimpanan untuk bulan berikutnya.

| Kriteria (1–5) | attendance-sheet | Frappe HR (dinilai dari dokumentasi) | **absensi-lokal** |
|---|---|---|---|
| Kualitas hasil untuk skenario 01 | 2 (lembar warna saja) | 4 (setelah dikonfigurasi) | **5** |
| Kesesuaian konteks Indonesia (PP 35/2021, pola 5/6 hari, Rupiah, mesin lokal) | 1 | 2 | **5** |
| Akurasi angka lembur/jam | 1 (tidak menghitung) | 3 (perlu rumus dibuat sendiri) | **5** (diverifikasi independen) |
| Siap pakai untuk awam (tanpa setup) | 3 (butuh openpyxl) | 1 (server, Docker) | **4** (Python standar) |
| Keamanan/privasi | 2 (ditandai VirusTotal) | 4 (self-host) | **5** (lokal, tanpa jaringan) |

**Hasil: skill kita menang telak** atas pesaing skill. Sebagai pengganti SaaS, Frappe HR lebih lengkap fiturnya tetapi terlalu berat untuk UMKM awam dan tidak punya hitungan PP 35/2021 bawaan.

## Yang bisa dipelajari (ide, bukan salinan)
- attendance-sheet: keluaran **Excel berwarna** (grid karyawan × tanggal) disukai HR. Kita hanya punya CSV polos; pertimbangkan `--xlsx` grid bulanan (bisa ditulis dengan Python standar, zip + XML).
- Frappe HR / aplikasi berbayar: saldo **cuti tahunan** (12 hari/tahun menurut UU Ketenagakerjaan sebagaimana diubah UU 6/2023 — pasal perlu dicek pembuat), **jadwal shift rotasi**, **approval lembur oleh atasan** di HP, laporan per divisi/cabang, dan tanda "kelebihan jam tanpa SPL".

## Pengganti SaaS: yang masih kurang dibanding aplikasi absensi berbayar yang wajar diharapkan UMKM
1. Absen mandiri karyawan (HP/selfie/lokasi) — sengaja tidak didukung; harus lewat mesin/admin.
2. Tarik data otomatis dari mesin (SDK/LAN) — harus ekspor file manual.
3. Saldo & pengajuan cuti, persetujuan atasan — belum ada (hanya catat keterangan).
4. Shift rotasi/jadwal mingguan per karyawan — belum (satu karyawan = satu shift).
5. Multi-cabang/divisi, akses beberapa admin — belum (satu file database).
6. Laporan Excel berformat (grid berwarna), grafik — hanya CSV.
Untuk UMKM 3–30 karyawan dengan mesin fingerprint, kekurangan ini wajar untuk produk sekali bayar, dan README sudah jujur soal poin 1–2.
