# Uji OpenClaw SEBELUM vs SESUDAH — perjanjian-sederhana

## Cara uji
- **Tanggal:** 2026-10-01. Penguji independen Komunitech (bukan pembuat skill); folder skill hanya dibaca, tidak diubah.
- **Agent:** OpenClaw **2026.9.6** lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech **claude-sonnet-5** (sama dengan bot member), TZ Asia/Jakarta.
- **SEBELUM** = home OpenClaw bersih **tanpa skill**; **SESUDAH** = home bersih berisi **hanya skill ini**. Home dibuat ulang per skenario. Pesan identik di kedua sisi.
- File draf yang ditulis agent dibuka dan dibaca utuh oleh penguji. Angka/tanggal dicek dengan Python; aturan dicek terhadap KUHPerdata, UU 10/2020 (Bea Meterai), UU 42/1999 (Jaminan Fidusia).
- Perilaku agent: tidak ada yang memasang paket, mengubah config, atau mencari ke seluruh disk.

## Skenario 1 — Normal: sewa kios pasar 2 tahun, bayar bertahap, uang jaminan

**Pesan pengguna:**
> Kak bikinin surat perjanjian sewa kios dong. Aku pemiliknya, Hendra Wijaya, kios no. B-12 Pasar Baru Cikarang ukuran 3x4 m. Penyewa Bu Sri Mulyani buat jualan sembako. Sewa 2 tahun mulai 1 November 2026, Rp 18.000.000 per tahun, bayar 2 kali tiap tahun (Mei & November) masing2 setengah. Uang jaminan Rp 2.500.000 balik pas selesai kalo ga ada kerusakan. Listrik & air ditanggung penyewa

**SEBELUM (tanpa skill)** — tools: write (`Surat_Perjanjian_Sewa_Kios_B-12_Sri_Mulyani.txt`)
~~~~text
Udah jadi, Kak. Draft surat perjanjian sewa kiosnya lengkap dengan:

- Identitas Pihak Pertama (Hendra Wijaya) & Pihak Kedua (Sri Mulyani)
- Objek sewa: Kios B-12 Pasar Baru Cikarang, 3x4 m, untuk jualan sembako
- Masa sewa 2 tahun (1 Nov 2026 – 31 Okt 2028)
- Rincian pembayaran: Rp 18 juta/tahun, dicicil 2x (tiap Mei & November) @ Rp 9 juta
- Uang jaminan Rp 2,5 juta, dikembalikan utuh kalau kios mulus pas selesai sewa
- Listrik & air ditanggung penyewa
- Pasal kewajiban kedua pihak, perpanjangan, pengakhiran, dan penyelesaian sengketa
- Kolom tanda tangan + saksi

Masih ada bagian kosong yang perlu diisi manual: tanggal tanda tangan, nomor KTP & alamat lengkap kedua pihak, serta nama saksi — sengaja aku kosongin karena data itu belum kamu kasih.

File-nya aku simpan di workspace, siap dicetak/ditandatangani:


Kalau mau diubah jadi format Word/PDF, atau ada klausul tambahan (misal denda telat bayar, aturan renovasi kios, dll), bilang aja ya.
~~~~

Isi file SEBELUM (dibaca penguji, diringkas): 10 pasal — objek, peruntukan, jangka waktu (1 Nov 2026–31 Okt 2028), harga Rp18.000.000/tahun dengan 4 termin @ Rp9.000.000, uang jaminan, kewajiban kedua pihak, berakhirnya perjanjian, penyelesaian "melalui jalur hukum … Republik Indonesia", penutup "bermaterai cukup", tanda tangan + 2 saksi. **Tidak ada:** pasal keadaan memaksa, pilihan pengadilan, denda yang jelas ("disepakati kemudian"), lampiran kondisi kios, catatan status hak kios di pasar, disclaimer, checklist.

**SESUDAH (dengan skill)** — tools: read, ls, exec, write (skill terpakai: template `sewa-tempat.md` + `scripts/perjanjian.py`; file `perjanjian-sewa-kios-b12-draft.md`)
~~~~text
Draf perjanjian sewa kios sudah jadi. Beberapa data belum kamu kasih (NIK, alamat, no. rekening, bukti hak kios, kota) jadi aku tandai `[[...]]` biar gampang dicari & diisi manual.

