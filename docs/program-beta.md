# Program Beta Tester

Tujuan: menguji skill di tangan **pengguna sungguhan** (pengusaha & profesional awam) sebelum dijual.

## Alur
1. **Pilih skill**: status `beta` di `catalog.csv` (sudah lulus uji agent + uji platform asli).
2. **Rekrut 5–10 member VIP** yang cocok dengan target skill (mis. skill marketplace → pemilik toko online). Campur pengguna OpenClaw, Codex, Claude Code, Cursor, dan Windows/Mac.
3. **Kirim paket**: `python3 scripts/build.py --pembeli "Beta - <nama>" --skill <nama> --beta` (satu paket per orang; watermark tetap berlaku).
4. **Masa uji ±7 hari.** Minta mereka memakai skill untuk pekerjaan nyata minimal 3 kali.
5. **Kumpulkan masukan** dengan formulir di bawah (Google Form / WA).
6. **Rangkum** di `skills/<nama>/examples/MASUKAN-BETA.md` (tanpa data pribadi: pakai "Beta 1", "Beta 2", dst.).
7. **Revisi** → uji ulang singkat → status `rilis` → naikkan `versi`.
8. **Minta testimoni** (dengan izin tertulis) untuk halaman jualan.

**Imbalan usulan:** skill yang diuji gratis selamanya + 1 skill lain gratis / diskon perpanjangan VIP.

## Formulir masukan (5 menit)
1. Platform & OS yang dipakai?
2. Apakah instalasi berhasil tanpa bantuan? (Ya / Perlu bantuan / Gagal) — kalau tidak, di langkah mana?
3. Berapa kali dipakai untuk pekerjaan nyata minggu ini?
4. Seberapa berguna hasilnya? (1–5)
5. Seberapa sering hasilnya bisa langsung dipakai tanpa diedit? (Selalu / Sering / Kadang / Jarang)
6. Berapa lama biasanya pekerjaan ini tanpa skill? Dengan skill?
7. Pernah dapat hasil yang salah/aneh? Ceritakan (tempel contoh bila boleh, hapus data pribadi).
8. Apa yang paling kamu suka?
9. Apa satu hal yang harus diperbaiki?
10. Berapa harga yang menurutmu wajar untuk skill ini? (Rp0 / Rp29rb / Rp49rb / Rp99rb / Rp149rb+)
11. Boleh kutip jawabanmu sebagai testimoni? (Ya, dengan nama / Ya, anonim / Tidak)

## Kriteria naik ke `rilis`
- ≥ 80% beta tester berhasil instal tanpa bantuan.
- Rata-rata nilai kegunaan ≥ 4.
- Tidak ada laporan hasil salah yang belum diperbaiki.
