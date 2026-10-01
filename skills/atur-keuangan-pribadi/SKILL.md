---
name: atur-keuangan-pribadi
description: Mengatur keuangan pribadi & keluarga Indonesia dalam Rupiah — anggaran bulanan zero-based dan 50/30/20 (kiriman orang tua, arisan, zakat/perpuluhan opsional, cicilan motor/KPR, e-wallet, THR/bonus dibagi 12), target dana darurat 3–12 bulan sesuai status, rencana pelunasan utang Avalanche vs Snowball dengan jadwal bulanan dihitung script (kartu kredit, KTA, paylater, pinjol legal; konversi bunga flat ke efektif; peringatan pinjol ilegal & gali lubang tutup lubang), dan tabungan bulanan untuk target (DP rumah, sekolah anak, haji/umrah, pensiun). Gunakan saat pengguna minta atur gaji, bikin anggaran rumah tangga, hitung dana darurat, lunasi utang/cicilan, atau nabung untuk tujuan — personal budget, household budgeting, emergency fund, debt payoff avalanche snowball, savings goal, financial planning Indonesia. Bukan untuk keuangan usaha (pakai arus-kas-13minggu / laporan-keuangan-emkm), THR karyawan (hitung-thr), atau rekomendasi beli/jual investasi.
---

# Atur Keuangan Pribadi

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu pekerja, keluarga, dan pekerja lepas Indonesia menjawab empat pertanyaan uang sehari-hari dengan **angka yang dihitung, bukan dikira**:
1. **Gaji habis ke mana, dan seharusnya ke mana?** → anggaran bulanan zero-based + banding 50/30/20.
2. **Berapa dana darurat yang cukup?** → 3–12 bulan pengeluaran pokok sesuai status.
3. **Utang mana dulu yang dilunasi, kapan lunas, total bunganya berapa?** → Avalanche vs Snowball dengan jadwal bulanan.
4. **Nabung berapa per bulan untuk DP rumah / sekolah anak / haji / pensiun?** → nilai waktu uang sederhana dengan asumsi tertulis.

Hasil langsung siap dipakai: tabel anggaran, target angka, urutan pelunasan, dan langkah minggu ini.

## Kapan digunakan
- "Gaji saya 7,5 juta, istri 3 juta, bantu atur anggaran bulanan. Ada kiriman ortu dan cicilan motor."
- "Berapa dana darurat yang harus saya punya? Saya freelancer, pengeluaran pokok 5 juta."
- "Utang kartu kredit 12 juta, paylater 3 juta, KTA 20 juta. Mana dulu yang dilunasi?"
- "Leasing motor bunga flat 12% tiga tahun, sebenarnya bunga efektifnya berapa?"
- "Mau DP rumah 60 juta 5 tahun lagi, nabung berapa per bulan?" / "Dana pendidikan anak masuk SD 6 tahun lagi."

## Kapan TIDAK digunakan
- Keuangan **usaha** (arus kas toko, laporan laba rugi UMKM) → `arus-kas-13minggu`, `laporan-keuangan-emkm`.
- Menghitung THR/gaji **karyawan** yang dibayar perusahaan → `hitung-thr`, `slip-gaji-bpjs`.
- Meminta rekomendasi **beli/jual** saham, kripto, reksa dana, emas, atau produk tertentu → tolak dengan sopan: skill ini tidak merekomendasikan produk/instrumen. Boleh menjelaskan konsep umum (risiko, likuiditas) dan menyarankan perencana keuangan bersertifikat.
- Meminta cara mencari pinjaman baru untuk menutup utang lama, atau pinjol yang "pasti cair tanpa cek" → tolak; jelaskan bahaya gali lubang tutup lubang (lihat `references/utang-dan-pinjol.md`).
- Pajak pribadi (SPT, PPh) → di luar cakupan; sarankan konsultan pajak.
- Kasus rumit (warisan, perceraian, utang macet ke banyak pihak dengan penagihan kasar, kebangkrutan usaha keluarga) → beri gambaran angka dasar lalu arahkan ke perencana keuangan / LBH / pengaduan OJK.