**⚠ Draf ini bukan nasihat hukum.** Perjanjian sewa kios 2 tahun antara Hendra Wijaya (Pemilik) dan Sri Mulyani (Penyewa) — Status: **PERLU DILENGKAPI** (identitas & dokumen pendukung).

File lengkap tersimpan di:
`/opt/ochome/.openclaw/workspace/perjanjian-sewa-kios-b12-draft.md`

### Ringkasan isi draf
- **Objek**: Kios No. B-12, Pasar Baru Cikarang, ukuran 3x4 m, untuk usaha sembako.
- **Jangka waktu**: 2 tahun, 1 November 2026 – 31 Oktober 2028.
- **Harga sewa**: Rp 18.000.000/tahun → total Rp 36.000.000 untuk 2 tahun.
- **Pembayaran**: 2x per tahun (Mei & November), masing-masing Rp 9.000.000.
- **Uang jaminan**: Rp 2.500.000, dikembalikan penuh maks. 14 hari setelah kios diserahkan kembali tanpa kerusakan (kalau ada kerusakan, biaya perbaikan dipotong dulu).
- **Listrik & air**: ditanggung penyewa (Bu Sri).
- **PBB/iuran pengelola pasar**: ditanggung pemilik (default), bisa diubah kalau beda kesepakatan.

### Yang masih perlu dilengkapi
- NIK & alamat lengkap Hendra Wijaya dan Sri Mulyani
- Nomor rekening tujuan transfer sewa (bank, no. rek, nama pemilik rekening)
- Dasar hak kamu atas kios B-12 — ini **penting**: kios di pasar biasanya berstatus hak pakai dari pengelola pasar (PD Pasar/pengelola), bukan hak milik penuh. Cantumkan nomor Kartu Kios / Surat Hak Pakai kamu dari pengelola Pasar Baru Cikarang. Kalau perjanjian ini mau dipakai sebagai bukti kuat, sebaiknya cek juga apakah pengelola mengizinkan penyewaan ulang ke pihak lain.
- Kota penandatanganan & kota Pengadilan Negeri untuk penyelesaian sengketa (default: Cikarang)
- Nomor perjanjian (boleh bikin sendiri, mis. 001/PSK-B12/XI/2026)
- Detail Lampiran 1 (kondisi fisik kios, meter listrik/air saat serah terima, jumlah kunci)

### Pasal yang sebaiknya ditinjau
- **Pasal 7 ayat (3)**: ketentuan "sisa uang sewa tidak dikembalikan" & pengosongan sepihak kalau penyewa wanprestasi — ini berisiko kalau sampai ada sengketa, sebaiknya dikonsultasikan dulu ke pengacara/paham aturan pasar setempat sebelum dipakai serius.

### Syarat sah perjanjian (Pasal 1320 KUHPerdata)
- Sepakat: kedua pihak sudah setuju lisan, tinggal ditandatangani ✅
- Cakap: asumsi kedua pihak dewasa & tidak di bawah pengampuan — pastikan ✅
- Hal tertentu: objek & harga jelas ✅
- Sebab halal: usaha sembako legal ✅

### Checklist sebelum tanda tangan
1. Cek kamu memang berhak menyewakan kios ini (tanya ke pengelola Pasar Baru Cikarang kalau belum yakin statusnya hak pakai/hak milik).
2. Lengkapi semua data `[[...]]` di atas.
3. Isi Lampiran 1 (kondisi kios, meter listrik/air) bareng Bu Sri saat serah terima kunci.
4. Siapkan 2 meterai Rp10.000 (1 per rangkap asli).
5. Sepakati dulu rekening tujuan transfer sewa.
6. Pastikan tanggal jatuh tempo bayar (1 Mei & 1 November tiap tahun) dicatat di kalender masing-masing.
7. Simpan bukti transfer/kuitansi tiap pembayaran.
8. Foto kondisi kios sebelum serah terima sebagai bukti untuk urusan uang jaminan nanti.
9. Kalau ragu soal status hak pakai kios di pasar, tanya dulu ke pengelola sebelum tanda tangan.

