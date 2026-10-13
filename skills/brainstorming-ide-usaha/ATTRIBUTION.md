# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi dengan nilai tambah BESAR).** Skill ini mengadaptasi **pola proses** (bukan teks) dari skill publik berlisensi MIT yang ditujukan untuk agen coding, ditulis ulang ±90% ke konteks curah gagasan usaha UMKM/profesional Indonesia.

## Sumber yang diadaptasi
- **Repo:** [obra/superpowers](https://github.com/obra/superpowers)
- **Skill sumber:** `skills/brainstorming/`
- **Pembuat:** Jesse Vincent
- **Lisensi:** MIT (dicek langsung di file `LICENSE` repo sumber — lihat `LICENSE-MIT` di folder ini untuk teks lengkapnya, "Copyright (c) 2025 Jesse Vincent")
- **Commit yang dipakai:** `5bf4e78011075bcfc0dc295f0724994cd123ee71` (default branch, tanggal commit 2026-09-18), diambil via `git clone --depth 1 --filter=blob:none --sparse` pada 2026-09-25, sparse-checkout folder `skills/brainstorming` + `LICENSE`.
- **File yang dibaca penuh:** `skills/brainstorming/SKILL.md`, `skills/brainstorming/spec-document-reviewer-prompt.md`, `skills/brainstorming/visual-companion.md`, serta isi `skills/brainstorming/scripts/` (`server.cjs`, `helper.js`, `frame-template.html`, `start-server.sh`, `stop-server.sh`) — dibaca untuk audit, **tidak dijalankan**.

## Audit lisensi & keamanan (Tahap 2–3 CLAUDE.md)
- File `LICENSE` di root repo sumber dicek langsung via `git show`/`cat`: MIT, Copyright (c) 2025 Jesse Vincent — mengizinkan modifikasi & penjualan turunan.
- Seluruh isi `skills/brainstorming/` (termasuk folder `scripts/`) dibaca penuh dan di-`grep` untuk pola mencurigakan (perintah destruktif, unduh-lalu-eksekusi skrip dari internet, pengiriman data ke server luar, permintaan kredensial/SSH key/data browser, kode ter-obfuscate, instruksi tersembunyi menyuruh mengabaikan pengguna).
- Satu-satunya perintah berpotensi destruktif ditemukan: `stop-server.sh` berisi `rm -rf "$SESSION_DIR"` — tapi `$SESSION_DIR` adalah folder sesi sementara yang dibuat oleh skill itu sendiri (server companion visual lokal berbasis Node.js), bukan folder sembarang milik pengguna. Tidak berbahaya dalam konteksnya.
- Tidak ditemukan pola unduh-lalu-eksekusi skrip dari internet, eksfiltrasi data ke server luar, API key/token tertanam, atau prompt injection ("ignore the user", instruksi menonaktifkan konfirmasi, dll.) — instruksi `SKILL.md` murni prosedural (klasifikasi → tanya → gerbang persetujuan).
- **Kesimpulan: lolos audit.** Sesuai catatan catatan riset internal kurator (tidak disertakan dalam paket) bagian obra/superpowers, versi Indonesia ini **sengaja tidak menyertakan** server companion visual (`scripts/server.cjs` dkk., file `visual-companion.md`) — di luar cakupan prinsip "tanpa setup, tanpa Node.js" CLAUDE.md Bagian 1; hanya alur teksnya yang diadaptasi.

## Apa yang diubah/ditambahkan (nilai tambah ATM, ±90% ditulis ulang)
Sumber aslinya untuk **agen coding** (klasifikasi spike/bounded/architectural, spec file, git worktree, invoke skill `writing-plans`) — konsepnya generik ("gali dulu, baru eksekusi, dengan gerbang persetujuan") tapi seluruh contoh, istilah, dan target keluarannya spesifik pengembangan software. Perubahan besar untuk versi ini:
1. **Domain diganti total**: dari "ide fitur software" menjadi "ide usaha, promo, nama, diversifikasi, solusi operasional" — tidak ada satu pun contoh/istilah teknis (spec file, git worktree, bounded/architectural code change) yang dipertahankan apa adanya.
2. **Tiga jalur ditulis ulang** dari spike/bounded/architectural (istilah coding) menjadi Jalur A "Cepat" / B "Perlu Diuji" / C "Perlu Rencana" — pola bertingkat & aturan "kalau ragu pilih yang lebih dalam, hidden complexity menaikkan jalur" dipertahankan karena terbukti berguna, tapi kriteria & bahasanya bisnis, bukan kode.
3. **Batasan nyata UMKM Indonesia** (`references/musim-dan-momentum.md`): modal, waktu, SDM, lokasi, dan kalender momentum belanja Indonesia (gajian, tanggal tua, Harbolnas 9.9–12.12, Ramadan–Lebaran, tahun ajaran baru, musim hujan/kemarau) — tidak ada padanannya sama sekali di sumber.
4. **Teknik ide terstruktur dalam bahasa awam** (`references/teknik-ide-terstruktur.md`: SCAMPER, gabung-kombinasi, pembalikan masalah) — sumber tidak punya teknik ideation sama sekali, hanya "ajukan pertanyaan satu per satu" tanpa kerangka pemunculan ide.
5. **Penyaringan ide dengan skor tertimbang yang DIHITUNG script** (`scripts/skor_ide.py`, 32 kasus uji lolos, termasuk data rusak: nilai di luar 1–5, bobot kosong/negatif/nol, kolom kriteria tidak cocok, nama ide kosong/duplikat) — sumber sama sekali tidak punya mekanisme skor/penyaringan ide, hanya diskusi kualitatif.
6. **Titik impas kasar** (`skor_ide.py impas`: modal awal ÷ margin per unit, dibulatkan ke atas) — tidak ada di sumber.
7. **Uji murah/MVP untuk konteks usaha** (`templates/kerangka-uji-murah.md`: pre-order WA, tes 1 minggu, target 10 pelanggan, kapan berhenti/lanjut) — sumber tidak membahas uji pasar sama sekali (fokusnya implementasi kode setelah spec disetujui).
8. **Ringkasan penutup berupa Rencana Aksi 7 Hari** — bentuk keluaran baru, tidak ada padanan di sumber (sumber berakhir di "invoke skill writing-plans" untuk membuat plan implementasi kode).
9. **Prinsip "instan"**: jalur cepat (Jalur A) dan aturan "kalau pengguna minta cepat, pakai default & sebutkan asumsi" — sumber justru menuntut satu pertanyaan per pesan tanpa jalur pintas eksplisit seperti ini.
10. **100% Bahasa Indonesia**, contoh kasus lokal (usaha laundry), dan dokumentasi pembeli (README.md) — sumber berbahasa Inggris dan ditujukan untuk agen coding, bukan produk untuk dijual ke pembeli awam.
11. **Tidak menyertakan server companion visual** — keputusan sengaja mengurangi kompleksitas demi prinsip "tanpa setup" (lihat Audit di atas), bukan sekadar oversight.

Pola yang **dipertahankan** dari sumber karena memang yang membuatnya kuat (bukan sekadar terjemahan, tapi diakui secara sadar): klasifikasi skala permintaan di awal & disebutkan ke pengguna untuk dikoreksi, satu pertanyaan fokus per pesan, "tulis ulang pemahaman lalu minta koreksi" sebelum lanjut, menawarkan beberapa pendekatan dengan untung-rugi (bukan satu ide tunggal), gerbang persetujuan wajib sebelum lanjut ke tahap berikutnya, aturan "kalau ragu pilih jalur lebih berat" dan "kerumitan tersembunyi menaikkan jalur, tidak pernah turun", serta prinsip YAGNI.

## Pembagian lisensi bagian ini
- **Pola proses tiga jalur & gerbang persetujuan** yang diadaptasi ke `SKILL.md` bagian "Langkah Kerja": terinspirasi struktur MIT `obra/superpowers` skill `brainstorming`, ditulis ulang total (istilah, contoh, kriteria, dan seluruh kalimat berbeda dari sumber) — dicatat di sini untuk transparansi sesuai `LICENSE-MIT` meski secara teks sudah orisinal.
- **Semua bagian lain** — teks lengkap `SKILL.md`, `references/`, `templates/`, `scripts/`, `examples/`, dan `README.md` — adalah karya orisinal Komunitech, tidak mengandung materi pihak ketiga, dan boleh diperlakukan sebagai proprietary Komunitech.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, ditambah ketentuan MIT pada bagian yang disebut di atas.
