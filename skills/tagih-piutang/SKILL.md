---
name: tagih-piutang
description: Menyusun pesan penagihan piutang bertahap (WA/email/surat): pengingat sebelum jatuh tempo, hari H, lewat 7/14/30 hari, sampai surat teguran resmi (somasi), sopan tapi tegas tanpa ancaman ilegal atau mempermalukan; script menghitung hari terlambat, sisa, denda sesuai kesepakatan tertulis, dan umur piutang dari CSV. Gunakan saat pengguna minta nagih utang pelanggan, invoice belum dibayar, telat bayar, surat teguran pembayaran, debt collection, payment reminder, overdue invoice. Bukan untuk membuat invoice (buat-invoice) atau follow-up calon pembeli.
---

# Tagih Piutang

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

> **Bahasa ke pengguna (wajib):** pengguna umumnya awam teknologi. Jangan pernah menyebut kata *script*, *skill*, *file*, *folder*, *path*, *JSON*, *parameter*, *tahap kode*, atau nama berkas (mis. `hitung_telat.py`) dalam jawaban; ceritakan hasilnya dengan bahasa sehari-hari ("saya hitung", "dari daftar Anda", "ada satu nota yang sudah lunas"). Sapa pengguna dengan "Anda" atau cerminkan gayanya (aku/kamu); **jangan memakai sapaan bergender atau gaul** ("Ibu", "Bapak", "Kak", "Agan", "Bro") untuk pengguna. Untuk debitur di dalam pesan tagihan: pakai nama dan sapaan persis seperti yang diberikan pengguna ("Pak Hendra", "Bu Lina"); bila tidak diberi, tulis netral "Bapak/Ibu [Nama]" (jangan menebak gender dari nama).

## Tujuan
Membantu pemilik usaha menagih pembayaran yang tertunda dengan urutan pesan yang makin tegas tapi tetap menjaga hubungan dan tetap di koridor hukum. Angka (hari terlambat, sisa, denda) dihitung script, sehingga pesan tidak salah nominal.

## Kapan digunakan
- "Invoice ke CV Sinar Abadi 12,5 juta udah lewat sebulan belum dibayar. Bikinin pesan tagihan."
- "Ingetin pelanggan langganan katering yang jatuh temponya Jumat."
- "Buat surat teguran resmi untuk toko yang nunggak 3 bulan."
- "Ini daftar piutangku (CSV), mana yang harus ditagih duluan?"

## Kapan TIDAK digunakan
- Membuat invoice/tagihan baru → `buat-invoice`.
- Calon pembeli belum membeli → `follow-up-prospek`.
- Menagih utang pribadi antar-teman/keluarga dengan emosi tinggi: boleh dibantu dengan nada kekeluargaan, tanpa format surat resmi.
- Pinjaman uang berbunga antar-perorangan: tagih pokoknya saja; bunga/denda tanpa perjanjian tertulis jangan dihitung; sarankan advokat/LBH bila bersengketa.
- Penagihan atas nama lembaga keuangan/pinjol/leasing (tunduk aturan OJK khusus), penagihan ke konsumen dengan jaminan fidusia, gugatan, atau pailit → jelaskan batasan, arahkan ke advokat.
- Permintaan pesan yang mengancam, mempermalukan (sebar di grup/medsos), menghubungi keluarga/atasan debitur untuk menekan, atau memakai kata kasar → **tolak bagian itu secara singkat**: 1–2 kalimat (apa yang tidak dibantu + satu alasan hukum paling kuat, mis. UU ITE 27A/27B dan UU PDP untuk menyebar ke pihak ketiga; "lapor polisi" bukan jalur untuk utang dagang biasa), satu kalimat alternatif sah (surat teguran bertenggat), lalu **langsung kerjakan bagian yang boleh** (ringkasan angka + surat teguran + WA singkat). Jangan berceramah, jangan mengulang alasan di beberapa tempat, tanpa daftar poin risiko panjang (detail ada di `references/regulasi.md` untuk dirimu sendiri). Satu catatan hukum singkat di bagian akhir cukup.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama debitur (pelanggan/perusahaan + PIC) | Ya | `[Nama]` |
| Nominal tagihan & nomor invoice | Ya | — (tanyakan nominal); nomor `[No. Invoice]` |
| Tanggal jatuh tempo | Ya | — (tanyakan) |
| Pembayaran sebagian yang sudah masuk | Tidak | Belum ada |
| Hubungan & nada: pelanggan lama/baru, B2B/perorangan | Tidak | Profesional-sopan |
| Denda/bunga keterlambatan **yang tertulis** di kontrak/invoice/PO | Tidak | **Tanpa denda** |
| Rekening pembayaran | Tidak | `[Bank – No. Rek – a.n.]` |
| Riwayat penagihan sebelumnya & janji bayar debitur | Tidak | Belum pernah ditagih |
| Saluran: WA / email / surat | Tidak | WA untuk tahap 1–4; surat (PDF) + email untuk tahap 5–6 |