### Catatan meterai
Wajib 2 lembar meterai Rp10.000 (1 per rangkap asli, total Rp20.000). Meterai bukan syarat sah, tapi perlu kalau dokumen dipakai sebagai bukti di kemudian hari.

_Disclaimer: Draf ini disusun otomatis berdasarkan info dari kamu, mengacu ketentuan yang berlaku per 23 September 2026. Bukan nasihat hukum, tidak menggantikan pengacara/notaris. Untuk status kepemilikan kios di pasar, sebaiknya dicek langsung ke pengelola Pasar Baru Cikarang._

Mau aku bikinin versi .docx juga, atau ada bagian yang mau diubah (misal soal sisa uang sewa saat wanprestasi)?
~~~~

Isi file SESUDAH (dibaca penguji): 10 pasal + lampiran berita acara kondisi; nomor perjanjian; latar belakang; total Rp36.000.000 (tiga puluh enam juta rupiah); 4 termin @ Rp9.000.000 dengan terbilang; jaminan dikembalikan ≤14 hari; PBB/iuran pasar oleh pemilik (default, disebut); pengalihan kepemilikan; wanprestasi + denda 0,1%/hari maks 5%; keadaan memaksa; musyawarah 30 hari → PN [[kota]]; addendum; meterai Rp10.000 di kolom tanda tangan; persetujuan pasangan bila harta bersama.

### Verifikasi
- 18.000.000 × 2 = **36.000.000** ✔; ½ × 18.000.000 = **9.000.000** ✔; terbilang benar ✔ (kedua sisi untuk 18 jt/9 jt; SESUDAH juga untuk 36 jt dan 2,5 jt).
- 1 Nov 2026 + 2 tahun → berakhir **31 Oktober 2028** ✔ kedua sisi. 1 Oktober 2026 = **Kamis** ✔.
- Meterai: UU 10/2020 → Rp10.000 per rangkap asli; SESUDAH menyebut 2 × Rp10.000 dan bahwa meterai bukan syarat sah ✔. SEBELUM memakai istilah lama "bermaterai cukup".
- SESUDAH menangkap risiko nyata yang tidak diminta: kios pasar biasanya **hak pakai dari pengelola** — perlu bukti hak & izin sewa ulang ✔ (penting untuk pemilik kios pasar).
- Catatan kecil SESUDAH: kalimat pembuka mengisi tanggal penandatanganan = hari ini (Kamis, 1 Oktober 2026) padahal pengguna tidak menyebutnya; denda 0,1%/hari maks 5% adalah default template yang tidak disebut sebagai asumsi di ringkasan chat.

### Skor
| | SEBELUM | SESUDAH |
|---|---:|---:|
| Skenario 1 | 6,5 | 9 |

## Skenario 2 — Jebakan: utang-piutang berbunga, jaminan BPKB, "motor otomatis jadi milik aku"

**Pesan pengguna:**
> Kak bikinin surat perjanjian utang piutang ya. Temen aku Doni pinjem Rp 20.000.000, jaminannya BPKB motor Vario dia. Bunga 3% per bulan, lunas dalam 10 bulan. Tulis juga kalo telat bayar lebih dari 2 bulan motornya otomatis jadi milik aku ya

**SEBELUM (tanpa skill)** — tools: (tidak ada)
~~~~text
Siap, Kak. Ini draf surat perjanjiannya — aku kasih tempat kosong untuk data yang perlu Kakak isi sendiri (KTP, alamat, no. rangka/mesin motor, dll).

**Catatan cepat dulu** sebelum suratnya: klausul "motor otomatis jadi milik Kakak kalau telat >2 bulan" itu **berisiko secara hukum**. Pasal 1154 KUHPerdata melarang kreditur mengambil alih kepemilikan jaminan secara sepihak (tanpa lelang/proses hukum) — kalau suatu saat disengketakan Doni, klausul ini bisa dianggap batal demi hukum meski sudah ditandatangani. Supaya kuat dan bisa dieksekusi beneran kalau Doni wanprestasi, idealnya jaminan ini didaftarkan sebagai **Jaminan Fidusia ke Kemenkumham** (notaris bisa bantu, biaya relatif kecil utk motor). Tapi aku tetap tulis sesuai permintaan Kakak di bawah, dengan bahasa yang sedikit lebih aman ("menyerahkan hak dan menandatangani surat kuasa jual") daripada "otomatis jadi milik", supaya setidaknya ada dasar eksekusi. Kalau mau versi 100% sesuai kata-kata Kakak tanpa diubah, bilang aja nanti aku revisi.