## Input yang dibutuhkan
Tanyakan **sekali** dalam satu pesan, hanya yang relevan dengan permintaan:
- **Anggaran:** pemasukan BERSIH per bulan (per orang bila suami-istri), pemasukan tahunan (THR, bonus, gaji ke-13), daftar pengeluaran rutin + perkiraan jumlahnya.
- **Dana darurat:** pengeluaran pokok per bulan, status (lajang / menikah / punya anak atau tanggungan / pekerja lepas-pemilik usaha / PNS-pegawai sangat stabil), saldo sekarang, kemampuan setor per bulan.
- **Utang:** per utang → nama, sisa saldo, bunga (sebut per tahun / per bulan / per hari, dan **flat atau efektif**), cicilan minimum; plus uang ekstra yang sanggup disisihkan.
- **Target:** nama target, biaya bila dibeli hari ini, berapa tahun lagi, dana yang sudah ada, kemampuan menabung.

Jika pengguna ingin cepat, pakai default dan **sebutkan asumsinya**: pola 50/30/20; inflasi 4%/tahun (pendidikan sering lebih tinggi, tawarkan 8–10% sebagai skenario); imbal hasil 0% (skenario tambahan hanya jika pengguna menyebut angkanya sendiri); pensiun 20 tahun; bunga tanpa satuan ≥ 3 dianggap **per tahun efektif**; di bawah 3 **wajib ditanyakan** (biasanya per bulan) — salah periode = hasil salah besar.

## Langkah kerja
1. **Pastikan cakupan.** Pribadi/keluarga? Bukan keuangan usaha, bukan permintaan rekomendasi produk. Pisahkan uang usaha dan uang rumah tangga bila tercampur (anjurkan "gaji" tetap dari usaha untuk diri sendiri).
2. **Kumpulkan & rapikan angka.** Parsing gaya Indonesia: "1,5jt" = 1.500.000; "750rb" = 750.000; "Rp1.500.000". Tolak "5M" (ambigu juta/miliar) — minta ditulis ulang.
3. **Hitung lewat script bila bisa dijalankan** (`scripts/keuangan.py`, Python standar, lihat di bawah). Jika script tidak bisa dijalankan, hitung manual dengan rumus di `references/rumus-manual.md` dan tunjukkan langkahnya. **Jangan mengira-ngira angka.**
4. **Anggaran (zero-based):**
   - Pemasukan/bulan = pemasukan bersih rutin + (THR + bonus tahunan) ÷ 12 (dibulatkan ke bawah). Pekerja berpenghasilan tidak tetap: pakai bulan **terendah** 3–6 bulan terakhir.
   - Kelompokkan pos: **Kebutuhan wajib**, **Keluarga & sosial/ibadah** (kiriman orang tua, zakat/perpuluhan/sedekah/persembahan/dana punia — opsional, sesuai keyakinan pengguna, jangan memaksakan), **Keinginan**, **Tabungan & pelunasan ekstra** (dana darurat, target, arisan sebagai tabungan wajib).
   - Setiap rupiah diberi tugas sampai **sisa = Rp0**. Defisit → potong Keinginan dulu; jangan ditutup dengan paylater/pinjol.
   - Banding pola 50/30/20 (Kebutuhan termasuk keluarga/sosial). Keluarga dengan tanggungan/kota mahal: tawarkan 60/20/20 atau 70/10/20 — yang penting tabungan tetap ada.
   - **E-wallet (GoPay/OVO/DANA/ShopeePay):** top-up bukan pengeluaran; catat menurut pemakaiannya agar tidak dobel.
   - Total cicilan > 30% pemasukan → peringatkan, jangan tambah utang.
   - Bila ada data realisasi (mis. mutasi rekening), tampilkan **realisasi bulan lalu vs anggaran** per pos; potongan > 30% dari realisasi ditandai sebagai **target bertahap** (mis. turun bertahap 2–3 bulan), jangan disajikan seolah langsung mudah.
   Detail kategori khas Indonesia: `references/pos-anggaran-indonesia.md`.
