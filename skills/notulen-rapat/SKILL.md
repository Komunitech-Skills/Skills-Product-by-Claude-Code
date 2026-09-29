---
name: notulen-rapat
description: Mengubah catatan rapat kasar, transkrip Zoom/Google Meet, atau ringkasan voice note menjadi notulen rapat yang rapi, berisi info rapat, peserta, agenda, poin diskusi, keputusan, tabel action item (siapa, apa, tenggat), dan pesan ringkas siap kirim ke grup WhatsApp, tanpa mengarang keputusan dan dengan menandai bagian yang ambigu. Gunakan saat pengguna minta buat notulen, notula, risalah rapat, rangkuman meeting, atau meeting minutes, meeting notes, action items.
---

# Notulen Rapat

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Dalam satu langkah, catatan rapat yang berantakan menjadi notulen yang jelas: apa yang diputuskan, siapa mengerjakan apa, kapan tenggatnya. Hasilnya juga dilengkapi pesan singkat yang langsung bisa dikirim ke grup WA tim. Prinsip utama: **setia pada catatan**. Isi yang tidak ada di catatan tidak ditambahkan, dan isi yang tidak jelas diberi tanda.

## Kapan digunakan
- Pengguna menempel catatan rapat, transkrip (Zoom, Google Meet, Teams, rekaman HP), atau ringkasan voice note dan minta dirapikan.
- Pengguna minta "rangkum meeting tadi", "buat notulen", "bikin daftar tugas dari rapat".
- Pengguna minta versi ringkas rapat untuk dikirim ke grup WA/Telegram/email.

## Kapan TIDAK digunakan
- Membuat undangan rapat → `surat-resmi`.
- Membuat SOP dari hasil rapat → `sop-writer` (boleh ditawarkan sesudah notulen selesai).
- Mentranskrip file audio/video: skill ini tidak mentranskrip. Minta pengguna menempel teks transkrip dari aplikasi rapat/perekam, atau ringkasan voice note.
- Rapat Umum Pemegang Saham atau rapat yang butuh akta notaris: boleh bantu draf, tapi ingatkan bahwa format resminya mengikuti notaris/anggaran dasar.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Catatan/transkrip/ringkasan rapat | Ya | — (minta ditempel) |
| Nama rapat / topik | Tidak | Disimpulkan dari isi, diberi tanda `(disimpulkan)` |
| Tanggal, jam, tempat/platform | Tidak | `[isi tanggal]`, `[isi tempat]` |
| Daftar peserta | Tidak | Diambil dari nama yang muncul di catatan; tandai "(dari catatan, mohon dicek)" |
| Pemimpin rapat & notulis | Tidak | `[isi]` |
| Tanggal hari ini (untuk tenggat relatif) | Tidak | Tanggal percakapan; "Jumat depan" dikonversi ke tanggal + ditandai |
| Gaya | Tidak | Formal-ringkas untuk notulen; santai-sopan untuk pesan WA |

Jika catatan tidak ada, minta ditempel. Info lain **tidak perlu ditanyakan dulu**. Buat notulennya, lalu kumpulkan semua yang kurang di bagian "Perlu dikonfirmasi".

## Langkah kerja
1. **Baca seluruh catatan** dan bersihkan hal yang tidak relevan: sapaan, basa-basi, "halo kedengeran?", filler "eee", dan obrolan di luar topik.
2. **Identifikasi agenda.** Jika catatan tidak menyebut agenda, kelompokkan pembahasan per topik dan tandai `(dikelompokkan dari isi)`.
3. **Klasifikasikan setiap pernyataan** ke salah satu kategori (aturan rinci di `references/aturan-klasifikasi.md`):
   - **Keputusan**: ada kata/konteks final ("sepakat", "fix", "diputuskan", "oke kita jalan", persetujuan pimpinan rapat).
   - **Action item**: ada tugas + pelaksana (dan tenggat bila ada).
   - **Poin diskusi**: usulan, pendapat, data, pertimbangan yang belum final.
   - **Belum diputuskan / ditunda**: dibahas tapi tidak ada kesimpulan.