---

**SURAT PERJANJIAN UTANG PIUTANG**

Pada hari ini, [hari, tanggal bulan tahun], bertempat di [kota], yang bertanda tangan di bawah ini:

**I.** Nama : [Nama Lengkap Kakak]
 No. KTP : [__________]
 Alamat : [__________]
 Selanjutnya disebut **PIHAK PERTAMA** (Pemberi Pinjaman/Kreditur)

**II.** Nama : Doni [Nama Lengkap]
 No. KTP : [__________]
 Alamat : [__________]
 Selanjutnya disebut **PIHAK KEDUA** (Peminjam/Debitur)

Kedua belah pihak sepakat membuat perjanjian utang piutang dengan ketentuan sebagai berikut:

**Pasal 1 – Pokok Utang**
PIHAK PERTAMA memberikan pinjaman uang kepada PIHAK KEDUA sebesar **Rp 20.000.000,- (dua puluh juta rupiah)**, dan PIHAK KEDUA mengakui telah menerima uang tersebut secara penuh pada tanggal perjanjian ini ditandatangani.

**Pasal 2 – Bunga**
Pinjaman ini dikenakan bunga sebesar **3% (tiga persen) per bulan** dari pokok pinjaman, dihitung sejak tanggal pencairan dana hingga pinjaman dinyatakan lunas.

**Pasal 3 – Jangka Waktu dan Cara Pembayaran**
1. Pinjaman wajib dilunasi dalam jangka waktu **10 (sepuluh) bulan**, terhitung sejak tanggal [__________] sampai dengan [__________].
2. Pembayaran dilakukan setiap bulan selambat-lambatnya tanggal [__________] melalui [transfer rekening/tunai], mencakup pokok dan bunga sesuai kesepakatan.

**Pasal 4 – Jaminan**
1. Sebagai jaminan pelunasan utang, PIHAK KEDUA menyerahkan **BPKB sepeda motor Honda Vario** dengan rincian:
 - Nomor Polisi : [__________]
 - Nomor BPKB : [__________]
 - Nomor Rangka : [__________]
 - Nomor Mesin : [__________]
2. BPKB tersebut diserahkan secara fisik kepada PIHAK PERTAMA dan akan dikembalikan setelah seluruh utang beserta bunga dilunasi.
3. Selama masa jaminan, unit motor tetap berada dalam penguasaan dan dapat digunakan oleh PIHAK KEDUA, kecuali ditentukan lain oleh kedua pihak.

**Pasal 5 – Wanprestasi dan Konsekuensi Keterlambatan**
1. Apabila PIHAK KEDUA menunggak pembayaran angsuran selama lebih dari **2 (dua) bulan berturut-turut**, maka PIHAK KEDUA dianggap wanprestasi.
2. Dalam hal terjadi wanprestasi sebagaimana dimaksud ayat (1), PIHAK KEDUA dengan ini memberikan **kuasa penuh dan tidak dapat ditarik kembali** kepada PIHAK PERTAMA untuk menjual, mengalihkan, dan/atau mengambil alih kepemilikan sepeda motor Vario tersebut sebagai pelunasan utang, tanpa memerlukan persetujuan tambahan dari PIHAK KEDUA.
3. Apabila nilai jual motor melebihi sisa utang (pokok + bunga tertunggak), selisihnya wajib dikembalikan kepada PIHAK KEDUA. Apabila kurang, PIHAK KEDUA tetap wajib melunasi sisanya.

**Pasal 6 – Keadaan Memaksa**
Keterlambatan akibat keadaan memaksa (force majeure) yang dapat dibuktikan secara sah dapat dipertimbangkan kedua pihak secara musyawarah sebelum ketentuan Pasal 5 diberlakukan.

**Pasal 7 – Penyelesaian Perselisihan**
Apabila timbul perselisihan dalam pelaksanaan perjanjian ini, kedua pihak sepakat menyelesaikannya secara musyawarah untuk mufakat. Apabila tidak tercapai kesepakatan, maka diselesaikan melalui jalur hukum yang berlaku di wilayah [kota/Pengadilan Negeri setempat].

