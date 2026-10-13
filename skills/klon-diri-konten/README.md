# Klon Diri untuk Konten (Avatar & Suara Sendiri)
**Tampil konsisten di video tanpa shooting terus, memakai avatar (tiruan digital wajah dan suara) Anda sendiri, dengan persetujuan tertulis dan label konten AI.**

Diuji AI penguji independen di OpenClaw: 7,75 → 8,5 dari 10 (pembedanya paket lengkap: persetujuan tertulis, hitungan menit termasuk cadangan revisi 25%, dan label AI wajib, dibanding saran alat umum).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Tahu **alat mana** yang cocok dan berapa biayanya dalam Rupiah (perbandingan bertanggal, jujur soal kekurangan).
- Hitung apakah paket cukup untuk jumlah video Anda (lewat skrip hitung; angka dihitung, bukan dikira).
- Formulir persetujuan tertulis siap pakai untuk diri sendiri maupun staf/talent.
- Panduan rekam sampel dan naskah latihan Bahasa Indonesia supaya klon terdengar natural.
- Alur konten bulanan + label AI + langkah bila Anda ditiru orang lain.

## Cocok untuk siapa
Pemilik UMKM, kreator, konsultan, dan profesional yang ingin tampil rutin di TikTok/Reels/Shorts tanpa rekam ulang tiap hari.

**Batasnya:** hanya untuk wajah/suara Anda sendiri, atau orang lain yang memberi persetujuan tertulis, dan setiap konten diberi label konten AI sesuai aturan platform. **Bukan** untuk meniru orang lain tanpa izin, testimoni palsu, atau konten politik/penipuan.

## Contoh sebelum/sesudah
**Sebelum:** "Harus dandan, cari cahaya, rekam 20 kali; akhirnya seminggu tidak posting." Tanpa skill, AI memberi saran alat dan harga terkini, tetapi tanpa persetujuan tertulis, tanpa hitungan revisi, dan label AI dianggap opsional.

**Sesudah (cukup ketik):** "Halo kak, saya pemilik toko skincare kecil. Mau bikin video ngomong ke kamera pakai wajah dan suara AI saya sendiri biar nggak perlu syuting terus. Kira2 12 video sebulan, tiap video 45 detik, budget maks Rp600.000 per bulan. Tayang di TikTok sama Reels."

Cuplikan balasan (dipotong; contoh dengan data fiktif dari uji OpenClaw, `examples/00-openclaw-sebelum-sesudah.md`; harga alat perkiraan per 2026-09-29):
```
Kebutuhan render (termasuk revisi): 11.25 menit/bulan
Paket                      Butuh     Batas     Sisa  Status           Biaya/bulan  Rp/menit
HeyGen Creator            112.50    600.00   487.50  cukup              Rp478.500  Rp42.533
HeyGen Pro                112.50   1000.00   887.50  lewat-anggaran     Rp808.500  Rp71.867
Synthesia Starter          11.25     10.00     0.00  kurang             Rp957.000  Rp85.067
Synthesia Creator          11.25     30.00    18.75  lewat-anggaran   Rp1.468.500 Rp130.533
Termurah yang mencukupi: HeyGen Creator (Rp478.500/bulan)
…
Label AI (wajib dicentang + taruh di caption)
"Video ini dibuat dengan bantuan AI. Avatar dan suara adalah tiruan digital saya sendiri."
```
Kolom Butuh/Batas adalah kredit paket; angka kredit per menit di contoh ini hanya ilustrasi, cek di akun Anda. Hasil lengkapnya juga memuat rencana rekam sampel, kalender konten, dan peringatan keamanan. Contoh lain: `examples/01-toko-hijab-12-video.md`; perbandingan tanpa skill vs dengan skill: `examples/00-pembanding-tanpa-skill.md`.

## Cara pakai
Ketik: "Saya mau bikin avatar AI diri sendiri untuk [usaha], [jumlah] video/bulan, anggaran Rp[...]." Skill bertanya sekali bila info kurang.

## Instalasi singkat
Salin folder `klon-diri-konten` ke folder skill platform Anda (OpenClaw, Codex, Claude Code, Cursor). Lokasi per platform: `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Tidak butuh API key. Pasangkan dengan skill Komunitech `studio-video-pendek-ai` (pembuat naskah video pendek) untuk naskah.

Untuk yang terbiasa dengan terminal: hitung paket lewat `python3 scripts/rencana_konten_avatar.py --paket paket.json --video 12 --menit 0.75 --kurs 16500 --anggaran 500000` (Windows: `python` atau `py`; format di `examples/contoh-paket.json`, angka paket isi dari halaman harga resmi). Uji skrip: `python3 tests/uji_regresi.py`.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.5), skor 1–10: tanpa skill **7,75** → dengan skill **8,5** (LULUS). Contoh 12 video × 45 detik + cadangan revisi 25% = **11,25 menit**; HeyGen Creator perkiraan **Rp478.500** muat budget Rp600.000 + gerbang persetujuan & label AI. Pada uji jebakan (minta klon suara artis tanpa izin dan buang label AI), AI tanpa skill pun menolak (8,5 → 8,5), jadi skill ini bukan satu-satunya pencegah penyalahgunaan. Catatan jujur: di uji itu AI menyusun tabel hitungan sendiri tanpa menjalankan skrip; angkanya diperiksa penguji dan benar. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.

**Status uji (jujur):** sudah diuji OpenClaw sebelum/sesudah otomatis (2026-10-02). Harga alat = perkiraan bertanggal (cek situs resmi). Tidak merender video; Codex/Cursor belum uji platform asli.

## FAQ
**Apakah skill membuat klon atau video?** Tidak. Skill memandu keputusan, persetujuan, rekam sampel, dan hitungan; render (proses membuat videonya) dilakukan di alat pilihan Anda, dan unggah dilakukan manual oleh Anda.
**Boleh klon wajah/suara karyawan atau artis?** Karyawan/talent hanya dengan persetujuan tertulis (formulir tersedia). Artis/tokoh atau siapa pun tanpa izin: tidak.
**Apakah harga alat di skill ini sudah final?** Tidak. Harga di `references/pilihan-alat.md` adalah perkiraan bertanggal 2026-09-29; cek halaman resmi.

Skill ini tidak berafiliasi dengan HeyGen, ElevenLabs, CapCut, D-ID, Synthesia, TikTok, YouTube, Meta, atau proyek open-source yang disebut. Bukan nasihat hukum.
