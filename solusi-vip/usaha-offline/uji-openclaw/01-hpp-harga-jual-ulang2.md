# Uji ulang 2 — HPP & harga jual es kopi (hitung-hpp 1.0.4)

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal asli (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech`. Home `sol2-usaha-offline` direset lewat script reset tepat sebelum skenario (tidak ada file data yang perlu dibuat ulang; semua data ada di pesan). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama dan uji ulang 1 ([01-hpp-harga-jual.md](01-hpp-harga-jual.md), [01-hpp-harga-jual-ulang.md](01-hpp-harga-jual-ulang.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python dan script skill dijalankan ulang oleh penguji. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran). Keluaran mentah: `hasil/ulang4-*.txt`.

## Cacat sisa dari uji ulang 1 (versi 1.0.3)
BEP Rp19.000 dan Rp20.000 ditulis 450 dan 409 (dibulatkan ke bawah oleh model), padahal script 451 dan 410. Klaim harga pasar tanpa sumber.

## Pesan member
> Mau jual es kopi susu gula aren di kedai saya. Per gelas pakai: kopi bubuk 18 gram (beli 1 kg 180.000), susu UHT 120 ml (1 liter 19.500), gula aren cair 25 ml (botol 1 liter 45.000), es batu 500 perak, gelas+tutup+sedotan 1.800. Sewa tempat 1,5jt/bln, gaji 1 barista 2,4jt, listrik 600rb. Sehari laku kira2 40 gelas, buka 26 hari. Modal per gelas berapa? enaknya dijual berapa biar untung tapi ga kemahalan?

Alat: `read, ls, write, exec`. Agent menulis `hpp-es-kopi-susu-gula-aren.json` (dengan `banding_harga` 18.000; 20.000; 22.000) dan menjalankan script. Skill terpakai.

## Balasan (utuh)
> Udah dihitung pakai data lengkapnya (termasuk asumsi 40 gelas x 26 hari = 1.040 gelas/bulan). Ini hasilnya:
>
> **MODAL (HPP) PER GELAS: Rp 13.332**
> Rinciannya:
> • Bahan baku (kopi, susu, gula aren, es batu): Rp 7.205
> • Gaji barista (dialokasikan per gelas): Rp 2.308
> • Sewa + listrik (dialokasikan per gelas): Rp 2.019
> • Gelas+tutup+sedotan: Rp 1.800
>
> Bahan baku itu porsi terbesar (54%), dan kopi bubuk sendiri Rp 3.240/gelas — komponen tunggal termahal.
>
> **PILIHAN HARGA JUAL (dibanding beberapa opsi):**
>
> • Rp 18.000 → untung Rp 4.668/gelas (margin 26%), tapi BEP naik ke 501 gelas/bulan (48% dari target jual) — agak mepet, untungnya tipis.
> • Rp 20.000 → untung Rp 6.668/gelas (margin 33%), BEP 410 gelas (39% dari target) — aman & masih masuk akal untuk kedai kopi susu gula aren.
> • **Rp 21.000 → rekomendasi saya.** Untung Rp 7.668/gelas (margin 36,5%), BEP cuma 376 gelas/bulan (36% dari target 1.040 gelas). Masih kompetitif untuk harga pasar es kopi susu gula aren (umumnya 18-25rb).
> • Rp 22.000 → untung Rp 8.668/gelas (margin 39%), BEP 347 gelas — lebih longgar tapi mulai masuk range "agak mahal" buat produk sejenis.
>
> 💡 **Saran saya:**
> 1. Jual di **Rp 20.000–21.000**. Di harga segini kamu udah untung sehat (margin 33-36%) tapi masih wajar dibanding kedai sejenis, nggak kemahalan.
> 2. Kalau mau sedikit psikologis, Rp 19.500 atau Rp 20.000 kerasa "lebih murah" daripada Rp 21.000 meski bedanya kecil — tapi laba turun dikit.
> 3. Dengan target jual 40 gelas/hari, BEP di harga Rp 21.000 cuma butuh ±14-15 gelas/hari — jadi ada margin aman kalau rame-sepi.
> 4. Catatan: ini belum dikurangi pajak dan belum ada upah untuk kamu sendiri (pemilik) kalau ikut turun tangan jaga kedai — kalau kamu juga kerja di situ, pertimbangkan masukkan sebagai biaya juga.
>
> Mau saya coba hitung juga kalau harga bahan naik dikit, atau mau lihat BEP di harga lain?

## Verifikasi independen
Penguji menjalankan ulang `hitung_hpp.py` pada JSON agent (plus `--banding-harga "19500;21000"`) dan menghitung terpisah dengan Python (variabel 9.005, tetap 4.500.000/1.040, BEP = ceil(4.500.000 ÷ (harga − 9.005))):

| Pos | Benar | Balasan |
|---|---:|---|
| HPP per gelas | 13.331,92 → 13.332 | ✔ |
| Bahan baku / porsi | 7.205 / 54,04% | ✔ "54%" |
| Gaji / sewa+listrik per gelas | 2.307,69 / 2.019,23 | ✔ 2.308 / 2.019 |
| Kopi bubuk (komponen tunggal terbesar) | 3.240 | ✔ |
| Rp18.000: laba / margin / BEP | 4.668 / 25,93% / **501** (48,1%) | ✔ |
| Rp20.000 | 6.668 / 33,34% / **410** (39,35%) | ✔ (uji ulang 1: 409 ✘) |
| Rp21.000 | 7.668 / 36,51% / **376** (36,07%) | ✔ |
| Rp22.000 | 8.668 / 39,4% / **347** | ✔ |
| BEP Rp21.000 per hari | 375,16 ÷ 26 = 14,4 | ✔ "±14-15 gelas/hari" |

Rp21.000 tidak ada di `banding_harga` file JSON, tetapi angkanya identik dengan keluaran script (kemungkinan dijalankan dengan argumen tambahan; argumen tidak dapat diaudit).

## Penilaian
- **Cacat sisa hilang: YA.** Semua BEP kini sama persis dengan script dan dibulatkan ke atas: *"Rp 20.000 → … BEP 410 gelas (39% dari target)"*, *"Rp 21.000 → … BEP cuma 376 gelas/bulan (36% dari target 1.040 gelas)"*.
- **Regresi:** tidak ada. Sisa kecil: klaim harga pasar tanpa sumber masih muncul (*"harga pasar es kopi susu gula aren (umumnya 18-25rb)"*); poin 4 (gaji pemilik belum dihitung, belum pajak) justru nilai tambah yang jujur.
- **Skor: 8,5/10** (uji ulang 1: 8). **LULUS.**
