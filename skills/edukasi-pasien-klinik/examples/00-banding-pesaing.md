# 00 — Uji banding pesaing (skenario 01: leaflet cabut gigi)

## Pencarian (24 September 2026)
- Web search: `SKILL.md "patient education" skill`, `clawhub clinic receptionist patient reminder`, `"discharge instructions" OR "patient handout" agent skill`.
- ClawHub API (`clawhub.ai/api/v1/search`): `clinic`, `dental`, `discharge instructions`, `appointment reminder clinic`. Kueri `patient education` dan `patient leaflet` gagal/timeout.
- GitHub: `FreedomIntelligence/OpenClaw-Medical-Skills` (±3k★, MIT, 896 SKILL.md, commit terakhir 21-07-2026), `Open-Medica/open-medical-skills`, dan `VoltAgent/awesome-openclaw-skills` kategori health-and-fitness (tidak ada skill klinik/edukasi pasien).
- Skill berbahasa Indonesia untuk edukasi pasien/klinik: **tidak ditemukan**.

Kandidat yang relevan (hanya dibaca untuk dinilai, script tidak dijalankan, isi tidak disalin):

| Pesaing | Sumber | Lisensi | Sinyal | Relevansi |
|---|---|---|---|---|
| **uae-clinic-arabic-comms** (dralmazrouei) | https://clawhub.ai/dralmazrouei/skills/uae-clinic-arabic-comms | MIT-0 (ClawHub) | 758 unduhan, 16 instal, 1 versi | Paling mirip: komunikasi pasien klinik (pengingat, instruksi pasca-operasi, WA) yang dilokalkan untuk satu negara |
| **patiently-ai** (PharmaTools.AI) | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/tree/main/skills/patiently-ai | MIT (repo) | Bagian dari koleksi ±3k★ | Menyederhanakan dokumen medis untuk pasien (bahasa awam) |
| digital-twin-discharge-drafter, *-pediatric-dental-clinic-client-education-handout (2 salinan hampir identik dari pembuat berbeda) | ClawHub | – | 575–840 unduhan | Tidak diuji: yang satu untuk ringkasan pulang RS, yang lain berpola duplikat (tanda AI slop) |

---

## Output pesaing untuk skenario 01 (simulasi: penguji berperan sebagai agent yang memuat skill pesaing)

### P1. uae-clinic-arabic-comms
Skill ini tidak punya templat cabut gigi, jadi agent memakai "Post-Operative Instructions Template" dan menyesuaikannya ke permintaan (bahasa pengguna Indonesia; aturan "produce both Arabic and English" hanya berlaku untuk komunikasi berbahasa Arab):
```
Instruksi Setelah Tindakan — [Nama Pasien] — [Tanggal]
Klinik Gigi Senyum Sejahtera

1. Luka
• Gigit kapas/tampon 30 menit, jangan dilepas-lepas
• Jangan kumur 24 jam; jangan hisap-hisap bekas cabut
2. Obat
• Amoxicillin 500 mg 3x1 — habiskan 5 hari
• Asam mefenamat 500 mg bila nyeri, maks 3x sehari
• Jangan minum obat tambahan tanpa konsultasi dokter
3. Aktivitas
• Istirahat selama [X] hari
4. Makanan
• Makanan lembut & dingin 2 hari; hindari makanan berlemak & pedas selama seminggu
5. Kapan menghubungi kami — segera jika:
🚨 Darah tidak berhenti lebih dari 1 jam
🚨 Demam di atas 38,5°C
🚨 Kemerahan, bengkak, atau cairan dari luka
🚨 Nyeri hebat yang tidak reda dengan obat
Kontrol: [Tanggal] pukul [Jam]
Klinik Gigi Senyum Sejahtera — [Telepon]
Instruksi ini untuk edukasi — selalu ikuti dokter Anda.
```