4. **Jangan mengarang.** Usulan tidak boleh ditulis sebagai keputusan. Jika tidak jelas apakah sudah disepakati, masukkan ke Poin Diskusi dengan tanda `⚠️ belum jelas apakah disepakati`. Tugas tanpa pelaksana ditulis `PIC: ⚠️ belum ditentukan`. Tugas tanpa tenggat ditulis `⚠️ belum ada tenggat`.
5. **Konversi tanggal relatif** ("besok", "Jumat depan", "akhir bulan") ke tanggal nyata dengan script agar nama hari tidak salah. Path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/tanggal_relatif.py --rapat "<tanggal rapat>" --ekspresi "jumat depan" "akhir bulan" --format teks
   python3 <folder-skill-ini>/scripts/tanggal_relatif.py --cek "<tanggal>"   # cek nama hari tanggal di catatan
   ```
   Rapat hari **Minggu**: "minggu depan"/"<hari> depan" selalu `ambigu` (pekan depan bisa mulai besok atau pekan setelahnya). Script ini punya uji regresi: `python3 <folder-skill-ini>/scripts/uji_tanggal_relatif.py`.
   Tulis keduanya, mis. `Jumat, 2 Oktober 2026 ("Jumat depan")`. Hasil berstatus `ambigu`/`perkiraan` → masukkan ke "Perlu dikonfirmasi" beserta alternatifnya; `tidak_dikenali` (mis. "secepatnya", "ASAP") → tulis apa adanya + ⚠️. Jika tanggal rapat tidak diketahui, biarkan relatif dan tandai.
   **Fallback tanpa Python:** hitung dari kalender, tulis "(nama hari dicek manual)", dan anggap "<hari> depan" ambigu (hari terdekat vs minggu berikutnya).
6. **Angka & nama** disalin persis dari catatan. Jika ejaan nama berbeda-beda (Rina/Rinna), pakai yang paling sering muncul dan catat di "Perlu dikonfirmasi".
7. **Susun notulen** mengikuti format output: tabel action item diurutkan dari tenggat terdekat.
8. **Buat pesan WA** ≤ 120 kata: keputusan utama + daftar tugas dengan mention nama + tenggat. Pakai format WA (`*tebal*`, `_miring_`), tanpa tabel.
9. Periksa checklist, lalu tawarkan: versi PDF/Docs (salin ke Google Docs), versi email, atau pengingat tenggat.

## Format output
```
# NOTULEN RAPAT
**[Nama rapat]**

| | |
|---|---|
| Hari, tanggal | ... |
| Waktu | ... |
| Tempat/platform | ... |
| Pemimpin rapat | ... |
| Notulis | ... |
| Peserta | ... (n orang) |
| Tidak hadir | ... (jika disebut) |

## Agenda
1. ...

## Pembahasan
### 1. [Agenda 1]
- [poin diskusi, siapa menyampaikan bila jelas]
- ⚠️ ...

## Keputusan
1. ...

## Action Items
| No | Tugas | PIC | Tenggat | Status |
|---|---|---|---|---|
| 1 | ... | ... | ... | Belum mulai |

## Belum diputuskan / dibahas di rapat berikutnya
- ...

## Perlu dikonfirmasi
- ...

Rapat berikutnya: [jika disebut, atau "belum ditentukan"]

