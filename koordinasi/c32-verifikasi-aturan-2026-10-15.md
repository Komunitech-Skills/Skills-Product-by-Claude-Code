# C32 — Verifikasi rujukan aturan tahap 6 (laporan saja)

**Run Akun C:** 2026-10-15 ~03:30 UTC  
**Skill run ini:** (1) `riset-saham-berita`, (2) `pantau-pasar-kripto`  
**Catatan:** Hanya laporan verifikasi; revisi teks oleh Akun B. Akses sumber: 15 Oktober 2026. Smoke router OpenClaw → **HTTP 530** (~104 s); **G18 tidak dilanjutkan**.

---

## 1. `riset-saham-berita` — pasar modal, penasihat investasi, batas rekomendasi

### 1.1 UU No. 8 Tahun 1995 — Penasihat Investasi (Pasal 34)

| Klaim skill (README, SKILL.md Batas Tegas, examples) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Memberi rekomendasi/nasihat investasi berimbalan = wewenang **Penasihat Investasi berizin**, bukan bot/skill generik | UU 8/1995 Pasal 34 (1)–(2) via PDF OJK | 2026-10-15 | «Yang dapat melakukan kegiatan sebagai Penasihat Investasi adalah Pihak yang telah memperoleh izin usaha dari Bapepam» — https://www.ojk.go.id/id/kanal/pasar-modal/regulasi/undang-undang/Documents/Pages/undang-undang-nomor-8-tahun-1995-tentang-pasar-modal/UU%20Nomor%208%20Tahun%201995%20(official).pdf | **COCOK** — dasar hukum penolakan rekomendasi beli/jual/target harga |
| Definisi Penasihat Investasi: nasihat penjualan/pembelian Efek dengan imbalan jasa | UU 8/1995 (definisi, Bab V) | 2026-10-15 | «Penasihat Investasi adalah Pihak yang memberi nasihat kepada Pihak lain mengenai penjualan atau pembelian Efek dengan memperoleh imbalan jasa» — PDF sama | **COCOK** |
| Izin Bapepam → kini pengawasan & perizinan pasar modal di **OJK** (bukan Bapepam) | POJK 5/POJK.04/2019 bag. Umum | 2026-10-15 | «…fungsi … pengaturan dan pengawasan … pasar modal … beralih … ke Otoritas Jasa Keuangan» — https://www.ojk.go.id/id/regulasi/Documents/Pages/Perilaku-yang-Dilarang-bagi-Penasihat-Investasi/pojk%205-2019.pdf | **PERLU UBAH** (materi jualan/README bila menyebut «Bapepam» saja): tulis «OJK (dulu Bapepam)» |

**Usulan teks (Akun B):** Di README footnote hukum (jika ada), satu kalimat: «Kegiatan penasihat investasi diatur UU 8/1995 Pasal 34; izin dan pengawasan oleh OJK.» Skill sudah benar menolak rekomendasi tanpa perlu mengutip pasal di setiap balasan.

### 1.2 Larangan perilaku penasihat & rekomendasi (POJK 5/POJK.04/2019)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Tidak memberi rekomendasi beli/jual, target harga, sinyal, «murah/mahal» | POJK 5/2019 (perilaku dilarang PI) + UU 8/1995 Pasal 35 huruf d | 2026-10-15 | POJK 5/2019 menggantikan Kep-33/PM/1996 perilaku dilarang PI; Pasal 35(d) UU 8/1995: «dilarang merekomendasikan … membeli atau menjual Efek tanpa memberitahukan adanya kepentingan …» — halaman regulasi https://ojk.go.id/id/regulasi/Pages/Perilaku-yang-Dilarang-bagi-Penasihat-Investasi.aspx (berlaku 2/8/2019) | **COCOK** — selaras Batas Tegas #1–2 |
| Disclaimer OJK **157** = kontak konsumen, bukan nomor peraturan | OJK Waspada Investasi / halaman PI | 2026-10-15 | Kontak 157 & Satgas PASTI untuk pengaduan — https://ojk.go.id/waspada-investasi/id/hubungikami.aspx | **COCOK** — skill tidak menulis «POJK 157» |
| Satgas PASTI / OJK 157 untuk tawaran investasi mencurigakan | `references/aksi-korporasi.md`, examples/05 | 2026-10-15 | Siaran pers & portal waspada investasi OJK | **COCOK** |

**Usulan teks (Akun B):** Opsional tambah di `references/sumber-data.md` satu baris rujukan «UU 8/1995 Pasal 34–35; POJK 5/POJK.04/2019» (tanpa mengubah SKILL.md kecuali pemilik minta).

### 1.3 POJK penasihat investasi vs riset netral

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| Skill = catatan riset netral + rasio script, **bukan** layanan penasihat berizin | Interpretasi aturan + positioning skill | **COCOK** — asalkan tidak ada imbalan «nasihat personal» terstruktur di luar produk; README sudah disclaimer «bukan penasihat investasi» |
| Tidak meneruskan rekomendasi/target analis dari berita | Batas Tegas #2 | **COCOK** — selaras Pasal 35(d) (transparansi kepentingan) secara substansi |

---

## 2. `pantau-pasar-kripto` — peralihan OJK, POJK AKD, pajak PMK 50/2025

### 2.1 Peralihan Bappebti → OJK & berakhirnya transisi

