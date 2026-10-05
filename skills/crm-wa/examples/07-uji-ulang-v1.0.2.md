# Uji ulang v1.0.2 (Akun B, penguji independen)

**Penguji:** agent penguji independen (bukan pembuat/perevisi crm-wa). Simulasi Claude Code.
Dijalankan dari `/tmp/.../scratchpad/uji-crm/` (salinan skill), dengan `HOME` dan `KOMUNITECH_DATA`
palsu terpisah dari repo. Semua nama/nomor kontak fiktif.

## 1. Otomatis
- `python3 tests/uji_regresi.py` → **57 tes OK** (0 gagal).
- `python3 scripts/validate.py --skill crm-wa` (dari root repo) → **1 skill valid, 68 baris katalog sesuai.**

## 2. Uji ulang temuan (kasus baru, di luar test milik pembuat)

### N1 — draf pesan, titik/koma desimal & nominal kata
| Input `--kebutuhan` | Draf dihasilkan | Catatan |
|---|---|---|
| `kue tart Rp1.250.000 buat kantor` | "kue tart buat kantor" | benar, titik ribuan bertingkat terbuang |
| `daging rendang 2,5 kg buat hajatan` | "daging rendang 2,5 kg buat hajatan" | benar — "2,5 kg" **bukan** uang, sengaja tidak dibuang |
| `nasi kotak 1.500.000, tapi budgetnya ketat banget` | "nasi kotak" | benar, koma-komentar + nominal terbuang |
| `renovasi dapur 12,75 juta selesai bulan depan` | "renovasi dapur selesai bulan depan" | benar, koma desimal 2 digit tidak lagi memutus kalimat |
| `hampers 2.5jt buat lebaran, minta diskon dong` | "hampers buat lebaran" | benar |

Semua kasus baru (termasuk yang sengaja bukan nominal uang, "2,5 kg") ditangani benar. Tidak ditemukan regresi
atau kasus baru yang gagal.

### N2 — CSV kutip tak tertutup
- Kutip terbuka di **baris data pertama**, tak pernah ditutup sampai akhir file: seluruh sisa file (baris 2-4)
  menyatu jadi 1 baris logis. Peringatan jelas muncul: *"1 baris di file dibaca menyatu dengan baris sesudahnya
  (2-4): kemungkinan ada tanda kutip (") yang tidak tertutup..."* — tidak ada baris hilang diam-diam.
- Kutip terbuka di **baris ke-3** (tengah file), menelan 2 baris berikutnya ("Deni", "Eka"): peringatan
  menyebut rentang baris yang benar (3-5), jumlah "Baris bermasalah dilewati: 1" konsisten dengan rentang.
- Kedua kasus baru (variasi posisi kutip) lolos — peringatan selalu tampil di pratinjau, sebelum `--ya`.

### N3 — impor tanpa `tgl masuk`
- File tanpa kolom `tgl masuk` sama sekali (2 kontak): peringatan *"2 kontak tanpa kolom/tanggal masuk..."*
  muncul di pratinjau, sebelum simpan.
- File dengan kolom `tgl masuk` tapi **sebagian** kosong (1 dari 2 baris kosong): peringatan menghitung
  tepat **1** (bukan 2), sesuai baris yang benar-benar kosong — verifikasi independen: benar.
- Tidak ditemukan kasus di mana kolom disebut ada tapi peringatan salah hitung.

### K2 — pesan "jadwal prospek lama diganti" pada kontak baru
- Kontak **baru** dibuat langsung di tahap `deal` (dua variasi: dengan & tanpa `--nilai`): pesan follow-up
  **tidak** menyebut "jadwal prospek lama diganti" — benar.
- Kontak **lama** (dibuat di tahap `baru`, lalu `catat --tahap deal`): pesan follow-up **tetap** menyebut
  "; jadwal prospek lama diganti" — benar, tidak ada regresi pada jalur pindah tahap.

## 3. Tanpa regresi — verifikasi angka independen
Kontak yang benar-benar tersimpan (`--ya`) selama sesi ini: 5 kontak tahap "baru" (N1a/N1c/N1d/N1b/N1e) dan
3 kontak tahap "deal" (K2a, K2b, K2c; nilai diisi hanya pada K2c = Rp 5.000.000). File CSV N2/N3 hanya
dijalankan tanpa `--ya` (pratinjau), sehingga tidak menambah data.

Dihitung manual dari daftar kontak yang dibuat vs `rekap --json`:
- `posisi.baru.jumlah` = **5** — cocok.
- `posisi.deal.jumlah` = **3**, `posisi.deal.nilai` = **5.000.000** — cocok (hanya K2c berisi nilai).

Tidak ada selisih. `tests/uji_regresi.py` (57 tes, termasuk 4 tes baru N1/N2/N3/K2 milik pembuat) tetap OK
di lingkungan penguji terpisah ini.

## 4. Skor kualitas: **9 / 10 — LULUS**
Alasan:
- (+) Keempat temuan rendah/kosmetik dari uji ulang v1.0.1 (N1, N2, N3, K2-sebagian) diverifikasi tuntas
  dengan kasus buatan sendiri di luar test milik pembuat, termasuk variasi bentuk uang (titik ribuan
  bertingkat, koma desimal 2 digit, "2.5jt") dan posisi kutip CSV yang berbeda (awal vs tengah file).
- (+) Tidak ada regresi: 57 tes otomatis OK, `validate.py` lolos, dan angka pipeline (jumlah & nilai per
  tahap) cocok 100% dengan perhitungan manual independen.
- (+) Perbaikan bersifat sempit dan terdokumentasi jujur (K2 sisa & K1/R6 diakui belum diperbaiki, bukan
  diklaim tuntas).
- (−) K2 belum tuntas sepenuhnya (deal berjadwal besok masih ikut blok "BESOK") dan K1 (inisial ganda, format
  telepon rumah) masih ada — keduanya sudah diketahui, kosmetik, dan bukan penghalang rilis.
- Tidak ditemukan cacat baru. Skill v1.0.2 dinyatakan **lulus**, siap lanjut ke uji platform asli (Tahap 6
  langkah 10) bila belum dilakukan.