**Info wajib kurang → kerjakan bagian yang berguna dulu, baru tanya di akhir.** Jangan membuka dengan daftar pertanyaan. Urutannya: (1) satu kalimat pembuka; (2) langsung berikan templat pesan tagih yang umum untuk tahap pertama (WA ramah, tahap 3–4) dengan isian `[Nama]`, `[No. Invoice]`, `[Nominal]`, `[Tanggal jatuh tempo]`, `[Bank – No. Rek – a.n.]`, plus satu versi lebih tegas bila kata "sudah lama" muncul; (3) di akhir, tanyakan **maksimal 3 pertanyaan singkat** (nama + nominal + jatuh tempo; lalu sudah berapa kali diingatkan) agar pesan bisa dibuat pas, dan sebut bahwa tanpa jawaban pun templat di atas sudah bisa dipakai. Jangan menanyakan hal yang punya default (rekening, denda, saluran). Jika pengguna ingin cepat, pakai default dan tulis "Asumsi" di akhir.

**Sumber data = hanya yang diberikan pengguna.** Jika data tagihan tidak disebut di chat atau di file yang ia tunjuk, **tanyakan** — jangan menjelajah folder, membuka invoice/kuitansi/log lain, grep, atau mencari di memori untuk "menemukan" piutang. File Excel `.xlsx` dibaca langsung oleh script (tanpa paket tambahan); `.xls`/`.ods`/format lain atau file yang gagal dibaca → minta pengguna menyimpannya sebagai **CSV UTF-8**. **Jangan pernah menjalankan `pip install` (openpyxl, pandas, dll.)** atau menginstal apa pun untuk skill ini.

