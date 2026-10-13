# Riwayat perubahan — surat-resmi

Catatan teknis per versi.

## Catatan revisi 1.0.3 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`) karena lambat dan menyentuh data pribadi.

## Catatan revisi 1.0.2 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri (mis. `pip install`), tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (disimpan di folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.1 (2026-09-24)
- Versi saat skill pertama masuk repo, setelah uji internal pertama. Yang terlihat di SKILL.md: nama hari yang ditulis pengguna (mis. "Jumat, 3 Oktober 2026") wajib dibandingkan dengan hasil script; bila berbeda, agent tidak boleh memilih sendiri dan menanyakannya dulu. Perbaikan lain: rincian di riwayat git.

## Catatan revisi 1.0.0 (sebelum 2026-09-24)
- Rilis awal (uji internal).
