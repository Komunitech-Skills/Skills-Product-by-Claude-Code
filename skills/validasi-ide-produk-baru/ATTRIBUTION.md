# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi dengan nilai tambah BESAR).** Skill ini mengadaptasi **kerangka proses** (bukan teks) dari koleksi skill publik berlisensi Apache-2.0 yang ditujukan untuk product manager software (Foundation Sprint / Design Sprint / hipotesis produk), ditulis ulang total ke konteks uji pasar murah UMKM/profesional Indonesia.

## Sumber yang diadaptasi
- **Repo:** [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills)
- **Skill sumber yang dibaca:** `skills/define-hypothesis/`, `skills/tool-foundation-sprint-founding-hypothesis/`, `skills/tool-foundation-sprint-basics/`, `skills/tool-design-sprint-test-and-score/`, `skills/measure-experiment-design/`, `skills/discover-market-sizing/` (dibaca untuk audit & pemahaman kerangka, **tidak dijalankan**)
- **Pembuat:** product-on-purpose (proyek aktif, rilis reguler)
- **Lisensi:** Apache License 2.0 — teks lengkap ada di [`LICENSE-APACHE`](LICENSE-APACHE) (disalin dari file `LICENSE` root repo sumber)
- **Commit yang dipakai:** `1cef1a9eae10017389863d51e289e0ae41e17fcb` (default branch, 10 September 2026), diambil via `git clone --depth 1` pada 2026-09-26
- **NOTICE:** repo sumber **tidak menyertakan file `NOTICE`** (dicek langsung — tidak ada `NOTICE`/`NOTICE.txt` di root maupun folder skill) — sesuai Apache-2.0 §4(d), tidak ada NOTICE untuk disertakan.
- **File telah diubah:** ya — seluruh teks dalam paket ini (`SKILL.md`, `references/`, `templates/`, `scripts/`, `examples/`, `README.md`) ditulis ulang dari nol dalam Bahasa Indonesia untuk konteks UMKM; tidak ada teks sumber yang disalin verbatim.

## Audit lisensi & keamanan (Tahap 2–3 CLAUDE.md)
- File `LICENSE` di root repo sumber dicek langsung: Apache License 2.0 — mengizinkan modifikasi & penjualan turunan dengan syarat menyertakan teks lisensi, atribusi, NOTICE (jika ada), dan keterangan file diubah. Semua syarat dipenuhi di file ini.
- Skill-skill terkait (`define-hypothesis`, `tool-foundation-sprint-*`, `tool-design-sprint-test-and-score`, `measure-experiment-design`, `discover-market-sizing`) dibaca penuh dan di-`grep` untuk pola mencurigakan di seluruh repo (`skills/`, `scripts/`): perintah destruktif (`rm -rf` dsb.), unduh-lalu-eksekusi skrip dari internet, pengiriman data ke server luar, permintaan kredensial/SSH key/data browser, kode ter-obfuscate, dan prompt injection tersembunyi ("ignore the user/previous instructions", instruksi menonaktifkan konfirmasi).
- Tidak ditemukan pola berbahaya pada skill yang diadaptasi — isinya murni instruksi prosedural (kerangka hipotesis, kriteria sukses, metode validasi) tanpa script executable dan tanpa data pribadi/kredensial tertanam.
- Repo memiliki banyak file `scripts/*.mjs`/`*.ps1` untuk tooling internal CI proyek sumber (pengecekan lintas-skill, generator situs) — **tidak diadaptasi/disalin sama sekali**, di luar cakupan kebutuhan skill ini (di luar prinsip "tanpa setup" CLAUDE.md).
- **Kesimpulan: lolos audit.**

## Apa yang diubah/ditambahkan (nilai tambah ATM)
Sumber aslinya untuk **product manager tim software** (hipotesis fitur/produk digital, Foundation Sprint 5 hari ala tim startup, eksperimen A/B terukur dengan sample size statistik, "founding hypothesis" untuk pitch investor). Konsepnya generik ("nyatakan hipotesis → tentukan metrik sukses → uji → putuskan") tapi seluruh contoh, istilah, dan skala eksekusinya untuk tim produk software dengan sumber daya jauh lebih besar. Perubahan besar untuk versi ini:
1. **Domain diganti total**: dari "hipotesis fitur software/produk digital tim startup" menjadi "ide produk/menu/jasa UMKM" — tidak ada satu pun istilah sumber (founding hypothesis, Design Sprint 5 hari, A/B test statistik) dipertahankan apa adanya.
2. **Lima metode uji murah ala Indonesia** (pre-order WA/status, polling story IG, lapak marketplace PO, sampel ke pelanggan tetap, titip warung) — sumber tidak membahas kanal ini sama sekali (fokusnya prototype digital & eksperimen produk software).
3. **Kriteria lulus/gagal berbasis persentase konversi sederhana** (15%/8%, `scripts/hitung_validasi.py`) — sumber memakai kerangka signifikansi statistik A/B test yang butuh sample size besar & alat analitik, tidak cocok untuk UMKM bermodal & data kecil; kerangka ini ditulis ulang total jadi heuristik praktis skala UMKM.
4. **Perhitungan margin & balik modal uji** (`hitung_validasi.py`, teruji dengan data rusak: preorder>ditawari, angka negatif, harga 0, non-numerik) — tidak ada padanan di sumber.
5. **Template pesan siap pakai** (broadcast WA, status WA, caption polling IG, listing PO marketplace, pitch titip warung, pesan tanya alasan tidak beli) — sumber tidak punya template pesan berorientasi kanal konsumen ritel.
6. **Contoh kasus lokal** (kopi susu gula aren literan, jasa laundry sepatu, kelas online Canva) — sumber memakai contoh produk software (fitur aplikasi, SaaS).
7. **100% Bahasa Indonesia**, disclaimer eksplisit "ambang 15%/8% heuristik praktis, bukan angka baku ilmiah" — sumber berbahasa Inggris, ditujukan tim produk profesional, tanpa disclaimer awam.

Pola yang **dipertahankan** dari sumber karena memang yang membuatnya kuat: format kalimat hipotesis eksplisit ("kami percaya... akan... karena..."), keharusan menetapkan kriteria sukses **sebelum** menjalankan uji (bukan sesudah), dan prinsip "uji murah dulu sebelum investasi besar" — dituliskan ulang total dengan bahasa, angka, dan konteks yang seluruhnya berbeda dari sumber.

## Pembagian lisensi bagian ini
- **Kerangka hipotesis & urutan "hipotesis → kriteria → uji → keputusan"** yang menjiwai `SKILL.md`: terinspirasi struktur Apache-2.0 `product-on-purpose/pm-skills`, ditulis ulang total (istilah, contoh, kriteria, dan seluruh kalimat berbeda dari sumber) — dicatat di sini untuk transparansi sesuai Apache-2.0 meski secara teks sudah orisinal.
- **Semua bagian lain** — teks lengkap `SKILL.md`, `references/`, `templates/`, `scripts/`, `examples/`, dan `README.md` — adalah karya orisinal Komunitech, tidak mengandung materi pihak ketiga, dan boleh diperlakukan sebagai proprietary Komunitech, dengan tetap menyertakan `LICENSE-APACHE` sesuai kewajiban Apache-2.0 §4.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, ditambah ketentuan Apache-2.0 pada bagian yang disebut di atas.