## Langkah kerja
1. **Hitung dengan script.** Script `hitung_telat.py` ada di subfolder `scripts/` di folder yang sama dengan file SKILL.md ini (mis. di OpenClaw: `~/.openclaw/skills/tagih-piutang/scripts/hitung_telat.py`). Pakai path itu langsung — **jangan mencari script atau file data ke seluruh disk** (`find /`, `dir /s`, dsb.); file dari pengguna ada di folder kerja. Windows: `python`/`py`.
   ```bash
   python3 scripts/hitung_telat.py --nominal "Rp 12.500.000" --dibayar "Rp 2.500.000" \
     --jatuh-tempo 2026-08-24 --tanggal 2026-09-23 --sudah-diingatkan 2
   ```
   - `--hubungan dekat` untuk tetangga/kenalan/keluarga/pelanggan perorangan langganan (jeda antartahap 14 hari, bukan 7). Script menulis baris `Jadwal` (tenggat bayar + kapan tahap berikutnya) — **salin kalimat itu apa adanya** ke bagian "Tahap berikutnya"; jangan menghitung tanggal sendiri.
   - `--sudah-diingatkan N` = jumlah pengingat yang **sudah** terkirim (dari "Riwayat penagihan"; default 0). Script memakainya untuk menentukan tahap.
   - Denda **hanya** jika ada kesepakatan tertulis: tambahkan `--denda-persen 0,1 --denda-per hari` (atau `--denda-per bulan`, `--denda-tetap "Rp 100.000"`), `--tenggang 3`, `--denda-maks 5%`, dan `--dasar-denda "Pasal 4 Perjanjian No. ..."`. Jika script menulis PERINGATAN bahwa dasar denda kosong, jangan cantumkan denda di pesan sampai pengguna mengonfirmasi dasarnya.
   - Banyak tagihan: `--file piutang.csv` atau `--file piutang.xlsx` (opsional `--sheet NamaSheet`) → rekap umur piutang, total yang sudah telat, dan urutan prioritas. Nama kolom umum ID/EN dikenali otomatis (mis. `no_faktur`, `nilai_faktur`, `customer`, `due_date`, `amount`, atau kolom `sisa`/`outstanding`); kolom lain (no. WA, tanggal faktur) diabaikan. **Kolom pembayaran** dikenali dari banyak judul ("sdh bayar", "sudah dibayar", "dibayar", "DP", "cicilan", "lunas", "status bayar", dst.; huruf besar/kecil, spasi, garis bawah, aksen tidak berpengaruh) dan otomatis **dikurangkan** dari tagihan; nota yang sudah lunas **tidak** masuk daftar tagih dan total (script menuliskannya di blok "Sudah lunas, TIDAK ditagih" — sebut singkat ke pengguna, mis. "UD Maju Jaya sudah lunas, tidak saya tagih"). Jumlah pengingat bisa terbaca dari kolom keterangan ("sudah WA 2x", "diingatkan 3x"); sebut asumsi itu ke pengguna dan minta koreksi bila keliru. **Baris berawal ⚠️ di output** berarti ada kolom yang mirip kolom pembayaran tetapi tidak terbaca, atau isinya aneh: **sampaikan di awal jawaban dengan bahasa biasa** (mis. "Di daftar Anda ada isian 'sdh transfer' yang belum bisa saya baca sebagai pembayaran, jadi angka di bawah belum mengurangi itu — betulkan judulnya atau beri tahu saya mana yang sudah dibayar") dan **jangan** memakai total itu sebagai final sebelum pengguna mengonfirmasi; jangan menebak sendiri isinya; angka format Indonesia (`Rp 1.500.000`, `2,5jt`) dan tanggal `25/09/2026`/`25 Sep 2026` diterima. Jika script menulis `ERROR: kolom wajib tidak ditemukan`, sampaikan pesan itu ke pengguna (minta ganti judul kolom) — jangan menebak isi kolom. Hanya file yang ditunjuk pengguna. Pakai tabel & total dari output apa adanya (tanpa menyebut asalnya).
   - **Grup/tim:** bila pengguna minta "laporin ke grup/tim", salin **hanya** blok "Ringkasan aman untuk grup" dari output script (jumlah faktur & total telat, tanpa nama pelanggan, nomor invoice, nomor HP, atau sisa per pelanggan; JSON: `ringkasan_grup`). Tabel per pelanggan diberi judul "khusus pemilik/admin keuangan — jangan ditempel ke grup"; jangan menyuruh menyalin tabel/ringkasan lain ke grup. Mode satu tagihan tidak punya versi grup (satu faktur mudah dikenali) — sampaikan ke pemilik saja. Jangan menawarkan jadwal/kirim otomatis ke grup.
   - Script menolak denda > 1% per hari (atau setara per bulan) sebagai kemungkinan salah ketik, serta `--denda-maks` tanpa satuan ≤ 100 atau < Rp 1.000. Tanyakan konfirmasi ke pengguna; tambahkan `--konfirmasi-denda-tinggi` hanya bila pengguna memastikan angka itu memang tertulis di perjanjian.
   - Script keluar dengan kode ≠ 0 dan pesan `ERROR:` bila input salah; perbaiki, jangan menebak.
