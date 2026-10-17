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
5. Uji oleh agent/orang **berbeda** dari pembuat (maker ≠ tester; lihat checklist QA), lalu `bash scripts/uji_openclaw.sh`.
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

## Uji OpenClaw & acuan lulus

- Uji internal sebelum/sesudah di OpenClaw (skill mati vs aktif). Acuan lulus: **skor sesudah ≥ 8 dan selisih rata-rata ≥ 1,5**. Di bawah itu skill tidak diiterasi lagi (diusulkan `arsip`; perubahan bundle/paket VIP menunggu pemilik).
- **Pra-cek `scratchpad/openclaw-real/uji-tg.sh`** (konteks kanal Telegram) wajib untuk skill berhasil panjang/berupa file dan untuk setiap calon gelombang Telegram. Kirim ke Telegram hanya setelah persetujuan pemilik.
- Setelah uji baru/ulang: perbarui `promosi/sebelum-sesudah.jsonl` dan jalankan `python3 scripts/promosi_sebelum_sesudah.py` (lihat `promosi/README.md`).

- Skrip bantu rilis (opsional): `scripts/pracek_rilis.py` (pra-cek kesiapan rilis) dan `scripts/rilis_batch.py`; lihat docstring masing-masing.
- Status skill: `ide → draft → uji → lulus → beta → rilis` (atau `ditolak`/`arsip`).

## Pola wajib di SKILL.md

- **Kerjakan dulu, tanya di akhir:** beri hasil memakai asumsi yang disebut; pertanyaan tambahan satu kali di penutup.
- **Isi utuh di chat:** hasil lengkap ada di balasan, bukan hanya di file. File (mis. Word) dilampirkan bila kanal bisa; bila tidak, jalur file tidak disebut dan ditawarkan "balas 'kirim file'".
- **Tanpa kata proses:** jangan menulis "Langkah 1", "saya memeriksa skill", dsb. di jawaban untuk pengguna.
- **Blok angka "UNTUK AGENT SAJA":** perhitungan/angka kunci untuk agent diberi penanda ini dan tidak ditampilkan mentah ke pengguna.
- **Pola penolakan + tetap kerja:** bila sebagian permintaan di luar cakupan/kebijakan, tolak bagian itu dengan sopan dan tetap kerjakan bagian yang boleh.

## Lisensi sumber (ringkas; rujuk CLAUDE.md Tahap 2)

- MIT/BSD/Apache/CC-BY: salin-edit (ATM) dengan nilai tambah besar; sertakan teks lisensi, atribusi, `NOTICE`, dan keterangan perubahan.
- GPL/AGPL/CC-BY-SA: boleh, hasil wajib berlisensi sama dan bisa dibagikan ulang.
- CC-BY-NC, tanpa lisensi, proprietary: jangan disalin; tulis ulang bersih (agent 1 menulis daftar ide, agent 2 menulis tanpa membaca sumber). Ragu = tulis ulang bersih / tandai PERLU REVIEW.
- Catat lisensi di `catalog.csv` dan sumbernya di `research/sources/`. Merek pihak ketiga hanya sebagai penyebut + "tidak berafiliasi".
- Audit keamanan (CLAUDE.md Tahap 3) wajib sebelum menjalankan kode sumber luar.

## Versi

Semantic versioning di `catalog.csv`:
- `PATCH` (1.0.1): perbaikan kecil
- `MINOR` (1.1.0): fitur baru, kompatibel
- `MAJOR` (2.0.0): perubahan besar pada cara pakai