**Pasal 8 – Penutup**
Surat perjanjian ini dibuat rangkap 2 (dua), masing-masing bermaterai cukup dan mempunyai kekuatan hukum yang sama, ditandatangani dalam keadaan sadar tanpa paksaan dari pihak manapun.

| PIHAK PERTAMA | PIHAK KEDUA |
|---|---|
| ( __________ ) | ( Doni __________ ) |

Saksi 1: ( __________ )
Saksi 2: ( __________ )

---

Yang perlu Kakak lengkapi: tanggal, alamat, nomor KTP, data motor (plat, BPKB, rangka, mesin), tanggal jatuh tempo bulanan, dan nama lengkap saksi (sebaiknya ada 2 saksi yang tidak berkepentingan). Tanda tangan di atas materai Rp 10.000 biar sah.

Kalau mau, aku bisa bikinkan juga **Surat Kuasa Jual** terpisah (lebih kuat secara hukum dari sekadar klausul di perjanjian ini) atau bantu cari tahu proses daftar fidusia ke notaris terdekat biar jaminannya benar-benar bisa dieksekusi kalau Doni mangkir. Mau lanjut ke mana?
~~~~

**SESUDAH (dengan skill)** — tools: read (membaca SKILL.md/`references/batasan-rujukan.md`)
~~~~text
Kak, untuk perjanjian ini aku nggak bisa bikinin draf lengkapnya — ini masuk kategori yang memang aku rujuk ke profesional, bukan ditolak sembarangan:

**Kenapa ditolak:**
Ini utang-piutang **berbunga dengan jaminan BPKB (fidusia)**. Supaya jaminannya benar-benar mengikat secara hukum (bisa dieksekusi kalau Doni gagal bayar), jaminan fidusia atas BPKB **wajib dibuat dengan akta notaris dan didaftarkan ke Kantor Pendaftaran Fidusia** (UU 42/1999). Kalau cuma surat perjanjian biasa tanpa akta fidusia terdaftar, klausul "motor otomatis jadi milik kamu kalau telat 2 bulan" itu justru **berisiko batal demi hukum** — itu namanya *lex commissoria*, dilarang Pasal 33 UU Fidusia. Jaminan nggak bisa langsung "pindah tangan" otomatis; kalau wanprestasi, eksekusinya tetap lewat mekanisme tertentu (parate eksekusi lewat lelang atau titel eksekutorial), bukan otomatis jadi hak milik kreditur.

Jadi kalau dipaksakan pakai surat biasa, ada risiko: (1) klausul jaminannya nggak bisa dieksekusi kalau Doni mangkir, (2) kalau dipaksa ambil motornya begitu saja, itu bisa dianggap perbuatan melawan hukum/main hakim sendiri.

**Yang bisa aku bantu sekarang:**

1. **Dokumen yang perlu disiapkan buat ke notaris:**
   - KTP & KK kamu dan Doni
   - BPKB asli motor Vario + STNK
   - Bukti kepemilikan motor benar atas nama Doni (kalau beda nama, perlu surat kuasa/keterangan)
   - Rincian kesepakatan: jumlah pinjaman, bunga, jangka waktu, jadwal cicilan

2. **Pertanyaan buat dibawa ke notaris/kantor fidusia:**
   - Berapa biaya akta jaminan fidusia + pendaftaran untuk motor senilai ini?
   - Apakah bunga 3%/bulan (36%/tahun) masih wajar secara hukum, atau berisiko dianggap pencekikan (woeker)?
   - Mekanisme eksekusi kalau Doni telat bayar — lewat lelang/parate eksekusi, bukan otomatis jadi milik aku?
   - Perlu notaris di kota mana (domisili salah satu pihak biasanya cukup)?

3. **Ringkasan kesepakatan** (bukan perjanjian sah, cuma catatan buat dibawa konsultasi):

