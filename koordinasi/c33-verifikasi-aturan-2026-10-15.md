# C33 — Verifikasi rujukan aturan tahap 7 (laporan saja)

**Run Akun C:** 2026-10-15 ~05:30 UTC  
**Skill run ini:** (1) `sop-onboarding`, (2) `laporan-insiden-usaha`  
**Catatan:** Hanya laporan verifikasi; revisi teks oleh Akun B. Akses sumber: 15 Oktober 2026. Smoke router OpenClaw → **HTTP 530** (~77 s); **G18 tidak dilanjutkan**.

---

## 1. `sop-onboarding` — masa percobaan PKWTT, larangan percobaan PKWT, BPJS

### 1.1 Masa percobaan PKWTT (maks. 3 bulan, upah ≥ UMK)

| Klaim skill (SKILL.md, contoh uji, checklist) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Masa percobaan hanya PKWTT, maks. 3 bulan | UU 13/2003 Pasal 60 ayat (1) | 2026-10-15 | «Perjanjian kerja untuk waktu tidak tertentu dapat mensyaratkan masa percobaan kerja paling lama 3 (tiga) bulan.» — https://jdih.kemnaker.go.id/asset/data_puu/2003uu013.pdf | **COCOK** |
| Upah masa percobaan tidak boleh di bawah upah minimum | UU 13/2003 Pasal 60 ayat (2) | 2026-10-15 | «…pengusaha dilarang membayar upah di bawah upah minimum yang berlaku.» — PDF sama | **COCOK** — skill menolak jebakan gaji 70% UMR |
| Dasar hukum disebut PP 35/2021 + UU 13/2003 Ps. 60 jo. UU 6/2023 | PP 35/2021; UU 6/2023 | 2026-10-15 | PP 35/2021 mengimplementasikan Cipta Kerja; Ps. 60 UU 13/2003 masih berlaku sebagaimana diubah | **COCOK** arah; **PERLU UBAH** (ringan): bila README/SKILL menyebut «Ps. 58» untuk larangan PKWT, selaraskan dengan PP 35/2021 Pasal 12 (bukan hanya UU 13/2003 Ps. 58) |

**Usulan teks (Akun B):** Satu baris footnote: «Masa percobaan: UU 13/2003 Pasal 60 (maks. 3 bulan, upah ≥ UMK).»

### 1.2 PKWT tidak boleh mensyaratkan masa percobaan

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| PKWT dilarang punya klausul masa percobaan; batal demi hukum | PP 35/2021 Pasal 12 | 2026-10-15 | «(1) PKWT tidak dapat mensyaratkan adanya masa percobaan kerja. (2) … batal demi hukum dan masa kerja tetap dihitung.» — https://jdih.kemnaker.go.id/asset/data_puu/PP352021.pdf | **COCOK** — selaras contoh jebakan barista PKWT |
| Contoh uji mengutip UU 13/2003 Pasal 58 jo. UU 6/2023 Ps. 81 angka 14 | UU 6/2023; MK | 2026-10-15 | Putusan MK menguatkan percobaan di PKWT batal demi hukum, masa kerja tetap dihitung — https://www.mkri.id/berita/-21783 | **COCOK** substansi; **PERLU UBAH** (klarifikasi): tambahkan rujukan eksplisit **PP 35/2021 Pasal 12** di SKILL/examples agar pembeli awam tidak bingung |

**Usulan teks (Akun B):** «PKWT: tidak boleh ada masa percobaan (PP 35/2021 Pasal 12; bila tetap dicantumkan, klausul batal demi hukum).»

### 1.3 Pendaftaran BPJS (30 hari, wajib — bukan ditunda)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| BPJS Ketenagakerjaan & Kesehatan wajib; contoh «paling lambat 30 hari sejak mulai kerja» | PP 45/2015 Pasal 4 ayat (2) (JK/JP); portal BPJS Ketenagakerjaan | 2026-10-15 | «…mendaftarkan Pekerja yang baru paling lama 30 (tiga puluh) hari terhitung sejak tanggal Pekerja tersebut mulai bekerja.» — https://jdih.kemnaker.go.id/asset/data_puu/PP_NOMOR_45_TAHUN2015.PDF ; FAQ BPJS: formulir paling lambat 30 hari sejak mulai bekerja — https://www.bpjsketenagakerjaan.go.id/search.html/ | **COCOK** untuk **BPJS Ketenagakerjaan** (pendaftaran pekerja baru) |
| «Wajib sejak H1», bukan setelah lolos percobaan | Praktik kepesertaan + PP 45/2015 | 2026-10-15 | Kewajiban pendaftaran tidak menunda sampai evaluasi percobaan | **COCOK** — skill menolak jebakan «BPJS nanti setelah lolos» |
| SKILL.md tidak membedakan program JKK/JHT vs hanya «BPJS» generik | PP 46/2015 (JHT), PP 44/2015 (JKK), dll. | 2026-10-15 | Masing-masing program punya PP penyelenggaraan; tenggat 30 hari umum untuk pendaftaran pekerja baru | **COCOK** untuk UMKM awam; **PERLU UBAH** (opsional): footnote «dasar tenggat 30 hari: PP 45/2015 Ps. 4(2); program JKK/JHT/JP/Kesehatan terpisah» |

