# Skenario 1 (S1) — Toko kue rumahan, Bekasi, IG+TikTok, minggu berisi tanggal kembar 10.10

**Kategori:** Normal, profil belum ada (wawancara sekali) — minggu spesifik diminta manual (bukan minggu
depan dari hari ini) supaya memuat tanggal kembar 10.10.2026, sekaligus menguji `nomor_minggu.py` pada
minggu nyata.

## Input pengguna (giliran 1)
> Buatin paket konten buat usaha kue rumahan aku dong, minggu tanggal 5-11 Oktober 2026. Aku jualan di
> IG sama TikTok.

## Output agent (giliran 1) — wawancara profil (sekali, sesuai `templates/PROFIL.md`)
```
Sebelum bikin paket kontennya, aku perlu tahu sedikit soal usahamu dulu (cukup sekali ya, nanti dipakai
lagi tiap minggu tanpa tanya ulang). Jawab santai aja, boleh singkat:

1. Nama usaha & produk utama apa yang paling mau didorong minggu ini? (mis. kue apa aja)
2. Target pembelinya siapa dan di kota/wilayah mana?
3. Order lewat mana (WA/DM/lainnya), dan ada nomor WA yang mau dicantumkan?
4. Sanggup bikin berapa video pendek minggu ini (sisanya foto/Story aja)?
5. Punya PIRT/BPOM/halal yang BENAR-BENAR sudah terdaftar? Ada klaim yang TIDAK boleh dipakai?

Kalau mau cepat, bilang aja "pakai default" — aku isi asumsi wajar dan nanti kucatat di akhir hasil.
```

## Input pengguna (giliran 2)
> 1. Kue Rumahan Bu Sari, di Bekasi. Lagi mau dorong kue lapis legit sama brownies kukus, nastar toples juga ada
> 2. Ibu-ibu arisan & pekerja kantoran usia 25-45 di Bekasi, buat oleh-oleh/snack kantor
> 3. WA ya, nomornya 0812-0000-1234, DM IG juga boleh
> 4. 2 video aja minggu ini, sisanya foto
> 5. Ada PIRT (P-IRT No. 2023217010203-fiktif ya buat contoh ini). Jangan bilang "paling laris di Bekasi" soalnya belum ada buktinya

## Output agent (giliran 2)

`konten/PROFIL.md` disimpan (ringkasan): Kue Rumahan Bu Sari — Bekasi — kue lapis legit, brownies kukus,
nastar toples — target ibu arisan & pekerja kantoran 25-45 Bekasi — nada hangat/santai — order WA
0812-0000-1234 & DM IG — 2 video/minggu — PIRT P-IRT No. 2023217010203 (fiktif, contoh uji) — kategori
pangan/kuliner (sensitif) — dilarang klaim "paling laris di Bekasi" tanpa bukti.

Perintah yang dijalankan:
```
python3 scripts/nomor_minggu.py --mulai 2026-10-05 --format json
```
Hasil relevan: minggu **2026-W41** (Senin 05 Okt – Minggu 11 Okt 2026). Momen otomatis terdeteksi:
Sabtu 10 Okt 2026 = **Tanggal kembar 10.10** (promo). Tidak ada gajian (tgl 25/1) di minggu ini — dicek,
bukan dikarang.

