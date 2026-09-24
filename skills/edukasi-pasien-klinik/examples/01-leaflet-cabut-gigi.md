# 01 — Leaflet & pesan WA setelah cabut gigi (skenario normal)

**Skenario:** Admin klinik gigi (awam) menyalin poin singkat dari dokter gigi dan minta leaflet + pesan WA pendek untuk pasien. Nomor klinik dan tanggal kontrol tidak diberikan.

**Input pengguna (persis):**
> tolong bikinin leaflet buat pasien abis cabut gigi, sekalian versi wa yg pendek. dari drg rina poinnya: gigit kapas/tampon 30 menit jgn dilepas2, jgn kumur2 dulu 24 jam, jgn dihisap2 bekas cabutnya, makan yg lembut & dingin dulu 2 hari, obat amoxicillin 500mg 3x1 dihabiskan 5 hari, asam mefenamat 500mg kalo nyeri max 3x sehari. kalo darah ga berhenti lebih dr 1 jam langsung ke klinik. kontrol 7 hari lagi. klinik gigi senyum sejahtera

---

## Output

### A. Leaflet (siap tempel WA / cetak)

```
🏥 Klinik Gigi Senyum Sejahtera
Perawatan Setelah Cabut Gigi — [tanggal hari ini]

Terima kasih sudah datang hari ini. Berikut panduan perawatan di rumah dari drg. Rina:

✅ Boleh / dianjurkan
- Gigit kapas/tampon selama 30 menit. Jangan dilepas-lepas dulu.
- Makan makanan yang lembut dan dingin dulu, selama 2 hari.

🚫 Hindari dulu
- Jangan berkumur selama 24 jam.
- Jangan menghisap-hisap bagian bekas cabut gigi.

💊 Obat (sesuai resep drg. Rina)
- Amoxicillin (antibiotik) 500 mg — 3× sehari — dihabiskan selama 5 hari.
- Asam mefenamat (obat pereda nyeri) 500 mg — diminum bila nyeri — paling banyak 3× sehari.

⚠️ Segera ke klinik bila:
- Darah tidak berhenti lebih dari 1 jam.

📅 Kontrol berikutnya
- 7 hari lagi, yaitu [isi tanggal kontrol dari klinik], di Klinik Gigi Senyum Sejahtera.

📞 Ada pertanyaan? Hubungi kami di [isi nomor/kontak klinik].

Catatan: pesan ini bukan pengganti konsultasi. Kalau kondisi memburuk atau terasa darurat,
segera ke IGD terdekat atau hubungi 119 — jangan menunggu balasan chat ini.
```

### B. Versi WA pendek

```
Halo, terima kasih sudah berobat di Klinik Gigi Senyum Sejahtera hari ini 🙏

Pesan drg. Rina setelah cabut gigi:
✅ Gigit kapas 30 menit, jangan dilepas-lepas
✅ Makan lembut & dingin dulu 2 hari
🚫 Jangan kumur 24 jam, jangan hisap-hisap bekas cabut
💊 Amoxicillin 500 mg 3× sehari, dihabiskan 5 hari
💊 Asam mefenamat 500 mg bila nyeri, maks. 3× sehari
⚠️ Darah tidak berhenti lebih dari 1 jam → segera ke klinik
📅 Kontrol: [isi tanggal], 7 hari lagi

Pertanyaan: [isi nomor klinik]. Kondisi darurat → IGD terdekat / 119.
```

*Mohon dilengkapi sebelum dikirim:* `[tanggal hari ini]`, `[isi tanggal kontrol dari klinik]` (skill tidak menghitung jadwal kontrol sendiri), dan `[isi nomor/kontak klinik]`.

---

## Catatan penguji
- ✅ Semua instruksi (kapas 30 menit, tidak kumur 24 jam, tidak menghisap, makan lembut/dingin 2 hari, dua obat + aturan pakai, tanda "darah >1 jam", kontrol 7 hari) **persis dari input**. Tidak ada tambahan umum yang biasa dikarang AI (mis. "jangan merokok 48 jam", "jangan pakai sedotan", "kompres es", "demam >38 °C").
- ✅ Dosis & frekuensi disalin persis, tidak diubah. Tanggal kontrol tidak dihitung sendiri → `[isi …]`.
- ✅ Kalimat keselamatan IGD/119 dari template, bukan penilaian kegawatan.
- ⚠️ (RINGAN) Label "(antibiotik)" dan "(obat pereda nyeri)" ditambahkan karena `references/bahasa-awam-pasien.md` prinsip 2 menyuruh memberi penjelasan singkat nama obat. Isinya umum & benar, tapi secara teknis **informasi yang tidak diberikan dokter** — bertentangan tipis dengan aturan "tidak menambah". Saran: prinsip 2 dibatasi ke "golongan obat bila dokter/apoteker menyebutnya; bila tidak, biarkan nama obat saja".
- ⚠️ SKILL.md tidak menyebut format "versi WA pendek" terpisah; agent tetap bisa membuatnya dari template, tapi sebaiknya ada pola ringkas di `templates/leaflet-pasca-tindakan.md`.
