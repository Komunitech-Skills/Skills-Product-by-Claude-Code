# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Metodologi rasio (kelompok rasio, rumus dasar, gagasan tolok ukur per industri, dan tafsiran berjenjang) diadaptasi dari contoh skill resmi Anthropic berlisensi MIT. Setelah itu seluruhnya ditulis ulang untuk UMKM Indonesia, dan script hitungnya dibuat baru (lihat "Apa yang diubah/ditambahkan").

## Sumber yang diadaptasi
- **Repo:** [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks)
- **Bagian:** `skills/custom_skills/analyzing-financial-statements/` (`SKILL.md`, `calculate_ratios.py`, `interpret_ratios.py`). Folder ini adalah contoh "Financial Ratio Analyzer" (`financial_analyzer`) yang diunggah di notebook `skills/notebooks/03_skills_custom_development.ipynb`. Notebook `02_skills_financial_applications.ipynb` dibaca sebagai konteks (dasbor & laporan keuangan).
- **Pembuat:** Anthropic
- **Lisensi:** MIT, "Copyright (c) 2023 Anthropic". Teks dibaca langsung dari `LICENSE` root repo, dan teks lengkapnya ada di `LICENSE-MIT` folder ini (disalin tanpa perubahan).
- **Commit yang dipakai:** `813fbeec03cdedfda7808529438d1c7af71f26eb` (Thu Sep 24 14:19:10 2026 -0400). Diambil 2026-09-26 lewat `git clone --depth 1 --filter=blob:none --sparse` + `git sparse-checkout set skills`.
- **Bagian yang TIDAK dipakai:** rasio valuasi/pasar modal (P/E, P/B, EV/EBITDA, PEG, EPS), DCF & simulasi Monte Carlo (`creating-financial-models`), pembuatan file Excel/PowerPoint lewat Skills API, dan seluruh kode notebook yang memanggil API Anthropic.

## Audit lisensi & keamanan (Tahap 2–3 CLAUDE.md)
- `LICENSE` MIT dibaca langsung. Lisensi ini mengizinkan modifikasi & penjualan turunan dengan menyertakan pemberitahuan hak cipta dan izin.
- `calculate_ratios.py` (346 baris) dan `interpret_ratios.py` (377 baris) **dibaca penuh, tidak dijalankan**. Keduanya hanya mengimpor `json`/`typing`. Tidak ada akses jaringan, berkas, subprocess, `eval`/`exec`, atau kode ter-obfuscate.
- Notebook 02 & 03 dibaca tanpa dieksekusi. Isinya memanggil API Anthropic dengan kunci dari `.env` milik pengguna notebook sendiri, serta membuat, mengunggah, dan menghapus skill di akun pengguna tersebut. Semua itu tidak relevan dan tidak ikut disalin.
- `SKILL.md` sumber diperiksa: tidak ada prompt injection, instruksi tersembunyi, API key, atau data pribadi.
- Kesimpulan: **lolos audit**.

