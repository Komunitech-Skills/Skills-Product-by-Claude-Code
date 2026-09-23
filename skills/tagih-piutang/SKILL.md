---
name: tagih-piutang
description: Menyusun pesan penagihan piutang bertahap (WA/email/surat): pengingat sebelum jatuh tempo, hari H, lewat 7/14/30 hari, sampai surat teguran resmi (somasi), sopan tapi tegas tanpa ancaman ilegal atau mempermalukan; script menghitung hari terlambat, sisa, denda sesuai kesepakatan tertulis, dan umur piutang dari CSV. Gunakan saat pengguna minta nagih utang pelanggan, invoice belum dibayar, telat bayar, surat teguran pembayaran, debt collection, payment reminder, overdue invoice. Bukan untuk membuat invoice (buat-invoice) atau follow-up calon pembeli.
---

# Tagih Piutang

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
- Penagihan atas nama lembaga keuangan/pinjol/leasing (tunduk aturan OJK khusus), penagihan ke konsumen dengan jaminan fidusia, gugatan, atau pailit → jelaskan batasan, arahkan ke advokat.
- Permintaan pesan yang mengancam, mempermalukan (sebar di grup/medsos), menghubungi keluarga/atasan debitur untuk menekan, atau memakai kata kasar → **tolak bagian itu**, jelaskan risikonya (lihat `references/regulasi.md`), tawarkan alternatif yang sah.

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

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat, pakai default dan tulis "Asumsi" di akhir.