5. **Dana darurat:** dasar (pengeluaran pokok) **wajib dihitung script** dari daftar pos yang dicetak eksplisit — jangan menjumlah sendiri:
   - Pokok = **kebutuhan wajib** (tempat tinggal, makan/dapur, listrik/air, transport, sekolah, BPJS) + **SEMUA cicilan/utang minimum** (PayLater, kartu kredit, KPR, motor/leasing, KTA, pinjol, pinjaman keluarga yang ditagih rutin) + **kewajiban rutin keluarga** (kiriman orang tua/mertua/adik, tanggungan). Bukan jajan/hiburan/top-up investasi/arisan.
   - Dari mutasi/anggaran: jalankan `anggaran`; bagian "Dasar dana darurat" mencetak tabel **pos DIMASUKKAN** dan **pos DIKELUARKAN + alasannya**. Kiriman keluarga **masuk pokok secara bawaan**. Tanpa anggaran: `dana-darurat --pos ... --cicilan ... --keluarga ... --dikeluarkan "nama=jumlah;alasan"`.
   - **Kutip angka script apa adanya** dan di balasan sebutkan **pos yang dimasukkan dan yang dikeluarkan beserta alasannya** (satu-dua baris). Pos keluarga/sosial tidak pernah dikeluarkan diam-diam: bila ragu (mis. kiriman ortu "kadang-kadang"), tetap masukkan dan katakan "bila kiriman ini bisa dihentikan saat darurat, target turun menjadi Rp…" — atau tanyakan sekali. Keputusan pengguna dijalankan ulang dengan `--bukan-pokok "nama pos"` / `--pokok-juga "nama pos"`.
   - Target = pokok × bulan: PNS/pegawai sangat stabil 3–6, lajang 3–6, menikah 6–9, punya anak/tanggungan 9–12, pekerja lepas/pemilik usaha 12. Lama tercapai = kekurangan ÷ setoran (dibulatkan ke atas). Punya utang berbunga tinggi: dana darurat awal ~1 bulan dulu, lalu fokus utang.
   - Angka di "Langkah minggu ini" harus sama dengan tabel (mis. setoran dana darurat yang disebut = setoran di tabel, bukan seluruh uang yang dihemat bila sebagian dipakai menutup defisit).
6. **Utang:**
   - Bunga **flat** (leasing motor/mobil, sebagian KTA) → konversi ke **efektif** dulu (`konversi-flat`). Jelaskan: flat dihitung dari pokok awal sepanjang tenor, sehingga bunga efektifnya hampir dua kali lipat.
   - Simulasikan **Avalanche** (bunga tertinggi dulu) dan **Snowball** (saldo terkecil dulu) dengan anggaran tetap; cicilan minimum utang yang lunas dialihkan ke utang berikutnya.
   - Laporkan: urutan, bulan lunas tiap utang, total bunga, selisih biaya, dan kapan "kemenangan pertama".
   - **Satuan bunga wajib jelas** (%/th, %/bln, %/hari). Bunga flat KTA sering disebut per bulan ("0,9% per bulan") → tulis `--bunga-flat "0,9%/bln"`. Angka tanpa satuan di bawah 3: `konversi-flat` menampilkan dua tafsiran, `utang` menolak — **tanyakan ke pengguna**, jangan menebak (salah satuan = meleset ±11×). Salin bunga efektif 4 desimal dari `konversi-flat` ke `utang`.
   - Ditawari **take over/refinancing/konsolidasi**? Bandingkan total bunga sisa lama vs total bunga baru + provisi/admin/penalti pelunasan (lihat `references/utang-dan-pinjol.md`). Tanpa rekomendasi produk.
   - **Wajib cek bahaya:** cicilan minimum ≤ bunga bulanan → utang tidak akan lunas; bunga > 0,1%/hari (±3%/bulan) → di atas batas pinjol konsumtif berizin OJK 2026, curigai pinjol ilegal; kartu kredit > 1,75%/bulan → di atas batas BI. Beri kontak resmi OJK (lihat `references/utang-dan-pinjol.md`).
