# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengadaptasi **kerangka** perancangan urutan pesan yang terbukti dari skill publik berlisensi Apache-2.0, ditulis ulang total dalam Bahasa Indonesia untuk usaha kecil Indonesia berbasis WhatsApp/Telegram/email, dengan aturan etika lokal dan script jadwal.

## Sumber yang diadaptasi
- **Repo:** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (pembuat: Anthropic)
- **Skill sumber:** `marketing/skills/email-sequence/SKILL.md` (nama skill sumber: `email-sequence`; 220 baris; satu-satunya file di folder skill itu)
- **Lisensi:** Apache License 2.0 (teks lengkap: `LICENSE-APACHE`, disalin dari `marketing/LICENSE` repo sumber, diambil 2026-10-06; 202 baris, bersih; SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`). Pemegang hak cipta di berkas sumber berupa placeholder; tidak disebut di repo sumber.
- **NOTICE:** repo sumber tidak memiliki berkas NOTICE (404, dicek 2026-10-05), jadi tidak ada NOTICE untuk diteruskan.
- **Cara pengambilan:** `raw.githubusercontent.com` dibaca pada 2026-10-06 (tanpa clone, tanpa menjalankan kode apa pun). SHA-256 `SKILL.md` sumber saat dibaca: `4303252cbe340b19945b3e58d46430fdf42ea47b3e26d985e3ef1d6da5e36021`.
- **Bagian yang dipelajari (kerangka saja):** delapan jenis urutan (onboarding, lead nurture, re-engagement, win-back, peluncuran produk, tindak lanjut acara, upgrade/upsell, edukasi bertahap), pemetaan jumlah dan jarak pesan per jenis, tujuan tiap langkah, definisi kondisi keluar ("tanda rangkaian sudah berhasil"), aturan penekanan (jangan kirim bila penerima sudah berhenti, sudah di rangkaian lain, atau baru menghubungi layanan pelanggan), satu ajakan utama per pesan.
- **Bagian yang TIDAK dipakai:** seluruh konektor (Klaviyo, Mailchimp, HubSpot dan sejenisnya), tabel tolok ukur persentase (tidak berlaku untuk skala UMKM Indonesia dan tidak dapat dipertanggungjawabkan), saran uji A/B ala platform email, diagram alur bercabang berbasis pembukaan email, tindak lanjut acara dan upsell paket perangkat lunak, field `argument-hint`.

## Audit keamanan (Tahap 3 CLAUDE.md), 2026-10-06
- Dibaca penuh: `SKILL.md` sumber dan `LICENSE`. Tidak ada script maupun berkas pendukung di folder skill sumber. Tidak ada yang dijalankan.
- Diperiksa (dibaca + pencarian pola curl/wget/eval/base64/rm/ssh/token/api key/password/secret/ignore): perintah destruktif, pengiriman data ke luar, pembacaan kredensial, unduh-dan-jalankan, kode ter-obfuscate, instruksi tersembunyi, rahasia tertanam. **Nihil.** Satu-satunya kemunculan "token" adalah istilah personalisasi (token nama depan). Penanda konektor dan `argument-hint` di frontmatter tidak dibawa. **Lolos audit.**

## Pernyataan perubahan (Apache-2.0 bagian 4b: berkas telah diubah)
Materi asal **telah diubah** oleh Komunitech. Perubahan utama:
1. Diterjemahkan dan ditulis ulang total ke Bahasa Indonesia; format email-saja dan pembungkus konektor dibuang.
2. Kanal diganti ke **WhatsApp (mode Copilot, pemilik mengirim satu per satu), Telegram, dan email untuk daftar opt-in**; tidak ada pengiriman otomatis ke pelanggan.
3. Delapan jenis urutan disusun ulang menjadi delapan situasi pelanggan UMKM Indonesia (sambutan, edukasi, keranjang tertunda, setelah beli, minta ulasan, perpanjangan, reaktivasi, peluncuran) dengan jarak hari dan jumlah pesan yang disesuaikan.
4. Ditambahkan seluruhnya baru (karya orisinal Komunitech): bank pesan WA berbahasa sehari-hari; opt-out di tiap pesan; batas frekuensi dan jam kirim; aturan UU PDP, UU 8/1999, dan platform; larangan imbalan/penyaringan ulasan; script `scripts/jadwal_rangkaian.py` + `tests/uji_regresi.py`; contoh kasus lokal; README pembeli.

## Pembagian lisensi
- **Kerangka jenis urutan dan prinsip kondisi berhenti** di `SKILL.md` (bagian "Peta 8 situasi" dan "Aturan keras"): turunan dari materi Apache-2.0 `anthropics/knowledge-work-plugins`, tunduk pada `LICENSE-APACHE`; telah diubah (lihat di atas).
- **Semua bagian lain:** `scripts/`, `tests/`, `references/`, `examples/`, `README.md`: karya orisinal Komunitech, tidak mengandung materi pihak ketiga.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, ditambah ketentuan Apache-2.0 pada bagian turunan. Anthropic tidak berafiliasi dengan dan tidak mengesahkan produk Komunitech ini.

## Riwayat versi
### v1.0.0 (2026-10-06), rilis awal (status `uji`), hasil kurasi ATM dari `email-sequence`.