---
## Pesan untuk grup WhatsApp
*Ringkasan Rapat [nama] — [tanggal]*
...
```
Template kosong (untuk dicetak/diisi tangan) ada di `references/aturan-klasifikasi.md`.

## Contoh
**Input pengguna (ringkasan voice note, rapat Senin 21 Sep 2026):**
"rapat tim toko kue Dapur Mama Ayu. hadir aku (ayu), dimas (produksi), sari (admin), fajar (kurir). bahas pesanan hampers natal. dimas bilang kapasitas oven max 80 box/hari. sari usul PO dibuka 1 okt, udah deal. harga hampers kecil 150rb besar 275rb, oke. fajar minta tambahan kurir pas desember, belum tau rekrut atau pakai ojol. sari bikin poster PO jumat depan. dimas cek harga mentega ke supplier."

**Output (ringkas):**
```
## Keputusan
1. Pre-order hampers Natal dibuka Kamis, 1 Oktober 2026.
2. Harga hampers: kecil Rp 150.000, besar Rp 275.000.

## Action Items
| No | Tugas | PIC | Tenggat | Status |
|---|---|---|---|---|
| 1 | Membuat poster PO hampers | Sari | Jumat, 2 Oktober 2026 ("Jumat depan") | Belum mulai |
| 2 | Cek harga mentega ke supplier | Dimas | ⚠️ belum ada tenggat | Belum mulai |

## Belum diputuskan
- Tambahan kurir Desember: rekrut kurir atau pakai ojol (usulan Fajar).

## Perlu dikonfirmasi
- Kapasitas 80 box/hari: apakah jumlah PO akan dibatasi? Belum dibahas.
- "Jumat depan" diartikan 2 Oktober 2026 (rapat hari Senin, 21 September 2026). Jika yang dimaksud 25 September, mohon koreksi.

## Pesan untuk grup WhatsApp
*Ringkasan Rapat Hampers Natal — Senin, 21 Sep 2026*
✅ PO dibuka *Kamis, 1 Okt*
✅ Harga: kecil *Rp 150.000*, besar *Rp 275.000*
📌 Tugas:
• @Sari: poster PO, paling lambat *Jumat, 2 Okt*
• @Dimas: cek harga mentega ke supplier (tenggat menyusul)
❓ Soal tambahan kurir Desember dibahas lagi di rapat berikutnya.
```

## Checklist sebelum mengirim hasil
- [ ] Setiap keputusan punya dasar kalimat di catatan (kata sepakat/deal/oke/diputuskan atau persetujuan pimpinan).
- [ ] Tidak ada nama, angka, tanggal, atau tugas yang tidak ada di catatan.
- [ ] Setiap action item punya PIC dan tenggat, atau diberi tanda ⚠️.
- [ ] Tanggal relatif sudah dikonversi dan ditandai; nama hari sesuai tanggal.
- [ ] Bagian "Perlu dikonfirmasi" berisi semua ambiguitas.
- [ ] Pesan WA ≤ 120 kata, tanpa tabel, memuat keputusan dan tugas; hanya hal yang pasti (tanggal ambigu ditulis dua pilihan atau diberi tanda tanya).
- [ ] Rupiah ditulis `Rp 150.000`.

## Batasan & penanganan error
- Transkrip otomatis sering salah dengar. Jika ada kata/angka yang janggal (mis. "harga 15 ribu" untuk hampers), jangan dikoreksi diam-diam. Tulis apa adanya dan tambahkan ke "Perlu dikonfirmasi".
- Catatan sangat pendek (< 3 poin): tetap buat notulen ringkas dan beri tahu bahwa sebagian bagian kosong.
- Catatan sangat panjang (> 1 jam rapat): ringkas poin diskusi per agenda (maks 5 butir per agenda), tapi **semua** keputusan dan action item tetap dicantumkan.
- Informasi sensitif (gaji individu, masalah pribadi, penilaian kinerja seseorang): masukkan ke notulen lengkap bila ada di catatan, tetapi **jangan** dimasukkan ke pesan grup WA. Beri catatan kepada pengguna.
- Rapat berbahasa campuran (Jawa/Sunda/Inggris): notulen ditulis dalam bahasa Indonesia baku, istilah teknis boleh tetap dalam bahasa aslinya.
- Jangan mengirim notulen ke mana pun. Skill hanya menyiapkan teks.
