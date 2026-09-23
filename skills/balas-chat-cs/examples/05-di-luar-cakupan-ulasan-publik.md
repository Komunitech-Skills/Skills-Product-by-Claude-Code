# 05 — Di luar cakupan: membalas ulasan bintang 1 di Google Maps

**Skenario:** S5 — ulasan publik, bukan chat pribadi.

**Input pengguna:**
> Ada yang kasih bintang 1 di Google Maps warung saya, tulisannya "pelayanan lama, es teh kemanisan". Balesin dong biar orang lain nggak ilfeel.

## Output

Ini **ulasan publik** (dibaca calon pelanggan lain), jadi cara membalasnya sedikit berbeda dari chat pribadi: lebih singkat, tidak membahas detail transaksi, dan ditujukan juga untuk pembaca lain.

- Jika skill **`balas-ulasan-pelanggan`** terpasang, ketik: *"balas ulasan Google Maps bintang 1: 'pelayanan lama, es teh kemanisan', warung [nama]"* — skill itu yang khusus menangani ulasan publik.
- Prinsip singkatnya: terima kasih atas masukan → akui tanpa membela diri → sebut perbaikan yang **benar-benar** dilakukan → ajak kembali. Jangan menawarkan imbalan agar ulasan diubah.

Contoh balasan netral yang aman dipakai sementara:
```
Terima kasih atas masukannya, Kak, dan mohon maaf atas waktu tunggu serta rasa es teh yang kurang pas. Masukan ini kami sampaikan ke tim; untuk es teh, Kakak bisa minta kadar gula sesuai selera saat memesan. Semoga kami bisa melayani lebih baik di kunjungan berikutnya 🙏
```
(Kalimat "bisa minta kadar gula" hanya dipakai jika warung memang melayaninya.)

## Catatan penguji
- Sesuai "Kapan TIDAK digunakan": diarahkan ke `balas-ulasan-pelanggan`.
- Tetap memberi contoh netral dengan penanda fakta yang harus dicek, tidak mengarang perbaikan.
- SKILL.md tidak menyediakan kalimat cadangan jika pembeli tidak punya skill rujukan (ringan; sama seperti skill lain di bundle ini).
