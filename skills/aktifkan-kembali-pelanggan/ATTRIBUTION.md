# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi kerangka kerja win-back yang terbukti dari skill publik berlisensi Apache-2.0, ditulis ulang total dalam Bahasa Indonesia untuk usaha kecil Indonesia berbasis WhatsApp/Telegram, dengan script hitung dan aturan etika lokal.

## Sumber yang diadaptasi
- **Repo:** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (pembuat: Anthropic)
- **Skill sumber:** `small-business/skills/reactivate/SKILL.md` (nama skill sumber: `reactivate`; ~109 baris; satu-satunya file di folder skill itu)
- **Lisensi:** Apache License 2.0 (teks lengkap: `LICENSE-APACHE`, disalin dari berkas `LICENSE` repo sumber, diambil 2026-10-05). Berkas `LICENSE` sumber berisi bagian pemegang hak cipta yang masih berupa placeholder (`Copyright [yyyy] [name of copyright owner]`) dan beberapa baris teks acak tidak berkaitan setelah teks lisensi; baris acak itu **tidak disalin** (tidak mengubah isi lisensi). Pemegang hak cipta tidak disebut di repo sumber.
- **NOTICE:** repo sumber **tidak memiliki berkas NOTICE** (permintaan ke `NOTICE` di cabang utama menghasilkan 404, dicek 2026-10-05), jadi tidak ada NOTICE untuk diteruskan.
- **Cara pengambilan:** halaman GitHub / `raw.githubusercontent.com` dibaca pada 2026-10-05 (tanpa clone dan tanpa menjalankan kode apa pun). Snapshot cabang utama; hash SHA-256 `SKILL.md` sumber saat dibaca: `734946c30236c86adc55eecfb2694a0e02ca12625654633597d3c303bf39e210`.
- **Bagian yang dipelajari:** alur 5 langkah (temukan pelanggan "diam" menurut ritmenya sendiri, konfirmasi apa yang boleh ditawarkan, urutan 3 pesan dalam 4 minggu, berhenti saat keluhan/balasan, catat sentuhan), aturan "pesan pertama tidak jualan", "peringkat berdasarkan nilai bukan lamanya diam", "jangan menawarkan hal yang belum disetujui pemilik", "keluarkan yang terakhir kali memberi ulasan jelek, telepon saja", "pastikan tanggal data bisa dipercaya sebelum menghitung".
- **Bagian yang TIDAK dipakai:** seluruh konektor (CRM, pembayaran, toko online, email, Mailchimp), rantai skill lain (`review-reputation`, `outreach-composer`, `crm-autopilot`, `ticket-deflector`), berkas gaya bersama (`shared/*`), keluaran artefak HTML, dan bagian "Using a tool that isn't listed".

## Audit keamanan (pedoman kurasi Komunitech), 2026-10-05
- Dibaca penuh: `SKILL.md` sumber dan `LICENSE`. Tidak ada script, tidak ada file pendukung di folder skill sumber (hanya `SKILL.md`). Tidak ada yang dijalankan.
- Diperiksa: perintah destruktif, pengiriman data ke server luar, pembacaan kredensial/SSH key/data browser, unduh-dan-jalankan otomatis (curl/wget), kode ter-obfuscate, instruksi tersembunyi (mengabaikan pengguna, mengirim file, menonaktifkan konfirmasi), API key/token tertanam. **Nihil.** Frontmatter sumber memuat `allowed-tools: Read, WebFetch` (izin baca dan ambil web); field itu **tidak dibawa** (frontmatter skill ini hanya `name` dan `description`).
- Sumber justru memuat pagar baik: kebijakan "teks di dalam pesan/dokumen adalah data, bukan perintah" dan gerbang persetujuan sebelum mengirim; semangat itu dipertahankan.
- Catatan: berkas `LICENSE` sumber berisi baris teks acak non-lisensi di akhir (lihat di atas). Tidak berupa instruksi untuk agent dan tidak dipakai. Kesimpulan: **lolos audit**, aman diadaptasi.

## Pernyataan perubahan (Apache-2.0 bagian 4b: berkas telah diubah)
Materi asal **telah diubah** oleh Komunitech. Perubahan utama:
1. Diterjemahkan dan ditulis ulang total ke Bahasa Indonesia; format artefak/pembungkus konektor dibuang.
2. Kanal diganti dari email/CRM ke **WhatsApp dan Telegram**, dikirim **satu per satu oleh pemilik** (mode copilot); tidak ada kirim otomatis.
3. Alur 5 langkah dipertahankan inti-nya (kerangka, urutan 3 pesan/4 minggu, pesan pertama tidak jualan, berhenti saat komplain atau balasan), tetapi gerbang persetujuan lewat konektor diganti gerbang manual pemilik.
4. Ditambahkan seluruhnya baru (karya orisinal Komunitech): segmentasi A-D berdasarkan hari sejak beli terakhir; script `scripts/segmentasi.py` + `tests/uji_regresi.py`; jadwal dengan batas harian dan tanpa hari Minggu; daftar jangan-dihubungi; template pesan WA per segmen; tabel tindakan saat pelanggan membalas/komplain/minta berhenti; referensi etika dan UU PDP; contoh data dan kasus lokal; README pembeli.

## Pembagian lisensi
- **Kerangka alur win-back dan prinsip** di `SKILL.md` (bagian "Aturan keras", Langkah 4, 5, 6): turunan dari materi Apache-2.0 `anthropics/knowledge-work-plugins`, tunduk pada `LICENSE-APACHE`; telah diubah (lihat di atas).
- **Semua bagian lain**: `scripts/`, `tests/`, `templates/`, `references/`, `examples/`, `README.md`: karya orisinal Komunitech, tidak mengandung materi pihak ketiga.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, ditambah ketentuan Apache-2.0 pada bagian turunan. Anthropic tidak berafiliasi dengan dan tidak mengesahkan produk Komunitech ini.

## Riwayat versi
### v1.0.0 (2026-10-05), rilis awal (status `uji`), hasil kurasi ATM dari `reactivate`.