2. **Tentukan tahap** dari output `tahap` script:

   | Tahap | Waktu | Nada | Isi kunci |
   |---|---|---|---|
   | 1 | H-3 s.d. H-1 | Ramah, informatif | Pengingat jatuh tempo, nominal, rekening |
   | 2 | Hari H | Ramah | "Hari ini jatuh tempo", konfirmasi bila sudah transfer |
   | 3 | Lewat 1–6 hari | Ramah, asumsi baik (mungkin terlewat) | Minta konfirmasi & bukti bila sudah bayar |
   | 4 | Lewat 7–13 hari | Tegas-sopan | Minta **tanggal pasti** pembayaran |
   | 5 | Lewat 14–29 hari | Resmi | Pemberitahuan tertulis, tawaran cicilan/jadwal, sebut denda bila tertulis |
   | 6 | Lewat ≥ 30 hari | Resmi-tegas | **Surat teguran (somasi)** dengan tenggat (mis. 7 hari) & langkah lanjutan yang sah |

   **Pakai riwayat penagihan, bukan umur piutang saja.** Tahap maksimal: belum pernah diingatkan → tahap 4 (tahap 5 bila ≥ 30 hari); 1 pengingat → tahap 5; ≥ 2 pengingat tanpa hasil → boleh tahap 6 (somasi). Jadi invoice 39 hari yang belum pernah ditagih dimulai dari tahap 5 (pemberitahuan resmi yang tetap membuka opsi cicilan), bukan somasi. Naikkan satu tahap bila 7 hari tanpa respons. Script sudah menerapkan aturan ini dan menulis PERINGATAN bila tahap dibatasi.
   Jika debitur sudah memberi janji bayar, sesuaikan: tagih pada tanggal janji, rujuk janjinya secara faktual.
   **Hubungan dekat** (tetangga, kenalan, keluarga, pelanggan perorangan langganan): pakai `--hubungan dekat`; jangan menyarankan naik ke tahap tegas sebelum jeda 14 hari lewat, dan sarankan bicara langsung dulu sebelum pesan tertulis yang lebih tegas atau surat resmi.
3. **Tulis pesan** sesuai tahap (contoh lengkap semua tahap + surat teguran: `references/template-penagihan.md`). Selalu cantumkan: nomor invoice, nominal sisa (dari script), tanggal jatuh tempo, rekening, cara konfirmasi. Tahap 1–3 tambahkan "Abaikan pesan ini jika sudah membayar". **Baris rekening selalu ada di setiap pesan, semua tahap** (isi dari pengguna, atau `[Bank – No. Rek – a.n.]` beserta catatan "isi rekening Anda sebelum kirim"). Bila ada denda dengan batas maksimal, tulis batas itu dalam rupiah di pesan (mis. "maksimal Rp425.000").
   - **Rincian dari pengguna wajib masuk ke pesan.** Bila pengguna memberi rincian (per bulan, per invoice, per barang — mis. "Juli 420rb, Agustus 465rb, September 465rb"), tulis rincian itu sebagai daftar di pesan lalu totalnya, agar debitur bisa mencocokkan.
   - **Saluran tahap 5–6:** bentuk utamanya surat/email resmi. Bila pengguna meminta lewat WA, beri versi WA singkat (fakta, nominal, tenggat) **plus** saran melampirkan/mengirim surat resminya — jangan menjadikan WA panjang sebagai pengganti surat.
   - **Lampiran:** jangan menulis "kami lampirkan surat/invoice/bukti" kecuali pengguna menyebut file itu ada dan akan ia sertakan. Kamu tidak membuat PDF/file. Bila surat resmi disarankan, tulis di pesan `[lampirkan: surat pemberitahuan — simpan/ekspor sebagai PDF dulu]` dan beri catatan di luar blok pesan, dalam bahasa biasa: "Surat resminya perlu Anda simpan sebagai PDF lalu Anda lampirkan sendiri." Catatan untuk pemilik taruh **di luar** blok pesan yang akan disalin ke debitur.
   - Agent tidak mengirim pesan ke debitur; pengguna yang mengirim sendiri. Jangan menawarkan "saya kirimkan langsung".
4. **Surat teguran (tahap 6)**: format surat resmi, fakta kronologis (tanggal invoice, jatuh tempo, pengingat yang sudah dikirim, pembayaran sebagian), jumlah yang harus dibayar, tenggat, rekening, dan langkah lanjutan yang sah ("menempuh upaya hukum sesuai peraturan yang berlaku"). Tanda tangan pemilik/direktur. Tambahkan disclaimer di bawah hasil.
5. **Beri saran tindakan** untuk pengguna: kapan tahap berikutnya dikirim, simpan bukti, tawarkan cicilan tertulis (surat kesepakatan cicilan/pengakuan utang adalah surat perjanjian/pernyataan → bermeterai Rp10.000 **berapa pun nilainya**; kuitansi pelunasan bermeterai bila > Rp5.000.000), kapan ke advokat/gugatan sederhana. Untuk layanan langganan yang masih berjalan (katering, jasa bulanan), jangan hentikan layanan sepihak tanpa pemberitahuan tertulis lebih dulu.
6. **Periksa** dengan checklist.