### P2. patiently-ai
Skill ini mewajibkan bertanya dulu soal tingkat baca, nada, panjang, dan bahasa. Bahasa Indonesia **tidak ada** dalam daftar bahasanya. Dengan default (Adult / Informative / Standard) dan bahasa mengikuti pengguna, strukturnya: Summary → Section breakdown → Medical terms → Questions for your doctor → Reminder.
```
Ringkasan: Dokter gigi memberi petunjuk perawatan setelah cabut gigi, dua obat, dan jadwal kontrol.
Penjelasan per bagian: … (menjelaskan ulang poin kapas, kumur, makanan, obat) …
Istilah medis: Amoxicillin = antibiotik untuk infeksi bakteri; Asam mefenamat = obat antinyeri
golongan NSAID …
Pertanyaan untuk dokter Anda: Bolehkah saya menyikat gigi malam ini? Kapan saya boleh makan
normal? Apa yang harus dilakukan bila lupa minum antibiotik? …
Pengingat: Ini penjelasan sederhana; selalu diskusikan perawatan Anda dengan tenaga kesehatan.
```
Hasilnya bukan leaflet/pesan WA dari klinik. Ini penjelasan untuk pasien yang membaca dokumennya sendiri, dan tidak ada versi WA pendek.

### K. Skill kita (edukasi-pasien-klinik)
Lihat `01-leaflet-cabut-gigi.md`.

---

## Penilaian berdampingan (1–10)

| Kriteria | uae-clinic-arabic-comms | patiently-ai | **edukasi-pasien-klinik** |
|---|---|---|---|
| Kualitas & kesesuaian tugas (leaflet + WA klinik) | 6: templat rapi, tapi tidak ada tindakan gigi dan tidak ada versi WA pendek | 3: formatnya penjelasan dokumen, bukan materi kirim klinik | **9** |
| Kesetiaan pada instruksi dokter / keamanan medis | 3: templat **berisi instruksi bawaan** (demam >38,5 °C, hindari lemak/pedas seminggu, tanda infeksi) yang ikut masuk padahal tidak diberikan dokter | 6: aturan "jangan menambah" bagus, tapi bagian "Medical terms" menambah info obat (NSAID dll.), dan contoh bawaannya menilai hasil lab "normal/tidak normal" | **9**: hanya dari input; kalimat IGD/119 |
| Konteks Indonesia (bahasa, WA, BPJS, 119, regulasi) | 2 (UEA/Arab) | 2 (tidak ada Bahasa Indonesia) | **9** |
| Akurasi & penandaan data kurang | 6 (`[X]`, `[Tanggal]`) | 5 | **9** (`[isi …]` + catatan) |
| Siap pakai untuk admin awam | 5 | 3 | **9** |
| Cakupan lain (FAQ, pengingat, konten bersumber, rekap agregat) | Pengingat & konfirmasi janji saja | Tidak ada | Lengkap, termasuk script rekap yang menjaga privasi |

**Kesimpulan:** skill kita **unggul jelas** untuk tugas ini. Pesaing terdekat (uae-clinic-arabic-comms) justru memperlihatkan risiko yang dicegah skill kita: templat berisi instruksi medis bawaan yang ikut terkirim ke pasien.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Instruksi pra-tindakan** (persiapan sebelum tindakan: puasa, pakaian, pendamping) sebagai jenis materi tambahan. Isinya tetap wajib dari dokter.
2. **Pertimbangan budaya/kalender:** pesaing UEA menyebut penyesuaian saat puasa Ramadan. Versi Indonesia bisa menambah catatan agar pengingat/aturan minum obat saat Ramadan **ditanyakan ke dokter**, bukan diubah sendiri oleh skill.
3. **Opsi tingkat baca/pembaca** (patiently-ai): versi "untuk orang tua/pendamping" atau "untuk lansia" (huruf besar, kalimat lebih pendek). Ini opsi format, bukan isi medis.
4. **Versi bilingual** (ID + EN, atau ID + bahasa daerah bila klinik menyediakan terjemahan) untuk klinik di daerah wisata/ekspat.
