# 00 — Uji A/B: skenario 01 (leaflet cabut gigi) TANPA skill vs DENGAN skill

**Input pengguna (sama persis untuk keduanya):**
> tolong bikinin leaflet buat pasien abis cabut gigi, sekalian versi wa yg pendek. dari drg rina poinnya: gigit kapas/tampon 30 menit jgn dilepas2, jgn kumur2 dulu 24 jam, jgn dihisap2 bekas cabutnya, makan yg lembut & dingin dulu 2 hari, obat amoxicillin 500mg 3x1 dihabiskan 5 hari, asam mefenamat 500mg kalo nyeri max 3x sehari. kalo darah ga berhenti lebih dr 1 jam langsung ke klinik. kontrol 7 hari lagi. klinik gigi senyum sejahtera

Metode: output A ditulis penguji sebagai AI agent umum yang **tidak** membaca skill apa pun, meniru kebiasaan asisten umum. Output B adalah hasil dengan skill (lengkap di `01-leaflet-cabut-gigi.md`).

---

## A. TANPA skill

```
🦷 KLINIK GIGI SENYUM SEJAHTERA
PANDUAN PERAWATAN SETELAH CABUT GIGI

Terima kasih telah mempercayakan perawatan gigi Anda kepada kami. Agar proses penyembuhan
berjalan lancar, ikuti panduan berikut:

1. Gigit kapas/tampon selama 30 menit. Jangan dilepas-lepas.
2. Jangan berkumur selama 24 jam pertama.
3. Jangan menghisap area bekas cabut, dan hindari minum dengan sedotan.
4. Makan makanan lembut dan dingin selama 2 hari. Hindari makanan keras, pedas, dan panas.
5. Jangan merokok dan minum alkohol minimal 48–72 jam.
6. Kompres dingin di pipi 10–15 menit untuk mengurangi bengkak.
7. Tidur dengan kepala sedikit ditinggikan pada malam pertama.
8. Setelah 24 jam, boleh berkumur perlahan dengan air garam hangat 3–4 kali sehari.

💊 OBAT
- Amoxicillin 500 mg, 3x1, dihabiskan dalam 5 hari (walau sudah tidak sakit).
- Asam mefenamat 500 mg bila nyeri, maksimal 3x sehari, diminum setelah makan.

⚠️ SEGERA HUBUNGI KLINIK JIKA:
- Perdarahan tidak berhenti lebih dari 1 jam
- Demam di atas 38°C
- Bengkak makin besar setelah hari ke-3
- Nyeri hebat yang muncul lagi 2–4 hari setelah pencabutan (kemungkinan dry socket)

📅 Kontrol: 7 hari lagi.

Semoga lekas pulih! 😊
```
Versi WA pendek:
```
Halo! Setelah cabut gigi: gigit kapas 30 mnt, jgn kumur 24 jam, jgn pakai sedotan/merokok,
makan lembut & dingin 2 hari. Obat: Amoxicillin 3x1 (habiskan 5 hari), asam mefenamat bila
nyeri maks 3x/hari sesudah makan. Darah >1 jam atau demam >38°C → hubungi klinik. Kontrol
7 hari lagi. Lekas sembuh! 🦷
```

## B. DENGAN skill
Lihat `01-leaflet-cabut-gigi.md`. Ringkasnya: semua poin dan obat persis dari drg. Rina, dikelompokkan ✅/🚫/💊/⚠️/📅. Tanggal kontrol dan nomor klinik ditulis `[isi …]`. Ada kalimat keselamatan IGD/119, dan versi WA pendek tidak menambah instruksi.

---

## Penilaian berdampingan

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Kesetiaan pada instruksi dokter | ❌ **8 tambahan yang tidak diberikan dokter**: sedotan, rokok/alkohol 48–72 jam, kompres dingin, kepala ditinggikan, kumur air garam, "sesudah makan" untuk asam mefenamat, "hindari pedas/panas", "habiskan walau tidak sakit" | ✅ 100% dari input. Satu-satunya tambahan hanyalah label golongan obat (lihat catatan RINGAN di 01) |
| Tanda bahaya | ❌ Menambah "demam >38 °C", "bengkak setelah hari ke-3", dan menyebut kemungkinan "dry socket" (**menyerupai diagnosis**) | ✅ Hanya "darah >1 jam" dari dokter, plus kalimat baku IGD/119 tanpa menilai kegawatan |
| Instruksi yang bertentangan | ❌ "Setelah 24 jam boleh kumur air garam" bisa bertentangan dengan protokol dokter, yang hanya menyebut "jangan kumur 24 jam" | ✅ Tidak ada |
| Data yang kurang | ❌ Tanggal kontrol & nomor klinik tidak ditandai; leaflet terlihat "lengkap" padahal belum | ✅ `[isi tanggal kontrol]`, `[isi nomor klinik]` + catatan agar dilengkapi |
| Keselamatan | ❌ Tidak ada rujukan IGD/119 | ✅ Ada |
| Kerapian & siap kirim | Rapi | Rapi, struktur konsisten dengan template |
| Tanggung jawab hukum klinik | Berisiko: klinik menyebarkan instruksi medis yang tidak diputuskan dokternya | Aman: isi medis bisa dipertanggungjawabkan dokter |

**Kesimpulan:** hasil dengan skill **jelas lebih baik**. Perbedaan utamanya bukan gaya bahasa. AI tanpa skill secara alami "membantu" dengan menambah instruksi medis generik dan tanda bahaya, bahkan menyebut kemungkinan diagnosis (dry socket). Untuk klinik, itu berisiko: pasien menerima instruksi yang tidak diberikan dokternya. Skill mencegah hal ini secara konsisten. Nilai tambah ini bisa dipakai sebagai materi "sebelum/sesudah" di README.