```
# Paket Konten Minggu 2026-W41 — Kue Rumahan Bu Sari
Periode: Senin, 05 Okt 2026 s.d. Minggu, 11 Okt 2026  |  Platform: Instagram, TikTok

## Senin 05 Okt 2026 — Instagram Feed/Foto
Pilar: Edukasi produk  |  Momen: -  |  Jam disarankan: 11.00 & 19.30 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Tau gak bedanya kue lapis legit 18 lapis sama yang cuma 9 lapis?"
Caption:
Kue lapis legit Bu Sari dipanggang 18 lapis satu-satu, sabar demi tekstur lembut & aroma rempah yang
kerasa sampai gigitan terakhir. Cocok buat oleh-oleh arisan atau parsel kantor.
Bahan dipilih sendiri tiap minggu, dipanggang di rumah — bukan produksi massal.
Mau pesan buat acara arisan bulan ini? Chat WA aja, Kak, kita bantu hitung porsinya. 🍰
Order: WA 0812-0000-1234 / DM Instagram
Naskah video: - (format foto, tidak perlu naskah)
Brief foto/video: potongan kue lapis legit tampak samping (lapisan kelihatan jelas), cahaya natural dekat
jendela pagi, alas kayu polos
Hashtag: #kuelapislegit #kuerumahanbekasi #oleholehbekasi #umkmbekasi #kuearisan
CTA: Chat WA untuk pesan/tanya porsi arisan

---

## Selasa 06 Okt 2026 — TikTok/Video pendek
Pilar: Proses produksi (di balik layar)  |  Momen: -  |  Jam disarankan: 12.00-13.00 & 19.00-22.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Ini alasan brownies kukusnya selalu ludes duluan"
Caption: Proses ngukus brownies cokelat sampai bener-bener lumer di dalam. No ribet, langsung dari dapur
rumah ke tanganmu. Yuk cobain! 🍫
Naskah video ±30 detik:
| Detik | Adegan | Teks di layar | VO/Narasi |
|---|---|---|---|
| 0-3 | Close-up adonan brownies dituang ke loyang | "Ini alasan brownies ini ludes duluan" | "Ini alasan brownies kukusnya selalu ludes duluan" |
| 3-15 | Loyang masuk kukusan, uap mengepul, timer berjalan | "Dikukus ±40 menit, dicek manual" | "Kita kukus pelan, dicek manual biar matangnya pas, gak keras di luar" |
| 15-25 | Brownies dipotong, tekstur lumer/fudgy kelihatan | "Tekstur fudgy, bukan kering" | "Lihat sendiri teksturnya, lumer tapi gak lembek" |
| 25-30 | Brownies dikemas rapi + tempel logo | "Order: WA 0812-0000-1234" | "Order lewat WA ya, Kak, kita kirim area Bekasi" |
Brief foto/video: rekam dari atas (top-down) saat menuang adonan, lalu angle depan saat kukusan
mengepul, terakhir close-up potongan brownies
Hashtag: #brownieskukus #kuerumahan #jajanbekasi #dibalikdapur
CTA: Order lewat WA, area kirim Bekasi

---

## Rabu 07 Okt 2026 — Instagram Story
Pilar: Interaksi/polling  |  Momen: -  |  Jam disarankan: 11.00-13.00 & 19.00-21.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Nastar toples atau brownies kukus buat cemilan sore ini?"
Caption: Poll: "Nastar toples 🫙 vs Brownies kukus 🍫 — kamu Team mana?" (stiker poll IG Story)
Naskah video: - (format foto/Story, tidak perlu naskah)
Brief foto/video: dua produk berdampingan di meja yang sama, pencahayaan sama rata, kasih ruang kosong
di tengah untuk stiker poll
Hashtag: (Story tidak perlu hashtag banyak, cukup 1-2 kalau mau) #kuerumahanbekasi
CTA: Vote di poll, lanjut DM kalau mau pesan

---

## Kamis 08 Okt 2026 — Instagram Feed/Foto
Pilar: Testimoni/kepuasan pelanggan  |  Momen: -  |  Jam disarankan: 11.00 & 19.30 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Kata Kak Rina, pelanggan langganan arisan RT-nya:"
Caption: "Kak Rina" (pelanggan, dengan izin) cerita: kue lapis legitnya jadi andalan tiap arisan RT-nya
sejak setahun lalu — katanya lapisannya "gak pernah gagal, selalu lembut". Terima kasih ya, Kak! 🙏
Pesan buat arisanmu juga? WA aja.
Naskah video: - (format foto, tidak perlu naskah)
Brief foto/video: foto kue di meja arisan/acara (kalau ada dokumentasi dari pelanggan, minta izin
pakai); kalau tidak ada, foto produk biasa + teks testimoni sebagai overlay
Hashtag: #testimonijujur #kuearisan #kuelapislegit #umkmbekasi
CTA: WA untuk pesan buat acara arisan
Catatan kepatuhan: nama pelanggan & cerita di atas FIKTIF untuk contoh ini — saat dipakai sungguhan,
WAJIB testimoni asli dengan izin tertulis/chat dari pelanggan (lihat `references/aturan-iklan.md`).

---

## Jumat 09 Okt 2026 — TikTok/Video pendek
Pilar: Edukasi ringan  |  Momen: -  |  Jam disarankan: 12.00-13.00 & 19.00-22.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "3 cara simpan kue lapis legit biar tahan seminggu"
Caption: Tips simpan kue lapis legit di rumah biar tetap lembut sampai seminggu. Save postingan ini! 📌
Naskah video ±30 detik:
| Detik | Adegan | Teks di layar | VO/Narasi |
|---|---|---|---|
| 0-3 | Kue lapis legit utuh di piring | "3 cara simpan kue lapis legit" | "3 cara simpan kue lapis legit biar tahan seminggu" |
| 3-12 | Kue dibungkus plastik wrap rapat | "1. Bungkus rapat plastic wrap" | "Pertama, bungkus rapat pakai plastic wrap, jangan biarkan kena udara" |
| 12-21 | Kue dimasukkan wadah kedap udara di kulkas | "2. Simpan di wadah kedap udara, kulkas" | "Kedua, taruh di wadah kedap udara, simpan kulkas" |
| 21-30 | Kue dipotong siap disajikan + logo toko | "3. Diamkan suhu ruang 10 menit sebelum makan" | "Ketiga, sebelum disajikan, diemin dulu di suhu ruang. Mau order? WA di bio ya" |
Brief foto/video: rekam proses membungkus & menyimpan di kulkas rumah, pencahayaan dapur terang
Hashtag: #tipskue #kuelapislegit #kuerumahan #dapurbekasi
CTA: Save video ini & order lewat WA di bio

---

## Sabtu 10 Okt 2026 — Instagram Feed + TikTok/Video pendek (Promo)
Pilar: Promo tanggal kembar  |  Momen: Tanggal kembar 10.10  |  Jam disarankan: 10.00-12.00 (akhir pekan bergeser lebih siang, perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Cuma hari ini, 10.10 — beli 1 lapis legit gratis 3 nastar"
Caption:
Spesial 10.10! Beli 1 kue lapis legit ukuran standar, langsung dapat bonus 3 pcs nastar toples. Berlaku
HANYA hari ini, 10 Oktober 2026, selama stok harian masih ada (kami produksi terbatas per hari, bukan
kelangkaan buatan — kalau habis, bisa pre-order untuk besok).
Order: WA 0812-0000-1234 / DM Instagram, sebut kode "1010" ya, Kak.
Naskah video ±30 detik:
| Detik | Adegan | Teks di layar | VO/Narasi |
|---|---|---|---|
| 0-3 | Angka "10.10" muncul besar di layar | "10.10 SPESIAL HARI INI" | "Cuma hari ini, tanggal kembar 10.10" |
| 3-15 | Kue lapis legit + toples nastar disandingkan | "Beli 1 lapis legit + gratis 3 nastar" | "Beli 1 kue lapis legit, langsung dapat bonus 3 nastar toples" |
| 15-25 | Kemasan dengan stiker "kode 1010" | "Sebut kode 1010 saat order" | "Order lewat WA, sebut kode 1010 biar dapat bonusnya" |
| 25-30 | Logo toko + nomor WA | "WA 0812-0000-1234, stok harian terbatas" | "Buruan chat, stok harian kami memang terbatas karena bikin manual tiap hari" |
Brief foto/video: kue lapis legit + toples nastar bersanding, tambahkan properti angka "10.10" (kertas
tulisan tangan atau print sederhana), cahaya terang
Hashtag: #promo1010 #kuelapislegit #kuerumahanbekasi #umkmbekasi #nastartoples
CTA: WA sebut kode "1010", stok harian terbatas (bukan kelangkaan palsu — memang produksi harian manual)

---

📥 Arsip disimpan: konten/minggu-2026-W41.md
📝 Asumsi: tidak ada asumsi tambahan — semua kolom profil dijawab pengguna di wawancara giliran 2.
⚠️ Ingat: paket ini belum terposting — jadwalkan sendiri lewat Meta Business Suite/TikTok Studio (lihat
"Cara jadwalkan sendiri" di file arsip), atau aktifkan pengingat harian OpenClaw.

Mau aku bantu sekalian: (a) pasang pengingat otomatis Jumat sore + pengingat harian lewat OpenClaw, (b)
buat brief foto detail produk (`foto-produk-brief`), atau (c) buatkan naskah live jualan untuk hari
Sabtu promo 10.10 (`naskah-live-jualan`)?
```

