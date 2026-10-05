---
name: spesifikasi-produk-usaha
description: Menyusun spesifikasi produk ringan (PRD versi UMKM) siap pakai untuk produk fisik (makanan/minuman, fashion, kosmetik, kerajinan) maupun produk digital/jasa sederhana - masalah, target pembeli, atribut/resep/bahan, kemasan, HPP target, standar mutu, pengingat izin PIRT/BPOM/halal - plus roadmap Sekarang/Berikutnya/Nanti, skor prioritas RICE/ICE dihitung script, versi resep/spesifikasi, dan brief ke supplier/maklon/desainer. Gunakan saat pengguna bilang "bikin spesifikasi produk", "PRD", "brief maklon", "urutan produk mana dulu", "roadmap produk", "resep versi 2", "product spec", "product roadmap", "prioritize features".
---

# Spesifikasi Produk Usaha (ringan)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah ide produk yang masih di kepala menjadi **satu dokumen spesifikasi 1-3 halaman** yang bisa langsung diberikan ke maklon, supplier, penjahit, desainer, atau tim - lengkap dengan prioritas (mana dikerjakan dulu, dihitung), urutan rilis, dan catatan versi supaya perubahan resep/spesifikasi tidak hilang jejak.

## Kapan digunakan
- "Aku mau bikin minuman kemasan botol 250 ml, bantu susun spesifikasinya."
- "Tolong buatkan brief untuk maklon skincare / konveksi / desainer kemasan."
- "Ada 6 ide varian baru, mana yang dikerjakan dulu?"
- "Resep sudah revisi 3 kali, catat perubahannya."
- Produk digital/jasa sederhana: fitur aplikasi/website, paket layanan.

## Kapan TIDAK digunakan
- Menghitung modal dan harga jual -> skill `hitung-hpp` (di sini hanya menetapkan **target** HPP lalu merujuk ke sana). Harga tayang setelah potongan marketplace -> `harga-jual-marketplace`.
- Menguji apakah ide layak dijual -> `validasi-ide-produk-baru`.
- Naskah listing/foto -> `listing-marketplace`, `foto-produk-brief`.
- Nasihat hukum, uji laboratorium, atau memastikan izin sah: skill ini hanya **pengingat**, bukan jaminan (lihat Batasan).

## Input
| Info | Wajib? | Bila kosong |
|---|---|---|
| Jenis produk + gambaran singkat | Ya | tanyakan |
| Pembeli yang dituju & masalah yang diselesaikan | Ya | usulkan 1 dugaan, tandai **[ASUMSI]** |
| Bahan/resep/ukuran/fitur yang sudah terpikir | Tidak | tulis "[belum ditentukan]" |
| Target harga jual & margin | Tidak | tulis "[isi setelah `hitung-hpp`]" |
| Daftar ide/fitur untuk diurutkan | Hanya untuk prioritas | - |
| Siapa pembaca dokumen (maklon, penjahit, developer, diri sendiri) | Tidak | anggap diri sendiri + calon produsen |