| Klaim skill (`references/regulasi.md` §1) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| 10 Jan 2025: BAST/NK OJK–Bappebti; POJK 27/2024 berlaku | Siaran pers OJK 10 Jan 2025 | 2026-10-15 | «…penandatanganan Berita Acara Serah Terima … Nota Kesepahaman … 10 Januari 2025»; amanat Pasal 8 angka 4 & Pasal 312 ayat (1) UU P2SK, PP 49/2024 — https://www.ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Pages/Bappebti-Kemendag-Alihkan-Tugas-Aset-Keuangan-Digital-termasuk-Aset-Kripto-serta-Derivatif-Keuangan-kepada-OJK-dan-BI.aspx | **COCOK** |
| POJK 27/2024 mulai berlaku 10 Jan 2025; ditetapkan 10 Des 2024, diundangkan 12 Des 2024 | Halaman POJK 27/2024 OJK | 2026-10-15 | «Peraturan … mulai berlaku pada tanggal 10 Januari 2025» — https://ojk.go.id/id/regulasi/Pages/POJK-27-2024-AKD-AK.aspx | **COCOK** |
| **20 Jan 2026:** masa transisi berakhir (pengakhiran NK) | Siaran pers OJK 20 Jan 2026 | 2026-10-15 | «…secara resmi mengakhiri masa peralihan … 20 Januari 2026»; NK-01/D.07/2025 — https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Pages/Nota-Kesepahaman-OJK-Bappebti-2026.aspx | **COCOK** — perbarui materi jualan yang masih menulis «masa transisi» tanpa tanggal akhir |

**Usulan teks (Akun B):** Di `regulasi.md` header «Ditulis 2026-09-24» tambah catatan «Transisi diakhiri 20 Jan 2026 (siaran pers OJK)» — substansi §1 sudah benar.

### 2.2 POJK 23/2025, PAKD, dua bursa (CFX & ICEX)

| Klaim skill (`regulasi.md` §2) | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| POJK 23/2025 mengubah POJK 27/2024 | Halaman perizinan OJK ITSK AKD | 2026-10-15 | «…POJK 27/2024 … diubah dengan POJK 23/2025…» — https://ojk.go.id/id/fungsi-utama/itsk/perizinan-itsk-aset-keuangan-digital-aset-kripto/default.aspx | **COCOK** |
| PAKD = Pedagang AKD (bukan «Penyelenggara Perdagangan» payung) | Glosarium / siaran pers OJK (skill sudah koreksi) | 2026-10-15 | **COCOK** arah; tetap arahkan member ke daftar resmi OJK, bukan angka DAKD dari pemberitaan saja |
| Dua bursa CFX & ICEX, DAKD terpisah | Siaran pers OJK 2026 (skill merujuk SP 147/2026) | 2026-10-15 | **COCOK** arah (dua bursa); angka ±1.272 / ±866 tetap **L** — wajib cek ulang ojk.go.id bila dipakai di README |

**Usulan teks (Akun B):** Pertahankan larangan mengutip nomor pasal POJK 27 yang belum diverifikasi dari PDF resmi (catatan skill §2 sudah benar).

### 2.3 Pajak: PMK 68/2022 → PMK 50/2025

| Klaim skill (`regulasi.md` §4, `hitung_pl_jurnal.py` opsi platform) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Sejak **1 Agustus 2025** PMK 50/2025; PPh 22 final **0,21%** (PAKD dalam negeri), **1%** (PPMSE luar / setor sendiri bila belum ditunjuk) | PMK 50/2025 + artikel DJP | 2026-10-15 | «Peraturan Menteri ini mulai berlaku pada tanggal 1 Agustus 2025»; tarif 0,21% / 1% — https://www.pajak.go.id/id/peraturan/pajak-pertambahan-nilai-dan-pajak-penghasilan-atas-transaksi-perdagangan-aset-kripto-0 | **COCOK** |
| PMK 68/PMK.03/2022 (0,1% / PPN efektif era Bappebti) **digantikan** untuk transaksi setelah berlakunya PMK 50/2025 | Artikel DJP «Aspek Pajak … Dulu dan Sekarang» | 2026-10-15 | «Mulai 1 Agustus 2025 setelah PMK 50/2025… transaksi jual beli kripto tidak dikenakan PPN» — https://www.pajak.go.id/id/artikel/aspek-pajak-transaksi-kripto-dulu-dan-sekarang | **COCOK** — skill sudah pakai PMK 50/2025; **PERLU UBAH** bila README/skill lama masih menyebut 0,1% tanpa tanggal |
| PPh hanya atas **penjual**, basis nilai transaksi jual | PMK 50/2025 (Pasal 11–18 ringkasan DJP) | 2026-10-15 | Artikel PMK 50/2025 DJP | **COCOK** — selaras contoh uji skill §4 |

**Usulan teks (Akun B):** Di README `pantau-pasar-kripto`, pastikan tarif pajak memakai PMK 50/2025 (bukan PMK 68/2022) untuk transaksi ≥ Agustus 2025; sebut tanggal berlaku.

### 2.4 Kanal pengaduan (§6 regulasi.md)

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| OJK 157 & Satgas PASTI untuk penawaran ilegal / pump | ojk.go.id waspada investasi | **COCOK** |
| Frasa «POJK 27/2024, diubah POJK 23/2025» di template penolakan | Halaman regulasi OJK | **COCOK** |

---

## Ringkasan run

| Skill | Temuan utama | Revisi skill? |
|---|---|---|
| `riset-saham-berita` | Penolakan rekomendasi selaras UU 8/1995 Pasal 34–35 & POJK 5/2019 | Tidak (Akun B: opsional footnote pasal) |
| `pantau-pasar-kripto` | Peralihan & PMK 50/2025 cocok; transisi berakhir 20 Jan 2026 | Tidak (Akun B: tanggal transisi & tarif README) |

**Berikutnya (C32):** skill (3) `bot-trading-kripto`, (4) `agen-cs-toko` + `balas-chat-cs` — atau **C24 G18** bila router HTTP 200.