**Usulan teks (Akun B):** Checklist baku: «Daftarkan pekerja ke BPJS Ketenagakerjaan paling lambat 30 hari sejak mulai kerja (PP 45/2015 Ps. 4 ayat 2); BPJS Kesehatan wajib terpisah — ikuti ketentuan BPJS Kesehatan.»

### 1.4 Tafsir tanggal batas 3 bulan (bukan kepastian hukum)

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| Batas hukum = tanggal sama 3 bulan kalender − 1 hari; evaluasi keputusan 5 hari kerja sebelumnya | UU 13/2003 Ps. 60 tidak merinci perhitungan harian | **COCOK** — skill sudah menandai **tafsir**, bukan kepastian hukum (disclaimer ada) |

---

## 2. `laporan-insiden-usaha` — cakupan K3 vs klaim aturan

### 2.1 Apakah skill mengutip UU 1/1970, PP 50/2012 SMK3, Permenaker 5/2018, lapor 2×24 jam?

| Klaim / tidak-klaim | Temuan di repo | Kesimpulan |
|---|---|---|
| Brief C33 menyebut verifikasi UU 1/1970 K3, PP 50/2012, Permenaker 5/2018, pelaporan 2×24 jam | **SKILL.md / README / references** tidak mengutip UU 1/1970, PP 50/2012, atau Permenaker 5/2018 untuk kecelakaan kerja | **COCOK** — skill **sengaja** mengecualikan kecelakaan kerja berat (SKILL.md: arahkan ke pihak berwenang, bukan format laporan operasional) |
| UU PDP Pasal 46 (3×24 jam) untuk kebocoran data | UU 27/2022 Pasal 46 | **COCOK** — sudah diverifikasi di uji internal (bukan fokus C33 run ini) |

**Catatan verifikator:** Papan tugas C33 merujuk **Permenaker 5/2018** untuk batas **2×24 jam** pelaporan kecelakaan — **tidak tepat**. Permenaker **5/2018** = K3 **lingkungan kerja** (bukan tata cara lapor kecelakaan). Batas **2×24 jam** ke BPJS Ketenagakerjaan + Dinas ada di **Permenaker 5/2021 Pasal 8** (program JKK). UU **1/1970 Pasal 11** mewajibkan pengurus melaporkan kecelakaan ke pejabat yang ditunjuk Menteri, **tanpa** angka 2×24 jam di batang tubuh UU.

| Aturan (referensi pembanding, bukan klaim skill) | Sumber | Tanggal akses | Kutipan ringkas | Relevansi skill |
|---|---|---|---|---|
| Kewajiban lapor kecelakaan (pengurus) | UU 1/1970 Pasal 11 ayat (1) | 2026-10-15 | «Pengurus diwajibkan melaporkan tiap kecelakaan … pada pejabat yang ditunjuk oleh Menteri Tenaga Kerja.» — https://lapormenaker.kemnaker.go.id/uploads/file/UU%20Nomor%201%20Tahun%201970.pdf | Skill **tidak** mengisi formulir K3 — **benar** |
| Lapor tahap I paling lambat 2×24 jam | Permenaker 5/2021 Pasal 8 ayat (2) | 2026-10-15 | «…paling lama 2 x 24 jam sejak terjadinya Kecelakaan Kerja atau sejak didiagnosis PAK.» — https://pasal.id/peraturan/permen/permenaker-no-5-tahun-2021 | **Usulan materi jualan (Akun B):** bila nanti README menambah catatan «insiden kecelakaan kerja → lapor Kemnaker/BPJS», gunakan **Permenaker 5/2021**, bukan 5/2018 |
| SMK3 sistem manajemen | PP 50/2012 | 2026-10-15 | Mengatur SMK3 perusahaan; bukan template laporan insiden operasional UMKM | Di luar cakupan skill saat ini — **tidak perlu klaim** |

**Usulan teks (Akun B):** Pertahankan larangan memaksa format skill untuk kecelakaan kerja. Opsional satu kalimat di README «Di luar cakupan: kecelakaan kerja berat — lapor ke BPJS Ketenagakerjaan/Dinas (Permenaker 5/2021 Ps. 8) dan pihak berwenang, bukan postmortem operasional toko.»

---

## Progress C33

| # | Skill | Status run ini |
|---|---|---|
| 1 | `sop-onboarding` | selesai (§1) |
| 2 | `laporan-insiden-usaha` | selesai (§2) |
| 3 | `notulen-rapat` | menunggu run berikutnya |
| 4 | `kelola-stok` / `buku-stok` | menunggu run berikutnya |
| Ringkasan C25–C33 | `ringkasan-verifikasi-aturan-2026-10-15.md` | setelah §3–4 selesai |
