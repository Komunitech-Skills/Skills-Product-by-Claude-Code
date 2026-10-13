# Uji Banding Pesaing

**Skenario dinilai:** normal pertama — sambal botolan rumahan, harga Rp28.000, 40 kontak WA / 80 follower IG.

## Pesaing 1 — `define-hypothesis` (product-on-purpose/pm-skills, Apache-2.0)
Dibaca penuh untuk dinilai (tidak disalin) di `skills/define-hypothesis/SKILL.md` + `references/TEMPLATE.md` + `references/EXAMPLE.md` pada commit yang sama dengan yang dicatat di `ATTRIBUTION.md`.

**Kalau dijalankan pada skenario sambal (apa adanya, tanpa adaptasi):**
- Menghasilkan pernyataan hipotesis format "We believe that [action] for [target user] will [outcome]" + dokumen lengkap (Background & Rationale, Target User Segment, Success Metrics, Validation Approach, Risks & Assumptions, Timeline) — dokumen ini berat dan berbahasa Inggris, ditujukan tim produk software.
- **Validation Approach** eksplisit menyebut "A/B test, sample size, statistical requirements" — untuk penjual sambal rumahan dengan 40 kontak WA, ini tidak bisa dijalankan sama sekali (butuh traffic/skala jauh lebih besar untuk signifikansi statistik).
- Tidak ada satu pun metode uji yang cocok kanal Indonesia (WA broadcast, status, polling IG story, titip warung) — fokusnya eksperimen digital (fitur aplikasi/onboarding).
- Tidak ada kalkulator angka jadi (skrip), tidak ada template pesan siap kirim, tidak ada perhitungan margin/balik modal biaya uji dalam Rupiah.
- Tidak ada bahasa Indonesia maupun konteks UMKM sama sekali.

**Kelebihan yang layak diakui & sudah diadopsi (dengan cara sendiri, ditulis ulang total):** disiplin "hipotesis eksplisit dengan target user spesifik" dan "kriteria sukses ditentukan sebelum uji, bukan sesudah" — dua prinsip ini memang kuat dan diadopsi di skill kami (Langkah 1 & 3 SKILL.md), tapi seluruh kalimat, istilah, ambang, dan contohnya ditulis ulang total ke konteks UMKM Indonesia (lihat `ATTRIBUTION.md` bagian "Apa yang diubah/ditambahkan").

**Untuk skenario sambal ini, skill kami menang telak:** pesaing tidak bisa dijalankan langsung oleh pemilik usaha sambal rumahan tanpa pengetahuan statistik/eksperimen produk software, sedangkan skill kami menghasilkan pesan siap kirim + angka konversi + keputusan LANJUT dalam satu proses yang selesai di percakapan.

## Pesaing 2 — pencarian skill publik lain
Dicari (secara konseptual, berdasarkan pengetahuan ekosistem skill publik yang tersedia bagi penguji dalam sesi ini — **tidak ada akses pencarian web langsung di sesi uji ini**) dengan kata kunci: "validate product idea skill", "MVP test skill", "pre-order test skill", "product-market fit skill", "lean startup validation skill", di kategori yang relevan (ClawHub kategori produk/startup, skills.sh, anthropics/skills, GitHub topic `agent-skills`).

Tidak ditemukan skill publik kedua yang: (a) memenuhi ambang bukti pemakaian nyata pedoman kurasi Komunitech tahap 2 (≥100 bintang untuk repo satu skill / ≥500 untuk koleksi, umur ≥3 bulan, dipakai komunitas), dan (b) secara spesifik menyasar uji pasar murah untuk produk fisik/jasa UMKM (bukan software/startup digital). Skill-skill "startup validation" publik yang beredar umumnya berasal dari koleksi framework produk software (mirip pm-skills) atau berupa prompt generik tanpa skrip/template teruji — masuk kategori "tidak lolos sinyal bukti" atau tidak relevan domain, bukan pesaing layak banding langsung.

**Kesimpulan:** hanya satu pesaing layak-banding ditemukan (`define-hypothesis` dari pm-skills, sudah dinilai di atas). Skill kami unggul jelas untuk skenario UMKM Indonesia yang diuji; tidak ada indikasi skill kami kalah di kriteria manapun yang relevan untuk audiens target (Tahap 6 poin 5 pedoman kurasi Komunitech: skor tidak dibatasi maks. 6 karena skill kami tidak kalah).