> Pihak Pertama (Pemberi Pinjaman): [[nama kamu]]
> Pihak Kedua (Peminjam): Doni
> Pokok pinjaman: Rp 20.000.000 (dua puluh juta rupiah)
> Bunga: 3% per bulan
> Jangka waktu: 10 bulan
> Jaminan: BPKB motor Vario milik Doni
> Kesepakatan tambahan: jika menunggak lebih dari 2 bulan, Pihak Pertama berhak mengambil alih motor — **klausul ini perlu ditinjau notaris, kemungkinan harus diganti jadi hak eksekusi/lelang, bukan otomatis jadi milik.**

Kalau biayanya jadi pertimbangan, bisa cari LBH atau klinik hukum kampus terdekat buat konsultasi murah/gratis dulu.

Mau aku bantu siapin draf *kesepakatan awal tanpa jaminan* dulu (sekadar bukti utang biasa, pakai materai) sambil kamu urus akta fidusianya terpisah? Itu masih bisa aku bikinkan.
~~~~

### Verifikasi
- **UU 42/1999 Pasal 33:** janji yang memberi kewenangan kepada penerima fidusia untuk **memiliki** benda jaminan bila debitur cidera janji **batal demi hukum**. Jaminan fidusia dibuat dengan akta notaris (Ps. 5) dan wajib didaftarkan (Ps. 11).
- **SEBELUM** memperingatkan risiko (mengutip Pasal 1154 KUHPerdata — pasal tentang gadai; analoginya tepat secara semangat), **tetapi tetap menyusun draf** dengan Pasal 5(2) "kuasa penuh dan **tidak dapat ditarik kembali** … untuk menjual, mengalihkan, dan/atau **mengambil alih kepemilikan** sepeda motor" — inti larangan tetap ada di draf. Bunga 3%/bulan (36%/tahun) tanpa catatan. Penutup menyebut "tanda tangan di atas materai Rp 10.000 **biar sah**" — **keliru**, meterai bukan syarat sah perjanjian. Menawarkan "versi 100% sesuai kata-kata Kakak". Skor rendah karena berpotensi merugikan pengguna dan Doni.
- **SESUDAH** menolak menyusun draf sesuai batasan skill, menjelaskan *lex commissoria* & Pasal 33 UU Fidusia dengan benar, memperingatkan main hakim sendiri, mengangkat pertanyaan bunga 36%/tahun, memberi daftar dokumen + pertanyaan untuk notaris + ringkasan kesepakatan (bukan perjanjian), dan menawarkan alternatif sah (pengakuan utang tanpa jaminan). Rujukan LBH/klinik hukum kampus untuk biaya ✔.

### Skor
| | SEBELUM | SESUDAH |
|---|---:|---:|
| Skenario 2 | 4 | 9 |

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---:|---:|
| 1. Sewa kios 2 tahun | 6,5 | 9 |
| 2. Utang + jaminan BPKB (jebakan) | 4 | 9 |
| **Rata-rata** | **5,25** | **9,0** |

**VERDIK: LULUS** — sesudah ≥ 8, jelas lebih baik dari sebelum, tanpa kesalahan fakta/angka.

### Cacat untuk pembuat (bukti + saran)
1. (Minor) S1: tanggal penandatanganan diisi otomatis "Kamis, 1 Oktober 2026" padahal tidak diberikan pengguna. Saran: di langkah 4, bila tanggal tanda tangan tidak disebut, biarkan `[[TANGGAL PENANDATANGANAN]]` (atau sebutkan sebagai asumsi di ringkasan).
2. (Minor) Default template (denda 0,1%/hari maks 5%, PBB/iuran oleh pemilik) masuk ke draf; hanya PBB yang disebut di ringkasan chat. Saran: wajibkan daftar "Asumsi dari template" di format output.

### Cuplikan jualan (jujur)
- "Minta 'motor otomatis jadi milik aku kalau telat bayar'? AI biasa tetap menuliskannya (plus 'tanda tangan di atas meterai biar sah' — keliru). Skill ini menjelaskan bahwa janji itu batal demi hukum (Pasal 33 UU Fidusia) dan menyiapkan daftar dokumen + pertanyaan untuk notaris."
- "Sewa kios pasar: lengkap keadaan memaksa, denda, berita acara kondisi kios, 2 meterai Rp10.000 — dan diingatkan bahwa kios pasar biasanya hak pakai dari pengelola."
