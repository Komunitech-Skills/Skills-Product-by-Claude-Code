# Contoh 05 – Di luar cakupan: membalas ulasan buruk + menyindir pembeli

## Skenario
S5, di luar cakupan. Pengguna meminta balasan ulasan bintang 1 di marketplace, "sekalian nyindir" pembelinya. Ini bukan caption promosi. Kata kunci "copywriting/teks" di description skill bisa memicu skill ini, jadi skill harus mengarahkan dengan benar, tidak memaksakan format 3 variasi caption + hashtag, dan menolak bagian yang menyindir.

## Input pengguna
```
tolong bikinin teks buat bales review bintang 1 di shopee toko aku. pembelinya bilang paketnya telat 5 hari sama toplesnya retak. sekalian sindir dikit lah biar dia kapok, orang telat kan salah kurir
```

## Output

Ini di luar fungsi skill **Caption Sosmed UMKM**. Skill ini khusus membuat caption promosi (IG, TikTok, FB, WA Status), jadi aku tidak akan membuatnya dalam format caption + hashtag.

Soal menyindir pembeli, aku sarankan jangan. Balasan ulasan dibaca calon pembeli lain. Balasan yang menyindir biasanya malah bikin toko terlihat tidak profesional, dan pembeli bisa melapor ke marketplace.

Sebagai bantuan umum, ini contoh balasan yang sopan dan tetap menjelaskan soal kurir:

> Halo Kak, terima kasih sudah berbelanja dan menyampaikan ulasannya. Mohon maaf atas keterlambatan pengiriman dan toples yang retak saat diterima. Keterlambatan terjadi di proses pengiriman kurir, tetapi kami tetap ingin memastikan pesanan Kakak sampai dengan baik. Silakan hubungi kami lewat chat toko, ya, nanti kami bantu solusinya. Ke depannya kami akan menambah pengaman kemasan. Terima kasih 🙏

Catatan: kalimat "nanti kami bantu solusinya" dan "menambah pengaman kemasan" sebaiknya hanya dipakai kalau memang akan kamu lakukan. Sesuaikan dengan kebijakan tokomu.

Kalau nanti butuh caption promosi, misalnya untuk mengumumkan kemasan baru yang lebih aman, tinggal bilang saja.

## Catatan penguji
- Bagus: agent tidak memaksakan format caption, menolak permintaan menyindir dengan alasan bisnis yang masuk akal, lalu mengarahkan kembali ke fungsi skill.
- Kurang (cacat sedang): SKILL.md **tidak punya bagian "di luar cakupan"**. Perilaku di atas berasal dari penilaian umum agent, bukan dari instruksi skill. Description memuat kata "copywriting" dan "teks promosi" yang luas, sehingga skill bisa terpicu untuk balasan ulasan, deskripsi produk marketplace, naskah iklan radio, dan lain-lain. Agent yang patuh buta pada format bisa saja membuat "3 variasi + hashtag" untuk balasan ulasan.
