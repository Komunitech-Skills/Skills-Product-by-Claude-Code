# Panduan Memilih Grafik

Pilih grafik berdasarkan **apa yang mau ditunjukkan**, bukan data apa yang tersedia.
Kalau formatnya tidak bisa menampilkan gambar (WA, skrip bicara), gambarkan tren dengan
kata — jangan paksakan deskripsi grafik yang tidak akan dilihat siapa pun.

## Cara memilih (langkah cepat)
1. **Apa yang mau ditunjukkan?**
   - Perubahan dari waktu ke waktu (harian/mingguan/bulanan) → **grafik garis**
   - Bandingkan beberapa kategori (cabang, produk, tim) → **grafik batang**
   - Bagian dari keseluruhan (komposisi biaya, porsi produk) → **batang bertumpuk** atau
     **pie/donat** (maksimal 2–3 kategori untuk pie; lebih dari itu, pakai batang)
   - Sebelum vs sesudah / dua titik saja (bulan ini vs bulan lalu) → **batang berdampingan
     2 kolom**, bukan garis (garis untuk data ≥ 3 titik waktu)
2. **Berapa kategori/serinya?**
   - ≤ 7 kategori → batang vertikal biasa
   - 8–15 kategori → batang horizontal (label panjang lebih terbaca)
   - > 15 kategori → ringkas dulu (top 5–10 + "lainnya"), jangan tampilkan semua
3. **Untuk atasan yang tidak sempat baca detail**, grafik harus bisa dipahami **dalam 5
   detik**: judul grafik = kesimpulannya ("Omzet turun 3 bulan berturut-turut"), bukan
   nama variabel ("Omzet per Bulan"). Tandai titik/batang yang paling penting dengan
   warna beda dari yang lain (1 warna aksen, sisanya netral).

## Kesalahan umum yang dihindari
- Pie chart dengan > 5 potongan → tidak terbaca, ganti batang.
- Grafik garis untuk membandingkan kategori (bukan waktu) → menyiratkan tren yang tidak
  ada; ganti batang.
- Sumbu Y tidak mulai dari 0 pada grafik batang → melebih-lebihkan perbedaan secara
  visual (menyesatkan); sumbu Y batang **selalu mulai dari 0**. Sumbu Y garis boleh tidak
  dari 0 hanya jika judul menjelaskan itu menunjukkan laju perubahan, bukan nilai mutlak.
- Legenda terpisah jauh dari grafik → beri label langsung di ujung garis/ujung batang
  bila memungkinkan, kurangi ketergantungan pada legenda.
- Warna-warni tanpa makna → satu warna netral untuk semua, satu warna aksen untuk yang
  ingin ditonjolkan (kenaikan/penurunan/target).

## Bila format tidak mendukung gambar (WA, skrip bicara)
Gantikan grafik dengan kalimat yang membawa arah & besaran tren, contoh:
- "Omzet turun 3 bulan berturut-turut, dari Rp32 juta jadi Rp24,5 juta (-23%)."
- "Biaya iklan naik tajam (+40%) sementara omzet stagnan — rasio biaya-terhadap-omzet
  naik dari 12% ke 23%."

## Untuk 1 halaman eksekutif / email
Grafik dibuat lewat skill/tool visualisasi yang tersedia di environment (mis. artifact
chart, atau grafik sederhana di `presentasi-instan`), bukan bagian dari script skill ini
— skill ini hanya menentukan **jenis grafik dan pesan judulnya** yang tepat berdasarkan
prinsip di atas.
