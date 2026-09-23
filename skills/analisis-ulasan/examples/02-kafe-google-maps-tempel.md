# 02 — Kafe: 25 ulasan Google Maps ditempel (S2, normal, bukan marketplace)

## Skenario
Pemilik kafe menempel 25 ulasan Google Maps (format `bintang | teks`). Ada keluhan khas kafe (waktu tunggu, parkir, toilet, wifi), sarkasme, ulasan keamanan pangan (rambut di pastry), dan nomor WA di dalam ulasan.

## Input pengguna
> Ini review Google Maps kafe aku (Kopi Senja Fiktif) bulan ini, tolong dirangkum ya, mau aku bahas sama barista besok pagi.
> 5 | Kopi susu gula arennya enak bgt, tempatnya nyaman buat nugas
> 4 | enak, cuma parkiran sempit bgt
> 2 | pelayanannya lama, pesen jam 7 baru dateng jam 8 kurang
> 5 | baristanya ramah, mas Dimas Fiktif ngejelasin menu dgn sabar
> 3 | kopinya oke tp harga lumayan mahal buat porsi segitu
> 1 | Mantap, nunggu 45 menit buat 1 gelas es kopi. Recommended bgt buat yg sabar
> 5 | croissantnya renyah, kopi enak, wifi kenceng
> 4 | enak sih tapi AC nya kurang dingin
> 2 | es kopi nya hambar, kayak air gula doang
> 5 | tempat cozy, musik enak, pasti balik lagi
> 1 | kasir jutek, kembalian kurang 5rb
> 4 | harga terjangkau buat mahasiswa, rasa oke
> 5 | best kopi susu di kota ini sih
> 3 | lumayan, tapi toilet kotor
> 2 | pesanan lama bgt dateng, ramai tapi pegawainya cuma 2
> 5 | matcha latte nya enak, ga terlalu manis
> 4 | wifi sering putus, selebihnya oke
> 5 | pelayanan cepat, ramah
> 1 | nemu rambut di pastry. udah bilang ke kasir cuma dibilang "oh iya kak"
> 5 | nyaman, colokan banyak
> 3 | kopi enak tp nunggu lama
> 4 | kue enak, harga masuk
> 5 | langganan tiap minggu, ga pernah kecewa
> 2 | parkir susah, tukang parkir minta 5rb
> 5 | es kopi susunya juara, reservasi via wa 0812-0000-7788 fast respon

## Langkah agent
1. Tempelan disimpan ke `kafe.txt`, lalu `python3 scripts/olah_ulasan.py kafe.txt --format teks`.
2. Hasil pertama: 6 ulasan (24%) belum terklasifikasi dan 4 ulasan bintang rendah tanpa keluhan terdeteksi. Kamus bawaan berorientasi toko online, sehingga waktu tunggu di kafe, parkir, toilet dan rambut di makanan tidak dikenali.
3. Karena ada pola yang muncul ≥ 3 kali, agent membuat `kamus-kafe.json` di folder kerja (tema `k_tunggu`, `k_fasilitas`, `k_kebersihan`, `p_suasana`) lalu menjalankan ulang dengan `--kamus-tambahan kamus-kafe.json`. Hasilnya tinggal 1 ulasan belum terklasifikasi.

## Output

# Analisis Ulasan — Kopi Senja Fiktif (Google Maps, bulan ini, 25 ulasan)
*Sampel kecil (25 ulasan): anggap sebagai gambaran awal, bukan tren.*

## Ringkasan cepat
- Rata-rata **3,6★**. 60% positif, **28% negatif (1–2★)**.
- Masalah utama: **waktu tunggu pesanan lama** (4 ulasan, termasuk sarkasme "nunggu 45 menit buat 1 gelas… Recommended bgt buat yg sabar", 1★).
- ⚠️ **1 ulasan keamanan pangan**: "nemu rambut di pastry", dan kasir hanya menjawab "oh iya kak" (1★). Satu ulasan saja, tapi ini prioritas segera.
- Kekuatan: **rasa kopi & makanan** (8 ulasan) dan **suasana nyaman untuk nugas** (4 ulasan).

## Sebaran bintang
| Bintang | Jumlah | % |
|---|---|---|
| 5★ | 10 | 40,0% |
| 4★ | 5 | 20,0% |
| 3★ | 3 | 12,0% |
| 2★ | 4 | 16,0% |
| 1★ | 3 | 12,0% |
Rata-rata 3,6★ · Positif 60,0% · Netral 12,0% · Negatif 28,0%.

## Keluhan teratas
| # | Keluhan | Ulasan (%) | Rata-rata ★ | Contoh kutipan | Area |
|---|---|---|---|---|---|
| 1 | Waktu tunggu pesanan lama | 4 (16,0%) | 2,0 | "pesen jam 7 baru dateng jam 8 kurang" | Bar/dapur saat ramai |
| 2 | Fasilitas: parkir, toilet, AC, wifi | 5 (20,0%) | 3,4 | "toilet kotor" · "tukang parkir minta 5rb" · "wifi sering putus" | Fasilitas |
| 3 | Kasir kurang ramah / kembalian kurang | 1 | 1,0 | "kasir jutek, kembalian kurang 5rb" | Kasir |
| 4 | Keamanan pangan (benda asing) | 1 | 1,0 | "nemu rambut di pastry" | Dapur |
| 5 | Rasa hambar | 1 | 2,0 | "es kopi nya hambar, kayak air gula doang" | Bar |
| 6 | Harga dirasa mahal untuk porsinya | 1 | 3,0 | "harga lumayan mahal buat porsi segitu" | Harga |

