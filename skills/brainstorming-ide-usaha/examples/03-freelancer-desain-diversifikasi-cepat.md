# Uji 03 — Freelancer desain grafis cari ide diversifikasi, "cepat saja, jangan banyak tanya" (skenario normal, mode instan)

Penguji independen (Tahap 6), 2026-09-25. Jawaban pengguna disimulasikan.

## Permintaan awal

> "Saya freelancer desain grafis, klien kebanyakan UMKM, order naik turun. Mau nambah layanan/produk lain biar pemasukan stabil. Cepat saja ya, jangan banyak tanya."

## Pesan agent #1 (satu pesan, tanpa tanya-jawab)

"Ini **diversifikasi ke lini baru → Jalur C (Perlu Rencana)**. Karena Anda minta cepat, saya **tidak** menggali satu per satu; saya pakai asumsi wajar (daftar di akhir) — koreksi saja kalau meleset.

**Ide (teknik: SCAMPER-P 'alihkan keahlian' + Gabung-Kombinasi 'produk + segmen baru'):** 6 ide realistis, lalu disaring dengan skor tertimbang memakai kriteria & bobot contoh dari `templates/format-data-skor.md` (modal 5, permintaan 4, kemudahan 3, keahlian 2, margin 4 — karena Anda tidak sempat menentukan bobot sendiri)."

Perintah:
```
python3 scripts/skor_ide.py skor --ide ide03.csv --bobot bobot03.json
```
Keluaran asli script:
```
Peringkat Nama Ide                                           Skor Tertimbang
----------------------------------------------------------------------------
1         Paket branding UMKM (logo+kemasan+feed)                      4.389
2         Jasa desain konten bulanan (langganan)                       4.000
3         Template Canva siap jual (produk digital)                    3.778
4         Kelas online desain untuk UMKM                               3.611
5         Jasa desain kemasan + cetak (makelar percetakan)             3.333
6         Jasa foto produk                                             2.667

Bobot kriteria dipakai (total bobot = 18):
   - kesesuaian_modal: 5
   - potensi_permintaan: 4
   - kemudahan_eksekusi: 3
   - kecocokan_keahlian: 2
   - potensi_margin: 4
```
Verifikasi independen (Python terpisah): 79/18 = 4,3889; 72/18 = 4,0000; 68/18 = 3,7778; 65/18 = 3,6111; 60/18 = 3,3333; 48/18 = 2,6667 — **cocok**.

| Ide | Kenapa unggul/kalah | Risiko |
|---|---|---|
| **1. Paket branding UMKM** (4,39) | Memaketkan pekerjaan yang sudah Anda kuasai jadi harga tetap → nilai order lebih besar | Revisi bisa melebar — batasi jumlah revisi di paket |
| **2. Desain konten bulanan (langganan)** (4,00) | Paling menjawab "pemasukan stabil": tagihan rutin tiap bulan | Waktu tersita tiap bulan; harga harus menutup jam kerja |
| **3. Template Canva siap jual** (3,78) | Dibuat sekali, dijual berulang | Permintaan belum pasti; harga pasar template murah |
| (6. Foto produk — skor terendah: butuh kamera/lampu & keahlian baru, bertentangan dengan asumsi modal kecil) | | |

**Rekomendasi:** karena tujuan Anda *stabil*, bukan sekadar *besar*, saya sarankan **#2 langganan** walau skornya #2 — skor hanya alat bantu. #1 bisa jadi pintu masuk (klien paket branding ditawari langganan).

**Pilih satu: ketik 1, 2, atau 3** — atau "lanjut" untuk rekomendasi saya (#2). Rencana uji & aksi 7 hari saya susun setelah Anda pilih.

*Asumsi yang dipakai:* modal di bawah Rp5 juta; dikerjakan sendiri, paruh waktu di sela order; online; berhasil = 10 calon klien serius/pemesan uji dalam 1 minggu tanpa rugi; bobot kriteria = contoh template."

## Pengguna

> "lanjut"

## Pesan agent #2 (output akhir)

**Ide terpilih:** Jasa desain konten bulanan untuk UMKM.

**Titik impas kasar** (modal awal Rp1.200.000 untuk contoh portofolio, iklan kecil & langganan aset desain 1 bulan; margin per klien-bulan diasumsikan Rp45.000 setelah dikurangi biaya aset & waktu tambahan — silakan ganti angkanya):
```
python3 scripts/skor_ide.py impas --modal 1200000 --margin 45000
Titik impas (BEP)  : 27 unit
```
Verifikasi: 1.200.000 ÷ 45.000 = 26,67 → dibulatkan ke atas **27** klien-bulan. Artinya dengan 5 klien langganan, modal kembali di bulan ke-6. (Perkiraan kasar; belum termasuk pajak & biaya bulanan lain.)

**Uji murah (MVP):** tawarkan "Paket Konten Bulanan – 12 desain/bulan" ke 20 klien lama lewat chat personal + 1 postingan portofolio. Durasi 7 hari. Target: ≥3 klien setuju uji 1 bulan (untuk jasa B2B, target default 10 pesanan terlalu tinggi — disesuaikan sesuai `templates/kerangka-uji-murah.md` bagian 3). Lanjut jika ≥3; perbaiki harga/isi paket jika 1–2; ganti ke ide #1 jika 0 dari 20.

**Rencana Aksi 7 Hari**

| Hari | Tugas |
|---|---|
| 1 | Tulis isi paket (jumlah desain, revisi, jadwal kirim) + 2 pilihan harga |
| 2 | Buat 1 contoh "kalender konten 12 desain" dari klien lama (izin dulu) sebagai portofolio |
| 3 | Kirim tawaran personal ke 10 klien lama pertama |
| 4 | Kirim ke 10 klien lama berikutnya + posting portofolio |
| 5 | Follow-up yang membaca tapi belum membalas |
| 6 | Catat jawaban: setuju / tertarik tapi mahal / tidak |
| 7 | Evaluasi vs target 3 klien → lanjut, perbaiki, atau ganti ke paket branding |

**Asumsi:** seperti di pesan #1; margin Rp45.000/klien-bulan adalah asumsi agent, belum dihitung dari tarif Anda.

## Catatan penguji
- Prinsip instan dijalankan: 0 pertanyaan di awal, asumsi disebut, gerbang persetujuan tetap ada tetapi dipadatkan jadi satu kata ("lanjut"). SKILL.md **tidak menjelaskan** bagaimana gerbang wajib Jalur C berinteraksi dengan mode "jangan banyak tanya" — agent harus menafsirkan sendiri.
- SKILL.md bilang "kriteria & bobot wajib disepakati atau memakai default yang disebutkan", tetapi **tidak ada bobot default resmi** di SKILL.md; agent memakai bobot contoh dari template. Sebaiknya tetapkan bobot default eksplisit (mis. semua 1 atau contoh template) di SKILL.md.
- Istilah "unit" di keluaran `impas` kurang pas untuk jasa langganan (klien-bulan); pengguna awam bisa bingung.