Kalau info kurang: tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan singkat. Bila pengguna ingin cepat, pakai default masuk akal dan **sebutkan asumsinya di bagian atas dokumen**.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Tentukan jenis** dokumen yang diminta: (A) spesifikasi lengkap, (B) prioritas + roadmap, (C) brief ke pihak lain, (D) catatan versi. Kalau tidak jelas, kerjakan A lalu tawarkan B/C.
2. **Pilih templat** dari `templates/spesifikasi-produk.md` sesuai jenis usaha: F&B/minuman, fashion, kosmetik/perawatan, kerajinan, atau digital/jasa. Buang bagian yang tidak relevan; jangan mengisi bagian yang tidak diketahui dengan karangan.
3. **Isi bagian inti** (lihat Format Output), termasuk **Ukuran keberhasilan**: 1-3 target terukur dengan batas waktu (jumlah terjual, pembeli ulang, skor uji rasa/pakai, komplain). Kalau pengguna belum punya angka, usulkan dan tandai **[ASUMSI]**. Tulis dalam bahasa sehari-hari; tiap persyaratan harus bisa **dicek** ("botol 250 ml, isi bersih 240-250 ml", bukan "botol bagus").
4. **HPP target:** hitung mundur dari harga jual yang diinginkan. Rumus sederhana: `HPP maksimal = harga jual x (1 - margin kotor target)` dan **jangan dihitung di kepala**; angka pasti ada di `hitung-hpp` (kalau skill itu terpasang, panggil; kalau tidak, tulis rumus + hitung teliti dan tandai "perkiraan"). Jangan mengarang harga bahan.
5. **Perizinan:** bagian "Pengingat izin & legalitas" wajib ada untuk produk fisik. Isi dari `references/perizinan-produk.md`: tentukan dulu **jalur** (PIRT hanya untuk pangan suhu ruang risiko rendah; produk **dingin/beku, kemasan kedap, SNI wajib, berklaim kesehatan, pangan bayi -> BPOM MD**; jamu/herbal -> BPOM TR; kosmetik -> notifikasi; pakaian bayi & mainan anak -> **SNI wajib**), lalu tulis tenggat halal yang berlaku (makanan-minuman UMK dan kosmetik/sandang: Oktober 2026), dasar aturan, tautan resmi, dan tanggal cek. Bila spesifikasi (mis. "simpan dingin") mengubah jalur izin, katakan terang-terangan.
6. **Prioritas** (bila ada >1 ide/fitur): kumpulkan skor dari pengguna, simpan sebagai CSV, jalankan `python3 scripts/prioritas.py --metode rice --csv ide.csv` (Windows: `python` atau `py`). Pakai **ICE** bila pengguna tidak punya angka jangkauan/usaha (skala 1-10 semua). Jangan menghitung skor sendiri; kalau script tidak bisa jalan, hitung dengan rumus di `references/prioritas.md` dan tulis langkahnya.
7. **Roadmap Sekarang / Berikutnya / Nanti:** ambil dari kolom Tahap keluaran script (aturan pembagian: `references/prioritas.md`; bila ada "Catatan" ide lebih besar dari kapasitas, sarankan memecahnya), lalu tuliskan tiap butir sebagai hasil untuk pembeli ("Pembeli bisa mencoba 3 rasa dengan ukuran mini"), bukan sekadar daftar pekerjaan. Tanpa tanggal pasti; pakai kapan-kira-kira bila diminta.
8. **Versi:** beri nomor versi (mis. `Resep v0.3`, `Spesifikasi v1.0`) dan isi tabel "Catatan perubahan" (tanggal, apa yang berubah, alasan, hasil uji rasa/pakai). Perubahan bahan/kemasan/ukuran **selalu** memicu tanya: HPP berubah? label/izin perlu diperbarui?
9. **Brief ke pihak lain:** dari spesifikasi, buat versi ringkas yang hanya memuat yang dibutuhkan pihak itu (`templates/brief-pihak-ketiga.md`): tujuan, spesifikasi teknis, jumlah pesanan awal (MOQ) yang ditanyakan, sampel, tenggat, kriteria terima, pertanyaan yang harus mereka jawab. Jangan mencantumkan HPP/margin internal ke pihak luar.
10. **Produk digital/jasa:** ganti bagian bahan/kemasan dengan "Fitur & alur pengguna" (cerita pengguna singkat: "Sebagai [siapa], saya ingin [apa], supaya [hasil]") dan "Kriteria selesai" per fitur. Untuk perangkat lunak, tambah: data yang disimpan (dan persetujuan pengguna bila data pribadi), hal yang di luar cakupan, cara uji.
11. **Cek akhir sebelum diberikan:** (a) tidak ada angka karangan, (b) semua **[ASUMSI]** terdaftar, (c) ada bagian "Di luar cakupan versi ini", (d) tabel perubahan terisi, (e) disclaimer izin ada, (f) ukuran keberhasilan terukur ada, (g) jalur izin cocok dengan cara simpan/kemasan/klaim produk (mis. produk dingin tidak diarahkan ke PIRT).

## Format output
Selalu dalam urutan ini (buang yang tidak relevan, jangan ubah urutan):