## Pujian teratas
| # | Pujian | Ulasan (%) | Contoh kutipan |
|---|---|---|---|
| 1 | Rasa enak | 8 (32,0%) | "Kopi susu gula arennya enak bgt" · "croissantnya renyah" |
| 2 | Suasana nyaman, colokan, wifi | 4 (16,0%) | "tempatnya nyaman buat nugas" |
| 3 | Barista/pelayanan ramah | 4 (16,0%) | "baristanya ramah… ngejelasin menu dgn sabar" |
| 4 | Harga ramah mahasiswa | 2 (8,0%) | "harga terjangkau buat mahasiswa" |

## Prioritas perbaikan
| Prioritas | Masalah | Bukti | Tindakan konkret | Ukuran keberhasilan |
|---|---|---|---|---|
| **Segera (hari ini)** | Rambut di pastry + tanggapan kasir | 1 ulasan 1★ (keamanan pangan) | Tim dapur wajib memakai penutup rambut dan menutup etalase pastry. Kasir diberi SOP: minta maaf, ganti atau refund, lalu catat kejadiannya. Balas ulasan itu (skill `balas-ulasan-pelanggan`) | 0 keluhan benda asing; setiap komplain di tempat tercatat |
| **Segera (minggu ini)** | Waktu tunggu lama | 4 ulasan, rata-rata 2,0★ | Tambah 1 orang di bar pada jam ramai (catat jam ramainya dari data kasir). Kasir memberi info estimasi saat bayar ("±15 menit"). Siapkan batch es kopi susu | Tidak ada ulasan "nunggu lama" bulan depan; waktu saji terukur ≤ 15 menit |
| **Minggu ini** (murah) | Toilet kotor, wifi putus | 2 ulasan | Tempel jadwal cek toilet tiap 2 jam; restart atau cek router, lalu tanyakan ke provider | Keluhan fasilitas turun |
| **Pantau** | Parkir sempit/juru parkir | 2 ulasan (di luar kendali langsung) | Tulis info parkir di profil Google Maps; bicarakan tarif dengan pengelola parkir | – |
| **Pantau** | Es kopi hambar; kembalian kurang | 1 + 1 ulasan | Timbang takaran gula dan espresso; kasir menghitung ulang kembalian di depan pembeli | – |

## Ide konten dari pujian
1. **Reels 15 detik "Sudut nugas favorit"**: Hook "Cari kafe colokan banyak?" Kutipan: "tempatnya nyaman buat nugas". CTA: "Simpan lokasi di Google Maps."
2. **Story "Kenalan sama barista kami"**: pakai kutipan "baristanya ramah… ngejelasin menu dgn sabar". Tampilkan barista **dengan izin barista**; nama pembeli tidak ditampilkan.
3. **Carousel "Menu andalan"**: kopi susu gula aren dan croissant, dengan kutipan "croissantnya renyah, kopi enak". Rating yang dikutip harus sama persis dengan angka di Google Maps saat posting.

## Catatan metode
- 25 ulasan dibaca, semuanya berbintang. Nama barista pada kutipan ("mas [nama]") dan nomor WA disamarkan.
- Tema tambahan dibuat lewat `kamus-kafe.json` (waktu tunggu, fasilitas, kebersihan, suasana), lalu script dijalankan ulang. Semua jumlah di atas berasal dari hasil run kedua.
- Koreksi agent:
  - "matcha latte nya enak, ga terlalu manis" (5★) ditandai script sebagai keluhan rasa, padahal ini **pujian**, jadi dihapus dari keluhan.
  - "tempat cozy, musik enak" terhitung "rasa enak" karena kata "enak" untuk musik, jadi dipindah ke suasana. Hasilnya rasa enak 8, bukan 9.
  - "pesanan lama bgt dateng" dihitung script juga sebagai "pengiriman" dan "respons admin". Istilah itu tidak berlaku untuk kafe, jadi digabung ke waktu tunggu.
- Batasan: 25 ulasan terlalu sedikit untuk menyimpulkan tren; ulangi analisis bulan depan.

## Catatan penguji
- Sebaran & rata-rata dicek ulang manual: 10/5/3/4/3 → (50+20+9+8+3)/25 = 3,6 ✓.
- **Kelemahan penting:** kamus bawaan tidak cocok untuk kafe/resto, padahal README menyebut "kafe, resto, salon, klinik Google Maps". Akibatnya keluhan yang **paling penting** (waktu tunggu dan rambut di makanan) tidak terdeteksi tanpa kamus tambahan. Selain itu, "ga terlalu manis" dianggap keluhan (negasi `tidak_manis` masuk `k_rasa`). Mekanisme `--kamus-tambahan` berfungsi baik dan memang menyelesaikannya, tapi menuntut agent menulis regex.
- Semua ulasan di atas fiktif (dibuat penguji); nomor WA memakai pola 0812-0000-xxxx.