## Catatan penguji
**Bagus:**
- Perintah `nomor_minggu.py --mulai 2026-10-05` benar-benar dijalankan; label minggu `2026-W41` dan
  momen "Tanggal kembar 10.10" di hari Sabtu **cocok persis** dengan output script (diverifikasi ulang
  manual dengan `datetime.isocalendar()`, lihat `HASIL-UJI.md`).
- Promo 10.10 hanya 1 dari 6 hari (~17%), sesuai target 20-30% maksimal, dan hari-hari lain bervariasi
  pilar (edukasi produk, di balik layar, interaksi, testimoni, tips) — tidak ada dua hari yang isinya
  mirip.
- Hook spesifik ke produk (bukan "Halo semua!" generik), sesuai `references/gaya-caption.md`.
- Klaim "stok terbatas" di hari promo diberi klarifikasi eksplisit "bukan kelangkaan buatan" sesuai
  `references/aturan-iklan.md` — ini detail bagus yang menunjukkan skill benar-benar menerapkan aturan,
  bukan cuma template kosong.
- Testimoni palsu (Kamis) diberi **catatan kepatuhan eksplisit** bahwa nama/cerita di contoh ini fiktif
  dan pemakaian asli wajib izin — ini inisiatif baik dari penguji mengikuti aturan data pribadi di
  `references/aturan-iklan.md`, tapi **SKILL.md sendiri tidak secara eksplisit mengingatkan agent untuk
  menandai testimoni contoh sebagai fiktif saat mendemokan** — lihat catatan cacat di `HASIL-UJI.md`.
- Naskah video 30 detik format tabel detik-adegan-teks-VO bisa langsung dipakai untuk syuting, tidak
  perlu diterjemahkan lagi oleh pengguna awam.

**Kurang / catatan:**
- Skill tidak menanyakan preferensi "berapa hari" secara eksplisit di daftar 5 pertanyaan wawancara —
  agent (mengikuti SKILL.md §Langkah kerja 3) memutuskan sendiri 6 hari default karena pengguna tidak
  menyebutkan kapasitas produksi selain jumlah video. Ini sesuai default di SKILL.md, tapi pembeli awam
  yang tidak baca SKILL.md mungkin kaget kenapa dapat 6 hari padahal tidak diminta — sebaiknya agent
  menyebutkan secara eksplisit "aku buatkan 6 hari (Senin-Sabtu) sesuai default, bilang kalau mau lebih
  sedikit/banyak" di awal output. Ini **cacat ringan** (bukan salah, tapi kurang transparan untuk awam).
- Jam posting Story (Rabu) memakai acuan jam Instagram Feed/Reels karena `gaya-caption.md` tidak
  punya baris jam khusus untuk Instagram Story — agent menaksir sendiri. Lihat cacat di `HASIL-UJI.md`.