### Fallback jika Python tidak bisa dijalankan
Hitung manual, tulis langkahnya, dan beri tahu pengguna "dihitung manual, mohon dicek":
- Hari terlambat = tanggal hari ini − tanggal jatuh tempo (hari kalender). Sisa = nominal − total dibayar.
- Hari kena denda = hari terlambat − masa tenggang (minimal 0).
- Denda harian = sisa × persen × hari kena denda. Denda bulanan = sisa × persen × jumlah bulan (tiap 30 hari atau bagiannya = 1 bulan). Batasi dengan denda maksimal bila ada. Bulatkan ke rupiah terdekat.

## Format output
```
### Ringkasan tagihan
[Hasil script: sisa, jatuh tempo, hari terlambat, tahap, denda (jika ada, beserta dasarnya), total]

### Pesan tahap [N] · [WA/Email/Surat] · kirim [tanggal]
[isi siap kirim]

### Tahap berikutnya (jika belum dibayar)
- [salin kalimat `Jadwal` dari output script, mis. "Tenggat bayar di pesan ini: Kamis, 8 Oktober 2026 … pada Jumat, 9 Oktober 2026 kirim tahap 6."]

### Saran tindakan
- ...

### Catatan hukum
Bukan nasihat hukum. Dasar: KUHPerdata (wanprestasi/somasi)[, UU Bea Meterai bila menyarankan kesepakatan cicilan bermeterai] — per 2026-09-23. Untuk sengketa/gugatan, konsultasikan ke advokat.
```
Sebut UU ITE/UU PDP **hanya bila relevan** dan dengan alasannya dalam satu kalimat (mis. pengguna ingin menyebar nama debitur di grup/medsos atau mengancam lewat chat → "dilarang UU ITE Pasal 27A/27B dan UU PDP"). Jangan mencantumkannya sebagai "dasar" pesan tagihan biasa.
Bila pengguna minta "semua tahap sekaligus", tampilkan tahap 1–6 berurutan dengan tanggal kirim masing-masing (tanggal = jatuh tempo −3, 0, +3, +7, +14, +30).

## Contoh
**Input pengguna:** "Aku supplier kemasan 'Kemas Prima' di Tangerang. CV Sinar Abadi (Pak Hendra, bagian keuangan) invoice INV-0788 Rp 12.500.000, jatuh tempo 24 Agustus 2026, baru bayar 2,5 juta. Di PO ada denda 0,1% per hari setelah 3 hari, maks 5%. Sudah 2 kali kuingatkan lewat WA (26 Agustus & 7 September), nggak ada respons. Hari ini 23 September."

