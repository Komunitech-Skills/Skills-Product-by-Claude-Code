# Contoh 3 (Uji Independen — Akun B) — Sambal Botolan Rumahan

**Input pengguna:**
> "Saya bikin sambal rumahan, enak katanya keluarga saya, mau saya botolin dan jual online. Belum pernah jualan sama sekali. Punya sekitar 80 follower IG (kebanyakan teman/keluarga) dan 40 kontak WA."

## Simulasi jalan skill (dibaca hanya dari SKILL.md)
Input wajib "harga rencana" belum disebutkan pengguna → sesuai Langkah 1/Input, agent seharusnya tanya sekali dalam satu pesan. Untuk kelanjutan skenario, diasumsikan pengguna menjawab: harga Rp28.000/botol 250ml, belum ada HPP pasti tapi diperkirakan Rp14.000/botol.

### 1. Hipotesis
> "Kami percaya **ibu rumah tangga/pekerja kantoran yang suka makan pedas tapi malas ulek sambal tiap hari** mau membayar **Rp28.000** untuk **sambal botolan rumahan 250ml** karena bisa **menghemat waktu masak tanpa kehilangan rasa 'buatan rumah'**. Kami akan tahu ini benar jika minimal 15% dari yang ditawari benar-benar pre-order dalam 7 hari."

Catatan kesesuaian: follower IG 80 < ambang 100 di `references/menu-uji-murah.md` untuk metode polling story — skill mengarahkan memakai kanal yang **paling sesuai**, jadi Akun B memilih pre-order WA (40 kontak ≥ ambang 30) sebagai metode utama, IG story sebagai pelengkap saja (bukan metode utama sendirian). Ini konsisten dengan aturan "boleh pakai lebih dari satu metode sekaligus".

### 2. Metode uji terpilih
Pre-order via broadcast WA (40 kontak, di atas ambang 30) + status/story sebagai penguat kesadaran.

### 3. Kriteria lulus/gagal (ditetapkan sebelum uji)
- Minimal ditawari: 25 (kirim ke 25 dari 40 kontak yang relevan dengan urusan masak/rumah tangga)
- LULUS: konversi ≥15% | LULUS BERSYARAT: 8%–<15% | GAGAL: <8%
- Harga Rp28rb tergolong menengah-bawah, ambang default dipertahankan (tidak dinaikkan ke 20%/10% karena bukan barang impulsif murni — makanan tahan lama, dipikir dulu meski sebentar).

### 4. Hasil setelah 7 hari
25 ditawari, 4 pre-order.

```
$ python3 scripts/hitung_validasi.py --ditawari 25 --preorder 4 --harga 28000 --hpp 14000 --biaya-uji 35000
=== HASIL VALIDASI IDE ===
Ditawari       : 25 orang/tampilan
Pre-order/beli : 4
Konversi       : 16.0%
Ambang         : LULUS >= 15% | LULUS BERSYARAT >= 8% | GAGAL < 8%
Klasifikasi    : LULUS
...
Margin per unit      : Rp14.000  (Rp28.000 - Rp14.000)
Total margin preorder: Rp56.000  (14000 x 4 unit)
Biaya uji            : Rp35.000
Selisih              : Rp21.000  (SUDAH balik modal uji)
```
Verifikasi independen (Decimal, manual): 4/25 = 0.16 → 16.0% ✅. Margin unit 28.000-14.000=14.000 ✅. Total margin 14.000×4=56.000 ✅. Selisih 56.000-35.000=21.000 ✅. Cocok persis dengan output script.

### 5. Keputusan
**LANJUT.** Konversi 16,0% di atas ambang LULUS, sudah balik modal uji (+Rp21.000). Sesuai SKILL.md Langkah 6, agent seharusnya mengarahkan ke `hitung-hpp` untuk HPP/BEP produksi rutin dan `harga-jual-marketplace` bila mau listing di Shopee/TikTok Shop.

## Catatan penguji
- Alur SKILL.md diikuti persis tanpa perlu menebak-nebak; angka cocok 100% dengan perhitungan independen.
- Satu titik longgar: SKILL.md tidak eksplisit menjelaskan apa yang terjadi kalau kanal pengguna (follower IG 80) berada **di bawah** ambang tabel referensi (100) untuk satu metode tapi di atas ambang metode lain (WA 40≥30) — agent harus menyimpulkan sendiri memakai WA sebagai utama. Ini masih masuk akal dan tidak menyesatkan, tapi sebaiknya SKILL.md menambah satu kalimat eksplisit untuk kasus kanal "campuran, sebagian di bawah ambang".
