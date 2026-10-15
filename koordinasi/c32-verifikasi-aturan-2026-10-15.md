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

## 3. `bot-trading-kripto` — API tanpa tarik dana, disclaimer, OJK AKD

**Run Akun C:** 2026-10-15 ~04:00 UTC (lanjutan)

### 3.1 Perizinan & bursa berizin OJK (PAKD)

| Klaim skill (README, SKILL.md, `keamanan-kunci-api.md`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Live utamakan **PAKD berizin OJK**; cek daftar di ojk.go.id | Halaman perizinan AKD OJK | 2026-10-15 | «POJK Nomor 27 Tahun 2024 … diubah dengan POJK Nomor 23 Tahun 2025»; BAST/NK pengalihan Bappebti→OJK **10 Januari 2025** — https://www.ojk.go.id/id/fungsi-utama/itsk/perizinan-itsk-aset-keuangan-digital-aset-kripto/default.aspx | **COCOK** |
| Binance global bukan PAKD berizin → pernyataan tambahan sebelum live | POJK 27/2024 + positioning skill | 2026-10-15 | Perdagangan AKD di Indonesia diatur OJK; bursa luar negeri di luar kerangka PAKD | **COCOK** — selaras SKILL.md §E.7 |
| Bot **bukan** nasihat investasi / sinyal / janji profit | UU 8/1995 Pasal 34 (Penasihat Investasi) — selaras C32 §1 | 2026-10-15 | (cross-check `riset-saham-berita`) | **COCOK** — disclaimer README & SKILL.md |

**Usulan teks (Akun B):** Pastikan README menyebut «cek daftar PAKD/ITSK di ojk.go.id» dengan tanggal akses, bukan daftar statis.

### 3.2 Kunci API — tanpa withdraw

| Klaim skill | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| Izin hanya view + trade; **withdraw dilarang** | `references/keamanan-kunci-api.md`, `siapkan_live.py` DAFTAR PERIKSA | 2026-10-15 | Aturan emas #1 & frasa konfirmasi live `LIVE <kode> SAYA TANGGUNG RISIKONYA` + `--saya-sudah-cek-tanpa-withdraw` | **COCOK** |
| Binance: cek otomatis `apiRestrictions`, tolak bila withdraw | Implementasi `siapkan_live.py --cek-kunci` (audit kode, bukan live) | 2026-10-15 | Script memanggil endpoint baca-saja, bukan withdraw | **COCOK** |
| Indodax: **tidak** memanggil metode withdraw apa pun (termasuk baca-saja) | Keputusan kurator 2026-09-29; SKILL.md §E.4 | 2026-10-15 | Izin withdraw hanya lewat daftar periksa manual member | **COCOK** — selaras keputusan pemilik no. 30 (frasa member + checklist cukup) |
| Kunci tidak disimpan/ditampilkan agent; revoke bila bocor | SKILL.md § langkah awal | 2026-10-15 | Praktik keamanan, bukan norma OJK khusus | **COCOK** |

**Usulan teks (Akun B):** Tidak perlu ubah SKILL; opsional README satu kalimat «Indodax: izin tarik dana dicek manual di situs bursa sebelum live».

### 3.3 Pajak & disclaimer risiko

| Klaim skill | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| PPh final PMK **50/2025** (0,21 % / 1 %), berlaku 1 Agustus 2025 | pajak.go.id PMK 50/2025 — selaras C32 §2 | 2026-10-15 | **COCOK** |
| Peringatan risiko, contoh backtest rugi, default simulasi | README blok PERINGATAN | 2026-10-15 | Selaras POJK/OJK waspada investasi (157) arah edukasi, bukan promosi return | **COCOK** |
| Auto-trading hanya aturan member di akun member | Keputusan pemilik 2026-09-29 | 2026-10-15 | **COCOK** — batas risiko & tombol berhenti di SKILL |

---

## 4. `agen-cs-toko` & `balas-chat-cs` — konsumen, PDP, WhatsApp

**Run Akun C:** 2026-10-15 ~04:00 UTC

### 4.1 UU 8/1999 — Perlindungan Konsumen

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Pelanggan berhak info benar & ganti rugi bila barang tidak sesuai | UU 8/1999 — JDIH BPK | 2026-10-15 | Judul resmi «UU Nomor 8 Tahun 1999 tentang Perlindungan Konsumen»; berlaku 20 April 2000 — https://peraturan.bpk.go.id/Details/45288/uu-no-8-tahun-1999 | **COCOK** — `balas-chat-cs/references/alur-komplain.md` |
| Alur komplain empati → solusi → tindak lanjut | Praktik CS + UU 8/1999 (hak konsumen) | 2026-10-15 | Skill tidak mengutip pasal spesifik di setiap balasan; rujukan di references | **COCOK** |
| Tidak janji ganti rugi otomatis / tidak menggantikan ahli hukum | SKILL.md batasan | 2026-10-15 | **COCOK** |

**Usulan teks (Akun B):** Di `alur-komplain.md`, opsional tambah Pasal 4 (hak atas informasi) & Pasal 7 (hak atas tuntutan ganti rugi) dengan tautan BPK di atas.

### 4.2 UU 27/2022 — Data pelanggan

| Klaim skill | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| Data pelanggan (nama, WA, isi chat) = data pribadi | UU 27/2022 — JDIH BPK | 2026-10-15 | https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022 (metadata & pasal — selaras verifikasi C30) | **COCOK** |
| `agen-cs-toko`: log `cs/log/` minimal, tanpa nama/nomor lengkap | UU 27/2022 Ps. 16 (minimalisasi) + `eskalasi-dan-kanal.md` §3a | 2026-10-15 | **COCOK** |
| `balas-chat-cs`: tidak simpan data pribadi di output template | SKILL.md | 2026-10-15 | **COCOK** arah |
| Promosi WA butuh persetujuan (crm-wa — run berikutnya C32 §5) | UU 27/2022 Ps. 20–21 | 2026-10-15 | **COCOK** arah untuk skill CS umum |

**Usulan teks (Akun B):** README CS sebut «simpan data pelanggan sesuai UU PDP; jangan tempel data sensitif ke chat AI».

### 4.3 WhatsApp — resmi vs Web (OpenClaw)

| Klaim skill (`agen-cs-toko` references, examples) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| **Level 1 Copilot default** — manusia yang kirim ke pelanggan | Keputusan pemilik Komunitech 2026-09-23 | 2026-10-15 | **COCOK** operasional |
| WA Web (OpenClaw/Baileys) **tidak resmi**; risiko blokir; larangan auto-reply massal | WhatsApp Business Messaging Policy | 2026-10-15 | «You may only contact people … opt-in»; otomasi Platform: wajib jalur eskalasi manusia dalam 24 jam — https://www.whatsapp.com/legal/business-policy (perbarui 23 Sep 2026) | **COCOK** — skill menolak auto-balas nomor toko; **PERLU UBAH** README bila masih terkesan «pasang bot auto-reply» tanpa penjelasan Copilot |
| **WhatsApp Business Platform (WABA):** otomasi dengan template & opt-in | Policy §2 | 2026-10-15 | Berbeda dari consumer WA Web; Level 3 skill hanya referensi BSP | **COCOK** arah |
| `balas-chat-cs`: draf untuk admin, bukan kirim otomatis ke pasien (klinik) | examples/00-openclaw | 2026-10-15 | Selaras keputusan medis + WA | **COCOK** |

**Usulan teks (Akun B):** Satu paragraf README `agen-cs-toko`: «Balasan otomatis ke pelanggan di WA butuh WhatsApp Business API resmi + opt-in; OpenClaw WA Web hanya untuk Copilot/notifikasi ke pemilik (nomor terpisah).»

---

## 5. `crm-wa` — persetujuan promosi, UU PDP, WhatsApp Business

**Run Akun C:** 2026-10-15 ~04:30 UTC (lanjutan)

### 5.1 UU 27/2022 — opt-in promo & minimisasi data

| Klaim skill (SKILL.md aturan 6, 10; `references/openclaw-jadwal.md`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Nomor HP pelanggan = data pribadi; jangan tampilkan daftar lengkap ke grup | UU 27/2022 — JDIH BPK | 2026-10-15 | «…melindungi Data Pribadi dalam rangkaian pemrosesan…» — https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022 | **COCOK** |
| Promo hanya ke kontak label `setuju-promo`; pembeli marketplace default belum setuju | UU 27/2022 (persetujuan pemrosesan) + praktik platform | 2026-10-15 | Hak subjek & pemrosesan wajib dasar hukum (UU 27/2022 abstrak BPK) | **COCOK** — selaras aturan 10 SKILL.md |
| Permintaan hapus data → `hapus` dengan konfirmasi | UU 27/2022 hak subjek (akses/penghapusan) | 2026-10-15 | Metadata UU 27/2022 BPK | **COCOK** arah |
| Pengingat Telegram ke pemilik saja, bukan ke pelanggan | Keputusan pemilik 2026-09-23 + `openclaw-jadwal.md` §Aturan | 2026-10-15 | **COCOK** |

**Usulan teks (Akun B):** README opsional satu kalimat: «Label `setuju-promo` = bukti persetujuan sesuai UU PDP; simpan tanggal/sumber persetujuan di catatan kontak.»

### 5.2 Larangan broadcast & WhatsApp Web

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| **Tidak pernah** kirim ke pelanggan; draf + wa.me; pemilik kirim satu per satu | Keputusan pemilik WA Web + SKILL.md aturan 1 | 2026-10-15 | **COCOK** operasional |
| Tolak kirim massal/broadcast; tidak sarankan blast | WhatsApp Business Messaging Policy §1 | 2026-10-15 | «You may only contact people … (b) … opt-in permission … Do not … spam» — https://www.whatsapp.com/legal/business-policy (perbarui 23 Sep 2026) | **COCOK** |
| Integrasi `broadcast-wa` hanya variasi teks + wa.me untuk yang sudah setuju | Policy §1 opt-in + positioning skill | 2026-10-15 | **COCOK** — bukan blast otomatis |

**Usulan teks (Akun B):** Pastikan README menegaskan perbedaan «daftar wa.me untuk copy-paste» vs «WhatsApp Business Platform resmi».

---

## 6. `broadcast-wa` — UU PDP, opt-out, anti-spam WA

**Run Akun C:** 2026-10-15 ~04:30 UTC

### 6.1 UU PDP & persetujuan

| Klaim skill (`references/aturan-pdp-wa.md`, SKILL.md) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Promo wajib persetujuan; tolak database beli / grup / tanpa izin | UU 27/2022 BPK | 2026-10-15 | https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022 | **COCOK** |
| Teks STOP/BERHENTI wajib; patuhi permintaan berhenti | UU 27/2022 (hak subjek menarik persetujuan) + Policy §1 opt-out | 2026-10-15 | «You must respect … opt out of communications» — WhatsApp Business Policy | **COCOK** |
| Catatan PP pelaksana «BELUM TERVERIFIKASI» di references | Jujur skill | 2026-10-15 | **COCOK** — Akun B bisa tambah PP terbaru bila sudah final di BPK |

**Usulan teks (Akun B):** Ganti atau lengkapi sumber sekunder di `aturan-pdp-wa.md` dengan tautan BPK resmi (baris 17–18) untuk materi jualan.

### 6.2 Kebijakan WhatsApp & volume

| Klaim skill | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| Tolak WA mod/blast tidak resmi | Policy §1; Messaging Guidelines | 2026-10-15 | **COCOK** |
| Broadcast list hanya ke yang simpan nomor kita; batas ~256 (cek terbaru) | Policy + references §2 | 2026-10-15 | **COCOK** arah — skill sudah minta cek batas terbaru |
| Kirim bertahap (batch/jeda) = saran konservatif, bukan aturan resmi | Policy §1 anti-spam | 2026-10-15 | **COCOK** — README jujur «bukan batas resmi» |
| WABA/API resmi + template + opt-in untuk volume besar | Policy §2 Message Template | 2026-10-15 | **COCOK** — selaras penolakan alat blast |
| Variasi pesan ≠ izin kirim tanpa opt-in | references §3 | 2026-10-15 | **COCOK** |

**Usulan teks (Akun B):** Satu paragraf README: «Promo massal resmi lewat WhatsApp Business Platform (API), bukan consumer WA Web/OpenClaw.»

---

## Ringkasan run (kumulatif C32) — **SELESAI 6/6**

| Skill | Temuan utama | Revisi skill? |
|---|---|---|
| `riset-saham-berita` | Penolakan rekomendasi selaras UU 8/1995 & POJK 5/2019 | Tidak (Akun B opsional footnote) |
| `pantau-pasar-kripto` | Peralihan OJK & PMK 50/2025 cocok | Tidak (Akun B: tanggal transisi README) |
| `bot-trading-kripto` | PAKD OJK, no-withdraw, disclaimer selaras | Tidak (Akun B: daftar PAKD dinamis) |
| `agen-cs-toko` / `balas-chat-cs` | UU 8 & UU 27 cocok; WA Web vs Business Policy selaras Copilot | Tidak (Akun B: README WA resmi vs Web) |
| `crm-wa` | Opt-in promo & no-broadcast selaras UU 27 & WA Policy | Tidak (Akun B: footnote setuju-promo) |
| `broadcast-wa` | Opt-in/opt-out & tolak blast selaras UU 27 & WA Policy | Tidak (Akun B: sumber BPK di references) |

**Berikutnya:** **C24 G18** bila router HTTP 200; bila masih 530, antrean tanpa-router habis — fokus G18 atau tugas baru di papan.