```
# Spesifikasi Produk: <nama> - v<versi> - <tanggal>
Asumsi: ...
1. Ringkasan (2-3 kalimat)
2. Masalah & pembeli sasaran (siapa, situasi, alasan beli) + Ukuran keberhasilan (1-3 target terukur)
3. Produk: atribut / resep-bahan / ukuran-varian / fitur
4. Kemasan & label (bahan, ukuran, informasi wajib di label)
5. HPP & harga target (rumus, angka dari hitung-hpp)
6. Standar mutu & cara uji terima (rasa, tampilan, daya simpan, toleransi)
7. Pengingat izin & legalitas (PIRT/BPOM/halal/merek; tautan resmi)
8. Prioritas & roadmap (tabel skor + Sekarang/Berikutnya/Nanti)
9. Risiko & hal yang belum diketahui
10. Di luar cakupan versi ini
11. Catatan perubahan (tabel)
```
Untuk prioritas: tampilkan tabel keluaran script apa adanya (termasuk baris PERINGATAN/Catatan), lalu 2-3 kalimat penjelasan awam ("skor tinggi = banyak pembeli tersentuh, dampak besar, kecil usaha"). Untuk brief: satu halaman, siap kirim lewat WhatsApp/email.

## Contoh
**Masukan:** "Mau bikin teh serai jahe botol 250 ml, jual Rp15.000, target margin 50%. Ide lain: varian tanpa gula, paket 6 botol, langganan mingguan."

**Ringkasan hasil:** spesifikasi lengkap (resep v0.1 dengan bahan [belum ditentukan] bila belum ada resep, HPP maksimal Rp7.500 dihitung dari 15.000 x (1 - 0,5), kemasan botol PET 250 ml + label, pengingat izin: karena disimpan dingin -> **BPOM MD, bukan PIRT**, tenggat halal 17-10-2026, merek, label), tabel skor RICE untuk 3 ide, roadmap, dan catatan versi. Contoh lengkap: `examples/01-minuman-teh-serai-spesifikasi.md`.

## Batasan & penanganan error
- **Bukan nasihat hukum/perizinan/keamanan pangan.** Persyaratan izin (PIRT, BPOM, halal, merek, label) hanyalah pengingat berdasar pengetahuan umum; aturan, tarif, dan kategori produk bisa berubah. Arahkan pengguna memeriksa tautan resmi dan bertanya ke Dinas Kesehatan setempat/pendamping halal/konsultan. Cantumkan "dicek terakhir: <tanggal>"; bila tidak yakin, tulis "belum diverifikasi".
- **Tanpa anjuran takaran konsumsi/dosis.** Untuk minuman/pangan fungsional, jangan menulis anjuran "berapa botol/hari", "diminum 2x sehari", atau takaran sejenis, kecuali pengguna sendiri yang menyebutnya dan wajar/aman; bila ada, tandai sebagai kutipan dari pengguna dan arahkan cek ke BPOM/ahli gizi.
- **Daya simpan tanpa dasar:** jangan mengusulkan umur/daya simpan (mis. "tahan 6 bulan"); tulis "[perlu uji umur simpan]" sampai ada hasil uji.
- **Ringkasan chat untuk awam:** istilah teknis (RICE, ICE, PIRT, BPOM MD, MOQ) wajib diberi penjelasan singkat bahasa sehari-hari saat pertama muncul, mis. "RICE (skor untuk mengurutkan ide)", "PIRT (izin usaha pangan rumahan dari Dinas Kesehatan)".
- **Tanpa klaim kesehatan/medis.** Untuk minuman, suplemen, kosmetik: jangan menulis klaim khasiat ("menyembuhkan", "menurunkan gula darah") atau menyarankan dosis; ingatkan bahwa klaim diatur BPOM. Tanpa diagnosis.
- **Jangan mengarang** harga bahan, hasil uji laboratorium, nomor izin, atau kapasitas maklon. Tulis "[belum ditentukan]" atau minta pengguna mengisi.
- **Data prioritas buruk** (usaha 0, persen di luar 0-100, keyakinan ditulis pecahan 0,8, angka ambigu `10,000`, angka huruf, judul kolom salah, file kosong): script menolak baris/file itu dan menyebut alasannya, baris lain tetap dihitung. Sampaikan baris yang tidak dihitung ke pengguna dan minta perbaikannya. Jangan menebak angka pengganti.
- **Skor hanya alat bantu urutan**, bukan kebenaran. Nilai "keyakinan" dari tebakan harus diberi nilai rendah; sarankan uji kecil (pre-order, sampel) untuk ide skor tinggi tapi keyakinan rendah.
- **Di luar cakupan** (mis. minta hitung pajak, tulis kontrak, resep obat): jelaskan singkat dan arahkan ke skill lain atau profesional.
- Skill ini tidak butuh internet, akun, atau API key. Script hanya memakai Python standar.