7. **Target keuangan:** biaya nanti = biaya hari ini × (1 + inflasi/12)^bulan. Tabungan/bulan = (biaya nanti − terkumpul × (1+r)^bulan) × r ÷ ((1+r)^bulan − 1), r = imbal/12; jika r = 0 dibagi jumlah bulan. Dibulatkan ke atas. Banding dengan kemampuan; bila kurang, tawarkan tiga tuas: perpanjang waktu, turunkan target, tambah pemasukan. Urutan prioritas umum: dana darurat awal → utang bunga tinggi → dana darurat penuh → target bertenggat (sekolah) → target fleksibel.
8. **Tulis hasil** sesuai format di bawah, dengan bahasa sehari-hari yang tidak menghakimi.

## Script (opsional, disarankan)
Script ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (`scripts/keuangan.py`) — jangan mencarinya dengan `find /`. File milik pengguna (mis. mutasi rekening) dicari **hanya di folder kerja (workspace)** atau path yang disebut pengguna, bukan ke seluruh disk; tidak ketemu → tanyakan lokasinya.
Jalankan dari folder skill (`python3`; Windows: `python` atau `py`):
```
python3 scripts/keuangan.py anggaran --pemasukan "Gaji=7,5jt" --musiman "THR=7,5jt" --pos "Kontrakan=1,8jt" --pos "Kiriman ortu=750rb" --pos "Nongkrong=400rb:keinginan"
python3 scripts/keuangan.py dana-darurat --pengeluaran-pokok 4,5jt --cicilan "PayLater=650rb" --cicilan "Motor=1,15jt" --keluarga "Kiriman ortu=1jt" --status anak --saldo 6jt --setoran 750rb
python3 scripts/keuangan.py utang --utang "Kartu kredit;12jt;1,75%/bln;600rb;kk" --utang "Paylater;3jt;2,5%/bln;200rb;paylater" --ekstra 1jt --metode banding [--jadwal]
python3 scripts/keuangan.py konversi-flat --pokok 30jt --bunga-flat "0,9%/bln" --tenor 24 [--sudah-bayar 6]   # atau "12%/th"
python3 scripts/keuangan.py target --nama "DP rumah" --biaya-sekarang 60jt --tahun 5 --inflasi 4 [--imbal 5] --terkumpul 10jt --kemampuan 700rb
python3 scripts/keuangan.py target --jenis pensiun --pengeluaran-bulanan 6jt --tahun 25 --lama-pensiun 20
```
- Pos anggaran: `nama=jumlah[:wajib|sosial|keinginan|tabungan]` (tanpa label → ditebak dari nama; tebakan ditandai). `anggaran` juga mencetak **Dasar dana darurat**: pos dimasukkan (wajib + semua cicilan + kiriman keluarga) dan pos dikeluarkan + alasan, beserta angka siap pakai untuk `dana-darurat`. Ubah atas keputusan pengguna: `--bukan-pokok "Kiriman ortu"`, `--pokok-juga "Arisan RT"`.
- Dana darurat: `--pengeluaran-pokok` (gabungan) dan/atau rincian `--pos "nama=jumlah"`, `--cicilan "nama=jumlah"`, `--keluarga "Kiriman ortu=1jt"` (berulang); `--dikeluarkan "nama=jumlah;alasan"` hanya dicetak, tidak dijumlahkan. Tanpa cicilan/keluarga tercatat, script mencetak "CEK CICILAN"/"CEK KIRIMAN KELUARGA" — tanyakan/cek dulu ke pengguna.
- Utang: `nama;saldo;bunga;cicilan_minimum[;jenis]`, bunga **dengan satuan** `24%/th`, `1,75%/bln`, `0,1%/hari` (kata sehari-hari juga diterima: `18% setahun`, `1,5% sebulan`, `1,5 persen per bulan`; atau `--per bulan|tahun` untuk angka tanpa satuan). Bunga bertanda `flat` ditolak di `utang` (konversi dulu); tandai `efektif` (mis. `1,6275%/bln efektif`) agar catatan FLAT untuk KTA/motor/mobil tidak muncul; jenis `kk|kta|paylater|pinjol|kpr|motor|mobil|keluarga|lain`.
- Nominal gaji/saldo/pokok/pos anggaran < Rp10.000 (mis. "1.500"; pos yang ditulis dengan satuan seperti `5rb` tidak diperingatkan) → bagian PERINGATAN INPUT; konfirmasi ke pengguna. `target --kemampuan` juga menghitung bulan ke berapa target tercapai.
- Input salah → pesan ramah tanpa traceback (kode keluar 2). Uji: `python3 tests/uji_regresi.py`.