## Langkah kerja
1. **Hitung dengan script** (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/hitung_telat.py --nominal "Rp 12.500.000" --dibayar "Rp 2.500.000" \
     --jatuh-tempo 2026-08-24 --tanggal 2026-09-23
   ```
   - Denda **hanya** jika ada kesepakatan tertulis: tambahkan `--denda-persen 0,1 --denda-per hari` (atau `--denda-per bulan`, `--denda-tetap "Rp 100.000"`), `--tenggang 3`, `--denda-maks 5%`, dan `--dasar-denda "Pasal 4 Perjanjian No. ..."`. Jika script menulis PERINGATAN bahwa dasar denda kosong, jangan cantumkan denda di pesan sampai pengguna mengonfirmasi dasarnya.
   - Banyak tagihan: `--file piutang.csv` (kolom `pelanggan,no_invoice,nominal,jatuh_tempo,dibayar`) → rekap umur piutang + urutan prioritas penagihan.
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

   Jika debitur sudah memberi janji bayar, sesuaikan: tagih pada tanggal janji, rujuk janjinya secara faktual.
3. **Tulis pesan** sesuai tahap (contoh lengkap semua tahap + surat teguran: `references/template-penagihan.md`). Selalu cantumkan: nomor invoice, nominal sisa (dari script), tanggal jatuh tempo, rekening, cara konfirmasi. Tahap 1–3 tambahkan "Abaikan pesan ini jika sudah membayar".
4. **Surat teguran (tahap 6)**: format surat resmi, fakta kronologis (tanggal invoice, jatuh tempo, pengingat yang sudah dikirim, pembayaran sebagian), jumlah yang harus dibayar, tenggat, rekening, dan langkah lanjutan yang sah ("menempuh upaya hukum sesuai peraturan yang berlaku"). Tanda tangan pemilik/direktur. Tambahkan disclaimer di bawah hasil.
5. **Beri saran tindakan** untuk pengguna: kapan tahap berikutnya dikirim, simpan bukti, tawarkan cicilan tertulis (surat pengakuan utang > Rp5.000.000 perlu meterai Rp10.000), kapan ke advokat/gugatan sederhana.
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
- [tanggal] → tahap [N+1]: [ringkas]

### Saran tindakan
- ...

### Catatan hukum
Bukan nasihat hukum. Dasar: KUHPerdata (wanprestasi/somasi), UU ITE, UU PDP, UU Bea Meterai — per 2026-09-23. Untuk sengketa/gugatan, konsultasikan ke advokat.
```
Bila pengguna minta "semua tahap sekaligus", tampilkan tahap 1–6 berurutan dengan tanggal kirim masing-masing (tanggal = jatuh tempo −3, 0, +3, +7, +14, +30).

## Contoh
**Input pengguna:** "Aku supplier kemasan 'Kemas Prima' di Tangerang. CV Sinar Abadi (Pak Hendra, bagian keuangan) invoice INV-0788 Rp 12.500.000, jatuh tempo 24 Agustus 2026, baru bayar 2,5 juta. Di PO ada denda 0,1% per hari setelah 3 hari, maks 5%. Hari ini 23 September."

**Output (ringkas):** script → sisa Rp 10.000.000, terlambat 30 hari, tahap 6, denda Rp 270.000 (Rp 10.000.000 × 0,1% × 27 hari; dasar: PO), total Rp 10.270.000.
```
Nomor   : 015/KP/SP/IX/2026
Perihal : Surat Teguran Pembayaran Invoice INV-0788

Kepada Yth. Pimpinan CV Sinar Abadi
u.p. Bapak Hendra – Bagian Keuangan

Dengan hormat,
Berdasarkan Purchase Order yang telah disetujui, kami telah mengirimkan barang dan menerbitkan Invoice No. INV-0788 senilai Rp 12.500.000 dengan jatuh tempo 24 Agustus 2026. Hingga surat ini dibuat, kami telah menerima pembayaran sebesar Rp 2.500.000, sehingga masih terdapat sisa kewajiban Rp 10.000.000. Pengingat telah kami sampaikan pada [tanggal-tanggal pengingat].

Sesuai ketentuan keterlambatan pada PO (denda 0,1% per hari setelah masa tenggang 3 hari, maksimal 5%), denda per 23 September 2026 adalah Rp 270.000. Total yang perlu diselesaikan: Rp 10.270.000.

Kami meminta pembayaran tersebut diselesaikan paling lambat 30 September 2026 ke rekening [Bank – No. Rek – a.n. Kemas Prima]. Apabila terdapat kendala, kami terbuka untuk membahas jadwal pembayaran secara tertulis sebelum tanggal tersebut.

Apabila hingga batas waktu tersebut belum ada pembayaran maupun tanggapan, dengan menyesal kami akan menempuh langkah penyelesaian sesuai peraturan perundang-undangan yang berlaku.

Hormat kami,
[Nama] – Pemilik, Kemas Prima
```
Asumsi: tenggat 7 hari; pengingat sebelumnya perlu diisi tanggalnya oleh pengguna.

## Checklist sebelum mengirim hasil
- [ ] Nominal, hari terlambat, denda dari output script (atau hitung manual tertulis + peringatan).
- [ ] Denda hanya muncul jika ada dasar tertulis dan dasarnya disebut di pesan.
- [ ] Tidak ada ancaman kekerasan, ancaman menyebarkan/viralkan, hinaan, atau tekanan ke keluarga/atasan/rekan debitur.
- [ ] Tidak menyebarkan data/utang debitur ke pihak lain (grup, medsos, status WA).
- [ ] "Langkah hukum" hanya disebut umum dan benar ("sesuai peraturan yang berlaku"); tidak menyebut polisi/pidana untuk utang dagang biasa.
- [ ] Ada jalan keluar: konfirmasi bila sudah bayar, tawaran jadwal/cicilan.
- [ ] Nomor invoice, rekening, tenggat jelas; disclaimer ada di bawah hasil tahap 5–6.

## Batasan & penanganan error
- Bukan nasihat hukum. Somasi, gugatan (termasuk gugatan sederhana), dan penagihan lintas negara → advokat.
- Script tidak menghitung bunga moratoir menurut undang-undang, bunga berbunga, atau denda dengan dasar pembayaran bertanggal; jika diminta, jelaskan dan sarankan advokat/akuntan.
- Jika pengguna tidak punya bukti tertulis (invoice, PO, chat kesepakatan), sarankan mengumpulkan bukti dulu dan gunakan nada tahap 3–4 saja.
- Jika debitur membantah tagihan (barang cacat, belum diterima), hentikan eskalasi; sarankan klarifikasi & rekonsiliasi dulu.
