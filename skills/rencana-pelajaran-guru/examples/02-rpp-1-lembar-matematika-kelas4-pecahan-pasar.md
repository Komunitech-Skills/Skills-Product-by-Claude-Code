# Skenario 02 — Normal — "RPP 1 lembar Matematika kelas 4 SD tentang pecahan, dengan konteks pasar"

## Input pengguna
> "RPP 1 lembar Matematika kelas 4 SD tentang pecahan, dengan konteks pasar"

## Langkah yang diikuti
1. Jenjang: SD kelas 4 → Fase B (kelas 3–4), 35 menit/JP.
2. Jumlah pertemuan & JP tidak disebut → default **1 pertemuan × 2 JP = 70 menit**.
3. Jenis dokumen **disebutkan eksplisit**: "RPP 1 lembar" → keluarkan **RPP 1 lembar saja**
   (`templates/kerangka-rpp-1-lembar.md`), tanpa Modul Ajar lengkap/LKPD/soal terpisah,
   sesuai aturan Format Output ("bila guru minta hanya salah satu dokumen, keluarkan
   dokumen itu saja").
4. Baca `references/panduan-mapel.md` §Matematika → konteks harga di pasar/warung, soal
   cerita dihitung ulang, alat bantu sederhana (bukan alat peraga digital berbayar).
5. CP tidak ditempel guru → ringkasan umum + tanda "(cek CP resmi)".
6. Verifikasi waktu:
   ```
   python3 scripts/hitung_alokasi_waktu.py --jenjang sd --jp 2 --pertemuan "10,50,10"
   ```
   Hasil: **COCOK** (70 menit = 70 menit target).

## Log script (bukti)
```json
{
  "jenjang": "sd", "menit_per_jp": 35, "jp_per_pertemuan": 2,
  "target_menit_per_pertemuan": 70, "jumlah_pertemuan": 1,
  "total_menit_seluruh_pertemuan": 70, "target_menit_seluruh_pertemuan": 70,
  "semua_pertemuan_cocok": true,
  "rincian": [{"pertemuan": 1, "pembukaan_menit": 10, "inti_menit": 50, "penutup_menit": 10, "total_menit": 70, "status": "COCOK"}]
}
```

## Output

```
RPP (1 Lembar) — Matematika

Sekolah: [nama sekolah]           Mapel/Kelas/Fase: Matematika / IV / B
Topik: Pecahan (penjumlahan pecahan sederhana penyebut sama & beda, konteks jual-beli)
Alokasi waktu: 2 JP (70 menit) — asumsi 1 pertemuan × 2 JP karena tidak disebutkan guru.

Tujuan Pembelajaran
1. Membandingkan nilai dua pecahan sederhana dari berat/jumlah barang di pasar
   (mis. 1/2 kg gula vs 1/4 kg gula).
2. Menghitung penjumlahan dua pecahan berpenyebut sama dan beda dari daftar belanja
   sederhana.

Langkah Kegiatan
- Pembukaan (10’): guru menunjukkan gambar/kartu harga barang pasar (gula, tepung,
  minyak per 1/4 kg, 1/2 kg, 3/4 kg) + pertanyaan pemantik: "Kalau Bu Ani beli 1/2 kg
  gula dan 1/4 kg gula lagi, berapa total gulanya?" Diagnostik lisan: cek siswa sudah
  kenal lambang pecahan sederhana.
- Inti (50’): (15’) Guru jelaskan pecahan sebagai bagian dari satu kesatuan dgn contoh
  memotong "roti pasar"/kertas menjadi 1/2, 1/4. (20’) Kerja berpasangan: siswa
  mengerjakan LKPD daftar belanja pasar (menjumlahkan pecahan berat belanjaan,
  mis. 3/4 kg + 1/2 kg = 1 1/4 kg — dihitung ulang & diverifikasi guru, lihat kunci di
  Lampiran soal terpisah bila diminta). (15’) Bahas bersama 2 soal tersulit di papan tulis.
- Penutup (10’): formatif — guru amati LKPD; simpulan bersama; refleksi 1 pertanyaan
  ("bagian mana yang masih bingung tentang pecahan hari ini?").

Asesmen
- Diagnostik: tanya jawab lisan pengenalan lambang pecahan (awal).
- Formatif: pengamatan LKPD berpasangan selama kegiatan inti.
- Sumatif (bila diperlukan terpisah): tidak diminta guru pada permintaan ini — RPP 1
  lembar ini fokus komponen inti; bila guru ingin soal+kunci+rubrik terpisah, minta
  sebagai permintaan lanjutan ("sekalian buatkan soal & kuncinya juga").

Asumsi yang dipakai: 1 pertemuan × 2 JP (70 menit) karena JP tidak disebutkan guru.
Cek sebelum dipakai: CP di atas ringkasan umum — cocokkan dengan dokumen CP resmi
Matematika Fase B (kelas 3–4) dari sekolah/dinasmu.
Cara pindah ke Word/Google Docs: ...

Mau saya (1) buatkan juga LKPD + soal & kunci untuk topik ini, (2) naikkan ke pecahan
berpenyebut beda yang lebih menantang, atau (3) buatkan versi untuk kelas dengan siswa
yang masih kesulitan mengenal angka?
```

## Verifikasi angka independen (dihitung ulang manual, bukan memakai kode skill)
| Soal contoh dalam RPP | Hitungan manual |
|---|---|
| 1/2 kg + 1/4 kg | = 2/4 + 1/4 = **3/4 kg** ✓ (RPP menyebutnya sebagai perbandingan, bukan penjumlahan — konsisten) |
| 3/4 kg + 1/2 kg | = 3/4 + 2/4 = 5/4 = **1 1/4 kg** ✓ cocok dengan yang ditulis di Langkah Inti |
| Menit: 10+50+10 | = 70 = 2×35 ✓ |

Tidak ditemukan angka yang salah atau ditulis kira-kira.

## Penilaian
**Lulus.** Skill benar memilih HANYA RPP 1 lembar (bukan paket penuh) karena jenis
dokumen disebut eksplisit — sesuai aturan "Format Output". Konteks pasar konkret dan
relevan usia SD (barang sehari-hari, bukan abstrak). CP jujur ditandai "cek CP resmi".
Waktu 100% cocok dan diverifikasi. Tidak ada cacat pada skenario ini.