**Output (ringkas):** script (`--sudah-diingatkan 2`) → sisa Rp 10.000.000, terlambat 30 hari, tahap 6, denda Rp 270.000 (Rp 10.000.000 × 0,1% × 27 hari; dasar: PO), total Rp 10.270.000.
```
Nomor   : 015/KP/SP/IX/2026
Perihal : Surat Teguran Pembayaran Invoice INV-0788

Kepada Yth. Pimpinan CV Sinar Abadi
u.p. Bapak Hendra – Bagian Keuangan

Dengan hormat,
Berdasarkan Purchase Order yang telah disetujui, kami telah mengirimkan barang dan menerbitkan Invoice No. INV-0788 senilai Rp 12.500.000 dengan jatuh tempo 24 Agustus 2026. Hingga surat ini dibuat, kami telah menerima pembayaran sebesar Rp 2.500.000, sehingga masih terdapat sisa kewajiban Rp 10.000.000. Pengingat telah kami sampaikan pada 26 Agustus 2026 dan 7 September 2026 melalui WhatsApp.

Sesuai ketentuan keterlambatan pada PO (denda 0,1% per hari setelah masa tenggang 3 hari, maksimal 5%), denda per 23 September 2026 adalah Rp 270.000. Total yang perlu diselesaikan: Rp 10.270.000.

Kami meminta pembayaran tersebut diselesaikan paling lambat 30 September 2026 ke rekening [Bank – No. Rek – a.n. Kemas Prima]. Apabila terdapat kendala, kami terbuka untuk membahas jadwal pembayaran secara tertulis sebelum tanggal tersebut.

Apabila hingga batas waktu tersebut belum ada pembayaran maupun tanggapan, dengan menyesal kami akan menempuh langkah penyelesaian sesuai peraturan perundang-undangan yang berlaku.

Hormat kami,
[Nama] – Pemilik, Kemas Prima
```
Asumsi: tenggat 7 hari. (Jika pengguna belum pernah mengirim pengingat, script memberi tahap 5 — kirim pemberitahuan resmi dulu, bukan somasi.)

## Checklist sebelum mengirim hasil
- [ ] Nominal, hari terlambat, denda dari output script (atau hitung manual tertulis + peringatan).
- [ ] Denda hanya muncul jika ada dasar tertulis dan dasarnya disebut di pesan.
- [ ] Tidak ada ancaman kekerasan, ancaman menyebarkan/viralkan, hinaan, atau tekanan ke keluarga/atasan/rekan debitur.
- [ ] Tidak menyebarkan data/utang debitur ke pihak lain (grup, medsos, status WA).
- [ ] Bila ada permintaan untuk grup/tim: hanya blok "Ringkasan aman untuk grup" dari script yang disarankan ditempel.
- [ ] "Langkah hukum" hanya disebut umum dan benar ("sesuai peraturan yang berlaku"); tidak menyebut polisi/pidana untuk utang dagang biasa.
- [ ] Ada jalan keluar: konfirmasi bila sudah bayar, tawaran jadwal/cicilan.
- [ ] Nomor invoice, rekening, tenggat jelas; disclaimer ada di bawah hasil tahap 5–6.
- [ ] Rincian yang diberikan pengguna (per bulan/per invoice) tercantum di pesan.
- [ ] Jadwal tahap berikutnya = kalimat `Jadwal` dari script (hubungan dekat: jeda 14 hari).
- [ ] Tidak menawarkan mengirim pesan sendiri; tidak mencari file ke seluruh disk.
- [ ] Jawaban tidak memuat kata script/skill/file/folder/path/JSON atau nama berkas; tidak ada sapaan bergender untuk pengguna; debitur disapa sesuai yang diberikan pengguna atau "Bapak/Ibu".
- [ ] Bila output script berawal ⚠️: peringatan sudah disampaikan di awal jawaban dengan bahasa biasa.
- [ ] Info kurang: ada pekerjaan berguna dulu (templat), pertanyaan maksimal 3 dan di akhir.
- [ ] Permintaan yang ditolak: penolakan 1–2 kalimat, lalu bagian yang boleh langsung dikerjakan.
- [ ] Baris rekening ada di semua pesan; batas maksimal denda (bila ada) ditulis dalam rupiah.

## Batasan & penanganan error
- Bukan nasihat hukum. Somasi, gugatan (termasuk gugatan sederhana), dan penagihan lintas negara → advokat.
- Script tidak menghitung bunga moratoir menurut undang-undang, bunga berbunga, atau denda dengan dasar pembayaran bertanggal; jika diminta, jelaskan dan sarankan advokat/akuntan.
- Jika pengguna tidak punya bukti tertulis (invoice, PO, chat kesepakatan), sarankan mengumpulkan bukti dulu dan gunakan nada tahap 3–4 saja.
- File tidak terbaca (`.xls` lama, terkunci kata sandi, rusak) → script menulis `ERROR:` + minta CSV; sampaikan itu ke pengguna. Jangan mencari cara lain dengan menginstal paket.
- Jika debitur membantah tagihan (barang cacat, belum diterima), hentikan eskalasi; sarankan klarifikasi & rekonsiliasi dulu.