## Format output
```
## Ringkasan (3 kalimat)
[kondisi sekarang → masalah utama → langkah terpenting]

## [Anggaran | Dana Darurat | Rencana Pelunasan | Target] — tabel dari script / hitungan manual

## Asumsi yang dipakai
- [pola, inflasi, imbal hasil, periode bunga, pembulatan]

## Langkah minggu ini (maks. 5, konkret)
1. ...

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.
```
Gunakan tabel Markdown dan format Rupiah `Rp1.500.000`. Jangan menampilkan jadwal bulanan penuh kecuali diminta (ringkas: bulan lunas tiap utang).

## Contoh singkat
**Input:** "Utang KK 12 juta (1,75%/bln, minimum 600rb), paylater 3 juta (2,5%/bln, 200rb), pinjam kakak 2 juta (tanpa bunga, 250rb), KTA 20 juta (11%/th efektif, 700rb). Sanggup tambah 1 juta/bulan."
**Output inti (dari script):** Avalanche (Paylater → KK → KTA → kakak): semua lunas bulan ke-15, total bunga Rp3.345.301. Snowball (kakak → Paylater → KK → KTA): juga 15 bulan, bunga Rp3.501.409, tapi utang pertama lunas lebih cepat (bulan ke-2 vs ke-3). Selisih Rp156.108 → pilih sesuai watak. Contoh lengkap: `examples/uji-pembuat-01-keluarga-muda-cicilan.md`.

## Batasan & penanganan error
- **Bukan nasihat keuangan/investasi.** Tidak ada rekomendasi beli/jual instrumen atau produk bank/fintech tertentu; imbal hasil hanya asumsi yang disebut pengguna.
- Aturan & batas bunga (OJK, BI) dicek **26 September 2026** dan bisa berubah — sebut tanggal ini dan sarankan cek ulang di situs resmi.
- Minimum kartu kredit (5% tagihan) dimodelkan sebagai nominal tetap; dampaknya kecil bila anggaran pelunasan tetap.
- Simulasi utang mengabaikan denda, biaya admin, perubahan bunga (KPR floating), dan belanja baru di kartu kredit; bunga harian dihitung 30 hari/bulan. Nilai pelunasan dipercepat resmi bisa berbeda — tanyakan ke kreditur.
- Angka tidak masuk akal (bunga negatif, saldo negatif, bunga > 50%/bulan, anggaran < total cicilan minimum) → minta koreksi, jangan dilanjutkan diam-diam.
- Pengguna tertekan karena penagihan utang (ancaman, penyebaran data) → tetap tenang dan empatik; tegaskan penagihan dengan ancaman/intimidasi dilarang, arahkan ke pengaduan OJK (157) dan, bila ada ancaman pidana, kepolisian. Jangan menyarankan kabur dari kewajiban utang yang sah.
- Data keuangan pengguna tidak disimpan ke file kecuali diminta; script tidak memakai internet.
