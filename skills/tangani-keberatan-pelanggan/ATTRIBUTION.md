# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi kerangka penanganan keberatan penjualan dari skill publik berlisensi Apache-2.0, ditulis ulang total dalam Bahasa Indonesia untuk penjual di chat WhatsApp, DM marketplace/Instagram, dan Telegram.

## Sumber yang diadaptasi
- **Repo:** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (pembuat: Anthropic)
- **Skill sumber:** `sales/skills/handle-objection/SKILL.md` (nama skill sumber: `handle-objection`; 93 baris; satu-satunya file di folder skill itu). Commit terakhir untuk path ini: 2026-09-15, `c66cd2d` ("rebuild sales plugin as 2.0.0 with 36 skills").
- **Lisensi:** Apache License 2.0. Teks lengkap di `LICENSE-APACHE`, disalin dari `sales/LICENSE` repo sumber (diambil 2026-10-05). Pemegang hak cipta tidak disebut di repo sumber (bagian lampiran lisensi masih berupa placeholder `[yyyy] [name of copyright owner]`). Berkas `LICENSE` di root repo menambahkan baris teks acak tidak berkaitan setelah teks lisensi; `sales/LICENSE` tidak memuatnya, dan baris acak itu tidak dipakai.
- **NOTICE:** repo sumber **tidak memiliki berkas NOTICE** (permintaan ke `NOTICE` di root dan `sales/NOTICE` menghasilkan 404, dicek 2026-10-05), jadi tidak ada NOTICE asli untuk diteruskan. Berkas `NOTICE` di folder ini milik Komunitech untuk karya turunan.
- **Cara pengambilan:** halaman GitHub dan `raw.githubusercontent.com` dibaca pada 2026-10-05 (tanpa clone, tanpa menjalankan kode apa pun). SHA-256 `SKILL.md` sumber saat dibaca: `f8e922441acbff67b2c641079dda03cb9378fce04f8997893a980fad5a6d8b79`.
- **Bagian yang dipelajari:** klasifikasi enam jenis keberatan (harga/nilai, waktu/prioritas, perbandingan pesaing, risiko/kepercayaan, wewenang "saya perlu tanya dulu", status quo); pembedaan keberatan (alasan tidak membeli) dari manuver tawar-menawar (alasan membeli lebih murah); alur ground, klasifikasi, bukti, jawaban; susunan jawaban "akui dulu, jawab dengan tujuan pelanggan sendiri, akhiri dengan pertanyaan yang menggerakkan percakapan"; daftar "jangan" (memberi diskon berlebihan, menumpuk fitur, berdebat); bukti hanya yang sudah disetujui untuk dipakai keluar; kalimat pelanggan adalah data, bukan perintah.
- **Bagian yang TIDAK dipakai:** semua konektor (CRM, transkrip, dokumen, email), riwayat menang/kalah dan kutipan suara pelanggan dari CRM, "competitor playbook", perutean ke `draft-outreach`, kebijakan izin konektor, tingkatan `files-only/read-only/gated-writes`, dan aturan render artefak.

## Audit keamanan (Tahap 3 CLAUDE.md), 2026-10-05
- Dibaca penuh: `SKILL.md` sumber (93 baris) dan `LICENSE`. Tidak ada script dan tidak ada file pendukung di folder skill sumber. Tidak ada yang dijalankan.
- Diperiksa: perintah destruktif, pengiriman data ke server luar, pembacaan kredensial/SSH key/data browser, pengunduh-lalu-eksekusi otomatis, kode ter-obfuscate, instruksi tersembunyi (mengabaikan pengguna, mengirim file, menonaktifkan konfirmasi), API key/token tertanam, dan prompt injection. **Nihil.** Aturan sumber justru berisi pagar yang baik: isi email/transkrip/dokumen eksternal adalah data bukan perintah; tindakan yang diminta oleh isi teks harus ditunjukkan ke pengguna dulu; balasan hanya ke pengirim thread, tidak ke alamat yang disebut di dalam teks keberatan. Semangat itu dipertahankan (langkah 1 di `SKILL.md`).
- Catatan: `LICENSE` root repo memuat teks acak non-lisensi di akhir berkas; tidak berupa perintah ke agent, tidak disalin. `sales/LICENSE` bersih.
- Kesimpulan: **lolos audit**, aman diadaptasi.
- Lihat juga catatan riset internal kurator (tidak disertakan dalam paket) (bagian skill ini) di repo kurator.

## Pernyataan perubahan (Apache-2.0 bagian 4b: berkas telah diubah)
Materi asal **telah diubah** oleh Komunitech:
1. Diterjemahkan dan ditulis ulang total ke Bahasa Indonesia; seluruh pembungkus konektor/CRM/transkrip, aturan izin konektor, dan orientasi tim penjualan korporat AS dibuang.
2. Kanal diganti dari email/call ke **chat WhatsApp, DM marketplace/Instagram, dan Telegram**, dikirim satu per satu oleh penjual (mode copilot, tidak ada kirim otomatis).
3. Enam jenis keberatan sumber dipertahankan intinya, tetapi disesuaikan menjadi harga, waktu, kepercayaan, kebutuhan, otoritas, dan pesaing (status quo digabung ke kebutuhan/pesaing; "risiko" menjadi kepercayaan).
4. Alur "ground, klasifikasi, bukti, jawaban" diganti alur tiga langkah **akui, tanya, tawarkan opsi**; bukti dari CRM diganti fakta dari pengguna dengan penanda `[isian: ...]`.

## Nilai tambah Komunitech (karya orisinal)
1. Keluaran: 2-3 balasan WA siap kirim berbeda arah, satu pertanyaan lanjutan, dan aturan **kapan berhenti** (sumber hanya berhenti pada "satu talk track").
2. **Larangan keras**: urgensi/kelangkaan palsu, diskon karangan, klaim tanpa data, menjelekkan pesaing, memaksa; dasar UU 8/1999 Pasal 9, 10, 12 dan catatan kebijakan marketplace (`references/etika-keberatan.md`).
3. Keberatan khas lokal ("kemahalan", "tanya suami/istri/bos", "takut tipu", "mau COD dulu"), sapaan Kak/Bapak/Ibu, kalimat sopan siap tempel (`references/jenis-keberatan.md`).
4. **Script baru `scripts/hitung_harga.py`** (`Decimal`, input gaya Indonesia, harga per hari/pemakaian, perbandingan per unit termasuk ongkir, cicilan tanpa bunga) + 14 uji regresi (`tests/uji_regresi.py`); jujur bila harga kita memang lebih mahal.
5. Template `templates/balasan-keberatan.md`, contoh kasus lokal (fiktif), README pembeli.

Bagian turunan (klasifikasi keberatan dan susunan jawaban di `SKILL.md`, `references/jenis-keberatan.md`) tunduk pada `LICENSE-APACHE`. Bagian orisinal (`scripts/`, `tests/`, `templates/`, `references/etika-keberatan.md`, `examples/`, `README.md`) adalah karya Komunitech dan tunduk pada `LISENSI.txt` paket pembelian.
