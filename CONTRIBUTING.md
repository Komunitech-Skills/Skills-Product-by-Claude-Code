# Panduan Membuat Skill

Aturan lengkap (riset, kurasi, lisensi, audit keamanan, pengujian, harga) ada di [CLAUDE.md](CLAUDE.md).
Ringkasannya:

## Langkah

1. Salin template:
   ```bash
   mkdir skills/<nama-skill>
   cp templates/SKILL.template.md skills/<nama-skill>/SKILL.md
   cp templates/README.template.md skills/<nama-skill>/README.md
   ```
   `nama-skill` memakai huruf kecil, angka, dan tanda hubung (maks. 64 karakter), sama dengan nama folder.
2. Isi `SKILL.md`: Tujuan → Kapan Digunakan / Tidak → Input → Langkah Kerja → Format Output → Contoh → Batasan.
3. Tambahkan baris di `catalog.csv` (status `draft`/`uji`; `tier_final` & `harga_final_idr` diisi sesuai keputusan pemilik).
4. Jalankan `python3 scripts/validate.py` sampai lolos.
5. Uji oleh agent/orang **berbeda** dari pembuat (lihat checklist QA), lalu `bash scripts/uji_openclaw.sh`.
6. Commit dengan pesan `skill: <nama> (<status>)`.

## Aturan format

- Frontmatter **hanya** `name` dan `description` (tanpa field khusus platform).
- `description`: apa yang dikerjakan **dan kapan** dipakai, satu baris, maks. 1024 karakter, kata kunci ID & EN.
- `SKILL.md` ringkas (idealnya < 300 baris); materi panjang di `references/`.
- Script hanya **Python standar**, lintas OS; perhitungan uang/pajak/gaji wajib lewat script atau rumus eksplisit.
- Sertakan `README.md` (panduan pembeli + materi jualan), `examples/`, dan `LICENSE`/`ATTRIBUTION.md`.
- Jangan pernah menyimpan API key, token, atau data pribadi di skill.

## Checklist QA sebelum `lulus`

- [ ] `validate.py` lolos
- [ ] 5 skenario uji: 3 normal, 1 input tidak lengkap, 1 di luar cakupan (+ data rusak bila ada script)
- [ ] Angka diverifikasi independen
- [ ] Uji A/B (tanpa vs dengan skill) → `examples/00-pembanding-tanpa-skill.md`
- [ ] Uji banding pesaing → `examples/00-banding-pesaing.md`
- [ ] Hasil & skor (≥ 7) di `examples/HASIL-UJI.md`
- [ ] `uji_openclaw.sh` lolos
- [ ] `versi` di `catalog.csv` dinaikkan bila ini update

## Versi

Semantic versioning di `catalog.csv`:
- `PATCH` (1.0.1): perbaikan kecil
- `MINOR` (1.1.0): fitur baru, kompatibel
- `MAJOR` (2.0.0): perubahan besar pada cara pakai