## Apa yang diubah/ditambahkan (nilai tambah ATM)
1. **Script baru `scripts/rasio.py`** (Python standar, `Decimal`). Sumber memakai float dan `safe_divide` yang diam-diam mengembalikan **0** saat pembagi nol. Akibatnya "utang lancar 0" terbaca rasio lancar 0 (seolah bangkrut), dan "hari piutang = 365 ÷ 0" juga menjadi 0. Di skill ini pembagi nol, modal ≤ 0, laba negatif, dan aset/utang negatif ditangani **jujur**: "tidak dihitung" + alasan, "tidak bermakna", "rugi", atau "mustahil".
2. **Input Indonesia:** `Rp 1.500.000`, `1,5jt`, `150rb`, `(8.000.000)`, `1,2 M`; tabel CSV `;`/`,`/tab atau tabel Markdown yang ditempel dari chat; nama pos berbahasa Indonesia (HPP, piutang, utang usaha, modal, dll.); **output langsung dari `laporan-keuangan-emkm`** (SAK EMKM), termasuk pemisahan utang bank lancar/jangka panjang. Sumber hanya menerima dict berbahasa Inggris.
3. **Ambang per jenis UMKM** (dagang/warung, jasa, produksi/kuliner). Sumber memakai sektor perusahaan besar AS (technology, healthcare, financial) yang disebut sendiri *"simplified for demonstration"*. Dasar & sumber ambang dicatat di `references/ambang-wajar.md` (Kasmir, bunga KUR Permenko 1/2026).
4. **Rasio khas usaha kecil:** umur stok (hari), lama piutang, lama bayar pemasok, **siklus kas**, modal kerja bersih, dan ROA/ROE **disetahunkan** dari periode bulanan/kuartalan. Bila saldo awal tersedia, dipakai **rata-rata saldo**.
5. **Tren antarperiode** (membaik/memburuk menurut arah baik tiap rasio, pertumbuhan penjualan & laba dengan penanganan basis nol/rugi). Sumber hanya menyebut tren tanpa implementasi.
6. **Kesiapan KUR/kredit** (laba positif, modal positif, DER, rasio lancar, neraca seimbang, rasio cicilan ÷ laba per bulan dengan ambang yang sama dengan `pengajuan-kur`) serta **saran tindakan konkret** yang diurutkan (rugi & modal negatif didahulukan).
7. **Tes regresi `tests/uji_regresi.py`** (71 uji pada v1.0.1; angka harapan dihitung manual dan dicek dengan `Fraction`), contoh nyata di `examples/`, template isian, disclaimer keuangan, dan penolakan untuk memoles angka atau memberi nasihat investasi.

## Pembagian lisensi bagian ini
- **Metodologi yang diadaptasi** (pengelompokan rasio likuiditas/profitabilitas/leverage/efisiensi, rumus dasar rasio, gagasan tafsiran berjenjang per industri) di `SKILL.md` dan `references/ambang-wajar.md`: turunan dari materi MIT `anthropics/claude-cookbooks`. Bagian ini tunduk pada ketentuan MIT (lihat `LICENSE-MIT`) dan sudah ditulis ulang total dalam bahasa Indonesia.
- **Semua bagian lain**, yaitu `scripts/rasio.py` (ditulis baru, tidak menyalin kode sumber), `tests/`, `templates/`, `examples/`, `README.md`, dan tabel ambang UMKM, adalah karya orisinal Komunitech.

Penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian, ditambah ketentuan MIT pada bagian yang disebut di atas.

## Riwayat versi
### v1.0.1 (2026-09-26): revisi dari HASIL-UJI (skor 8)
- Tren antarperiode kini memakai basis yang sama (saldo akhir) untuk semua periode, dan basisnya ditulis di output. Sebelumnya periode terakhir memakai rata-rata saldo sedangkan periode pertama memakai saldo akhir, sehingga ROA warung tampil membaik padahal memburuk dan lama piutang konveksi tampil 61 hari padahal 75.
- CSV berpemisah koma dengan angka ribuan tanpa tanda kutip (`Kas,1,250,000`) kini ditolak dengan GALAT yang jelas, tidak lagi terbaca Rp 1. Kolom kosong di ujung (ekspor Excel) tetap diterima.
- Data minim (< 5 rasio bisa dinilai) menghasilkan status/ringkasan/kesiapan KUR "DATA BELUM CUKUP" beserta daftar pos yang kosong, tidak lagi "pertahankan".
- Saran kontekstual: rasio cepat rendah dengan stok kecil (< 30% aset lancar) diarahkan ke utang/kas, bukan "kurangi stok". ROA rendah dengan stok kecil diarahkan ke pemakaian alat. Saran cicilan membedakan rencana vs cicilan berjalan.
- Ringan: peringatan bila `--bagian-lancar-utang-bank` > utang bank; catatan periode pendek tidak lagi membuat status SEMENTARA; tebakan jenis usaha memakai kata utuh dengan prioritas produksi/kuliner ("jasa fotokopi" → jasa, "toko kue"/"warung kopi"/"jasa katering" → produksi).
- Tes regresi 56 → 71 (G1–G15), semua tes lama tetap lulus.

### v1.0.0 (2026-09-26): rilis awal, status `draft`
Belum diuji penguji independen (Tahap 6). Tes regresi pembuat: `tests/uji_regresi.py` (56 uji lulus).
