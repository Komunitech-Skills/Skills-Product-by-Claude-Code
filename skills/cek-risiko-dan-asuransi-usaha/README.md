# Cek Risiko Usaha, Tahu Perlu Asuransi atau Tidak

*Peta risiko usaha Anda dan dana darurat yang masuk akal, dalam satu tabel.*

Diuji AI penguji independen di OpenClaw: 6,6 → 9,0 dari 10 (tanpa skill hanya daftar risiko umum dan rentang dana darurat; dengan skill tiap risiko berskor dengan keputusan asuransinya dan target dana darurat dihitung).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Tahu risiko mana yang paling berbahaya untuk warung, toko, bengkel, kafe, atau jasa Anda.
- Langkah murah yang bisa dilakukan minggu ini, sebelum membeli apa pun.
- Jelas mana yang memang layak dialihkan ke asuransi dan mana yang tidak.
- Target dana darurat usaha dihitung dengan rumus tetap dari biaya tetap Anda.
- Daftar pertanyaan siap bawa ke agen asuransi terdaftar (tanpa menyebut merek).

## Cocok untuk siapa
Pemilik usaha kecil yang bingung apakah perlu asuransi, dan profesional yang membantu mereka. Tidak perlu paham istilah asuransi.

## Cara pakai
Ketik satu kalimat, mis. "Kafe saya di ruko dekat sungai, 3 karyawan, apa risikonya dan perlu asuransi apa?" Hasil langsung berupa tabel; di akhir ada maksimal 3 pertanyaan.

## Sebelum / sesudah
Contoh: toko kelontong di Semarang Utara yang sering kena banjir rob (air laut pasang); satu pesan yang sama, jawaban AI tanpa dan dengan skill. Angka ujinya ada di bagian "Hasil uji" di bawah.

- **Tanpa skill:** daftar risiko umum, perkiraan premi (biaya asuransi) dan tarif iuran BPJS dari ingatan, arisan ikut dihitung sebagai biaya tetap tanpa catatan, dana darurat hanya berupa rentang ("11,5 sampai 23 juta"), tanpa skor dan tanpa keputusan "perlu asuransi atau tidak" per risiko.
- **Dengan skill:** 9 risiko diberi skor dan tingkat, tiap risiko ada keputusan asuransinya (utang pelanggan macet ditulis "tidak ada asuransi umum, pakai langkah lain"), dana darurat dihitung dengan rumus tetap, hasilnya "kurang Rp4.050.000, sisihkan Rp675.000 per bulan selama 6 bulan", tanpa merek dan tanpa premi karangan.

Cuplikan keluaran dengan skill (uji isi oleh agent, bukan uji OpenClaw; dipotong; `examples/06-kelontong-semarang-uji-ulang.md`):

> | No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah minggu ini | Perlu asuransi? |
> |---|---|---|---|---|---|---|
> | 1 | Banjir rob masuk toko | 4 | 3 | 12 TINGGI | Semua stok di palet/rak ≥ 40 cm, karung beras & gula di rak atas, colokan kulkas dipindah lebih tinggi | Tidak perlu (terlalu sering; kurangi dengan langkah murah) |
> | 4 | Pencurian rokok/uang laci | 3 | 3 | 9 SEDANG | Rokok di etalase terkunci, setor uang laci tiap sore, CCTV murah | Tidak perlu |
> | 5 | Bapak/Ibu sakit, toko tutup | 2 | 3 | 6 SEDANG | Catat harga & pemasok di satu buku agar pegawai bisa jaga | Tidak perlu |
> | … | | | | | | |
>
> **Dana darurat (3 bulan)**
> - Biaya tetap per bulan: Rp3.350.000 (gaji pegawai 1,8 jt + listrik 650 rb + cicilan motor 900 rb)
> - Target: **Rp10.050.000**
> - Kas sekarang: Rp6.000.000 (cukup 1,8 bulan biaya tetap)
> - Kekurangan: **Rp4.050.000** → sisihkan **Rp675.000 per bulan selama 6 bulan**.

## Instalasi
Lihat `docs/instalasi.md` untuk OpenClaw, Codex, Claude Code, dan Cursor. Script opsional memakai Python standar (`python3`; Windows `python`/`py`).

**Hasil uji (angka nyata):** skor 1–10 penguji independen.
- Uji OpenClaw (uji otomatis agent, 10 Okt 2026, v1.0.2, 4 skenario): tanpa skill **6,6** → dengan skill **9,0** (LULUS). Rincian: `examples/00-openclaw-v1.0.2-sebelum-sesudah.md`.
- Uji isi oleh agent pada contoh toko kelontong di atas (simulasi, bukan uji OpenClaw, 9 Okt 2026, v1.0.1): tanpa skill **6** → dengan skill **8,5**. Bahan: `examples/00-pembanding-tanpa-skill.md`.
- Hasil di bot Telegram asli ada di bagian berikutnya.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan bot Telegram uji; Claude Code lewat simulasi agent; Codex dan Cursor belum diuji langsung (format skill-nya sama). Rujukan aturan asuransi di skill ini (mis. POJK 23/2023) berasal dari sumber sekunder dan belum direview ahli; cek ulang di situs resmi OJK sebelum bertindak.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech), 2026-10-12.
- Tanpa skill: skor **6,5** — dana darurat hanya rentang kasar tanpa hitung kekurangan.
- Dengan skill: skor **8,5** (LULUS) — peta risiko berskor, target dana darurat dihitung, tanda perlu asuransi, jalur aduan ke OJK (Otoritas Jasa Keuangan, kontak pengaduan 157) bila klaim ditolak. Hasil di bot ini diuji pada skill v1.0.2.

## FAQ
1. **Apakah ini nasihat asuransi?** Bukan. Ini alat bantu awam; polis (surat perjanjian asuransi) dibeli lewat perusahaan asuransi berizin OJK dan agen yang terdaftar.
2. **Bisakah memilihkan merek asuransi terbaik?** Tidak. Skill memberi kriteria dan pertanyaan, bukan merek.
3. **Apakah klaim pasti cair?** Tidak ada yang bisa menjamin; skill membantu menyiapkan dokumentasi.

Terkait: skill Laporan Insiden Usaha (untuk kejadian yang sudah terjadi) dan skill Kas UMKM (keuangan harian).

## Riwayat perubahan

Versi terkini: **1.0.2**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
